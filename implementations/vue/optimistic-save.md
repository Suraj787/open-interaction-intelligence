# Optimistic Save — Vue 3

A `<script setup>` component that demonstrates the optimistic-save pattern: the UI
commits to the user's intent immediately, shows a transient progress → confirmation,
and only surfaces an error (with retry) if the async work rejects.

File: [`OptimisticSave.vue`](./OptimisticSave.vue). No external dependencies.

## Usage

```vue
<script setup>
import OptimisticSave from "./OptimisticSave.vue";

// Inject the real async work — keeps the component transport-agnostic.
const saveTitle = () =>
  fetch("/api/save", { method: "POST" }).then((r) => {
    if (!r.ok) throw new Error("save failed");
  });
</script>

<template>
  <OptimisticSave
    :save-fn="saveTitle"
    label="Save"
    @saved="onSaved"
    @error="onError"
  />
</template>
```

## Algorithm / state machine

```
idle ──save()──▶ saving ──resolve──▶ saved ──(savedDuration)──▶ idle
                     └────reject────▶ error ──save()/Retry──▶ saving
```

- `save()` flips to **saving** *immediately* (optimistic — no waiting for the
  network to show feedback) and ignores re-entry while a save is in flight.
- On resolve → **saved**, emit `saved`, then a timer returns to **idle** after
  `savedDuration` (default 1600 ms) so the control is reusable.
- On reject → **error**, emit `error`; the button relabels to "Retry" and calling
  `save()` again restarts the cycle.
- Every transition emits `stateChange(next)` for host orchestration.
- The saved timer is cleared on re-save and on unmount (no stray timers).

The async work is the `saveFn` prop, so the component has no knowledge of `fetch`,
Axios, or Frappe — making it trivially unit-testable with a stub promise.

## Accessibility

- **`role="status" aria-live="polite"`** visually-hidden region is the single
  accessible source of truth; it announces "Saving…", "Saved", "Couldn't save — tap
  to retry" without stealing focus. The *visible* status chip is `aria-hidden` to
  avoid double announcement.
- **`aria-busy`** on the button reflects the saving state; the button is `disabled`
  while in flight (cursor `progress`).
- **Focus is never moved or trapped**; `:focus-visible` keeps a visible ring.
- Error state is conveyed by **text** ("Couldn't save"), not colour alone.
- Button meets the 44px minimum target for coarse pointers.

## Reduced-motion behaviour

Two layers, both honoured:

1. A dependency-free `usePrefersReducedMotion`-style `ref` tracks
   `matchMedia('(prefers-reduced-motion: reduce)')` live (subscribed in
   `onMounted`, cleaned up in `onUnmounted`). When reduced (or `disableAnimation`
   prop is set), the `<Transition>` name becomes `motif-none` — a transition with no
   CSS — so status swaps are **instant**.
2. A scoped `@media (prefers-reduced-motion: reduce)` block disables the saving
   pulse and the chip enter/leave transition outright.

Result: state changes are instantaneous with no transforms or pulsing; the aria-live
announcement still fires, so non-visual feedback is unchanged.

## Contract knobs

| Prop / event       | Type       | Purpose                                    |
| ------------------ | ---------- | ------------------------------------------ |
| `saveFn`           | Function   | async work returning a Promise             |
| `label`            | String     | idle button label                          |
| `savedDuration`    | Number     | ms the "Saved" state lingers               |
| `disableAnimation` | Boolean    | force-off animation                        |
| `--motif-accent` etc.| CSS var    | design-token colour overrides (scoped)     |
| `@stateChange`     | event      | fires on every state transition            |
| `@saved`           | event      | fires on success                           |
| `@error`           | event      | fires with the rejection reason            |

Colours read from CSS custom properties (`--motif-accent`, `--motif-danger`,
`--motif-success`, `--motif-focus`, `--motif-muted`, `--motif-border`) for design-token
compatibility.

## Browser support

All evergreen browsers and Safari 12.1+. Uses only Vue 3 `<Transition>`, scoped CSS,
`matchMedia`, and `setTimeout`. `matchMedia` access is mount-guarded so SSR
(Nuxt/`@vue/server-renderer`) renders the idle markup without touching `window`.

## Provenance: original (clean-room).
