# Motif v3 "Motif Live", Pre-Release Review (12 perspectives)

A deliberately critical review of Motif v3 before release, from the 12 perspectives named in
the spec. For each perspective: **friction**, **missing evidence**, **misleading-claim risk**,
**unsafe behaviour**, and **how it's addressed**. Honesty about the experimental/planned
browser parts is mandatory; this review mirrors
[`docs/reviews/motif-v3-gap-analysis.md`](motif-v3-gap-analysis.md).

**Standing caveat (applies to every perspective).** No browser runtime (Playwright) is
installed in this environment. So Visual Twin rendering, Playwright/axe assurance, live
preview, pixel/semantic visual diff and interactive Studio apply are **experimental/planned**.
They ship as real interfaces with their static layers built, and every one degrades to "not
executed (no runtime)" rather than fabricating results. The deterministic platform
(findings, policy, memory, Atlas, MCP, Guardian, design-system extraction,
run/create/improve orchestration, recommendation, compile plan) is implemented and gated by
`make check`.

---

## 1. New user

- **Friction:** the command surface is large; knowing where to start (`motif init` →
  `motif improve`) isn't obvious.
- **Missing evidence:** a first run produces records under `.motif/` that a newcomer may not
  know to look at.
- **Misleading-claim risk:** seeing `run`/`twin`/`assure` listed could imply full live
  rendering works out of the box.
- **Unsafe behaviour:** none for read-first commands; the only risk is running an unknown
  app, which is opt-in.
- **Addressed:** `motif init` scaffolds and runs a first audit; `--dry-run` is the default for
  `run`; every guide opens with an honest status table; experimental steps are flagged inline.

## 2. Frontend developer

- **Friction:** wants to apply changes directly; v3 is plan-first and applies only in a
  worktree.
- **Missing evidence:** without a browser runtime there are no screenshots to diff a change
  against.
- **Misleading-claim risk:** `compile apply`/`pr` could be read as a turnkey codemod; apply is
  partial and preview is experimental.
- **Unsafe behaviour:** automated edits to a working branch, prevented.
- **Addressed:** apply runs in a git worktree with a rollback record and never touches `main`;
  `compile plan` is the implemented, reviewable artefact; apply/preview are labelled
  partial/experimental in [`docs/create`](../create/README.md) and the compiler section.

## 3. Product designer

- **Friction:** wants visual concepts; concepts are structured records, not rendered comps.
- **Missing evidence:** no pixel preview of a concept without a runtime.
- **Misleading-claim risk:** "concept generation + preview" could imply rendered mockups.
- **Unsafe behaviour:** none.
- **Addressed:** concepts are honest typed records (compare/select works); preview is marked
  experimental; rejected concepts are remembered via project memory so they aren't re-proposed.

## 4. Design-system lead

- **Friction:** needs to trust extracted tokens match the real system.
- **Missing evidence:** extraction is static parse only, runtime-computed styles aren't
  captured.
- **Misleading-claim risk:** "design-system extraction" sounding like a full runtime audit.
- **Unsafe behaviour:** none (read-only).
- **Addressed:** `motif design-system extract` is implemented and scoped to static
  tokens/Tailwind/CSS vars → `.motif/design-system/`; the static boundary is stated; runtime
  style capture is part of the experimental twin rendering.

## 5. Accessibility specialist

- **Friction:** wants real axe results; only static a11y checks run without a runtime.
- **Missing evidence:** runtime a11y violations (focus order, live regions) need Playwright.
- **Misleading-claim risk:** an a11y policy passing could be misread as full a11y conformance.
- **Unsafe behaviour:** falsely asserting accessibility, avoided.
- **Addressed:** static a11y checks ship; the axe layer is explicitly experimental and reports
  "not executed (no runtime)"; policy reports runtime inputs as unavailable rather than
  passing them ([`docs/assurance`](../assurance/README.md), [`docs/policies`](../policies/README.md)).

## 6. Performance engineer

- **Friction:** wants real load/interaction traces; only static checks run here.
- **Missing evidence:** no runtime performance trace without a browser.
- **Misleading-claim risk:** a "performance" policy implying measured metrics.
- **Unsafe behaviour:** none.
- **Addressed:** the perf trace layer is marked experimental; the `performance.yml` policy
  gates only on inputs that exist and flags missing runtime metrics as unavailable.

## 7. Security reviewer

- **Friction:** v3 can start an external app and run an MCP server, both need scrutiny.
- **Missing evidence:** wants proof writes are guarded and process start is contained.
- **Misleading-claim risk:** "runtime" implying unsandboxed execution.
- **Unsafe behaviour:** live process start of an arbitrary target app (the one genuinely risky
  action); silent MCP writes.
- **Addressed:** process start is `--dry-run` by default, worktree-isolated, behind an explicit
  `--allow-runtime` flag, and never touches `main`; MCP writes dry-run by default, are scoped,
  and are appended to an audit log; the supply chain (scanners, licence gate, quarantine)
  is unchanged from v2. See the gap analysis "Risky/Blocked" section.

## 8. Enterprise buyer

- **Friction:** needs to know what is production-ready vs aspirational before committing.
- **Missing evidence:** wants a single authoritative status source.
- **Misleading-claim risk:** treating experimental browser features as shipped.
- **Unsafe behaviour:** none.
- **Addressed:** the [gap analysis](motif-v3-gap-analysis.md) is the single status table that
  every doc mirrors; `make check` defines "implemented"; policy/Guardian/audit logs provide
  governance evidence; v2 compatibility is guaranteed.

## 9. OSS contributor

- **Friction:** wants to extend the catalogue and know the contribution lifecycle.
- **Missing evidence:** how a new source is reviewed end to end.
- **Misleading-claim risk:** assuming live network refresh of sources works.
- **Unsafe behaviour:** importing unvetted external code.
- **Addressed:** community workflow, issue/PR templates and requirements are implemented;
  the quarantine → scan → review → approve/reject lifecycle is enforced; live network refresh
  is explicitly **planned** (offline approved registry is the exercised runtime).

## 10. Claude Code user

- **Friction:** wants Motif usable from within Claude Code without setup friction.
- **Missing evidence:** how the agent reaches Motif's data safely.
- **Misleading-claim risk:** assuming the agent can auto-apply changes.
- **Unsafe behaviour:** an agent triggering live runs or writes unprompted.
- **Addressed:** the MCP server (implemented, stdlib JSON-RPC/stdio) exposes read tools openly
  and write tools guarded (dry-run + audit); apply/run remain explicit, gated actions, not
  agent defaults. See [`docs/mcp`](../mcp/README.md).

## 11. MCP client

- **Friction:** needs a predictable tool list and schema-stable responses.
- **Missing evidence:** which tools mutate state.
- **Misleading-claim risk:** treating guarded writes as having taken effect when they
  dry-ran.
- **Unsafe behaviour:** unaudited mutations.
- **Addressed:** `motif mcp tools` lists tools and marks writers; writes dry-run by default and
  return a clear "dry-run" result; every call is audited; reads are side-effect free and
  served from the one shared registry.

## 12. Existing v2 user

- **Friction:** worried an upgrade breaks current commands or schemas.
- **Missing evidence:** proof nothing was removed.
- **Misleading-claim risk:** assuming v2 behaviour changed.
- **Unsafe behaviour:** none.
- **Addressed:** all v2 commands, the `ii`/`oii` aliases, the 25 schemas and the registries are
  preserved; **no schema is removed**; v3 is additive. See
  [`docs/migration/v2-to-v3.md`](../migration/v2-to-v3.md).

---

## Readiness verdict

v3 ships the **deterministic Motif Live platform fully and honestly**, with every
browser-dependent surface built to its static boundary and clearly marked
experimental/planned. No capability is claimed beyond what `make check` verifies, and the
[gap analysis](motif-v3-gap-analysis.md) remains the single source of truth for status. The
principal residual risk, live start of an external app, is contained by dry-run defaults,
worktree isolation, an explicit flag, and never touching `main`.
