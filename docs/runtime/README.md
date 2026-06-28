# Motif Runtime, `motif run`

The flagship loop that drives a target interface from inspection to a validated, recorded,
reversible outcome. Status mirrors
[`docs/reviews/motif-v3-gap-analysis.md`](../reviews/motif-v3-gap-analysis.md) (§5/§6:
**partial**, orchestration + run records implemented; runtime steps that need a browser are
experimental).

## The pipeline

```
Inspect → Model → Start → Discover → Observe → Twin → Audit → Concepts →
Recommend → Preview → Plan → Apply-in-isolation → Validate → Compare → Record → Deliver/rollback
```

Implemented stages: Inspect, Model, Discover, Concepts, Recommend, Plan, Record,
Deliver/rollback. Experimental (need a browser runtime, not installed here): Start, Observe,
Twin, Audit, Preview, Apply-in-isolation, Validate, Compare.

## Commands

```bash
motif run --goal "tighten the checkout flow" --target ./app   # full loop (browser steps degrade gracefully)
motif run --mode improve --target ./app --dry-run             # default: plan + records, no live start, no apply
motif run --mode audit --target ./app                         # discover + findings, no changes
motif run --allow-runtime --target ./app   # EXPERIMENTAL: enable Start/Observe/Twin (needs Playwright)
motif run --resume <run-id>                                   # resume a recorded run
motif run --rollback <run-id>                                 # restore the worktree + .motif/rollback
```

`mode` is one of `create | improve | audit | repair | redesign | govern | benchmark`
(see `schemas/run-record.schema.json`). Aliases: `ii run`, `oii run`.

## Isolation and records

- Every run executes against a **git worktree**, never your working branch or `main`.
- Each run writes `.motif/runs/<id>/run-record.json`: mode, goal, `target_commit`, the exact
  commands, `files_changed`, linked findings and concepts, and the outcome.
- `--rollback` is reversible from the run record + `.motif/rollback/`.

## Honest status

| Stage group | Status |
|---|---|
| Inspect / Model / Discover / Concepts / Recommend / Plan / Record / Deliver | implemented |
| Start / Observe / Twin / Audit | experimental (browser runtime absent) |
| Preview / Apply-in-isolation / Validate / Compare | experimental |

## Safety

`--dry-run` is the default. Live process start of an arbitrary target app is the one
genuinely risky action; it is mitigated by worktree isolation, an explicit `--allow-runtime`
flag, an explicit apply step, and never touching `main`. Browser-dependent stages report
"not executed (no runtime)" rather than fabricating results.

## See also

- [`docs/architecture/motif-v3-live-architecture.md`](../architecture/motif-v3-live-architecture.md) §4
- [`docs/visual-twin/README.md`](../visual-twin/README.md), [`docs/assurance/README.md`](../assurance/README.md)
