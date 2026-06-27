# Principles — Interface Intelligence OS

These are the core product principles. They are decision rules, not slogans: when two paths
conflict, the higher principle wins. They govern every engine and every release.

---

## 1. Honesty is paramount

Every capability is labelled **implemented**, **experimental**, or **planned**, and the
labels are kept true. IIOS never fabricates facts, version numbers, benchmarks, licences,
coverage figures, or source counts. Where a check is partial (e.g. automated accessibility
catches only part of the issues — see [problem-evidence](../research/problem-evidence.md)),
it says so and flags the rest for human review. An honest "partial" beats a fabricated
"complete".

## 2. Reason from product context, not from aesthetics

Start from *who the user is and what must be understood, felt, or accomplished* — then
choose the interface. The chain is `product purpose → user intent → screen → objective →
pattern → effect → implementation`, never "make it look impressive first."

## 3. Least complexity that works

Prefer the simplest technique that achieves the objective: browser-native before a library,
a pattern before an effect, no motion before gratuitous motion. Complexity must earn its
place.

## 4. Fidelity follows certainty

Move up the fidelity ladder (context → spec → structure → states → high-fidelity) only as
confidence increases. Refuse premature high-fidelity output. (See
[problem P2](../research/problem-evidence.md).)

## 5. Completeness over happy path

A UI is not done until every applicable state is addressed: empty, loading, partial, ideal,
error, offline/degraded, permission-denied, overflow. Missing states are defects, not
follow-ups.

## 6. Accessibility and reduced-motion are mandatory

Not optional, not a later pass. WCAG 2.2 conformance intent, keyboard/focus correctness,
contrast and target-size at design time, and `prefers-reduced-motion` fallbacks are
required. Motion that harms accessibility is refused.

## 7. Performance is a budget, not an afterthought

Interactions respect responsiveness budgets (INP-aware), animations stay off the critical
path, and effects that degrade performance are rejected. (See
[problem P5](../research/problem-evidence.md).)

## 8. Security and licensing are non-negotiable

Untrusted-by-default ingestion, static scanning, and a licence gate (`unknown →
reference-only`; source-available/Commons-Clause are *not* permissive). Third-party install
scripts never run against the user's repo. IIOS reduces risk but does not eliminate it —
human review remains required.

## 9. Originality by default

Resist generic-AI convergence. Propose distinctive, context-fit design rather than the
statistically modal template, and audit output for default-template signatures. (See
[problem P1](../research/problem-evidence.md).)

## 10. Framework neutrality, with Vue and Frappe-Vue first-class

Browser-native, Vue, Frappe-Vue, React, and Svelte are all real targets. IIOS owns the
source it emits (clean-room or adapted), rather than depending on opaque runtimes.

## 11. Deterministic tools decide; agents judge

Anything that must be repeatable, auditable, or safety-affecting — validation, scanning,
licence gating, ranking, scoring — runs in **deterministic, dependency-free tooling**.
Agents handle judgment and synthesis. The boundary is explicit and enforced.

## 12. Record every decision

Every selection is written to a decision ledger with rationale, provenance, and the
rejected alternatives, so a human can audit *why* — and so quality can be defended and
maintained over time.

## 13. Maintain coherence over long horizons

Quality must not silently degrade across a long agent session. Drift from recorded
decisions and accumulating inconsistency ("interface debt") are detected and corrected.

## 14. Reuse, do not rebuild

Import proven layers — axe-core for a11y rules, Playwright for execution, the shadcn
registry format for distribution, DTCG for tokens, curated design knowledge — rather than
recreating them. Build the *judgment and governance* layer that is missing.

## 15. Open, self-hostable, dependency-free core

MIT-licensed, runnable on a stock Python interpreter with no third-party dependencies in
the core, so `make check` runs anywhere and the system can be inspected and trusted.

---

### Precedence (when principles collide)

Safety and honesty (1, 6, 7, 8) outrank expressiveness (3, 9). Correctness and completeness
(2, 4, 5) outrank speed. Determinism (11) outranks convenience. If a principle cannot be
honoured, IIOS says so (1) rather than pretending otherwise.
