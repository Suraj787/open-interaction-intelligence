# Project Memory

Scoped, auditable memory that lets Motif remember decisions, preferences and **rejected
approaches** across runs. Status mirrors
[`docs/reviews/motif-v3-gap-analysis.md`](../reviews/motif-v3-gap-analysis.md) (§24:
**implemented**).

## What it does

- Stores typed memory entries (schema `schemas/memory.schema.json`) **scoped** to a project,
  surface or run.
- Records **rejected-approach memory** so a concept the team turned down is not re-proposed.
- Every write is **auditable**, who/what/when and why.

## Commands

```bash
motif memory add --scope project "prefer system fonts; no carousel on the homepage"
motif memory add --rejected "full-bleed hero video"   # remember a rejected approach
motif memory list --scope project                     # show entries in a scope
motif memory show <id>                                 # inspect one entry + its audit trail
motif memory forget <id>                               # remove an entry (recorded in the audit log)
```

Aliases: `ii memory`, `oii memory`.

## How it is used

- **Recommendation** and **concept generation** read memory to avoid re-suggesting rejected
  approaches and to honour standing preferences.
- `motif run` links the memory entries it consulted into the run record.

## Honest status

| Capability | Status |
|---|---|
| Scoped, typed memory entries | implemented |
| Rejected-approach memory | implemented |
| Auditable add / list / show / forget | implemented |

## Storage and safety

Memory lives under `.motif/` (gitignored runtime state). It is project-local, never sent
anywhere, and every mutation is appended to an audit trail, including `forget`, so history is
never silently rewritten.

## See also

- [`docs/architecture/motif-v3-live-architecture.md`](../architecture/motif-v3-live-architecture.md) §11
- [`docs/mcp/README.md`](../mcp/README.md), memory is exposed (guarded) over MCP
