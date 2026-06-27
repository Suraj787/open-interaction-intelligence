# Motif Architecture

Motif is an **intelligence and governance system** for UI
interactions, motion and effects, not an animation bundle. Its job is to help an AI
coding agent decide what a user needs to *understand, feel or accomplish*, then select
and implement the **least complex interaction** that achieves it, safely and with full
provenance.

This document describes the layers, how they fit together, and the secure ingestion
pipeline that brings any external material under governance.

## Design invariants

These hold across every layer and override convenience:

- **Intelligence over inventory.** Reason from product context down to implementation.
  Search for a **PATTERN before an EFFECT**.
- **Websites vs web applications are distinguished** at every decision. A marketing
  website optimises persuasion; a web application optimises task completion and repeated
  use. The same effect is rarely right for both.
- **Vue and Frappe-Vue are first-class** adaptation targets, alongside browser-native
  and React. Never install one framework to obtain an effect for another.
- **Offline approved registry is the default runtime mode.** The internet is reached
  only through an explicit `source refresh` / new-source workflow.
- **Untrusted by default.** All retrieved material is quarantined and **never executed
  during ingestion**.
- **Licence gate.** Unknown licence ⇒ `reference-only`, never `bundled`.
- **Accessibility and reduced motion are mandatory.** Performance budgets are explicit.
  Ranking is transparent.

## Layer overview

```mermaid
flowchart TB
    subgraph Skills["Agent Skills (entry point)"]
        ORCH["web-experience-orchestrator\n(SKILL.md, 16-step workflow)"]
        SPEC["specialist skills:\nproduct-context-analysis, interaction-design\neffect-discovery, effect-selection, framework-adaptation\nmotion-accessibility, motion-performance\nimplementation-validation, source-governance"]
    end

    subgraph CLI["motif CLI  (python -m motif)"]
        C1["search, rank-sources, generate-index"]
        C2["component search/inspect/alternatives"]
        C3["component plan-install/install/rollback"]
        C4["source discover/retrieve/scan/approve/reject"]
        C5["validate, doctor"]
    end

    subgraph Intel["Intelligence (intelligence/)"]
        I1["product-types, page-types, user-intents"]
        I2["interaction-problems, effect-taxonomy"]
        I3["selection-policies, anti-patterns, quality-profiles"]
    end

    subgraph Reg["Approved Registry (registry/)"]
        R1["sources, components, effects"]
        R2["patterns, recipes"]
        R3["licenses, dependencies"]
    end

    subgraph Adapt["Adapters (adapters/)"]
        A1["browser-native, react, vue, frappe-vue\nframework-neutral algorithm → adapter"]
    end

    subgraph Ingest["Ingestion + Connectors"]
        CN["connectors/ (generic-github + source-specific)"]
        QD[".motif/ quarantine → reviewed → approved/rejected"]
    end

    subgraph Scan["Scanners (scanners/) + Policies (security/)"]
        S1["source_scanner, dependency_scanner\nlicense_scanner, behaviour_scanner, secret_scanner"]
        P1["security/*.yml (domain, behaviour, network, licence)"]
    end

    ORCH --> SPEC
    SPEC --> CLI
    CLI --> Intel
    CLI --> Reg
    CLI --> Adapt
    CLI --> Ingest
    Ingest --> Scan
    Scan --> Reg
    Adapt --> Reg
```

### Skills layer

`SKILL.md` is the root orchestrator: an 8-level reasoning model (development purpose →
product type → user intent → page/screen type → interaction objective → pattern → effect
→ implementation) and a 16-step workflow. Specialist skills in `skills/` are loaded
selectively as the workflow demands. Skills hold judgement; the CLI holds enforcement.

### motif CLI layer

`python -m motif` is the single tool surface. It is **dependency-free core** (Python
standard library only) so `make check` runs anywhere; optional tools such as
`jsonschema` are used if present but never required. The CLI enforces the
offline-approved-registry default, it is preferred over ad-hoc internet retrieval.

### Intelligence layer

`intelligence/` holds the machine-readable knowledge that drives reasoning *before* any
effect is considered: product/page/user taxonomies, interaction problems, the effect
taxonomy, selection policies, anti-patterns and quality profiles.

### Registry layer

`registry/` is the committed, offline-by-default catalogue: `sources`, `components`,
`effects`, `patterns`, `recipes`, plus `licenses` and `dependencies`. Every record
validates against a schema in `schemas/`. This is what normal usage reads.

### Adapters layer

`adapters/` turns a framework-neutral algorithm into a project-specific implementation
for `browser-native`, `react`, `vue` and `frappe-vue`. See
[framework-adaptation.md](framework-adaptation.md).

### Connectors + ingestion layer

`connectors/` (a strict `generic-github` connector plus justified source-specific
connectors) retrieve **only** from approved official locations into quarantine. A
connector may read public metadata and collect licence/attribution; it must **not**
execute code, run install scripts, modify a target project, follow unknown domains,
access secrets or open binaries. Quarantine state lives under `.motif/`.

### Scanners + policies layer

`scanners/` (`source_scanner`, `dependency_scanner`, `license_scanner`,
`behaviour_scanner`, `secret_scanner`) statically analyse quarantined material against the
policies in `security/*.yml`. Nothing is executed. See [threat-model.md](threat-model.md).

## Ingestion pipeline

Every piece of external material follows the same one-way pipeline. Internet access only
happens here, via an explicit source-refresh, never during normal registry use.

```mermaid
flowchart LR
    D["discover"] --> V["verify official source"]
    V --> R["retrieve into\n.motif/quarantine/"]
    R --> P["pin version + SHA-256 checksum"]
    P --> L["identify licence"]
    L --> SS["static security analysis"]
    SS --> DI["dependency inspection"]
    DI --> BC["behaviour classification"]
    BC --> AP["accessibility + performance review"]
    AP --> DEC{"decision"}
    DEC -->|approve| OK["approved/ + registry record"]
    DEC -->|adapt| CR["clean-room adapt\n→ original recipe"]
    DEC -->|reference| REF["reference-only record"]
    DEC -->|reject| REJ["rejected/"]
    OK --> CI["controlled installation\n(diff + rollback + provenance manifest)"]
    CR --> CI
```

Operating modes (the connector layer supports three; the runtime default is the first):

1. **Offline approved registry** *(default)*, read committed registry, no network.
2. **Catalogue-only**, metadata and references only, no source retrieval.
3. **Review**, retrieve untrusted text into disposable quarantine for static review; do
   not execute.
4. **Approved installation**, only approved entries are applied to a target project via a
   controlled patch with diff, rollback snapshot and a provenance manifest.

### Quarantine state machine

```
.motif/quarantine/  → material as retrieved, untrusted, never executed
        │ static scan + licence + dependency + behaviour review
        ▼
.motif/reviewed/    → scanned, findings recorded
        │ decision
        ├──► .motif/approved/   (redistributable, licence-clear, scans clean)
        └──► .motif/rejected/   (unsafe, licence-incompatible, or unverifiable)
```

A clean-room adaptation produces an **original** recipe that retains no source code; the
quarantined original is not redistributed.

## Trust tiers

Sources carry a tier 1-5 (`source.schema.json`). Lower trust requires stronger review.

| Tier | Meaning | Default disposition |
|-----:|---------|---------------------|
| 1 | Official browser/framework documentation | Highest confidence |
| 2 | Established open-source project | Normal review |
| 3 | Maintained component library, clear ownership | Normal review |
| 4 | Community contribution | Stronger review |
| 5 | Unknown or unverifiable | **reference-only or rejected** |

## Status and scope

Motif v0.1.0 ships a **working secure pipeline with representative, high-confidence
records** rather than fabricated breadth. See `PHASE_STATUS.md` for what is complete vs
representative, and [release-process.md](release-process.md) for release discipline.
