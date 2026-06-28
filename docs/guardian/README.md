# Motif Guardian

A local + PR-time governance gate over staged or branch diffs, with trend tracking. Status
mirrors [`docs/reviews/motif-v3-gap-analysis.md`](../reviews/motif-v3-gap-analysis.md) (§22:
**implemented**).

## What it does

- Runs **policy as code**, originality and debt gates over a diff.
- Produces a pass / warn / fail verdict with a human-readable report.
- Ships a **GitHub Action** for PR enforcement and tracks **trends** over time.

## Commands

```bash
motif guard staged              # gate the currently staged changes (pre-commit)
motif guard branch              # gate the whole branch diff vs the base
motif guard explain <finding>   # why a gate fired, and how to resolve or suppress it
motif guard trend               # show governance trend history
```

Aliases: `ii guard`, `oii guard`. Install the pre-commit hook with `motif guard install-hook`.

## CI

A GitHub Action (under `.github/`) runs `motif guard branch` on pull requests, posting the
verdict and trend delta. The same binary runs locally and in CI, so results match.

## Honest status

| Capability | Status |
|---|---|
| `motif guard staged` / `branch` | implemented |
| Policy / originality / debt gates | implemented |
| GitHub Action | implemented |
| Trend commands | implemented |

## Safety

Guardian is read-only over your diff, it reports and gates, it never edits code. Policy
verdicts are explainable (`guard explain`) and suppressible only with a reason + expiry,
recorded as findings.

## See also

- [`docs/policies/README.md`](../policies/README.md), the policy language Guardian enforces
- [`docs/architecture/motif-v3-live-architecture.md`](../architecture/motif-v3-live-architecture.md) §9
