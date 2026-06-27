# Motif Adapter, Browser-Native

This adapter is the **reference baseline** for Motif.
Every recipe is first expressed here using only platform features: HTML, CSS, and
vanilla DOM APIs. All other adapters are *translations* of this baseline into a
framework's idioms. If a behaviour cannot be expressed here, it does not belong in
the catalogue.

> Provenance: original (clean-room). No third-party source is copied.

## Why browser-native first

Per the Motif technique order, we always reach for the simplest accessible layer
before climbing:

```
CSS → native framework transitions → existing dependency → Web Animations API
   → View Transitions API → approved motion dep → GSAP → Canvas → WebGL
```

A browser-native recipe has zero install cost, no hydration mismatch, and survives
framework churn. It is the contract every other adapter must honour.

## Idiomatic structure

A recipe ships as up to three artifacts:

| File          | Role                                                        |
| ------------- | ----------------------------------------------------------- |
| `*.css`       | Declarative motion/state. The preferred home for animation. |
| `*.js`        | Progressive enhancement: observers, state machines, ARIA.   |
| `*.html`/docs | Minimal markup contract and usage.                          |

Markup is authored so that **the page is fully usable with CSS and JS disabled**.
JS only *enhances*, it never gates content visibility.

```html
<!-- Content is present and readable before any script runs -->
<section class="motif-reveal" data-motif="blur-reveal">
  <h2>Readable immediately</h2>
</section>
```

## Lifecycle handling

There is no framework lifecycle, so we bind to the document lifecycle directly:

- **Init:** run on `DOMContentLoaded` or defer the script (`<script defer>`); query
  target nodes and attach observers/listeners.
- **Update:** when nodes are added dynamically, re-run the initializer on the new
  subtree (expose an idempotent `init(root = document)`).
- **Teardown:** every initializer returns a `dispose()` that disconnects observers
  and removes listeners (see Cleanup).

## Cleanup

Native APIs leak if you forget them. Each recipe must:

- `observer.disconnect()` for `IntersectionObserver`/`ResizeObserver`/`MutationObserver`.
- Pair every `addEventListener` with `removeEventListener`, or use an
  `AbortController` and call `controller.abort()` on dispose.
- `cancelAnimationFrame` any pending RAF; `.cancel()` any `Animation` from WAAPI.

```js
const ac = new AbortController();
el.addEventListener('pointermove', onMove, { signal: ac.signal });
return () => ac.abort(); // one-shot teardown
```

## SSR

Browser-native recipes are SSR-trivial: the server emits plain HTML/CSS. CSS-only
recipes (e.g. scroll-driven animations) run with **no JavaScript at all**. For
JS-enhanced recipes, the markup is the server output and the script attaches on the
client. Guard every DOM/`window`/`matchMedia` access behind a `typeof window`
check if the script is ever evaluated server-side.

## Hydration

There is nothing to hydrate, the server HTML *is* the final DOM. To avoid a flash,
set the resting (pre-animation) visual state in CSS keyed off a class the script
adds (`.js` / `data-motif-ready`), so non-JS users see content and JS users get the
enhanced start state only once the script confirms support.

```css
/* Only hide/blur when JS has signalled it can animate */
html.motif-js .motif-reveal { opacity: 0; }
```

## Keyboard behaviour

- Never move or remove focus as a side-effect of animation.
- Interactive recipes use real focusable elements (`<button>`, `<a>`), full
  `:focus-visible` styling, and standard key handling (Enter/Space activate,
  Escape dismisses, arrow keys for composite widgets).
- Decorative motion is `aria-hidden` and not focusable.

## Pointer & coarse-pointer support

- Use **Pointer Events** (`pointerdown`/`pointermove`) to unify mouse/touch/pen.
- Gate hover-only effects behind `@media (hover: hover) and (pointer: fine)`.
- For `@media (pointer: coarse)`, enlarge targets to >=44px and replace hover
  affordances with tap/visible equivalents.

## Responsive behaviour

Drive thresholds from media/container queries rather than JS measurement where
possible. Use `clamp()`/`min()`/`max()` for fluid durations and distances, and
container queries (`@container`) so a recipe adapts to its slot, not just the
viewport.

## Reduced-motion strategy

The non-negotiable default. Author motion behind a "motion is okay" guard so the
**static state is the baseline**:

```css
@media (prefers-reduced-motion: reduce) {
  .motif-reveal { animation: none; opacity: 1; filter: none; transition: none; }
}
```

In JS, branch on `matchMedia('(prefers-reduced-motion: reduce)')` and **listen for
changes** so a mid-session preference flip is honoured. Reduced motion means the
end state is shown instantly, never a blank or stuck state.

## Testing

- **Unit:** initializer attaches expected attributes/classes; `dispose()` removes
  them and disconnects observers (spy on `disconnect`).
- **Integration:** jsdom lacks `IntersectionObserver`/`matchMedia`, provide stubs.
- **Visual/E2E:** Playwright with `prefers-reduced-motion` emulation, both
  `reduce` and `no-preference`, plus coarse-pointer emulation.

## Dependency trade-offs

Zero dependencies, zero bundle cost, maximum longevity. Cost: more verbose than a
framework's sugar, and you hand-roll the state plumbing other adapters get free.
This is the price of being the portable reference, accept it here so consumers can
choose lighter integration elsewhere.

## Normalised component contract knobs

Even without a component model, expose these via `data-*` attributes / CSS custom
properties so all adapters share one vocabulary:

| Knob                 | Browser-native surface                                  |
| -------------------- | ------------------------------------------------------- |
| class/style override | author classes; `--motif-*` custom properties             |
| design tokens        | read from CSS variables on `:root` / ancestor           |
| intensity            | `--motif-intensity` (e.g. blur radius / distance scalar)  |
| duration             | `--motif-duration`                                        |
| delay                | `--motif-delay`                                            |
| easing               | `--motif-easing`                                           |
| disable-animation    | `data-motif-disabled` / omit the script                   |
| reduced-motion       | media query + JS `matchMedia` listener                  |
| responsive controls  | media / container queries on the knobs above            |
| accessible labels    | `aria-label`/`aria-live` on the markup                  |
| event callbacks      | `CustomEvent` dispatch (`motif:reveal`, etc.)             |
