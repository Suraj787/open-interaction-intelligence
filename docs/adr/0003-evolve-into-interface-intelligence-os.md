# ADR 0003 — Evolve Motif into Interface Intelligence OS

- Status: Accepted
- Date: 2026-06-28
- Supersedes scope of: ADR 0001 (extends, does not replace the safety baseline)

## Context

The existing repository (originally Open Interaction Intelligence, renamed Motif, released
v1.0.0) is a complete and validated **secure interaction foundation**: registry, schemas,
five scanners, secure-source pipeline, transparent ranking, controlled installer, and
framework adapters with Vue and Frappe-Vue as first-class targets.

The Interface Intelligence OS specification treats that foundation as **one engine** (the
Interaction Intelligence Engine plus the Secure Component Supply Chain) inside a larger
platform with six engines: Design Intelligence, Product Intelligence, Interaction
Intelligence, Implementation Intelligence, Assurance, and Governance and Learning. The
spec's Phase 0 directs: when a compatible repository exists, **preserve its history** and
**migrate**, rather than start from scratch.

## Decision

1. **Evolve in place, on a branch.** Build Interface Intelligence OS on the
   `interface-intelligence-os` branch so `main` keeps the intact, validated Motif v1.0.0.
   Git history is preserved. The publish decision (rename the GitHub repo vs publish as a
   new repo) is deferred to a human at release time; nothing is renamed or pushed without
   confirmation.

2. **`ii` is the primary CLI; `oii` and `motif` are compatibility aliases.** No breaking
   change for existing users of the foundation.

3. **Reuse, do not rebuild, the foundation.** The existing `registry/`, `scanners/`,
   `security/`, `connectors/`, `ingestion/`, `adapters/`, `implementations/` and the
   interaction skills become the Interaction Intelligence Engine and Secure Supply Chain.
   New engines are added alongside them.

4. **Target a strong, honest v0.2.0.** Implement functioning foundations for the new
   engines (product context, design intelligence schemas plus curated data, design genome,
   interaction graph, originality analysis, motion and density grammars, state
   completeness, assurance evidence model, decision ledger, debt and drift, InterfaceBench
   foundation, the Interface Specification Language). Anything that cannot be responsibly
   completed is marked `experimental` or `planned` in a capability matrix, never claimed
   as implemented.

5. **Dependency-free core preserved.** New tooling continues to use only the Python
   standard library so `make check` runs anywhere.

## Consequences

- `main` remains shippable as Motif v1.0.0 throughout the evolution.
- A capability matrix becomes the source of truth for implemented vs experimental vs
  planned, enforced by honesty in the README and `PROJECT_STATUS.md`.
- The release will be tagged only when it meets its own definition of done.
