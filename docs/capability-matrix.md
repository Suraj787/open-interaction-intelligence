# Capability matrix

Honest status of every Interface Intelligence OS capability as of v0.2.0.
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
