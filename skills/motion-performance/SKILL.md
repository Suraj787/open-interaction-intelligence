---
name: motion-performance
description: Use when validating that an interaction stays within performance budget, animating cheap properties, avoiding jank, and never running costly decorative motion behind dense UIs.
---

# Motion Performance

**Responsibility:** Keep interactions cheap and smooth. Protect dense work UIs from
decorative cost.

## When to invoke

- During implementation and at validation (step 13 of the root workflow).

## Inputs

- The implemented interaction, its animated properties, and the page context.

## Outputs

- Pass/fail against the performance budget, with required fixes.

## Checks

- Animate `transform`/`opacity`; avoid layout-triggering properties (width, height,
  top/left, box-shadow spread) unless justified.
- No continuous decorative motion behind dense or data-heavy screens.
- Effects are composited and do not cause long frames or layout thrash.
- Off-screen and reduced-motion paths do no needless work.
- WebGL/canvas only when a simpler technique cannot meet the objective.

## How it connects

- Reads `intelligence/` performance guidance and `registry/` cost metadata.
- Reports to `implementation-validation`; failures block the ship.

## Notes

If an effect is expensive and the objective could be met more cheaply, send it back to
`effect-selection`. Performance is a selection input, not just a post-hoc check.
