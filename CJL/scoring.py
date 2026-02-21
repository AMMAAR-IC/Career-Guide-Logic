"""
scoring.py
==========
Converts raw answers → normalized trait scores → career cluster probabilities.

Neural-network-style logic:
  Layer 0 : raw answers
  Layer 1 : normalised trait scores (APTITUDE, O, C, E, A, N, R, I, Art)
  Layer 2 : softmax-like activation → career cluster "neurons" fire
  Layer 3 : cross-trait synergy weights (e.g. high I + high C → Research)
  Output  : dict of career_cluster → probability %
"""

import math
from typing import Dict, List

# ─────────────────────────────────────────────────────────────────
# 1. PERSONALITY OPTION → SCORE MAPPING
# ─────────────────────────────────────────────────────────────────
OPTION_SCORE_POS = {"A": 2, "B": 1, "C": 0, "D": -1, "E": -2}
OPTION_SCORE_NEG = {"A": -2, "B": -1, "C": 0, "D": 1, "E": 2}

PERSONALITY_SECTIONS = {
    "OPENNESS", "CONSCIENTIOUSNESS", "EXTRAVERSION",
    "AGREEABLENESS", "NEUROTICISM",
    "REALISTIC", "INVESTIGATIVE", "ARTISTIC"
}

APTITUDE_SECTION = "APTITUDE"

# Per section: number of items and max possible score (items × 2)
SECTION_META = {
    "APTITUDE":          {"n": 40, "max": 40},   # 1 point per correct
    "OPENNESS":          {"n": 20, "max": 40},
    "CONSCIENTIOUSNESS": {"n": 20, "max": 40},
    "EXTRAVERSION":      {"n": 20, "max": 40},
    "AGREEABLENESS":     {"n": 20, "max": 40},
    "NEUROTICISM":       {"n": 20, "max": 40},
    "REALISTIC":         {"n": 20, "max": 40},
    "INVESTIGATIVE":     {"n": 20, "max": 40},
    "ARTISTIC":          {"n": 20, "max": 40},
}

# ─────────────────────────────────────────────────────────────────
# 2. CAREER CLUSTER DEFINITIONS
# Each cluster has:
#   - weights: how much each normalised trait (0-1) drives it
#   - threshold: minimum weighted sum to appear in results
# Traits: apt, O, C, E, A, N (inverted → stability), R, I, Art
# N is inverted: high neuroticism → low emotional stability
# ─────────────────────────────────────────────────────────────────
CAREER_CLUSTERS = {
    "STEM / Technology": {
        "weights": {"apt": 0.35, "I": 0.30, "C": 0.15, "O": 0.10, "E": 0.02, "A": 0.02, "stab": 0.03, "R": 0.03},
        "roles": ["Software Engineer", "Data Scientist", "AI Researcher", "Systems Analyst"]
    },
    "Engineering / Trades": {
        "weights": {"apt": 0.20, "R": 0.35, "I": 0.20, "C": 0.15, "O": 0.05, "E": 0.02, "A": 0.01, "stab": 0.02},
        "roles": ["Mechanical Engineer", "Electrician", "Civil Engineer", "Automotive Technician"]
    },
    "Science / Research": {
        "weights": {"apt": 0.25, "I": 0.35, "O": 0.20, "C": 0.12, "E": 0.02, "A": 0.03, "stab": 0.02, "R": 0.01},
        "roles": ["Biologist", "Chemist", "Physicist", "Epidemiologist"]
    },
    "Creative Arts & Design": {
        "weights": {"Art": 0.40, "O": 0.25, "E": 0.10, "C": 0.10, "apt": 0.05, "A": 0.05, "stab": 0.03, "I": 0.02},
        "roles": ["Graphic Designer", "UX Designer", "Film Director", "Musician", "Architect"]
    },
    "Business / Management": {
        "weights": {"apt": 0.20, "C": 0.25, "E": 0.20, "A": 0.10, "O": 0.10, "stab": 0.10, "I": 0.03, "R": 0.02},
        "roles": ["Business Analyst", "Project Manager", "Entrepreneur", "Operations Manager"]
    },
    "Healthcare / Medicine": {
        "weights": {"apt": 0.20, "I": 0.22, "A": 0.22, "C": 0.18, "stab": 0.12, "O": 0.03, "E": 0.02, "R": 0.01},
        "roles": ["Doctor", "Nurse", "Pharmacist", "Therapist", "Dentist"]
    },
    "Social Work / Counseling": {
        "weights": {"A": 0.38, "E": 0.20, "stab": 0.15, "O": 0.12, "C": 0.08, "apt": 0.04, "I": 0.02, "Art": 0.01},
        "roles": ["Social Worker", "Counselor", "Community Organizer", "School Counselor"]
    },
    "Education / Academia": {
        "weights": {"O": 0.22, "A": 0.20, "C": 0.18, "E": 0.15, "I": 0.12, "apt": 0.08, "stab": 0.04, "Art": 0.01},
        "roles": ["Teacher", "Professor", "Curriculum Designer", "Education Administrator"]
    },
    "Law / Policy": {
        "weights": {"apt": 0.25, "E": 0.20, "C": 0.18, "O": 0.15, "A": 0.10, "I": 0.07, "stab": 0.03, "Art": 0.02},
        "roles": ["Lawyer", "Judge", "Policy Analyst", "Public Administrator"]
    },
    "Finance / Economics": {
        "weights": {"apt": 0.35, "C": 0.25, "I": 0.20, "stab": 0.10, "O": 0.05, "E": 0.02, "A": 0.02, "R": 0.01},
        "roles": ["Accountant", "Financial Analyst", "Economist", "Actuary", "Investment Banker"]
    },
    "Communication / Media": {
        "weights": {"Art": 0.25, "E": 0.25, "O": 0.20, "A": 0.12, "C": 0.08, "stab": 0.05, "apt": 0.03, "I": 0.02},
        "roles": ["Journalist", "PR Specialist", "Content Creator", "Broadcaster", "Copywriter"]
    },
    "Sports / Physical Education": {
        "weights": {"R": 0.30, "E": 0.25, "stab": 0.20, "C": 0.12, "A": 0.08, "O": 0.03, "apt": 0.01, "I": 0.01},
        "roles": ["Athletic Trainer", "Sports Coach", "Physiotherapist", "PE Teacher"]
    },
    "Military / Law Enforcement": {
        "weights": {"R": 0.25, "C": 0.25, "stab": 0.25, "E": 0.10, "A": 0.08, "apt": 0.05, "O": 0.01, "I": 0.01},
        "roles": ["Police Officer", "Military Officer", "Border Security", "Firefighter"]
    },
    "Hospitality / Tourism": {
        "weights": {"E": 0.35, "A": 0.30, "O": 0.15, "C": 0.10, "stab": 0.07, "Art": 0.02, "apt": 0.01},
        "roles": ["Hotel Manager", "Tour Guide", "Chef", "Event Planner"]
    },
    "Environment / Agriculture": {
        "weights": {"R": 0.30, "I": 0.20, "O": 0.18, "C": 0.15, "A": 0.10, "stab": 0.04, "apt": 0.02, "E": 0.01},
        "roles": ["Environmental Scientist", "Agricultural Manager", "Park Ranger", "Forester"]
    },
}

# ─────────────────────────────────────────────────────────────────
# 3. CORE FUNCTIONS
# ─────────────────────────────────────────────────────────────────

def compute_raw_scores(questions: list, answers: Dict[int, str]) -> Dict[str, float]:
    """Return raw accumulated score per section."""
    scores = {s: 0.0 for s in SECTION_META}
    for q in questions:
        qid = q["id"]
        if qid not in answers:
            continue
        ans = answers[qid].upper()
        section = q["section"]
        if section == APTITUDE_SECTION:
            if ans == q.get("correct", ""):
                scores[section] += 1
        elif section in PERSONALITY_SECTIONS:
            polarity = q.get("polarity", "positive")
            mapping = OPTION_SCORE_POS if polarity == "positive" else OPTION_SCORE_NEG
            scores[section] += mapping.get(ans, 0)
    return scores


def normalise(raw: Dict[str, float]) -> Dict[str, float]:
    """
    Normalise each section raw score to [0, 1].
    Personality sections: raw min is -max, so shift and divide by 2*max.
    Aptitude: raw min is 0.
    """
    norm = {}
    for section, val in raw.items():
        meta = SECTION_META[section]
        mx = meta["max"]
        if section == APTITUDE_SECTION:
            norm[section] = max(0.0, min(1.0, val / mx))
        else:
            # raw in [-max, +max] → [0, 1]
            norm[section] = max(0.0, min(1.0, (val + mx) / (2 * mx)))
    return norm


def build_trait_vector(norm: Dict[str, float]) -> Dict[str, float]:
    """
    Map section normalised scores to trait keys used in cluster weights.
    Neuroticism is inverted → emotional stability (stab).
    """
    return {
        "apt":  norm.get("APTITUDE", 0.5),
        "O":    norm.get("OPENNESS", 0.5),
        "C":    norm.get("CONSCIENTIOUSNESS", 0.5),
        "E":    norm.get("EXTRAVERSION", 0.5),
        "A":    norm.get("AGREEABLENESS", 0.5),
        "stab": 1.0 - norm.get("NEUROTICISM", 0.5),   # inverted
        "R":    norm.get("REALISTIC", 0.5),
        "I":    norm.get("INVESTIGATIVE", 0.5),
        "Art":  norm.get("ARTISTIC", 0.5),
    }


def _sigmoid(x: float) -> float:
    """Squashes weighted sum into (0,1) – non-linear activation."""
    return 1.0 / (1.0 + math.exp(-12 * (x - 0.5)))


def _softmax(values: Dict[str, float]) -> Dict[str, float]:
    """Normalise across clusters so they sum to 100%."""
    exp_vals = {k: math.exp(v * 5) for k, v in values.items()}  # temperature=5
    total = sum(exp_vals.values()) or 1.0
    return {k: round(v / total * 100, 2) for k, v in exp_vals.items()}


def compute_cluster_scores(trait_vec: Dict[str, float]) -> Dict[str, float]:
    """
    Neural-network forward pass:
      weighted dot product → sigmoid → softmax across all clusters.
    """
    activations = {}
    for cluster, cfg in CAREER_CLUSTERS.items():
        w = cfg["weights"]
        dot = sum(w.get(t, 0) * trait_vec.get(t, 0.5) for t in w)
        activations[cluster] = _sigmoid(dot)
    return _softmax(activations)


def score_assessment(questions: list, answers: Dict[int, str]) -> Dict:
    """
    Full pipeline: answers → raw → norm → traits → cluster %.
    Returns structured dict ready for JSON serialisation.
    """
    raw   = compute_raw_scores(questions, answers)
    norm  = normalise(raw)
    traits = build_trait_vector(norm)
    probs  = compute_cluster_scores(traits)

    # Sort clusters by probability desc
    ranked = sorted(probs.items(), key=lambda x: x[1], reverse=True)

    return {
        "raw_scores":        raw,
        "normalised_traits": {
            "aptitude":           round(traits["apt"], 3),
            "openness":           round(traits["O"],   3),
            "conscientiousness":  round(traits["C"],   3),
            "extraversion":       round(traits["E"],   3),
            "agreeableness":      round(traits["A"],   3),
            "emotional_stability":round(traits["stab"],3),
            "realistic":          round(traits["R"],   3),
            "investigative":      round(traits["I"],   3),
            "artistic":           round(traits["Art"], 3),
        },
        "career_probabilities": {
            cluster: {
                "probability_pct": pct,
                "sample_roles": CAREER_CLUSTERS[cluster]["roles"]
            }
            for cluster, pct in ranked
        },
        "top_career_cluster": ranked[0][0] if ranked else None,
    }


# ─────────────────────────────────────────────────────────────────
# 4. ADAPTIVE QUESTION SELECTOR (the "15-20 questions" layer)
# ─────────────────────────────────────────────────────────────────
import random

def select_adaptive_questions(all_questions: list, n_per_section: dict = None) -> list:
    """
    Sample a balanced subset (~15-20 questions) from the full 200-question bank.
    Uses a stratified sampling approach, weighted toward high-discriminating
    sections (aptitude + 3 RIASEC types). 

    n_per_section defaults:
      APTITUDE: 3 (objective baseline)
      Each of 5 Big Five: 1
      Each of 3 RIASEC: 2  (most career-relevant)
    Total = 3 + 5 + 6 = 14, +2 random = 16 average
    """
    if n_per_section is None:
        n_per_section = {
            "APTITUDE":          3,
            "OPENNESS":          1,
            "CONSCIENTIOUSNESS": 2,
            "EXTRAVERSION":      1,
            "AGREEABLENESS":     1,
            "NEUROTICISM":       1,
            "REALISTIC":         2,
            "INVESTIGATIVE":     2,
            "ARTISTIC":          2,
        }

    by_section: Dict[str, list] = {}
    for q in all_questions:
        s = q["section"]
        by_section.setdefault(s, []).append(q)

    selected = []
    for section, count in n_per_section.items():
        pool = by_section.get(section, [])
        chosen = random.sample(pool, min(count, len(pool)))
        selected.extend(chosen)

    random.shuffle(selected)
    return selected
