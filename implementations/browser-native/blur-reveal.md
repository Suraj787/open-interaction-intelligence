# Blur Reveal on Scroll, browser-native

Content gently rises and sharpens (blur → 0, `translateY` → 0, opacity → 1) as it
enters the viewport. Pure platform features: CSS scroll-driven animation as the
progressive-enhancement path, with an `IntersectionObserver` fallback.

Files: [`blur-reveal.css`](./blur-reveal.css), [`blur-reveal.js`](./blur-reveal.js).

## Markup contract

```html
<!-- Readable with no CSS and no JS. The attribute is the only requirement. -->
<section data-motif="blur-reveal">
  <h2>Heading</h2>
  <p>Body copy that reveals as you scroll.</p>
</section>

<link rel="stylesheet" href="./blur-reveal.css" />
<script type="module" src="./blur-reveal.js"></script>
```

The script adds the `motif-reveal` class and toggles `data-motif-reveal="shown"`; the
CSS does the rest. You can also `import { initBlurReveal } from './blur-reveal.js'`
and call it from a framework lifecycle hook to control teardown via the returned
`dispose()`.

## Algorithm

The script picks the cheapest accessible technique available, in this order:

1. **Reduced motion requested** → add `motif-js`, immediately mark every element
   `shown`, attach **no** observers. Content appears instantly, no blur, no travel.
2. **CSS scroll-driven animations supported** (`@supports (animation-timeline:
   view())`) → add `motif-js motif-css-scroll` and let **CSS** drive the reveal from
   scroll position (`animation-timeline: view()`, `animation-range: entry 0% cover
   35%`). No JS observers run, zero runtime cost. Elements are still marked `shown`
   and the `motif:reveal` event still fires so consumers have a consistent contract.
3. **`IntersectionObserver` fallback** → add `motif-js` (which arms the resting
   blurred state in CSS), observe each element, and on first intersection toggle
   `data-motif-reveal="shown"` then `unobserve` it (one-shot). A `transition` on
   `opacity`/`transform`/`filter` animates the change. `rootMargin: 0 0 -10% 0` and
   `threshold: 0.15` trigger slightly before the element is fully on screen.
4. **No `IntersectionObserver`** (very old engines) → reveal everything immediately.

The resting (hidden/blurred) state is gated behind the `motif-js` class that the
script adds, so if the script fails to load the content is never left invisible.

A `matchMedia('(prefers-reduced-motion: reduce)')` `change` listener reveals all
elements and disconnects the observer if the user flips the preference mid-session.

## Why these CSS properties

`opacity`, `transform: translateY`, and `filter: blur` are all GPU-cheap and avoid
layout. The reveal never changes element box size, so surrounding content does not
reflow. `will-change` is set on the resting state and dropped under reduced motion.

## Accessibility

- **Content-first:** the markup is complete and readable with no CSS and no JS. JS
  only enhances; it never gates visibility.
- **No focus interference:** the recipe is purely visual and does not move, trap, or
  remove keyboard focus. Focusable children remain reachable in source order
  throughout (they are visible to AT even while visually transitioning).
- **Not announced:** the reveal is decorative; it adds no ARIA noise.
- **Consistent end state:** every path guarantees the element ends fully visible,
  unblurred, untranslated.

## Reduced-motion behaviour

`@media (prefers-reduced-motion: reduce)` (last rule in the stylesheet, with
`!important`) forces `opacity: 1`, no `transform`, no `filter`, and disables both
`transition` and `animation` for all three paths. The JS path additionally skips all
observers and reveals instantly. Net effect: content simply appears, exactly as a
static page would, no blur, no movement.

## Browser support

- **IntersectionObserver fallback:** all current evergreen browsers and Safari
  12.1+. This is the baseline experience.
- **CSS scroll-driven path** (`animation-timeline: view()`): Chrome/Edge 115+, and
  other Chromium browsers; progressively enhances where present. Browsers without it
  automatically use the observer path via the `@supports` gate and the runtime
  `CSS.supports` check.
- **`matchMedia` change listener:** uses the modern `addEventListener('change')`
  API with optional chaining so absence is harmless.
- Guarded against SSR/non-browser evaluation via `typeof window` checks.

## Contract knobs

Override via CSS custom properties (per element or on `:root`):

| Property                | Default     | Meaning                                  |
| ----------------------- | ----------- | ---------------------------------------- |
| `--motif-reveal-duration` | `600ms`     | timed-fallback transition duration       |
| `--motif-reveal-delay`    | `0ms`       | timed-fallback delay                     |
| `--motif-reveal-easing`   | `ease-out`  | easing                                   |
| `--motif-reveal-distance` | `16px`      | travel distance (intensity)              |
| `--motif-reveal-blur`     | `8px`       | starting blur radius (intensity)         |

Event: each element dispatches a bubbling `CustomEvent('motif:reveal', { detail: {
element } })` when revealed.

## Provenance: original (clean-room).
