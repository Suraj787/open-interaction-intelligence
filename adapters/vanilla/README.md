# Motif Adapter, Vanilla JS

How Motif recipes map onto a no-framework codebase: hand-written ES modules, custom
elements, and the DOM. Closely related to the browser-native baseline, but this
adapter covers the **JS architecture** patterns for shipping reusable recipes
without a framework runtime.

> Provenance: original (clean-room). No third-party source is copied.

## Idiomatic structure

Two equally idiomatic packagings:

1. **Factory function**, `initBlurReveal(root = document)` queries
   `[data-motif="blur-reveal"]`, wires each, and returns a `dispose()`.
2. **Custom element**, `class OiiReveal extends HTMLElement` with
   `connectedCallback`/`disconnectedCallback`. This gives you framework-grade
   lifecycle with zero dependencies and is the recommended path for reusable
   widgets.

```js
customElements.define('motif-reveal', class extends HTMLElement {
  connectedCallback() { /* observe */ }
  disconnectedCallback() { /* disconnect */ }
});
```

Keep motion in CSS (a stylesheet or the element's `<template>`/shadow styles).

## Lifecycle handling

- Custom elements: `connectedCallback` (enter DOM), `disconnectedCallback` (leave),
  `attributeChangedCallback` + `observedAttributes` (knob changes),
  `adoptedCallback` (moved between documents).
- Factory style: init on `DOMContentLoaded`/`defer`; re-run on dynamically inserted
  subtrees (keep `init` idempotent via a `data-motif-ready` guard).

## Cleanup

- Custom element: undo everything in `disconnectedCallback`, `observer.disconnect()`, `controller.abort()`, `cancelAnimationFrame`. Note it
  fires on every detach, so re-acquire in `connectedCallback`.
- Factory: return a `dispose()` that tears down all per-node state. Use a
  `WeakMap<Element, State>` so node state is GC'd with the node.

```js
const ac = new AbortController();
el.addEventListener('pointermove', onMove, { signal: ac.signal });
this._dispose = () => ac.abort();
```

## SSR

There's no framework SSR, but recipes must work with server-rendered HTML (e.g. a
PHP/Django/Frappe template). The markup is authored to be complete and readable
before scripts run; the script *enhances* it. Custom elements upgrade automatically
when defined, even if the element was in the initial HTML. Guard module top-level
code against non-browser evaluation if bundled for an SSR pipeline.

## Hydration

No hydration step, the script attaches to existing DOM. Prevent flashes by keying
the resting state on a class the script adds (`html.motif-js`) or by using a custom
element's `:defined` pseudo-class:

```css
motif-reveal:not(:defined) { opacity: 1; }   /* visible until upgraded */
```

## Keyboard behaviour

- Build on real focusable elements; for custom controls set `tabindex="0"`, a
  `role`, and handle Enter/Space/Escape/arrows yourself.
- Never trap or discard focus for animation. Style `:focus-visible`.
- For shadow DOM, use `delegatesFocus: true` on `attachShadow` when wrapping a
  single control.

## Pointer & coarse-pointer support

- Pointer Events unify mouse/touch/pen; set `touch-action` to avoid scroll
  conflicts.
- Gate hover effects behind `@media (hover: hover) and (pointer: fine)`; provide
  tap equivalents for `@media (pointer: coarse)` with >=44px targets.

## Responsive behaviour

CSS media/container queries first. If JS must branch, subscribe to
`matchMedia(...).addEventListener('change', …)` and remove it on dispose, avoid
`resize` polling.

## Reduced-motion strategy

CSS `@media (prefers-reduced-motion: reduce)` sets the static baseline. In JS,
read `matchMedia('(prefers-reduced-motion: reduce)').matches` and subscribe to its
`change` event so a mid-session flip is honoured; on reduce, skip transitions and
apply the end state immediately. Remove the listener on dispose.

## Testing

- **Vitest/Jest + jsdom** (or `@web/test-runner` in a real browser, ideal for
  custom elements) for behaviour/ARIA.
- Stub `IntersectionObserver`/`matchMedia` under jsdom.
- Assert `disconnectedCallback`/`dispose()` disconnects observers and aborts
  listeners.
- Playwright for reduced-motion / coarse-pointer E2E.

## Dependency trade-offs

Maximum portability, zero runtime weight, no build required (ship ES modules
directly). Cost: you hand-roll state, attribute reflection, and rendering. Custom
elements recover most ergonomics natively. Add a micro-library only if a recipe's
state truly warrants it, per the technique order.

## Normalised component contract knobs

| Knob                 | Vanilla surface                                         |
| -------------------- | ------------------------------------------------------- |
| class override       | author classes; reflected attributes                    |
| style override       | inline `style`; `--motif-*` custom properties             |
| design tokens        | read CSS variables from `:root`/ancestor                |
| intensity            | `intensity` attribute (reflected to property)           |
| duration             | `duration` attr / `--motif-duration`                      |
| delay                | `delay` attr / `--motif-delay`                            |
| easing               | `easing` attr / `--motif-easing`                          |
| disable-animation    | `data-motif-disabled` attribute                           |
| reduced-motion       | media query + `matchMedia` listener                     |
| responsive controls  | media/container queries on the knobs                    |
| accessible labels    | `aria-label`/`aria-live` on markup                      |
| event callbacks      | `dispatchEvent(new CustomEvent('motif:reveal'))`          |
