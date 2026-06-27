---
name: performance-assurance
description: Use when an interface needs performance validation — animated properties, budgets, payload, and jank — with claims backed by measurement rather than assertion.
---

# Performance Assurance

**Responsibility:** Keep the interface fast and ensure any performance claim is measured,
not assumed.

## When to invoke

- Step 16 of the root workflow, especially where motion or heavy rendering exists.

## Inputs

- The compiled plan or built UI; animated properties; bundle and payload shape.

## Outputs

- A report on animated properties (prefer transform/opacity), budget adherence, and
  observed cost.
- Flags for layout-thrashing properties, oversized payloads, and unnecessary WebGL.
- An explicit note distinguishing **measured** results from **estimated** ones.

## Engine data + CLI

- Reads `assurance/` performance rules and `interaction-intelligence/motion`.
- `ii assure --perf`.

## Notes

Never claim measured performance without measurement. Never use WebGL when CSS/SVG/native
suffices. Never run continuous decorative motion behind dense work UIs.
