#!/usr/bin/env python3
"""
main.py  ─  Career Assessment CLI
===================================
Usage:
  python main.py                   → interactive adaptive quiz (15-20 Qs)
  python main.py --full            → all 200 questions
  python main.py --demo            → runs with random answers (for testing)
  python main.py --no-ai           → skip Ollama call, pure scoring output

Output: pretty JSON to stdout + saves result_{timestamp}.json
"""

import argparse
import json
import random
import sys
import os
from datetime import datetime

# ── local modules ──────────────────────────────────────────────────
from questions   import QUESTIONS
from scoring     import (select_adaptive_questions, score_assessment,
                         PERSONALITY_SECTIONS, APTITUDE_SECTION)
from ai_reasoning import generate_reasoning

# ──────────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────────

OPTION_LABELS = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E"}

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def print_banner():
    print("""
╔══════════════════════════════════════════════════════════╗
║          CAREER PATH ASSESSMENT SYSTEM v1.0              ║
║     Powered by Big Five + RIASEC + Aptitude + Kimi K2    ║
╚══════════════════════════════════════════════════════════╝
""")

def ask_question(q: dict, num: int, total: int) -> str:
    """
    Presents one question to the user and returns their answer letter.
    """
    section_label = q["section"].replace("_", " ").title()
    print(f"\n[{num}/{total}]  [{section_label}]")
    print(f"  {q['text']}\n")

    options = q["options"]
    for i, opt in enumerate(options):
        print(f"  {OPTION_LABELS[i]}) {opt}")

    while True:
        ans = input("\n  Your answer: ").strip().upper()
        if ans in [OPTION_LABELS[i] for i in range(len(options))]:
            return ans
        print("  ⚠  Please enter a valid option letter.")

def random_answer(q: dict) -> str:
    """For demo mode: returns a random valid answer."""
    return random.choice([OPTION_LABELS[i] for i in range(len(q["options"]))])

# ──────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────

def run(full_mode: bool = False, demo_mode: bool = False, no_ai: bool = False):
    print_banner()

    # ── Select questions ─────────────────────────────────────────
    if full_mode:
        quiz = QUESTIONS
        print(f"  Mode: FULL ASSESSMENT — {len(quiz)} questions\n")
    else:
        quiz = select_adaptive_questions(QUESTIONS)
        print(f"  Mode: ADAPTIVE ASSESSMENT — {len(quiz)} questions selected\n")

    if not demo_mode:
        print("  Instructions:")
        print("  • Aptitude Qs: choose the correct answer (A/B/C/D)")
        print("  • Personality / RIASEC Qs: A=Strongly Agree … E=Strongly Disagree")
        print("  • Answer honestly — there are no right/wrong personality answers\n")
        input("  Press ENTER to begin…")

    # ── Collect answers ──────────────────────────────────────────
    answers = {}
    for idx, q in enumerate(quiz, 1):
        if demo_mode:
            answers[q["id"]] = random_answer(q)
            # small visual feedback in demo mode
            if idx % 20 == 0 or idx == len(quiz):
                print(f"  Demo: answered {idx}/{len(quiz)} questions…")
        else:
            clear()
            print_banner()
            ans = ask_question(q, idx, len(quiz))
            answers[q["id"]] = ans

    # ── Score ────────────────────────────────────────────────────
    print("\n  Calculating your profile…")
    result = score_assessment(QUESTIONS, answers)  # always score against full bank

    # ── AI Reasoning ─────────────────────────────────────────────
    if no_ai:
        reasoning = {"note": "AI reasoning skipped (--no-ai flag)"}
    else:
        print("  Generating AI reasoning via Ollama (Kimi K2)…")
        reasoning = generate_reasoning(result)

    # ── Assemble final output ─────────────────────────────────────
    output = {
        "meta": {
            "timestamp":       datetime.now().isoformat(),
            "mode":            "full" if full_mode else "adaptive",
            "questions_asked": len(quiz),
            "total_bank":      len(QUESTIONS),
        },
        "profile":              result,
        "ai_analysis":          reasoning,
    }

    # ── Print ─────────────────────────────────────────────────────
    clear()
    print_banner()
    print("  ✅  ASSESSMENT COMPLETE\n")

    print("  ─── TRAIT SCORES (0.0 = low / 1.0 = high) ───────────────")
    for trait, val in result["normalised_traits"].items():
        bar_len = int(val * 30)
        bar = "█" * bar_len + "░" * (30 - bar_len)
        print(f"  {trait:<22} [{bar}]  {val:.2f}")

    print("\n  ─── TOP 5 CAREER CLUSTERS ────────────────────────────────")
    for i, (cluster, data) in enumerate(
            list(result["career_probabilities"].items())[:5], 1):
        pct = data["probability_pct"]
        bar = "█" * int(pct / 3.5) + "░" * (int(30 - pct / 3.5))
        print(f"  {i}. {cluster:<35} {pct:>5.1f}%  [{bar}]")
        print(f"     Roles: {', '.join(data['sample_roles'][:3])}")

    if not no_ai and "narrative" in reasoning:
        print("\n  ─── AI INSIGHT ───────────────────────────────────────────")
        print(f"  {reasoning.get('key_insight', '')}\n")
        if "roadmap" in reasoning:
            print("  ─── YOUR ROADMAP ─────────────────────────────────────────")
            for step in reasoning["roadmap"]:
                print(f"  Step {step['step']}  [{step.get('timeline','')}]  {step['title']}")
                print(f"         {step['detail']}")

    # ── Save JSON ─────────────────────────────────────────────────
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"result_{ts}.json"
    with open(filename, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\n  📄  Full JSON result saved → {filename}")
    print("=" * 62)

    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Career Assessment CLI")
    parser.add_argument("--full",  action="store_true", help="Run all 200 questions")
    parser.add_argument("--demo",  action="store_true", help="Auto-fill with random answers")
    parser.add_argument("--no-ai", action="store_true", help="Skip Ollama AI call")
    args = parser.parse_args()

    run(full_mode=args.full, demo_mode=args.demo, no_ai=args.no_ai)
