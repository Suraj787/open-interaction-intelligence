# Workflow: Implement a Pattern

Turn a selected pattern (and effect) into a working, validated implementation in the
target framework, with provenance. Assumes the pattern/effect is already chosen (see
[select-effects.md](select-effects.md)).

## Preconditions

- A pattern in `registry/patterns/` fits the problem; an effect is selected.
- Target framework and design system known. Default **offline approved registry** mode.

## Steps

1. **Read the pattern.** Confirm `problem`, `user_intent`, `interaction_states`,
   `accessibility_requirements`, `performance_budget`, `success_criteria`.
2. **Find or author the recipe.** Look for a recipe in `registry/recipes/` whose
   `pattern` matches and whose `framework` is your target. If none exists, author one
   (see [recipe-authoring.md](../docs/recipe-authoring.md)).
3. **Write the framework-neutral algorithm** (the recipe `algorithm`): triggers, states,
   transitions, cleanup, reduced-motion path.
4. **Pick the implementation level.** Use the highest viable hierarchy step
   (browser-native CSS → transitions → existing dep → WAAPI → View Transitions →
   lightweight motion dep → GSAP → Canvas → WebGL). **No new framework; no unjustified
   dependency.**
5. **Apply the framework adapter** (`skills/framework-adaptation`). Fill every
   adapter-contract concern: lifecycle, cleanup, SSR, hydration, keyboard, pointer/
   coarse-pointer, responsive, reduced-motion, testing. For Frappe-Vue, respect Frappe UI
   conventions.
6. **Implement** in the project, preserving design-system conventions.
7. **Gate — accessibility:** keyboard, focus, semantics, reduced-motion; status never
   motion-only.
8. **Gate — performance:** transform/opacity, budget respected, no jank.
9. **Gate — responsiveness:** breakpoints + input modes.
10. **Record** the recipe + decision + provenance. If installing an approved component,
    use `python -m motif component install` (diff + rollback + manifest).
11. **Validate:** `python -m motif validate`; then
    [validate-experience.md](validate-experience.md).

## Done when

The pattern's `success_criteria` are met in the target framework, all gates pass, and the
recipe/decision/provenance are recorded.
