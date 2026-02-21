"""
engine.py
=========
Three-stage scoring engine.
Each stage:
  1. Asks targeted questions
  2. Combines with accumulated trait vector from ALL prior answers
  3. Applies weighted dot-product → sigmoid → softmax
  4. Returns ranked candidates for that stage's taxonomy level
"""

import math
import random
from typing import Dict, List, Tuple

# ─────────────────────────────────────────────────────────────────
# BASE TRAIT VECTOR  (accumulates across all 3 stages)
# ─────────────────────────────────────────────────────────────────
TRAIT_KEYS = ["apt", "O", "C", "E", "A", "stab", "R", "I", "Art"]

def empty_traits() -> Dict[str, float]:
    return {k: 0.0 for k in TRAIT_KEYS}


# ─────────────────────────────────────────────────────────────────
# ANSWER → TRAIT DELTA
# All stage 1/2/3 questions are positive-polarity Likert.
# A=SA=+2, B=A=+1, C=N=0, D=D=-1, E=SD=-2
# Then multiplied by each trait's weight in the question definition.
# ─────────────────────────────────────────────────────────────────
LIKERT_MAP = {"A": 2, "B": 1, "C": 0, "D": -1, "E": -2}


def apply_answer(traits: Dict[str, float], question: dict, answer: str) -> Dict[str, float]:
    """
    Adds weighted answer delta to the running trait accumulator.
    Returns updated trait dict (immutable pattern — returns new dict).
    """
    delta = LIKERT_MAP.get(answer.upper(), 0)
    updated = dict(traits)
    for trait, weight in question.get("traits", {}).items():
        if trait in updated:
            updated[trait] += delta * weight
    return updated


# ─────────────────────────────────────────────────────────────────
# NORMALISE accumulated traits
# Each trait's raw range depends on how many questions contribute.
# We use a running zscore-like clamped normalisation.
# ─────────────────────────────────────────────────────────────────
def normalise_traits(raw: Dict[str, float],
                     n_questions: int,
                     max_weight: float = 2.0) -> Dict[str, float]:
    """
    Normalise raw accumulated traits to [0, 1].
    Theoretical max per trait ≈ n_questions * max_weight * 2 (SA score)
    Theoretical min per trait ≈ n_questions * max_weight * -2 (SD score)
    We use a generous bound and clamp.
    """
    bound = max(n_questions * max_weight * 2, 1.0)
    return {k: max(0.0, min(1.0, (v + bound) / (2 * bound)))
            for k, v in raw.items()}


# ─────────────────────────────────────────────────────────────────
# NEURAL-NET FORWARD PASS
# ─────────────────────────────────────────────────────────────────
def _sigmoid(x: float, sharpness: float = 10.0) -> float:
    """Steep sigmoid — makes the model decisive rather than mushy."""
    try:
        return 1.0 / (1.0 + math.exp(-sharpness * (x - 0.5)))
    except OverflowError:
        return 0.0 if x < 0.5 else 1.0


def _softmax(scores: Dict[str, float], temperature: float = 4.0) -> Dict[str, float]:
    """
    Softmax with temperature.
    Higher temperature → more spread; lower → winner takes more.
    """
    exp_vals = {}
    for k, v in scores.items():
        try:
            exp_vals[k] = math.exp(v * temperature)
        except OverflowError:
            exp_vals[k] = float("inf")

    total = sum(exp_vals.values()) or 1.0
    # Handle inf
    inf_keys = [k for k, v in exp_vals.items() if v == float("inf")]
    if inf_keys:
        share = 100.0 / len(inf_keys)
        return {k: (share if k in inf_keys else 0.0) for k in scores}

    return {k: round(v / total * 100, 2) for k, v in exp_vals.items()}


def score_nodes(nodes: dict, norm_traits: Dict[str, float]) -> Dict[str, float]:
    """
    Forward pass for a set of taxonomy nodes (fields, sub-fields, or specs).
    Each node has trait_weights.
    Returns softmax'd probability dict.
    """
    activations = {}
    for name, cfg in nodes.items():
        weights = cfg.get("trait_weights", {})
        dot = sum(weights.get(t, 0.0) * norm_traits.get(t, 0.5) for t in weights)
        activations[name] = _sigmoid(dot)
    return _softmax(activations)


# ─────────────────────────────────────────────────────────────────
# ADAPTIVE QUESTION SELECTION
# Selects N questions from a pool, avoiding repeats.
# For Stage 2/3: optionally biases toward high-signal questions
# that best discriminate the current candidate set.
# ─────────────────────────────────────────────────────────────────
def select_questions(pool: List[dict],
                     n: int,
                     used_ids: set,
                     norm_traits: Dict[str, float] = None) -> List[dict]:
    """
    Adaptive stratified sample.
    If norm_traits is provided, reorders pool to maximise informativeness:
    a question is more informative if its trait vector is most orthogonal
    to the current trait vector (i.e. fills knowledge gaps).
    """
    available = [q for q in pool if q["id"] not in used_ids]

    if norm_traits:
        def informativeness(q: dict) -> float:
            """
            Score = how much this question would reduce uncertainty.
            Questions targeting traits with extreme (near 0 or 1) scores
            are less informative. Questions targeting mid-range traits (≈0.5)
            are most informative.
            """
            score = 0.0
            for trait, w in q.get("traits", {}).items():
                current = norm_traits.get(trait, 0.5)
                uncertainty = 1.0 - abs(current - 0.5) * 2  # max at 0.5
                score += uncertainty * w
            return score

        available.sort(key=informativeness, reverse=True)
        # Take top 2*n then shuffle to introduce variety
        top = available[:min(2 * n, len(available))]
        random.shuffle(top)
        return top[:n]
    else:
        random.shuffle(available)
        return available[:n]


# ─────────────────────────────────────────────────────────────────
# BIG FIVE APTITUDE PRIOR  (from original 200-Q bank, if used)
# ─────────────────────────────────────────────────────────────────
def traits_from_bigfive_bank(questions: list,
                              answers: Dict[int, str]) -> Dict[str, float]:
    """
    Convert Big Five + RIASEC + Aptitude bank answers into trait vector.
    Used to seed Stage 1 if the full 200-Q bank was already answered.
    """
    # Import here to avoid circular
    from scoring import (compute_raw_scores, normalise,
                         build_trait_vector, SECTION_META)
    raw  = compute_raw_scores(questions, answers)
    norm = normalise(raw)
    tv   = build_trait_vector(norm)
    # Remap keys
    return {
        "apt":  tv["apt"],
        "O":    tv["O"],
        "C":    tv["C"],
        "E":    tv["E"],
        "A":    tv["A"],
        "stab": tv["stab"],
        "R":    tv["R"],
        "I":    tv["I"],
        "Art":  tv["Art"],
    }
