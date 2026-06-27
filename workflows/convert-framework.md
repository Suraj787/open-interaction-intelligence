# Workflow: Convert an Interaction to Another Framework

Re-express an existing interaction in a different framework (e.g. a React reference into a
Vue/Frappe-Vue implementation) by moving the *idea* through the adaptation model, never
by porting code or installing the source framework.

## Hard rule

**Never install another framework for an effect.** A Vue/Svelte/Angular project never
gets React added to obtain an interaction. Re-implement via the adapter instead.

## Preconditions

- The interaction is understood and (if third-party) its source/licence is known.
- Target framework and design system known. Default **offline approved registry** mode.

## Steps

1. **Extract the concept, not the code.** State what the user must understand, feel or
   accomplish, independent of the original framework.
2. **Write the framework-neutral algorithm:** triggers, states, transitions, cleanup,
   reduced-motion path. This is licence-safe (concept, not source).
3. **Check provenance.** If the original is licence-restricted, this is **clean-room
   adaptation**: retain no source code, record inspiration in the recipe's
   `source_references`, set `provenance_type: adapted-concept`. Otherwise `original` or
   `browser-native`.
4. **Choose the implementation level** for the target via the hierarchy (browser-native
   CSS first; heavy deps last). Prefer the target framework's built-ins (e.g. Vue
   `<Transition>`).
5. **Apply the target adapter** (`skills/framework-adaptation`) and fill every
   adapter-contract concern: lifecycle, cleanup, SSR, hydration, keyboard, pointer/
   coarse-pointer, responsive, reduced-motion, testing.
6. **Implement** in the target's conventions and design system. For Frappe-Vue, use
   Frappe UI patterns; do not add a parallel animation engine.
7. **Gates:** accessibility, performance, responsiveness, re-validate; the reduced-motion
   path must exist in the new framework too.
8. **Author the recipe** (`recipe-authoring.md`) for the new `framework`, with provenance
   and `source_references`; record the decision.
9. **Validate:** `python -m motif validate`.

## Done when

The interaction works in the target framework with full adapter coverage, no foreign
framework was installed, provenance is recorded, and all gates pass.
