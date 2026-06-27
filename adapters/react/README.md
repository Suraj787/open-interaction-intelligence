# Motif Adapter, React

How Motif recipes map onto idiomatic React (18/19, function components + hooks).
Recipes stay CSS-first; React owns *state, lifecycle, and cleanup*, not the motion.

> Provenance: original (clean-room). No third-party source is copied.

## Idiomatic structure

Package a recipe as a **custom hook + a thin component**:

- `useBlurReveal(ref, options)`, encapsulates the observer/state machine.
- `<SkeletonLoader />`, presentational, accepts the contract knobs as props.

Keep DOM access in `ref`s; keep motion in a co-located CSS module / stylesheet.
Avoid inline animation in JS unless the Web Animations API is genuinely required.

```tsx
function Reveal({ children, intensity }: RevealProps) {
  const ref = useRef<HTMLDivElement>(null);
  useBlurReveal(ref, { intensity });
  return <div ref={ref} className="motif-reveal">{children}</div>;
}
```

## Lifecycle handling

- Side effects (observers, listeners, WAAPI) belong in `useEffect`
  (`useLayoutEffect` only when you must measure/set before paint to avoid flicker).
- Dependencies array tracks the knobs that should re-bind the effect.
- Never start animations during render; render must stay pure.

## Cleanup

Return a cleanup function from every `useEffect`. Under React 18 Strict Mode the
effect runs twice in dev, your cleanup must make that a no-op:

```tsx
useEffect(() => {
  const io = new IntersectionObserver(/* … */);
  io.observe(node);
  return () => io.disconnect();         // also abort listeners, cancel RAF/anims
}, [node]);
```

Use `AbortController` for listeners (`{ signal }`) so one `abort()` clears them all.

## SSR

For Next.js / RSC: the component renders static markup on the server. Any hook that
touches `window`, `matchMedia`, or `IntersectionObserver` must run **client-side
only**, mark the file `'use client'` and read browser APIs inside `useEffect`, not
during render. Provide an SSR-safe initial state (content visible, motion not yet
applied).

## Hydration

Avoid mismatches: do **not** branch markup on `typeof window` during render. Render
the same tree on server and client; apply the enhanced/hidden start state inside an
effect (or via a `mounted` flag set in `useEffect`) so the first client render
matches the server output. Prefer CSS for the resting state to dodge a hydration
flash entirely.

## Keyboard behaviour

- Use semantic elements; let the browser handle focus.
- Don't `tabIndex={-1}` interactive content to "clean up" tab order.
- Manage focus only deliberately (e.g. move focus into a revealed dialog) and
  restore it on unmount. Style `:focus-visible`.

## Pointer & coarse-pointer support

- Use React's unified pointer handlers (`onPointerDown`/`onPointerMove`).
- Detect capability with `matchMedia('(hover: hover)')` /
  `'(pointer: coarse)'` inside an effect; store in state to switch affordances.
- Ensure >=44px hit targets on coarse pointers.

## Responsive behaviour

Prefer CSS media/container queries. When layout logic truly needs JS, use a
`useMediaQuery` hook (subscribe to `MediaQueryList` change events, cleanup on
unmount) rather than reading `window.innerWidth` on resize.

## Reduced-motion strategy

Ship a `usePrefersReducedMotion()` hook that subscribes to
`matchMedia('(prefers-reduced-motion: reduce)')` and updates on change. Components
read it to skip transitions and jump to the end state. Always also include the CSS
`@media (prefers-reduced-motion: reduce)` block so the static state holds even
before hydration.

```tsx
const reduced = usePrefersReducedMotion();
return <div data-animate={!reduced} className="motif-reveal">{children}</div>;
```

## Testing

- **React Testing Library** for behaviour/ARIA; assert `aria-busy`, `aria-live`
  content, focus order.
- Mock `IntersectionObserver`/`matchMedia` in the jsdom setup file.
- Assert cleanup: unmount and verify `disconnect`/`removeEventListener` were called.
- Playwright for reduced-motion and coarse-pointer emulation E2E.

## Dependency trade-offs

Stay dependency-free: hooks + CSS cover the catalogue. Reach for `framer-motion`
only when orchestration (layout/shared-element/spring choreography) genuinely
exceeds CSS + WAAPI, and never add it just to fade something in. Document any such
escalation per the technique order.

## Normalised component contract knobs (props)

| Knob                 | Prop                                                    |
| -------------------- | ------------------------------------------------------- |
| class override       | `className`                                             |
| style override       | `style` (and `--motif-*` custom properties via `style`)   |
| design tokens        | inherits CSS variables; `tokens` prop optional          |
| intensity            | `intensity`                                             |
| duration             | `duration`                                              |
| delay                | `delay`                                                 |
| easing               | `easing`                                                |
| disable-animation    | `disableAnimation`                                      |
| reduced-motion       | `reducedMotion?: 'system' \| 'force' \| 'allow'`        |
| responsive controls  | `responsive` map / CSS queries                          |
| accessible labels    | `aria-label`, `aria-live`, `label`                      |
| event callbacks      | `onReveal`, `onStateChange`, `onSettled`                |
