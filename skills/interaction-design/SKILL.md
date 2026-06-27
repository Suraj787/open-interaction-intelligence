---
name: interaction-design
description: Use when product context is known and you need to convert the user's need into a precise interaction objective and select the UI pattern that satisfies it before any effect is chosen.
---

# Interaction Design

**Responsibility:** Translate context into an **interaction objective** and a
**pattern**. This is the PATTERN-before-EFFECT gate.

## When to invoke

- After `product-context-analysis` (steps 5-7 of the root workflow).
- Whenever someone proposes an effect without a stated objective.

## Inputs

- Product type, page/screen type, user + primary task.
- The interaction problem statement.

## Outputs

- A single-sentence **interaction objective**: what the user must understand, feel,
  or accomplish.
- A chosen **pattern** (e.g. progressive disclosure, optimistic feedback, focus
  guidance, state transition, affordance hint) with rationale.
- A constraint set passed to `effect-discovery` (attention budget, density, frequency
  of use, criticality).

## How it connects

- Reads `intelligence/` pattern catalogues and objective→pattern mappings.
- Produces the query that `effect-discovery` runs against `registry/`.
- Never selects a concrete effect — that is `effect-selection`'s job.

## Notes

If the objective can be met with no motion at all (layout, copy, color, spacing),
say so and stop. The strongest interaction is often the absence of an effect.
