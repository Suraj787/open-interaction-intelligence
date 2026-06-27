# Interaction Intelligence

The interaction-intelligence engine for **Interface Intelligence OS**. Where the registry answers *what to build* (effects, patterns, recipes) and design-intelligence answers *how it should look*, this engine answers **how it should move, breathe, and respond** — and whether an interface has actually handled every state it can land in.

It does not reinvent the registry. It **reuses** the registry's effects, patterns, and recipes, and layers three new dimensions on top:

1. **Motion grammars** — coherent, named motion systems (durations, easing, entrance/exit, status, loading, errors, and reduced-motion fallback) so motion is consistent and accessible rather than ad hoc.
2. **Density grammars** — spacing, row height, and hit-area systems with responsive transformations, so the same UI can serve expert pointer users and touch users correctly.
3. **State completeness** — per-component-type requirements for the states an interface must implement (loading, empty, error, success, stale, slow-network, keyboard, touch, …) so "it works on the happy path" is no longer mistaken for "done".

## Layout

```
interaction-intelligence/
  motion/        motion grammars        (schema: schemas/motion-grammar.schema.json)
  density/       density grammars       (schema: schemas/density-grammar.schema.json)
  states/        state requirements     (schema: schemas/state-requirements.schema.json)
  anti-patterns/ motion/interaction anti-patterns + better alternatives
  navigation/    navigation guidance
  feedback/      feedback guidance
```

### Motion grammars (`motion/`)
- `enterprise-restrained` — minimal, fast, comprehension-only motion for dense operational tools.
- `saas-balanced` — confirming cause-and-effect motion for general-purpose SaaS (recommended default).
- `marketing-expressive` — choreographed, brand-voice motion for top-of-funnel surfaces.

Every grammar ships a `reduced_motion` path that collapses motion to instant/static.

### Density grammars (`density/`)
- `compact` — expert pointer users, maximum information density (32px targets, opt-in).
- `comfortable` — balanced default (40px targets), promotes to touch on small/coarse-pointer devices.
- `touch` — finger-first, **44px** minimum hit area, hard floor for coarse pointers.

### State requirements (`states/`)
Twelve component types: `form`, `table`, `list`, `button`, `data-fetch-region`, `upload`, `async-action`, `navigation`, `modal`, `search`, `chart`, `kanban-board`. Each lists `required_states`, `conditional_states` (with the triggering condition), a `rationale`, and `evidence`. For example a **data-fetch-region** must implement `loading + empty + error + success + stale + slow-network`; a **button** must implement `default + hover + focus + active + disabled + loading`.

## CLI

```
ii motion validate            # validate motion grammars against the motion-grammar schema
ii density validate           # validate density grammars against the density-grammar schema
ii states validate            # validate state-requirement records against the schema
ii states matrix              # print the component-type x state coverage matrix
```

- `ii motion validate` / `ii density validate` check each record in `motion/` and `density/` for schema conformance (required keys, kebab-case `id`, value types) and that the filename matches the record `id`.
- `ii states validate` checks every record in `states/` and confirms each required/conditional state name is drawn from the known state vocabulary.
- `ii states matrix` renders a grid of component types against states (required / conditional / —), making missing coverage obvious at a glance.

## How it plugs into the OS
- **Inputs:** a chosen motion grammar + density grammar + the component types present in a recipe.
- **Checks:** state completeness per component, anti-pattern violations (e.g. motion-only status, no reduced-motion), and density/target-size correctness for the target input.
- **Outputs:** a coverage matrix and a list of gaps that feed back into the registry recipe and the assurance/evidence layer.
