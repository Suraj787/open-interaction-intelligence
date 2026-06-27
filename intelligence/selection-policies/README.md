# Selection Policies — The Transparent Ranking Model

This is how Motif turns a context (product type, page, intent, objective) into a
single defensible choice. The model is **transparent**: every recommendation can
be explained as priorities scored, penalties subtracted, and an implementation
order followed.

> One sentence: **maximise the priorities, subtract the penalties, then build
> with the cheapest tool that satisfies the objective.**

---

## Priorities (in strict order)

Higher items win ties. A choice that improves a lower priority must never
sacrifice a higher one.

1. **Usability** — does it help the user do the task? Speed, clarity, no friction.
2. **Comprehension** — does it make the interface easier to understand (hierarchy, structure, meaning)?
3. **Feedback** — does it confirm the system received and acted on input?
4. **Continuity** — does it keep the user oriented across changes of state/view?
5. **Accessibility** — keyboard, screen reader, contrast, and `prefers-reduced-motion`. (A hard gate, see below.)
6. **Performance** — frame rate, payload, battery, main-thread cost.
7. **Maintainability** — can the team keep it working without specialist knowledge?
8. **Product identity** — does it express the brand appropriately for the context?
9. **Novelty** — is it fresh/memorable? Lowest priority; never traded against the above.

**Accessibility is also a gate, not just a priority.** A candidate that lacks a
reduced-motion fallback, relies on motion-only status, or breaks keyboard access
is **rejected** before scoring — it cannot be bought back by identity or novelty.

---

## Penalties (subtracted from any candidate)

Each applicable penalty lowers a candidate's score; severe ones disqualify it.

| Penalty | What triggers it | Severity |
|---|---|---|
| **Distraction** | Pulls attention from the task; competes with primary content | High |
| **Dependency weight** | Adds significant bundle size for the effect | Medium–High |
| **Maintenance complexity** | Bespoke/fragile code, hard to debug or hand over | Medium |
| **Mobile incompatibility** | Pointer-only, heavy, or breaks on touch/small screens | High |
| **Missing reduced-motion** | No `prefers-reduced-motion` fallback | Disqualifying |
| **Licence uncertainty** | Unclear/restrictive licence on a dependency or asset | High |
| **Continuous rendering** | Animates forever (CPU/GPU/battery, never resolves) | High |
| **Framework mismatch** | Fights the project's framework (e.g. non-Vue lib in a Vue/Frappe-Vue app) | Medium–High |
| **Source risk** | Unvetted/copy-pasted code, supply-chain or provenance concerns | High |

A candidate matching an `../anti-patterns/` entry inherits that pattern's penalty
or rejection.

---

## Preferred implementation order

When two candidates satisfy the objective, pick the one **higher on this ladder**.
Descend only when the objective genuinely cannot be met above.

1. **Browser-native CSS** — transitions, transforms, animations, `prefers-reduced-motion`.
2. **Native framework transitions** — Vue `<Transition>` / `<TransitionGroup>`, Frappe-Vue equivalents.
3. **Existing project dependency** — reuse what's already installed before adding anything.
4. **WAAPI** — Web Animations API for JS-driven control without a library.
5. **View Transitions API** — for route / shared-element / layout continuity.
6. **Lightweight approved motion dependency** — small, Vue-friendly, well-licensed.
7. **GSAP** — only when complex sequencing/timeline control is genuinely required.
8. **Canvas** — custom 2D visuals/particles when DOM/CSS cannot.
9. **Three.js / WebGL / shaders** — last resort, for immersive/3D experiences with mandatory fallbacks.

> **Vue / Frappe-Vue first.** In Frappe-Vue projects, native `<Transition>` and
> existing Frappe UI motion are preferred over any external library. A non-Vue
> animation library incurs the framework-mismatch penalty.

---

## The scoring walk-through

For each candidate effect that implements the chosen pattern:

1. **Gate:** reject if it fails accessibility (reduced-motion, keyboard, motion-only status) or matches a disqualifying anti-pattern.
2. **Score priorities:** weight by the ordered list above, anchored to the product type's posture and the active quality profile (`../quality-profiles/`).
3. **Subtract penalties:** apply every penalty that fits.
4. **Break ties by implementation order:** prefer the higher rung of the ladder.
5. **Respect the profile budgets:** dependency budget, performance budget, `max_high_attention_effects_per_viewport`, continuous-motion policy.
6. **Emit a recipe:** chosen pattern + minimal effect + implementation rung + reduced-motion fallback + a one-line rationale referencing the objective.

The output is always explainable: *"For this objective, in this context, this
pattern wins; the cheapest acceptable effect is X, built with Y, with reduced-
motion fallback Z, because higher-ranked priorities were satisfied and no
disqualifying penalty applied."*

If nothing scores positively, the correct answer is **no animation** — a still,
fast, accessible interface beats a decorated one.
