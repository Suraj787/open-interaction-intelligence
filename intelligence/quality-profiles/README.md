# Quality Profiles

A quality profile is a **preset of constraints** that tunes the selection model
(`../selection-policies/`) for a class of product. It is chosen from the product
type (`../product-types/`) and then refined per page.

Each profile is a YAML file with these keys:

| Key | Meaning |
|---|---|
| `goals` | What this profile optimises for, in priority order. |
| `preferred_patterns` | Patterns this profile reaches for first. |
| `restricted_effects` | Effects to avoid or forbid in this context. |
| `continuous_motion_policy` | Stance on forever-animating effects. |
| `dependency_budget` | How freely animation libraries may be added. |
| `performance_budget` | Frame-rate / payload / main-thread expectations. |
| `max_high_attention_effects_per_viewport` | Cap on attention-grabbing effects visible at once. |
| `reduced_motion_policy` | How `prefers-reduced-motion` is honoured (always mandatory). |
| `mobile_constraints` | Touch/small-screen/low-power rules. |

## Profiles

- `enterprise-strict.yml`, dense internal tools, ERP/financial. Maximum restraint.
- `saas-balanced.yml`, consumer/B2B SaaS apps. Useful polish, task-first.
- `marketing-expressive.yml`, SaaS marketing & corporate sites. Brand-forward.
- `ecommerce-conversion.yml`, storefronts. Lively browse, calm checkout.
- `documentation-calm.yml`, docs & reference. Near-zero motion.
- `editorial-storytelling.yml`, publications & case studies. Narrative set-pieces.
- `portfolio-creative.yml`, portfolios & agencies. Signature expression.
- `experimental.yml`, immersive/showcase. Highest licence, hard fallbacks.
- `low-power-device.yml`, constraint overlay for weak hardware.
- `accessibility-first.yml`, constraint overlay where inclusion leads everything.

## Page-level overrides

A profile sets the **baseline** for a whole product, but individual pages can
**tighten** it. Overrides follow two rules:

1. **Tighten freely, loosen with justification.** Any page may be *more*
   restrained than the profile (e.g. the checkout page under
   `ecommerce-conversion` adopts near-`enterprise-strict` restraint). Loosening
   beyond the profile requires an explicit objective that demands it.
2. **Most-restrictive-wins on overlays.** `low-power-device` and
   `accessibility-first` are **overlays**: when active, their constraints are
   intersected with the base profile and the stricter value always wins. They
   can never be loosened by a page override.

Resolution order for any given screen:

```
base profile  →  page-type tightening  →  active overlays (low-power / a11y)
                                          (most restrictive wins)
```

The resolved constraint set is then fed into the selection model as budgets and
gates. This keeps every recommendation traceable: *profile → page override →
overlay → final budget*.
