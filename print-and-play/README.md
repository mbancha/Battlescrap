# Moonfall Tactics print and play
Current starter kit: **4 November 2026**. [Download the complete kit](current/Moonfall-Tactics-print-and-play.pdf) or [just the action tracks](current/06-action-queue.pdf).

Print **19 US Letter pages, single-sided, 100% / Actual size**. Enable automatic portrait/landscape rotation. Do not use Fit to page. The action-track page is landscape; both complete strips are on that single sheet.

## Components
- 3-page rules, assembly and scenario reference.
- Two **multirow 3-inch-section** tracks: six slots for 2 players; eight for 3-4 players sharing two factions.
- 10 poker-size hero cards, 10 compact 1.25 x 1.75 inch queue portraits, and 10 folding hero standees.
- 36 tactics: one shared deck, nine per element. Remove the omitted element for 2-player games (27 cards).
- 6 objectives, each awarding **1 VP + 1 tactic**. Start with **2 tactics** per faction.
- Ten tokens of each of five statuses, eight ability markers, four traps, seventeen Moonstones, nine identical setup-token backs and a VP track.
- Eight faction/element badges, two Recruit references, fourteen equipment/upgrade reminders, and the original map on two joined sheets.

Use compact queue portraits with these strips; the former wide holders do not fit eight across Letter. Place element badges beneath the portraits and match standee-base markings. Supply Recruit pieces (three per faction plus purchased extras), red damage cubes, dice and two VP markers. Opaque sleeves hide card backs. Print more status tokens as required.

The current Cancel cards follow the newer combat-only rule. The live sheet and runtime text still contain older ability-cancellation wording; this discrepancy is recorded in the [Sol plan](../planning/sol-update-2026-11-04.md). Unfinished regional heroes remain unavailable. Team setup and campaign income remain TEST.

## Rebuild and verify
From the repository root:
```powershell
python print-and-play/build_current.py
python print-and-play/verify_current.py
```

Requires Python with Pillow, ReportLab, pypdf, pypdfium2 and pdfplumber; the current font paths use Windows Georgia/Arial. Assets are under assets/print, assets/heroes/current, assets/equipment and assets/maps. source-snapshot.json is a dated readback of the single authoritative Google sheet, not a second editable design database. rules-current.txt is the print export of the existing rules document plus assembly instructions. Approved raster faces are verified against starter IDs and live gameplay fields; vector track labels remain sharp.

current/manifest.json records geometry and quantities; current/verification.json records automated checks. All 19 rendered pages were inspected. These checks do not certify runtime behavior or balance.

The old pdf/ directory, build.py and verify.py are **historical only** and must not be used to build or print the current game.

