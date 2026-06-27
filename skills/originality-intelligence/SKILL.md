---
name: originality-intelligence
description: Use when an interface risks converging on generic AI aesthetics and you need to detect templated output and steer toward intentional, context-fitting design.
---

# Originality Intelligence

**Responsibility:** Detect generic AI-aesthetic convergence and ensure visual decisions
are intentional and fitted to the product, not defaulted from training priors.

## When to invoke

- Step 10 of the root workflow, after structural concepts and before pattern lock-in.
- Whenever output resembles a templated landing-page or dashboard default.

## Inputs

- Proposed structural concepts, visual direction, and the genome slice.

## Outputs

- A **convergence assessment**: which choices read as generic and why.
- Specific, lower-complexity alternatives that fit the product's actual identity.
- A pass/flag verdict feeding the decision ledger.

## Engine data + CLI

- Reads `design-intelligence/styles` and the genome in `governance/design-genome`.
- `ii originality check`, `ii originality diff`.

## Notes

Originality is not novelty for its own sake. Never let visual novelty outrank user
outcomes. The goal is design that is recognisably *this product's*, achieved with the
least complexity. Flag, explain, and offer alternatives — do not silently restyle.
