# Workflow: Build a New Website

For **websites** (marketing, narrative, persuasion) — distinct from web applications.
Motion may be expressive here, but it still earns its place: search a pattern before an
effect, and keep a reduced-motion path.

## Preconditions

- Target repo inspected (framework, design system, existing motion conventions).
- Motif runs in the default **offline approved registry** mode (no network needed).

## Steps

1. **Frame the purpose.** Confirm development purpose = *new website* and the product type
   (corporate, SaaS marketing, product-launch, e-commerce, documentation, portfolio).
   Load `skills/product-context-analysis`.
2. **Map screens.** List page/screen types (hero, features, pricing, story, footer CTA).
3. **Per screen, state the objective** — what the visitor must understand, feel or
   accomplish. Load `skills/interaction-design`.
4. **Search patterns first:**
   `python -m motif search "<problem>"` then inspect candidate patterns. Only then look at
   effects via `skills/effect-discovery`.
5. **Rank transparently.** Load `skills/effect-selection`; produce multiple candidates and
   score them (complexity, performance, accessibility, fit). Pick the **simplest fully
   effective** option.
6. **Check marketing suitability.** Prefer effects with `marketing_suitability:
   recommended`. Avoid combining multiple high-attention effects without justification.
7. **Implement in the target framework** (`skills/framework-adaptation`). Follow the
   implementation hierarchy (browser-native CSS first). Do not introduce a new framework.
8. **Accessibility gate** (`skills/motion-accessibility`): keyboard, focus, semantics,
   `prefers-reduced-motion` path. Never make essential actions hover-only.
9. **Performance gate** (`skills/motion-performance`): animate transform/opacity, respect
   budgets, no jank.
10. **Responsiveness gate:** breakpoints and input modes (touch/coarse pointer).
11. **Record the decision** (`schemas/decision.schema.json`) and provenance; install any
    approved component via `python -m motif component install` (diff + rollback + manifest).
12. **Validate the experience** — see [validate-experience.md](validate-experience.md).

## Done when

Each screen has a justified pattern+effect, a reduced-motion path, passing
accessibility/performance/responsiveness checks, and a written decision + provenance log.
