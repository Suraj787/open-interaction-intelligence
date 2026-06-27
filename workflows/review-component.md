# Workflow: Review a Component

Take a quarantined or candidate component through the security, licence, accessibility and
quality gates, and assign its **usability mode**. The component is treated as untrusted
until it passes.

## Preconditions

- Component material present in `.motif/quarantine/` (from a source-refresh) or a candidate
  to catalogue. Load `skills/source-governance`.

## Steps

1. **Confirm provenance.** Identify the parent source (`registry/sources/`) and the
   canonical component page / repository path. No execution at any point.
2. **Licence.** Read the licence as it applies to *this* component (some collections
   licence per component). Set `license`, `attribution`, `component_exceptions`,
   `commercial_use`, `modification`. Unknown ⇒ heading for `reference-only`.
3. **Static security scan.** Run the `source`, `behaviour` and `secret` scanners against
   the quarantined files. Review every flagged item: `eval`/dynamic execution, remote
   script loading, undocumented `fetch`/WebSocket, storage/cookie/clipboard, service
   workers, device access, unsafe HTML, obfuscation, embedded secrets.
4. **Dependency inspection.** Run the `dependency` scanner: direct/transitive/peer/optional
   deps, lifecycle scripts, maintainer identity, typosquatting, advisories, growth,
   licence compatibility.
5. **Behaviour policy.** Confirm an ordinary effect needs none of: cookies, persistent
   storage, clipboard, geolocation, camera, microphone, service worker, analytics,
   persistent WebSockets, remote scripts. Any such need requires explicit justification.
6. **Accessibility + responsiveness + performance.** Set `accessibility_status`,
   `reduced_motion_support`, `responsive_behaviour`, `performance_cost`, `complexity`,
   `quality_status`.
7. **Assign usability mode:** `bundled` (licence clearly permits redistribution + scans
   clean) · `installable` · `adaptable` (clean-room) · `reference-only` (default for
   unknown/restricted licence) · `rejected` (unsafe/incompatible).
8. **Record** the component (`schemas/component.schema.json`) with `verification_date` and
   `evidence`; move quarantined material to `.motif/reviewed/` then `approved/` or
   `rejected/`.
9. **Validate:** `python -m motif validate`.

## Done when

The component has a security/licence/accessibility verdict, a justified usability mode,
recorded evidence, and its quarantined material is promoted or rejected.
