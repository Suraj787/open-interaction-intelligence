# Source Landscape — Interface Intelligence OS

> The **candidate set** in the evidence-based release model
> ([methodology](./research-methodology.md)): the 50–100 effect/component/knowledge
> sources that map where UI interaction, motion, components and design judgment actually
> come from. **~90 of these are already catalogued** as machine-readable records in
> [`registry/sources/`](../../registry/sources) (one JSON per source, validated against
> `schemas/source.schema.json`); this document is the human-readable grouping and the
> governance reading of that registry.
>
> The smaller, deeply-verified **core set** (15–25) that may back safety decisions is the
> [research ledger](./research-ledger.md). This landscape is for discovery and reference,
> not for un-reviewed installation: anything not yet confirmed stays
> `pending-verification` and is excluded from approved-installation flows.

---

## How the landscape is governed

Each source record carries `redistribution` — the disposition that controls how IIOS may
use it:

- **`redistributable`** — permissive licence confirmed; code may be adapted and bundled.
- **`adaptable-concept`** — learn from it, re-implement clean-room; do not copy verbatim
  (e.g. copyleft, restricted design-system code/assets, GSAP's custom terms).
- **`reference-only`** — inspiration or unverified/unknown licence; never bundled.
- **`rejected`** — fails the licence or security gate.

Galleries are `reference-only` **by default**. Public visibility is never redistribution
permission. (See [problem P6](./problem-evidence.md).)

---

## Categories (the `source.schema.json` `category` enum)

Counts below reflect the current `registry/sources/` catalogue (~90 records). Treat them as
the live count's snapshot, not a fixed number.

### 1. Accessible UI foundations
The most important tier for IIOS: unstyled, behaviour-correct primitives.
**Radix UI · React Aria · Ark UI · Base UI · Bits UI · Headless UI · Melt UI · Reka UI ·
shadcn/ui · shadcn-vue.** Mostly MIT/Apache‑2.0 → `redistributable`. Radix and React Aria
are core-ledger sources ([#9, #10](./research-ledger.md)).

### 2. Browser-native capabilities
Preferred before any library (cheapest, most accessible, no supply-chain cost).
**CSS Transitions / Animations / Scroll-driven Animations · Web Animations API ·
View Transitions API · Intersection Observer · Resize Observer · Pointer Events ·
SVG (SMIL+CSS) · Canvas 2D · WebGL · WebGPU.** Browser standards → `redistributable`,
documented via MDN ([ledger #8](./research-ledger.md)).

### 3. Animation engines
**Motion (Framer Motion) · Motion for Vue · @vueuse/motion · Svelte Motion · react-spring ·
Anime.js · AutoAnimate · Theatre.js (Apache core) · GSAP.** Mostly MIT → `redistributable`;
**GSAP** uses a custom "now free" standard licence → `adaptable-concept` (not SPDX-permissive).

### 4. Scrolling & transitions
**Lenis · Locomotive Scroll · AOS · Barba.js · Swup · GSAP ScrollTrigger · ScrollReveal.**
Mostly MIT; **ScrollReveal is GPL‑3.0 / dual-licensed → `reference-only`**; ScrollTrigger
inherits GSAP terms → `adaptable-concept`. A worked example of why per-source licence
reading matters.

### 5. Canvas / particles / generative
**PixiJS · Konva · Fabric.js · Paper.js · tsParticles · Vanta.js · regl · OGL (Unlicense) ·
p5.js.** Mostly MIT → `redistributable`; **p5.js is LGPL‑2.1 → `adaptable-concept`**.

### 6. 3D / shader
**Three.js · Babylon.js · React Three Fiber · Threlte · TresJS · curtains.js** (MIT/Apache →
`redistributable`); **Shadertoy (per-author, default CC‑BY‑NC‑SA) · The Book of Shaders
(all rights reserved) · Spline (proprietary SaaS)** → `reference-only`.

### 7. SVG / icon motion
**Lottie (lottie-web) · Rive (MIT runtimes; paid editor) · Rough Notation · Vivus.** MIT →
`redistributable`.

### 8. Animated component collections
High-fidelity effect collections — the highest-risk tier for licence/quality.
**Magic UI · React Bits · Motion Primitives · Cult UI · Kokonut UI · SmoothUI · Animata ·
Fancy Components · GodUI** (MIT but copy-paste → mostly `adaptable-concept`); **Aceternity UI
(unknown per-component) · Uiverse (community-submitted) · Hover.dev (proprietary) ·
Animate UI / Vue Bits / Svelte Bits (MIT + Commons Clause, source-available)** →
`reference-only`. The Commons-Clause cases are why "source-available ≠ open source".

### 9. Enterprise design systems
Design *judgment* sources, with split code/asset terms IIOS must respect.
**Material Design (guidance, reference-only) · Apple HIG (reference-only) · IBM Carbon
(Apache‑2.0 code) · Microsoft Fluent 2 (MIT code) · GitHub Primer (MIT code) · Adobe
Spectrum (Apache‑2.0 React code) · Atlassian (Apache‑2.0 Atlaskit) · Ant Design (MIT) ·
Shopify Polaris (modified-MIT, field-of-use restricted) · Salesforce SLDS (BSD‑3 code +
CC‑BY‑NC‑ND assets).** Most are `adaptable-concept`; guidance-only systems are
`reference-only`. Several are core-ledger sources ([#11–15](./research-ledger.md)).

### 10. Creative references (inspiration only)
**Awwwards · Codrops · SiteInspire · Godly · Hoverstates.** All `reference-only` — IIOS
draws *ideas* here, never code.

---

## Beyond effect/component sources

The candidate landscape also feeds the non-source engines (knowledge cited the same way):

- **Standards & platform** — W3C/WAI (WCAG 2.2, WAI-ARIA), web.dev/Chrome (Core Web Vitals,
  INP), MDN (the web platform). → Design Intelligence, Assurance.
- **Design tokens** — DTCG Format Module (first stable 2025‑10). → Design Intelligence
  interop ([ledger #6](./research-ledger.md)).
- **Usability theory** — NN/g 10 heuristics. → UX-principle checks ([ledger #7](./research-ledger.md)).
- **Tooling** — axe-core, Storybook, Playwright. → Assurance execution
  ([ledger #5, #16](./research-ledger.md)).
- **Agent runtime** — Claude Code skills/subagents. → Orchestrator + specialist agents
  ([ledger #17](./research-ledger.md)).

---

## Landscape governance summary

| Disposition | Meaning | Typical examples |
|-------------|---------|------------------|
| `redistributable` | Bundle/adapt freely (permissive, confirmed) | Radix, Three.js, PixiJS, Motion, browser-native |
| `adaptable-concept` | Re-implement clean-room; don't copy | GSAP, p5.js, Carbon/Fluent/Primer code, most collections |
| `reference-only` | Inspiration / unverified / restricted | Aceternity, Commons-Clause collections, ScrollReveal, galleries, guidance-only systems |
| `rejected` | Fails licence/security gate | (case-by-case) |

**Reading.** The landscape is intentionally **wide for discovery, narrow for trust**.
~90 catalogued candidates give breadth; only the verified ledger backs decisions; the
licence gate keeps the long tail from leaking into shipped code. This is the
evidence-based release model in practice — depth and honesty over fabricated scale.
