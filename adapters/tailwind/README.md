# Motif Adapter, Tailwind CSS

How Motif recipes map onto a Tailwind-styled codebase (v3 and v4). Tailwind is a
*styling layer*, not a framework, this adapter explains how to express Motif's
CSS-first motion as utilities, where to drop to custom CSS, and how to keep the
accessibility guarantees intact.

> Provenance: original (clean-room). No third-party source is copied.

## Idiomatic structure

- Compose the **resting and end states** with utilities
  (`opacity-0` → `opacity-100`, `translate-y-4` → `translate-y-0`,
  `blur-sm` → `blur-none`) toggled by a state class or `data-*` variant.
- Put **keyframes and scroll-driven timelines** in a small custom CSS layer
  (`@layer utilities` / `@utility` in v4, or `tailwind.config` `extend.keyframes`).
  Tailwind's `animate-*` utilities reference those keyframes.
- Pair with whichever framework adapter renders the markup, Tailwind only supplies
  classes.

```html
<div data-motif-state="hidden"
     class="opacity-0 blur-sm translate-y-4 transition
            data-[motif-state=shown]:opacity-100
            data-[motif-state=shown]:blur-none
            data-[motif-state=shown]:translate-y-0
            motion-reduce:transition-none motion-reduce:opacity-100
            motion-reduce:blur-none motion-reduce:translate-y-0">
  …
</div>
```

## Lifecycle / cleanup / SSR / hydration

Tailwind has no runtime, these concerns are owned by the host framework adapter
(React/Vue/Svelte/Angular/vanilla). Tailwind contributes only static classes, which
are SSR- and hydration-safe by construction (same classes on server and client).
Use `data-*` attributes (toggled by the host) plus arbitrary variants
(`data-[state=open]:`) so the visual state is fully declarative and never depends on
hydration timing. JIT requires the variant classes to appear literally in source so
they're generated.

## Keyboard behaviour

- Style focus with `focus-visible:` variants (`focus-visible:ring-2`); never remove
  outlines without a visible replacement.
- Don't use utilities to hide focusable content from keyboard users, prefer
  `sr-only` for visually-hidden-but-accessible labels, not `hidden`.

## Pointer & coarse-pointer support

- Gate hover affordances with the `hover:` variant **plus** a `pointer-fine`
  custom variant so coarse pointers don't get stuck hover states. In v4:
  `@custom-variant pointer-fine (@media (hover: hover) and (pointer: fine))`.
- Ensure tap targets meet >=44px via sizing utilities (`min-h-11 min-w-11`).
- Add a `pointer-coarse` variant for touch-specific spacing.

## Responsive behaviour

Native to Tailwind: responsive variants (`sm:`/`md:`/`lg:`) and container queries
(`@container` + `@sm:` in v4 / the container-queries plugin in v3). Drive intensity,
duration, and offsets responsively by swapping utilities at breakpoints.

## Reduced-motion strategy

Tailwind ships first-class `motion-reduce:` and `motion-safe:` variants, **use
them on every animated element**. Author the static end state under
`motion-reduce:` (as in the example above) so reduced-motion users land on the
final visual instantly. For `animate-*` keyframe utilities, neutralise with
`motion-reduce:animate-none`.

```html
<div class="motion-safe:animate-[motif-shimmer_1.5s_linear_infinite]
            motion-reduce:animate-none"></div>
```

## Testing

- Snapshot the rendered class list; assert `motion-reduce:` variants are present on
  animated nodes (a lint/test guard prevents regressions).
- Build-time: ensure dynamically-composed class names are safelisted so JIT emits
  them.
- Visual: Playwright with `prefers-reduced-motion` emulation to confirm the
  `motion-reduce:` end state.

## Dependency trade-offs

Tailwind is a build-time dependency many projects already have; it adds no runtime
JS. It excels at the *state* half of a recipe (resting/end utilities + transitions)
but keyframes/scroll-timelines still live in a thin CSS layer. Don't reach for a JS
animation lib for things `transition`/`animate-*` utilities already do. Escalate
only per the Motif technique order.

## Normalised component contract knobs

| Knob                 | Tailwind surface                                        |
| -------------------- | ------------------------------------------------------- |
| class override       | utility classes (the native model); `class` merge       |
| style override       | arbitrary values `[--motif-x:…]`; inline `style`          |
| design tokens        | theme tokens (`theme()` / `@theme` in v4)               |
| intensity            | swap utilities (`blur-sm`↔`blur-md`) / arbitrary value  |
| duration             | `duration-300` / `[transition-duration:…]`              |
| delay                | `delay-150`                                             |
| easing               | `ease-out` / `[transition-timing-function:…]`           |
| disable-animation    | `motion-reduce:*` and/or a `no-anim` data variant       |
| reduced-motion       | `motion-reduce:` / `motion-safe:` variants              |
| responsive controls  | `sm:`/`md:`/`@container` variants                       |
| accessible labels    | `sr-only` label + host-provided `aria-*`                |
| event callbacks      | provided by the host framework adapter                  |
