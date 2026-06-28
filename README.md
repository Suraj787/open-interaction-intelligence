# Motif

**Design judgment, interface engineering, assurance, and governance for AI coding agents.**

AI coding agents already know how to generate interface code. They do not reliably know
what should be built, why a design choice belongs, whether a pattern fits the user and
workflow, whether the output is generic, whether it is accessible, whether it is fast on
real devices, whether third-party code is safe and legally reusable, whether it fits the
existing design language, or whether the codebase stays coherent after many changes.
Motif is the intelligence and governance layer that answers those
questions.

[![CI](https://github.com/Suraj787/motif/actions/workflows/ci.yml/badge.svg)](https://github.com/Suraj787/motif/actions)
&nbsp;Licence: MIT. Status: v3.1.0 "Evidence-Grounded Runtime" (interaction core shipped as v1.0.0; intelligence platform as v2.0.0)

> Defining principle: first determine what the user needs to understand, feel, decide, or
> accomplish, then choose the least complex interface and interaction that achieves it.
> Visual novelty never outranks usability, accessibility, security, performance, or
> maintainability.

## Honesty first

This README distinguishes what is **implemented**, **experimental**, and **planned**. See
the full [capability matrix](docs/capability-matrix.md). Nothing marked planned is claimed
to work. Anything you can run is covered by `make check`.

## The six engines

```
Product intent
> Product Intelligence      (context manifest: facts vs inference vs assumption)
> Design Intelligence       (styles, colour, typography, layout, ux-principles, industry packs)
> Interaction Intelligence  (patterns before effects, motion + density grammars, state completeness)
> Implementation            (framework detection, controlled install, rollback, provenance)
> Assurance                 (security static scans, evidence model; runtime checks planned)
> Governance and Learning   (design genome, interaction graph, originality, decisions, debt, drift)
```

The Interaction Intelligence Engine and Secure Component Supply Chain are the validated
**Motif** interaction foundation (originally the v1.0 core) (90 web-verified sources, 64
components, 30 effects, 28 patterns, 14 recipes, 5 scanners, controlled installer). Vue and
Frappe-Vue are first-class.

## What you can run today (implemented)

```bash
ii inspect                              # detect the target project's framework + conventions
ii model-product                        # scaffold a Product Context Manifest
ii context validate                     # validate manifests (uncertainty stays explicit)
ii genome validate|explain|diff <name>  # Product Design Genome
ii graph validate|query <name>          # Interaction Specification Graph (surfaces real gaps)
ii originality audit <path>             # Aesthetic Convergence Score over real source
ii states matrix|validate|inspect       # State Completeness Engine
ii motion validate ; ii density validate
ii debt calculate <path>                # explainable Interface Debt Score
ii decision create|list                 # design decision ledger
ii source scan <path>                   # 5 security scanners (foundation)
ii component plan-install <id> --target <dir>   # controlled install plan
ii search "<query>" ; ii rank <pattern> # registry search + transparent ranking
ii validate ; ii doctor                 # validate all engine data; health check
make check                              # full local gate (mirrors CI)
```

`motif` is the primary command; `ii` and `oii` are aliases. All three expose the full platform.

### Motif Live (v3, runtime and governance)

```bash
motif init                        # first run: inspect, create .motif/, first audit
motif improve --target ./app --goal "Make project risk easier to scan"
motif findings audit|list         # unified findings with evidence + lifecycle
motif policy init|check           # policy as code (blocking thresholds)
motif memory add --type rejected-approach --content "..."   # auditable project memory
motif atlas build                 # static public catalogue from the registry
motif system extract              # extract the project's design system
motif guard branch --base main    # Guardian: scan a diff against policy
motif mcp serve                   # MCP server (read tools + guarded writes)
motif studio                      # local read-only Studio viewer
motif bench --target ./app        # InterfaceBench automated measures
```

The browser-runtime surfaces (Visual Twin rendering, Playwright assurance, live preview,
semantic visual diff, interactive apply) are marked experimental and never fake output.
See the [capability matrix](docs/capability-matrix.md) and
[v3 architecture](docs/architecture/motif-v3-live-architecture.md).

### Evidence-grounded runtime (v3.1)

```bash
motif evidence query --product-form dashboard --purpose monitor --ability colour-vision-deficiency --risk financial:3
motif evidence explain claim-status-colour-001     # source, tier, limitations, validation
motif evidence check-myth "three click rule"
motif repair golden --target evals/fixtures/sample-vue-app --route /projects   # detect -> evidence -> worktree fix -> verify -> exact rollback -> report
motif doctor --browser                              # browser runtime status (optional motif[browser] extra)
```

A version-controlled UX Evidence Graph (110 Tier 1-3 claims with sources, limitations, and
validation) grounds the audit-and-repair decisions. Browser capture/validation is an
optional extra and reports `not-executed` without a runtime, never faked.

## Installation

Requirements: Python 3.11+ and `git`. Node.js 18+ is optional. The core CLI has no Python
dependencies.

```bash
git clone https://github.com/Suraj787/motif.git motif
cd motif
python -m ii doctor          # run in place, zero install
# or install the entry points:
python -m pip install -e .   # gives `ii`, `oii`, `motif`
ii doctor
```

Use it as a Claude Code Agent Skill by pointing Claude Code at this repo. The root
[`SKILL.md`](SKILL.md) is the orchestrator (an 18-step workflow with hard rules); specialist
skills live in [`skills/`](skills/).

## Repository map

| Area | What's there |
|------|--------------|
| `SKILL.md`, `skills/`, `agents/` | Orchestrator, 11 specialist skills, 15 reviewer agents |
| `product-intelligence/` | Product Context Manifest + sub-models |
| `design-intelligence/` | Styles, colour, typography, layout, ux-principles, 10 industry packs |
| `interaction-intelligence/` | Motion + density grammars, state requirements, anti-patterns |
| `governance/` | Design genome, interaction graph, decision ledger, debt, drift |
| `registry/`, `scanners/`, `security/`, `connectors/`, `ingestion/` | Secure supply chain (foundation) |
| `adapters/`, `implementations/`, `compiler/` | Framework adaptation and the controlled installer |
| `assurance/` | Assurance evidence model (static scans implemented; runtime planned) |
| `specifications/` | Interface Specification Language (schema + examples) |
| `interfacebench/` | Production-survival benchmark (15 capabilities, 10-round scenario) |
| `ii/`, `motif/` | The platform CLI module (`ii`) and the Motif foundation engine |
| `schemas/` | 25 strict JSON Schemas every record must satisfy |
| `evals/`, `tests/` | Adversarial judgement + security evaluations; test suite |
| `docs/` | Research, competitive analysis, architecture, capability matrix, ADRs |

## What v2.0.0 contains

- All six engines have functioning, schema-validated foundations.
- Design intelligence: 12 styles, 12 layouts, 15 executable UX principles, colour and
  typography systems, 10 deep industry packs (workflow and risk, not themes).
- Governance: 2 design genomes, a 31-node / 40-edge interaction graph with six deliberately
  seeded gaps that the queries surface, a decision ledger, and an explainable debt analyzer.
- Honesty discipline: the Product Context Manifest separates verified facts from inference
  and assumptions; recommendations carry confidence levels; performance is never reported as
  measured without measurement.
- `make check`: foundation self-check (75) plus the `ii` self-check (20), engine-data and
  graph validation, and a secret scan.

Planned next (v0.3.0): live `ii compile plan/apply`, workflow simulation (Playwright),
visual-regression assurance, drift trend tracking, external provider imports, and the
automated InterfaceBench runner. See the [capability matrix](docs/capability-matrix.md) and
[`docs/product/roadmap.md`](docs/product/roadmap.md).

## Honest limitations

- Live network connectors are declarative; ingestion is offline and proven on fixtures.
- Accessibility and performance assurance are static estimates plus state completeness, not
  runtime measurement.
- The design-intelligence and governance catalogues are representative, not exhaustive.
- Third-party code can never be guaranteed completely safe; automated accessibility checks
  are incomplete; AI-generated contributions require human review.

## Licence

Original code is [MIT](LICENSE). Third-party sources keep their own licences and
obligations; public source metadata does not imply redistribution rights. See
[`LICENSE_POLICY.md`](LICENSE_POLICY.md) and [`THIRD_PARTY_SOURCES.md`](THIRD_PARTY_SOURCES.md).
