# Effect Taxonomy — EFFECT vs PATTERN vs RECIPE

Motif separates three things that are often confused. Getting the vocabulary right
is what lets us search **problems → patterns → effects** instead of reaching for
an animation bundle.

## Definitions

### EFFECT
A concrete visual/motion technique. The *how*. Examples: a blur-in text reveal,
a tilt-on-hover card, an aurora background, a count-up number.
- An effect is **implementation**. It has cost (dependency weight, CPU, a11y burden).
- An effect is **not a decision** — it's an option that may or may not serve a pattern.

### PATTERN
A reusable solution to an interaction **objective**. The *what and why*. Examples:
"shared-element transition for spatial continuity", "skeleton screen to reduce
perceived waiting", "inline validation to prevent errors".
- A pattern maps to a LEVEL 5 interaction problem.
- One pattern can be implemented by several effects of differing cost.

### RECIPE
A vetted, context-bound combination: **product type + page type + intent +
objective → chosen pattern → specific effect(s) + implementation order +
accessibility + reduced-motion fallback + performance budget.**
- A recipe is the deliverable Motif ultimately produces — a defensible, ready-to-build choice.
- Recipes are where Vue / Frappe-Vue specifics, dependency budgets, and profiles get applied.

> **Search direction:** Problem → Pattern → (cheapest) Effect → Recipe.
> Never Effect → "where can I use this?". The taxonomy below is the *menu of
> implementations*, deliberately placed last in the reasoning chain.

---

## Effect families

These are the implementation families Motif can draw from. For each, note the
**objective it usually serves** and its **main cost** — both feed selection
policy. Effects with no clear objective are decoration (see `../anti-patterns/`).

### Text & typography
- **Text reveal** (fade/slide/clip in) — serves *guide attention*, *hierarchy*. Low cost.
- **Kinetic typography** (animated, expressive type) — serves *emotional impact*. Website-leaning; readability risk.

### Numeric & surface treatments
- **Blur-in / focus-in** — *attract attention*, *hierarchy*. Low cost; watch text legibility.
- **Shimmer** — *reduce perceived waiting* (skeletons). Low cost.
- **Gradient animation** — *emotional impact*. Continuous-render risk.
- **Counter / odometer** — *attract attention* to a stat. Forbidden on financial/precise values.

### Backgrounds & ambient
- **Auroras / beams / grids / noise / particles** — *emotional impact*, *brand identity*. Continuous-render and battery cost; website/immersive only; never in dense work areas.

### Cards & surfaces
- **Tilt / parallax card** — *strengthen affordance*. Pointer-only; provide non-tilt fallback.
- **Magnetism** (cursor-attracted elements) — *affordance*, *delight*. Pointer-only; can hurt precision.
- **Spotlight / hover glow** — *attract attention*, *affordance*. Watch stacked-glow overload.
- **Animated borders** — *attract attention*. Continuous-render risk.
- **Glassmorphism** — *hierarchy/depth*. Contrast and performance (backdrop-filter) cost.

### Navigation & command
- **Nav/menu motion** — *spatial continuity*, *affordance*. Keep fast.
- **Command-palette motion** — *discoverability*, *feedback*. Must not delay input.

### View & layout transitions
- **Route transitions** — *spatial continuity*. Use native framework / View Transitions API first.
- **Shared-element transitions** — *spatial continuity*, *cause/effect*. High value in apps.
- **Layout / FLIP transitions** — *continuity* on reorder/resize. Low cost done right.

### Scroll
- **Scroll reveal** — *guide attention*, *hierarchy*. Use sparingly; never hide essential content.
- **Parallax** — *emotional impact*. Website-leaning; motion-sickness + perf risk.
- **Pinned / scroll-jacked sections** — *guide attention* (storytelling). High risk; see anti-patterns.
- **Scroll progress** — *reduce uncertainty*, *navigate*. Low cost.

### Pointer & cursor
- **Pointer-follow / custom cursor** — *delight*, *affordance*. High accessibility/usability risk; rarely justified.

### Loading & progress
- **Skeleton screens** — *reduce perceived waiting*. Preferred loader.
- **Spinners / progress bars** — *system feedback*. Honest, determinate where possible.

### Feedback
- **Save / success / validation / error feedback** — *system feedback*, *confirm completion*, *prevent errors*. Always pair motion with text + colour + icon.

### Manipulation
- **Drag-and-drop / reordering** — *cause/effect*, *continuity*, *affordance*. Needs keyboard alternative.

### Data & visualisation
- **Table / kanban / timeline motion** — *continuity*, *feedback*. Subtle only; protect density.
- **Chart motion** — *guide attention* to change. One-time, not continuous.

### Advanced rendering
- **SVG animation** — *cause/effect*, *brand*. Moderate cost.
- **Canvas** — *emotional impact*, custom viz. Continuous-render cost; manage lifecycle.
- **3D** — *emotional impact*. Heavy; immersive/website only.
- **WebGL / shaders** — *emotional impact*, signature experiences. Heaviest; last resort; mandatory fallbacks.

---

## Cost ladder (summary)

From cheapest/safest to most expensive/risky:

1. CSS transitions & transforms, skeletons, FLIP/layout, native framework transitions
2. WAAPI, View Transitions API, scroll progress, simple reveals
3. Approved lightweight motion dependency (e.g. small Vue-friendly libs)
4. GSAP (when genuinely justified)
5. SVG / Canvas
6. 3D / WebGL / shaders

Selection always starts at the top of this ladder and only descends when the
objective truly demands it. See `../selection-policies/` for the full ranking
and penalty model.
