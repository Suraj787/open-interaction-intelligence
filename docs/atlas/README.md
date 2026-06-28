# Motif Atlas

A static, browsable catalogue of the registry: sources, components, patterns, effects and
recipes with filters. Status mirrors
[`docs/reviews/motif-v3-gap-analysis.md`](../reviews/motif-v3-gap-analysis.md) (§11:
**implemented**, `motif atlas build` generates a static site from the registry).

## What it does

- Generates source, component and pattern pages plus a filters dataset from the registry.
- Fully **offline and deterministic**, the same registry produces the same site.
- Reads the one shared source of truth via library functions (no private copy).

## Commands

```bash
motif atlas build              # generate the static catalogue site from the registry
motif atlas build --out ./site # choose an output directory
motif atlas serve              # preview the generated site locally (offline)
```

Aliases: `ii atlas`, `oii atlas`.

## Honest status

| Capability | Status |
|---|---|
| Static site from registry (sources / components / patterns) | implemented |
| Filters data | implemented |
| Live/remote data | not applicable, Atlas is intentionally static and offline |

## Output

A static site (HTML + a filters JSON dataset) under the chosen output directory. Because it
is derived purely from the versioned registry, it is reproducible and needs no runtime.

## Atlas vs Studio

- **Atlas** = the durable *knowledge* catalogue (registry). Stable, shareable, versioned.
- **Studio** = the *project* viewer over `.motif/` runtime state (findings, runs, concepts).

## See also

- [`docs/studio/README.md`](../studio/README.md)
- [`docs/mcp/README.md`](../mcp/README.md), the same data over MCP
- [`docs/architecture/motif-v3-live-architecture.md`](../architecture/motif-v3-live-architecture.md) §11
