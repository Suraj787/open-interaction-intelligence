# Capability matrix

Honest status of every Motif capability as of v2.0.0.
Status: **implemented** (working, tested by `make check`) | **experimental** (works but
narrow or unverified) | **planned** (interface defined, not built).

Run `ii <command>` for anything marked implemented. Nothing marked planned is claimed to
work.

## Foundation (Interaction Intelligence Engine + Secure Supply Chain)
| Capability | Status | Entry point |
|---|---|---|
| Secure source ingestion, quarantine, no-exec | implemented | `ii source scan` |
| 5 static scanners (dangerous/behaviour/dependency/licence/secret) | implemented | `ii source scan` |
| Licence gate, trust tiers, provenance | implemented | registry + scanners |
| Registry: 90 sources, 64 components, 30 effects, 28 patterns, 14 recipes | implemented | `ii search`, `ii validate` |
| Transparent ranking | implemented | `ii rank <pattern>` |
| Controlled installer (detect, plan, scan, snapshot, rollback) | implemented | `ii component plan-install` / `install` |
| Framework adapters + clean-room implementations | implemented | `adapters/`, `implementations/` |

## Design Intelligence Engine
| Capability | Status | Entry point |
|---|---|---|
| Style intelligence (cliche/overuse risk) | implemented | `design-intelligence/styles/`, `ii validate` |
| Layout intelligence (compare layouts) | implemented | `design-intelligence/layout/` |
| Executable UX principles (trigger/action/validation) | implemented | `design-intelligence/ux-principles/` |
| Colour + typography systems | implemented | `design-intelligence/colour|typography/` |
| Industry packs (workflow + risk, 10 domains) | implemented | `design-intelligence/industry-packs/` |
| Product classification model | implemented | `product-intelligence/` |
| Content design / generic-copy detection | partial | covered by originality audit |
| Data-visualisation guidance | planned | `design-intelligence/data-visualisation/` |

## Product Intelligence Engine
| Capability | Status | Entry point |
|---|---|---|
| Product Context Manifest (facts vs inference vs assumption) | implemented | `ii context validate` / `explain` |
| Project inspection / framework detection | implemented | `ii inspect` |
| Manifest scaffolding | implemented | `ii model-product` |

## Governance and Learning Engine
| Capability | Status | Entry point |
|---|---|---|
| Product Design Genome (validate/explain/diff) | implemented | `ii genome validate|explain|diff` |
| Interaction Specification Graph (build/validate/query) | implemented | `ii graph validate|query` |
| Aesthetic Convergence Detector | implemented | `ii originality audit <path>` |
| State Completeness Engine (matrix/validate/inspect) | implemented | `ii states matrix|validate|inspect` |
| Motion + density grammars | implemented | `ii motion validate`, `ii density validate` |
| Interface Debt score (explainable) | implemented | `ii debt calculate <path>` |
| Decision ledger | implemented | `ii decision create|list` |
| Drift detection | experimental | `ii drift` (signals defined; trend tracking planned) |
| Learning / project-specific adaptation | planned | `governance/learning/` |

## Implementation Intelligence Engine (Compiler)
| Capability | Status | Entry point |
|---|---|---|
| Framework/convention/dependency detection | implemented | `ii inspect`, installer |
| Controlled installation + rollback + provenance | implemented | `ii component install` |
| `ii compile plan` (full spec-to-plan) | planned | reads ISL + genome + grammars |
| `ii compile apply` beyond the installer | planned | v0.3.0 |

## Assurance Engine
| Capability | Status | Entry point |
|---|---|---|
| Security assurance (static) | implemented | scanners |
| Assurance evidence model (schema) | implemented | `schemas/assurance-evidence.schema.json` |
| Accessibility static checks | partial | state completeness + reduced-motion debt signal |
| Performance estimation (never reported as measured) | partial | debt + dependency/bundle notes |
| Workflow simulation (Playwright) | planned | `ii simulate` |
| Visual-regression | planned | needs screenshot runtime |

## Interface Specification Language
| Capability | Status | Entry point |
|---|---|---|
| Schema + JSON examples + validation | implemented | `specifications/`, `ii validate` |
| YAML authoring | implemented | `motif/yaml_min.py` |
| Migration rules | planned | versioned migrations |

## InterfaceBench
| Capability | Status | Entry point |
|---|---|---|
| 15-capability framework + 10-round longitudinal scenario + rubric | implemented (spec) | `interfacebench/` |
| Machine-readable bench cases | implemented | `interfacebench/cases/` (schema-valid) |
| Automated harness runner | planned | executes rounds end to end |

## Providers
| Capability | Status | Entry point |
|---|---|---|
| Provider architecture (declared trust/licence/freshness) | partial | `providers/`, `registry/providers/` |
| External dataset import (e.g. UI UX Pro Max-style) | planned | normalise + cross-check |

The README links here. Anything not listed as implemented is not claimed to work.

---

## Motif v3.0.0 "Motif Live" (added this release)

Status legend unchanged. Browser-runtime parts are experimental because no browser
runtime (Playwright) is installed; they degrade to "not executed" rather than faking
output. Command is `motif` (`ii`/`oii` aliases). All covered by `make check` v3 self-check.

| Capability | Status | Entry point |
|---|---|---|
| First-run experience | implemented | `motif init` |
| Flagship loop (create/improve/audit/govern/benchmark) | partial | `motif run --mode ...` |
| Create workflow | partial | `motif create --goal ...` |
| Improve workflow | partial | `motif improve --target ... --goal ...` |
| Autopilot with approval gates | partial | `motif autopilot --goal ...` (stops at plan/preview/delivery) |
| Motif Runtime (state, run records, detection, worktree) | implemented | `.motif/runs/`, `motif init` |
| Visual Twin (static manifest) | partial | `motif twin build|inspect` |
| Visual Twin rendering (screenshots, a11y tree, traces) | experimental | needs Playwright |
| Unified Findings model + lifecycle | implemented | `motif findings audit|list|show|accept|fix|verify|suppress` |
| Policy as code | implemented | `motif policy init|validate|check|explain` |
| Project memory (incl. rejected-approach) | implemented | `motif memory list|add|invalidate|explain` |
| Motif Atlas (static catalogue site) | implemented | `motif atlas build` (183 pages from the registry) |
| Design-system extraction | implemented | `motif system extract|violations` |
| Motif Studio (local read-only viewer) | implemented | `motif studio` / `--build-only` |
| Motif Studio (interactive apply) | experimental | needs runtime |
| Motif Guardian (diff scan + policy) | implemented | `motif guard staged|branch`, `.github/workflows/guardian.yml` |
| MCP server (read tools + guarded writes, audit log) | implemented | `motif mcp serve [--allow-write]` |
| Contextual recommendation | implemented | `motif recommend <pattern> --profile` |
| Concept generation | implemented | `motif concepts generate` |
| Concept visual preview | experimental | needs runtime |
| Compiler `plan` | implemented | `motif compile plan --component --target` |
| Compiler `preview`/`apply`/`pr` (screen compiler) | experimental/planned | apply via the installer; full compiler v3.1 |
| Semantic visual comparison | experimental | `motif compare` (needs rendered screenshots) |
| InterfaceBench runner (automated measures) | partial | `motif bench` |
| Playwright/axe runtime assurance | experimental/planned | needs a browser runtime |
| Trend tracking (debt/drift/a11y/perf) | planned | `motif drift` (experimental), debt trend planned |

Honest boundary: the deterministic Motif Live platform (runtime state, findings, policy,
memory, Atlas, Studio viewer, MCP, Guardian, design-system extraction, recommendation,
compile plan, run/create/improve/init orchestration) is implemented and tested. Every
capability requiring a live browser is marked experimental and never reports faked results.

---

## Motif v3.1.0 "Evidence-Grounded Runtime" (added this release)

Status legend unchanged. The browser runtime cannot be installed in this environment
(pip is broken), so browser-executed steps return `not-executed` and are never faked.
Per ADR-UXE-001, v3.1.0 is not tagged until a browser CI run passes the golden loop.

| Capability | Status | Entry point |
|---|---|---|
| UX Evidence Graph schemas (claim/source/myth/contradiction/validation/pack/context-vector) | implemented | `ux-evidence/schemas/` |
| Ontology (9 dimensions, controlled vocab) | implemented | `ux-evidence/ontology/` |
| 110 executable evidence claims (Tier 1-3, sourced, with validation + freshness) | implemented | `ux-evidence/claims/` |
| 13 sources, 12 myths, 5 contradictions, 8 validation methods, 3 packs | implemented | `ux-evidence/` |
| Deterministic query engine (context vector -> claims, merge rules, conflicts) | implemented | `motif evidence query` |
| Evidence CLI (validate/index/query/explain/sources/check-myth/contradictions/stale/pack) | implemented | `motif evidence ...` |
| Evidence MCP tools (6) + resources (5) | implemented | `motif mcp serve` |
| Context vector with provenance + confidence reduction on assumptions | implemented | query `_assumptions`, repair context |
| `motif doctor --browser` | implemented | reports browser unavailable here |
| App runner (detect/start/readiness/stop, no-secret env, policy-gated) | implemented (logic) | `motif app start|status|stop` (start gated; not-executed here) |
| Browser evidence capture (screenshot/axe/a11y snapshot) | experimental | `ii/browser.py` (optional `motif[browser]`; not-executed here) |
| Colour-only-status detection | implemented (static) | `motif repair golden` |
| Evidence-grounded repair plan | implemented | `motif repair golden` |
| Controlled repair apply in isolated worktree + exact rollback | implemented | `motif repair golden` |
| Browser before/after validation + finding-closed-in-browser | experimental | not-executed without a runtime (static verify implemented) |
| Before/after evidence report (HTML + JSON) | implemented | `.motif/evidence/<run>/report.html` |
| Golden InterfaceBench scenario | implemented (deterministic) | `motif bench --scenario vue-dashboard-evidence-repair` |
| Guardian uses evidence graph for findings | implemented | `motif guard branch --format markdown` |

Honest boundary: the entire UX Evidence Graph and the deterministic repair loop
(detect -> evidence -> plan -> worktree apply -> verify -> exact rollback -> report) are
implemented and tested by `make check` (146 self-checks). The browser-executed capture and
runtime validation are real code behind the optional `[browser]` extra and report
`not-executed` here; v3.1.0 is held from tagging until a browser CI run passes.

---

## Browser verification (proven in GitHub Actions CI, 2026-06-28)

The `browser-golden-loop` workflow ran the golden audit-and-repair loop in real Chromium
148 on `ubuntu-latest` with `--require-browser` (any `not-executed` browser stage fails the
job). It passed: `outcome: browser-verified`. Status updated from experimental to implemented
for the proven capabilities; broader coverage remains experimental/planned.

### Implemented (browser-proven on the bundled Vue fixture)
- application startup and HTTP readiness; clean process teardown
- before/after screenshot capture (real PNGs)
- accessibility representation (aria snapshot) and axe runtime checks
- runtime colour-only status detection; before-state axe violation observed
- evidence-grounded repair applied in an isolated git worktree
- runtime finding closure (the repaired status label rendered in the browser)
- regression check (no new blocking axe violations)
- exact rollback; source branch and fixture byte-for-byte unchanged
- before/after HTML + JSON evidence report; CI artifact upload
- golden browser benchmark (`motif bench --scenario vue-dashboard-evidence-repair --require-browser`)

### Experimental
- arbitrary application authentication; multi-route crawling
- semantic visual comparison; broad repair classes; interactive Studio apply
- non-Vue repair support

### Planned
- focus / reduced-motion / target-size repair classes
- authenticated workflows; cross-browser testing; wider framework support

Honest scope: the loop is proven against the bundled Vue benchmark app. It does not audit
arbitrary applications, does not prove full accessibility (axe passing is not certification),
and is not a fully autonomous redesign. Human and assistive-technology review remain required.
