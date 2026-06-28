# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Toward v3.2: run the golden loop under a real browser CI (Playwright/axe), broader
repair classes, Visual Twin rendering, and semantic visual comparison.

## [3.1.0] - 2026-06-28 "Evidence-Grounded Runtime"

Adds a deterministic UX Evidence Graph and a real audit-and-repair golden loop. Same repo
and name. Per ADR-UXE-001 the browser-executed steps are an optional extra and report
not-executed where no runtime is present; v3.1.0 is held from tagging until a browser CI
run passes the golden loop.

### Added (implemented, covered by `make check`, 146 self-checks)

- **UX Evidence Graph** under `ux-evidence/`: a 9-dimension ontology, 7 schemas, and 110
  web-grounded executable claims (Tier 1-3, each with sources, limitations, validation, and
  freshness), 13 sources, 12 myths, 5 contradictions, 8 validation methods, and 3 packs
  (enterprise, public-service, ecommerce).
- **Deterministic query engine**: a screen/workflow context vector resolves to applicable
  claims with explicit merge rules (specificity wins, normative cannot be overridden by
  weaker, higher-risk guardrails win, hypotheses never block, stale cannot newly block,
  conflicts surfaced, sources + limitations exposed) and confidence that drops when critical
  context is an assumption.
- **Evidence CLI** (`motif evidence validate|index|query|explain|sources|check-myth|
  contradictions|stale|pack`) and **6 MCP tools + 5 resources** (read-only, audit-logged).
- **Golden repair loop** (`motif repair golden`, `motif bench --scenario
  vue-dashboard-evidence-repair`): detect colour-only status (static) -> build context vector
  -> query the applicable normative claim -> generate a repair plan -> apply a text-label fix
  in an isolated git worktree -> verify the finding is closed (static) -> exact rollback ->
  before/after HTML+JSON evidence report. The fixture on `main` is never modified.
- **Browser foundation** behind the optional `motif[browser]` extra: `ii/browser.py`,
  `ii/apprunner.py` (detect/start/HTTP-readiness/stop, no-secret env, policy-gated start),
  and `motif doctor --browser`. Guardian now attaches evidence claims to findings.

### Experimental / not-executed here (honestly marked, never faked)

Browser capture (screenshots, axe, accessibility tree, traces), the runtime before/after
validation, and the in-browser finding-closed check require Playwright + a browser, which
cannot be installed in this environment. They return `not-executed`. See
`docs/reviews/motif-v3-1-gap-analysis.md` and ADR-UXE-001.

### Compatibility

Additive. All v2/v3 commands, `ii`/`oii` aliases, schemas, and registries are preserved;
nothing removed. Migration guide: `docs/migration/v3-to-v3-1.md`.

## [3.0.0] - 2026-06-28 "Motif Live"

Activates the intelligence and governance platform into a runtime, execution, assurance,
and continuous-governance product. Same repo, same name. `motif` is the command (`ii`,
`oii` aliases). All v2 commands and schemas are preserved (see docs/migration/v2-to-v3.md).

### Added (implemented, covered by `make check`)

- **Motif Runtime**: project state under `.motif/`, run records, framework/route/component
  detection, isolated git worktrees. `motif init` first-run experience.
- **Create / Improve / run / autopilot** orchestration loops (deterministic steps run;
  browser steps are experimental and skipped, never faked).
- **Unified Findings** model + lifecycle + CLI (`motif findings audit|list|show|accept|fix|
  verify|suppress`), with suppressions requiring reason/scope/author/expiry.
- **Policy as code** (`motif policy ...`), **project memory** incl. rejected-approach
  (`motif memory ...`), **contextual recommendation** (`motif recommend`), **concept
  generation** (`motif concepts generate`).
- **Motif Atlas**: a static public catalogue generated from the one registry
  (`motif atlas build`, 183 pages). **Design-system extraction** (`motif system extract`).
- **Motif Studio**: a local read-only viewer over `.motif/` + registry (`motif studio`).
- **Motif Guardian**: diff scanning + policy gate (`motif guard staged|branch`) and a
  GitHub Action that comments on PRs.
- **MCP server** (`motif mcp serve`): dependency-free JSON-RPC over stdio, 11 read tools +
  guarded write tools + audit log; write actions require `--allow-write`.
- **Compiler plan** (`motif compile plan`), **InterfaceBench runner** (`motif bench`,
  automated measures kept separate from model/human evaluation), a **Vue fixture app** for
  static runtime inspection, and 7 new schemas (32 total).

### Experimental / planned (honestly marked, NOT claimed)

Visual Twin rendering, Playwright/axe runtime assurance, live preview, interactive Studio
apply, semantic pixel/visual comparison, the full screen compiler apply/pr, and trend
tracking all require a browser runtime not present in this environment. See
`docs/capability-matrix.md` and `docs/reviews/motif-v3-gap-analysis.md`.

### Compatibility

All v2 CLI commands, `ii`/`oii` aliases, schemas, and registries are preserved; no schema
removed. `.motif/` runtime state is gitignored. Migration guide: `docs/migration/v2-to-v3.md`.

## [2.0.0] - 2026-06-28

Evolves the Motif secure interaction foundation (tagged below as 1.0.0) into a full platform: the intelligence, compilation, assurance, and governance layer for AI
coding agents. History preserved; `motif` is the primary command, with `ii` and `oii` aliases.

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

[Unreleased]: https://github.com/Suraj787/motif/compare/v3.1.0...HEAD
[3.1.0]: https://github.com/Suraj787/motif/compare/v3.0.0...v3.1.0
[3.0.0]: https://github.com/Suraj787/motif/compare/v2.0.0...v3.0.0
[2.0.0]: https://github.com/Suraj787/motif/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/Suraj787/motif/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/Suraj787/motif/releases/tag/v0.1.0
