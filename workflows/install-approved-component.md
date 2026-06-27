# Workflow: Install an Approved Component

Apply an **approved** registry component to a real project through controlled
installation: preview, snapshot, patch, validate, and auto-revert on failure. Third-party
installers are never run directly against the target.

## Preconditions

- The component is `approved` in the registry with a clear licence and clean scans
  (see [review-component.md](review-component.md)).
- Target project inspected (framework, design system, existing dependencies).

## Steps

1. **Confirm eligibility.** `python -m motif component inspect <id>`, verify
   `usability_mode` is `bundled` or `installable`, licence permits the intended use, and
   security findings are acceptable. Reject `reference-only`/`rejected` here.
2. **Consider alternatives / weight.** `python -m motif component alternatives <id>`; apply
   the no-automatic-new-dependency rule (prefer dependency-free → existing dep → original
   recipe → approved lightweight dep). 
3. **Plan the install.** `python -m motif component plan-install <id>` shows: files to
   create/modify, source + licence, security findings, scripts, and dependency impact.
   Review all of it.
4. **Snapshot + patch.** `python -m motif component install <id>` creates a **rollback
   snapshot**, then applies a **controlled patch** (no third-party installer is run
   against the project).
5. **Validate.** Run the project's build/tests plus the Motif gates (accessibility,
   performance, responsiveness, reduced-motion). If validation fails, the install
   **automatically reverts**; otherwise run `python -m motif component rollback <id>`
   manually if needed.
6. **Provenance manifest.** Confirm the manifest was written: component, implementation ID,
   source type, inspiration sources, source version/commit, licence, install date,
   created/modified files, dependencies, security review, accessibility + reduced-motion
   behaviour.
7. **Record the decision** (`schemas/decision.schema.json`) and update any THIRD_PARTY
   notices/attribution required by the licence.

## Done when

The component is applied, validation passed (or auto-reverted), a provenance manifest
exists, attribution obligations are met, and the change is reversible.
