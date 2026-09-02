#!/usr/bin/env python3
# Authored rehearsal budget. Seconds include explanation, pauses and demo work.
SLIDE_SECONDS = [
    45,  # 1 title / question / anchor
    75,  # 2 handwritten baseline
    75,  # 3 language family / why extensibility
    80,  # 4 coupling threshold
    75,  # 5 ownership + canonical configuration model
    85,  # 6 pipeline becomes a transformation graph
    100, # 7 automatic route search + truth boundaries
    75,  # 8 LanguageCompiler naming + immutable LanguagePlan
    75,  # 9 authoring/planning/materialization/source-build lifecycle
    110, # 10 source-backed route-changing demo
    85,  # 11 two once boundaries
    80,  # 12 Evaluate vs Compile boundary
    85,  # 13 full extensibility cost / measurement boundary
    95,  # 14 strongest counterargument / when not to use planner
    60,  # 15 final anchor
]
HARD_CONTENT_LIMIT = 25 * 60
OFFICIAL_QA = 5 * 60
DEMO_SECONDS = SLIDE_SECONDS[9]
INTERACTION_SECONDS = 20

total = sum(SLIDE_SECONDS)
buffer = HARD_CONTENT_LIMIT - total

assert len(SLIDE_SECONDS) == 15
assert 19 * 60 <= total <= 21 * 60, f"talk target drift: {total}s"
assert DEMO_SECONDS <= 120, f"demo budget too large: {DEMO_SECONDS}s"
assert INTERACTION_SECONDS <= 60, f"interaction budget too large: {INTERACTION_SECONDS}s"
assert buffer >= 3 * 60, f"hard-stop buffer too small: {buffer}s"


def mmss(seconds: int) -> str:
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


print(f"talk target: {mmss(total)}")
print(f"demo inside talk: {mmss(DEMO_SECONDS)}")
print(f"interaction allowance inside talk: {mmss(INTERACTION_SECONDS)}")
print(f"buffer before 25:00 hard content limit: {mmss(buffer)}")
print(f"official Q&A window: {mmss(OFFICIAL_QA)}")
print("Timing audit PASS")
