# Authoring a Pattern Record

A **pattern** is the problem-first unit of Motif intelligence. It describes a user problem,
the user intent behind it, the interaction states involved, and the accessibility and
success criteria a solution must meet. Patterns are what Motif searches **before** effects, they connect "what the user needs to understand/feel/accomplish" to candidate effects.

- **Schema:** `schemas/pattern.schema.json`
- **Location:** `registry/patterns/`
- **Validate:** `python -m motif validate`

## Required fields

`id`, `name`, `problem`, `user_intent`, `interaction_states`,
`accessibility_requirements`, `success_criteria`.

## Field guidance

| Field | Guidance |
|-------|----------|
| `id` | slug, `^[a-z0-9-]+$` |
| `name` | human name (e.g. "Progressive disclosure of advanced options") |
| `problem` | the real user/product problem, framed without reference to any effect |
| `user_intent` | what the user is trying to do (drives selection) |
| `suitable_pages` / `unsuitable_pages` | page/screen types where it does / does not belong |
| `recommended_effects` / `rejected_effects` | `id`s from `registry/effects/`; rejected ones document anti-patterns |
| `interaction_states` | e.g. idle, hover, focus, active, loading, empty, error, success |
| `accessibility_requirements` | keyboard, focus, semantics, reduced-motion, non-motion status |
| `performance_budget` | the cost ceiling a solution must respect |
| `success_criteria` | observable outcomes that mean the pattern worked |
| `tests` | how conformance is checked |

## Author problem-first

Write `problem` and `user_intent` **before** thinking about any effect. A pattern that
starts from a desired animation is inverted and will be rejected in review. The pattern
should read sensibly even if every `recommended_effects` entry were removed.

## Encode rejection, not just recommendation

`rejected_effects` is as important as `recommended_effects`. It records *why* a tempting
effect is wrong for this problem (e.g. "continuous parallax rejected: competes with data
scanning on dense screens"). This is how Motif resists novelty-for-novelty's-sake. Align
rejections with `intelligence/anti-patterns/`.

## Accessibility is structural

`accessibility_requirements` must always cover keyboard reachability, visible focus,
correct semantics, a reduced-motion path, and never relying on motion alone to convey
status. `interaction_states` must include focus and error/empty states, not just the
happy path.

## Required provenance

Patterns are Motif's own intelligence, derived from `intelligence/interaction-problems/`
and selection policies rather than copied from a vendor. They carry no third-party code.
Where a pattern is informed by an enterprise design system's guidance, cite that guidance
as evidence in the surrounding documentation, but the pattern text is original.

## Example skeleton

```json
{
  "id": "reveal-on-scroll",
  "name": "Reveal content as it enters the viewport",
  "problem": "Long pages feel flat and users miss that new sections have begun",
  "user_intent": ["orient within a long page", "notice section boundaries"],
  "suitable_pages": ["marketing-landing", "documentation-landing"],
  "unsuitable_pages": ["dashboard", "data-table", "form"],
  "recommended_effects": ["scroll-reveal-fade"],
  "rejected_effects": ["heavy-parallax-pin"],
  "interaction_states": ["offscreen", "entering", "revealed", "reduced-motion"],
  "accessibility_requirements": [
    "content readable without JS",
    "no reliance on motion to convey meaning",
    "respects prefers-reduced-motion"
  ],
  "performance_budget": "transform/opacity only; no layout thrash on scroll",
  "success_criteria": ["all content reachable", "no CLS", "works with reduced motion"],
  "tests": ["reduced-motion path", "no-JS fallback"]
}
```
