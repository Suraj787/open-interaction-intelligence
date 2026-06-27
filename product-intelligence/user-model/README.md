# User Model

The user model answers: **who acts, how skilled are they, how often do they return, and
what are they trying to achieve?** It populates the `users` array of the
[Product Context Manifest](../../schemas/product-context.schema.json).

Each entry is one *role*, not one named person. A manifest usually has several: the
primary actor plus the secondary roles whose needs constrain the design.

## Fields (per user entry)

| Field | Required | Meaning |
|-------|----------|---------|
| `role` | yes | The acting role, kebab-case, e.g. `delivery-manager`, `bedside-nurse`, `shopper-purchaser`. |
| `expertise` | no | Skill with *this tool* and with the *domain*. They can differ — a nurse is a domain expert who may be a software novice. |
| `frequency` | no | How often the role uses the product: `daily`, `frequent`, `infrequent`, `on-demand`. Drives learnability vs efficiency. |
| `goals` | no | What this role is trying to accomplish, as outcomes. Ordered by importance. |

## How it is built

1. **Identify the primary actor first.** The brief usually names them (delivery manager,
   nurse, shopper). Everything else is calibrated around this role.
2. **Separate domain expertise from tool expertise.** This distinction changes the design
   profoundly: experts want density and keyboard speed; novices need guidance and few
   choices.
3. **Set frequency honestly**, because it trades off learnability against efficiency:
   - *Daily/frequent* → optimise for speed, recall, and throughput (the user will learn it).
   - *Infrequent/one-off* → optimise for first-use clarity (the user will not learn it).
4. **Write goals as outcomes, ranked.** "See the true status of every project at a glance"
   is a goal; "use the filter bar" is not. Goals become the spine of the workflow model.
5. **Add the constraining secondary roles** (e.g. the executive who reads but cannot learn
   the tool; the charge nurse who supervises). Leaving them out hides real requirements.

## How it is validated

- Every entry has a non-empty `role` (schema-enforced).
- The primary actor named in the brief appears and is recognisable.
- `frequency` and `expertise` are consistent with the workflows and the chosen
  information density (a daily expert with low density, or a one-off novice with high
  density, is a contradiction to resolve).
- Goals are outcomes, not features, and map to at least one workflow.

## Honesty rules

- A persona built from priors ("nurses are usually interrupted") is an **inference**, not
  a fact — record it in `inferred`, citing the prior.
- If the real user mix is unknown (which roles, what proportion), say so in `unresolved`
  rather than inventing a confident segmentation.
- Never inflate expertise or frequency to justify a design you already want.
