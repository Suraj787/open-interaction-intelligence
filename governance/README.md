# Governance Engine

The Governance engine is the part of **Interface Intelligence OS** that turns
*intent* about an interface into something **machine-checkable**, and then keeps
the realised UI honest against that intent over time. It answers three questions:

1. **What is this product's interface supposed to be?** → the **design genome**
2. **How is it supposed to behave?** → the **interaction graph**
3. **Why is it built this way, and where has it drifted?** → the **decision
   ledger**, **debt**, and **drift**

Everything here is data: JSON conforming to the schemas in `../schemas/`, plus
human-readable READMEs. Nothing is enforced by prose alone — every rule resolves
to a node, edge, finding, or genome field that the `ii` CLI can validate.

## Subsystems

| Directory | Schema | Purpose |
|-----------|--------|---------|
| `design-genome/` | `design-genome.schema.json` | Per-product DNA: brand & prohibited traits, colour semantics, typography, geometry, spacing, density, motion, confirmation/error/navigation patterns, accessibility & performance posture, framework & component conventions, exceptions, evidence. |
| `interaction-graph/` | `graph-node` / `graph-edge` | Typed nodes (user, role, task, workflow, screen, action, state, pattern, effect, recipe, component, constraint, evidence, test) and relations modelling intended behaviour. |
| `decision-ledger/` | `decision-ledger.schema.json` | Durable record of design decisions: problem, alternatives, decision, rationale, evidence, impacts, status, supersession. |
| `debt/` | `debt-finding.schema.json` | Interface Debt findings with category, severity, evidence, weight, remediation — and the Interface Debt Score. |
| `drift/` | — | Trend detection: divergence of the realised UI from the genome, graph, and ledger over time. |
| `exceptions/` | (genome `exceptions`) | Sanctioned, time-boxed deviations from genome rules. A deviation covered here is *governed*, not debt or drift. |
| `learning/` | — | Captured outcomes (usability results, A/B tests, audits) that raise genome `confidence` and feed back into decisions and patterns. |

## How the pieces connect

```
   design-genome ──governs──> interaction-graph ──realised by──> UI code
        ▲                          │                               │
        │                          │ queries surface gaps          │ scans surface findings
   learning (evidence)             ▼                               ▼
        ▲                       debt findings  ◄───────────────  debt/drift
        └──────── decision-ledger (why) ──── exceptions (sanctioned deviations)
```

- The **genome** governs the **graph** (constraints) and the UI (conventions).
- **Graph queries** find behavioural gaps (missing states, missing feedback,
  conflicting effects); **scanners** find code-level **debt findings**.
- The **ledger** records *why*; **exceptions** record *what is allowed to differ*.
- **Drift** watches the trend; **learning** feeds evidence back, raising genome
  `confidence` and informing new decisions.

## Worked example

This directory ships a full enterprise-project-dashboard example:

- Two genomes: `enterprise-pm-genome`, `marketing-saas-genome`.
- A 31-node / 40-edge interaction graph with six deliberate gaps.
- Three ledger decisions (table-over-cards, restrained-motion, no-particles).
- Three debt findings (missing-state, duplicate-component, arbitrary-value)
  totalling a **debt score of 15**, each tied to graph gaps and genome rules.

## Principle

> **Never a score, a verdict, or a "fix" without a breakdown and evidence.**

Every governance output — a debt score, a drift signal, a query result — must be
traceable to a node, edge, finding, genome field, or ledger entry. See each
subsystem's README for the relevant `ii` commands:
`ii graph build|validate|query|explain|render`,
`ii debt calculate|explain|trend|fix-plan`, and `ii drift detect|explain`.
