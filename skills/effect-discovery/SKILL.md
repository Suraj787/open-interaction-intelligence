---
name: effect-discovery
description: Use when a pattern and interaction objective are fixed and you need to enumerate candidate effects from the approved offline registry that could realise that pattern.
---

# Effect Discovery

**Responsibility:** Given a pattern + constraints, produce a **set of candidate effects**
from the approved registry. Discovery is breadth; selection comes next.

## When to invoke

- After `interaction-design` (step 8 of the root workflow).

## Inputs

- The chosen pattern and constraint set.
- Target framework and design-system tokens.

## Outputs

- Multiple candidate effects, each with: registry id, complexity tier, dependencies,
  framework fit, accessibility notes, and provenance.

## How it connects

- Queries `registry/` via `python -m motif` (offline approved registry by default).
- Reads `intelligence/` to map a pattern to candidate effect families.
- Only `source-governance` may widen the search beyond the offline registry via an
  explicit `source-refresh`.

## Notes

Always return more than one candidate, and always include the **least-complex** option
(often "CSS-only" or "no motion"). Do not pre-rank here; hand the full candidate set to
`effect-selection`. Discard any candidate whose licence or provenance is unresolved.
