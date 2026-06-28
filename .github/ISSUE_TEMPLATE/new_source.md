---
name: Propose a new source
about: Propose adding a library, design system or reference to the registry
title: "source: <name>"
labels: [new-source, needs-review]
assignees: []
---

> Cataloguing a source does **not** imply a right to redistribute it. Please read
> [`LICENSE_POLICY.md`](../../LICENSE_POLICY.md) and
> [`THIRD_PARTY_SOURCES.md`](../../THIRD_PARTY_SOURCES.md) first. Unknown licence ⇒
> `reference-only`, never bundled. Bundling requires a verified permissive licence **and**
> trust tier ≥ 3.

## Source identity

- **Name:**
- **Category:** (e.g. animation-engine, accessible-ui-foundation, design-system, reference)
- **Official homepage:**
- **Official repository:**
- **Frameworks supported:** (vanilla / react / vue / svelte / …)

## Licence

- **Licence (SPDX or exact name):**
- **Canonical licence URL (`license_reference`):**
- **Is it source-available / Commons-Clause / premium?** (yes/no, if yes, it is
  reference-only at most)
- **Attribution required?** (yes/no, what notice?)
- **Licence confidence:** (high / medium / low)

## Redistribution class

Pick one (see `LICENSE_POLICY.md`):

- [ ] redistributable (verified permissive OSS / open standard)
- [ ] adaptable-concept (learn the concept; clean-room original only)
- [ ] reference-only (unknown / guidance / premium / source-available)
- [ ] rejected

## Trust tier (1-5)

- **Proposed trust tier:**
- **Rationale:** (maintenance, provenance clarity, accessibility maturity, security
  posture; tier 5 = reference-only/rejected)

## Evidence

Provide links and notes that support the licence, redistribution and trust assessment
(homepage, repo, licence file, NOTICE, release cadence, security history):

-
-

## Why Motif should include it

What interaction problem / pattern does it serve? Website vs web application? Vue /
Frappe-Vue relevance?

## Accessibility & reduced-motion

- **Keyboard / focus / semantics:** (how usable is it without a pointer? ARIA quality?)
- **`prefers-reduced-motion` support:** (built-in / partial / none, and the documented
  fallback)
- **Essential-status reliance on motion or hover:** (any? how is it mitigated?)

## Performance

- **Animated properties:** (transform/opacity only, or layout-affecting?)
- **Bundle / runtime cost:** (approx size, dependencies, main-thread work)
- **Behaviour under dense UIs / low-end devices:** (notes, budgets, known jank)

## Maintainer declaration

- [ ] I am proposing this in good faith and have linked **official** sources only.
- [ ] To the best of my knowledge the licence facts above are accurate as of the date
      filed, and I understand a maintainer will independently re-verify them.
- [ ] I am **not** asking Motif to bundle source-available / Commons-Clause / premium code.
- [ ] **Popularity is not trust**, I have justified the trust tier on provenance,
      maintenance and accessibility, not download counts or stars.

## Checklist

- [ ] Licence verified against the official source (not assumed).
- [ ] Confirmed it is not source-available / Commons-Clause / premium (or marked
      reference-only).
- [ ] Evidence links included.
- [ ] I understand a maintainer will re-verify before any bundling.
- [ ] AI assistance (if any) is disclosed and human-reviewed.
