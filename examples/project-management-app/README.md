# Project Management App — Status & Row Change Feedback

A worked example from **Motif**. PATTERNS before
EFFECTS; browser-native first; accessibility and reduced-motion mandatory.

## Context
- **Product type:** Team project-management tool (board + list views of tasks).
- **Page/screen:** A task **list** view with status, assignee, due date; statuses change
  often and rows are added/removed as work flows.
- **Target user:** Team members and leads scanning and updating many tasks per session.
- **Primary task:** Change a task's status, add/remove tasks, and trust that what they
  see reflects reality — without losing their place in a long list.

## User problem
Status changes and row insert/remove happen instantly with no transition, so updates
feel abrupt and easy to miss; when a row disappears (e.g. moved/completed-filtered),
users aren't sure what happened. The risk on the other side is over-animating a
high-frequency list into something seasick-inducing.

## Candidate approaches considered
1. **No transitions (current).** Fast but changes are easy to miss and removals feel
   like glitches. Rejected.
2. **Elaborate per-row choreography** (slide + scale + color sweep on every change).
   Pretty once, nauseating across dozens of edits per minute. Rejected.
3. **Minimal, meaningful micro-feedback:** a brief status-color crossfade, and
   height/opacity transitions for insert/remove so rows enter and leave instead of
   popping. Driven by a list-transition primitive. **Selected.**

## Selected pattern
**Object permanence for list mutations.** Items appear, change, and leave in ways that
preserve the user's mental model — just enough motion to explain *what changed*, no more.

## Selected effect/technique
Simplest that works, native first:
- **Status change:** ~200ms crossfade of the status pill's background/label color via CSS
  `transition`. The label text is the source of truth; color reinforces.
- **Insert:** new row fades in and expands from 0 → full height (~180ms).
- **Remove:** row collapses height + fades out (~180ms) before leaving the DOM, so the
  gap closes smoothly instead of snapping.
- Implemented with Vue's `<TransitionGroup>` (FLIP) so neighbors slide rather than jump.

## Rejected effects (and why)
- **Scale/bounce on every status change** — decoration-only; meaningless at high frequency.
- **Confetti on task complete** — confetti for a frequent action; quickly becomes noise.
- **Long (>300ms) reorder animations** — make a fast tool feel slow; users out-pace them.
- **Continuous shimmer on "active" rows** — continuous motion behind dense text.

## Implementation sketch
Vue `<TransitionGroup>` with FLIP for neighbor movement; CSS owns the actual motion.

```vue
<script setup>
defineProps({ tasks: Array })   // [{ id, title, status }]
</script>

<template>
  <TransitionGroup tag="ul" name="row" class="task-list">
    <li v-for="t in tasks" :key="t.id" class="task-row">
      <span class="title">{{ t.title }}</span>
      <span class="status" :data-status="t.status">{{ t.status }}</span>
    </li>
  </TransitionGroup>
</template>

<style>
.status { transition: background-color .2s ease, color .2s ease; }
.row-enter-from, .row-leave-to { opacity: 0; }
.row-enter-active, .row-leave-active { transition: opacity .18s ease, transform .18s ease; }
.row-leave-active { position: absolute; }     /* let FLIP close the gap */
.row-move { transition: transform .18s ease; } /* neighbors slide, no jump */

@media (prefers-reduced-motion: reduce) {
  .status, .row-enter-active, .row-leave-active, .row-move { transition: none; }
}
</style>
```

## Accessibility
- **Reduced motion:** all transitions disabled; rows still appear/disappear and statuses
  still recolor — instantly, not jankily.
- **No motion-only meaning:** status is text first (color is reinforcement); insert/remove
  is reflected in an `aria-live="polite"` summary ("Task moved to Done").
- **Keyboard/focus:** when a focused row is removed, focus moves to the next logical row,
  never lost to `<body>`.

## Performance
- Animations limited to `opacity`/`transform`/`height` short bursts; `row-move` uses
  `transform` (compositor-friendly).
- No persistent/offscreen animation; transitions fire only on actual mutations.
- Budget posture: virtualize long lists; cap concurrent transitions so bulk updates
  don't animate hundreds of rows at once (animate the viewport, settle the rest).

## Validation
- Change status repeatedly — feedback reads as calm, never seasick.
- Insert/remove rows — neighbors slide, no snap, focus preserved.
- Bulk update — no frame drops; offscreen rows don't animate.
- Reduce-motion on — instant updates, all meaning intact.
