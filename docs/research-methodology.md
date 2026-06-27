# Research Methodology

Motif's value depends on the quality of its source research. This document describes how
the source landscape (target: **50–100 sources**) is researched, what is recorded, how
unverified records are handled, and the non-negotiable rule: **do not fabricate facts.**

## Goals

- Build a broad, accurate map of where UI interactions, motion and effects actually come
  from — animated component collections, accessible UI foundations, animation engines,
  browser-native capabilities, scroll/transition systems, canvas/particle/generative
  systems, 3D/shader ecosystems, SVG/icon motion, creative references, and enterprise
  design systems.
- Capture enough governance metadata (licence, redistribution, trust tier, evidence) to
  make safe selection decisions *offline*.
- Distinguish reusable code from inspiration-only references.

## Source categories

Research spans the categories enumerated in `source.schema.json` (`category` enum):

`animated-component-collection`, `accessible-ui-foundation`, `animation-engine`,
`browser-native`, `scrolling-transitions`, `canvas-particles-generative`, `3d-shader`,
`svg-icon-motion`, `creative-reference`, `enterprise-design-system`.

Visual galleries (Codrops, Awwwards resources, SiteInspire, Godly, Hover.states, etc.)
are treated as **inspiration, not automatically reusable code**.

## Record fields

Every source is one machine-readable record validated against
`schemas/source.schema.json`. Required and key fields:

| Field | Notes |
|-------|-------|
| `id`, `name` | Stable slug + canonical name |
| `category` | One of the category enum above |
| `homepage`, `repository` | Official URLs; repository may be `null` |
| `frameworks`, `technologies` | What it targets / how it is built |
| `dependency_model`, `delivery_model` | e.g. `copy-paste`, `npm-package`, `registry-cli`, `cdn`, `reference`, `mixed` |
| `access_class` | `free` / `open-source` / `source-available` / `freemium` / `paid` |
| `license`, `license_reference` | SPDX-style identifier + where it was read |
| `redistribution` | `redistributable` / `adaptable-concept` / `reference-only` / `rejected` |
| `attribution_required` | Boolean |
| `trust_tier` | Integer 1–5 (see architecture.md) |
| `maintenance` | `active` / `maintained` / `slow` / `stale` / `unknown` |
| `documentation_quality`, `accessibility_maturity` | Quality signals |
| `performance_characteristics` | Free text |
| `suitable_contexts`, `unsuitable_contexts` | Where it fits / does not |
| `strengths`, `weaknesses` | Honest assessment |
| `evidence` | References that back the claims (URLs, files, commit) |
| `last_reviewed` | ISO date of the review |
| `confidence` | `high` / `medium` / `low` |
| `status` | `verified` / `pending-verification` / `rejected` |

A source is **not complete merely because its homepage was reviewed.** Where technically
and legally possible, discover its component/effect catalogue and create per-component
records (`component.schema.json`) — see [component-authoring.md](component-authoring.md).

## Research procedure (per source)

1. **Identify the official source.** Confirm the canonical homepage and official
   repository. Prefer, in order: official tagged release → official package registry →
   official component registry → pinned official commit → webpage source (last resort).
2. **Read the licence at its official location.** Record the SPDX identifier and a
   `license_reference`. Public visibility is **not** redistribution permission.
3. **Classify access and delivery** (`access_class`, `delivery_model`,
   `dependency_model`).
4. **Assess maintenance, documentation, accessibility maturity, performance.**
5. **Assign a trust tier** (1–5) and a `redistribution` disposition.
6. **Record evidence** for every non-obvious claim. Each strength/weakness/licence claim
   should be traceable.
7. **Set `confidence` and `status`** honestly (see below).
8. **Validate** the record: `python -m motif validate`.

## `pending-verification` handling

When internet access is unavailable, or a fact cannot be confirmed at its official
source, the record still gets created — but:

- `status` is set to **`pending-verification`** (never `verified`).
- `confidence` reflects reality (`low`/`medium`).
- `evidence` notes what could *not* be confirmed and what would confirm it.
- The record is **excluded from approved-installation flows**; it may inform
  catalogue/reference use only.
- A later `source refresh` re-checks the official source, fills evidence, and promotes
  the record to `verified` (or `rejected`) — never silently.

This is why the build pipeline can exist before exhaustive online verification:
**create the full research pipeline and mark records as `pending-verification`** rather
than inventing confirmed facts.

## Do not fabricate

This is the governing rule of all Motif research:

- **Never present assumptions as verified research.** No invented version numbers,
  benchmark figures, licence identifiers, or accessibility ratings.
- If a number is not measured or read from an authoritative source, it is not recorded as
  fact — describe the uncertainty instead.
- Prefer a smaller set of **high-confidence, evidence-backed** records over fabricated
  breadth. Motif v0.1.0 deliberately ships representative depth (16 deeply reviewed
  sources plus the pipeline and schema for the rest) rather than 100 unverified rows.
- Every claim that affects a safety decision (licence, redistribution, behaviour) must be
  backed by `evidence` or downgraded in `confidence`/`status`.

## Completeness reporting

Use `python -m motif source completeness` to report how far each source has been taken
(homepage-only vs catalogued, verified vs pending). Completeness is a first-class signal:
an honest "partial" beats a fabricated "complete".
