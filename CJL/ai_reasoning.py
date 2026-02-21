"""
ai_reasoning.py
===============
Calls Ollama (Kimi K2 or any local model) to generate:
  1. Career reasoning narrative
  2. Roadmap steps (structured JSON inside the LLM response)
  3. Caveat / growth areas
"""

import json
import subprocess
import sys
from typing import Dict

DEFAULT_MODEL = "kimi-k2"   # change to any Ollama model you have pulled
FALLBACK_MODEL = "llama3"   # fallback if kimi-k2 isn't available


def _call_ollama(prompt: str, model: str = DEFAULT_MODEL) -> str:
    """
    Calls Ollama via its REST API (subprocess curl).
    Requires Ollama running: `ollama serve`
    """
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 1024
        }
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
            return _fallback_reasoning()

        resp = json.loads(result.stdout)
        return resp.get("response", "").strip()

    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        return _fallback_reasoning()


def _fallback_reasoning() -> str:
    """Returns a deterministic fallback when Ollama is unavailable."""
    return json.dumps({
        "narrative": (
            "Based on your assessment, your profile shows a distinctive blend of strengths. "
            "Your aptitude scores reveal analytical capacity, while your personality dimensions "
            "highlight how you naturally interact with work environments and people. "
            "The RIASEC profile pinpoints the type of activities that energise you most."
        ),
        "strengths": ["Analytical thinking", "Curiosity", "Reliability"],
        "growth_areas": ["Consider broadening interpersonal exposure", "Build on hands-on skills"],
        "roadmap": [
            {"step": 1, "title": "Self-exploration", "detail": "Research top roles in your career cluster via job boards and informational interviews."},
            {"step": 2, "title": "Skill gap analysis", "detail": "Identify 2-3 technical or soft-skill gaps compared to entry-level job descriptions."},
            {"step": 3, "title": "Targeted learning", "detail": "Enroll in a focused course (online or in-person) to address top gap."},
            {"step": 4, "title": "Portfolio / Experience", "detail": "Build a project, internship, or volunteer record in your target area."},
            {"step": 5, "title": "Network & apply", "detail": "Connect with 5 professionals in the field via LinkedIn and apply to 3+ positions."},
        ],
        "source": "fallback (Ollama unavailable)"
    })


def generate_reasoning(score_data: Dict) -> Dict:
    """
    Feeds normalised trait scores + top career cluster into Kimi K2
    and extracts structured JSON reasoning.
    """
    traits = score_data["normalised_traits"]
    top_cluster = score_data["top_career_cluster"]
    top_roles = score_data["career_probabilities"][top_cluster]["sample_roles"]
    top_pct = score_data["career_probabilities"][top_cluster]["probability_pct"]

    # Build top-5 cluster summary
    cluster_summary = "\n".join([
        f"  - {c}: {d['probability_pct']}%"
        for c, d in list(score_data["career_probabilities"].items())[:5]
    ])

    prompt = f"""You are an expert career counselor and psychometric analyst.

A person has completed a 200-question career assessment (Aptitude + Big Five + RIASEC).
Here are their normalised trait scores (0.0 = very low, 1.0 = very high):

Aptitude:             {traits['aptitude']}
Openness:             {traits['openness']}
Conscientiousness:    {traits['conscientiousness']}
Extraversion:         {traits['extraversion']}
Agreeableness:        {traits['agreeableness']}
Emotional Stability:  {traits['emotional_stability']}
Realistic:            {traits['realistic']}
Investigative:        {traits['investigative']}
Artistic:             {traits['artistic']}

Top Career Cluster: {top_cluster} ({top_pct}%)
Sample Roles: {', '.join(top_roles)}

Top 5 Career Clusters:
{cluster_summary}

Please provide a detailed analysis in STRICT JSON format with these keys:
{{
  "narrative": "<2-3 paragraph personalised explanation of why this career cluster fits>",
  "strengths": ["<strength 1>", "<strength 2>", "<strength 3>", "<strength 4>"],
  "growth_areas": ["<area 1>", "<area 2>", "<area 3>"],
  "why_top_cluster": "<1 paragraph specific reasoning>",
  "roadmap": [
    {{"step": 1, "title": "<action title>", "detail": "<specific action step>", "timeline": "<e.g. Week 1-2>"}},
    {{"step": 2, "title": "<action title>", "detail": "<specific action step>", "timeline": "<e.g. Month 1>"}},
    {{"step": 3, "title": "<action title>", "detail": "<specific action step>", "timeline": "<e.g. Month 2-3>"}},
    {{"step": 4, "title": "<action title>", "detail": "<specific action step>", "timeline": "<e.g. Month 3-6>"}},
    {{"step": 5, "title": "<action title>", "detail": "<specific action step>", "timeline": "<e.g. Month 6-12>"}},
    {{"step": 6, "title": "<action title>", "detail": "<specific action step>", "timeline": "<e.g. Year 1-2>"}}
  ],
  "alternative_paths": ["<alt cluster 1>", "<alt cluster 2>"],
  "key_insight": "<one powerful sentence summary>"
}}

Return ONLY valid JSON. No markdown. No extra text."""

    raw = _call_ollama(prompt)

    # Try to parse as JSON; if it fails, wrap in a result object
    try:
        parsed = json.loads(raw)
        parsed["source"] = "kimi-k2 (ollama)"
        return parsed
    except json.JSONDecodeError:
        # Try extracting JSON block from messy response
        try:
            start = raw.index("{")
            end   = raw.rindex("}") + 1
            parsed = json.loads(raw[start:end])
            parsed["source"] = "kimi-k2 (ollama, extracted)"
            return parsed
        except (ValueError, json.JSONDecodeError):
            fallback = json.loads(_fallback_reasoning())
            fallback["raw_llm_response"] = raw[:500]
            return fallback
