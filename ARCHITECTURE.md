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

One shared tactic draw/discard supply serves private faction hands. State includes holder elements, AP/RAP, independent hero action counters, shared Recruit counters, status stacks, ongoing-effect flags, scenario modifiers and secured stones. Ongoing abilities use abilityActive with authored expiry at activation start or defeat.

Combat responses operate on committed combat tactics. Paid abilities resolve through resumable effects. Status stacks are captured at the roll boundary. Victory and settlement consequences resolve once.

The current configuration identifies card-images-v16; saves use schema 2 and require matching content version.

## Presentation status
Current local views use hero/tactic/objective card images and identity-correct watercolor portraits. Equipment uses generated complete image faces. Hands wrap, objectives remain visible, current choices sit above the chronological log, and dice have an animated click-to-roll control.

A shared generator and manifest supply 53 image faces across the in-use card families. Public plays drive a centered one-second opponent reveal and inspectable history. Asset validation checks the generated face hashes.

## Implemented 5 November 2026
The local runtime now uses content version card-images-v16, complete generated image faces for 53 cards, current triangle elements, duration-based abilityActive state, centered 1-second public opponent-card reveals and inspectable played-card history. Simulation reports individual heroes across varied legal rosters, game actions/turns/deaths and actual tactic receipts by source, with sample counts and intervals. Three/four-hero batches use their respective preparation budgets.
Validation: 71 tests pass; TypeScript/Vite build and 53-face hash validation pass. Fifty three-hero games and two four-hero games completed without stalls. Browser checks passed at 1366×768, 1920×1080 and 1024×768. Simulation-panel checks and the timed opponent reveal/history check passed. Desktop screenshots and representative card faces were visually inspected. These bot samples establish functioning reports and completion; sample size and teammate dependence remain visible in hero results.

The digital prototype uses the 2D SVG battlefield. Preserve readable hex positions, card inspection and current rules when extending the interface.
