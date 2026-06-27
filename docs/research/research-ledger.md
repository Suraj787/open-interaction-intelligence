# Research Ledger — Interface Intelligence OS

> The **core verified source set** behind IIOS. Per the
> [research methodology](./research-methodology.md), this is the 15–25 deeply-reviewed
> tier set — the only sources permitted to back a safety-affecting decision. The broader
> 50–100 candidate landscape lives in [`source-landscape.md`](./source-landscape.md) and
> `registry/sources/`.
>
> **Verification note.** Entries marked **verified (web, 2026‑06‑28)** were looked up at
> their official location during this research pass and the cited fact confirmed. Entries
> marked **carried (registry)** are reused from the foundation's own verification pass
> (recorded per-record under `evidence` in `registry/sources/*.json`); their homepages are
> known-good but the specific date below was not re-confirmed in this pass and is labelled
> accordingly. No entry is asserted as `verified` without a real lookup.

---

## How to read this table

- **Type** uses the source-hierarchy tiers from the methodology (1 = standards body … 9 = video).
- **Confidence** reflects how directly the source supports the claim IIOS uses it for.
- **Time-sensitivity**: `stable` / `slow` / `volatile` (volatile = re-check on a cadence).
- **Claims used** = the specific facts IIOS relies on, not a summary of the whole source.

---

## Core verified sources

| # | Title | Org / Source | Type (tier) | Date (source) | Claims IIOS uses | Confidence | Time-sens. | Verification | Link |
|--:|-------|--------------|-------------|---------------|------------------|:---------:|:----------:|--------------|------|
| 1 | WCAG 2.2 — "is a W3C Recommendation" | W3C / WAI | 1 — standard | Rec. 2023‑10‑05 (update 2024‑12‑12) | WCAG 2.2 is the current ratified standard; success-criteria set IIOS conformance checks map to | high | stable | verified (web, 2026‑06‑28) | https://www.w3.org/WAI/news/2023-10-05/wcag22rec/ |
| 2 | What's New in WCAG 2.2 | W3C / WAI | 1 — standard | 2023‑10 | The 9 new SC (e.g. target size, focus not obscured, dragging movements) the assurance engine should consider | high | stable | verified (web, 2026‑06‑28) | https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/ |
| 3 | "INP becomes a Core Web Vital on March 12" | web.dev (Chrome team) | 2 — official docs | 2024‑03‑12 | INP replaced FID as a Core Web Vital on 2024‑03‑12; "good" INP = ≤200 ms at p75 | high | volatile | verified (web, 2026‑06‑28) | https://web.dev/blog/inp-cwv-march-12 |
| 4 | The WebAIM Million — 2025 report | WebAIM (Utah State Univ.) | 5 — industry org | 2025 | 94.8% of top‑1M home pages had detected WCAG failures; low-contrast text most common (79.1%); ~51 errors/page avg | high | volatile | verified (web, 2026‑06‑28) | https://webaim.org/projects/million/2025 |
| 5 | axe-core (accessibility engine) | Deque Systems | 3 — official repo | 4.x (2024+) | axe-core detects "up to ~57%" of WCAG issues automatically; flags "incomplete" needing manual review; licensed MPL‑2.0; ~90 rules; covers WCAG 2.0/2.1/2.2 A–AAA | high | volatile | verified (web, 2026‑06‑28) | https://github.com/dequelabs/axe-core |
| 6 | Design Tokens Format Module | Design Tokens Community Group (W3C CG) | 2 — official spec | First stable 2025‑10 | Vendor-neutral token format IIOS design-intelligence data aligns to; Colour/Motion/Typography modules in progress | high | volatile | verified (web, 2026‑06‑28) | https://www.designtokens.org/ |
| 7 | 10 Usability Heuristics for UI Design | Nielsen Norman Group | 5 — industry org | 1994, rev. 2020/2024 | The 10 heuristics IIOS UX-principle checks reference (visibility of status, error prevention, recognition over recall, etc.) | high | stable | verified (web, 2026‑06‑28) | https://www.nngroup.com/articles/ten-usability-heuristics/ |
| 8 | MDN Web Docs — Web platform reference | Mozilla | 2 — official docs | continuously updated | Browser-native API behaviour (View Transitions, Web Animations, Intersection/Resize Observer, scroll-driven animations) IIOS prefers before libraries | high | slow | carried (registry) + spot web check | https://developer.mozilla.org/ |
| 9 | Radix UI Primitives | WorkOS / Radix | 3 — official repo/docs | active | Accessible unstyled primitives; MIT; reference model for IIOS accessible-foundation tier | high | slow | carried (registry) | https://www.radix-ui.com |
| 10 | React Aria | Adobe | 3 — official repo/docs | active | ARIA-pattern behaviour + accessibility hooks; Apache‑2.0; authoritative interaction/a11y behaviour reference | high | slow | carried (registry) | https://react-spectrum.adobe.com/react-aria |
| 11 | Material Design 3 | Google | 2 — vendor docs | M3 (active) | Design-system guidance, motion/elevation/colour systems; **guidance is reference-only** (CC‑BY/Google terms), code separate | medium | slow | carried (registry) | https://m3.material.io |
| 12 | IBM Carbon Design System | IBM | 2/3 — vendor docs + repo | active | Enterprise design-system patterns & tokens; Apache‑2.0 code (`adaptable-concept`) | medium | slow | carried (registry) | https://carbondesignsystem.com |
| 13 | Microsoft Fluent 2 | Microsoft | 2/3 — vendor docs + repo | active | Cross-platform design-system guidance; MIT Fluent UI code, guidance is Microsoft's | medium | slow | carried (registry) | https://fluent2.microsoft.design |
| 14 | Shopify Polaris | Shopify | 2/3 — vendor docs + repo | active | Product-admin patterns; **modified-MIT with field-of-use restriction** — key example for the licence gate | high | slow | carried (registry) | https://polaris.shopify.com |
| 15 | GitHub Primer | GitHub | 2/3 — vendor docs + repo | active | Design-system patterns/tokens; MIT code, GitHub brand reserved | medium | slow | carried (registry) | https://primer.style |
| 16 | Storybook — Accessibility & Interaction tests | Storybook (maintained OSS) | 2/3 — official docs | active | a11y addon built on axe-core (~57% coverage); play-function interaction tests — model for IIOS assurance integration | high | slow | verified (web, 2026‑06‑28) | https://storybook.js.org/docs/writing-tests/accessibility-testing |
| 17 | Claude Code — Subagents | Anthropic | 2 — official docs | 2025+ | Subagent/skill mechanics IIOS's specialist-agent + orchestrator layer targets | high | volatile | verified (web, 2026‑06‑28) | https://docs.anthropic.com/en/docs/claude-code/sub-agents |

> 17 core sources spanning standards (1–2), performance (3), empirical accessibility
> evidence (4), tooling (5, 16), tokens (6), usability theory (7), the web platform (8),
> accessible foundations (9–10), enterprise design systems (11–15), and the agent runtime
> (17). This sits inside the methodology's 15–25 target band.

---

## Volatile facts to re-check

These carry a re-check cadence because the underlying source moves:

- **INP threshold / Core Web Vitals composition** (#3) — Chrome may revise thresholds or
  metrics; re-check at the start of each release cycle.
- **WebAIM Million figure** (#4) — annual report; refresh the 94.8% figure each year
  (2026 report already exists at the project root URL).
- **axe-core coverage / rule count / version** (#5) — moves per release.
- **DTCG spec stability** (#6) — modules (Colour/Motion/Typography) are still landing.
- **Claude Code skills/subagents** (#17) — runtime semantics evolve; re-confirm per release.

## Notes on honesty

- Where a date column says "active" rather than a specific date, the source is
  continuously updated and pinning a single date would be misleading.
- "carried (registry)" entries are trustworthy for their licence/redistribution
  disposition (the foundation confirmed those at official locations) but were not
  re-fetched in this pass; they are not upgraded to "verified (web, 2026‑06‑28)".
- Any source that could not be confirmed at an official location is **not** in this
  ledger; it stays in `registry/sources/` as `pending-verification`.
