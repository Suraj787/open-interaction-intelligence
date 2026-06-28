# ADR-REL-002 — Browser-verified v3 release

- Status: Accepted
- Date: 2026-06-28

## Context

The deterministic v3 (runtime, governance) and v3.1 (UX Evidence Graph, evidence-grounded
repair) work is complete on `motif-v3-live` and `motif-v3-1-evidence` and passes 146
self-checks plus a clean-clone test. The golden audit-and-repair loop runs deterministically,
but the browser-executed validation (screenshots, axe, accessibility snapshot, runtime
finding closure) has never executed because no browser runtime is installable locally (`pip`
is broken here). The public repository has tags up to `v2.0.0` and no public v3.

## Alternatives considered

1. Tag `v3.0.0` and `v3.1.0` now from the deterministic work. Rejected: the spec and our own
   honesty rules forbid tagging a stable release while any browser stage is `not-executed`.
2. Ship `v3.1.0` directly. Rejected: no public `v3.0.0` exists; we must not invent release history.
3. Combine v3 + v3.1 into a single browser-verified `v3.0.0` (beta first). **Chosen.**

## Decision

- **Chosen public version:** `v3.0.0`, combining the v3 foundation and the v3.1 Evidence
  Graph + browser-verified repair. The internal CHANGELOG retains [3.0.0] and [3.1.0] as
  development milestones; the public combined tag is `v3.0.0`.
- **Branch merge order:** PR1 `motif-v3-live -> main`; PR2 `motif-v3-1-evidence -> main`
  (after PR1, or stacked). No direct edits to `main`. No force-push, no branch deletion.
- **Tag policy:** No stable tag until the `browser-golden-loop` CI job runs and passes with
  no `not-executed` browser stage. A `v3.0.0-beta.1` prerelease may be created only after the
  first green browser CI AND explicit owner permission, marked clearly as not-stable.
- **Browser gate:** `motif bench --scenario vue-dashboard-evidence-repair --require-browser`
  must pass in CI; any `not-executed` browser stage fails the job and blocks tagging.
- **Rollback policy:** The golden loop modifies only an isolated worktree and verifies a
  byte-for-byte baseline afterward; releases can be reverted by tag deletion (owner action)
  without affecting `main` history.

## Consequences

- This session: push the two branches, add the browser workflow and the real Playwright
  capture, keep the deterministic gate green, and report the actual CI outcome. No tag is
  created. Browser-dependent capability-matrix rows stay experimental until CI is green.
- A human with the repo and a green browser CI run creates the beta/stable tags.
