# Workflow: Improve an Existing UI

Enhance an existing product without destabilising it: preserve the design system, add
motion only where it solves a real problem, and keep everything reversible.

## Preconditions

- Existing repo with established framework, design system and (possibly) motion
  conventions.
- Default **offline approved registry** mode.

## Steps

1. **Inspect the target** thoroughly: framework, design tokens, existing motion
   conventions, existing dependencies. Load `skills/product-context-analysis`.
2. **Classify the product** as website vs web application — the bar for motion differs.
3. **Find the real problem.** Identify the specific interaction problem to solve (e.g.
   "users miss that the save succeeded"), not "make it feel modern."
4. **Reuse before adding.** Check whether an existing project dependency or a
   browser-native mechanism already covers it (implementation hierarchy steps 1–3).
   **No automatic new dependency.**
5. **Search patterns first:** `python -m motif search "<problem>"`; consider effects only
   after a pattern fits.
6. **Produce candidates and rank** (`skills/effect-selection`); choose the simplest
   effective option that fits the existing design system.
7. **Implement in the current framework** (`skills/framework-adaptation`). Do not
   introduce a new framework; preserve design-system conventions.
8. **Accessibility + performance + responsiveness gates** as in the build workflows; add a
   reduced-motion path if one is missing.
9. **Install reversibly:** `python -m motif component plan-install` to preview the diff,
   licence, security findings and dependency impact; then `python -m motif component install`
   (creates a rollback snapshot + provenance manifest). Use
   `python -m motif component rollback` if validation fails.
10. **Record the decision** (`schemas/decision.schema.json`) and provenance.

## Done when

The targeted problem is measurably better, the design system is intact, no unjustified
dependency was added, and the change is recorded and reversible.
