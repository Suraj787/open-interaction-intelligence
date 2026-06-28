# ADR-UXE-001, v3.1 release and integration strategy

- Status: Accepted
- Date: 2026-06-28

## Context

Motif v3.0.0 ("Motif Live") foundation exists on the `motif-v3-live` branch and is not yet
merged or tagged on the remote. The v3.1 spec adds the UX Evidence Graph and a real
browser-driven audit-and-repair golden loop. The build environment cannot install or run a
browser runtime (`pip` is broken here), so the browser-executed steps cannot be observed.

## Decision

1. **Build v3.1 on a branch off `motif-v3-live`** (`motif-v3-1-evidence`), preserving history.
   v3.0.0 and v3.1.0 ship together at publish time; the user tags `v3.1.0` on merge. We do not
   tag a `v3.0.0` release separately first, to avoid a release that immediately supershadows.

2. **The UX Evidence Graph integrates as a version-controlled evidence layer**, not a new
   engine or database. It lives under `ux-evidence/` (flat YAML/JSON + generated indexes) and
   is consumed by Improve, Guardian, Studio, MCP, and InterfaceBench through one deterministic
   query engine (`ii/evidence.py`).

3. **Browser execution is an optional extra** (`motif[browser]`, Playwright + axe). The base
   CLI never requires it. A clean abstraction (`ii/browser.py`) uses Playwright when importable
   and otherwise returns a structured `not-executed` result. `make check` stays dependency-free;
   browser tests are a separate CI job.

4. **Honesty gate on tagging.** Per the spec, v3.1.0 is not tagged until a browser CI job runs
   the golden loop successfully. In this environment that job cannot run, so the deterministic
   work is completed and validated, and the release is held with the browser steps reported
   `not-executed`. No browser result is ever fabricated.

## Consequences

- The deterministic Evidence Graph and the repair/rollback/report path are fully implemented
  and tested by `make check`.
- The capability matrix marks browser capture, runtime validation, and the full golden loop as
  experimental (not-executed without a runtime).
- Publishing/tagging is deferred to a human with a browser CI run available.
