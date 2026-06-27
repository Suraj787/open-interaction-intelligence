# Command Palette, Reveal Motion & Focus Management

A worked example from **Motif**. PATTERNS before
EFFECTS; browser-native first; accessibility and reduced-motion mandatory.

## Context
- **Product type:** Productivity/SaaS app with a Cmd/Ctrl-K command palette.
- **Page/screen:** Overlay palette for fast navigation and actions, summoned from anywhere.
- **Target user:** Power users who live on the keyboard and expect instant response.
- **Primary task:** Summon, type, choose, execute, in well under a second. Speed and
  keyboard correctness dominate; the reveal is incidental.

## User problem
The palette either pops in with no transition (feels abrupt, unclear where focus went) or,
in an over-designed variant, animates in slowly (~400ms) so fast users out-type the
animation and the first keystrokes get lost. We need a reveal that is **fast, calm, and
keyboard-perfect**, focus into the input immediately, restore it on close.

## Candidate approaches considered
1. **No transition, hard show/hide.** Maximally fast but jarring and the overlay's origin
   is unclear; focus handling still required regardless. Acceptable but slightly harsh.
2. **Large scale/blur cinematic entrance (~400ms).** Looks premium, costs latency on a
   hot path; users hit Enter before it settles. Rejected.
3. **Tiny, fast reveal:** ~120ms opacity + 4-8px upward translate, input focused on the
   same frame it opens; Escape closes and restores focus. **Selected.**

## Selected pattern
**Fast modal reveal with strict focus management.** The motion is a courtesy, never a gate;
the input is usable from frame one.

## Selected effect/technique
Simplest that works, native first:
- **Reveal:** `opacity 0→1` + `translateY(6px→0)` over ~120ms, `ease-out`. A light scrim
  fades with it. That's all.
- **Focus:** move focus to the search input as the palette mounts; don't wait for the
  transition to end. Type-ahead works immediately.
- **Close:** Escape (or scrim click) hides instantly-ish (~100ms) and returns focus to the
  element that opened it.
- Use the platform `<dialog>` or a focus-trapped container; native first.

## Rejected effects (and why)
- **Slow/cinematic entrance**, adds latency to a latency-critical interaction; users beat it.
- **Bouncy spring overshoot**, decoration that delays focus settling and selection.
- **Backdrop blur animation on a big surface**, expensive paint on the hot path for no info.
- **Result rows animating in one-by-one as you type**, continuous motion that fights rapid
  filtering; results should update instantly.

## Implementation sketch
Vue overlay using native `<dialog>`-style semantics; focus trap + restore. CSS owns motion.

```vue
<script setup>
import { ref, watch, nextTick } from 'vue'
const open = ref(false)
const input = ref(null)
let opener = null

function show() { opener = document.activeElement; open.value = true
  nextTick(() => input.value?.focus()) }            // focus now, not after anim
function hide() { open.value = false; opener?.focus() }

function onKey(e) {
  if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); show() }
  if (e.key === 'Escape' && open.value) hide()
}
window.addEventListener('keydown', onKey)
</script>

<template>
  <Transition name="palette">
    <div v-if="open" class="palette-scrim" @click.self="hide" role="presentation">
      <div class="palette" role="dialog" aria-modal="true" aria-label="Command palette">
        <input ref="input" type="text" role="combobox" aria-expanded="true"
               aria-controls="cmd-results" placeholder="Type a command…" />
        <ul id="cmd-results" role="listbox"><!-- results, arrow-key navigable --></ul>
      </div>
    </div>
  </Transition>
</template>

<style>
.palette-enter-active, .palette-leave-active { transition: opacity .12s ease; }
.palette-enter-from, .palette-leave-to { opacity: 0; }
.palette-enter-active .palette { transition: transform .12s ease; }
.palette-enter-from .palette { transform: translateY(6px); }
@media (prefers-reduced-motion: reduce) {
  .palette-enter-active, .palette-leave-active,
  .palette-enter-active .palette { transition: none; }
}
</style>
```

## Accessibility
- **Focus management:** focus enters the input on open and is **restored to the opener** on
  close; focus is trapped within the dialog while open (`aria-modal="true"`).
- **Keyboard-first:** Cmd/Ctrl-K opens, arrows move the active option (`aria-activedescendant`),
  Enter executes, Escape closes. No pointer needed.
- **Reduced motion:** transitions removed; open/close are instant, the fast path users
  actually want.
- **No motion-only meaning:** selection/active state is conveyed by `aria-selected` and a
  visible highlight, not by movement.

## Performance
- Animate only `opacity`/`transform` for ~120ms; no blur animation, no per-row stagger.
- Nothing animates while closed (component unmounted); no offscreen/continuous motion.
- Budget posture: the reveal must never delay first input, focus and typing precede the tween.

## Validation
- Open and immediately type, no keystrokes lost, no wait.
- Escape and scrim-click close and restore focus to the opener.
- Tab cannot leave the open dialog; arrows + Enter run a command.
- Reduce-motion → instant open/close; everything still works.
