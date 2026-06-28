# `motif create`, new interface from intent

Turn a brief or spec into product context, ranked concepts and a reversible compile plan.
Part of the v3 "Motif Live" platform. Status mirrors
[`docs/reviews/motif-v3-gap-analysis.md`](../reviews/motif-v3-gap-analysis.md) (§1A: **partial**, spec→context→concepts→plan implemented; preview / compile-apply experimental).

## What it does

1. Normalise a brief into an `interface-spec` (schema `schemas/interface-spec.schema.json`).
2. Derive product context + design genome (`product-context`, `design-genome`).
3. Recommend sources, patterns and effects (explainable, registry-backed).
4. Generate and compare structured `concept` records.
5. Emit an ordered, reversible **compile plan**.
6. *(experimental)* Render a visual preview and apply the plan in an isolated worktree.

## Commands

```bash
motif create "B2B analytics dashboard, dense, dark, keyboard-first"   # brief → spec → concepts → plan
motif create --spec specifications/project-dashboard.json             # start from an existing spec
motif create --concepts 3                                             # generate N concepts to compare
motif create --plan-only                                              # stop at the compile plan (no apply)
motif create --preview      # EXPERIMENTAL: needs a browser runtime (not installed)
motif create --apply        # EXPERIMENTAL: applies the plan in a git worktree
```

Aliases `ii create` and `oii create` are equivalent.

## Honest status

| Step | Status |
|---|---|
| Spec normalise → context → genome | implemented |
| Recommend + concept generation + compare/select | implemented |
| Compile **plan** (ordered, reversible) | implemented |
| Visual **preview** | experimental (Playwright not installed) |
| Compile **apply / pr** | partial, applies in a worktree, never touches `main` |
| Validate rendered result | experimental |

## Output

Artefacts land under `.motif/` (gitignored runtime state):

- `.motif/concepts/<id>.json`, candidate concepts
- `.motif/previews/<id>/`, preview outputs (experimental; empty without a runtime)
- `.motif/runs/<id>/run-record.json`, the create run, reproducible and reversible

## Safety

`create` is plan-first. Nothing is written to your source tree until an explicit `--apply`,
which runs in an isolated git worktree with a rollback record. The preview and validate steps
are clearly marked experimental and degrade to "not rendered" rather than faking pixels.

## See also

- [`docs/runtime/README.md`](../runtime/README.md), the full `motif run` loop
- [`docs/visual-twin/README.md`](../visual-twin/README.md), what preview can/can't show
- [`docs/architecture/motif-v3-live-architecture.md`](../architecture/motif-v3-live-architecture.md) §2
