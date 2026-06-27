# ERP Form — Save Feedback (Frappe-Vue)

A worked example from **Motif**. PATTERNS before
EFFECTS; browser-native first; accessibility and reduced-motion mandatory.

## Context
- **Product type:** Frappe/ERPNext business application (Frappe-Vue frontend).
- **Page/screen:** A document form (e.g. Customer, Sales Order) with many fields,
  child tables, and auto-save or explicit save.
- **Target user:** Back-office staff entering and editing records all day.
- **Primary task:** Edit fields and be **certain** the change persisted before moving on.

## User problem
> "Users cannot tell if their changes were saved."

After editing, nothing visibly confirms persistence. Users re-click Save, navigate
away unsure, or lose trust. The fix must make save **state** legible — dirty, saving,
saved, error — without blocking work or being patronizing.

## Candidate approaches considered
1. **Blocking modal "Saved successfully" on every save.** Unambiguous but stops the
   workflow dead and demands a dismiss click on a routine action. Rejected.
2. **Confetti / celebratory animation on save.** Save is a frequent, mundane action;
   celebrating it is noise and quickly insulting. Rejected.
3. **Persistent inline save-state indicator** near the form title — a quiet label that
   moves through *Unsaved changes → Saving… → Saved HH:MM*, plus a polite
   screen-reader announcement and a toast only on **error**. **Selected.**

## Selected pattern
**Ambient save-state indicator + error-only interruption.** Success is shown calmly
and continuously; only failure earns an interrupt, because only failure needs action.

## Selected effect/technique
Simplest that works, native first:
- A small status pill bound to save state. Text changes do the communicating.
- On transition to **Saved**, a brief checkmark with a ~200ms opacity fade-in (CSS
  `transition`), then it rests as "Saved 14:32". No movement of surrounding layout.
- **Saving…** may show a small spinner (native CSS rotation) but never blocks input.
- **Error** raises a non-blocking toast with a Retry action and keeps the form editable.

## Rejected effects (and why)
- **Confetti on save** — confetti for a frequent action; trivializes routine work.
- **Blocking success modal** — interrupts a non-exceptional event; adds a needless click.
- **Full-form flash/shake on save** — decoration that distracts from the field just edited.
- **Continuous pulsing "saving" overlay** — continuous motion over dense form fields.

## Implementation sketch
Frappe-Vue framing using a resource/save handler. The indicator reflects `state`; the
live region announces it.

```vue
<script setup>
import { ref } from 'vue'
import { createResource } from 'frappe-ui'

const state = ref('saved')      // 'dirty' | 'saving' | 'saved' | 'error'
const savedAt = ref('')

const doc = createResource({
  url: 'frappe.client.save',
  onSuccess() { state.value = 'saved'; savedAt.value = new Date().toLocaleTimeString() },
  onError()   { state.value = 'error' },        // toast handled by watcher
})

function onFieldChange() { state.value = 'dirty' }
function save() { state.value = 'saving'; doc.submit({ doc: /* current doc */ }) }
</script>

<template>
  <div class="form-header">
    <h1>{{ title }}</h1>
    <span class="save-state" :data-state="state">
      <template v-if="state === 'dirty'">Unsaved changes</template>
      <template v-else-if="state === 'saving'">Saving…</template>
      <template v-else-if="state === 'saved'">Saved {{ savedAt }}</template>
      <template v-else>Save failed</template>
    </span>
    <!-- polite SR announcement, separate from visual pill -->
    <span class="sr-only" role="status" aria-live="polite">
      {{ state === 'saved' ? 'Changes saved' : state === 'error' ? 'Save failed' : '' }}
    </span>
  </div>
</template>

<style>
.save-state[data-state="saved"]::before { content:"✓ "; }
.save-state { transition: opacity .2s ease; }
.sr-only { position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0 0 0 0); }
@media (prefers-reduced-motion: reduce) { .save-state { transition:none; } }
</style>
```

## Accessibility
- **Screen-reader announcement** via `role="status" aria-live="polite"` — "Changes saved"
  is announced without stealing focus. Errors announced the same way plus the toast.
- **Reduced motion:** checkmark/spinner fades removed; the *text* still conveys state,
  so meaning is never motion-only.
- **Keyboard/focus:** save is reachable via keyboard; focus stays in the field the user
  was editing — no modal grabs it. Error toast is reachable and dismissible by keyboard.

## Performance
- Only `opacity` transitions; spinner is a single transformed element, paused when idle.
- No layout shift: the pill reserves its width so text changes don't nudge the title.
- Budget posture: effectively free; the network save dominates, the UI just reports it.

## Validation
- Edit → indicator shows "Unsaved changes"; save → "Saving…" → "Saved HH:MM".
- Screen reader announces "Changes saved" once per successful save (not on keystrokes).
- Force a save failure → non-blocking toast with Retry; form stays editable; SR announces failure.
- Toggle reduce-motion → no animation, status text still fully informative.
