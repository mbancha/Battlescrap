# Verification — card-images-v16

72 tests passed, including deterministic replay, privacy, source-attributed draws, repeated defeat counting and completed-game report denominators. Production TypeScript/Vite build and validation of 53 complete card-face hashes passed.

Fifty paired three-hero matches and two four-hero matches completed without stalls. The three-hero batch averaged 15.96 faction turns, 102.34 gameplay actions, 5.84 hero defeats, 5.32 Recruit defeats and 14.56 earned tactics. This is a bot-policy sample across varied teams; the report presents sample counts and confidence intervals per hero.

Browser journeys passed at 1366×768, 1920×1080 and 1024×768. The simulation dashboard displayed hero-only results and game/source averages. The opponent-card image appeared centrally for approximately one second and remained inspectable in public history. Screenshots and generated equipment/card faces were visually inspected. Physical touch-device and independent unfamiliar-player sessions are playtest follow-up.

The current print kit passes 154 checks, with all sixteen rendered pages visually reviewed. The print generator and browser faces share current data and visual assets.

## Independent implementation audit — 5 November 2026

Reviewed the live Design Draft, Build Specification and all seven component-sheet tables against the release checkout, rules engine, UI, simulation code, asset pipeline, tests and publication workflow. GitHub main was f71bb8a4ea596acc5c2eddbe1b3b5be9d267b002. The live site's index-DKXEdcxz.js and index-Fe6H8fYL.css references matched a fresh build of that checkout. The release checkout is publish-queue; standalone has older Git history and extensive pre-existing edits. Those edits were preserved. Audit fixes below are local and have not been published.

### Reproduced defects and local corrections

- High: clicking New game and Begin scenario during a dice animation let the old delayed callback overwrite the new game. The new browser regression failed with battle instead of bid. Dice now commit once immediately; only presentation is timed, further actions wait for the animation, and navigation clears presentation state. The regression passes and is included in npm run smoke.
- Medium: paired simulations swapped rosters and zone preferences simultaneously, keeping each roster on the same deployment side twice. A new test reproduced stone versus stone. Pairing now swaps each roster's deployment side; simulation policyVersion is 2. Previous balance reports should be rerun before using them to justify balance changes.
- Medium: Bisti's granted Vital Dart attack did not increment freeAttacks. A new engine fixture reproduced the missing count; the committed cardTarget action now records it separately from the paid ability activation.
- Medium: in-game help incorrectly said Cancel interrupts paid abilities, described all four elements in normal games, and generalized ongoing durations. Corrected to the live rules. Preparation now explains random element assignment.
- Reveal presentation now consumes newly committed public-card events. Privacy handoff and match replacement clear inspection state so a previous view cannot reopen its tooltip afterward.

### Fresh evidence

- Baseline: 72 tests passed; production build and existing 53-face validator passed. These did not detect the defects above.
- Corrected code: 74 tests passed, TypeScript/Vite build passed, existing asset validator passed, and git diff --check passed.
- Corrected simulations: 10/10 three-hero and 2/2 four-hero games completed without errors or command-limit exits. Raw reports are artifacts/audit-simulation-3.json and artifacts/audit-simulation-4.json (ignored local evidence). These are flow checks, not statistically adequate balance conclusions.
- Browser: existing journeys passed at 1366x768, 1920x1080 and 1024x768; the dice/new-game regression passed; dedicated opponent reveal timing and persistent history check passed. Browser execution required permission to access the local preview server after sandbox networking denied the first attempt.
- Live sheet comparison: Regions, Tactics, Objectives, Equipment, Battlefield modifiers and Scenarios matched the print snapshot cell-for-cell after trimming whitespace. Heroes differed only in ten starter Regional ability cells: live blank versus stored None. Runtime Heroes/Regions and tactic snapshots matched print data. No gameplay data edits were needed.
- Visually inspected the 1366px full-hand screenshot. Images load and hands wrap, but board scale and pale labels need further attention. This audit did not regenerate or independently certify the historical 16-page print kit.

### Remaining acceptance gaps

1. Asset validation is weaker than the Build Specification: scripts/validate-card-assets.mjs hashes existing manifest entries but does not check an expected card census, source revisions/hashes, transcription completeness, actual image dimensions or the approved palette. The generator has no source-drift fingerprint. A changed rule or removed manifest entry can leave validation green. Hash success is not evidence that card faces match current rules.
2. Visual/interaction acceptance is incomplete. The 1366px screenshot renders the battlefield very small inside a wide panel; objective eligibility and some card availability labels have weak contrast. Recruit upgrade purchase buttons still use text even though reminder faces exist. Objective/equipment inspection does not provide the same enlargement controls as tactic hands. Full keyboard/touch and contrast acceptance remains open.
3. Simulations do not meaningfully exercise equipment purchasing: the bot scores ready above buy/upgrade/equip. Small batches also traverse roster combinations in order, leaving some heroes unrepresented. Report sample counts honestly; completion alone does not establish equipment balance or even hero coverage.
4. Browser checks are absent from the Pages workflow, which runs tests/build/assets only. Existing smoke/reveal scripts hardcode a Windows Chrome path; the new audit check honors CHROMIUM_PATH. Portable browser CI and broader save/import/hotseat acceptance remain follow-up.
5. Source-of-truth maintenance is incomplete: equipment/objectives are hand-authored again in src/content.ts, rather than consumed from the shared sheet snapshot. The live Build Specification also retains obsolete baseline/future-work wording alongside its completion appendix. The standalone-versus-publish-queue ownership ambiguity should be resolved before the next implementation handoff, without discarding standalone edits.

The audit establishes specific defects and working checks, not exhaustive absence of bugs. Remaining gaps above are recorded for follow-up rather than represented as completed acceptance.

## 6 November 2026 — Shields/class update
Preserved the audit fixes in publish-queue. Live Heroes sheet read back after HP, PP, Shield and keyword updates. Added primary-class Shields/Fly/basic Heavy Attack; Pierce skips Shields and Fortified; only sixes after the first add damage. Content version shields-v17 rejects prior saves. TEST budgets 21/28.
80 tests pass, production build passes, 53 card faces regenerated, source dependency and raster dimension validation passes, 154 print checks pass, 16-page kit regenerated. Browser smoke at 1366/1920/1024 and dice/new-game regression passed with local server access. Four seeded simulations completed; no balance claim. Hester face visually inspected.
Remaining audit-plan work: full sheet-owned card compiler and variables/styles/assets tabs, real Dextrous import/export pilot, full source-census/mutation tests, equipment-buying simulation coverage and complete mobile/200% zoom accessibility matrix. Dextrous CSV exports are preliminary, not proof of imported layout.

6 November 2026 — restored the 2D SVG presentation as the active digital prototype. All current rules, prices, HP, Shields, Pierce, Fly, Heavy Attack and 21/28 PP budgets are preserved. Verification: 80 tests, production build, 53 card-face checks, browser journeys at 1366×768, 1920×1080 and 1024×768, and dice/new-game regression pass.
