# Motif v3 browser verification

This document records the real browser proof of the evidence-grounded golden loop, the
prerequisite for tagging a stable public v3 (ADR-REL-002).

## What was proven

The `browser-golden-loop` GitHub Actions workflow ran on `ubuntu-latest` with Python 3.12,
Node 20, and Chromium 148 via Playwright, on branch `motif-v3-1-evidence`. With the gate
flag `--require-browser` (any `not-executed` browser stage fails the job), the golden
scenario passed end to end:

```
detect (static)                    passed
context-vector                     passed
evidence-query                     passed   (claim-status-colour-001, normative, tier 1)
repair-plan                        passed
start-app                          passed   (Vite dev server, HTTP readiness)
browser-before                     executed-and-passed   (axe: 1 violation = seeded issue observed)
apply-in-worktree                  passed   (isolated git worktree)
verify-finding-closed (static)     passed
start-repaired-app                 passed
browser-after                      executed-and-passed
verify-runtime-finding-closed      executed-and-passed   ("on track" label rendered in the browser)
regression-check                   passed   (no new blocking axe violations)
rollback (exact)                   passed
baseline-unchanged                 passed   (source branch + fixture byte-for-byte unchanged)

outcome: browser-verified
```

Artifacts (uploaded by CI, `motif-browser-golden-loop`): real before/after screenshots,
`accessibility.json`, `axe.json`, `console.json`, `network.json`, `geometry.json`,
`metadata.json` (with Playwright/Chromium/Python versions), and the HTML/JSON report.

## Truthful statement

> Motif can now complete and prove an evidence-grounded repair against the bundled Vue
> benchmark application in a real browser environment. Broader framework, route,
> authentication, and repair coverage remains experimental.

## What this does NOT claim

- It does not audit arbitrary applications.
- axe passing does not prove full accessibility or any certification; human and
  assistive-technology review is still required.
- It is not a fully autonomous redesign and is not production-safe without review.

## Reproduce

```bash
pip install -e ".[browser]"
python -m playwright install --with-deps chromium
(cd evals/fixtures/sample-vue-app && npm install)
motif doctor --browser
make check
motif bench --scenario vue-dashboard-evidence-repair --target evals/fixtures/sample-vue-app --require-browser
```

## Release gate status

The browser gate (ADR-REL-002, spec section 20) is satisfied on `motif-v3-1-evidence`.
Remaining owner actions before a public tag: merge the branches into `main` (PRs prepared),
let the workflows run green on `main`, then tag `v3.0.0-beta.1` (prerelease) and, after
review, `v3.0.0`. No tag is created automatically.
