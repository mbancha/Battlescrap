# Moonfall Tactics
[Play](https://mbancha.github.io/Moonfall-Tactics/) · [Print and play](print-and-play/current/Moonfall-Tactics-print-and-play.pdf)

Tactical fantasy skirmishes on asymmetric hex maps, using a shared action queue and element tactics. Normal play fields three heroes and three 1-HP Recruits per faction; the shared-faction team test uses four heroes.

## Sources
- [Design Draft](https://docs.google.com/document/d/1PlwHc5BWQdSv77xgSlSmNEiZIhgJ40cii22NKibvcFM): current rules, quick sheet, scenarios, visual direction and design notebook.
- [Component sheet](https://docs.google.com/spreadsheets/d/1hfWFhxm-Su-qtR_hVrzFt6GBW1ure8W4xmp1o8hF-Rg/edit): hero and card definitions.
- [Sol Build Specification](https://docs.google.com/document/d/16-weAaDa4W7e4gC2jeiv_NN0cSAS_bcd_WATxPcDSAU): digital implementation plan and acceptance; [offline readback](planning/build-spec-current.txt).
- [Architecture](ARCHITECTURE.md), [active rulings](DECISIONS.md), [source audit](SOURCE_AUDIT.md) and [verification](VERIFICATION.md).

## Run and verify
Run npm ci, then npm run dev -- --host 127.0.0.1. On Windows use npm.cmd as needed.
Checks: npm test, npm run build, npm run assets, npm run sim, npm run smoke. Browser checks use installed Chrome or CHROMIUM_PATH.

## Print
The [16-page Letter kit](print-and-play/current/Moonfall-Tactics-print-and-play.pdf) includes current cards, map, both action queues, queue cards with VP track, standees, tokens and holders. [Print details](print-and-play/README.md).

The Sol plan brings the current local digital version into alignment with these components, including complete card-face images and a one-second central opponent-card reveal.
