# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Toward v0.3.0: live `ii compile plan/apply`, workflow simulation (Playwright),
visual-regression assurance, drift trend tracking, external provider imports, and the
automated InterfaceBench runner.

## [0.2.0] - 2026-06-28 — Interface Intelligence OS

Evolves the Motif secure interaction foundation (tagged below as 1.0.0) into Interface
Intelligence OS: the intelligence, compilation, assurance, and governance layer for AI
coding agents. History preserved; `ii` is the primary CLI with `oii` and `motif` aliases.

### Added

- **Six-engine architecture** built on the validated foundation. New top-level engines:
  Product Intelligence, Design Intelligence, Governance and Learning, plus the Assurance
  evidence model and the Implementation compiler scaffold.
- **Design Intelligence Engine**: 12 styles (with honest AI-cliche and overuse risk), 12
  layouts, 15 executable UX principles (trigger/recommendation/rejection/validation),
  colour and typography systems, and 10 deep industry packs (users, workflows, risks,
  regulations, anti-patterns).
- **Product Intelligence Engine**: the Product Context Manifest separating verified facts
  from inference, assumptions and unresolved questions, with `ii inspect`,
  `ii model-product`, `ii context validate|explain`.
- **Governance and Learning Engine**: Product Design Genome (`ii genome
  validate|explain|diff`), Interaction Specification Graph with queryable gap detection
  (`ii graph validate|query`), Aesthetic Convergence Detector (`ii originality audit`),
  decision ledger (`ii decision create|list`), and an explainable Interface Debt score
  (`ii debt calculate`).
- **Interaction Intelligence** additions: motion and density grammars and a State
  Completeness Engine (`ii motion|density validate`, `ii states matrix|validate|inspect`).
- **Interface Specification Language** (schema + JSON/YAML examples), **InterfaceBench**
  foundation (15 capabilities, 10-round longitudinal scenario, rubric, machine-readable
  cases), **provider architecture** declarations, and 18 new JSON Schemas (25 total).
- **`ii` CLI** that unifies the new engines and delegates foundation commands to Motif;
  15 adversarial judgement evals added; `make check` extended (foundation self-check 75 +
  `ii` self-check 20 + engine-data/graph validation + secret scan).
- Honesty artifacts: `docs/capability-matrix.md` (implemented/experimental/planned),
  migration ADR, gap analysis, research and competitive analysis, and `PROJECT_STATUS.md`.

### Notes

Live network connectors, runtime accessibility/performance/visual assurance, `ii compile
apply` beyond the installer, and the automated bench runner are marked planned, not
claimed as implemented. See the capability matrix.

## [1.0.0] - 2026-06-27

Broadens coverage to a thoroughly reviewed source set with web-verified licences, expands
the catalogues, and matures the controlled installer. The architecture, security model and
honesty discipline from 0.1.0 are unchanged.

### Added

- **Source set expanded 22 → 90.** Every new source's licence was verified against its
  actual `LICENSE` file, `package.json` `license` field, or official terms page (recorded
  under `evidence`). Split: 53 redistributable, 20 adaptable-concept, 17 reference-only.
- **Component catalogue expanded 10 → 64**, across all five usability modes (37 installable,
  17 adaptable, 9 reference-only, 1 rejected).
- **Taxonomies expanded**: effects 14 → 30, patterns 16 → 28; recipes 4 → 14 with real,
  dependency-free, reduced-motion-aware clean-room implementations across browser-native,
  Vue, Frappe-Vue, React and Svelte.
- **Matured controlled installer.** New `motif/project.py` detects the target's framework,
  TypeScript/Tailwind and installed dependencies; the install plan now includes a
  framework-compatibility gate, a dependency plan against the project's `package.json`, and
  a static security scan of the implementation before applying.
- **`THIRD_PARTY_SOURCES.md` regenerated from the registry** so it always matches the
  records, with a section documenting notable licence nuances.

### Changed

- `make check` now runs 60 self-checks (added project detection, dependency planning and
  the larger registry).
- Documentation, README and the research methodology updated with the verification pass and
  corrected licence facts (p5.js LGPL, ScrollReveal GPL-3.0, Shopify Polaris field-of-use,
  vue-bits/svelte-bits Commons Clause, Theatre.js dual-licensed, Salesforce SLDS split).

### Notes

Live network connectors remain declarative (specified, not yet implemented); the
source-refresh workflow is offline in this release. Licence facts are confidence-rated;
re-verify before bundling anything new.

## [0.1.0] - 2026-06-27

Initial release. Ships the **complete architecture and secure pipeline** with
**representative, high-confidence breadth** rather than fabricated volume.

### Added

- **Interaction-design intelligence model.** The 8-level reasoning model
  (development purpose → product type → user intent → page/screen type → interaction
  objective → pattern → effect → implementation), taxonomies, anti-patterns and 10 quality
  profiles in `intelligence/`. Distinguishes **websites** from **web applications** and
  searches PATTERNS before EFFECTS.
- **Orchestrator skill + specialists.** A root `SKILL.md` that loads knowledge
  selectively, 10 specialist skills in `skills/`, 8 reviewer agents and reusable runbooks
  in `workflows/`.
- **Secure ingestion pipeline.** Offline approved registry as the default runtime; explicit
  `source retrieve --refresh` against an allowlisted official host; untrusted-by-default
  quarantine (`.motif/quarantine|reviewed|approved|rejected/`) where retrieved code is never
  executed. Security policies in `security/*.yml`.
- **Five static scanners** in `scanners/`: `source_scanner`, `behaviour_scanner`,
  `dependency_scanner`, `license_scanner`, `secret_scanner`.
- **Licence & source governance.** The LICENCE GATE (unknown ⇒ reference-only),
  trust tiers 1-5, redistribution classes, `registry/licenses/`, `LICENSE_POLICY.md` and
  `THIRD_PARTY_SOURCES.md`. Original code is MIT-licensed.
- **Representative registry.** 22 reviewed sources (licence/redistribution classified, a
  few `pending-verification`), 10 component records spanning all five usability modes
  (including a rejected fixture), 14 effects, 16 patterns, 4 clean-room recipe
  implementations and 10 quality profiles.
- **CLI and transparent ranking.** A dependency-free `python -m motif` CLI (Python 3.11+,
  stdlib only) with registry search, transparent candidate ranking, controlled install
  (plan → snapshot → patch → validate → auto-rollback → provenance manifest), validation
  and a health `doctor`.
- **Framework adapters & clean-room implementations.** Adapter contract plus
  browser-native, Vue, Frappe-Vue and React implementations in `adapters/` and
  `implementations/`.
- **Evaluations.** 12 evaluation cases (judgement + security) and malicious fixtures in
  `evals/`.
- **Schemas.** 7 strict JSON Schemas in `schemas/` (source, component, effect, pattern,
  recipe, decision, evaluation) that every record must satisfy.
- **CI and local gate.** `make check` (runs `motif validate`, `tools/selfcheck.py` and the
  secret scan) mirrored by `.github/workflows/ci.yml`.
- **Open-source readiness.** README, `CONTRIBUTING.md`, `SECURITY.md`,
  `CODE_OF_CONDUCT.md`, this changelog, issue/PR templates and a pre-release self-review.

### Notes

This is representative breadth, not full coverage. Licence facts are confidence-rated and
**must be re-verified online** before any material is bundled; some sources remain
`pending-verification`. Live network connectors are specified but not implemented in this
release.

[Unreleased]: https://github.com/Suraj787/motif/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/Suraj787/motif/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/Suraj787/motif/releases/tag/v0.1.0
