---
name: framework-adaptation
description: Use when a selected effect must be implemented in the target stack (Vue, Frappe-Vue, or whatever the repo uses) without introducing a new framework or breaking design-system conventions.
---

# Framework Adaptation

**Responsibility:** Implement the selected effect in the **target framework**, idiomatically,
reusing existing primitives.

## When to invoke

- After `effect-selection` (step 11 of the root workflow).

## Inputs

- The selected effect and its registry entry.
- The target framework, version, and design-system tokens/components.

## Outputs

- Implementation code in the target stack (Vue/Frappe-Vue first-class; also React,
  Svelte, or vanilla as the repo dictates).
- A reduced-motion variant wired in.
- A note of any reused vs new primitives.

## How it connects

- Reads `registry/` for framework-specific snippets and `intelligence/` for adaptation
  guidance.
- Hands the result to `motion-accessibility`, `motion-performance`, and
  `implementation-validation`.

## Notes

Never install another framework for a single effect. Prefer the design system's existing
transition utilities and tokens. For Vue, prefer native `<Transition>`/`<TransitionGroup>`
and composables over heavyweight animation libraries unless the registry entry justifies it.
