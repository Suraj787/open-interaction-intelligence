# InterfaceBench

InterfaceBench measures whether an interface-building agent produces work that
**survives production**, not whether its first screenshot looks impressive.

Most UI benchmarks reward the opening frame: a striking hero, a bold gradient, a
clever animation. Those signals collapse the moment a real product applies real
pressure, new requirements, accessibility law, large datasets, brand changes,
ten rounds of edits. InterfaceBench is built to apply that pressure on purpose and
score what is left standing.

## What it measures, the 15 capabilities

Each capability is scored from automated checks where possible and a human rubric
where judgement is required (see `rubric.md`).

1. **Product understanding**, the interface reflects who the users are, the domain,
   and the primary task; it is not a generic template wearing the product's name.
2. **Structural concept diversity**, solutions differ in *structure* (layout,
   information model, interaction), not just colour and font; the agent does not
   reach for one default shape every time.
3. **Avoiding generic AI aesthetics**, no tell-tale defaults (purple gradient hero,
   glass cards everywhere, decorative blur, the same SaaS landing page) substituting
   for design thinking.
4. **Preserving product identity**, changes keep the product recognisably itself;
   redesigns evolve identity rather than erasing it.
5. **Required-state completeness**, every interactive surface ships its full state
   set: empty, loading, partial, error, success, disabled, selected, zero-results,
   permission-denied, not just the happy path.
6. **Keyboard / assistive-technology support**, full keyboard operability, visible
   focus, correct roles/labels, `aria-live` for async status, focus management in
   overlays.
7. **200% zoom**, layouts remain usable and unbroken at 200% browser zoom and
   reflow without horizontal scrolling traps.
8. **Reduced motion**, `prefers-reduced-motion` is honoured with meaningful static
   or instant fallbacks; motion is never forced on the user.
9. **Performance budgets**, explicit, respected budgets for bundle size, initial
   render, interaction latency and continuous rendering cost.
10. **Framework adaptation**, techniques are implemented in the project's actual
    framework; no foreign runtimes pulled in for a single effect.
11. **Dependency discipline**, dependencies are justified, minimal, licence-clean and
    removable; effects can be reproduced natively rather than vendored blindly.
12. **Decision explanation**, the agent can say *why* each significant choice was
    made, and what it rejected and why.
13. **Provenance**, sources studied are recorded; copied vs. reference-only vs.
    reimplemented is tracked, with licence status.
14. **Effect rejection**, the agent declines decorative or showcase effects that do
    not serve the product, the context, or the device.
15. **Coherence after repeated modifications**, after many rounds of edits the
    interface stays internally consistent, with bounded interface debt and no drift
    into a patchwork of conflicting patterns.

## How scoring works

InterfaceBench combines two layers:

- **Automated checks** (`kind: automated`), machine-verifiable signals: presence of
  required states, `prefers-reduced-motion` handling, focus management, virtualisation
  for large lists, dependency/licence findings, absence of forbidden patterns. These
  run against the agent's output and the fixtures, and gate the obvious failures.
- **Human rubric** (`kind: human-judgement`), a reviewer scores each capability 0-3
  using `rubric.md`. This captures the things automation cannot: whether the product
  was actually understood, whether a redesign preserved identity, whether a rejection
  was correct, whether the system stayed coherent.

A run's score is the per-capability rubric total, **gated** by the automated checks: an
output that fails a hard automated gate (e.g. defeats reduced motion, bundles
unknown-licence code, ships no error state) cannot score well on the related
capability regardless of visual polish. First-screenshot quality contributes nothing
on its own, it only counts when it survives the pressure in `longitudinal-scenario.md`.

## Files

- `README.md`, this file: what InterfaceBench measures and how it scores.
- `longitudinal-scenario.md`, the 10-round production-survival scenario.
- `rubric.md`, the 0-3 human-review rubric, one scored block per capability.
- `cases/*.json`, machine-readable bench cases conforming to
  `../schemas/evaluation.schema.json`, covering the longitudinal rounds plus
  state-completeness, originality and drift.
