"""
ai_reasoning.py  (v2 — 3-stage, no roadmap)
============================================
Calls Ollama (Kimi K2 or fallback) to generate career insight.
No roadmap — just deep narrative, strengths, growth areas.
"""

import json
import subprocess
from typing import Dict

DEFAULT_MODEL  = "kimi-k2"
FALLBACK_MODEL = "llama3"


def _call_ollama(prompt: str, model: str = DEFAULT_MODEL) -> str:
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.65, "num_predict": 900}
    })
    try:
        result = subprocess.run(
            ["curl", "-s", "-X", "POST",
             "http://localhost:11434/api/generate",
             "-H", "Content-Type: application/json",
             "-d", payload],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode != 0 or not result.stdout.strip():
            return ""
        resp = json.loads(result.stdout)
        return resp.get("response", "").strip()
    except Exception:
        return ""


def _extract_json(raw: str) -> dict:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        try:
            s = raw.index("{"); e = raw.rindex("}") + 1
            return json.loads(raw[s:e])
        except Exception:
            return {}


def _fallback(field: str, subfield: str, spec: str, traits: dict) -> dict:
    return {
        "narrative": (
            f"Your assessment reveals a strong alignment with {spec} within {subfield} "
            f"({field}). Your investigative drive, combined with your aptitude scores, "
            f"suggests you are well-suited for analytical and problem-solving work in this domain. "
            f"Your personality profile shows a balance of curiosity and conscientiousness that "
            f"are key differentiators in this specialization."
        ),
        "why_this_path": (
            f"The convergence of your RIASEC profile, Big Five personality dimensions, "
            f"and aptitude scores consistently points toward {spec}. "
            f"Your strongest trait signals create a profile that fits the demands "
            f"and culture of this career path exceptionally well."
        ),
        "strengths": [
            "Strong analytical and pattern-recognition capacity",
            "Ability to sustain focus on complex problems",
            "Curiosity-driven learning mindset",
            "Structured approach to tasks and deliverables",
        ],
        "growth_areas": [
            "Broaden exposure to adjacent disciplines for cross-functional thinking",
            "Invest in communication skills to articulate technical ideas clearly",
            "Seek collaborative experiences to complement independent work style",
        ],
        "key_insight": (
            f"You are built for {spec} — trust the data and your instincts equally."
        ),
        "source": "fallback (Ollama unavailable)",
    }


def generate_reasoning(field: str, subfield: str, specialization: str,
                        field_pct: float, sub_pct: float, spec_pct: float,
                        norm_traits: Dict[str, float]) -> Dict:

    traits_str = "\n".join(
        f"  {k:<24}: {v:.3f}" for k, v in norm_traits.items()
    )

    prompt = f"""You are a world-class career counselor and psychometric expert.

A person has completed a 3-stage adaptive career assessment.

=== RESULTS ===
Stage 1  Broad Field     : {field}  ({field_pct:.1f}% match)
Stage 2  Sub-Field       : {subfield}  ({sub_pct:.1f}% match)
Stage 3  Specialization  : {specialization}  ({spec_pct:.1f}% match)

=== TRAIT PROFILE (0.0 = very low, 1.0 = very high) ===
{traits_str}

Your task: Write a deep, personalised career analysis in STRICT JSON format.
Return ONLY valid JSON — no markdown, no preamble, no trailing text.

{{
  "narrative": "<3-4 sentences: why this career path uniquely fits this person>",
  "why_this_path": "<2-3 sentences: specific trait combinations that drove the result>",
  "strengths": ["<strength 1>", "<strength 2>", "<strength 3>", "<strength 4>"],
  "growth_areas": ["<growth area 1>", "<growth area 2>", "<growth area 3>"],
  "key_insight": "<One powerful sentence — the most important thing to know>"
}}"""

    raw = _call_ollama(prompt)
    if not raw:
        raw = _call_ollama(prompt, FALLBACK_MODEL)

    result = _extract_json(raw)
    if not result or "narrative" not in result:
        result = _fallback(field, subfield, specialization, norm_traits)
    else:
        result["source"] = "kimi-k2 (ollama)"

    return result
