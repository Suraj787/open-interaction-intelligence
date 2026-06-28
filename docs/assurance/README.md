# Browser Assurance

Checks a (running) interface against accessibility, performance, behaviour and visual
baselines, emitting typed evidence that feeds the policy gate. Status mirrors
[`docs/reviews/motif-v3-gap-analysis.md`](../reviews/motif-v3-gap-analysis.md) (§8:
**experimental**, interface + static-check layers implemented; runtime layers require
Playwright, which is not installed here. §18 semantic visual comparison: **experimental**).

## Layers

| Layer | What it checks | Status |
|---|---|---|
| Static config / token checks | tokens, config, declared a11y attrs | implemented |
| Pattern / anti-pattern checks | known-bad interaction patterns | implemented |
| Accessibility (axe) | runtime a11y violations | experimental |
| Performance trace | real load/interaction metrics | experimental |
| Behaviour (Playwright) | flows actually work | experimental |
| Visual regression / semantic diff | pixel + structural + semantic diff vs baseline | experimental |

Every check writes an `assurance-evidence` record (schema
`schemas/assurance-evidence.schema.json`) that the policy gate consumes.

## Commands

```bash
motif assure --target ./app                    # run the static + interface layers, emit evidence
motif assure --target ./app --baseline main    # compare findings against a recorded baseline
motif assure --runtime   # EXPERIMENTAL: axe + perf + Playwright + visual diff (needs a browser)
motif assure visual-diff --baseline <id>       # EXPERIMENTAL: pixel/structural/semantic diff
```

Aliases: `ii assure`, `oii assure`.

## Semantic visual comparison (§18)

The schema and CLI exist; pixel, structural and semantic diffs all need **rendered
screenshots** from the Visual Twin, so they are experimental until a browser runtime is
present. Without one, `visual-diff` reports "no rendered baseline" rather than a fake score.

## Honest status

- **Implemented:** interface + static-check layers, evidence records, policy gating.
- **Experimental:** every layer that requires running a browser (axe, perf, Playwright,
  visual regression / semantic diff).

## Safety

Runtime assurance only runs under `--runtime` and against an isolated worktree. Results are
never inferred, a layer that cannot execute is reported as not executed.

## See also

- [`docs/visual-twin/README.md`](../visual-twin/README.md), [`docs/policies/README.md`](../policies/README.md)
- [`docs/architecture/motif-v3-live-architecture.md`](../architecture/motif-v3-live-architecture.md) §7
