# Motif v3.0.0-beta.1 validation plan

Purpose: evaluate the beta against a real, non-fixture Vue project (BOSS v2 SPA) in
**audit-only** mode, and record what is trustworthy versus what needs work before a stable
v3.0.0.

## Safety rules for this validation
- **Read-only.** Run only auditors that do not modify the target. Do not write Motif runtime
  state (`.motif/`) into the BOSS tree.
- **No modification outside an isolated worktree.** No repair is applied. The colour-only
  repair class is the only supported repair and is not exercised here.
- **No unsupported repairs.** BOSS findings are reported, not fixed.
- **Honest browser status.** The local environment has no browser runtime; browser-executed
  steps are recorded as `not-executed`. The browser proof exists only in CI on the bundled
  fixture.

## Target
`apps/boss_v2/spa` (Vue 3 + Vite + frappe-ui), a git repository with `node_modules` present.

## What we run (read-only)
1. Project model: framework, routes, components, start/build commands.
2. Unified findings audit (static): accessibility (colour-only, focus), design-system
   (arbitrary values, hard-coded hex), reduced-motion, duplication, originality convergence.
3. UX Evidence query for a BOSS context vector (enterprise app, operator, daily operation).
4. Interface Debt score; Aesthetic Convergence score.
5. Design-system extraction (data only, not written into BOSS).
6. State completeness inspection on representative data-fetch components.
7. `doctor --browser` to record browser reliability.

## What we record
- **Findings:** counts by type and severity, with locations.
- **False positives:** a manual review of a sample of findings, classifying each as
  true / false / needs-context.
- **Context assumptions:** which context-vector dimensions are verified vs inferred vs
  assumed, and how that should lower confidence.
- **Browser reliability:** executed vs not-executed here; the CI proof scope.
- **Report quality:** is the output explainable, evidence-linked, and free of overclaiming?

## Pass/needs-work criteria for the beta
- Detectors run on a real project without crashing and produce explainable, located findings.
- No claim of full accessibility, certification, or autonomous repair.
- Clear separation of static vs browser-executed results.
- A reasonable false-positive rate, with the worst FP classes noted for tuning.

Results: `docs/releases/boss-beta-audit.md`.

---

## Corrections applied (2026-06-28)
The two defects this plan found are fixed on `fix/beta-evidence-query-originality`:
evidence-query over-filtering (corrected wildcard semantics) and originality false-saturation
(recalibrated aesthetic-convergence scoring). Results: `docs/releases/boss-beta-audit-after-corrections.md`,
the before/after table in `docs/releases/boss-beta-audit-comparison.md`, and the
cross-context proof in `docs/reviews/beta-correction-generalisation-report.md`.
