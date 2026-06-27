# Drift Detection

**Drift** is the gradual divergence of the realised UI from its governing
intent over time. Where a **debt finding** is a single point-in-time defect,
**drift** is the *trend* — the slow accumulation of small deviations that erode
the design genome, the interaction graph, and the decisions in the ledger.

Drift is detected by comparing successive snapshots of the codebase, the
compiled interaction graph, and the debt findings against three baselines:

1. **Design genome** (`../design-genome/`) — tokens, traits, conventions, postures.
2. **Interaction graph** (`../interaction-graph/`) — required states, feedback,
   constraints, governance edges.
3. **Decision ledger** (`../decision-ledger/`) — active decisions that must hold
   until explicitly superseded.

## Drift signals

| Signal | What it detects |
|--------|-----------------|
| **Token drift** | rising share of arbitrary values vs tokenised ones |
| **Genome drift** | components diverging from declared conventions / prohibited traits |
| **State drift** | new async surfaces shipping without loading/empty/error states |
| **Motion drift** | effects added without reduced-motion handling |
| **Decision drift** | code contradicting an `active` ledger decision with no supersede |
| **Provenance drift** | growing share of UI with no decision/evidence trail |
| **Score drift** | Interface Debt Score trending up over consecutive snapshots |

Drift is reported as a **direction and rate**, always with the contributing
findings and graph paths — like the debt score, **never a bare number without a
breakdown and evidence.** A genome with a low `confidence` widens drift
tolerances; a high-confidence genome tightens them.

## Relationship to debt and exceptions

- New deviations become **debt findings** (`../debt/`).
- A deviation sanctioned by an entry in the genome `exceptions` array or an
  `active` decision is **not** drift — it is governed.
- An unsanctioned deviation against an active decision is **decision drift** and
  is escalated, citing the decision it contradicts.

## CLI

```bash
# Detect drift by diffing the current state against the governance baselines
ii drift detect --baseline governance --since 2026-04-01

# Explain a specific drift signal: which findings/edges drive it, and the trend
ii drift explain token-drift --baseline governance/design-genome
```

`detect` surfaces the signals and their direction/rate with full breakdowns;
`explain` traces a single signal back to the findings, graph paths, and genome or
ledger rules that produced it. Drift output feeds `ii debt fix-plan` to convert a
worsening trend into a prioritised remediation backlog.
