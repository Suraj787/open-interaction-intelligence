---
name: effect-selection
description: Use when you have multiple candidate effects and must rank them transparently and select the simplest one that fully achieves the interaction objective.
---

# Effect Selection

**Responsibility:** Rank candidates **transparently** and choose the simplest fully
effective approach. Novelty must never outrank usability.

## When to invoke

- After `effect-discovery` (steps 9-10 of the root workflow).

## Inputs

- The candidate set from `effect-discovery`.
- The interaction objective and constraints.

## Outputs

- A transparent ranking table with explicit criteria and scores.
- The selected effect with a written justification for why it is the simplest
  effective choice.
- A rejected-alternatives note for the decision log.

## Ranking criteria

- Effectiveness against the objective.
- Complexity / implementation cost (lower wins on ties).
- Accessibility and reduced-motion friendliness.
- Performance cost (transform/opacity preferred).
- Dependency footprint and licence cost.
- Design-system fit.
- Appropriateness to website vs web application.

## How it connects

- Uses `python -m motif` ranking to keep scoring reproducible and auditable.
- Passes the winner to `framework-adaptation`; logs the table via `source-governance`.

## Notes

When two candidates tie on effectiveness, the simpler, cheaper, more accessible one wins.
Combining multiple high-attention effects requires explicit justification recorded here.
