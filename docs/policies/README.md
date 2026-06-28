# Policy as Code

Declarative policies that gate findings, debt and originality across `motif run`, Guardian
and assurance. Status mirrors
[`docs/reviews/motif-v3-gap-analysis.md`](../reviews/motif-v3-gap-analysis.md) (§23:
**implemented**).

## What it does

- Defines policy in YAML against `schemas/policy.schema.json`.
- Sets thresholds and gates for accessibility, performance, licensing, originality and debt.
- The same policy drives the CLI gate, Guardian, and the assurance policy gate, one source
  of enforcement.

## Bundled profiles

Ready-made policies live in [`policies/`](../../policies/):

- `accessibility.yml`, `performance.yml`, `licensing.yml`,
  `enterprise-ui.yml`, `marketing-ui.yml`

## Commands

```bash
motif policy init            # scaffold a policy file for this project
motif policy validate        # check a policy against the schema
motif policy check --target ./app   # evaluate the active policy, emit a verdict
motif policy explain <rule>  # explain a rule: what it gates and why it fired
```

Aliases: `ii policy`, `oii policy`.

## Honest status

| Capability | Status |
|---|---|
| Policy schema | implemented |
| `init` / `validate` / `check` / `explain` | implemented |
| Gates findings / debt / originality | implemented |
| Gating of **runtime** assurance evidence | depends on experimental runtime layers |

Policy evaluation itself is fully implemented. Where a policy references a runtime metric
(e.g. a real performance trace), that input is only available when the experimental browser
runtime is present; the policy engine reports the input as unavailable rather than passing it
silently.

## Safety

Policies are explicit and explainable. Suppressions require a reason and an expiry and are
recorded as findings, so a gate can never be silently disabled.

## See also

- [`docs/guardian/README.md`](../guardian/README.md), [`docs/assurance/README.md`](../assurance/README.md)
- [`docs/architecture/motif-v3-live-architecture.md`](../architecture/motif-v3-live-architecture.md) §9
