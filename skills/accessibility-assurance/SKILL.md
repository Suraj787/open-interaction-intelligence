---
name: accessibility-assurance
description: Use when an interface needs accessibility validation — keyboard operability, focus visibility, semantics, contrast, and reduced-motion — beyond automated checks alone.
---

# Accessibility Assurance

**Responsibility:** Verify the interface is operable and perceivable for all users, and
state the limits of what was actually checked.

## When to invoke

- Step 16 of the root workflow, on every interface that ships.

## Inputs

- The compiled implementation plan or built UI; the required-states set; motion choices.

## Outputs

- A keyboard, focus, semantics, and contrast report.
- Confirmation that meaning is never carried by motion or colour alone.
- Confirmation that a reduced-motion path exists wherever motion exists.
- A clear statement of which checks were automated vs. manually verified.

## Engine data + CLI

- Reads `assurance/` accessibility rules and `interaction-intelligence/states`.
- `ii assure --a11y`.

## Notes

Never treat automated accessibility checks as complete proof. Never remove visible focus;
never make essential actions hover-only. Report residual risk honestly.
