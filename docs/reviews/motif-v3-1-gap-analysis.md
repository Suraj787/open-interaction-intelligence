# Motif v3.1 gap analysis

Comparing the current repo (v3.0.0 foundation on `motif-v3-live`) against the v3.1
"Evidence-Grounded Runtime" spec. Status: implemented | partial | experimental | missing |
unsafe | blocked | misleadingly-named | ready-for-runtime-integration.

## Hard environment constraint
`pip` is non-functional in this environment (a Homebrew libexpat/pyexpat ABI mismatch), so
Playwright and a browser **cannot be installed or run here**. The spec makes the browser an
optional extra (`motif[browser]`) and gates tagging on a separate browser CI job. Therefore
the browser-executed parts of the golden loop are built as real code but reported
`not-executed` here, and v3.1 is **not tagged** until a browser CI run passes.

## UX Evidence Graph (the deterministic deliverable)
| Capability | Status |
|---|---|
| Evidence schemas (source, claim, myth, contradiction, validation, pack, context-vector, query-result) | ready-for-runtime-integration -> implemented this release |
| Ontology (product-form/purpose/workflow/expertise/abilities/risks/devices/environments) | missing -> implemented |
| 100-150 executable claims, Tier 1-3, with sources/limitations/validation/freshness | missing -> implemented |
| Myth register + contradictions | missing -> implemented |
| Three grounded packs (enterprise, public-service, ecommerce) | missing -> implemented |
| Deterministic query engine (context vector -> applicable claims + merge rules + conflicts) | missing -> implemented |
| `motif evidence ...` CLI + JSON output | missing -> implemented |
| MCP evidence tools + resources | missing -> implemented |
| Context vector on the Product Context Manifest (with provenance + confidence reduction) | partial -> implemented |

## Browser runtime + golden repair
| Capability | Status |
|---|---|
| `ii/runtime.py` worktree isolation, run records, detection | implemented (v3) |
| App runner (detect/start/readiness/stop, process-tree kill, log evidence) | partial (logic implemented; cannot start the fixture without node_modules + a browser here) |
| `motif doctor --browser` | implemented (honestly reports browser unavailable here) |
| Browser capture (screenshot/axe/a11y snapshot/console/network/trace/geometry) | experimental -> code path implemented behind the optional extra; not-executed here |
| Colour-only-status detection | implemented (static) ; runtime-geometry detection experimental |
| Evidence-grounded repair plan | implemented |
| Controlled repair apply in isolated worktree + exact rollback | implemented (git, deterministic) |
| Browser before/after validation + finding-closed verification | experimental -> not-executed without a runtime |
| Before/after evidence report (HTML+JSON) | implemented (deterministic artifacts; browser artifacts marked not-executed) |
| Golden InterfaceBench scenario | partial (deterministic steps run end-to-end; browser steps not-executed) |

## Integration
| Capability | Status |
|---|---|
| Guardian uses evidence graph for changed files | implemented |
| Studio shows evidence + repair + before/after | partial (read-only evidence display; before/after images not-executed here) |
| Tests (evidence + repair deterministic) | implemented ; browser tests = separate CI job |

## Misleadingly-named / unsafe risks (mitigated)
- Nothing claims browser assurance ran. Every browser result carries a status from
  {passed, failed, warning, not-applicable, not-executed, human-review-required}; here it is
  `not-executed`.
- No legal/medical/accessibility-certification claims. Claims carry `compliance_claim_allowed:
  false` and disclaimers.
- Code changes happen only in an isolated worktree; the user's active branch is never edited.

## Conclusion
v3.1 ships the complete, validated UX Evidence Graph (data + query engine + CLI + MCP) and
the full deterministic repair/rollback/report path, with the browser-executed validation
implemented behind the optional extra and honestly marked not-executed in this environment.
Tagging v3.1.0 awaits a passing browser CI job (ADR-UXE-001).
