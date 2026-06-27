# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Work toward the **v0.2.0** roadmap:

- Broaden the registry to roughly 40–50 reviewed sources.
- Expand component-level coverage across the five usability modes.
- Strengthen controlled-installer automation (planning, patching, validation, rollback).
- Add more tested clean-room recipes and worked decision examples.
- Re-verify licence facts online and reduce the number of `pending-verification` sources.

(Longer term, v1.0.0 targets 75–100 thoroughly reviewed sources, broad component
coverage, mature adapters and a proven contributor workflow.)

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
  quarantine (`.oii/quarantine|reviewed|approved|rejected/`) where retrieved code is never
  executed. Security policies in `security/*.yml`.
- **Five static scanners** in `scanners/`: `source_scanner`, `behaviour_scanner`,
  `dependency_scanner`, `license_scanner`, `secret_scanner`.
- **Licence & source governance.** The LICENCE GATE (unknown ⇒ reference-only),
  trust tiers 1–5, redistribution classes, `registry/licenses/`, `LICENSE_POLICY.md` and
  `THIRD_PARTY_SOURCES.md`. Original code is MIT-licensed.
- **Representative registry.** 22 reviewed sources (licence/redistribution classified, a
  few `pending-verification`), 10 component records spanning all five usability modes
  (including a rejected fixture), 14 effects, 16 patterns, 4 clean-room recipe
  implementations and 10 quality profiles.
- **CLI and transparent ranking.** A dependency-free `python -m oii` CLI (Python 3.11+,
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
- **CI and local gate.** `make check` (runs `oii validate`, `tools/selfcheck.py` and the
  secret scan) mirrored by `.github/workflows/ci.yml`.
- **Open-source readiness.** README, `CONTRIBUTING.md`, `SECURITY.md`,
  `CODE_OF_CONDUCT.md`, this changelog, issue/PR templates and a pre-release self-review.

### Notes

This is representative breadth, not full coverage. Licence facts are confidence-rated and
**must be re-verified online** before any material is bundled; some sources remain
`pending-verification`. Live network connectors are specified but not implemented in this
release.

[Unreleased]: https://github.com/Suraj787/open-interaction-intelligence/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Suraj787/open-interaction-intelligence/releases/tag/v0.1.0
