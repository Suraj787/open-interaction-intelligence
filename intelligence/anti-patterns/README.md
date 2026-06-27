# Anti-Patterns

These are the failure modes Motif actively guards against. Each entry states
**why it harms** and the **better alternative**. When a proposed effect matches
an anti-pattern, Motif rejects or downgrades it regardless of how impressive it looks.

> Most anti-patterns share a root cause: an effect was chosen for its own sake,
> not to solve a stated interaction objective.

---

### 1. Decoration-only animation
- **Why it harms:** Adds cognitive load, CPU, and maintenance with zero task benefit. The first thing to cut.
- **Better:** Tie every animation to a LEVEL 5 objective. If you can't name one, remove it.

### 2. Excessive entrance animation
- **Why it harms:** Delays content the user came for; punishing on repeat visits in apps.
- **Better:** Reserve entrances for first view; keep them short (<300ms); show content fast, animate subtly.

### 3. Scroll hijacking
- **Why it harms:** Steals control of scroll, breaks expectations, causes motion sickness, hurts accessibility.
- **Better:** Let native scroll work; use scroll-*linked* reveals that respect user pace, or explicit step controls.

### 4. Forced custom cursor
- **Why it harms:** Breaks affordance, hurts precision and accessibility, often lags.
- **Better:** Keep the native cursor; express brand elsewhere. If used, make it optional and never on app/work surfaces.

### 5. Hidden essential controls
- **Why it harms:** Clever motion that hides nav/actions makes core tasks undiscoverable.
- **Better:** Keep primary controls visible and stable; use progressive disclosure only for secondary actions.

### 6. Long success animation
- **Why it harms:** Blocks the next action; tedious after the first time.
- **Better:** Brief, clear acknowledgement (<800ms); let users proceed immediately.

### 7. Confetti for frequent actions
- **Why it harms:** Celebration loses meaning and becomes annoying when fired on routine tasks.
- **Better:** Reserve celebration for rare, high-stakes milestones; use quiet confirmation for routine success.

### 8. Layout-jank animation
- **Why it harms:** Animating layout properties (top/left/width/height) causes reflow, stutter, and content shift.
- **Better:** Animate transform/opacity; reserve space ahead of load; use FLIP for position changes.

### 9. Infinite motion in work areas
- **Why it harms:** Continuous animation in dashboards/editors distracts, drains battery, and never resolves.
- **Better:** Use one-time transitions; animate only on meaningful change; keep work surfaces still.

### 10. Stacked glow effects
- **Why it harms:** Multiple competing glows/spotlights create visual noise and reduce contrast.
- **Better:** At most one focal glow per viewport; rely on layout and contrast for hierarchy.

### 11. Excessive glassmorphism
- **Why it harms:** backdrop-filter is expensive; layered translucency wrecks contrast and readability.
- **Better:** Use sparingly on a single layer; verify contrast; provide a solid fallback on low-power devices.

### 12. Unnecessary 3D
- **Why it harms:** Heavy payload and GPU cost for marginal benefit; excludes low-power devices.
- **Better:** Use 2D/CSS unless 3D is core to the message (immersive/product showcase) with fallbacks.

### 13. Fake loading
- **Why it harms:** Indeterminate bars or artificial delays that misrepresent progress erode trust.
- **Better:** Show real, determinate progress where measurable; skeletons + optimistic UI otherwise; never invent progress.

### 14. Motion-only status
- **Why it harms:** Users who can't perceive motion (reduced-motion, low vision) miss the state entirely.
- **Better:** Always pair motion with text, colour, and icon. Motion is an enhancement, never the sole channel.

### 15. No reduced-motion support
- **Why it harms:** Ignores `prefers-reduced-motion`; causes discomfort and excludes users, a hard accessibility failure.
- **Better:** Provide a reduced-motion variant for every animation (fade/instant); treat it as mandatory, not optional.

### 16. Gratuitous dependency installation
- **Why it harms:** Pulling a heavy animation library for one effect bloats the bundle, adds licence/supply-chain risk and maintenance burden.
- **Better:** Implement with CSS/native/WAAPI or an existing project dependency first; add a library only when the objective genuinely requires it (see `../selection-policies/`).

---

## How Motif uses this list

During selection, every candidate effect is checked against these anti-patterns.
A match triggers either a **penalty** (see the penalty model in
`../selection-policies/`) or an outright **rejection** for the hard failures
(missing reduced-motion, motion-only status, scroll hijacking in non-narrative
contexts, fake loading, hidden essential controls). The better alternative is
always offered in the recipe.
