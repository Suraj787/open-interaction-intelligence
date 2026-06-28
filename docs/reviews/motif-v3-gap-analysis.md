# Motif v3 gap analysis

Comparing the current repository (Motif v2.0.0) against the Motif 3.0 "Motif Live" spec.
Status per capability: **implemented** | **partial** | **experimental** | **planned** |
**obsolete** | **missing** | **risky** | **blocked**.

Guiding constraint: the runtime/browser surfaces (Visual Twin rendering, Playwright
assurance, live preview, semantic pixel diff, interactive Studio apply) require a browser
runtime (Playwright) that is not installed in this environment. They are built as far as
is deterministic and honest, and marked experimental/planned with real interfaces, never
claimed as working.

## Foundation carried from v2 (reuse, do not rebuild)
| Capability | Status |
|---|---|
| Six engines (product/design/interaction/implementation/assurance/governance) | implemented |
| Registry (90 sources, 64 components, 30 effects, 28 patterns, 14 recipes) | implemented |
| 5 scanners, secure supply chain, licence gate, provenance | implemented |
| `motif`/`ii`/`oii` CLI, transparent ranking, controlled installer + rollback | implemented |
| 25 schemas, design genome, interaction graph, originality, debt, decisions | implemented |
| `make check` gate, CI, evals | implemented |

## v3 "Motif Live" target capabilities
| Capability | v3 spec | Status in this release | Notes |
|---|---|---|---|
| `motif run` flagship loop | §5 | partial | orchestration + run records implemented; runtime steps that need a browser are experimental |
| `motif create` workflow | §1A | partial | spec->context->concepts->plan implemented; preview/compile-apply experimental |
| `motif improve` workflow | §1B | partial | inspect->model->discover->findings->concepts->plan implemented; start-app + capture experimental |
| `motif init` first-run | §26 | implemented | inspect, detect, create .motif/, context, suggest profile, first audit |
| Motif Runtime (inspect/detect/worktree/run records) | §6 | implemented | git worktree isolation + run state in `.motif/runs/`; safe process start = experimental |
| Visual Twin (manifest + static parts) | §7 | partial | manifest + routes + component fingerprints from source; screenshots/a11y-tree/traces = experimental (Playwright) |
| Browser assurance (Playwright/axe) | §8 | experimental | interface + static-check layers implemented; runtime layers require Playwright |
| Unified Finding model + lifecycle + CLI | §9 | implemented | schema, statuses, `motif findings ...`, suppressions with reason/expiry |
| Motif Studio (local app) | §10 | partial | local-first static viewer over `.motif/` + registry; interactive apply = experimental |
| Motif Atlas (static catalogue) | §11 | implemented | `motif atlas build` generates a static site from the registry (source/component/pattern pages + filters data) |
| Shared source of truth | §12 | implemented | CLI/Studio/Atlas/MCP all read the one registry via library functions |
| Source update workflow + records | §13 | partial | quarantine pipeline + scanners implemented; live network refresh = planned |
| Community contribution workflow | §14 | implemented (docs+templates) | lifecycle, issue/PR templates, requirements |
| Recommendation engine (contextual) | §15 | implemented | explainable recommendation output over registry + profile |
| Concept generation + preview | §16 | partial | structured concept records + compare/select; visual preview = experimental |
| Real compiler (plan/preview/apply/pr) | §17 | partial | `compile plan` implemented (extends installer); apply/pr partial; preview experimental |
| Semantic visual comparison | §18 | experimental | schema + CLI; pixel/structural/semantic need rendered screenshots |
| MCP server | §19 | implemented | stdlib JSON-RPC over stdio; read-only tools + guarded writes; audit log; dry-run |
| Autopilot with approval gates | §20 | partial | 7-gate state machine + records; auto-apply gated, browser steps experimental |
| Design-system extraction | §21 | implemented | static parse of tokens/Tailwind/CSS vars -> `.motif/design-system/` |
| Motif Guardian (local + PR + trends) | §22 | implemented | `motif guard staged/branch`, GitHub Action, trend commands |
| Policy as code | §23 | implemented | schema, `motif policy init/validate/check/explain`, affects findings/debt/originality gates |
| Project memory | §24 | implemented | scoped, auditable `motif memory ...`, rejected-approach memory |
| InterfaceBench runner | §25 | partial | `motif bench run` executes automated measures over fixtures; model/human rubric separated |
| v2 compatibility | §30 | implemented | all v2 commands + schemas preserved; migration doc |

## Obsolete / risky / blocked
- **Obsolete:** none. v3 extends v2; nothing is removed.
- **Risky:** live process start of an arbitrary target app (mitigated: dry-run default, worktree isolation, explicit apply step, never touch main branch).
- **Blocked:** full runtime assurance and Visual Twin rendering are blocked on a browser runtime (Playwright) not present here. Interfaces and static layers ship; runtime execution is experimental and documented as such.

## Conclusion
v3 ships the deterministic Motif Live platform (findings, policy, memory, Atlas static site,
MCP server, Guardian, design-system extraction, run/create/improve orchestration,
recommendation, compiler plan) fully and honestly, with browser-dependent execution
implemented to the static boundary and marked experimental. No capability is claimed beyond
what `make check` verifies.
