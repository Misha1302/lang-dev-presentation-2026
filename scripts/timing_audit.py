#!/usr/bin/env python3
# Authored rehearsal budget. Seconds include explanation, pauses and demo work.
SLIDE_SECONDS = [
    45,   # 1 official title + architecture memory
    70,   # 2 explicit handwritten baseline
    75,   # 3 concrete pricing-restricted language
    80,   # 4 Wist source -> Bytecode -> AIR -> interpreter/CIL
    120,  # 5 parity boundary + source-backed demo beat
    80,   # 6 cross-owner correctness threshold
    80,   # 7 current UT staging
    110,  # 8 current conversion-first/pass-second planner limitation
    90,   # 9 proposed feasibility-before-preference model
    80,   # 10 current LanguagePlan vs proposed planner evidence
    75,   # 11 freeze boundary / make abstractions disappear
    80,   # 12 cost + performance evidence boundary
    90,   # 13 strongest counterargument / prior-art boundary
    55,   # 14 final decision rule
]
HARD_CONTENT_LIMIT = 25 * 60
OFFICIAL_QA = 5 * 60
DEMO_SECONDS = 110
INTERACTION_SECONDS = 20

total = sum(SLIDE_SECONDS)
buffer = HARD_CONTENT_LIMIT - total

assert len(SLIDE_SECONDS) == 14
assert 18 * 60 <= total <= 20 * 60, f"talk target drift: {total}s"
assert DEMO_SECONDS <= 120, f"demo budget too large: {DEMO_SECONDS}s"
assert INTERACTION_SECONDS <= 60, f"interaction budget too large: {INTERACTION_SECONDS}s"
assert buffer >= 5 * 60, f"hard-stop buffer too small: {buffer}s"


def mmss(seconds: int) -> str:
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


print(f"talk target: {mmss(total)}")
print(f"demo inside talk: {mmss(DEMO_SECONDS)}")
print(f"interaction allowance inside talk: {mmss(INTERACTION_SECONDS)}")
print(f"buffer before 25:00 hard content limit: {mmss(buffer)}")
print(f"official Q&A window: {mmss(OFFICIAL_QA)}")
print("Timing audit PASS")
