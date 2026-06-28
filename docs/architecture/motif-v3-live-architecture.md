# Motif v3 "Motif Live", Layered Architecture

> Motif v3 evolves Motif v2.0.0 (intelligence + governance) into a **runtime / execution /
> assurance / governance** platform. The command is `motif` (aliases `ii`, `oii`).
>
> **Honesty is mandatory.** Every box and capability below is tagged:
> **[impl]** implemented and verified by `make check`, **[exp]** experimental (interface +
> static layers built; runtime execution needs a browser runtime not installed here),
> **[plan]** planned (designed, not built). The browser-runtime surfaces, Visual Twin
> screenshot rendering, Playwright/axe assurance, live preview, pixel/semantic visual diff,
> and interactive Studio apply, are **[exp]/[plan]** because no browser runtime (Playwright)
> is present. The deterministic surfaces, findings, policy, memory, Atlas static site, MCP
> server, Guardian, design-system extraction, run/create/improve orchestration,
> recommendation, and the compile plan, are **[impl]**. This document mirrors
> [`docs/reviews/motif-v3-gap-analysis.md`](../reviews/motif-v3-gap-analysis.md); if the two
> ever disagree, the gap analysis wins.

---

## 1. The layered model

Motif v3 reasons top-down from human intent through to a delivered, validated interface, then
feeds evidence back up. Each layer consumes the layer above and emits typed records into
`.motif/` (the runtime state) governed by schemas in `schemas/`.

```mermaid
flowchart TB
  H["Human intent / existing interface"]
  P["Product layer, context, product model, risk [impl]"]
  D["Design layer, genome, tokens, design-system extract [impl]"]
  I["Interaction layer, patterns, effects, spec graph [impl]"]
  M["Implementation layer, adapters, compiler plan [impl] / apply [exp]"]
  R["Runtime + Visual Twin, inspect, start, observe, twin [exp]"]
  A["Assurance, a11y, perf, behaviour, visual diff [exp]"]
  G["Governance, findings, policy, memory, decisions [impl]"]
  S["Surfaces, Studio / Atlas / MCP / Guardian"]

  H --> P --> D --> I --> M --> R --> A --> G
  G -. "evidence + memory feeds back up" .-> P
  G --> S
  M --> S
  classDef impl fill:#e6ffed,stroke:#2da44e;
  classDef exp fill:#fff8c5,stroke:#bf8700;
  class P,D,I,G impl;
  class R,A exp;
```

**Reading the stack.** Product establishes *why* and *for whom*; Design fixes the visual
grammar; Interaction selects *patterns before effects*; Implementation compiles a concrete
plan; Runtime brings the target app up in isolation and builds a Visual Twin; Assurance
checks the running result against policy; Governance records findings, decisions and memory;
the Surfaces (Studio, Atlas, MCP, Guardian) expose all of it over one shared source of truth.

---

## 2. Create flow

`motif create` turns a brief into a spec, context, ranked concepts and a compile plan. The
preview and compile-apply tail is experimental (needs rendering).

```mermaid
flowchart LR
  brief["Brief / spec input"] --> spec["Spec normalise [impl]"]
  spec --> ctx["Product context + genome [impl]"]
  ctx --> rec["Recommend sources/patterns [impl]"]
  rec --> con["Generate concepts [impl]"]
  con --> sel["Compare + select [impl]"]
  sel --> plan["Compile plan [impl]"]
  plan -.-> prev["Visual preview [exp]"]
  plan -.-> apply["Apply in worktree [exp]"]
  apply -.-> val["Validate + record [exp]"]
  classDef exp fill:#fff8c5,stroke:#bf8700;
  class prev,apply,val exp;
```

## 3. Improve flow

`motif improve` inspects an existing interface, models it, discovers issues into the unified
Finding model, generates concepts and a plan. Starting the live app and capturing it are
experimental.

```mermaid
flowchart LR
  tgt["Existing interface"] --> insp["Inspect + detect framework [impl]"]
  insp --> model["Model routes/components [impl]"]
  model -.-> start["Start app [exp]"]
  model --> disc["Discover problems [impl]"]
  start -.-> cap["Capture twin [exp]"]
  disc --> find["Findings (typed, lifecycle) [impl]"]
  cap -.-> find
  find --> con["Concepts [impl]"]
  con --> plan["Compile plan [impl]"]
  plan -.-> prev["Preview + apply [exp]"]
  classDef exp fill:#fff8c5,stroke:#bf8700;
  class start,cap,prev exp;
```

## 4. `motif run`, the flagship runtime pipeline

The full loop. Deterministic stages run today; stages that need a browser are experimental
and gated behind `--allow-runtime`/explicit apply, never default.

```mermaid
flowchart TB
  Inspect["Inspect [impl]"] --> Model["Model [impl]"] --> Start["Start [exp]"]
  Start --> Discover["Discover [impl]"] --> Observe["Observe [exp]"]
  Observe --> Twin["Twin [exp]"] --> Audit["Audit [exp]"]
  Audit --> Concepts["Concepts [impl]"] --> Recommend["Recommend [impl]"]
  Recommend --> Preview["Preview [exp]"] --> Plan["Plan [impl]"]
  Plan --> ApplyIso["Apply-in-isolation (worktree) [exp]"]
  ApplyIso --> Validate["Validate [exp]"] --> Compare["Compare [exp]"]
  Compare --> Record["Record [impl]"] --> Deliver["Deliver / rollback [impl]"]
  Deliver -. "rollback restores worktree + .motif/rollback" .-> Inspect
  classDef impl fill:#e6ffed,stroke:#2da44e;
  classDef exp fill:#fff8c5,stroke:#bf8700;
  class Inspect,Model,Discover,Concepts,Recommend,Plan,Record,Deliver impl;
  class Start,Observe,Twin,Audit,Preview,ApplyIso,Validate,Compare exp;
```

Every run writes a `run-record` (schema `schemas/run-record.schema.json`) into
`.motif/runs/<id>/` capturing mode, goal, target commit, commands, files changed, findings,
concepts and outcome, so a run is reproducible and reversible.

## 5. Visual Twin

A typed, source-derived model of the interface. The manifest, routes and component
fingerprints come from **static source analysis** and are real today; screenshots, the
accessibility tree and traces require Playwright and are experimental.

```mermaid
flowchart LR
  src["Source tree"] --> det["Framework detect [impl]"]
  det --> routes["Route + screen map [impl]"]
  det --> comp["Component fingerprints [impl]"]
  routes --> man["twin-manifest.json [impl]"]
  comp --> man
  man -. "rendered=false until a runtime renders" .-> shots["Screenshots [exp]"]
  man -.-> axe["a11y tree [exp]"]
  man -.-> trace["Perf trace [exp]"]
  classDef exp fill:#fff8c5,stroke:#bf8700;
  class shots,axe,trace exp;
```

The manifest carries `"rendered": false` until a real runtime fills the pixel layer; nothing
downstream claims visual truth from an unrendered twin.

## 6. Compiler

The compiler extends the v2 controlled installer. `compile plan` is implemented; preview is
experimental; apply/pr are partial and always operate in an isolated worktree.

```mermaid
flowchart LR
  intent["Concept + spec"] --> map["Map to adapters/registry [impl]"]
  map --> plan["compile plan (ordered, reversible) [impl]"]
  plan -.-> prev["compile preview [exp]"]
  plan --> apply["compile apply (worktree) [partial]"]
  apply --> pr["compile pr [partial]"]
  apply --> rb["rollback record [impl]"]
  classDef exp fill:#fff8c5,stroke:#bf8700;
  class prev exp;
```

## 7. Assurance

Interface and static-check layers are implemented; runtime layers (Playwright + axe, real
perf, rendered visual regression) are experimental.

```mermaid
flowchart TB
  subgraph Static["Static layers [impl]"]
    cfg["Config / token checks"]
    semgrep["Pattern + anti-pattern checks"]
  end
  subgraph Runtime["Runtime layers [exp]"]
    a11y["axe accessibility"]
    perf["Performance trace"]
    behav["Playwright behaviour"]
    vis["Visual regression"]
  end
  Static --> ev["assurance-evidence records [impl]"]
  Runtime -.-> ev
  ev --> gate["Policy gate [impl]"]
  classDef exp fill:#fff8c5,stroke:#bf8700;
  class a11y,perf,behav,vis exp;
```

## 8. MCP server

A stdlib JSON-RPC-over-stdio server exposing the shared source of truth to MCP clients.
Read tools are open; write tools are guarded (dry-run default, audit log).

```mermaid
flowchart LR
  client["MCP client (Claude Code, etc.)"] <-->|JSON-RPC/stdio| srv["motif mcp serve [impl]"]
  srv --> reg["Registry / Atlas data [impl]"]
  srv --> find["Findings / memory / policy [impl]"]
  srv --> guarded["Guarded writes (dry-run, audited) [impl]"]
  guarded --> log["Audit log [impl]"]
```

## 9. Guardian

Local + PR-time governance gate over staged/branch diffs, with trend tracking.

```mermaid
flowchart LR
  diff["Staged / branch diff"] --> guard["motif guard [impl]"]
  guard --> pol["Policy as code [impl]"]
  guard --> orig["Originality / debt gates [impl]"]
  guard --> verdict["Pass / warn / fail + report [impl]"]
  verdict --> ci["GitHub Action [impl]"]
  verdict --> trend["Trend history [impl]"]
```

## 10. Source-update lifecycle

New external sources pass through quarantine, scanning and review before entering the
approved registry. Live network refresh is planned; the offline approved registry is the
exercised runtime.

```mermaid
flowchart LR
  ext["Candidate source"] --> q[".motif/quarantine [impl]"]
  q --> scan["5 scanners + licence gate [impl]"]
  scan --> rev[".motif/reviewed [impl]"]
  rev -->|approve| appr[".motif/approved → registry [impl]"]
  rev -->|reject| rej[".motif/rejected [impl]"]
  net["Live network fetch"] -.-> q
  classDef plan fill:#eef,stroke:#88a;
  class net plan;
```

## 11. Data ownership / source of truth

One registry, one set of schemas, many readers. Runtime state lives in `.motif/` (gitignored);
durable knowledge lives in the versioned registry.

```mermaid
flowchart TB
  reg[("Registry + schemas\n(versioned, source of truth) [impl]")]
  motifdir[(".motif/ runtime state\n(gitignored) [impl/exp]")]
  reg --> CLI["motif CLI"]
  reg --> Studio["Studio"]
  reg --> Atlas["Atlas"]
  reg --> MCP["MCP server"]
  CLI --> motifdir
  Studio --> motifdir
  MCP --> motifdir
  motifdir --> runs["runs / findings / concepts / previews"]
  motifdir --> dec["decisions / evidence / baselines"]
  motifdir --> pol["policies / twin / project / rollback"]
```

**Ownership rules.** The registry is the single durable source of truth; every surface reads
it through library functions, never a private copy. Per-project, per-run artefacts are owned
by `.motif/` and are reproducible from the registry plus the recorded run. Nothing in
`.motif/` is authoritative knowledge, it is evidence and state.

---

## 12. Status summary

| Layer / surface | Status |
|---|---|
| Product / Design / Interaction reasoning | implemented |
| Implementation: compile plan | implemented; apply/pr partial; preview experimental |
| Runtime: inspect / detect / worktree / run records | implemented; live process start experimental |
| Visual Twin: manifest + static fingerprints | implemented; screenshots / a11y tree / traces experimental |
| Assurance: interface + static layers | implemented; runtime (Playwright/axe) experimental |
| Governance: findings, policy, memory, decisions | implemented |
| Surfaces: Atlas, MCP, Guardian, design-system extract | implemented; Studio viewer implemented, interactive apply experimental |

See the per-surface guides under `docs/` and the
[gap analysis](../reviews/motif-v3-gap-analysis.md) for the authoritative status table.
