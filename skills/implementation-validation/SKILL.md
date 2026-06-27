---
name: implementation-validation
description: Use as the final acceptance gate to confirm an interaction is accessible, performant, responsive, design-system-consistent, and fully recorded before it is considered done.
---

# Implementation Validation

**Responsibility:** Run the final acceptance gates and produce the "After implementation
report". Nothing ships until this passes.

## When to invoke

- After implementation and the accessibility/performance sub-checks (steps 12-16).

## Inputs

- The implemented interaction and the sub-reports from `motion-accessibility` and
  `motion-performance`.

## Outputs

- A consolidated pass/fail with the required "After implementation report" fields:
  pattern/effect implemented, accessibility result, performance result, responsiveness
  result, design-system conventions preserved, dependencies added (with licence + cost)
  or none, and a decision-log + provenance entry.

## Gates

- Accessibility gate passed (`motion-accessibility`).
- Performance gate passed (`motion-performance`).
- Responsiveness verified across breakpoints and input modes (pointer, touch, keyboard).
- Design-system conventions preserved.
- Provenance and decision log written via `source-governance`.

## How it connects

- Aggregates the specialist gates; writes the final record.
- Any failed gate returns the work to the relevant specialist, not forward.

## Notes

Validation is binary per gate. Do not mark done with an open gate, and do not paper over
a failed accessibility or performance gate with a comment.
