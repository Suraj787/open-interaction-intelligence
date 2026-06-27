# Authoring an Effect Record

An **effect** record describes a reusable *motion/visual technique* in the abstract —
what objective it serves, its cost, its accessibility risk, and its mandatory
reduced-motion fallback. Effects are framework-leaning building blocks that patterns
recommend or reject. Remember the core rule: **search for a PATTERN before an EFFECT.**

- **Schema:** `schemas/effect.schema.json`
- **Location:** `registry/effects/`
- **Validate:** `python -m motif validate`

## Required fields

`id`, `name`, `category`, `objective`, `complexity`, `performance_cost`,
`reduced_motion_fallback`.

## Field guidance

| Field | Guidance |
|-------|----------|
| `id` | slug, `^[a-z0-9-]+$` |
| `category` | effect family (e.g. reveal, transition, parallax, particle) — align with `intelligence/effect-taxonomy/` |
| `objective` | the user-facing reason it exists: what it helps the user **understand, feel or accomplish**. Never "looks cool" |
| `contexts` | where it suits (e.g. marketing-hero, dashboard-empty-state) |
| `technologies`, `frameworks`, `dependencies` | how it can be built; keep dependencies minimal |
| `complexity`, `performance_cost`, `accessibility_risk` | `low` / `medium` / `high` |
| `mobile_suitability` | `good` / `conditional` / `poor` |
| `reduced_motion_fallback` | **required** — the non-motion experience when `prefers-reduced-motion` is set |
| `enterprise_suitability`, `marketing_suitability` | `recommended` / `conditional` / `discouraged` — encode the website-vs-web-application distinction |
| `provenance` | `original` / `adapted-concept` / `browser-native` |
| `testing`, `tags` | how it is validated; search aids |

## The reduced-motion fallback is mandatory

`reduced_motion_fallback` is a required field for a reason: Motif never ships an effect
without a reduced-motion path. Describe the actual fallback (e.g. "instant state change,
no translate/opacity tween"), not "respects user preference."

## Enterprise vs marketing suitability

Use `enterprise_suitability` and `marketing_suitability` to keep flashy motion out of
dense work UIs. Continuous decorative motion behind a data-heavy application screen should
be `discouraged` for enterprise even if `recommended` for a marketing hero.

## Required provenance

Set `provenance` honestly:

- `browser-native` — built on platform capabilities (CSS, WAAPI, View Transitions).
- `original` — Motif's own technique.
- `adapted-concept` — concept learned from a source via clean-room adaptation; **retains
  no source code** and records the inspiration in the related recipe's
  `source_references`.

An effect must never embed or imply copied restricted code. If a technique can only be
expressed by copying a licence-incompatible source, it is `reference-only` at the source
level and does not become a redistributable effect.

## Example skeleton

```json
{
  "id": "scroll-reveal-fade",
  "name": "Scroll Reveal (fade + rise)",
  "category": "reveal",
  "objective": "Draw attention to content as it enters the viewport without hiding it from non-JS users",
  "contexts": ["marketing-section", "documentation-landing"],
  "technologies": ["intersection-observer", "css-transition"],
  "frameworks": ["browser-native", "vue", "react"],
  "dependencies": [],
  "complexity": "low",
  "performance_cost": "low",
  "accessibility_risk": "low",
  "mobile_suitability": "good",
  "reduced_motion_fallback": "Content is shown immediately with no transform; only opacity may snap, no motion",
  "enterprise_suitability": "conditional",
  "marketing_suitability": "recommended",
  "provenance": "browser-native",
  "testing": ["reduced-motion snapshot", "keyboard reachability"],
  "tags": ["scroll", "reveal"]
}
```
