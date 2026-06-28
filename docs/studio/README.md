# Motif Studio

A local-first viewer over `.motif/` runtime state and the registry: browse findings,
concepts, twin manifests, decisions and policy in one place. Status mirrors
[`docs/reviews/motif-v3-gap-analysis.md`](../reviews/motif-v3-gap-analysis.md) (§10:
**partial**, local-first static viewer implemented; **interactive apply** experimental).

## What it does

- Renders a **read-only** view of `.motif/` (findings, concepts, previews, decisions,
  evidence, runs) and the registry, all from the one shared source of truth.
- Links each concept back to its findings and the run that produced it.
- *(experimental)* lets you select a concept and **apply** it, this needs the experimental
  compile-apply + preview path and a browser runtime.

## Commands

```bash
motif studio build         # generate the local static Studio site from .motif/ + registry
motif studio serve         # serve it locally (offline, no external calls)
motif studio open <run-id> # focus the viewer on a specific run
motif studio apply <concept-id>   # EXPERIMENTAL: interactive apply (needs runtime + compile-apply)
```

Aliases: `ii studio`, `oii studio`.

## Honest status

| Capability | Status |
|---|---|
| Local-first static viewer over `.motif/` + registry | implemented |
| Findings / concepts / decisions / runs browsing | implemented |
| Interactive **apply** | experimental |
| Live preview inside Studio | experimental (no browser runtime) |

## Safety

Studio is offline and read-only by default; it makes no network calls. The only state-changing
action, `apply`, is experimental, routes through the same worktree-isolated compile-apply path
as the CLI (rollback record, never touches `main`), and is clearly labelled as such in the UI.

## See also

- [`docs/atlas/README.md`](../atlas/README.md), the registry catalogue (Studio's read-side sibling)
- [`docs/architecture/motif-v3-live-architecture.md`](../architecture/motif-v3-live-architecture.md) §11
