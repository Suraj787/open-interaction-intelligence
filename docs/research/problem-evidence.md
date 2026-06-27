# Problem Evidence — Interface Intelligence OS

> Each problem category below is stated, **grounded in cited evidence** (see the
> [research ledger](./research-ledger.md)), and converted into an **engineering
> requirement** IIOS must satisfy. Where a figure is volatile (a metric threshold, an
> annual report), it is marked. Claims that are our synthesis rather than a source
> statement are marked *(inference)*.

---

## P1 — Generic AI aesthetics / convergence ("the sea of sameness")

**Evidence.** LLMs trained on the same internet-scale corpora regress toward the
statistically common form, so AI-assisted design "converges toward identical structures,
phrases, and tonal patterns". For UI specifically, models "probabilistically default to
the same familiar patterns — generic layouts, standard component libraries, and a clean
but non-distinctive professional veneer". Academic work on *design homogenization in web
vibe coding* documents this convergence directly, and model-collapse research shows
outputs growing more homogeneous as models train on AI-generated content.

- *Interrogating Design Homogenization in Web Vibe Coding* — arXiv (preprint; tier 4, not
  yet peer-reviewed): https://arxiv.org/html/2603.13036v1
- Industry synthesis on AI "sea of sameness" / visual homogenization (tier 5–7).

**Engineering requirement.** IIOS provides an **Originality / Aesthetic-Convergence
Detector**: heuristic rules that flag default-template signatures (stock gradient-on-dark
hero, generic SaaS layout, over-used component clichés) and an audit that pushes toward
intentional, context-fit design. Design Intelligence proposes *distinctive-but-appropriate*
options, not the modal default. *(The detector is heuristic, not a guarantee — marked
experimental in the capability matrix.)*

---

## P2 — Premature high-fidelity generation

**Evidence.** The dominant generators (v0, Stitch, Figma Make) optimise for jumping
straight to a polished, high-fidelity coded artefact from a prompt (see the
[competitive analysis](./competitive-analysis.md)). This is powerful but skips the
cheap-iteration stages (intent → information architecture → low-fidelity → states) where
the costly mistakes are actually caught — a long-standing UX principle that fidelity should
follow certainty *(inference, consistent with established design practice / NN/g, ledger #7)*.

**Engineering requirement.** IIOS enforces a **fidelity ladder**: product/context manifest
→ interaction specification → structure/low-fidelity → states → high-fidelity → assurance.
The orchestrator refuses to emit high-fidelity output before the product context and state
matrix exist. Fidelity is a governed gate, not a default.

---

## P3 — Happy-path-only UI (missing states)

**Evidence.** Generators and hand-authored stories alike tend to render the *success*
state and omit empty, loading, error, partial, offline, permission-denied, and
zero/overflow-data states. Storybook's own model — authors write the stories they remember
to write — illustrates that completeness depends on discipline, not defaults (ledger #16).
Missing error/empty states are among the most common real-world UI defects *(inference)*.

**Engineering requirement.** IIOS provides a **State Completeness Engine**: a required
state matrix per component/screen (at minimum: empty, loading, partial, ideal, error,
offline/degraded, permission-denied, overflow), validated before sign-off. A UI that has
not addressed each applicable state cannot pass assurance.

---

## P4 — Accessibility failures

**Evidence (strong, measured).** The **WebAIM Million 2025** report found **94.8%** of the
top one-million home pages had detected WCAG 2 failures, averaging ~51 errors per page;
**low-contrast text** was the single most common failure (79.1% of pages) (ledger #4,
*volatile* — annual). Automated tooling only catches part of this: **axe-core detects up to
~57%** of issues and explicitly flags the rest as needing manual review (ledger #5). The
standard itself is **WCAG 2.2**, a W3C Recommendation since **2023‑10‑05**, adding criteria
like target size and focus-not-obscured (ledger #1–2).

**Engineering requirement.** Accessibility is **mandatory, not optional**, in IIOS.
The Assurance engine runs axe-core-class automated checks, maps each finding to a WCAG 2.2
success criterion, enforces contrast and target-size at design time, requires
keyboard/focus and reduced-motion handling — and, mirroring axe-core's honesty, **records
that automated coverage is partial** and flags items for human review rather than claiming
full compliance.

---

## P5 — Performance & motion failures

**Evidence.** Responsiveness is now measured by **INP**, which **replaced FID as a Core Web
Vital on 2024‑03‑12**; "good" INP is **≤200 ms at p75** (ledger #3, *volatile*). Heavy,
main-thread-blocking animation and unbounded effects degrade INP and harm users who are
motion-sensitive; browser-native primitives (View Transitions, Web Animations, scroll-driven
animations, Intersection Observer) are the cheaper, more accessible path (MDN, ledger #8).

**Engineering requirement.** IIOS carries **performance and motion budgets**: prefer the
least-complex, browser-native technique that achieves the objective; enforce
`prefers-reduced-motion` fallbacks; keep interaction handlers within INP-friendly bounds;
and reject motion that hurts performance or accessibility. Assurance includes static
performance/motion checks tied to these budgets.

---

## P6 — Security & supply-chain risk

**Evidence.** The "easy" agent path — scrape a site, run its install script, copy its code
— executes untrusted third-party code and ignores licence terms. Registries (shadcn, v0,
arbitrary third-party) are powerful but place **trust on the consumer**; design-system
assets frequently carry **different and restrictive terms from their code** (Polaris's
field-of-use restriction; SLDS's CC‑BY‑NC‑ND assets; Commons-Clause "source-available"
collections) — all documented in `registry/sources/` and the
[competitive analysis](./competitive-analysis.md).

**Engineering requirement.** IIOS keeps the foundation's **secure supply chain**:
offline-approved registry by default; untrusted-by-default ingestion into quarantine;
five static scanners (dangerous patterns, browser behaviour, dependencies, licence,
secrets); a **licence gate** (`unknown → reference-only`; source-available/Commons-Clause
not treated as permissive); and a controlled installer (plan, snapshot, patch, validate,
auto-rollback, provenance). Third-party install scripts never run against the user's repo.
*(Risk-reducing, not risk-eliminating — human review remains required.)*

---

## P7 — Design drift & long-horizon degradation

**Evidence.** Over a long agent session or many edits, decisions made early (tokens,
spacing scale, interaction grammar, naming) erode: new code diverges from established
patterns, duplicate components accumulate, and the system's coherence decays — "interface
debt". This is the UI analogue of code drift in long agent runs *(inference; the
mechanism — context loss over long horizons — is well established for coding agents)*.

**Engineering requirement.** IIOS provides a **Decision Ledger** (every selection recorded
with rationale, provenance, and the rejected alternatives) plus **Interface Debt & Drift**
scoring: heuristics that detect divergence from recorded decisions and accumulating
inconsistency, surfaced through the CLI and the governance loop so quality is maintained
across long horizons rather than silently degrading.

---

## Requirements traceability

| # | Problem | Primary evidence | IIOS engine / mechanism | Status |
|--:|---------|------------------|-------------------------|:------:|
| P1 | Generic-AI convergence | arXiv vibe-coding homogenization; industry synthesis | Design Intelligence + Originality Detector | experimental |
| P2 | Premature high-fidelity | Generator positioning; UX fidelity principle | Fidelity ladder (orchestrator gate) | planned→v0.3 |
| P3 | Missing states | Storybook authorship model; common defects | State Completeness Engine | planned (schema in v0.2) |
| P4 | Accessibility failures | WebAIM Million 2025 (94.8%); axe-core ~57%; WCAG 2.2 | Assurance (axe-core + design-time a11y) | partial |
| P5 | Performance/motion | INP CWV (≤200 ms p75, 2024‑03‑12); MDN native APIs | Performance/motion budgets + Assurance | partial |
| P6 | Security/supply-chain | Registry trust model; mixed design-system licences | Secure supply chain + licence gate | **implemented (foundation)** |
| P7 | Design drift | Long-horizon agent context loss | Decision Ledger + Debt/Drift | planned |

Status reflects the capability matrix: only the secure supply chain (P6) is fully
implemented today (carried from Motif v1.0.0); the rest are partial/experimental/planned
and labelled as such — never claimed as done.
