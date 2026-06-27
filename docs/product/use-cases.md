# Use Cases — Interface Intelligence OS

Concrete scenarios IIOS is built to handle. Each names the engines involved and the
honest status of the capability (**implemented** / **experimental** / **planned**), per the
project capability matrix. Today, only the secure interaction foundation is fully
implemented; the rest are partial/experimental/planned and labelled accordingly.

---

## UC‑1 — Build a feature screen from a product brief

*"Build the subscription-management screen for our billing app."*

1. **Product Intelligence** builds a Context Manifest (product type = web app, user = paying
   admin, objectives = view/upgrade/cancel) — *planned (v0.2 schema)*.
2. **Interaction Intelligence** selects the least-complex patterns (status changes, optimistic
   save, destructive confirmation for cancel) — *implemented (foundation)*.
3. **Design Intelligence** proposes a distinctive-but-appropriate layout/typography/colour,
   not the modal SaaS template — *experimental*.
4. **State Completeness** requires empty/loading/error/permission-denied/overflow states —
   *planned*.
5. **Implementation** emits framework-correct, own-your-source code (e.g. Frappe-Vue) —
   *implemented (adapters)*.
6. **Assurance** runs a11y/perf/motion checks and records evidence — *partial*.
7. **Governance** writes the decision ledger entry — *planned*.

## UC‑2 — Add a tasteful interaction without hurting UX

*"Make the save feel responsive and add a subtle confirmation."*

- Interaction Intelligence chooses **optimistic-save + pending→saving→saved** over a heavy
  animation; enforces `prefers-reduced-motion`; keeps handlers INP-friendly. Refuses motion
  that blocks the main thread. — *implemented (patterns + budgets)*.

## UC‑3 — Safely reuse a third-party effect or component

*"Use that fancy animated card from <site>."*

- Secure supply chain: ingest into quarantine → five scanners → **licence gate**. If the
  licence is unknown/Commons-Clause/restricted, it becomes `reference-only` and IIOS
  re-implements the *concept* clean-room instead of copying. Controlled installer plans,
  snapshots, patches, validates, and can auto-rollback. — *implemented (foundation)*.

## UC‑4 — Guarantee state completeness before sign-off

*"Is this list view actually done?"*

- State Completeness Engine checks the required matrix (empty, loading, partial, ideal,
  error, offline, permission-denied, overflow) and fails sign-off if any applicable state is
  unaddressed. — *planned (matrix + validate)*.

## UC‑5 — Accessibility & performance assurance with honest coverage

*"Prove this meets our bar."*

- Assurance runs axe-core-class checks, maps findings to WCAG 2.2 SC, checks contrast/
  target-size/focus and reduced-motion, and reports INP-aware performance budgets — while
  **stating that automated coverage is partial (~half of issues)** and flagging the rest for
  human review. — *partial*.

## UC‑6 — Resist generic-AI convergence

*"Does this just look like every other AI site?"*

- Originality / Aesthetic-Convergence Detector flags default-template signatures (stock
  gradient-on-dark hero, generic component clichés) and nudges toward intentional design. —
  *experimental*.

## UC‑7 — Keep a long agent session coherent

*"We've been editing for hours — has the design drifted?"*

- Governance computes interface debt/drift against the decision ledger, flags divergence and
  duplicate components, and recommends consolidation. — *planned*.

## UC‑8 — Govern an agent fleet for an enterprise

*"Every team's agents must meet our standards."*

- Org-level: enforced licence/security gate, assurance evidence, and auditable ledgers across
  repos; design-system conformance via DTCG tokens and drift auditing. — *partial /
  planned*; security gate *implemented*.

## UC‑9 — Conform agent output to an existing design system

*"Make it match our system."*

- Design Intelligence consumes the team's DTCG tokens and patterns; Governance audits for
  divergence. — *experimental / planned*.

## UC‑10 — Benchmark interface quality (InterfaceBench)

*"How good is this agent at interfaces, really?"*

- InterfaceBench runs scenario rounds against a published rubric (judgment, completeness,
  a11y, performance, originality, security) and reports reproducible scores — never marketing
  numbers. — *planned (foundation in v0.2)*.

## UC‑11 — Extend IIOS (OSS contribution)

*"Add a new source / specialist agent / assurance check."*

- Author a machine-readable record or skill against the schemas; `make check` validates it
  (dependency-free); honesty rules apply (mark verified vs pending). — *implemented (schemas
  + gate)*.

---

## Coverage snapshot

| Use case | Lead engine | Status |
|----------|-------------|:------:|
| UC‑1 Feature from brief | Product → all | mixed (foundation done; new engines planned) |
| UC‑2 Tasteful interaction | Interaction | **implemented** |
| UC‑3 Safe reuse | Secure supply chain | **implemented** |
| UC‑4 State completeness | Assurance | planned |
| UC‑5 A11y/perf assurance | Assurance | partial |
| UC‑6 Anti-convergence | Design + Governance | experimental |
| UC‑7 Long-horizon coherence | Governance | planned |
| UC‑8 Enterprise fleet | Governance | partial/planned |
| UC‑9 Design-system conformance | Design + Governance | experimental/planned |
| UC‑10 InterfaceBench | Assurance | planned |
| UC‑11 Extend IIOS | (schemas + gate) | **implemented** |
