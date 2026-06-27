# Motif Adapter — Vue

How Motif recipes map onto idiomatic Vue 3 (`<script setup>`, Composition API). Vue is
a **first-class** Motif target. Recipes stay CSS-first; Vue contributes reactivity,
its `<Transition>`/`<TransitionGroup>` primitives, lifecycle, and cleanup.

> Provenance: original (clean-room). No third-party source is copied.

## Idiomatic structure

Package a recipe as a **composable + Single File Component**:

- `useBlurReveal(target, options)` — a composable returning reactive state and
  binding observers via `onMounted`/`onUnmounted`.
- `OptimisticSave.vue` etc. — SFC with `<template>`, `<script setup>`, scoped
  `<style>`. Knobs arrive as typed `defineProps`; callbacks as `defineEmits`.

Prefer Vue's native `<Transition>` for enter/leave — it adds/removes the
`*-enter-active` / `*-leave-to` classes you target in CSS, no JS animation needed.

```vue
<Transition name="motif-fade">
  <p v-if="visible">Revealed</p>
</Transition>
```

## Lifecycle handling

- `onMounted` to attach observers/listeners after the DOM exists.
- `onBeforeUnmount` / `onUnmounted` to tear them down.
- `watch`/`watchEffect` to re-bind when knobs change; use a template `ref` (or
  `useTemplateRef` in 3.5+) for the element handle.
- For animation hooks needing JS, use `<Transition>`'s
  `@enter`/`@leave` with the `done` callback.

## Cleanup

Register teardown in `onUnmounted`, or use `watchEffect`'s `onCleanup` /
`effectScope` so re-runs don't stack listeners:

```js
onMounted(() => {
  const io = new IntersectionObserver(/* … */);
  io.observe(el.value);
  onUnmounted(() => io.disconnect());
});
```

`<Transition>` cleans its own classes; you only own observers/listeners/RAF.

## SSR

For Nuxt / `@vue/server-renderer`: lifecycle hooks except `onServerPrefetch` don't
run on the server, so observer code is naturally client-only. Still guard
`window`/`matchMedia` access (use `import.meta.client` in Nuxt or a `typeof window`
check). `<Transition>` renders the resting state markup on the server with no JS.

## Hydration

Keep server and client markup identical to avoid hydration mismatch warnings. Don't
gate template structure on `window`. Apply the enhanced start state after mount (set
a reactive `mounted` flag in `onMounted`), or express the resting state in CSS so
hydration is flash-free. `<Transition appear>` can animate the initial render once
hydrated.

## Keyboard behaviour

- Use semantic elements and native `@keydown` handlers; bind with key modifiers
  (`@keydown.esc`, `@keydown.enter`).
- Don't strip focusability for layout/animation reasons.
- Manage focus explicitly only when revealing dialogs/menus; restore on close.
  Style `:focus-visible` in scoped CSS.

## Pointer & coarse-pointer support

- Unify input with `@pointerdown`/`@pointermove`.
- Detect capability via `matchMedia` inside a composable
  (`useMediaQuery`) and switch affordances reactively.
- Guarantee >=44px targets under `@media (pointer: coarse)`.

## Responsive behaviour

Lean on CSS media/container queries. When JS is required, a `useMediaQuery`
composable that subscribes to `MediaQueryList` (and cleans up in `onUnmounted`)
keeps it reactive without resize thrash.

## Reduced-motion strategy

Provide a `usePrefersReducedMotion()` composable returning a `ref<boolean>` that
tracks the media query live. Components read it to disable `<Transition>` (e.g.
`:css="false"` or a `name` swap to a no-op) and jump to the end state. Always pair
with the CSS `@media (prefers-reduced-motion: reduce)` guard.

```js
const reduced = usePrefersReducedMotion();
const transitionName = computed(() => (reduced.value ? 'motif-none' : 'motif-fade'));
```

## Testing

- **Vitest + @vue/test-utils**: mount, assert ARIA/state, trigger transitions.
- Stub `IntersectionObserver`/`matchMedia` in the test setup.
- Assert `onUnmounted` cleanup by unmounting and checking spies.
- Playwright for reduced-motion / coarse-pointer E2E.

## Dependency trade-offs

Vue's built-ins (`<Transition>`, `<TransitionGroup>`) cover most of the catalogue
dependency-free — prefer them. `@vueuse/core` is an *approved* convenience for
composables (`useIntersectionObserver`, `usePreferredReducedMotion`) if the project
already uses it; don't add it solely for one recipe. Escalate beyond CSS/WAAPI only
per the technique order.

## Normalised component contract knobs

| Knob                 | Vue surface                                             |
| -------------------- | ------------------------------------------------------- |
| class override       | `:class` binding / `class` attr                         |
| style override       | `:style`, `--motif-*` custom properties                   |
| design tokens        | inherited CSS variables; `tokens` prop optional         |
| intensity            | `defineProps({ intensity })`                            |
| duration             | `duration` prop / CSS var                               |
| delay                | `delay` prop / CSS var                                  |
| easing               | `easing` prop / CSS var                                 |
| disable-animation    | `disableAnimation` prop                                 |
| reduced-motion       | `reducedMotion` prop + composable                       |
| responsive controls  | media/container queries + `useMediaQuery`               |
| accessible labels    | `aria-label`, `aria-live`, `label` prop                 |
| event callbacks      | `defineEmits(['reveal','stateChange','settled'])`       |
