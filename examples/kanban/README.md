# Kanban — Drag Feedback & Column Move

A worked example from **Motif**. PATTERNS before
EFFECTS; browser-native first; accessibility and reduced-motion mandatory.

## Context
- **Product type:** Work-tracking board (Kanban) inside a project tool.
- **Page/screen:** Multi-column board; cards dragged within and across columns.
- **Target user:** Team members triaging and re-prioritizing work throughout the day.
- **Primary task:** Move a card to a new column/position and trust the new state — with
  clear feedback during the drag and a clean settle on drop.

## User problem
The board uses an abrupt drag with no lift cue, and on drop cards "teleport" while the
column re-lays-out with a jarring jump. Users lose track of where the card landed and
sometimes drop into the wrong column. The goal is **spatial continuity** — the eye
should follow the card from pickup to its resting place — without janky layout animation.

## Candidate approaches considered
1. **Instant move, no feedback.** Fast but disorienting; drop target is ambiguous and
   the relayout jumps. Rejected.
2. **Heavy physics / springy bounce on drop + animated placeholder pulsing.** Feels toy-
   like, slows repeated moves, and the pulsing is continuous motion behind dense cards.
   Rejected.
3. **Restrained drag affordances:** subtle lift (shadow + slight scale) on pickup, a
   clear gap/placeholder showing the insertion point, and a short FLIP settle on drop so
   neighbors slide into place. **Selected.**

## Selected pattern
**Pick-up / placeholder / settle with spatial continuity.** The card under the pointer is
the focus; everything else moves the minimum needed to make room and resolve cleanly.

## Selected effect/technique
Simplest that works, native first:
- **Pickup:** dragged card gets `transform: scale(1.02)` + raised box-shadow (≤150ms) so
  it visibly "lifts." Pointer drag uses native pointer/drag events; position via `transform`.
- **Insertion point:** a placeholder block of the card's height marks where it will land;
  the gap opens with a short height/transform transition.
- **Drop/settle:** FLIP — measure positions before/after, animate neighbors via `transform`
  over ~160ms so nothing teleports; the dropped card eases into the placeholder slot.

## Rejected effects (and why)
- **Springy bounce / overshoot on drop** — decoration that delays the next action and
  obscures the final position; precision tool, not a trampoline.
- **Pulsing/glowing placeholder** — continuous motion behind dense UI; a static highlighted
  gap reads better.
- **Full-column reflow animation on every hover** — janky layout animation; thrashes layout.
- **Confetti when a card hits "Done"** — confetti for a frequent action.

## Implementation sketch
Native pointer events drive the drag; CSS owns lift and gap; a FLIP pass owns the settle.
(Library-agnostic — no third-party component code.)

```js
// FLIP settle: call before mutating DOM order, then after.
function flip(container) {
  const items = [...container.children]
  const first = new Map(items.map(el => [el, el.getBoundingClientRect()]))
  return function play() {
    for (const el of items) {
      const last = el.getBoundingClientRect()
      const f = first.get(el); if (!f) continue
      const dx = f.left - last.left, dy = f.top - last.top
      if (dx || dy) {
        el.style.transform = `translate(${dx}px,${dy}px)`
        el.style.transition = 'none'
        requestAnimationFrame(() => {
          el.style.transition = 'transform .16s ease'
          el.style.transform = ''
        })
      }
    }
  }
}
```
```css
.card.dragging { transform: scale(1.02); box-shadow: 0 6px 16px rgba(0,0,0,.18);
  transition: transform .12s ease, box-shadow .12s ease; }
.placeholder { background: var(--accent-soft); border: 1px dashed var(--accent);
  border-radius: 8px; }
@media (prefers-reduced-motion: reduce) {
  .card.dragging { transform: none; transition: none; }
  .card { transition: none !important; }   /* FLIP becomes instant reposition */
}
```

## Accessibility
- **Keyboard DnD:** cards are focusable; arrow keys move within a column, modifier+arrow
  moves across columns; Space/Enter to pick up and drop — no pointer required.
- **Reduced motion:** lift, gap and FLIP collapse to instant repositioning; layout still
  correct, just no tween.
- **No motion-only meaning:** moves are announced via `aria-live="polite"` ("Card X moved
  to In Progress, position 2"); the placeholder also has an accessible label.
- **Focus:** focus stays on the moved card after drop.

## Performance
- Only `transform`/`opacity`/`box-shadow` animate — compositor-friendly, no layout in the
  animated frames (FLIP measures once, then transforms).
- No continuous/offscreen animation; motion exists only during an active drag/drop.
- Budget posture: virtualize tall columns; cap FLIP to visible cards.

## Validation
- Drag within and across columns — placeholder always shows the true drop target.
- Drop — neighbors slide, nothing teleports, focus lands on the card.
- Keyboard-only move works end to end with announcements.
- Reduce-motion → instant, correct, no jank. No motion when idle.
