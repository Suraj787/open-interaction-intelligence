# Beta correctness gap analysis

Branch `fix/beta-evidence-query-originality` from `main` (`9b61a50`). The `v3.0.0-beta.1`
tag is not touched. Two correctness defects found in the real BOSS audit are reproduced
deterministically below before any production logic is changed.

## Baseline (reproduced 2026-06-28)
- `make check`: 146 self-checks pass.
- Evidence query: minimal context (abilities only) returns **16** applicable claims; a
  realistic 8-dimension BOSS context returns **0**. Total claims: 110.
- Originality on BOSS (`apps/boss_v2/spa`): score **100/100**, "high convergence".

## Defect 1: evidence query over-filters rich contexts

### Reproduction
```python
from ii import evidence as ev
mini = {"abilities": ["colour-vision-deficiency"]}
rich = {"product_forms": ["enterprise-app","web-app","dashboard"], "purposes": ["monitor","configure"],
        "workflows": ["daily-operation","approval"], "expertise": ["domain-professional"],
        "abilities": ["keyboard-only","colour-vision-deficiency"], "risks": [{"type":"financial","severity":3}],
        "devices": ["desktop"], "environments": ["office"]}
len(ev.query(mini)["applicable_claims"])   # 16
len(ev.query(rich)["applicable_claims"])   # 0
```

### Root cause
The engine (`ii/evidence.py: applies()`) already treats an empty dimension as a wildcard,
but the **claim data** over-specifies. Every one of the 110 claims fills `product_forms`,
`purposes`, `workflows`, `expertise`, and `devices` with narrow values (0/110 leave these
empty). A universal normative principle such as `claim-status-colour-001` ("do not rely on
colour alone for status") is scoped to `web-app/dashboard, monitor, daily-operation, desktop,
office`. Matching is AND-across-dimensions, so any context that names a different value on
any co-specified dimension drops the claim. A richer context therefore matches fewer claims,
the opposite of correct behaviour: a universal claim must survive added context dimensions.

### Affected files
- `ii/evidence.py` (`applies`, `query`)
- `ux-evidence/claims/*.json` (110 files, over-specified applicability)
- `ux-evidence/schemas/evidence-claim.schema.json` (no way to mark hard vs soft dimensions)

### Fix model
Introduce an explicit `applicability.restrict` list naming the dimensions that are **hard
filters**; default `[]` means **universal** (wildcard on every dimension). Existing
applicability values are retained as **soft relevance/specificity signals** used only for
ranking, never for exclusion. A claim is excluded only when a dimension it lists in
`restrict` is constrained by both claim and context with no set-intersection. Only the
genuinely modality-specific claims (touch-input, pointer-gestures with `devices=[touch,mobile]`)
get `restrict: ["devices"]`. The query reports, per claim, match type, matched and wildcard
dimensions, a specificity score, and a human-readable reason.

### Acceptance criteria
- Universal normative claims survive every rich context (rule 8).
- Restricted claims match only intersecting contexts (rules 4, 5).
- More specific claims rank above universal ones (rule 6).
- Hypotheses never block; stale claims cannot newly block.
- Realistic BOSS context returns a useful non-zero result.
- Sources and limitations remain exposed; assumed context lowers confidence only.

## Defect 2: originality detector false-saturates

### Reproduction
`audit_path("apps/boss_v2/spa")` returns 100/100 from signals `excessive-rounded` (48),
`three-feature-cards` (22), `pill-overuse` (13), `gradient-hero` (9), `glass-blur` (7).

### Root cause
`score = min(100, raw * 4)` where `raw = sum(weight * min(count,5))` summed **per file**
across the whole tree. A few files using `rounded-2xl`, status pills, and `card` containers
saturate the score. The model has no diminishing returns, no concentration measure, no
design-system provenance, no product-context awareness, and no requirement that a strong
result come from a **combination** of cliche signals. Common Tailwind structure is treated
as proof of generic design.

### Affected files
- `ii/originality.py` (`audit_path`, `SIGNALS`, scoring)
- `ii/cli.py` (`cmd_originality` output)
- callers that consume the score: `ii/policy.py`, `ii/bench.py`, `ii/findings.py`,
  `ii/run.py`, `ii/mcp.py`

### Fix model
Tier the signals into marketing (strongest), decorative, and structural (weak). Score each
with diminishing returns (saturating in count), reduce structural signals for enterprise
product context and for design-system provenance, and require a combination of distinct
marketing/decorative signals for a high band. Cap confidence at moderate for static-only
evidence. Emit a signal-level breakdown (raw count, weighted score, context and provenance
adjustments, affected routes, explanation). Preserve detection of intentionally generic AI
fixtures.

### Acceptance criteria
- Enterprise dashboard: low or moderate, not saturated.
- Intentionally generic AI SaaS page: high, from explainable combined signals.
- Branded product and government form: low.
- Score deterministic and inspectable; Tailwind itself never labelled generic; no
  "AI-generated" classification.

## Regression risk
- Lowering originality scores could mask a genuinely generic design: mitigated by the
  generic-AI fixture test that must still score high.
- Wildcard semantics could make a restricted (e.g. touch-only) claim universal: mitigated by
  the desktop-mouse-only regression test that must exclude touch-only claims.
- Changing the score affects `policy.check` thresholds: re-verified by the v3 self-check and
  the policy regression test.
- All changes are additive to the schema (`restrict` optional) and preserve v2/v3 behaviour.
