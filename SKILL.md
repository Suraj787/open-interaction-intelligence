---
name: motif
description: Use when an AI coding agent must choose and implement a UI interaction, motion, or effect for a website or web application, and needs to select the least-complex pattern that serves a real user need rather than reach for a flashy animation.
---

# Motif

Motif is an intelligence and governance system, **not** an animation bundle. It helps you
select the RIGHT interaction for a product context. First determine what the user needs
to **understand, feel, or accomplish**; then select the **least complex** interaction
that achieves it. Always search for a PATTERN before an EFFECT.

## Reasoning model (8 levels)

development purpose → product type → user intent → page/screen type →
interaction objective → pattern → effect → implementation.

Always distinguish a **website** (marketing, narrative, persuasion) from a
**web application** (task completion, data density, repeated use). Vue and Frappe-Vue
are first-class targets. Default runtime is the **OFFLINE APPROVED REGISTRY**; reach the
internet only via an explicit `source-refresh`.

## 16-step orchestrator workflow

1. Inspect the target repo (framework, design system, existing motion conventions).
2. Identify the product purpose and product type.
3. Identify the page/screen type.
4. Identify the user and their primary task.
5. Identify the actual interaction problem to solve.
6. Load **only** the relevant local intelligence (`intelligence/`) and registry slices.
7. Search PATTERNS before EFFECTS.
8. Produce multiple candidate approaches.
9. Rank them transparently (state the criteria and scores).
10. Select the simplest approach that is fully effective.
11. Implement using the target framework (do not introduce a new one).
12. Validate accessibility (keyboard, focus, semantics, reduced-motion).
13. Validate performance (transform/opacity, budget, no jank).
14. Validate responsiveness across breakpoints and input modes.
15. Preserve the existing design-system conventions.
16. Record decisions and provenance.

## Hard rules (never)

- Never animate solely for novelty.
- Never install another framework for a single effect.
- Never use WebGL when something simpler suffices.
- Never run continuous decorative motion behind dense work UIs.
- Never depend only on motion to convey status.
- Never remove keyboard focus.
- Never make essential actions hover-only.
- Never block input for decorative motion.
- Never animate expensive layout properties when transform/opacity suffice.
- Never add a dependency without a licence + cost review.
- Never ship without a reduced-motion path.
- Never combine multiple high-attention effects without explicit justification.
- Never make enterprise apps resemble animation showcases.
- Never copy restricted or licence-incompatible code.
- Never let novelty outrank usability.

## Before implementation record:

- Product type and page/screen type.
- User and primary task.
- The interaction objective (what must be understood/felt/accomplished).
- Candidate approaches considered and the ranking rationale.
- The selected pattern and effect, and why it is the simplest effective choice.
- Accessibility and reduced-motion plan.
- Performance budget and properties to be animated.
- Source/provenance of any registry entry or external reference.

## After implementation report:

- The pattern and effect implemented, in the target framework.
- Accessibility validation result (keyboard, focus, semantics, reduced-motion).
- Performance validation result (animated properties, measured/observed cost).
- Responsiveness validation across breakpoints and input modes.
- Design-system conventions preserved or adjusted.
- Dependencies added (with licence + cost note) or confirmation that none were.
- Decision log + provenance entry written.

## Specialist skills

Load these selectively as the workflow demands:

- `skills/product-context-analysis`, purpose, product type, page/user/task.
- `skills/interaction-design`, interaction objective and pattern selection.
- `skills/effect-discovery`, find candidate effects in the registry.
- `skills/effect-selection`, rank candidates, pick the simplest effective one.
- `skills/framework-adaptation`, implement in Vue/Frappe-Vue or the target stack.
- `skills/motion-accessibility`, keyboard, focus, semantics, reduced-motion.
- `skills/motion-performance`, animation cost, budgets, jank avoidance.
- `skills/implementation-validation`, final acceptance gates.
- `skills/source-governance`, registry provenance, licences, source-refresh.
- `skills/web-experience-orchestrator`, thin alias that defers here.

## CLI

The registry, ranking, and provenance tooling is exposed through `python -m motif`
(for example registry search, candidate ranking, and source-refresh). Prefer the CLI
over ad-hoc internet retrieval; it enforces the offline-approved-registry default.
