#!/usr/bin/env python3
# Authored rehearsal budget. The notes are cues, not a verbatim transcript.
# Seconds include slide explanation, short prediction/reveal pauses and demo work.
SLIDE_SECONDS = [
    45,  # 1 title / thesis
    60,  # 2 handwritten baseline
    65,  # 3 language family
    55,  # 4 options
    80,  # 5 choices become coupled
    65,  # 6 ownership
    90,  # 7 UTL2002 prediction
    80,  # 8 routes
    75,  # 9 LanguagePlan
    75,  # 10 staging boundary
    120, # 11 source-backed demo
    65,  # 12 causal bridge
    120, # 13 semantic prediction
    110, # 14 capability prediction
    90,  # 15 two scales / boundaries
    70,  # 16 final decision rule
]
HARD_CONTENT_LIMIT = 25 * 60
OFFICIAL_QA = 5 * 60
DEMO_SECONDS = SLIDE_SECONDS[10]
INTERACTION_SECONDS = 50  # included inside slides 7, 13, 14

total = sum(SLIDE_SECONDS)
buffer = HARD_CONTENT_LIMIT - total

assert len(SLIDE_SECONDS) == 16
assert 19 * 60 <= total <= 22 * 60, f"talk target drift: {total}s"
assert DEMO_SECONDS <= 120, f"demo budget too large: {DEMO_SECONDS}s"
assert INTERACTION_SECONDS <= 60, f"interaction budget too large: {INTERACTION_SECONDS}s"
assert buffer >= 3 * 60, f"hard-stop buffer too small: {buffer}s"

def mmss(seconds: int) -> str:
    return f"{seconds // 60:02d}:{seconds % 60:02d}"

print(f"talk target: {mmss(total)}")
print(f"demo inside talk: {mmss(DEMO_SECONDS)}")
print(f"prediction/reveal allowance inside talk: {mmss(INTERACTION_SECONDS)}")
print(f"buffer before 25:00 hard content limit: {mmss(buffer)}")
print(f"official Q&A window: {mmss(OFFICIAL_QA)}")
print("Timing audit PASS")
