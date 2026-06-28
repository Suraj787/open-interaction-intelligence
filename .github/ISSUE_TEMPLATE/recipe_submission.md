---
name: Submit a clean-room recipe
about: Propose a concrete, original (clean-room) implementation of an interaction
title: "recipe: <name>"
labels: [recipe, clean-room, needs-review]
assignees: []
---

> Motif bundles **original** implementations, never copied third-party code. Read the
> **clean-room adaptation procedure** in [`CONTRIBUTING.md`](../../CONTRIBUTING.md) and
> [`docs/recipe-authoring.md`](../../docs/recipe-authoring.md) first. Study the *concept*,
> not the code. Never copy markup, assets, proprietary tokens, or reconstruct premium
> components from previews.

## Recipe identity

- **Name:**
- **Pattern it serves:** (the user need / interaction objective, patterns before effects)
- **Effect(s) involved:** (if any)
- **Target framework(s):** (browser-native / Vue / Frappe-Vue / React)
- **Website vs web application:** (which context, and why)

## Provenance (required)

- **Inspiring source id / name:** (the `source` record this derives from)
- **Official homepage / repository:**
- **Specific component or effect referenced:**
- **Evidence links:** (docs, demo, licence file that justify the concept and licence)
  -
  -

## Licence (required)

- **Source licence (SPDX or exact name):**
- **Canonical licence URL (`license_reference`):**
- **Does the licence permit clean-room adaptation of the concept?** (yes/no, if unknown,
  source-available, Commons-Clause or premium, **stop**: reference-only at most)
- **Attribution required and preserved?** (yes/no, what notice, and where)
- **Licence confidence:** (high / medium / low)

## Accessibility & reduced-motion (required)

- **Keyboard / focus / semantics:**
- **`prefers-reduced-motion` path:** (what happens when motion is reduced, this is
  mandatory, not optional)
- **No essential status is hover-only or motion-only:** (confirm / explain)

## Performance (required)

- **Animated properties:** (transform/opacity only? any layout thrash?)
- **Performance budget:** (frame budget, no continuous decorative motion behind dense UIs)
- **Cost / dependencies:** (added bytes, runtime work, low-end-device behaviour)

## Implementation plan

Where the implementation will live (`implementations/`, `registry/recipes/`), the schemas
it must satisfy (`schemas/recipe.schema.json`), and any decision/memory record it relates
to (`governance/decision-ledger/`).

## Maintainer declaration

- [ ] This is an **original** implementation written from scratch; no source code, markup,
      assets or proprietary tokens were copied.
- [ ] The inspiring source's licence permits adapting the **concept**, and attribution /
      third-party notices are preserved.
- [ ] Accessibility (keyboard, focus, semantics, reduced-motion) and performance
      (transform/opacity, budget, no jank) are handled, not deferred.
- [ ] The record will be labelled `original` and will validate against its JSON Schema.
- [ ] AI assistance (if any) is disclosed and a human has reviewed and taken
      responsibility for the result.

## Checklist

- [ ] Opened/linked a `new_source` issue if the inspiring source is not yet in the registry.
- [ ] Provenance, licence, accessibility and performance sections above are complete.
- [ ] `make check` passes locally.
- [ ] I understand a maintainer will re-verify licence and provenance before merge.
