# ADR 0001 — Architecture and safety baseline

- Status: Accepted
- Date: 2026-06-27
- Deciders: Motif maintainers

## Context

Motif is an Agent Skill + local knowledge system that
helps AI coding agents research, select, adapt and validate UI interactions, motion
and effects. The central risk is that "discover an effect on the web" naturally tempts
a system into scraping arbitrary sites and executing untrusted third-party code inside
a user's project. We must make that the hard path, not the easy one.

## Decision

1. **Intelligence over inventory.** The system reasons from product context → user
   intent → page type → interaction objective → pattern → effect → implementation.
   It searches for a *pattern* before an *effect*. It is not a component dump.

2. **Offline approved registry is the default runtime mode.** Internet retrieval only
   happens through an explicit `source refresh` / new-source workflow. Normal usage
   reads the committed local registry.

3. **Untrusted-by-default ingestion.** All externally retrieved material lands in
   `.motif/quarantine/` and is never executed during ingestion. It is statically scanned,
   licence-checked, dependency-inspected, then promoted to `reviewed/approved/rejected`.

4. **Dependency-free core.** The `motif` CLI and scanners use only the Python standard
   library so `make check` runs anywhere without installing packages. Optional tools
   (e.g. `jsonschema`) are used if present but never required.

5. **Vue and Frappe-Vue are first-class adaptation targets**, alongside browser-native
   and React. We never install one framework to obtain an effect for another.

6. **Accessibility and reduced motion are mandatory**, not optional flags. Performance
   budgets are explicit. Ranking is transparent and explains selection/rejection.

7. **Licence gate.** Unknown licence ⇒ `reference-only`, never `bundled`. Public
   visibility is not redistribution permission. Clean-room adaptation retains no source.

8. **Original code licence: MIT** (see ADR 0002). Third-party obligations always survive.

## Consequences

- The repository ships a working secure pipeline and a *representative*, high-confidence
  set of records for v0.1.0 rather than fabricated breadth.
- `make check` is the single local mirror of CI.
- A persistent `PHASE_STATUS.md` lets a later session continue without duplicating work.
