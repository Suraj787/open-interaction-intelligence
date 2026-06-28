# Beta correction generalisation report

The corrections are validated across many product contexts and fixtures, not only BOSS. Data
is reproduced by `tests/test_evidence_query.py` and `tests/test_originality_scoring.py`.

## Evidence query across 11 contexts

| Context | Applicable | Blocking | Colour claim retained |
|---|---:|---:|:--:|
| minimal-generic | 110 | 55 | yes |
| boss-enterprise | 105 | 52 | yes |
| ecommerce-checkout | 110 | 55 | yes |
| government-form | 105 | 52 | yes |
| healthcare-high-risk | 105 | 52 | yes |
| factory-tablet | 110 | 55 | yes |
| desktop-mouse-only | 105 | 52 | yes |
| mobile-touch | 110 | 55 | yes |
| keyboard-only | 105 | 52 | yes |
| multi-purpose | 110 | 55 | yes |
| multi-risk | 110 | 55 | yes |

Reading: every context returns a useful, non-zero, ranked result. The universal colour-only
normative claim is retained everywhere. Contexts that constrain `devices` to a non-touch value
(desktop / keyboard-only / government / healthcare) return 105 because the 5 device-restricted
touch/pointer claims are correctly excluded; touch and device-silent contexts return all 110.
This proves the wildcard fix did not turn a device-restricted claim universal, and did not
suppress universal claims under added context dimensions.

## Originality across 8 fixtures

| Fixture | Score | Band | Expectation met |
|---|---:|---|:--:|
| enterprise-dashboard | 2 | low | not saturated |
| generic-ai-saas | 100 | high | detection preserved |
| branded-product | 0 | low | low |
| government-form | 0 | low | low despite simplicity |
| ecommerce-grid | 4 | low | context-aware (functional cards) |
| dev-tool-dense | 0 | low | low |
| repeated-bento-template | 85 | high | combined cliche detected |
| minimal-site | 0 | low | low |

## What this proves
- The evidence fix works across enterprise, ecommerce, government, healthcare, factory, and
  device/ability-specific contexts, not only BOSS.
- The originality fix still catches intentionally generic designs (generic-ai-saas 100,
  repeated-bento-template 85) while no longer saturating on legitimate UI.
- No broad suppression of findings: blocking counts (52-55) are stable and substantial across
  contexts; the normative accessibility core always surfaces.
- No normative accessibility claim was weakened: `claim-status-colour-001` remains normative,
  tier 1, blocking, and is retained in all 11 contexts.
- No context-specific restriction became universal accidentally: the 5 touch/pointer claims
  remain device-restricted and are excluded exactly in the non-touch contexts.

## Limitations
Static evidence only; originality confidence is capped at moderate. The corpus is 110 claims;
adding ontology dimensions in future must keep the matrix test green so this defect cannot
silently return.
