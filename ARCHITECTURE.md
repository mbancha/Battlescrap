# Moonfall Tactics implementation map
Local code inspected 5 November 2026. The [Build Specification](planning/build-spec-current.txt) owns the target and release gates.

## Modules
- src/data/config.ts: budgets, queues, shared elements, reward defaults and modifiers.
- src/data/hero-snapshot.json and tactics.json: header-based content snapshots.
- src/content.ts: component definitions, equipment, upgrades, objectives and full-hex map geometry.
- src/engine.ts: serializable state/RNG, legal actions, setup, AP/RAP, combat, effect queues, statuses, terrain, rewards, projections, bots and replay.
- src/icons.tsx: digital symbol renderer; src/App.tsx and stylesheets: interaction, card views, inspection, log, dice and bot scheduling.
- print-and-play/build_current.py: current print layouts and native hero faces. scripts/build-card-faces.py invokes its character rebuild.
- scripts/: simulations, asset validation and browser checks.

## State and contracts
newGame and applyAction/dispatch expose the rules; legalActions/actions enumerate choices. The app validates a cloned state before committing. Seeded randomness and pending decisions remain in serializable state. Player projections govern hands, objectives, bids and public information.

One shared tactic draw/discard supply serves private faction hands. State includes holder elements, AP/RAP, independent hero action counters, shared Recruit counters, status stacks, ongoing-effect flags, scenario modifiers and secured stones. The current ongoing flag is u.tokens.ongoing; Sol's plan specifies the active-state migration.

Combat responses operate on committed combat tactics. Paid abilities resolve through resumable effects. Status stacks are captured at the roll boundary. Victory and settlement consequences resolve once.

The local configuration identifies shared-elements-v15; saves use schema 2. Versioning and migration acceptance are part of the next tested release.

## Presentation status
Current local views use hero/tactic/objective card images and identity-correct watercolor portraits. Equipment currently combines art with live text overlays. Hands wrap, objectives remain visible, current choices sit above the chronological log, and dice have an animated click-to-roll control.

The target is one manifest/generator for complete image faces across every in-use card family and a one-second central opponent-card reveal. The plan includes synchronizing the asset validator with the current triangle icons.
