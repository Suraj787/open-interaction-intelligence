# Enterprise Dashboard, Payroll & Analytics

A worked example from **Motif**. The discipline:
search PATTERNS before EFFECTS, prefer browser-native CSS, keep accessibility and
reduced-motion mandatory, and refuse motion that hurts a dense, data-heavy screen.

## Context
- **Product type:** Internal enterprise ERP / analytics suite.
- **Page/screen:** Payroll + workforce analytics dashboard, KPI tiles, a
trend chart, a paginated payroll run table, and a few drill-down filters.
- **Target user:** Payroll/finance operators and managers reviewing numbers under
time pressure, often for hours at a stretch, frequently on modest hardware.
- **Primary task:** Read current figures, spot anomalies, confirm a payroll run,
and export. Comprehension and trust matter far more than delight.

## User problem
The current dashboard gives no feedback when filters apply or data refreshes, so
users can't tell whether the numbers on screen are current or stale. Loading is a
hard content swap that causes layout jumps, and an earlier "improvement" added
decorative animated gradients and count-up number tickers that make the screen feel
busy and slow. Operators report eye fatigue and distrust of the figures.

## Candidate approaches considered
1. **Animated count-up on every KPI tile + animated gradient backdrop.** Looks
   "alive," but turns a reference surface into a showcase and obscures the actual
   value during the count. Rejected.
2. **Full-screen blocking spinner on every refresh.** Honest about loading but
   destroys context and hierarchy; users lose their place on each filter change.
   Rejected.
3. **Restrained inline feedback: skeleton placeholders that match final layout, a
   quiet "Updated HH:MM" timestamp, and a brief, non-blocking highlight on values
   that actually changed.** Communicates freshness without theatrics. **Selected.**

## Selected pattern
**Stable-layout loading + change confirmation.** Hierarchy is carried by typography,
spacing and weight, not motion. Feedback is reserved for two real events: "data is
loading" and "this value just changed."

## Selected effect/technique
Simplest thing that works, browser-native first:
- **Skeleton placeholders** sized to the real content so nothing reflows when data
  arrives (CSS only; a low-contrast shimmer at most, or static blocks).
- **Changed-value cue:** a ~600ms background fade on the specific tile/cell whose
  number changed since last load, a single `transition` on `background-color`,
  then back to transparent. No count-up; the final number is shown immediately.
- **Freshness:** a plain text "Updated 14:32" caption, updated on each successful fetch.

## Rejected effects (and why)
- **Count-up number tickers**, decoration-only animation that *delays* reading the
  value; actively harmful on a reference screen.
- **Continuous animated gradient / particles behind the charts**, continuous motion
  behind dense UI; raises cognitive load and burns GPU for zero information.
- **Confetti / celebratory burst on "payroll confirmed"**, confetti for a frequent,
  serious action trivializes it and annoys daily users.
- **Card flip / 3D tilt on tiles**, motion that conveys no state; pure decoration.

## Implementation sketch
Browser-native + light Vue/Frappe-Vue binding. Each metric component knows its
previous value and toggles a `.is-changed` class for one transition cycle.

```vue
<script setup>
import { ref, watch } from 'vue'
const props = defineProps({ value: Number, loading: Boolean, updatedAt: String })
const changed = ref(false)
let prev = props.value
watch(() => props.value, (v) => {
  if (prev !== undefined && v !== prev) {
    changed.value = true
    setTimeout(() => (changed.value = false), 650)
  }
  prev = v
})
</script>

<template>
  <div class="kpi" :class="{ 'is-changed': changed }">
    <span class="kpi__label">{{ label }}</span>
    <span v-if="loading" class="kpi__skeleton" aria-hidden="true" />
    <span v-else class="kpi__value">{{ value }}</span>
    <span class="kpi__updated">Updated {{ updatedAt }}</span>
  </div>
</template>

<style>
.kpi { transition: background-color .25s ease; }
.kpi.is-changed { background-color: var(--accent-soft); }
.kpi__skeleton { display:block; height:1.5rem; width:60%;
  background:linear-gradient(90deg,#eee,#f5f5f5,#eee); border-radius:4px; }
@media (prefers-reduced-motion: reduce) {
  .kpi { transition: none; }            /* still flips class; just no fade */
}
</style>
```

## Accessibility
- **Reduced motion:** `prefers-reduced-motion: reduce` removes the fade; the changed
  state can instead show a brief static outline so the meaning survives without motion.
- **No motion-only meaning:** "changed" is also conveyed by the updated timestamp and,
  for screen readers, an `aria-live="polite"` region announcing e.g. "Net pay updated."
- **Keyboard/focus:** filters and table are fully keyboard operable; refresh never
  steals focus or moves the user's position.
- Skeletons are `aria-hidden`; a single polite "Loading payroll data" status is announced.

## Performance
- Animations limited to `background-color`/`opacity`, cheap, compositor-friendly.
- **No offscreen or continuous motion**; the changed-value cue runs once and stops.
- Skeletons prevent layout thrash (no CLS) and reading is never blocked.
- Budget posture: motion is a rounding error in the frame budget; charts/data own it.

## Validation
- Toggle OS "reduce motion", fades disappear, meaning remains.
- Change a filter, verify no layout jump, timestamp updates, only truly-changed cells cue.
- Screen reader announces loading + value updates once (no spam).
- Confirm no animation runs while the tab/section is offscreen or idle.
