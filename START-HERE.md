# Battlescrap

[Play Battlescrap](https://mbancha.github.io/Battlescrap/) · [Repository](https://github.com/mbancha/Battlescrap)

This standalone repository contains shared-elements-v15, current character art, tests and historical print sources. Its history was extracted from BG-Prototypes.

Clone this repository and run npm ci, then npm run dev -- --host 127.0.0.1 from its root folder. Open the local address printed by Vite. On Windows, npm.cmd may be needed.

The live Design Draft owns rules and art direction. The Build Specification owns digital instructions. The Battlescrap sheet owns character data. Their links are in README.md. Read live sources before content changes. Keep Google files in the existing game Drive folder.

Current masters and class-color metadata are in assets/heroes/current. Browser copies are in public/heroes-current. All fifteen characters have current art. Kalawi uses a provisional Striker/Scout art pairing because his regional class fields are blank.

Run npm test, npm run build, npm run assets, npm run sim and npm run smoke for relevant checks. Browser checks use installed Chrome or CHROMIUM_PATH. GitHub Actions publishes main to Pages. VERIFICATION.md records evidence and limitations. Existing print PDFs are historical revisions.
