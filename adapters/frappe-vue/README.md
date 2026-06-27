# Motif Adapter — Frappe-Vue

How Motif recipes integrate inside a **Frappe** app's frontend: Vue 3 + `frappe-ui`,
built by Frappe's existing Vite/esbuild pipeline, talking to the Frappe backend via
`frappe.call` / `frappe-ui`'s resource layer. Frappe-Vue is a **first-class** Motif
target. This guide layers Frappe-specific concerns on top of the Vue adapter
(`adapters/vue/README.md`) — read that first.

> Provenance: original (clean-room). No third-party source is copied.

## Where Motif lives in a Frappe app

Frappe frontends come in two shapes; Motif recipes work in both:

1. **`frappe-ui` SPA** (e.g. a `frontend/` app like CRM/Helpdesk/Gameplan): a
   normal Vue 3 + Vite project. Motif components are plain SFCs imported here.
2. **Desk integration** (form scripts / custom HTML fields / `frappe.ui` dialogs):
   mount a small Vue app into a Desk-provided DOM node, or use a CSS-only recipe via
   a bundled stylesheet.

Either way, **do not add a new build system**. Use the Vite config Frappe already
ships (`frappe-ui`'s Vite preset) and let `bench build` / the app's `yarn build`
produce the bundle in `<app>/public/`.

## Idiomatic structure

```
<app>/frontend/src/
  components/motif/
    SaveStatus.vue          # SFC, contract knobs as defineProps
    useReducedMotion.js     # shared composable
```

- Components are standard `<script setup>` SFCs with scoped `<style>` — no global
  CSS leakage into Desk.
- Knobs as typed `defineProps`; events as `defineEmits`.
- Reuse `frappe-ui` primitives (`Button`, `Badge`, `FeatherIcon`) and **design
  tokens** (its CSS variables / Tailwind theme) so Motif visuals match the Frappe look.

## Wiring to Frappe data (`frappe.call` / `frappe-ui`)

Motif components stay **transport-agnostic** — they render state and emit intent; the
host wires the backend. Two idiomatic options:

```js
// Option A — frappe-ui resource (preferred in SPAs)
import { createResource } from 'frappe-ui';
const save = createResource({
  url: 'frappe.client.set_value',
  // onSuccess → component state 'saved'; onError → 'error'
});

// Option B — global frappe.call (Desk / classic)
frappe.call({ method: 'frappe.client.set_value', args, })
  .then(() => status.value = 'saved')
  .catch(() => status.value = 'error');
```

The Motif `SaveStatus`/`OptimisticSave` components **require neither** — they accept a
`status` prop or expose a method and emit `save`. This keeps them testable without a
Frappe backend and lets you swap `frappe.call` for `createResource` freely.

## Lifecycle, cleanup, SSR, hydration

- Lifecycle/cleanup: identical to the Vue adapter (`onMounted`/`onUnmounted`,
  composable teardown).
- **SSR:** Frappe frontends are client-rendered SPAs / Desk-mounted — there is no
  Node SSR. So hydration mismatch is a non-issue, but still mount only after the
  target node exists (Desk supplies it asynchronously in dialogs/forms).
- **Desk mount/unmount:** when embedding in a form, create the Vue app in
  `refresh`/field render and `app.unmount()` when the field/dialog is destroyed to
  avoid leaks across route changes within Desk.

## Keyboard behaviour

- Respect Desk's existing shortcuts — don't bind global keys that clash with
  Frappe's (`Ctrl/Cmd+S` save, `Esc` to close dialogs). Scope handlers to your
  component.
- Use `frappe-ui` focusable components or semantic elements; keep `:focus-visible`
  rings. Restore focus to the triggering control when closing a popover/dialog.

## Pointer & coarse-pointer support

- Frappe runs on desktop and mobile/PWA — use Pointer Events and guarantee >=44px
  targets on `@media (pointer: coarse)`.
- Gate hover affordances behind `@media (hover: hover) and (pointer: fine)`; Desk
  list/table rows are touched on mobile.

## Responsive behaviour

Use `frappe-ui`'s Tailwind breakpoints and container queries so Motif components adapt
inside Desk's variable-width form columns and the narrower mobile Desk. Don't assume
viewport width — a form field's slot can be narrow on a wide screen.

## Reduced-motion strategy

Same guarantee as everywhere in Motif: a `useReducedMotion()` composable
(`matchMedia('(prefers-reduced-motion: reduce)')`, live) plus a scoped CSS
`@media (prefers-reduced-motion: reduce)` guard. Status changes (saving→saved)
become **instant** with no transition, and the aria-live announcement still fires.
This matters in data-entry-heavy Frappe forms where motion on every field save would
be noise.

## Testing

- **Vitest + @vue/test-utils** for the SFCs in isolation — mock the `frappe`
  global / `createResource` so no backend is needed.
- Stub `matchMedia` in setup; assert reduced-motion path and `aria-live` content.
- For Desk integration, a Cypress/Playwright run against a `bench` dev site
  exercises the real `frappe.call` wiring.

## Dependency trade-offs

`frappe-ui` and Vue are already in the app — using them is free. Stay within them:
do **not** add React, GSAP, or a second animation runtime into a Frappe bundle just
for an effect; it bloats `bench build` output and clashes with Frappe's CSS. Plain
CSS + Vue `<Transition>` + `frappe-ui` cover the catalogue. Escalate only per the
Motif technique order, and keep everything inside Frappe's existing Vite build.

## Normalised component contract knobs

| Knob                 | Frappe-Vue surface                                      |
| -------------------- | ------------------------------------------------------- |
| class override       | `:class` / `frappe-ui` `class` prop                     |
| style override       | `:style`, `--motif-*` custom properties                   |
| design tokens        | `frappe-ui` CSS variables / Tailwind theme tokens       |
| intensity            | `defineProps({ intensity })`                            |
| duration             | `duration` prop / CSS var                               |
| delay                | `delay` prop / CSS var                                  |
| easing               | `easing` prop / CSS var                                 |
| disable-animation    | `disableAnimation` prop                                 |
| reduced-motion       | `reducedMotion` prop + `useReducedMotion()`             |
| responsive controls  | Tailwind breakpoints / container queries                |
| accessible labels    | `aria-label`, `aria-live`, `label` prop                 |
| event callbacks      | `defineEmits(['save','stateChange','settled'])`         |
