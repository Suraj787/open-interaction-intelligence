---
name: governance
description: Use when decisions, provenance, design genome, interaction graph, debt, and drift must be recorded and reconciled so the system learns and stays accountable.
---

# Governance and Learning

**Responsibility:** Persist *why* every decision was made and *where* it came from, keep
the design genome and interaction graph current, and track debt and drift over time.

## When to invoke

- Steps 6-7 (load/build genome and graph) and steps 17-18 (record, debt, drift).

## Inputs

- Decisions and rationale from every prior step; sources and licences; the built UI.

## Outputs

- **Design Product Genome** extracted or updated.
- **Interaction Specification Graph** built or updated.
- **Decision ledger** entries with rationale, confidence, and provenance.
- **Debt** items opened and **drift** reconciled against genome and graph.
- **Exceptions** recorded where a hard rule was justifiably relaxed.

## Engine data + CLI

- Reads/writes `governance/` (`design-genome`, `interaction-graph`, `decision-ledger`,
  `debt`, `drift`, `exceptions`, `learning`).
- `ii genome`, `ii graph`, `ii ledger`, `ii debt`, `ii drift`.

## Notes

Record provenance for anything sourced externally. Mark inferences with a confidence
level; never log an inference as verified fact. Every justified hard-rule exception must
be explicit and traceable.
