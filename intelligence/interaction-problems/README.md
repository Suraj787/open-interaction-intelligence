# LEVEL 5 — Interaction Problems (Objectives)

This is the heart of Motif. Everything above narrows context; this level names the
**precise objective** the interaction must achieve, and points to the
**pattern(s)** that solve it. We search *problems → patterns*, never
*effects → places to use them*.

> Search order is mandatory: identify the objective here, choose a PATTERN that
> solves it, and only then pick the smallest EFFECT that implements the pattern
> (see `../effect-taxonomy/` and `../selection-policies/`).

Each objective below lists the patterns that legitimately solve it.

---

### 1. Attract attention
Bring the eye to one important thing (new item, primary CTA, alert).
- **Patterns:** Highlight / pulse-once; entrance reveal; badge/notification motion; contrast-by-motion against still surroundings.
- **Note:** One attention-grabber per viewport. Continuous attraction becomes noise.

### 2. Explain hierarchy
Show what's primary vs secondary; structure relationships.
- **Patterns:** Staggered reveal (parent before child); depth/elevation cues; progressive disclosure; size/position transitions.

### 3. Show system feedback
Acknowledge that the system received and is acting on input.
- **Patterns:** Button/press states; inline loading; optimistic UI; toast/snackbar; save/success/error feedback.

### 4. Preserve spatial continuity
Keep the user oriented across a change of view or state.
- **Patterns:** Shared-element transitions; layout/FLIP transitions; route transitions; expand-in-place; View Transitions API.

### 5. Demonstrate cause and effect
Make it clear that *this action* produced *that result*.
- **Patterns:** Origin-anchored transitions (motion emanates from the trigger); connected enter/leave; directional movement that traces the causal link.

### 6. Guide attention (sequencing)
Lead the eye through a sequence in the right order.
- **Patterns:** Scroll-reveal in order; staggered lists; pinned/step-through sections (sparingly); spotlight/coach-marks.

### 7. Reduce perceived waiting
Make unavoidable waits feel shorter and less uncertain.
- **Patterns:** Skeleton screens; optimistic UI; progressive/streamed content; honest progress indicators; meaningful loading copy.
- **Note:** Never fake progress; reducing *perceived* wait must not mean *misrepresenting* it.

### 8. Confirm completion
Tell the user an action succeeded.
- **Patterns:** Brief success animation; checkmark/state change; toast confirmation; inline saved indicator.
- **Note:** Scale celebration to frequency and stakes — no confetti on routine actions.

### 9. Prevent errors
Stop mistakes before they happen, or make them recoverable.
- **Patterns:** Inline validation; confirmation dialogs for destructive actions; disabled→enabled affordance; undo windows; drag drop-target highlighting.

### 10. Strengthen affordance
Make it obvious what is interactive and how it responds.
- **Patterns:** Hover/focus/press states; cursor-appropriate feedback; tilt/magnetism (light, on rich UI); drag handles; clear focus rings.

### 11. Improve discoverability
Help users find features and actions they didn't know existed.
- **Patterns:** Command palette; subtle hover reveals; onboarding spotlights; empty-state prompts; progressive disclosure.

### 12. Create emotional impact
Make the experience feel crafted, branded, memorable.
- **Patterns:** Signature entrance/hero motion; expressive backgrounds (auroras/beams/particles); kinetic typography; scroll storytelling; 3D/WebGL set-pieces.
- **Note:** Licensed mainly on websites and immersive experiences; in applications, emotional impact comes from *speed and polish*, not spectacle.

---

## Problem → pattern → effect, in practice

1. **Name the objective** from the list above (driven by LEVEL 3 intent + LEVEL 4 screen).
2. **Pick a pattern** that solves it. Multiple objectives may share patterns — prefer one pattern that serves several.
3. **Choose the minimal effect** that implements the pattern, honouring the
   implementation order and penalties in `../selection-policies/`.
4. **Check anti-patterns** (`../anti-patterns/`) — many tempting effects solve a
   *different* objective than the one you actually have.

The objective, not the effect, is the unit of decision. If you cannot state
which objective an animation serves, it is decoration — and decoration is the
first thing Motif removes.
