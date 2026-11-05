# Moonfall Tactics working instructions
Read START-HERE.md, ARCHITECTURE.md, SOURCE_AUDIT.md and DECISIONS.md. This dedicated repository owns the game.

The Design Draft owns rules, world, visual direction and the design notebook. The Build Specification owns the Sol plan and acceptance. The live spreadsheet owns hero identities, stats, prices, effects and availability. Read its Heroes, Regions and card tabs by stable ID/header before content changes; record source revisions and preserve designer edits. Keep Google files in the existing game folder and approved visual masters under assets/.

Use concise current-state prose, first-person hero effects and consistent icons. Generate actual card-face images for player decisions, with accessible transcriptions and separate controls/live state. Follow the current Build Specification for exact layout, palette, print dimensions and opponent-card reveals.

State and RNG serialize. UI, bots and tests share authoritative legal actions and player projections. Keep tunable values in src/data/config.ts and component data in snapshots. Record active TEST rulings in DECISIONS.md. Resolve routine implementation details within the authorized task and identify material rule contradictions precisely.

Inspect icons together at play size and in grayscale. Use shared frames, distinct silhouettes, pale matching colors and countable quantities. Review actual cards, board and queue together. Keep current documentation in place and use Git for revision history.

Run the checks appropriate to the change. Record actual rules, build, assets, simulation, browser and print evidence in VERIFICATION.md. Publish the authorized scope while preserving existing local work.
