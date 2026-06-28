# Migrating from Motif v2.0.0 to v3 "Motif Live"

v3 is **additive**. It evolves v2.0.0 (intelligence + governance) into a runtime / execution /
assurance / governance platform without removing anything. This guide states exactly what is
preserved, what is added, and how runtime state is laid out. Status throughout mirrors
[`docs/reviews/motif-v3-gap-analysis.md`](../reviews/motif-v3-gap-analysis.md).

## What is preserved (unchanged)

- **All v2 CLI commands**: `validate`, `doctor`, `search`, `rank`, `rank-sources`, `source`,
  `component`, `generate-index`. Same flags, same output contract.
- **All three command names**: `motif`, and the aliases `ii` and `oii`, all keep working.
- **All 25 schemas** in `schemas/`, none removed, none renamed. v3 adds new schemas
  alongside them (e.g. `run-record`, `twin-manifest`, `finding`, `concept`, `recommendation`,
  `policy`, `memory`, `assurance-evidence`, `design-system-extract`).
- **The registry and registries**: 90 sources, 64 components, 30 effects, 28 patterns,
  14 recipes, plus the 5 scanners, licence gate, provenance and controlled installer.
- **The `make check` gate, CI and evals** continue to pass and remain the line for what may be
  claimed as implemented.

> **No schema is removed and no v2 command changes behaviour.** v2 workflows run on v3
> unchanged.

## What is added in v3

| Area | New surface | Status |
|---|---|---|
| Runtime loop | `motif run` (Inspect…Deliver/rollback) | partial |
| Authoring | `motif create`, `motif improve`, `motif init` | partial / implemented |
| Visual Twin | `motif twin` | partial |
| Findings | `motif findings …` (unified model + lifecycle) | implemented |
| Recommendation | `motif recommend` | implemented |
| Compiler | `motif compile plan/preview/apply/pr` | plan implemented; rest partial/exp |
| Assurance | `motif assure` | experimental (runtime layers) |
| Governance | `motif policy`, `motif memory`, `motif guard` | implemented |
| Catalogue / viewer | `motif atlas`, `motif studio` | atlas implemented; studio partial |
| Integration | `motif mcp serve` | implemented |
| Benchmark runner | `motif bench` | partial |
| Design system | `motif design-system extract` | implemented |

Experimental/planned items are the browser-runtime surfaces only (twin rendering, Playwright
assurance, live preview, pixel/semantic visual diff, interactive Studio apply), see the
gap analysis.

## `.motif/` runtime-state layout

v3 introduces per-project runtime state under `.motif/`. These directories are **gitignored**
runtime dirs, reproducible from the registry + recorded runs, never authoritative knowledge.

```
.motif/
  project/      # detected framework, target metadata, init results
  twin/         # Visual Twin manifests (and screens/ when rendered, experimental)
  findings/     # unified finding records + lifecycle/suppressions
  concepts/     # generated concept candidates
  previews/     # preview outputs (experimental; empty without a browser runtime)
  decisions/    # decision-ledger entries
  evidence/     # assurance-evidence records
  baselines/    # recorded baselines for comparison
  policies/     # active/resolved policy state for the project
  runs/         # run-record.json per run (mode, goal, commit, commands, changes, outcome)
  rollback/     # rollback records backing motif run --rollback
```

v2's existing `.motif/` governance dirs (`approved/`, `reviewed/`, `quarantine/`, `rejected/`,
`snapshots/`) are unchanged and continue to back the source-update lifecycle.

## Upgrade checklist

1. Pull v3. Existing v2 commands keep working immediately.
2. Run `motif init` once per project to create the `.motif/` runtime dirs and a first audit.
3. Confirm `.motif/` is gitignored (v3 ships the ignore entries; verify in your repo).
4. Adopt new surfaces incrementally, `motif findings`, `motif atlas build`, `motif guard`,
   `motif mcp serve` are all implemented and safe to use now.
5. Treat browser-runtime surfaces as experimental until a runtime (Playwright) is installed.

## See also

- [`docs/architecture/motif-v3-live-architecture.md`](../architecture/motif-v3-live-architecture.md)
- [`docs/reviews/motif-v3-gap-analysis.md`](../reviews/motif-v3-gap-analysis.md)
- [`docs/reviews/motif-v3-pre-release-review.md`](../reviews/motif-v3-pre-release-review.md)
