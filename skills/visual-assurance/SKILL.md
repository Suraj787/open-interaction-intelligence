---
name: visual-assurance
description: Use when an interface needs visual validation — every required state renders correctly, responsively, and faithfully to the design system across breakpoints and inputs.
---

# Visual Assurance

**Responsibility:** Confirm the interface looks and behaves correctly across all required
states, breakpoints, and input modes, and stays faithful to the design system.

## When to invoke

- Step 16 of the root workflow, after the UI is compiled or built.

## Inputs

- The built UI; the required-states set; the design system and genome.

## Outputs

- A per-state rendering report: empty, loading, partial, error, success, offline,
  permission-denied, dense, zero-data.
- Responsive checks across breakpoints; input-mode checks (pointer, touch, keyboard).
- Design-system fidelity findings and any drift from the genome.

## Engine data + CLI

- Reads `assurance/` visual rules, `design-intelligence/responsive-design`, and the
  genome in `governance/design-genome`.
- `ii assure --visual`.

## Notes

Validate every required state, not just the happy path. Report design-system deviations
to Governance as drift rather than silently accepting them.
