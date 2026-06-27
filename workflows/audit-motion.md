# Workflow: Audit Motion in an Existing Product

A read-first review that finds motion which hurts usability, accessibility or
performance, and produces a prioritised remediation list. Does not change code until
findings are agreed.

## Preconditions

- Existing repo. Default **offline approved registry** mode.

## Steps

1. **Inventory motion.** Locate every animation/transition/effect: CSS animations,
   transitions, JS-driven motion, scroll effects, canvas/WebGL, third-party widgets.
2. **Classify the product** (website vs web application), the acceptable motion profile
   differs sharply.
3. **Flag anti-patterns** against the hard rules and `intelligence/anti-patterns/`:
   - motion purely for novelty;
   - continuous decorative motion behind dense work UIs;
   - status conveyed by motion alone;
   - essential actions that are hover-only;
   - removed/!invisible keyboard focus;
   - expensive layout-property animation where transform/opacity would do;
   - multiple high-attention effects combined without justification;
   - missing reduced-motion path;
   - enterprise screens resembling animation showcases.
4. **Accessibility review** (`skills/motion-accessibility`): keyboard reachability, focus
   visibility, semantics, `prefers-reduced-motion` coverage, motion-independent status.
5. **Performance review** (`skills/motion-performance`): animated properties, jank, layout
   thrash, continuous timers, main-thread cost, mobile/coarse-pointer behaviour.
6. **Licence/provenance review** of any third-party effect in the tree: is its source and
   licence known? Flag unknown-licence code (should be `reference-only`).
7. **Prioritise findings:** severity (accessibility/perf regressions first) × effort.
8. **Record** each finding with location, rule violated, and recommended fix. Feed
   high-priority items into [improve-existing-ui.md](improve-existing-ui.md).

## Done when

A prioritised, evidence-backed findings list exists covering accessibility, performance,
anti-patterns and provenance, with no code changed yet.
