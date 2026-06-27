# Save Status Indicator, Frappe-Vue

A compact `pending / saving / saved / error` status pill suited to a Frappe form
field or toolbar. Presentational only: it renders the `status` it's given and emits
`retry`, it never calls the backend, so it carries **no Frappe dependency** and is
unit-testable in isolation.

File: [`SaveStatus.vue`](./SaveStatus.vue). Vue 3 + plain scoped CSS only.

## Where it fits

Drop it next to a field (custom HTML field in Desk, or a column in a `frappe-ui`
SPA) and bind its `status` to the parent's save lifecycle. Because it's transport
-agnostic, the parent owns the network call and just feeds the resulting state down.

## Wiring to Frappe (the parent owns the call)

### Option A, `frappe-ui` resource (SPA)

```vue
<script setup>
import { ref, watch } from "vue";
import { createResource } from "frappe-ui";
import SaveStatus from "./SaveStatus.vue";

const status = ref("idle");
const save = createResource({
  url: "frappe.client.set_value",
  onSuccess: () => (status.value = "saved"),
  onError: () => (status.value = "error"),
});

function persist(args) {
  status.value = "saving";
  save.submit(args);
}
</script>

<template>
  <SaveStatus :status="status" @retry="persist(lastArgs)" />
</template>
```

### Option B, classic Desk (`frappe.call`)

```js
status.value = "saving";
frappe.call({ method: "frappe.client.set_value", args })
  .then(() => (status.value = "saved"))
  .catch(() => (status.value = "error"));
```

To embed in a Desk form, mount a tiny Vue app into a custom HTML field's wrapper and
`app.unmount()` on form teardown (see `adapters/frappe-vue/README.md`). No new build
system, it rides Frappe's existing Vite/`bench build`.

## Algorithm

The component is a pure function of `status`:

- `idle` → renders nothing (`v-if` removes the node).
- `pending` → "Unsaved changes" with a marker dot, warning tone.
- `saving` → "Saving…" with a transform-only CSS spinner.
- `saved` → "Saved" with a check, success tone.
- `error` → the `errorMessage` text plus a real **Retry** `<button>` that emits
  `retry`.

A `validator` on the `status` prop guards against typos. Tone colours are driven by
class, never colour alone (each state also has distinct text/icon).

## Accessibility

- **`role="status" aria-live="polite"`** visually-hidden region announces each
  status change to assistive tech without moving focus, appropriate for a frequent,
  low-urgency form signal (polite, not assertive).
- The decorative icon/spinner is `aria-hidden`.
- **Retry** is a genuine focusable `<button>` with a visible `:focus-visible` ring
  and a >=28px target; the parent handles the retry via the emitted event.
- Status is conveyed by **text + icon**, not hue alone (colour-blind safe).

## Reduced-motion behaviour

- `@media (prefers-reduced-motion: reduce)` disables the spinner rotation and the
  entrance animation. The spinner degrades to a **static ring**, still a clear
  "in progress" affordance, just not spinning.
- A live `matchMedia` ref (mounted/unmounted cleanly) also sets a `.no-motion`
  class, covering runtime preference flips and the `disableAnimation` prop, for
  engines that don't re-evaluate the media query mid-session.
- Net effect: status appears instantly with no motion; the aria-live announcement is
  unchanged.

## Design-token compatibility

Colours read from Frappe / `frappe-ui` CSS variables with standalone fallbacks:
`--text-muted`, `--motif-pending`, `--motif-success`, `--motif-danger`, `--motif-focus`. In
a real Frappe app these resolve to the theme's tokens so the pill matches Desk.

## Contract knobs

| Prop / event       | Type    | Purpose                                |
| ------------------ | ------- | -------------------------------------- |
| `status`           | String  | `idle\|pending\|saving\|saved\|error`  |
| `errorMessage`     | String  | error sub-text (pass `frappe._('…')`)  |
| `disableAnimation` | Boolean | force-off animation                    |
| `@retry`           | event   | emitted when the user clicks Retry     |

## Browser support

All evergreen browsers and Safari 12.1+. Vue 3, scoped CSS, `matchMedia` (mount
-guarded for any non-browser context). No SSR concern, Frappe frontends are
client-rendered.

## Provenance: original (clean-room).
