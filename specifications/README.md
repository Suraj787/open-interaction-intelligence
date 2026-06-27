# Interface Specification Language (ISL)

A small, strict, version-controlled specification that captures what an interface must
be, before any pixels exist. It is the contract the framework compiler reads.

An ISL document describes: product, user, task, information hierarchy, navigation,
interaction, accessibility, performance, identity (which Product Design Genome governs
it), required states, and constraints. It is intentionally simple; it is not a DSL.

- Schema: `schemas/interface-spec.schema.json`
- Examples (JSON): `specifications/*.json` (e.g. `project-dashboard.json`, `checkout-mobile.json`)
- Validation: `ii validate` checks every spec against the schema.

YAML is a convenient authoring format and is read with the dependency-free reader in
`motif/yaml_min.py`; the canonical stored form is JSON so the same validator and tooling
apply everywhere.

Example (YAML form):

```yaml
interface:
  id: project-dashboard
  product:
    type: enterprise-project-management
    profile: enterprise-strict
  user:
    role: delivery-manager
    expertise: advanced
  task:
    primary: identify-project-risk
    frequency: daily
    criticality: high
  information:
    density: high
    hierarchy: [critical-risk, delayed-milestone, team-capacity]
  interaction:
    navigation: master-detail
    feedback: inline
    motion: restrained
  accessibility:
    keyboard: required
    zoom: 200-percent
    reduced_motion: required
  performance:
    bundle_budget_kb: 20
  identity:
    genome: enterprise-pm-genome
  required_states: [loading, empty, error, stale, slow-network]
  constraints: ["no continuous decorative motion behind dense data"]
```

The compiler (`ii compile plan`) reads a spec plus the genome, graph, and grammars to
produce a native implementation plan. Compilation and `compile apply` beyond the existing
controlled installer are on the v0.3.0 roadmap.
