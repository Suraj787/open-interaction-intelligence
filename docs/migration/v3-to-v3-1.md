# Migrating from Motif v3.0.0 to v3.1 "Evidence-Grounded Runtime"

> v3.1 is **additive**. It adds the UX Evidence Graph and an evidence-grounded, browser-driven
> audit-and-repair loop on top of v3.0.0 ("Motif Live") **without removing anything**. v2 and v3
> compatibility is preserved. Status throughout mirrors
> [`docs/reviews/motif-v3-1-gap-analysis.md`](../reviews/motif-v3-1-gap-analysis.md) and
> [`ADR-UXE-001`](../adr/ADR-UXE-001-release-and-integration-strategy.md). For the v2→v3 step,
> see [`v2-to-v3.md`](v2-to-v3.md).

## What is preserved (unchanged)

- **All v2 and v3 CLI commands** keep working with the same flags and output contract:
  `validate`, `doctor`, `search`, `rank`, `rank-sources`, `source`, `component`,
  `generate-index`, plus the v3 runtime verbs (`run`, `improve`, `bench`, `guardian`, `studio`,
  `atlas`, `genome`, …).
- **All three command names**: `motif` and the aliases `ii` and `oii`.
- **Every existing schema** in `schemas/`, none removed, none renamed. v3.1 adds new schemas
  *alongside* them.
- **The registries, scanners, licence gate and provenance** are unchanged.
- **The `make check` gate stays dependency-free** and remains the line for what may be claimed
  as implemented. The new Evidence Graph and deterministic repair path are inside it.

> No schema is removed and no existing command changes behaviour. v2 and v3 workflows run on
> v3.1 unchanged.

## What is added in v3.1

### 1. New `ux-evidence/` data layer
A version-controlled evidence layer (not a graph DB, not an encyclopedia) under
[`ux-evidence/`](../../ux-evidence/):

```
ux-evidence/
  ontology/        # 9 dimensions, controlled vocab
  schemas/         # source, evidence-claim, myth, contradiction,
                   # validation-method, evidence-pack, context-vector (+ query-result)
  sources/         # source metadata (no full articles)
  claims/          # tier 1-6 evidence claims
  myths/           # the myth register
  contradictions/  # recorded disagreements
  packs/           # pack-enterprise, pack-public-service, pack-ecommerce
  validations/     # val-… methods
  indexes/         # generated
```
See [`../ux-evidence/overview.md`](../ux-evidence/overview.md).

### 2. New `motif evidence …` commands
```bash
motif evidence validate                  # schema-validate the layer (part of make check)
motif evidence index                     # regenerate ux-evidence/indexes/
motif evidence query --context <file>    # context vector → applicable claims/warnings/blocked/validations/conflicts
motif evidence query --pack <pack-id>    # query a pack's context
motif evidence explain <claim-id>        # why it applied / what lowered confidence
motif evidence check-myth "<statement>"  # test a direction against the myth register
```

### 3. New `motif app …` commands (app runner)
```bash
motif app detect --target ./app          # deterministic
motif app start  --target ./app          # EXPERIMENTAL (needs the browser extra)
motif app stop   --target ./app
motif app rollback <run-id>              # reversible
```
See [`../runtime/browser-assurance.md`](../runtime/browser-assurance.md).

### 4. Optional `[browser]` extra
```bash
pip install "motif[browser]"   # Playwright + axe, OPTIONAL, never required by the base CLI
```
The base CLI, `make check` and the Evidence Graph run without it. Browser steps degrade to the
`not-executed` state when the extra is absent. See
[`../ux-evidence/browser-integration.md`](../ux-evidence/browser-integration.md).

### 5. Evidence-grounded repair + integration
- The [21-step golden loop](../improve/evidence-grounded-repair.md) grounds every repair in a
  claim, drops unsupported findings, applies in an isolated worktree and pre-computes rollback.
- Guardian uses the Evidence Graph for changed files; Studio displays evidence + before/after
  (read-only); InterfaceBench gains the
  [Vue dashboard evidence-repair scenario](../interfacebench/vue-dashboard-evidence-repair.md).

## What you have to do to migrate

**Nothing is mandatory.** v3.1 is drop-in:

```mermaid
flowchart TD
  A[On v3.0.0] --> B[Pull v3.1: ux-evidence/ + new commands appear]
  B --> C{Want browser audit/repair?}
  C -- no --> D[Use deterministic evidence query, grounding, repair plan, reports]
  C -- yes --> E[pip install 'motif[browser]' + playwright install]
  D --> F[make check passes, dependency-free]
  E --> F
```

1. Update; the `ux-evidence/` layer and the `motif evidence` / `motif app` commands appear.
2. `make check` continues to pass without the browser extra.
3. Install `motif[browser]` **only** if you want live capture/validation (experimental;
   `not-executed` where no runtime is available).

## Nothing removed; v2/v3 compatibility preserved

No command, schema, registry or output contract from v2 or v3 is removed or altered. The only
*risky* new action (live process start) is opt-in, isolated to a git worktree, and reversible.

## Tagging note

Per [`ADR-UXE-001`](../adr/ADR-UXE-001-release-and-integration-strategy.md), v3.1.0 is **not
tagged** until a separate browser CI job runs the golden loop successfully. In environments
without a browser runtime, the deterministic work is complete and validated, and the release is
held with browser steps reported `not-executed`. No browser result is ever fabricated.
