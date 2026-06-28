# Motif browser-release gap analysis

Scope: turn the deterministic v3 + v3.1 foundation into a browser-proven release. No new
product concepts. The only goal is real browser execution of the golden audit-and-repair
loop in CI, then the correct public release.

## Already implemented (deterministic, `make check`, 146 self-checks)
- UX Evidence Graph: 110 claims, sources, myths, contradictions, validations, 3 packs; query engine; CLI; MCP.
- Findings, policy, memory, Atlas, Studio viewer, Guardian, design-system extraction, run/create/improve.
- Golden loop deterministic path: detect (static) -> context vector -> evidence claim -> repair plan ->
  isolated git worktree apply -> static finding-closed verify -> exact rollback -> before/after report.
- App runner logic (detect/start/HTTP-readiness/stop, no-secret env, policy-gated start).
- Browser abstraction with honest `not-executed` fallback; `motif doctor --browser`.

## Only statically verified (needs browser execution to become implemented)
- Application startup against the real fixture (needs `npm ci` + a runtime).
- Before/after screenshot, accessibility snapshot, axe results, console, network, geometry.
- Runtime finding closure (the repaired label visibly rendered + axe colour-only resolved).
- Regression check against runtime axe.

## What GitHub Actions must prove (the gate)
On `ubuntu-latest`, Python 3.12, Node 20, Chromium via Playwright:
`pip install -e ".[browser]"` -> `playwright install --with-deps chromium` -> `npm ci` in the
fixture -> `motif doctor --browser` ready -> `make check` -> `motif bench --scenario
vue-dashboard-evidence-repair --require-browser` runs the full loop with NO `not-executed`
browser stage, uploads artifacts (before/after screenshots, axe, a11y, console, network,
geometry, traces, logs, report.html/json), and rolls back to a byte-for-byte baseline.

## What blocks stable release
Any `not-executed` browser stage blocks tagging. In this local environment `pip` is broken
(libexpat/pyexpat ABI mismatch), so the browser job cannot run here; it must run in CI.
Therefore no stable tag is created locally. The browser proof is delegated to the
`browser-golden-loop` workflow.

## Intended release strategy (see ADR-REL-002)
No public v3 tag exists, so the browser-verified release is **v3.0.0**, combining the v3
runtime/governance foundation and the v3.1 UX Evidence Graph + browser-verified repair.
Sequence: push both branches -> green browser CI -> (owner-permitted) `v3.0.0-beta.1`
prerelease -> review -> `v3.0.0` stable. The internal CHANGELOG keeps the [3.0.0] and
[3.1.0] development milestones; the public combined tag is v3.0.0.
