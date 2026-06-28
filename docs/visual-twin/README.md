# Visual Twin

A typed, source-derived model of an interface: routes, screens, component fingerprints, and
(when a runtime exists) screenshots, an accessibility tree and performance traces. Status
mirrors [`docs/reviews/motif-v3-gap-analysis.md`](../reviews/motif-v3-gap-analysis.md) (§7:
**partial**, manifest + routes + component fingerprints from source implemented;
screenshots / a11y-tree / traces experimental, require Playwright which is not installed).

## What is real today

- **`twin-manifest.json`** (schema `schemas/twin-manifest.schema.json`): project, generated
  time, `target_commit`, framework, routes, screens, components, viewport variants.
- **Routes + screens** mapped from the source tree by static analysis.
- **Component fingerprints** derived from source (no rendering).
- The manifest carries **`"rendered": false`** until a real runtime fills the pixel layer.

## What is experimental

- Screenshots / pixel layer
- Accessibility tree snapshot
- Performance traces

These need a browser runtime (Playwright). Without one, the twin is honest: `rendered` stays
`false` and no downstream step claims visual truth from it.

## Commands

```bash
motif twin build --target ./app          # static manifest: routes, screens, fingerprints
motif twin show --target ./app           # print the current twin manifest
motif twin build --render                # EXPERIMENTAL: screenshots + a11y tree (needs Playwright)
```

Aliases: `ii twin`, `oii twin`.

## Honest status

| Part | Status |
|---|---|
| Manifest + routes + screens | implemented |
| Component fingerprints (static) | implemented |
| Screenshots / a11y tree / traces | experimental |

## Output

`.motif/twin/<target_commit>/manifest.json` plus, if rendered, a `screens/` directory. The
twin is runtime state under `.motif/` (gitignored) and is reproducible from source + commit.

## See also

- [`docs/architecture/motif-v3-live-architecture.md`](../architecture/motif-v3-live-architecture.md) §5
- [`docs/assurance/README.md`](../assurance/README.md), visual comparison consumes the twin
