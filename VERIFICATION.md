# Verification — current evidence
## Documentation audit, 5 November 2026
Read the live design, build, source notebook and seven data tabs. Updated content was read back. General guidance merged through BG-Prototypes PR #8. Current rules, sources, print inventory and Sol acceptance are consolidated.

## Print
The current 16-page kit is validated by print-and-play/verify_current.py. Its report covers source hashes, card counts, Letter geometry, both complete queues, 3 × 1 inch sections, 1-HP Recruits, map margins, holders and the two-row 0–20 VP track. Rendered previews are in print-and-play/current.

## Digital baseline for Sol
The last reported local run had 69 tests: 66 passed and three failed (two starting-hand expectations, one Recruit Poison expectation). The current target uses 2 starting tactics and 1-HP Recruits. Sol must establish a fresh runtime baseline and complete the checks in planning/build-spec-current.txt.

This documentation and print pass leaves runtime release verification to that plan. Required evidence includes rules/build/assets, paired seeded simulations, privacy/undo/replay, complete card-image coverage and browser review of opponent reveals at the specified sizes. Simulation completion measures implementation behavior; human balance needs playtesting.
Print rebuild on 5 November 2026: 154 checks passed. All sixteen rendered page previews were visually inspected; current output is 16 Letter pages.
