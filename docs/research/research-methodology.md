# Research Methodology — Interface Intelligence OS

> This document governs how Interface Intelligence OS (IIOS) researches, records, and
> releases the knowledge that its six engines depend on. It **evolves** the foundation's
> [`docs/research-methodology.md`](../research-methodology.md) (Motif's source-research
> rules) and raises it to cover design, product, interaction, implementation, assurance,
> and governance knowledge — not only effect/component sources.
>
> Status of this document: **implemented** (governing policy, in force for v0.2.0).
> Honesty is the non-negotiable rule: nothing here authorizes fabricating facts, scale,
> or confidence.

---

## 1. Why methodology comes first

IIOS makes safety- and quality-affecting decisions on behalf of an AI coding agent:
"use this pattern", "this licence is redistributable", "this contrast ratio fails WCAG",
"this interaction needs a reduced-motion fallback". Every such decision is only as
trustworthy as the evidence behind it. The methodology exists to make the evidence
**auditable**: any claim IIOS acts on can be traced to a source, a date, and a confidence
level — or it is treated as an inference, not a fact.

The cost of getting this wrong is concrete: a fabricated licence identifier can cause a
licence violation; a fabricated contrast figure can ship an inaccessible UI; a fabricated
benchmark can mislead an architecture decision. So the methodology optimises for
**traceable correctness over impressive breadth**.

---

## 2. Source hierarchy

When two sources conflict, the higher tier wins. When a lower-tier source makes a claim
the higher tiers do not support, the claim is recorded as **inference**, not fact.

| Tier | Source class | Examples | Weight |
|----:|--------------|----------|--------|
| 1 | **Official standards bodies** | W3C / WAI (WCAG, WAI-ARIA), WHATWG, ECMA, IETF | Authoritative for *what the rule is* |
| 2 | **Official platform / vendor docs** | MDN Web Docs, web.dev (Chrome team), Apple HIG, Material, Fluent, Carbon, Polaris, Primer docs | Authoritative for *how a platform behaves / intends* |
| 3 | **Official source repositories & registries** | dequelabs/axe-core, radix-ui, adobe/react-spectrum, package registries, tagged releases | Authoritative for *code, licence, version* |
| 4 | **Peer-reviewed / formal research** | ACM/CHI, arXiv preprints (flagged as not-yet-peer-reviewed), empirical HCI studies | Authoritative for *measured effects*, with caveats |
| 5 | **Established industry organisations** | Nielsen Norman Group, WebAIM, Deque research, Smashing/A11Y project | Strong secondary; cross-check against tiers 1–3 |
| 6 | **Recognised practitioners** | Maintainers' talks, named-author engineering posts | Useful signal; verify before acting |
| 7 | **Articles / tutorials** | Vendor blogs, third-party explainers | Orientation only; never a sole basis for a safety decision |
| 8 | **Discussions** | GitHub issues, forum threads, Q&A | Lead-finding only |
| 9 | **Videos / talks without transcripts** | Conference recordings | Lowest; cite the underlying artefact instead |

Two standing rules:

- **Public visibility is not permission.** A source being readable on the web says
  nothing about its licence. Licence facts come from tier 1–3 only (the `LICENSE` file,
  the package `license` field, or the official terms page).
- **Galleries are inspiration, never code.** Awwwards, Codrops, SiteInspire, Godly,
  Hoverstates and similar are `reference-only` by default (see
  [`source-landscape.md`](./source-landscape.md)).

---

## 3. Evidence standard

Every recorded claim carries five attributes:

1. **Source** — the canonical URL or file path it came from (prefer the official one).
2. **Date** — the publication/update date of the source *and* the date IIOS reviewed it
   (`last_reviewed`). Both matter: a 2019 article about Core Web Vitals is stale.
3. **Confidence** — `high` / `medium` / `low`, reflecting how directly the source supports
   the claim, not how much we like the claim.
4. **Time-sensitivity** — `stable` (e.g. a ratified standard), `slow-moving` (e.g. a
   design-system guideline), or `volatile` (e.g. a metric threshold, a pre-1.0 API, a
   licence under negotiation). Volatile facts get a re-check cadence.
5. **Type** — **official-fact** vs **inference**. An official-fact is asserted verbatim by
   a tier 1–3 source. An inference is IIOS's own reasoning *over* facts; it is labelled as
   such and never laundered into a fact.

### official-fact vs inference (worked examples)

| Statement | Type | Why |
|-----------|------|-----|
| "WCAG 2.2 became a W3C Recommendation on 2023‑10‑05." | official-fact | Stated by W3C (tier 1). |
| "INP replaced FID as a Core Web Vital on 2024‑03‑12." | official-fact | Stated by web.dev / Chrome (tier 2). |
| "Automated tooling detects roughly half of WCAG issues." | official-fact (bounded) | Deque/axe-core state "up to ~57%"; record the figure *and* its bound. |
| "Therefore agents must not treat an axe pass as full compliance." | inference | IIOS's reasoning over the fact; labelled inference. |
| "This animated collection is unsafe to bundle." | inference-from-fact | The *fact* is "licence is Commons Clause / unknown"; the disposition is IIOS policy. |

---

## 4. The evidence-based release model

IIOS deliberately rejects the "thousands of sources" framing common to scraped catalogues.
Breadth without verification is a liability. The release model is:

- **Core set: 15–25 sources, deeply reviewed.** These are read at their official location,
  their licence confirmed, their claims attributed, and their records marked `verified`.
  They are the only sources allowed to back a safety-affecting decision. The
  [`research-ledger.md`](./research-ledger.md) is this set.
- **Candidate set: 50–100 sources, catalogued.** These map the landscape (see
  [`source-landscape.md`](./source-landscape.md); ~90 are already in `registry/sources`).
  They inform discovery and reference use, but anything not yet confirmed stays
  `pending-verification` and is **excluded from approved-installation flows**.
- **Depth over volume.** A source is not "done" because its homepage loaded. It is done
  when its licence, maintenance, accessibility posture and redistribution disposition are
  evidenced. An honest "partial" beats a fabricated "complete".
- **Do not fabricate scale.** IIOS never inflates counts, never invents version numbers,
  benchmark figures, or accessibility ratings, and never claims to have reviewed a source
  it only skimmed. Where the network is unavailable, records are created as
  `pending-verification` with reduced confidence and a note on what would confirm them.

### Promotion / demotion

A record moves `pending-verification → verified` only after an official-source check that
fills its evidence. A `verified` record whose volatile facts age past their re-check
cadence is **demoted**, not silently trusted. Nothing is promoted automatically.

### Confidence is reported, not hidden

`python -m motif source completeness` (carried into the `ii` CLI) reports how far each
source has been taken. Completeness and confidence are first-class outputs, surfaced in
the capability matrix so readers always know what is implemented, experimental, or planned.

---

## 5. Scope beyond sources

Because IIOS now reasons about design judgment and product understanding, the same
evidence standard applies to *non-source* knowledge:

- **Design-intelligence data** (styles, colour, typography, layout, UX principles) cites
  its provenance (e.g. NN/g heuristics, WCAG contrast, DTCG token format) the same way.
- **Assurance checks** record which rule they implement and its standard (e.g. axe-core
  rule → WCAG SC), and explicitly state their coverage limits.
- **Benchmarks (InterfaceBench)** publish their rubric and scoring method; scores are
  reproducible measurements, never marketing numbers.

---

## 6. Governing rules (summary)

1. Trace every safety-affecting claim to a tier 1–3 source, or downgrade it.
2. Separate official-fact from inference, always.
3. Prefer 15–25 verified sources to 1,000 unverified ones.
4. Mark volatile facts and re-check them; demote stale ones.
5. Never fabricate facts, counts, versions, licences, or confidence.
6. Report completeness and confidence honestly in the capability matrix.
