# Authoring a Recipe Record

A **recipe** is Motif's own installable implementation of a pattern in a specific framework.
Where a *component* is evidence about a third-party source and an *effect* is an abstract
technique, a recipe is the concrete, provenance-clean thing Motif can actually install into
a project. Recipes are where clean-room adaptation lands.

- **Schema:** `schemas/recipe.schema.json`
- **Location:** `registry/recipes/`
- **Validate:** `python -m motif validate`

## Required fields

`id`, `name`, `pattern`, `framework`, `provenance_type`, `license`, `reduced_motion`,
`accessibility`, `browser_support`, `maturity`.

## Field guidance

| Field | Guidance |
|-------|----------|
| `id` | slug, `^[a-z0-9-]+$` |
| `pattern` | the `id` of the pattern in `registry/patterns/` this recipe implements |
| `framework` | one of `browser-native`, `react`, `vue`, `svelte`, `angular`, `vanilla`, `frappe-vue` |
| `technology`, `dependencies` | implementation tech; keep dependencies minimal (see hierarchy) |
| `cost` | `none` / `low` / `medium` / `high`, dependency/runtime weight |
| `license` | licence of **this recipe** (Motif originals are MIT) |
| `provenance_type` | `original` / `browser-native` / `adapted-concept` |
| `source_references` | source `id`s that inspired an `adapted-concept`; the inspiration trail |
| `algorithm` | the framework-neutral algorithm the implementation follows |
| `implementation_path` | path to the actual implementation under `implementations/` (or `null`) |
| `reduced_motion` | the reduced-motion behaviour (required) |
| `responsive_behaviour` | breakpoint/input-mode behaviour |
| `browser_support` | required/optional capabilities |
| `accessibility` | keyboard, focus, semantics summary |
| `tests` | how it is validated |
| `maturity` | `stable` / `beta` / `experimental` |

## Provenance is the point

`provenance_type` records how the recipe came to exist:

- `browser-native`, built directly on platform capabilities; no third-party code.
- `original`, Motif's own design.
- `adapted-concept`, produced by **clean-room adaptation**: record the interaction
  objective and behaviour, write a framework-neutral `algorithm`, implement independently,
  and **retain no source code**. List the inspirations in `source_references`. Avoid
  line-by-line, structure-by-structure or distinctive-copy recreation. Preserve any
  required third-party notices even when adapting only the concept.

A recipe with `provenance_type: adapted-concept` must have at least one
`source_reference`, and the referenced source's licence must permit
`adaptable-concept`/redistribution at the recipe's chosen `license`. The project's MIT
licence never overrides a third-party obligation.

## Prefer the lightest implementation

The `framework` and `dependencies` choices follow the implementation hierarchy in
[framework-adaptation.md](framework-adaptation.md): browser-native CSS first, heavy
dependencies last. A `cost: high` recipe needs explicit justification in `algorithm`/
docs. **Never install another framework for a single effect**, a Vue project gets a
`vue`/`frappe-vue`/`browser-native` recipe, never a `react` one.

## Accessibility and reduced motion are required fields

`reduced_motion` and `accessibility` are required by the schema. Describe real behaviour,
not intentions. A recipe with no reduced-motion path cannot be authored.

## Example skeleton

```json
{
  "id": "reveal-on-scroll-vue",
  "name": "Reveal on scroll (Vue, browser-native)",
  "pattern": "reveal-on-scroll",
  "framework": "vue",
  "technology": ["intersection-observer", "css-transition"],
  "dependencies": [],
  "cost": "none",
  "license": "MIT",
  "provenance_type": "browser-native",
  "source_references": [],
  "algorithm": "Observe target; on first intersection add a class that transitions opacity/transform; disconnect observer; if prefers-reduced-motion, reveal immediately.",
  "implementation_path": "implementations/reveal-on-scroll-vue",
  "reduced_motion": "Reveals instantly, no transform animation",
  "responsive_behaviour": "Identical across breakpoints; no pointer dependence",
  "browser_support": "IntersectionObserver (graceful: content visible if unsupported)",
  "accessibility": "Content reachable by keyboard and screen reader regardless of reveal state",
  "tests": ["reduced-motion", "no-JS visibility"],
  "maturity": "stable"
}
```
