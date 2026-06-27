# Architecture — Interface Intelligence OS

> The six-engine architecture of IIOS, with diagrams for module structure, context flow,
> decision flow, the secure-ingestion trust boundary, the compilation pipeline, the
> assurance pipeline, the governance loop, and the agent/deterministic-tool boundary.
>
> **Honesty marker on diagrams.** Boxes are tagged where useful: **[impl]** implemented
> (carried from Motif v1.0.0), **[exp]** experimental, **[plan]** planned. Only the secure
> interaction foundation is fully implemented today; see the roadmap and capability matrix.

---

## 1. Module architecture

IIOS is six cooperating engines over a shared context model and a secure supply chain, all
driven by an orchestrator and exposed through the `ii` CLI and deterministic tools. Engine
names map to top-level directories (`design-intelligence/`, `product-intelligence/`,
`interaction-intelligence/`, `implementations/` + `compiler/`, `assurance/`, `governance/`).

```mermaid
flowchart TB
  subgraph Agent["Agent layer"]
    ORCH["Orchestrator SKILL.md [plan]"]
    SPEC["15 specialist subagents [plan]"]
  end
  subgraph Tools["Deterministic tools (ii CLI, stdlib-only)"]
    CLI["ii / oii / motif CLI [impl/plan]"]
    VAL["validate · rank · scan [impl]"]
  end
  subgraph Engines["Six engines"]
    PI["Product Intelligence<br/>Context Manifest · Genome [plan]"]
    DI["Design Intelligence<br/>style·colour·type·layout·UX [exp]"]
    II["Interaction Intelligence<br/>patterns·effects·spec graph [impl]"]
    IMP["Implementation<br/>adapters·compiler·fidelity [impl/plan]"]
    AS["Assurance<br/>state·a11y·perf·motion [partial]"]
    GOV["Governance & Learning<br/>ledger·drift·originality [plan]"]
  end
  subgraph Foundation["Secure supply chain [impl]"]
    REG["Registry (~90 sources)"]
    SCAN["5 scanners + licence gate"]
    INST["Controlled installer"]
  end
  CTX[("Shared context<br/>+ schemas")]

  ORCH --> SPEC
  ORCH --> CLI
  SPEC --> Engines
  CLI --> VAL --> Engines
  PI --> CTX
  DI --> CTX
  II --> CTX
  Engines --> CTX
  II --> Foundation
  IMP --> Foundation
  AS --> GOV
  Foundation --> REG & SCAN & INST
```

**Key relationships.** Product Intelligence seeds the shared context; Design and Interaction
Intelligence reason over it; Implementation compiles it; Assurance verifies it; Governance
records and maintains it. The secure supply chain underlies Interaction and Implementation
whenever third-party material is involved.

---

## 2. Context flow

Information flows from product understanding down to implementation — never the reverse.
This enforces *reason from context, not aesthetics* and *fidelity follows certainty*.

```mermaid
flowchart LR
  A["Product purpose"] --> B["User & intent"]
  B --> C["Screen / surface"]
  C --> D["Interaction objective"]
  D --> E["Pattern (preferred)"]
  E --> F["Effect (only if needed)"]
  F --> G["Implementation (framework)"]
  A -.Context Manifest.-> CTX[("Shared context")]
  B -.Product Design Genome.-> CTX
  D -.Interaction Spec Graph.-> CTX
  E -.decision + provenance.-> CTX
  CTX --> G
```

Each stage writes to the shared context, so later stages (and Assurance/Governance) can see
*why* earlier choices were made. The chain mirrors the foundation's
`purpose > product > intent > screen > objective > pattern > effect > implementation`.

---

## 3. Decision flow

How a single interface decision is made: search for the simplest sufficient option, gate it
on safety, and record it.

```mermaid
flowchart TB
  start(["Need: objective on a surface"]) --> ctx{"Context manifest exists?"}
  ctx -- no --> stop1["Refuse: build context first [fidelity gate]"]
  ctx -- yes --> cand["Generate candidates<br/>(pattern before effect, native before lib)"]
  cand --> rank["Transparent ranking [impl]"]
  rank --> simplest["Pick least-complex sufficient"]
  simplest --> gate{"Safety gates"}
  gate -->|a11y / reduced-motion fail| reject["Reject / choose simpler"]
  gate -->|perf / INP budget fail| reject
  gate -->|licence / security fail| reject
  gate -->|originality: too generic [exp]| revise["Revise toward intentional"]
  gate -->|pass| sel["Select"]
  revise --> cand
  reject --> cand
  sel --> ledger["Record in decision ledger<br/>(rationale + rejected alternatives) [plan]"]
  ledger --> done(["Decision committed"])
```

---

## 4. Secure-ingestion trust boundary

The foundation's defining property: untrusted-by-default ingestion. Nothing third-party is
executed, and nothing crosses into the trusted registry without passing every gate.
**[impl]** — this is shipped in Motif v1.0.0.

```mermaid
flowchart LR
  subgraph Untrusted["UNTRUSTED zone"]
    NET["Allowlisted official host"]
    Q[".motif/quarantine/<br/>(never executed)"]
  end
  subgraph Gate["Gates (deterministic, stdlib)"]
    S1["Dangerous-pattern scanner"]
    S2["Browser-behaviour scanner"]
    S3["Dependency scanner"]
    S4["Licence scanner + gate"]
    S5["Secret scanner"]
  end
  subgraph Trusted["TRUSTED zone"]
    REG["Approved registry"]
    IMPL["Clean-room / adapted impl"]
  end
  NET -->|explicit `source retrieve --refresh`| Q
  Q --> S1 --> S2 --> S3 --> S4 --> S5
  S4 -. unknown / restricted .-> RO["reference-only<br/>(re-implement concept)"]
  S5 -->|all pass| REG
  RO --> IMPL
  REG --> IMPL
  classDef danger fill:#ffe9e9,stroke:#c00;
  class Untrusted danger;
```

The **trust boundary** is the line between quarantine and the approved registry. Default
operation is fully offline against the committed registry; the network is touched only on an
explicit refresh against an allowlisted host. Third-party install scripts never run.

---

## 5. Compilation pipeline

How a verified context becomes framework-correct, own-your-source code, ascending the
fidelity ladder. **[plan for v0.3]**, building on implemented adapters.

```mermaid
flowchart LR
  CM["Context Manifest [plan]"] --> ISL["Interface Spec (ISL) [plan]"]
  ISL --> ISG["Interaction Spec Graph [exp]"]
  ISG --> L0["L0 structure / low-fi"]
  L0 --> L1["L1 states (all required) [plan]"]
  L1 --> L2["L2 high-fidelity"]
  L2 --> ADP{"Framework adapter [impl]"}
  ADP -->|browser-native| OUT1["Output"]
  ADP -->|Vue / Frappe-Vue| OUT1
  ADP -->|React / Svelte| OUT1
  OUT1 --> PROV["Provenance + ledger entry [plan]"]
  classDef gate fill:#fff3cd,stroke:#b8860b;
  class L0,L1,L2 gate;
```

The **fidelity gate** between L0→L1→L2 is the enforcement of *fidelity follows certainty*:
the compiler will not emit L2 high-fidelity before L1 state-completeness is satisfied.

---

## 6. Assurance pipeline

Verification with recorded evidence — and honest coverage statements. **[partial → v0.3]**.

```mermaid
flowchart TB
  art["Candidate UI / spec"] --> SC["State completeness check [plan]"]
  SC --> A11Y["Accessibility: axe-core rules → WCAG 2.2 SC [partial]<br/>contrast · target-size · focus · keyboard"]
  A11Y --> RM["Reduced-motion check [impl: policy]"]
  RM --> PERF["Performance: INP-aware + motion budgets [partial]"]
  PERF --> EV["Evidence record<br/>(rule → finding → standard)"]
  EV --> COV{"Coverage honest?"}
  COV --> H["State automated coverage limits<br/>(~half of a11y issues) + flag for human"]
  H --> verdict{"Pass?"}
  verdict -->|fail| back["Back to decision/compile"]
  verdict -->|pass w/ caveats| gov["Hand to Governance"]
```

Assurance mirrors axe-core's own honesty: it never claims full compliance from automation;
it records what it checked, what passed, and what a human must still review.

---

## 7. Governance loop

The long-horizon coherence loop: record, detect drift, correct, learn. **[plan]**.

```mermaid
flowchart LR
  DEC["Decisions + provenance"] --> LED[("Decision ledger [plan]")]
  LED --> DRIFT["Debt / drift scoring<br/>vs recorded decisions [plan]"]
  DRIFT --> ORIG["Originality / convergence audit [exp]"]
  ORIG --> FLAG{"Divergence or<br/>generic-template signal?"}
  FLAG -->|yes| FIX["Recommend consolidation /<br/>distinctive revision"]
  FLAG -->|no| OK["Maintain"]
  FIX --> ORCH["Back to orchestrator"]
  OK --> LED
  LED -. learning .-> DI["Improve Design/Interaction defaults"]
```

The loop keeps quality from silently degrading across a long agent session and feeds
learnings back into design/interaction defaults.

---

## 8. Agent / deterministic-tool boundary

The architectural line that makes IIOS auditable: **judgment** is for agents; anything
**safety-affecting, repeatable, or auditable** runs in deterministic, dependency-free tools.

```mermaid
flowchart TB
  subgraph AgentSide["Agents — judgment & synthesis (non-deterministic)"]
    O["Orchestrator"]
    P["Specialists: product, design, interaction,<br/>state, a11y, perf, originality, …"]
  end
  subgraph ToolSide["Deterministic tools — ii CLI (stdlib, repeatable)"]
    V["validate (schemas)"]
    R["rank (transparent)"]
    SC["scan (5 scanners + licence gate)"]
    AS["assurance checks (axe-core/Playwright wrappers)"]
    LG["ledger / drift scoring"]
  end
  O -->|calls| V & R & SC & AS & LG
  P -->|calls| V & R & SC & AS
  V & R & SC & AS & LG -->|facts, not opinions| O
  note["Rule: a decision that affects safety, licensing,<br/>or auditability MUST be produced by a tool,<br/>not asserted by an agent."]:::n
  classDef n fill:#eef,stroke:#557;
```

**Why this boundary.** Agents are powerful but non-deterministic; safety decisions must be
reproducible and inspectable. By pushing validation, scanning, licence gating, ranking,
assurance, and ledger/drift scoring into stdlib-only tools, IIOS guarantees that the same
input yields the same safety verdict, that `make check` runs anywhere, and that every
safety-affecting result is auditable independent of the agent that requested it.

---

## How the engines compose (summary)

| Engine | Reads | Produces | Status |
|--------|-------|----------|:------:|
| Product Intelligence | brief, repo | Context Manifest, Product Design Genome | plan |
| Design Intelligence | context, DTCG tokens, design knowledge | style/colour/type/layout/UX choices | exp |
| Interaction Intelligence | context, registry | pattern/effect selection, Interaction Spec Graph | **impl** |
| Implementation | spec, adapters | framework-correct own-your-source code | impl + plan |
| Assurance | artefact/spec | state/a11y/perf/motion evidence (honest coverage) | partial |
| Governance & Learning | decisions | ledger, drift/debt, originality audit | plan |
| Secure supply chain | external sources | approved registry, provenance | **impl** |

The architecture's load-bearing ideas are constant across statuses: **context before
aesthetics, least complexity that works, fidelity follows certainty, safety in deterministic
tools, and every decision recorded.**
