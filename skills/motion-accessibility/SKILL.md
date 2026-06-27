---
name: motion-accessibility
description: Use when validating that an interaction preserves keyboard access, focus, semantics, and honors reduced-motion before it can ship.
---

# Motion Accessibility

**Responsibility:** Enforce the mandatory accessibility and reduced-motion invariants.
This is a non-negotiable gate.

## When to invoke

- During implementation and again at validation (step 12 of the root workflow).

## Inputs

- The implemented interaction and its reduced-motion variant.

## Outputs

- Pass/fail per invariant, with required fixes.

## Invariants

- Keyboard focus is never removed or obscured; focus order stays logical.
- Essential actions are never hover-only; they work via keyboard and touch.
- Status is never conveyed by motion alone, pair with text/icon/ARIA.
- `prefers-reduced-motion: reduce` is respected with a meaningful non-motion path.
- Decorative motion never blocks or delays input.
- Semantics (roles, names, states) are correct and announced.

## How it connects

- Reads `intelligence/` accessibility guidance; does not touch `registry/` ranking.
- Reports to `implementation-validation`; failures block the ship.

## Notes

A reduced-motion path is not "disable the animation and leave a gap", it must still
communicate the state change clearly. No interaction ships without it.
