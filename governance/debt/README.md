# Interface Debt

**Interface Debt** is the measurable gap between the intended interaction model
(the design genome + interaction graph + decision ledger) and the realised UI.
Each instance is a **debt finding** conforming to `debt-finding.schema.json`:
`{ id, category, severity, evidence, weight, remediation }`.

## Core rule

> **Never a score without a breakdown and evidence.**

The Interface Debt Score is never reported as a bare number. Every score ships
with the per-category breakdown that produced it and, for every contributing
finding, concrete evidence (file + line, graph node/edge, or genome rule). A
finding with an empty `evidence` array is invalid and is rejected at validation.

## Categories

| Category | Meaning |
|----------|---------|
| `token-violation` | value bypasses a design token |
| `arbitrary-value` | hardcoded one-off (e.g. `p-[13px]`, raw hex) |
| `one-off-variant` | unsanctioned component variant |
| `duplicate-component` | a second component for an existing role |
| `unused-component` | component with no live usage |
| `custom-css-growth` | hand-written CSS escaping the system |
| `semantic-colour-inconsistency` | status colour used non-semantically |
| `missing-state` | async surface missing loading/empty/error |
| `accessibility-regression` | drop in contrast, focus, keyboard, ARIA |
| `motion-violation` | motion ignoring reduced-motion / motion budget |
| `responsive-failure` | breakpoint breakage |
| `dependency-growth` | new dependency for a solved problem |
| `bundle-growth` | route/bundle exceeds budget |
| `outdated-recipe` | component drifted from its recipe |
| `unapproved-exception` | genome deviation with no ledger exception |
| `provenance-gap` | UI element with no decision/evidence trail |

## Severity and weighting

Severity sets a base weight; the finding's `weight` may refine it within band.

| Severity | Base weight | Used for |
|----------|-------------|----------|
| `low` | 1 | cosmetic, isolated, no user impact |
| `medium` | 3 | systemic inconsistency, mild UX/a11y cost |
| `high` | 8 | broken state, accessibility regression, blocked task |

**Score** = sum of contributing finding weights, optionally normalised per 1,000
LOC or per surface for trend comparison. Categories touching accessibility and
missing states carry the heaviest severities because they break real tasks.

### This example

| Finding | Category | Severity | Weight |
|---------|----------|----------|--------|
| `task-board-missing-error-state` | missing-state | high | 8 |
| `duplicate-status-pill-component` | duplicate-component | medium | 4 |
| `kpi-card-arbitrary-values` | arbitrary-value | medium | 3 |

**Total = 15**, broken down as: missing-state 8, duplicate-component 4,
arbitrary-value 3 — always reported with this breakdown, never as "15" alone.

## CLI

```bash
# Compute the score from all findings — always emits the category breakdown
ii debt calculate governance/debt

# Explain a single finding: evidence chain, the rule broken, weight derivation
ii debt explain task-board-missing-error-state

# Show how the score has moved over time (requires historical snapshots)
ii debt trend governance/debt --since 2026-01-01

# Produce a prioritised, weight-ordered remediation plan from open findings
ii debt fix-plan governance/debt --order weight-desc
```

`calculate` never prints a bare number — it always includes the breakdown and the
evidence behind each contribution. `explain` justifies one finding, `trend` charts
movement, and `fix-plan` turns findings into an ordered backlog using each
finding's `remediation`.
