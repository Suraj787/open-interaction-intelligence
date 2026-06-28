# BOSS beta audit: before vs after corrections

Same target (`apps/boss_v2/spa`), same read-only audit-only mode, same context vector. Before
= `v3.0.0-beta.1` (`docs/releases/boss-beta-audit.md`). After = branch
`fix/beta-evidence-query-originality`.

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| Applicable evidence claims | 0 | 105 | Over-filtering fixed; universal claims now survive the rich context |
| Universal claims retained | 0 | 105 | All non-device-restricted claims apply (5 touch claims correctly excluded for desktop) |
| Context-specific claims | 0 | 105 | Every applicable claim matched >=1 context dimension and is ranked by specificity |
| Blocking findings | 0 | 52 | Normative tier-1 accessibility requirements now correctly surface as blocking |
| Originality score | 100 | 19 | False saturation removed; legitimate enterprise Tailwind no longer reads as generic |
| Originality confidence | high band, none reported | low (capped) | Static-only evidence now caps confidence honestly |
| False positives | originality saturated (3 structural signal classes) | 0 in originality | Structural signals down-weighted by context + provenance |
| Unsupported assumptions | 3 (risks, abilities, environments) | 3 (unchanged) | Same assumptions; now correctly lower confidence to medium instead of being ignored |
| Browser completion | not-executed (local) | not-executed (local) | Unchanged; browser proof remains CI-only on the fixture |
| BOSS files modified | 0 | 0 | Read-only contract preserved |

## Honest reading
The corrections turn an unusable evidence result (0 claims) into a useful, ranked, explainable
105-claim result, and turn a misleading originality verdict (100/generic) into a defensible
one (19/low) without weakening detection: the intentionally generic AI fixture still scores
100 and the repeated bento template scores 85. The static finding detectors and the BOSS
read-only guarantee are unchanged. Browser steps remain not-executed locally; that limitation
is not addressed by this change and is not claimed to be.
