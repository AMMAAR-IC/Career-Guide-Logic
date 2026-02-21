"""
terminal_ui.py
==============
All terminal rendering: banners, progress bars, question display,
results panels. No external dependencies — pure ANSI escape codes.
"""

import os
import sys
import time
import shutil
from typing import Dict

# ─────────────────────────────────────────────────────────────────
# ANSI COLOUR CODES
# ─────────────────────────────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    ITALIC  = "\033[3m"

    # Foreground
    BLACK   = "\033[30m"
    RED     = "\033[31m"
    GREEN   = "\033[32m"
    YELLOW  = "\033[33m"
    BLUE    = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN    = "\033[36m"
    WHITE   = "\033[37m"

    # Bright foreground
    BBLACK  = "\033[90m"
    BRED    = "\033[91m"
    BGREEN  = "\033[92m"
    BYELLOW = "\033[93m"
    BBLUE   = "\033[94m"
    BMAGENTA= "\033[95m"
    BCYAN   = "\033[96m"
    BWHITE  = "\033[97m"

    # Background
    BG_BLACK  = "\033[40m"
    BG_BLUE   = "\033[44m"
    BG_CYAN   = "\033[46m"
    BG_WHITE  = "\033[47m"


def cols() -> int:
    return shutil.get_terminal_size((80, 24)).columns


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def hr(char="─", color=C.BBLACK):
    print(f"{color}{char * cols()}{C.RESET}")


def cprint(text: str, color: str = C.RESET, bold: bool = False, center: bool = False):
    prefix = (C.BOLD if bold else "") + color
    if center:
        text = text.center(cols())
    print(f"{prefix}{text}{C.RESET}")


# ─────────────────────────────────────────────────────────────────
# BANNER
# ─────────────────────────────────────────────────────────────────
BANNER = r"""
  ██████╗ █████╗ ██████╗ ███████╗███████╗██████╗
 ██╔════╝██╔══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗
 ██║     ███████║██████╔╝█████╗  █████╗  ██████╔╝
 ██║     ██╔══██║██╔══██╗██╔══╝  ██╔══╝  ██╔══██╗
 ╚██████╗██║  ██║██║  ██║███████╗███████╗██║  ██║
  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝
     ██████╗ █████╗ ████████╗██╗  ██╗
    ██╔══██╗██╔══██╗╚══██╔══╝██║  ██║
    ██████╔╝███████║   ██║   ███████║
    ██╔═══╝ ██╔══██║   ██║   ██╔══██║
    ██║     ██║  ██║   ██║   ██║  ██║
    ╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝
"""

SUBTITLE = "  Powered by Aptitude · Big Five · RIASEC · Kimi K2"


def show_banner():
    clear()
    cprint(BANNER, C.BCYAN)
    cprint(SUBTITLE, C.BBLACK, center=True)
    hr()


# ─────────────────────────────────────────────────────────────────
# STAGE HEADER
# ─────────────────────────────────────────────────────────────────
STAGE_COLORS = {1: C.BCYAN, 2: C.BBLUE, 3: C.BMAGENTA}
STAGE_NAMES  = {
    1: "STAGE 1  ·  BROAD FIELD DISCOVERY",
    2: "STAGE 2  ·  SUB-FIELD FOCUS",
    3: "STAGE 3  ·  SPECIALIZATION PINPOINT",
}


def show_stage_header(stage: int, field: str = "", subfield: str = ""):
    clear()
    cprint(BANNER, C.BCYAN)
    color = STAGE_COLORS.get(stage, C.BWHITE)
    cprint(f"\n  {STAGE_NAMES[stage]}", color, bold=True)
    if field:
        cprint(f"  Field    ▸  {field}", C.BWHITE)
    if subfield:
        cprint(f"  Sub-field ▸  {subfield}", C.BYELLOW)
    hr()


# ─────────────────────────────────────────────────────────────────
# PROGRESS BAR
# ─────────────────────────────────────────────────────────────────
def progress_bar(current: int, total: int, label: str = "") -> str:
    pct = current / max(total, 1)
    width = min(40, cols() - 30)
    filled = int(pct * width)
    bar = "█" * filled + "░" * (width - filled)
    return (f"  {C.BBLACK}[{C.BCYAN}{bar}{C.BBLACK}]{C.RESET}"
            f"  {C.BWHITE}{current}/{total}{C.RESET}"
            f"  {C.BBLACK}{label}{C.RESET}")


# ─────────────────────────────────────────────────────────────────
# QUESTION DISPLAY
# ─────────────────────────────────────────────────────────────────
OPTION_KEYS   = ["A", "B", "C", "D", "E"]
LIKERT_LABELS = [
    "Strongly Agree",
    "Agree",
    "Neutral",
    "Disagree",
    "Strongly Disagree",
]
LIKERT_COLORS = [C.BGREEN, C.GREEN, C.BBLACK, C.YELLOW, C.BRED]


def ask_question(q: dict, num: int, total: int, stage: int,
                 demo: bool = False) -> str:
    """
    Renders a question and returns the chosen letter.
    """
    section = q.get("section", q.get("id", "")[:4])
    color   = STAGE_COLORS.get(stage, C.BWHITE)

    print()
    print(progress_bar(num, total))
    print()
    print(f"  {C.BBLACK}Q{num}  {color}▸{C.RESET}  {C.BWHITE}{C.BOLD}{q['text']}{C.RESET}")
    print()

    options = q.get("options", LIKERT_LABELS)
    for i, opt in enumerate(options):
        key   = OPTION_KEYS[i]
        lcol  = LIKERT_COLORS[i] if len(options) == 5 else C.BWHITE
        print(f"    {C.BOLD}{lcol}{key}{C.RESET}  {C.BBLACK}│{C.RESET}  {opt}")

    print()

    if demo:
        import random
        ans = random.choice(OPTION_KEYS[:len(options)])
        print(f"  {C.BBLACK}[demo] → {ans}{C.RESET}")
        return ans

    while True:
        try:
            raw = input(f"  {C.BCYAN}→{C.RESET} ").strip().upper()
        except (EOFError, KeyboardInterrupt):
            print("\n  Exiting.")
            sys.exit(0)
        if raw in OPTION_KEYS[:len(options)]:
            return raw
        cprint(f"  ⚠  Enter one of: {', '.join(OPTION_KEYS[:len(options)])}", C.BRED)


# ─────────────────────────────────────────────────────────────────
# RESULTS DISPLAY
# ─────────────────────────────────────────────────────────────────
RANK_COLORS = [C.BYELLOW, C.BWHITE, C.BBLACK, C.BBLACK, C.BBLACK]
RANK_PREFIX = ["  ★ 1st", "    2nd", "    3rd", "    4th", "    5th"]


def show_interim_result(stage: int, title: str, ranked: list,
                        context_field: str = "", context_sub: str = ""):
    """
    Displays ranked results after each stage.
    ranked = list of (name, probability_pct, cfg_dict) sorted desc.
    """
    clear()
    cprint(BANNER, C.BCYAN)
    color = STAGE_COLORS.get(stage, C.BWHITE)

    label = {1: "BROAD FIELD RESULT", 2: "SUB-FIELD RESULT", 3: "SPECIALIZATION RESULT"}[stage]
    cprint(f"\n  ╔══ {label} ══", color, bold=True)

    if context_field:
        cprint(f"  ║  Field     ▸  {context_field}", C.BWHITE)
    if context_sub:
        cprint(f"  ║  Sub-field ▸  {context_sub}", C.BYELLOW)
    cprint(f"  ╚{'═' * (cols() - 4)}", color)
    print()

    bar_max = 42

    for i, (name, pct, cfg) in enumerate(ranked[:5]):
        rcol   = RANK_COLORS[i]
        prefix = RANK_PREFIX[i]
        bar_len = int(pct / 100 * bar_max)
        bar = "█" * bar_len + "░" * (bar_max - bar_len)

        print(f"  {rcol}{C.BOLD}{prefix}{C.RESET}  "
              f"{rcol}{name:<40}{C.RESET}  "
              f"{C.BYELLOW}{pct:>5.1f}%{C.RESET}")
        print(f"          {C.BBLACK}[{C.BCYAN}{bar}{C.BBLACK}]{C.RESET}")

        desc = cfg.get("description", "")
        if desc:
            cprint(f"          {desc}", C.BBLACK)

        # Tools if available (stage 3)
        tools = cfg.get("tools", [])
        if tools:
            cprint(f"          Tools: {' · '.join(tools[:4])}", C.BBLACK)
        print()

    hr()


def show_trait_panel(norm_traits: Dict, label: str = "YOUR TRAIT PROFILE"):
    """
    Displays the current accumulated trait scores as horizontal bars.
    """
    TRAIT_DISPLAY = {
        "apt":  ("Aptitude",            C.BCYAN),
        "O":    ("Openness",            C.BBLUE),
        "C":    ("Conscientiousness",   C.BBLUE),
        "E":    ("Extraversion",        C.BBLUE),
        "A":    ("Agreeableness",       C.BBLUE),
        "stab": ("Emotional Stability", C.BBLUE),
        "R":    ("Realistic",           C.BGREEN),
        "I":    ("Investigative",       C.BGREEN),
        "Art":  ("Artistic",            C.BMAGENTA),
    }

    print()
    cprint(f"  ── {label} ──", C.BBLACK)
    print()
    bar_max = 30

    for key, (name, color) in TRAIT_DISPLAY.items():
        val = norm_traits.get(key, 0.5)
        bar_len = int(val * bar_max)
        bar = "█" * bar_len + "░" * (bar_max - bar_len)
        tier = ("▼ Low" if val < 0.35 else "◆ Mid" if val < 0.65 else "▲ High")
        tier_c = C.BRED if val < 0.35 else (C.BYELLOW if val < 0.65 else C.BGREEN)

        print(f"  {color}{name:<24}{C.RESET}"
              f"  {C.BBLACK}[{C.CYAN}{bar}{C.BBLACK}]{C.RESET}"
              f"  {C.BBLACK}{val:.2f}{C.RESET}"
              f"  {tier_c}{tier}{C.RESET}")
    print()
    hr()


def show_final_summary(field: str, subfield: str, specialization: str,
                        field_pct: float, sub_pct: float, spec_pct: float,
                        spec_cfg: dict, norm_traits: dict):
    """
    Full-screen final results panel.
    """
    clear()
    cprint(BANNER, C.BCYAN)
    print()
    hr("═", C.BYELLOW)
    cprint("  ✦  CAREER PATH ASSESSMENT COMPLETE  ✦", C.BYELLOW, bold=True, center=True)
    hr("═", C.BYELLOW)
    print()

    cprint(f"  {'STAGE 1  BROAD FIELD':<30}  {field}", C.BCYAN, bold=True)
    cprint(f"  {'':30}  {C.BBLACK}Confidence: {field_pct:.1f}%{C.RESET}", C.RESET)
    print()
    cprint(f"  {'STAGE 2  SUB-FIELD':<30}  {subfield}", C.BBLUE, bold=True)
    cprint(f"  {'':30}  {C.BBLACK}Confidence: {sub_pct:.1f}%{C.RESET}", C.RESET)
    print()
    cprint(f"  {'STAGE 3  SPECIALIZATION':<30}  {specialization}", C.BMAGENTA, bold=True)
    cprint(f"  {'':30}  {C.BBLACK}Confidence: {spec_pct:.1f}%{C.RESET}", C.RESET)
    print()

    desc = spec_cfg.get("description", "")
    if desc:
        print(f"  {C.BBLACK}What this means:{C.RESET}")
        print(f"  {C.BWHITE}{desc}{C.RESET}")
        print()

    tools = spec_cfg.get("tools", [])
    if tools:
        print(f"  {C.BBLACK}Key tools & technologies:{C.RESET}")
        print(f"  {C.BYELLOW}{' · '.join(tools)}{C.RESET}")
        print()

    hr("─", C.BBLACK)
    show_trait_panel(norm_traits, "FINAL TRAIT PROFILE")


def waiting_spinner(msg: str, secs: float = 1.5):
    frames = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    end = time.time() + secs
    i = 0
    while time.time() < end:
        sys.stdout.write(f"\r  {C.BCYAN}{frames[i % len(frames)]}{C.RESET}  {msg}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write("\r" + " " * (len(msg) + 10) + "\r")
    sys.stdout.flush()



