# Motif Adapter, Svelte

How Motif recipes map onto idiomatic Svelte (4 and 5/runes). Svelte's compiler and
built-in `transition:` / `animate:` directives make it an excellent Motif host, recipes stay CSS-first and let Svelte own state and teardown.

> Provenance: original (clean-room). No third-party source is copied.

## Idiomatic structure

Package a recipe as an **action + component**:

- A Svelte **action** (`use:blurReveal`) is the idiomatic home for
  observer/listener wiring on an element, it receives the node and returns
  `{ update, destroy }`.
- A `.svelte` component exposes the contract knobs as `export let` props (Svelte 4)
  or `$props()` (Svelte 5 runes), with scoped `<style>`.

Prefer Svelte's native `transition:fade` / `transition:fly` (and custom transition
functions) over hand-rolled animation, they respect mount/unmount automatically.

```svelte
<script>
  import { blurReveal } from './blur-reveal.js';
  export let intensity = 1;
</script>
<div use:blurReveal={{ intensity }} class="motif-reveal"><slot /></div>
```

## Lifecycle handling

- Component lifecycle: `onMount`, `onDestroy` (Svelte 4) or `$effect` (Svelte 5).
- **Actions** are the cleanest lifecycle unit for DOM effects: set up on call,
  react in `update(params)`, tear down in `destroy()`.
- Transition directives hook mount/unmount without manual lifecycle code.

## Cleanup

Return `destroy()` from the action; Svelte calls it when the node unmounts:

```js
export function blurReveal(node, params) {
  const io = new IntersectionObserver(/* … */);
  io.observe(node);
  return {
    update(next) { /* re-read params */ },
    destroy() { io.disconnect(); }, // also abort listeners / cancel RAF
  };
}
```

In Svelte 5, `$effect` returns its own cleanup closure, same discipline.

## SSR

SvelteKit renders components to HTML on the server. `onMount` and actions run
**client-only**, so observer code is naturally safe. Still guard any module-level
`window`/`matchMedia` access (use `browser` from `$app/environment`). `transition:`
directives don't run during SSR; the resting state is what's serialized.

## Hydration

SvelteKit hydrates the server HTML. Keep markup deterministic, don't branch on
`browser` during render in a way that changes structure, or hydration mismatches.
Apply enhanced start state in `onMount`/action, or via CSS, to avoid a flash.
`transition:...|local` and the `intro` option control whether transitions play on
initial hydration.

## Keyboard behaviour

- Use semantic elements; Svelte's `on:keydown` with modifiers
  (`on:keydown|preventDefault`) for handlers.
- Don't remove focusability for animation.
- Manage focus explicitly only for revealed dialogs/menus; restore on close. Style
  `:focus-visible` in scoped CSS. Svelte's a11y compiler warnings help here, heed
  them.

## Pointer & coarse-pointer support

- Unify input with `on:pointerdown`/`on:pointermove`.
- Detect capability via `matchMedia` in an action/store and switch affordances.
- Keep >=44px targets under `@media (pointer: coarse)`.

## Responsive behaviour

Prefer CSS media/container queries. For JS-driven layout, a small `media` store
(subscribes to `MediaQueryList`, cleans up on last unsubscribe) keeps it reactive.

## Reduced-motion strategy

Svelte transitions accept a `duration`; set it to `0` (or return an empty
transition) when reduced motion is preferred. Provide a `prefersReducedMotion`
readable store:

```js
const reduced = prefersReducedMotion(); // readable<boolean>, live
$: dur = $reduced ? 0 : 300;
```

Always include the CSS `@media (prefers-reduced-motion: reduce)` guard so the static
state holds pre-hydration too.

## Testing

- **Vitest + @testing-library/svelte** for behaviour/ARIA.
- Stub `IntersectionObserver`/`matchMedia` in setup.
- Assert action `destroy()` disconnects observers.
- Playwright for reduced-motion / coarse-pointer E2E.

## Dependency trade-offs

Svelte's built-in transitions/animations + `svelte/easing` cover most of the
catalogue with **zero runtime dependency** (it's compiled). This is one of the
lightest Motif hosts. Escalate beyond built-ins/CSS only per the technique order, and
never add a motion lib for an effect Svelte already ships.

## Normalised component contract knobs

| Knob                 | Svelte surface                                          |
| -------------------- | ------------------------------------------------------- |
| class override       | `class` prop / `class:` directive                       |
| style override       | `style` attr, `--motif-*` custom properties               |
| design tokens        | inherited CSS variables                                 |
| intensity            | `export let intensity` / `$props`                       |
| duration             | `duration` prop                                         |
| delay                | `delay` prop                                            |
| easing               | `easing` (from `svelte/easing`)                         |
| disable-animation    | `disableAnimation` prop                                 |
| reduced-motion       | `reducedMotion` prop + store                            |
| responsive controls  | media/container queries + media store                   |
| accessible labels    | `aria-label`, `aria-live`, `label` prop                 |
| event callbacks      | `createEventDispatcher` / callback props                |
