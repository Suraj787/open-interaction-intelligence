# Pull Request

## Summary

What does this change and why? Link any related issue (e.g. `Closes #123`).

## Type of change

- [ ] New / updated source record
- [ ] New / updated component, effect or pattern
- [ ] New / updated recipe (clean-room implementation)
- [ ] CLI / ranking / pipeline
- [ ] Scanners / security / policies
- [ ] Docs
- [ ] Other

## Checklist

- [ ] **`make check` passes** locally (runs `motif validate`, `tools/selfcheck.py`, secret scan).
- [ ] **Provenance recorded** for any source-derived material (source id, evidence links).
- [ ] **Licence verified** and the redistribution class is correct (unknown ⇒ reference-only;
      source-available / Commons-Clause are **not** permissive; bundling needs a verified
      permissive licence **and** trust tier ≥ 3).
- [ ] **Reduced-motion handled**, a `prefers-reduced-motion` path exists where motion is involved.
- [ ] **Accessibility considered**, keyboard, focus, semantics; nothing is hover-only or
      motion-only for essential status.
- [ ] **Performance considered**, animates transform/opacity within budget; no jank, no
      decorative continuous motion behind dense UIs.
- [ ] **No secrets** committed (the secret scan is clean).
- [ ] **Original implementations labelled `original`**; third-party notices preserved.
- [ ] **Conventional commit** message(s) used (`feat:`, `fix:`, `docs:`, …).
- [ ] **AI assistance disclosed** and human-reviewed, if applicable.

## Validation evidence

Paste relevant `make check` / `python -m motif validate` output, and any accessibility /
performance validation notes.

```
(paste here)
```

## Guardian / contribution checklist

Motif Guardian runs on every PR (`make check` + `motif guard branch`) and posts a report
comment. Confirm the governance basics before requesting review:

- [ ] **Provenance recorded**, source id and evidence links for any source-derived material.
- [ ] **Licence verified** against the official source; redistribution class is correct
      (unknown ⇒ reference-only; source-available / Commons-Clause are not permissive).
- [ ] **Reduced-motion handled**, a `prefers-reduced-motion` path exists wherever motion is used.
- [ ] **Accessibility notes**, keyboard, focus, semantics; nothing essential is hover- or
      motion-only.
- [ ] **Performance notes**, transform/opacity within budget; no jank, no decorative
      continuous motion behind dense UIs.
- [ ] **No secrets** committed (Guardian's secret scan is clean).
- [ ] **`make check` passes** locally and in CI.
- [ ] **Decision / memory updated if applicable**, a `governance/decision-ledger/` entry
      (or memory record) reflects any precedent this PR sets or relies on.

## Notes for reviewers

Anything that needs special attention (licence nuance, trade-offs, follow-ups).
