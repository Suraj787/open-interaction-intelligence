# Source Review Checklist

Use this checklist when adding or refreshing a source in `registry/sources/`. A source is
the top-level provenance anchor for the components, effects and recipes derived from it.
Do not mark a source `verified` until every applicable box is checked with evidence.

Schema: `schemas/source.schema.json`. Validate with `python -m motif validate`.

## 1. Official verification

- [ ] Canonical **homepage** confirmed (`homepage`).
- [ ] Official **repository** confirmed, or explicitly `null` if none exists.
- [ ] Preferred retrieval path identified, in priority order:
      official tagged release → official package registry → official component registry →
      pinned official commit → webpage source (last resort).
- [ ] No URL shorteners, IP-address hosts, redirects to unknown domains, localhost or
      private ranges. All hosts fit the domain allowlist (`security/*.yml`).

## 2. Licence

- [ ] Licence read **at its official location**, not inferred from popularity or "it's
      public so it must be free."
- [ ] `license` set to an SPDX-style identifier (or `UNKNOWN`).
- [ ] `license_reference` points at where the licence text was read.
- [ ] `access_class` set: `free` / `open-source` / `source-available` / `freemium` /
      `paid`.
- [ ] Source-available / Commons-Clause / paid terms are **not** treated as ordinary
      permissive open source.
- [ ] If licence is unknown ⇒ `redistribution` is `reference-only` (the licence gate).

## 3. Redistribution and attribution

- [ ] `redistribution` set: `redistributable` / `adaptable-concept` / `reference-only` /
      `rejected`.
- [ ] `attribution_required` set correctly; attribution text noted where needed.
- [ ] Premium/paid components are flagged as never-copy, never-reconstruct-from-preview.
- [ ] For restricted but conceptually useful sources: marked `adaptable-concept` and
      routed to clean-room adaptation (retain no source).

## 4. Trust tier

- [ ] `trust_tier` assigned 1–5:
  - 1 — official browser/framework documentation
  - 2 — established open-source project
  - 3 — maintained component library, clear ownership
  - 4 — community contribution
  - 5 — unknown or unverifiable ⇒ **reference-only or rejected**
- [ ] Lower trust → stronger review recorded.

## 5. Quality and fit

- [ ] `category` chosen from the schema enum.
- [ ] `frameworks` / `technologies` / `dependency_model` / `delivery_model` recorded.
- [ ] `maintenance`, `documentation_quality`, `accessibility_maturity`,
      `performance_characteristics` assessed.
- [ ] `suitable_contexts` and `unsuitable_contexts` listed (website vs web-application
      distinction made explicit).
- [ ] `strengths` and `weaknesses` are honest, not marketing copy.

## 6. Evidence and confidence

- [ ] `evidence` references every non-obvious or safety-relevant claim (licence,
      redistribution, behaviour).
- [ ] `last_reviewed` set to today's ISO date.
- [ ] `confidence` (`high`/`medium`/`low`) reflects how well evidence backs the record.
- [ ] `status` set honestly:
  - `verified` — every applicable box above checked with evidence
  - `pending-verification` — created but not yet confirmed at the official source
    (e.g. offline); excluded from approved-installation flows
  - `rejected` — fails the licence gate, trust tier, or safety review
- [ ] **No fabricated facts.** Unmeasured numbers and unread licences are never recorded
      as verified.

## 7. Downstream completeness

- [ ] If the source's catalogue is reachable, per-component records were created
      (`component.schema.json`) — a homepage review alone does not complete a source.
- [ ] `python -m motif source completeness` reflects the real state.

## Sign-off

A reviewer records the decision and date. Re-run this checklist on every `source refresh`
that changes pinned version, licence, or behaviour.
