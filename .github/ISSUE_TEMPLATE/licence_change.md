---
name: Report a licence change
about: Report that an existing source's licence or redistribution terms have changed
title: "licence: <source> changed to <new licence>"
labels: [licence-change, governance, needs-review]
assignees: []
---

> A licence change can move a source from `redistributable` to `reference-only` (or force
> removal of bundled material). This is governance-critical. See
> [`LICENSE_POLICY.md`](../../LICENSE_POLICY.md) and
> [`THIRD_PARTY_SOURCES.md`](../../THIRD_PARTY_SOURCES.md). If this also affects a security
> posture, follow [`SECURITY.md`](../../SECURITY.md) instead of filing a public issue.

## Source identity

- **Source id / name (as recorded in `registry/sources/`):**
- **Official homepage:**
- **Official repository:**
- **Framework(s) affected:**

## Licence change

- **Previous licence (SPDX or exact name):**
- **New licence (SPDX or exact name):**
- **Effective version / date of the change:**
- **New redistribution class:** (redistributable / adaptable-concept / reference-only /
  rejected)
- **Attribution / notice changes:**
- **Licence confidence:** (high / medium / low)

## Provenance (required, how do you know?)

Links that prove the change against the **official** source (commit, release notes,
LICENSE file diff, blog post):

-
-

## Impact assessment

- **Records affected:** (recipes, components, effects, implementations that derive from it)
- **Currently bundled material that must be reclassified or removed?** (yes/no, which)
- **Trust-tier impact:** (does this change the trust tier or `status`?)

## Accessibility & reduced-motion

If material must be removed or replaced, note any accessibility or `prefers-reduced-motion`
behaviour that downstream recipes relied on, so the replacement preserves it.

## Performance

Note any performance characteristics (animated properties, budget) of affected material
that a replacement must match.

## Maintainer declaration

- [ ] The licence change is verified against the **official** source (links above), not
      assumed or second-hand.
- [ ] I have identified the records/material that need reclassification or removal.
- [ ] I understand unknown / source-available / Commons-Clause / premium terms mean
      `reference-only` at most, never bundled.
- [ ] **Popularity is not trust**, a widely used source losing a permissive licence still
      gets reclassified.
- [ ] AI assistance (if any) is disclosed and human-reviewed; licence facts were
      independently re-verified.
