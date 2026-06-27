---
name: source-governance
description: Use when recording provenance, reviewing licences and costs, writing the decision log, or performing an explicit source-refresh to bring external references into the approved registry.
---

# Source Governance

**Responsibility:** Own provenance, licences, the decision log, and the only sanctioned
path to the internet — the explicit `source-refresh`.

## When to invoke

- Whenever a registry entry, external reference, or new dependency enters a decision.
- At the end of every task to write the decision log + provenance.

## Inputs

- Candidate sources, dependencies, ranking tables, and final selections.

## Outputs

- Provenance records (source, licence, retrieval date, approval status).
- A licence + cost review per dependency.
- The decision log entry for the task.

## How it connects

- Curates `registry/` entries; the default runtime is the **offline approved registry**.
- A `source-refresh` (via `python -m motif`) is the **only** way internet retrieval is
  allowed, and it must be explicit and recorded.

## Invariants

- Never copy restricted or licence-incompatible code into the registry or repo.
- Never add a dependency without a recorded licence + cost review.
- Never retrieve from the internet outside an explicit `source-refresh`.
- Every shipped interaction has a provenance entry.

## Notes

Offline-first is the default posture. Treat any unprovenanced or unlicensed candidate as
unusable until governance resolves it.
