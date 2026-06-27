# Interaction Specification Graph

A machine-checkable model of *how an interface is meant to behave*, expressed as
typed **nodes** and typed **edges**. This example models an **enterprise project
dashboard**. The graph is the substrate the Governance engine queries to find
where the realised UI diverges from the intended interaction model.

## Layout

```
interaction-graph/
  nodes/   one JSON file per node, filename = <id>.json   (graph-node.schema.json)
  edges/   one JSON file per edge, edge-NNN.json          (graph-edge.schema.json)
  README.md
```

This example contains **31 nodes** and **40 edges**.

## Node types

`user`, `role`, `task`, `workflow`, `screen`, `information-object`, `action`,
`state`, `pattern`, `effect`, `recipe`, `component`, `constraint`, `evidence`,
`test`, `decision`. Each node is `{ id, type, label, attributes }`.

## Edge relations

`performs`, `belongs-to`, `uses`, `shows`, `has-state`, `solves`, `implements`,
`requires`, `validated-by`, `evidenced-by`, `conflicts-with`, `depends-on`,
`navigates-to`, `produces`, `governed-by`. Each edge is `{ from, to, relation }`.

## What this graph says

- A **Portfolio Manager** `performs` three tasks and `belongs-to` the Project
  Administrator role.
- The **Weekly status review** workflow `uses` those tasks.
- Tasks `use` screens; screens `show` information objects and components, and
  declare their `has-state` loading / empty / error states.
- The **dense data table** pattern `solves` the health-review task, is
  `evidenced-by` a usability study, and is `implemented` by `ProjectTable`,
  which `uses` the status-pill recipe and is `governed-by` the token constraint.
- Effects are `governed-by` the reduced-motion constraint — except a decorative
  KPI count-up that `conflicts-with` it.

## Deliberate gaps (so queries return real findings)

The graph intentionally encodes six divergences that the standard queries surface:

| Gap | Node / missing edge |
|-----|---------------------|
| Screen with no error recovery | `screen-task-board` has only a loading state |
| Task with no feedback | `task-reassign-overdue-work` has no `produces` edge |
| Component violating the genome | `component-kpi-card` `conflicts-with` `constraint-token-spacing` |
| Effect conflicting with reduced motion | `effect-kpi-count-up` `conflicts-with` `constraint-reduced-motion` |
| Workflow with no offline handling | `workflow-weekly-status-review` has no `requires` edge to `constraint-offline-capable` |
| State with no test | `state-loading` has no `validated-by` edge |

## Example queries

Each query is a traversal over the typed graph. Run with `ii graph query`.

1. **Screens lacking error recovery** — screens with no `has-state -> state-error`.
   → returns `screen-task-board`.
2. **Tasks lacking feedback** — task nodes with no outgoing `produces` edge to an
   effect/state. → returns `task-reassign-overdue-work`.
3. **Components violating the genome** — components with a `conflicts-with` edge to
   a `constraint`. → returns `component-kpi-card`.
4. **Effects conflicting with reduced motion** — `effect` nodes with
   `conflicts-with -> constraint-reduced-motion`. → returns `effect-kpi-count-up`.
5. **Workflows lacking offline handling** — workflows with no `requires` edge to
   `constraint-offline-capable`. → returns `workflow-weekly-status-review`.
6. **States lacking tests** — `state` nodes with no `validated-by` edge.
   → returns `state-loading`.

## CLI

```bash
# Build the in-memory graph from nodes/ and edges/ and write the compiled index
ii graph build governance/interaction-graph

# Validate every node/edge against the schemas and check referential integrity
# (no dangling refs, valid types/relations, id == filename)
ii graph validate governance/interaction-graph

# Run a named or ad-hoc query
ii graph query "screens lacking error recovery"
ii graph query --from screen --missing "has-state:state-error"

# Explain a finding: show the path, the rule it breaks, and the supporting evidence
ii graph explain screen-task-board --query "screens lacking error recovery"

# Render the graph (or a sub-graph) to SVG/DOT for review
ii graph render governance/interaction-graph --focus screen-dashboard-overview --out graph.svg
```

`build` compiles, `validate` enforces the schemas and integrity, `query` traverses,
`explain` justifies a single result with its evidence chain, and `render`
visualises. Findings here feed the Interface Debt Score (see `../debt/README.md`)
and drift detection (see `../drift/README.md`).
