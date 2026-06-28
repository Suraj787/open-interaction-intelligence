# InterfaceBench, the runner

InterfaceBench is Motif's benchmark for interface quality. The **benchmark definition** (cases,
rubric, longitudinal scenario) already lives in [`interfacebench/`](../../interfacebench/);
this page documents the **runner**, `motif bench`. Status mirrors
[`docs/reviews/motif-v3-gap-analysis.md`](../reviews/motif-v3-gap-analysis.md) (§25:
**partial**, `motif bench run` executes automated measures over fixtures; model and human
rubric scoring are kept separate).

## What it does

- Executes the **automated measures** defined in the benchmark over the case fixtures.
- Keeps **model-scored** and **human-rubric** results separate, automated numbers are never
  blended with rubric judgement.
- Emits an `evaluation` record (schema `schemas/evaluation.schema.json`) per case.

## Commands

```bash
motif bench run                       # run automated measures over all cases in interfacebench/cases
motif bench run --case <id>           # run a single case
motif bench report                    # summarise the latest run
motif bench rubric --case <id>        # print the human rubric to score by hand (not auto-scored)
```

Aliases: `ii bench`, `oii bench`.

## What is and isn't automated

| Part | Status |
|---|---|
| Automated measures over fixtures | implemented |
| Per-case evaluation records | implemented |
| Model vs human rubric separation | implemented |
| Measures that need a **rendered** interface | experimental (browser runtime absent) |

Any measure requiring a running/rendered interface is reported as not executed when no browser
runtime is present, rather than being estimated.

## Honest status

§25 is **partial**: the runner and automated measures work; rubric-based and rendered-measure
scoring are intentionally human / runtime-gated.

## See also

- [`interfacebench/README.md`](../../interfacebench/README.md), the benchmark definition
- [`interfacebench/rubric.md`](../../interfacebench/rubric.md), [`interfacebench/longitudinal-scenario.md`](../../interfacebench/longitudinal-scenario.md)
- [`docs/assurance/README.md`](../assurance/README.md)
