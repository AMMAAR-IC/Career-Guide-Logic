#!/usr/bin/env python3
"""
run.py  ─  3-Stage Career Path Assessment
==========================================
Stage 1 : Broad Field Discovery        (~18 questions)
Stage 2 : Sub-Field Focus              (~15 questions)
Stage 3 : Specialization Pinpoint      (~12 questions)

Each stage is adaptive — questions are selected to maximise
discrimination based on the evolving trait profile.

Usage:
  python run.py                → full 3-stage interactive quiz
  python run.py --demo         → random answers (testing)
  python run.py --no-ai        → skip Ollama call
  python run.py --fast         → fewer questions per stage
"""

import argparse
import json
import random
import sys
import os
from datetime import datetime
from typing import Dict, List, Tuple

from engine           import (empty_traits, apply_answer, normalise_traits,
                               score_nodes, select_questions)
from taxonomy         import FIELDS, SUB_FIELDS, SPECIALIZATIONS
from stage_questions  import (STAGE1_QUESTIONS, STAGE2_QUESTIONS,
                               STAGE3_QUESTIONS)
from terminal_ui      import (show_banner, show_stage_header, ask_question,
                               show_interim_result, show_trait_panel,
                               show_final_summary, waiting_spinner,
                               cprint, hr, C)
from ai_reasoning     import generate_reasoning

# ─────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────
STAGE1_N  = 18   # questions for broad field
STAGE2_N  = 15   # questions for sub-field
STAGE3_N  = 12   # questions for specialization
FAST_MULT = 0.6  # question reduction in --fast mode


# ─────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────
def ranked_nodes(probs: Dict[str, float], taxonomy: dict) -> List[Tuple]:
    """Returns list of (name, pct, cfg) sorted descending by probability."""
    return sorted(
        [(name, pct, taxonomy[name]) for name, pct in probs.items()],
        key=lambda x: x[1], reverse=True
    )


def conduct_stage(stage: int, questions: List[dict], n: int,
                  trait_acc: Dict[str, float], used_ids: set,
                  demo: bool, field: str = "", subfield: str = "") -> Dict[str, float]:
    """
    Runs one assessment stage. Returns updated trait accumulator.
    """
    norm  = normalise_traits(trait_acc, max(len(used_ids), 1))
    pool  = select_questions(questions, n, used_ids, norm)

    for i, q in enumerate(pool, 1):
        show_stage_header(stage, field, subfield)
        ans = ask_question(q, i, len(pool), stage, demo)
        trait_acc = apply_answer(trait_acc, q, ans)
        used_ids.add(q["id"])

    return trait_acc


# ─────────────────────────────────────────────────────────────────
# MAIN FLOW
# ─────────────────────────────────────────────────────────────────
def run(demo: bool = False, no_ai: bool = False, fast: bool = False):

    n1 = max(6, int(STAGE1_N * (FAST_MULT if fast else 1)))
    n2 = max(5, int(STAGE2_N * (FAST_MULT if fast else 1)))
    n3 = max(4, int(STAGE3_N * (FAST_MULT if fast else 1)))

    show_banner()

    if not demo:
        cprint("\n  HOW IT WORKS", C.BYELLOW, bold=True)
        cprint("  ─────────────────────────────────────────────────────────", C.BBLACK)
        cprint("  Stage 1  ▸  Identify your broad career field", C.BWHITE)
        cprint("  Stage 2  ▸  Drill into the right sub-field within it", C.BWHITE)
        cprint("  Stage 3  ▸  Pinpoint your exact specialization", C.BWHITE)
        print()
        cprint("  For all questions, use the Likert scale:", C.BBLACK)
        cprint("  A = Strongly Agree   B = Agree   C = Neutral", C.BBLACK)
        cprint("  D = Disagree         E = Strongly Disagree", C.BBLACK)
        print()
        cprint("  Answer honestly. There are no right or wrong responses.", C.BYELLOW)
        hr()
        try:
            input(f"  {C.BCYAN}Press ENTER to begin your assessment…{C.RESET} ")
        except (EOFError, KeyboardInterrupt):
            sys.exit(0)

    traits   = empty_traits()
    used_ids = set()

    # ── STAGE 1 ─────────────────────────────────────────────────
    show_stage_header(1)
    traits = conduct_stage(1, STAGE1_QUESTIONS, n1, traits, used_ids, demo)

    waiting_spinner("Analysing your Stage 1 responses…", 1.2)

    norm1   = normalise_traits(traits, len(used_ids))
    probs1  = score_nodes(FIELDS, norm1)
    rank1   = ranked_nodes(probs1, FIELDS)

    show_interim_result(1, "BROAD FIELD DISCOVERY", rank1)

    top_field     = rank1[0][0]
    top_field_pct = rank1[0][1]

    cprint(f"  ✦  Your top field: {C.BYELLOW}{top_field}{C.RESET}  ({top_field_pct:.1f}%)", C.BWHITE, bold=True)
    print()
    hr()

    if not demo:
        try:
            input(f"  {C.BCYAN}Press ENTER to continue to Stage 2…{C.RESET} ")
        except (EOFError, KeyboardInterrupt):
            sys.exit(0)

    # ── STAGE 2 ─────────────────────────────────────────────────
    # Pull sub-field questions for the detected field
    s2_pool_key = top_field if top_field in STAGE2_QUESTIONS else random.choice(list(STAGE2_QUESTIONS.keys()))
    s2_pool     = STAGE2_QUESTIONS[s2_pool_key]
    sub_taxonomy = SUB_FIELDS.get(top_field, {})

    show_stage_header(2, field=top_field)
    traits = conduct_stage(2, s2_pool, n2, traits, used_ids, demo, field=top_field)

    waiting_spinner("Analysing your Stage 2 responses…", 1.2)

    norm2   = normalise_traits(traits, len(used_ids))
    if sub_taxonomy:
        probs2 = score_nodes(sub_taxonomy, norm2)
        rank2  = ranked_nodes(probs2, sub_taxonomy)
    else:
        # Fallback: reuse field probabilities
        rank2 = rank1

    show_interim_result(2, "SUB-FIELD FOCUS", rank2, context_field=top_field)

    top_sub     = rank2[0][0]
    top_sub_pct = rank2[0][1]

    cprint(f"  ✦  Your top sub-field: {C.BYELLOW}{top_sub}{C.RESET}  ({top_sub_pct:.1f}%)", C.BWHITE, bold=True)
    print()
    hr()

    if not demo:
        try:
            input(f"  {C.BCYAN}Press ENTER to continue to Stage 3…{C.RESET} ")
        except (EOFError, KeyboardInterrupt):
            sys.exit(0)

    # ── STAGE 3 ─────────────────────────────────────────────────
    # Pull specialization questions for detected sub-field
    spec_taxonomy = SPECIALIZATIONS.get(top_sub, SPECIALIZATIONS.get("_default_", {}))

    if top_sub in STAGE3_QUESTIONS:
        s3_pool = STAGE3_QUESTIONS[top_sub]
    else:
        s3_pool = STAGE3_QUESTIONS["_default_"]

    show_stage_header(3, field=top_field, subfield=top_sub)
    traits = conduct_stage(3, s3_pool, n3, traits, used_ids, demo,
                           field=top_field, subfield=top_sub)

    waiting_spinner("Running final analysis…", 1.5)

    norm3  = normalise_traits(traits, len(used_ids))
    if spec_taxonomy:
        probs3 = score_nodes(spec_taxonomy, norm3)
        rank3  = ranked_nodes(probs3, spec_taxonomy)
    else:
        rank3 = [("Core Practitioner", 100.0, {"description": "Main track", "tools": []})]

    show_interim_result(3, "SPECIALIZATION PINPOINT", rank3,
                        context_field=top_field, context_sub=top_sub)

    top_spec     = rank3[0][0]
    top_spec_pct = rank3[0][1]
    top_spec_cfg = rank3[0][2]

    cprint(f"  ✦  Your specialization: {C.BMAGENTA}{top_spec}{C.RESET}  ({top_spec_pct:.1f}%)", C.BWHITE, bold=True)
    print()
    hr()

    # ── AI REASONING ────────────────────────────────────────────
    ai_result = {}
    if not no_ai:
        if not demo:
            try:
                input(f"  {C.BCYAN}Press ENTER to generate your AI career insight…{C.RESET} ")
            except (EOFError, KeyboardInterrupt):
                sys.exit(0)
        waiting_spinner("Generating personalised AI analysis via Kimi K2…", 2.0)
        ai_result = generate_reasoning(
            field=top_field, subfield=top_sub, specialization=top_spec,
            field_pct=top_field_pct, sub_pct=top_sub_pct, spec_pct=top_spec_pct,
            norm_traits=norm3
        )

    # ── FINAL DISPLAY ────────────────────────────────────────────
    show_final_summary(
        field=top_field, subfield=top_sub, specialization=top_spec,
        field_pct=top_field_pct, sub_pct=top_sub_pct, spec_pct=top_spec_pct,
        spec_cfg=top_spec_cfg, norm_traits=norm3
    )

    # AI insight panel
    if ai_result:
        print()
        cprint("  ── AI CAREER INSIGHT  (Kimi K2) ──", C.BYELLOW, bold=True)
        print()

        narrative = ai_result.get("narrative", "")
        if narrative:
            cprint("  ANALYSIS", C.BCYAN, bold=True)
            # Word-wrap at ~75 chars
            words = narrative.split()
            line  = "  "
            for word in words:
                if len(line) + len(word) > 76:
                    print(f"{C.BWHITE}{line}{C.RESET}")
                    line = "  " + word + " "
                else:
                    line += word + " "
            if line.strip():
                print(f"{C.BWHITE}{line}{C.RESET}")
            print()

        why = ai_result.get("why_this_path", "")
        if why:
            cprint("  WHY THIS PATH", C.BCYAN, bold=True)
            words = why.split()
            line  = "  "
            for word in words:
                if len(line) + len(word) > 76:
                    print(f"{C.BBLACK}{line}{C.RESET}")
                    line = "  " + word + " "
                else:
                    line += word + " "
            if line.strip():
                print(f"{C.BBLACK}{line}{C.RESET}")
            print()

        strengths = ai_result.get("strengths", [])
        if strengths:
            cprint("  STRENGTHS", C.BCYAN, bold=True)
            for s in strengths:
                cprint(f"  {C.BGREEN}▶{C.RESET}  {s}", C.BWHITE)
            print()

        growth = ai_result.get("growth_areas", [])
        if growth:
            cprint("  GROWTH AREAS", C.BCYAN, bold=True)
            for g in growth:
                cprint(f"  {C.BYELLOW}◆{C.RESET}  {g}", C.BBLACK)
            print()

        insight = ai_result.get("key_insight", "")
        if insight:
            hr("─", C.BYELLOW)
            cprint(f"  KEY INSIGHT  ▸  {insight}", C.BYELLOW, bold=True)

    # ── SAVE JSON ─────────────────────────────────────────────────
    output = {
        "meta": {
            "timestamp":        datetime.now().isoformat(),
            "questions_asked":  len(used_ids),
            "demo_mode":        demo,
        },
        "results": {
            "stage_1": {
                "field":       top_field,
                "confidence":  top_field_pct,
                "all_fields":  {n: p for n, p, _ in rank1},
            },
            "stage_2": {
                "subfield":    top_sub,
                "confidence":  top_sub_pct,
                "all_subfields": {n: p for n, p, _ in rank2},
            },
            "stage_3": {
                "specialization": top_spec,
                "confidence":     top_spec_pct,
                "tools":          top_spec_cfg.get("tools", []),
                "all_specs":      {n: p for n, p, _ in rank3},
            },
        },
        "trait_profile": norm3,
        "ai_analysis":   ai_result,
    }

    ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"career_result_{ts}.json"
    with open(filename, "w") as f:
        json.dump(output, f, indent=2)

    print()
    hr("═", C.BYELLOW)
    cprint(f"  Full JSON result saved  ▸  {filename}", C.BBLACK)
    hr("═", C.BYELLOW)
    print()

    return output


# ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="3-Stage Career Assessment")
    parser.add_argument("--demo",  action="store_true", help="Random auto-fill (testing)")
    parser.add_argument("--no-ai", action="store_true", help="Skip Ollama AI analysis")
    parser.add_argument("--fast",  action="store_true", help="Fewer questions per stage")
    args = parser.parse_args()

    run(demo=args.demo, no_ai=args.no_ai, fast=args.fast)
