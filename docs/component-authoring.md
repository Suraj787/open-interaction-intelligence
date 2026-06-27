# Authoring a Component Record

A **component** record describes a concrete, catalogued UI component or distinct effect as
it exists in a third-party source, its framework, technologies, licence, accessibility
and the **usability mode** that governs how Motif may use it. Components are evidence about
the outside world; they are not Motif's own implementations (those are *recipes*).

- **Schema:** `schemas/component.schema.json`
- **Location:** `registry/components/`
- **Validate:** `python -m motif validate`

## When to create one

When cataloguing a source's publicly accessible catalogue. A source is **not complete**
because its homepage was reviewed, create one machine-readable record per component or
distinct effect, where technically and legally possible.

## Required fields

`id`, `name`, `source`, `framework`, `license`, `usability_mode`,
`accessibility_status`, `verification_date`.

## Field guidance

| Field | Guidance |
|-------|----------|
| `id` | slug, `^[a-z0-9-]+$`, unique |
| `source` | the `id` of the parent record in `registry/sources/` |
| `canonical_page`, `repository_path` | where the component officially lives (or `null`) |
| `preview_available`, `copy_paste_available` | booleans from the source |
| `framework`, `styling_technology`, `animation_technology` | how it is built |
| `dependencies`, `required_assets`, `browser_requirements` | runtime needs |
| `installation_method` | how the source ships it |
| `license`, `component_exceptions`, `attribution` | licence as it applies to *this* component; some collections licence components individually |
| `redistribution_permission` | boolean; **false unless the licence clearly permits it** |
| `commercial_use`, `modification` | `yes` / `no` / `unclear` |
| `accessibility_status` | `good` / `partial` / `poor` / `unknown` |
| `reduced_motion_support` | `yes` / `no` / `unknown` |
| `responsive_behaviour` | `good` / `partial` / `poor` / `unknown` |
| `performance_cost`, `complexity` | `low` / `medium` / `high` |
| `quality_status` | `high` / `medium` / `low` |
| `usability_mode` | see below |
| `verification_date` | ISO date the component was reviewed |
| `evidence` | references backing the above |

## Usability mode

`usability_mode` is the disposition gate. Choose exactly one:

- `bundled`, may be shipped as-is (licence clearly permits redistribution; scans clean).
- `installable`, fetched/applied via its official installation method under controlled
  installation.
- `adaptable`, concept may be re-implemented clean-room; source not redistributed.
- `reference-only`, inspiration only; **default when licence is unknown or restricted.**
- `rejected`, fails safety, licence or quality review.

**Licence gate:** unknown licence ⇒ `reference-only`, never `bundled`.

## Required provenance

Every component traces to a verified `source`. Licence/redistribution claims must be
backed by `evidence`. Never set `redistribution_permission: true` or
`usability_mode: bundled` without a clear licence basis. Never reconstruct a paid
component from a preview. If unsure, downgrade, `reference-only` is the safe default.

## Example skeleton

```json
{
  "id": "example-spotlight-card",
  "name": "Spotlight Card",
  "source": "example-source",
  "framework": "react",
  "styling_technology": "tailwind",
  "animation_technology": "css",
  "license": "MIT",
  "redistribution_permission": true,
  "commercial_use": "yes",
  "modification": "yes",
  "accessibility_status": "partial",
  "reduced_motion_support": "no",
  "responsive_behaviour": "good",
  "performance_cost": "low",
  "complexity": "low",
  "quality_status": "high",
  "usability_mode": "adaptable",
  "verification_date": "2026-06-27",
  "evidence": ["repo LICENSE", "component page"]
}
```
