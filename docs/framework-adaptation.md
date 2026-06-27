# Framework Adaptation

Motif never copies an effect across frameworks. It moves an *idea* through four stages so
the same interaction can be implemented correctly in browser-native code, React, Vue,
Frappe-Vue or another stack — using the **least complex** mechanism that works.

## The adaptation model

```
interaction concept
   → framework-neutral algorithm
      → framework adapter
         → project-specific implementation
```

1. **Interaction concept** — what the user must understand, feel or accomplish, drawn
   from the pattern (`registry/patterns/`). No framework, no library yet.
2. **Framework-neutral algorithm** — the steps in plain terms: triggers, states,
   transitions, cleanup, reduced-motion path. This is the `algorithm` field of a recipe.
3. **Framework adapter** — how that algorithm binds to a framework's lifecycle and
   reactivity (see the adapter contract below). Adapters live in `adapters/`
   (`browser-native`, `react`, `vue`, `frappe-vue`).
4. **Project-specific implementation** — the adapter applied within the target repo's
   conventions, design system and existing dependencies.

## Implementation hierarchy (preferred order)

Always choose the **highest** option that fully serves the objective. Going lower must be
justified by a real need the higher options cannot meet.

1. **Browser-native CSS** (transitions, animations, `:hover`/`:focus-visible`)
2. **Native CSS transitions / state-driven CSS**
3. **An existing project dependency** (already installed; no new weight)
4. **Web Animations API (WAAPI)**
5. **View Transitions API**
6. **A lightweight motion dependency** (only if 1–5 cannot serve the objective)
7. **GSAP** (when complex orchestration genuinely requires it)
8. **Canvas** (when DOM cannot express the visual)
9. **WebGL** (last resort)

Corollaries:

- **No automatic new dependency.** Prefer: dependency-free → existing project dependency
  → original internal recipe → approved lightweight dependency → heavier dependency only
  with clear justification (licence + cost review).
- **Never install React into a Vue/Svelte/Angular project for an effect** — or any
  framework to obtain an effect for another. A Vue project gets a `vue` / `frappe-vue` /
  `browser-native` recipe.
- **Never use WebGL when something simpler suffices.** Never run continuous decorative
  motion behind dense work UIs.

## Adapter contract

Every framework adapter must document how it handles each of the following. A recipe that
omits any of these is incomplete.

| Concern | What the adapter must specify |
|---------|-------------------------------|
| **Lifecycle** | Where the effect initialises and tears down in the framework's lifecycle (mount/update/unmount, `onMounted`/`onUnmounted`, effect hooks). |
| **Cleanup** | Observers, timers, animations and listeners are disconnected/cancelled on unmount — no leaks. |
| **SSR** | Behaviour when rendered on the server: no DOM/`window` access during SSR; safe initial markup. |
| **Hydration** | The effect attaches without mismatch; initial state matches server markup; motion does not run before hydration. |
| **Keyboard** | Fully operable by keyboard; focus is never removed; essential actions are never hover-only. |
| **Pointer / coarse-pointer** | Works with mouse, touch and coarse pointers; hit areas suit touch; no hover-only affordances on touch. |
| **Responsive** | Behaves correctly across breakpoints and input modes; degrades sensibly on small screens. |
| **Reduced motion** | A real non-motion path under `prefers-reduced-motion`; status never conveyed by motion alone. |
| **Testing** | How the adapter is validated (lifecycle/cleanup, reduced-motion, keyboard, hydration). |

## Vue and Frappe-Vue notes

Vue and Frappe-Vue are first-class targets, not afterthoughts.

- Use `<script setup>` + Composition API; initialise in `onMounted`, clean up in
  `onUnmounted`.
- Prefer Vue's built-in `<Transition>`/`<TransitionGroup>` and CSS before reaching for a
  motion library (hierarchy step 1–2).
- For **Frappe-Vue**, respect the existing Frappe UI design system and conventions; do not
  introduce a parallel styling system or a second animation engine for one effect.
- Guard all DOM/`window` access for SSR-capable setups and ensure hydration-safe initial
  state.

## Worked flow

1. Read the pattern → write/confirm the framework-neutral `algorithm`.
2. Pick the highest viable hierarchy step.
3. Select the adapter for the target framework; fill every adapter-contract concern.
4. Implement in the project's conventions; preserve the design system.
5. Validate accessibility, performance, responsiveness and reduced motion.
6. Record the recipe (`recipe-authoring.md`) and provenance.

See [recipe-authoring.md](recipe-authoring.md) and
[evaluation-methodology.md](evaluation-methodology.md).
