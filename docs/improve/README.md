# `motif improve`, improve an existing interface

Inspect an existing interface, model it, discover problems into the unified Finding model,
generate concepts and a reversible plan. Status mirrors
[`docs/reviews/motif-v3-gap-analysis.md`](../reviews/motif-v3-gap-analysis.md) (§1B: **partial**, inspect→model→discover→findings→concepts→plan implemented; start-app + capture experimental).

## What it does

1. **Inspect** the target and detect framework (React/Vue/Svelte/Angular/Tailwind/vanilla).
2. **Model** routes, screens and component fingerprints (static; no runtime needed).
3. *(experimental)* **Start** the app and **capture** a live Visual Twin.
4. **Discover** problems → typed `finding` records with lifecycle + suppressions.
5. Generate **concepts** that address the findings.
6. Emit a reversible **compile plan**; *(experimental)* preview and apply.

## Commands

```bash
motif improve ./path/to/app                 # inspect → model → discover → findings → concepts → plan
motif improve . --focus accessibility       # bias discovery toward one concern
motif improve . --findings-only             # stop after writing findings
motif improve . --plan-only                 # produce the compile plan, no apply
motif improve . --start --capture           # EXPERIMENTAL: live start + Visual Twin capture
motif improve . --apply                      # EXPERIMENTAL: apply plan in an isolated worktree
```

Aliases: `ii improve`, `oii improve`.

## Honest status

| Step | Status |
|---|---|
| Inspect + framework detect | implemented |
| Model routes / components (static) | implemented |
| Discover → Findings (typed, lifecycle, suppressions) | implemented |
| Concept generation + compare | implemented |
| Compile **plan** | implemented |
| Start app + live capture | experimental (no browser runtime here) |
| Preview / apply / validate (rendered) | experimental / partial |

## Output

- `.motif/findings/*.json`, unified findings (see [`docs/architecture`](../architecture/motif-v3-live-architecture.md) §3)
- `.motif/concepts/*.json`, `.motif/previews/*`, `.motif/runs/<id>/`

## Safety

Discovery and modelling are read-only over your source. Live start is opt-in
(`--start`), runs the target in isolation, and is experimental. Apply is worktree-only with
rollback; `main` is never touched.

## See also

- [`docs/runtime/README.md`](../runtime/README.md), [`docs/assurance/README.md`](../assurance/README.md),
  [`docs/policies/README.md`](../policies/README.md)
