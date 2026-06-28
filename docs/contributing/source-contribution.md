# Source contribution lifecycle

This document describes how a community-proposed **source**, **recipe**, or **adapter**
travels from an idea to approved, governed registry material in Motif v3. It complements
[`CONTRIBUTING.md`](../../CONTRIBUTING.md), [`LICENSE_POLICY.md`](../../LICENSE_POLICY.md)
and [`docs/source-review.md`](../source-review.md).

> **Popularity must not determine trust.** A library with a million downloads and an
> unknown or source-available licence is `reference-only`. A small, well-maintained
> project with a clear permissive licence and strong accessibility can earn a higher trust
> tier. Trust is justified by provenance, licence clarity, maintenance, accessibility and
> security posture, never by stars, downloads or hype.

## The lifecycle

```
submitted ─▶ automated validation ─▶ provenance verification ─▶ maintainer review ─▶ experimental ─▶ approved
                  │                          │                        │
                  └── fails ──▶ changes requested / rejected ◀────────┘
```

### 1. Submitted

A contributor opens the appropriate issue first, so links, licence and evidence can be
reviewed before any code lands:

- **Suggest a source**, [`new_source`](../../.github/ISSUE_TEMPLATE/new_source.md)
- **Submit a clean-room recipe**, [`recipe_submission`](../../.github/ISSUE_TEMPLATE/recipe_submission.md)
- **Report a licence change**, [`licence_change`](../../.github/ISSUE_TEMPLATE/licence_change.md)

The submission must state official links, licence + `license_reference`, framework(s),
accessibility + reduced-motion behaviour, performance characteristics, and a maintainer
declaration. A PR may follow, adding records under `registry/` and `implementations/`.

### 2. Automated validation

Motif Guardian runs on the PR (`.github/workflows/guardian.yml`):

- `make check`, the principal gate: dependency-free Python self-checks (`motif validate`,
  `tools/selfcheck.py` and the `ii` equivalents) plus the secret scan.
- `motif guard branch`, scans the changed files for findings and checks policy-as-code in
  `motif-policy.yml` against [`schemas/policy.schema.json`](../../schemas/policy.schema.json).
- The Guardian report is posted as a single, updated PR comment. Warnings are
  informational; **blocking findings fail the check.**

Records must validate against their JSON Schema in [`schemas/`](../../schemas/) or CI fails.

### 3. Provenance verification

A maintainer independently re-verifies, against the **official** source (not the
submission text), that:

- the licence and `license_reference` are accurate and current;
- the redistribution class is correct (unknown / source-available / Commons-Clause /
  premium ⇒ `reference-only`, never bundled);
- `evidence` links resolve and support the claims;
- AI-assisted facts have been re-checked by a human.

### 4. Maintainer review

A human reviewer assesses interaction-design value (patterns before effects), website vs
web-application fit, Vue / Frappe-Vue relevance, accessibility maturity, reduced-motion
behaviour, performance budget, and the proposed trust tier. The decision and any precedent
are recorded in [`governance/decision-ledger/`](../../governance/decision-ledger/).

### 5. Experimental

Accepted material enters in an **experimental** state (`status: experimental`, or
`pending-verification` with `confidence: low` where licence re-verification is incomplete).
It is usable and observed, but not yet trusted for bundling. Only a verified permissive
licence **and** trust tier ≥ 3 may be considered for bundling.

### 6. Approved

After provenance is fully verified and the experimental period is clean, a maintainer
promotes the record to **approved** (`status: verified`), updates `last_reviewed`, and the
material moves into the approved registry. Approval can be revoked, a
[`licence_change`](../../.github/ISSUE_TEMPLATE/licence_change.md) report reopens the
lifecycle and may demote material to `reference-only` or remove it.

## Requirements for every contribution

A contribution cannot advance past automated validation without all of the following:

- **Provenance**, `source` id, the specific component/effect referenced, and `evidence`
  links to the official homepage/repository/licence.
- **Licence**, SPDX or exact name, `license_reference` URL, redistribution class,
  attribution requirements, and a `confidence` level. Unknown ⇒ `reference-only`.
- **Official links**, homepage and repository on allowlisted official hosts.
- **Framework**, target framework(s): browser-native, Vue, Frappe-Vue, React.
- **Accessibility + reduced-motion**, keyboard/focus/semantics notes and an explicit
  `prefers-reduced-motion` path. Mandatory, never optional.
- **Performance**, animated properties (transform/opacity), a performance budget, and
  behaviour under dense UIs / low-end devices.
- **Maintainer declaration**, good-faith attestation, original (clean-room) work where
  applicable, and acknowledgement that maintainers will re-verify before bundling.
- **No secrets**, the secret scan must be clean.
- **`make check` passes** and records validate against their schemas.
- **Decision / memory**, a `governance/decision-ledger/` (or memory) entry where the
  contribution sets or relies on a precedent.

## Clean-room and licence gates

Recipes and adapters are **original** implementations. Follow the clean-room adaptation
procedure in [`CONTRIBUTING.md`](../../CONTRIBUTING.md): study the concept, not the code;
never copy markup, assets or proprietary tokens; preserve attribution; label Motif-authored
work `original`. The LICENCE GATE in [`LICENSE_POLICY.md`](../../LICENSE_POLICY.md) is
authoritative: source-available, Commons-Clause and premium terms are not permissive OSS.
