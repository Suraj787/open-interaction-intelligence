# Product Model

The product model answers the most basic question: **what is this product, and why does
it exist?** It populates the `product` object of the
[Product Context Manifest](../../schemas/product-context.schema.json).

## Fields

| Field | Required | Meaning |
|-------|----------|---------|
| `type` | yes | A concrete product category (kebab-case noun phrase), e.g. `enterprise-project-management-application`, `ecommerce-checkout-flow`. |
| `purpose` | yes | One sentence: the job the product does for its user. Outcome-oriented, not feature-oriented. |
| `business_model` | no | How it sustains itself, e.g. `b2b-saas-seat-based`, `b2c-transactional-retail`. Shapes incentives. |
| `audience` | no | One of `internal`, `public`, `mixed`. Drives polish, trust, and threat assumptions. |
| `maturity` | no | `prototype`, `established`, `established-regulated`, etc. Governs appetite for change. |
| `regulatory_sensitivity` | no | Named regimes and why they apply (PCI-DSS, HIPAA, GDPR…). Feeds the risk model. |

## How it is built

1. **Classify the product type** from the brief, the repository (routes, dependencies,
   domain language), or the live product. Prefer a specific category over a generic one.
2. **State the purpose as an outcome.** "Convert intent-to-buy into a paid order" beats
   "a checkout page". The purpose is the yardstick every later trade-off is measured by.
3. **Make the website-vs-application call explicit** where relevant (see the
   `product-context-analysis` skill): websites optimise persuasion; applications optimise
   task throughput. This single call cascades through every downstream decision.
4. **Record audience and regulatory sensitivity** because they set the floor for the risk
   and environment models — an `internal` tool and a `public`, PCI-bound flow demand
   different defaults.

## How it is validated

- `type` and `purpose` are present and non-empty (schema-enforced).
- `audience`, if present, is within the enum (`ii product validate` checks this).
- `type` is specific enough that two reviewers would classify it the same way.
- `purpose` describes a user outcome, not a UI artefact.
- Anything claimed here that is not directly evidenced (e.g. an assumed business model)
  is mirrored into `assumptions` in the manifest — see
  [`confidence/`](../confidence/README.md).

## Honesty rules

- Do not upgrade a *plausible* product type to a *verified* one without evidence; if the
  category was inferred from dependencies rather than stated, say so in `inferred`.
- `regulatory_sensitivity` is a hypothesis until the jurisdiction is confirmed. If unsure,
  state the likely regime and add the jurisdiction question to `unresolved`.
