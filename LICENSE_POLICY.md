# Licence Policy

This policy governs how Motif treats third-party material and how it decides what may be
**redistributed**, **adapted as a concept**, kept **reference-only**, or **rejected**.
Original Motif code is MIT-licensed (see [`LICENSE`](LICENSE)); that licence covers only
original code and **never overrides a third-party source's own licence or obligations**.

Licence records live in [`registry/licenses/`](registry/licenses/) and each source carries
a `license`, `license_reference`, `redistribution` class, `attribution_required`,
`trust_tier`, `confidence` and `status` field. See
[`THIRD_PARTY_SOURCES.md`](THIRD_PARTY_SOURCES.md) for the source-by-source summary.

## The LICENCE GATE

> **Unknown licence ⇒ `reference-only`, never bundled.**

Before any third-party material can move from quarantine toward approval, its licence must
be identified and verified. A source is treated as `reference-only` (at most) whenever:

- the licence is unknown, missing, ambiguous, or only stated informally;
- the terms are **source-available** or carry a **Commons-Clause** rider, these are **not**
  permissive OSS and must never be treated as such;
- the material is a premium/paid component or a preview of one;
- the licence is incompatible with redistribution under this project.

**Bundling requires a verified permissive licence _and_ trust tier ≥ 3.** Licence facts are
confidence-rated and must be **re-verified online** through
`python -m motif source retrieve --refresh` before bundling.

## Redistribution classes

Every source is assigned one of four redistribution classes:

| Class | Meaning | What Motif may do |
|-------|---------|-----------------|
| **redistributable** | Verified permissive OSS licence (e.g. MIT, Apache-2.0) or open browser standard. | The concept may be implemented and original implementations may be bundled, preserving attribution and notices. Bundling still requires trust tier ≥ 3 and a verified licence. |
| **adaptable-concept** | Licence/terms allow learning from the concept but not wholesale redistribution of the source's code/assets. | Learn the pattern and write a clean-room original implementation; never copy source code or assets. Record provenance. |
| **reference-only** | Unknown, restrictive, guidance-only, or premium/source-available terms. | Reference and cite only. Never bundle, never copy, never reconstruct. |
| **rejected** | Fails security or licensing review outright. | Excluded from the registry as a usable source; may exist only as a documented rejection. |

## Hard rules

These are non-negotiable:

1. **Never copy premium components** or any paid/closed material into the project.
2. **Never reconstruct paid components from previews**, screenshots, demos or minified
   bundles.
3. **Never remove attribution** required by a source's licence.
4. **Never copy unclear-licence code.** If the licence is not verified and permissive,
   the material is reference-only.
5. **Never treat source-available or Commons-Clause terms as permissive OSS.**
6. **The project licence never overrides third-party obligations.** MIT applies only to
   original Motif code.
7. **Record provenance for every recipe**, the inspiring source, the licence under which
   the concept may be adapted, and evidence links.
8. **Label original implementations `original`** so Motif-authored code is distinguishable
   from third-party material.
9. **Preserve third-party notices** (licence headers, NOTICE files, attribution) wherever
   they apply.

## Licence-review checklist

Use this when adding or re-verifying a source (it complements `docs/source-review.md`):

- [ ] Official homepage and repository identified and linked in `evidence`.
- [ ] Licence identified, with a `license_reference` URL to the canonical licence file.
- [ ] Licence matched to a record in `registry/licenses/` (or a new one added).
- [ ] Confirmed the licence is **not** source-available / Commons-Clause / premium.
- [ ] `redistribution` class assigned per the table above.
- [ ] `attribution_required` set correctly; required notices captured.
- [ ] `trust_tier` (1-5) assigned; bundling candidates are tier ≥ 3.
- [ ] `confidence` and `status` set; `pending-verification` if not re-verified online.
- [ ] For recipes: provenance recorded and the implementation is clean-room `original`.
- [ ] `python -m motif validate` / `make check` passes.

When in doubt, classify down (toward `reference-only`), not up.
