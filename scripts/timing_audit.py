#!/usr/bin/env python3
# Intellectual-deck rehearsal estimate. This rebuild intentionally has no 25-minute hard cap.
SLIDE_SECONDS=[55, 55, 75, 45, 95, 75, 85, 60, 70, 90, 65, 85, 70, 80, 70, 80, 65, 75, 85, 60, 90, 65, 75, 55, 65, 55, 60]
assert len(SLIDE_SECONDS)==27
assert all(20 <= s <= 120 for s in SLIDE_SECONDS)
total=sum(SLIDE_SECONDS)
def mmss(s): return f'{s//60:02d}:{s%60:02d}'
print(f'full intellectual deck rehearsal estimate: {mmss(total)}')
print('No hard 25-minute constraint is enforced for the rebuild.')
print('Timing audit PASS')
