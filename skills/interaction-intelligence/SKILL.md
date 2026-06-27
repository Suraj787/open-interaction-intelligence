---
name: interaction-intelligence
description: Use when a known product context must become a precise interaction objective, a UX pattern, required states, feedback, and only-then a motion or effect.
---

# Interaction Intelligence

**Responsibility:** Own the **pattern-before-effect** gate. Convert the user's need into
an interaction objective, select the pattern, define every required state, and choose the
least-complex feedback or motion that serves it.

## When to invoke

- Step 11 of the root workflow, after design structure is set.
- Whenever an effect is proposed without a stated objective.

## Inputs

- Interaction objective; product/user/workflow models; density and frequency of use.

## Outputs

- A single-sentence **interaction objective**.
- A chosen **pattern** with rationale (disclosure, optimistic feedback, focus guidance,
  state transition, affordance hint).
- The full **required-states** set: empty, loading, partial, error, success, offline,
  permission-denied, dense, zero-data.
- Feedback and motion choices with a reduced-motion path, or an explicit "no motion".

## Engine data + CLI

- Reads `interaction-intelligence/` (`motion`, `states`, `feedback`, `density`,
  `navigation`, `anti-patterns`).
- `ii interaction objective`, `ii interaction pattern`, `ii interaction states`.

## Notes

If layout, copy, colour, or spacing meets the objective with no motion, say so and stop.
Never rely on motion or colour alone for meaning; never block input for decoration.
