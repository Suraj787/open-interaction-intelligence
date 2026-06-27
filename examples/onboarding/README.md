# Onboarding — Progressive, Staged, Skippable

A worked example from **Motif**. PATTERNS before
EFFECTS; browser-native first; accessibility and reduced-motion mandatory.

## Context
- **Product type:** SaaS app first-run experience.
- **Page/screen:** A short onboarding flow — a few steps introducing key actions, shown
  on first login (and re-accessible from Help).
- **Target user:** A brand-new user, possibly evaluating the product, with limited patience.
- **Primary task:** Understand enough to take the first real action — and be able to
  **skip** to the product at any moment.

## User problem
The previous onboarding dumped everything at once (overwhelming) and a redesign over-
corrected with long auto-playing animated slides the user couldn't skip or control. New
users bounced. We need staged reveal that respects attention, is fully **skippable**, and
never traps anyone in a motion sequence.

## Candidate approaches considered
1. **One dense screen, everything visible.** No hand-holding; overwhelming and ignored.
   Rejected as default.
2. **Auto-advancing animated carousel, no skip.** Feels polished but removes user control,
   wastes time, and fails reduced-motion. Rejected.
3. **Self-paced staged disclosure:** one focused step at a time, user advances with
   Next/Enter, a persistent **Skip**, gentle per-step crossfade, progress shown as text +
   dots. **Selected.**

## Selected pattern
**User-paced staged disclosure with always-available skip.** Each step earns attention by
being small and advanced *by the user*, not a timer.

## Selected effect/technique
Simplest that works, native first:
- **Step transition:** ~180ms opacity crossfade (+ small translate) between steps, triggered
  only by user navigation — never auto-played.
- **Optional element stagger:** within a step, 2–3 elements may fade in with a small delay
  (≤250ms total). Cosmetic only; content is readable instantly if skipped.
- **Progress:** "Step 2 of 4" text plus dots — meaning is textual, not motion.
- **Skip** and **Back** are always present and keyboard-reachable.

## Rejected effects (and why)
- **Auto-advancing slides / timed animations** — removes control; a hostile pattern for
  first-run, and unusable under reduced motion.
- **Confetti on finishing onboarding** — borderline; once-only completion *could* justify a
  tiny flourish, but for a tool people set up repeatedly across workspaces it reads as
  forced delight, so we keep a calm "You're all set" instead.
- **Continuous looping illustrations/Lottie behind text** — continuous motion behind reading
  content; distracting and costly.
- **Long entrance choreography per step** — decoration that delays the point of each step.

## Implementation sketch
Vue stepper; user-driven transitions; skip/back persistent. CSS owns motion.

```vue
<script setup>
import { ref } from 'vue'
const steps = ['Welcome', 'Create a project', 'Invite a teammate', 'You're all set']
const i = ref(0)
const emit = defineEmits(['done'])
function next() { i.value < steps.length - 1 ? i.value++ : emit('done') }
function back() { if (i.value > 0) i.value-- }
function skip() { emit('done') }       // straight to the product
</script>

<template>
  <section class="onb" role="dialog" aria-modal="true" aria-label="Getting started">
    <p class="onb__progress" aria-live="polite">Step {{ i + 1 }} of {{ steps.length }}</p>
    <Transition name="step" mode="out-in">
      <div class="onb__step" :key="i">
        <h2>{{ steps[i] }}</h2>
        <slot :name="`step-${i}`" />
      </div>
    </Transition>
    <div class="onb__nav">
      <button v-if="i > 0" @click="back">Back</button>
      <button class="primary" @click="next">{{ i === steps.length - 1 ? 'Finish' : 'Next' }}</button>
      <button class="ghost" @click="skip">Skip</button>
    </div>
  </section>
</template>

<style>
.step-enter-active, .step-leave-active { transition: opacity .18s ease, transform .18s ease; }
.step-enter-from { opacity: 0; transform: translateY(8px); }
.step-leave-to   { opacity: 0; transform: translateY(-8px); }
@media (prefers-reduced-motion: reduce) {
  .step-enter-active, .step-leave-active { transition: none; }
}
</style>
```

## Accessibility
- **Skippable + self-paced:** Skip is always present; nothing auto-advances. Enter/Space
  triggers Next; Escape skips.
- **Reduced motion:** crossfades and staggers disabled; steps swap instantly.
- **Focus:** on each step, focus moves to the step heading/primary action; on finish/skip,
  focus returns to a sensible place in the app.
- **Announcements:** `aria-live="polite"` reports "Step 2 of 4"; the flow is a labeled dialog.
- **No motion-only meaning:** progress is text + dots; the stagger carries no information.

## Performance
- Animate only `opacity`/`transform`, brief, user-triggered.
- No looping background media; no offscreen/continuous motion.
- Budget posture: onboarding assets lazy-loaded; never block first paint of the real app.

## Validation
- Skip at any step lands directly in the product with sensible focus.
- Keyboard-only completes and exits the whole flow.
- Reduce-motion → instant step changes, all content intact.
- Nothing advances on its own; re-opening from Help works.
