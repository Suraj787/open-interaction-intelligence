# Confidence Model

> **The system must not invent certainty.**

The confidence model is what makes every other sub-model trustworthy. It records *how much
of the manifest is actually known*, and it forces every claim to declare its epistemic
status. It populates `confidence`, `verified`, `inferred`, `assumptions`, `unresolved`,
and `evidence` in the
[Product Context Manifest](../../schemas/product-context.schema.json).

## The four buckets

Every claim in a manifest belongs to **exactly one** of these. They are ordered by how
much we can rely on them.

| Bucket | Definition | Source | Treat as |
|--------|------------|--------|----------|
| `verified` | Directly evidenced — stated in the brief, observed in the product, or measured in telemetry. | Evidence in hand. | Fact. |
| `inferred` | Derived by reasoning from verified facts or domain priors. Plausible, not confirmed. | Logic over evidence. | Working hypothesis — flag the basis. |
| `assumptions` | Taken as true to proceed, with no evidence either way. | Convenience / default. | Cheap to be wrong — revisit early. |
| `unresolved` | Known unknowns. Questions whose answers would change the design. | Absence of evidence. | Work to be done; never a silent gap. |

The discipline: **never let a claim drift up a row without new evidence.** An inference
does not become verified because you grew confident in it; it becomes verified when
someone observes or measures it and records that in `evidence`.

## Why the distinction matters

A manifest that blurs these buckets is dangerous: a reader cannot tell which lines to
trust, so they either over-trust a guess or distrust everything. By contrast, an honest
manifest lets a reviewer attack exactly the soft claims. The cheapest correction in the
whole pipeline is a stakeholder reading `ii product explain` and saying "that inference is
wrong" — but that only works if the inference was labelled as one.

## The `confidence` number (0-1)

`confidence` is a single scalar summarising how grounded the manifest is **as a whole**.
It is not a vibe; it should track the verified/inferred/assumption split:

- Mostly `verified`, few open `unresolved` → high (≈ 0.8-0.95).
- Healthy mix of `verified` and reasoned `inferred`, some `assumptions` → moderate
  (≈ 0.5-0.7).
- Built largely from priors and `assumptions`, several material `unresolved` → low
  (≈ 0.3-0.5).
- Almost nothing grounded → very low (< 0.3) — and that is a valid, honest manifest.

The worked examples in [`manifests/`](../manifests/) sit at 0.5-0.62 on purpose: they were
authored from a short brief and domain priors only, with no telemetry, interviews, or
repository access — so most lines are `inferred` or `assumptions`, and the number says so.

### Anti-pattern

Reporting 0.9 confidence on a manifest whose `verified` list has two lines and whose
`assumptions` list has eight. That is inventing certainty. `ii product validate` flags a
`confidence` that is inconsistent with the bucket split.

## How it is built

1. As each sub-model is authored, file every claim into one bucket. If you cannot evidence
   it, it is at best `inferred` (state the basis) or `assumptions`.
2. Record what each verified/inferred claim rests on in `evidence` (brief line, telemetry,
   observation, or "inference-only").
3. Turn every "we don't know" into an explicit `unresolved` line, phrased as the question
   to answer.
4. Set `confidence` to reflect the resulting balance — and resist rounding it up.

## How it is validated

`ii product validate` checks:

- `confidence` is a number in `[0,1]`.
- No claim appears in more than one bucket.
- `verified` claims are backed by an `evidence` entry that is not "inference-only".
- `confidence` is broadly consistent with the verified-vs-(inferred+assumption) ratio.
- `unresolved` is non-empty unless the manifest is genuinely, evidentially complete (an
  empty `unresolved` with low confidence is itself suspicious).

## Promotion and decay

- **Promotion**: an `inferred` or `assumptions` line moves to `verified` only when new
  evidence is added to `evidence`. Re-run `ii model-product` so `confidence` rises with it.
- **Decay**: when the product or its users change, previously verified lines may become
  stale. Re-inspect; do not let yesterday's fact masquerade as today's.
