# Workflow: Validate an Experience

The final acceptance gate before an interaction is considered done. Validates
accessibility, performance, responsiveness, design-system fidelity and provenance — and
records the result. Load `skills/implementation-validation`.

## Preconditions

- An interaction has been implemented (build / improve / implement-pattern / convert).

## Steps

1. **Accessibility** (`skills/motion-accessibility`):
   - Keyboard: every action reachable and operable; focus never removed; visible
     `:focus-visible`.
   - Semantics: correct roles/labels; status announced to assistive tech.
   - **Reduced motion:** `prefers-reduced-motion` path verified; status never conveyed by
     motion alone.
   - No essential action is hover-only; input is never blocked for decorative motion.
2. **Performance** (`skills/motion-performance`):
   - Only transform/opacity animated where possible; no expensive layout-property
     animation when transform/opacity suffices.
   - Performance budget respected; no jank; no continuous decorative motion behind dense
     UIs; no unnecessary main-thread work.
3. **Responsiveness:** correct across breakpoints and input modes (mouse, touch, coarse
   pointer); sensible degradation on small screens.
4. **Design system:** existing conventions preserved (or a deliberate, recorded
   adjustment).
5. **Dependencies:** confirm none added, or each added one has a licence + cost note. No
   foreign framework introduced.
6. **Provenance:** decision record (`schemas/decision.schema.json`) and, for installed
   components, the provenance manifest are present and accurate.
7. **Registry integrity:** `python -m motif validate` passes for any new/changed records.
8. **Report** (the SKILL "After implementation" report): pattern + effect implemented,
   accessibility result, performance result, responsiveness result, design-system status,
   dependencies (with licence/cost) or confirmation of none, and the decision + provenance
   entry.

## Done when

Every gate passes, the result is reported, and the decision/provenance is recorded. A
failure on any gate sends the work back to the relevant build/improve/implement workflow
(and triggers rollback for a failed install).
