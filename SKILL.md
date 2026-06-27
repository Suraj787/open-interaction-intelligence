---
name: interface-intelligence-os
description: Use when an AI coding agent must design, build, improve, audit, or migrate any web interface and needs to choose the least-complex interface and interaction that achieves a real user outcome, governed by evidence rather than aesthetic impulse.
---

# Interface Intelligence OS

Interface Intelligence OS (IIOS) is the intelligence and governance layer between
product intent, AI coding agents, design systems, public UI libraries, and production
validation. It is **not** a component dump or an animation bundle.

**Defining principle:** First determine what the user needs to **understand, feel,
decide, or accomplish**. Then choose the **least complex** interface and interaction
that achieves that outcome.

This file is an **orchestrator**. It loads knowledge selectively from the six engines
and delegates to specialist skills. Do not inline whole knowledge bases; pull only the
slice the current step needs.

## Six engines

- **Design Intelligence** — `design-intelligence/` — classification, layout, type,
  colour, content, data-viz, UX principles, responsive, styles, framework guidance.
- **Product Intelligence** — `product-intelligence/` — product/user/workflow/risk/
  environment models and confidence.
- **Interaction Intelligence** — `interaction-intelligence/` — patterns, states,
  feedback, motion, density, navigation, anti-patterns.
- **Implementation Intelligence (compiler)** — `compiler/` — native-framework plans.
- **Assurance** — `assurance/` — accessibility, performance, security, visual checks.
- **Governance and Learning** — `governance/` — genome, interaction graph, decision
  ledger, debt, drift, exceptions, learning.

Vue and Frappe-Vue are first-class targets. Default runtime is the **offline approved
registry**; reach the internet only through an explicit, reviewed source refresh.

## Mandatory 18-step workflow

1. **Inspect the repo** — read structure, configs, conventions (`ii inspect`).
2. **Detect stack** — framework, language, styling system, dependencies, existing
   components, and test setup.
3. **Classify the task** — one of: new-website, new-web-app, improve, design-system,
   component, audit, migration (`ii classify`).
4. **Model product and users** — purpose, product type, audiences, jobs-to-be-done.
5. **Identify workflows** — tasks, frequency, risk, data density, device, environment.
6. **Load the Product Design Genome** — extract it if absent, else load it
   (`ii genome`).
7. **Build/update the Interaction Specification Graph** — entities, screens, states,
   flows (`ii graph`).
8. **Identify the actual problem** — the real outcome at stake, not the requested
   decoration.
9. **Generate multiple structural concepts** — only when ambiguity justifies it;
   otherwise proceed with one.
10. **Check generic AI-aesthetic convergence** — flag templated, derivative output.
11. **Select UX patterns before effects** — pattern first, motion/effect second.
12. **Search approved components and recipes** — registry first (`ii registry search`).
13. **Prefer existing project components and dependencies** before adding anything.
14. **Compile a native-framework plan** — in the detected stack (`ii compile`).
15. **Validate required states** — empty, loading, partial, error, success, offline,
    permission-denied, dense, zero-data.
16. **Run assurance** — accessibility, performance, security, visual (`ii assure`).
17. **Record decisions and provenance** — rationale, sources, licences (`ii ledger`).
18. **Update debt and drift** — open debt, reconcile against genome and graph
    (`ii debt`, `ii drift`).

## Hard rules (never)

- Never add animation solely because it is impressive.
- Never install React into a Vue/Svelte/Angular project for one effect.
- Never ignore an existing design system without explicit justification.
- Never add a dependency without a licence, security, and cost review.
- Never execute unreviewed code fetched from the internet.
- Never use WebGL when CSS, SVG, or native rendering suffices.
- Never rely only on motion or colour to convey meaning.
- Never remove visible focus.
- Never make essential actions hover-only.
- Never block input for decorative animation.
- Never ship motion without a reduced-motion path.
- Never treat automated accessibility checks as complete proof.
- Never claim measured performance without measurement.
- Never present low-confidence inference as verified fact.
- Never reconstruct premium or restricted components from previews.
- Never let visual novelty outrank user outcomes.

## Specialist skills (load selectively)

- `skills/orchestrator` — thin entry that defers here.
- `skills/product-intelligence` — product/user/workflow/risk/environment modelling.
- `skills/design-intelligence` — classification, layout, type, colour, content, viz.
- `skills/interaction-intelligence` — patterns, states, feedback, motion, density.
- `skills/originality-intelligence` — AI-aesthetic convergence and novelty checks.
- `skills/framework-compiler` — native-framework implementation plans.
- `skills/accessibility-assurance` — keyboard, focus, semantics, reduced-motion.
- `skills/performance-assurance` — budgets, measured cost, jank avoidance.
- `skills/security-assurance` — dependency, supply-chain, untrusted-code review.
- `skills/visual-assurance` — rendering, states, responsive, design-system fidelity.
- `skills/governance` — genome, interaction graph, decision ledger, debt, drift.

The Motif interaction foundation (`motif`, `skills/interaction-design`, and the other
`skills/*` from that layer) remains available; IIOS composes it rather than replacing it.

## CLI

The primary CLI is `ii` (aliases `oii`, `motif`). It exposes repo inspection, task
classification, genome extraction, the interaction graph, registry search, native
compilation, assurance runs, the decision ledger, and debt/drift tracking. Prefer the
CLI over ad-hoc internet retrieval; it enforces the offline-approved-registry default
and writes provenance automatically.

## Before implementation, record

Task type; product and user models; workflows with frequency/risk/density; the genome
slice in force; the interaction-graph nodes touched; the actual problem; candidate
concepts and selection rationale; the chosen patterns before effects; registry and
project components reused; the native compile plan; the required-states list.

## After implementation, report

Patterns and effects implemented in the target framework; assurance results
(accessibility, performance with measurement, security, visual) with their limits
stated; states validated; dependencies added with licence and cost notes, or none;
decision ledger and provenance entries written; debt opened and drift reconciled;
confidence level for any inference presented.
