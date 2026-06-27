# Motion & Interaction Anti-Patterns

Catalogue of motion and interaction anti-patterns the engine flags. Each entry states **what it is**, **why it is harmful**, and the **better alternative**. These are scored against the motion grammars (`../motion/`) and state requirements (`../states/`).

---

## 1. Decoration-only animation
**What:** Movement added purely for "polish" that conveys no state, change, or relationship — spinning icons, drifting blobs, hover wiggles inside dense work tools.
**Why harmful:** Adds cognitive load and visual noise, competes with real signals, and costs CPU/GPU and battery for zero information. In data-heavy screens it actively slows expert users.
**Better:** Reserve motion for communicating change (entrance, exit, status, reflow). If an animation can be removed without losing meaning, remove it. Keep ornamental motion to marketing zones only and pause it offscreen.

## 2. Scroll hijacking
**What:** Overriding native scroll — scroll-jacking to snap sections, intercepting wheel/trackpad to drive a custom animation, or trapping the user in a "scrollytelling" segment.
**Why harmful:** Breaks the user's mental model and muscle memory, defeats find-in-page and keyboard scrolling, causes motion sickness, and disproportionately harms assistive-tech and trackpad users.
**Better:** Respect native scroll position and velocity. Trigger reveals from scroll position without seizing control. Anything that pins must remain escapable and keyboard-scrollable.

## 3. Motion-only status communication
**What:** Signalling success/error/change with animation or colour alone — a pulse, a flash, a colour swap — and nothing else.
**Why harmful:** Invisible to users with reduced motion enabled, to colour-blind users, and to screen-reader users. The information is lost the instant the animation ends or for anyone who looked away.
**Better:** Always pair a change with a persistent, text/icon cue and a programmatic status message (`aria-live`). Motion may emphasise, never carry, the meaning. (Enforced by the `status_change` rule in every motion grammar.)

## 4. Confetti / celebration for frequent actions
**What:** Firing a celebratory burst (confetti, fireworks, big check animation) on routine, repeated actions — every save, every row added, every message sent.
**Why harmful:** Celebration that fires constantly becomes noise, delays the user from their next action, and trivialises genuine milestones. It is also expensive and distracting.
**Better:** Reserve one-shot celebration for rare, meaningful milestones (onboarding complete, first project shipped). Routine success gets a quiet, persistent confirmation (toast, inline check) instead.

## 5. Infinite / looping motion in work areas
**What:** Perpetually animating elements — pulsing dots, shimmering gradients, breathing buttons, endless carousels — inside primary working surfaces.
**Why harmful:** Continuous motion is a known accessibility hazard (vestibular triggers), draws the eye away from the task indefinitely, and never lets attention settle. WCAG 2.2.2 requires a mechanism to pause/stop/hide.
**Better:** Use finite, one-shot transitions. If something must loop (a genuine indeterminate loader), keep it small, steady, bounded to the loading period, and give it a static reduced-motion form.

## 6. Forced custom cursor
**What:** Replacing the system cursor with a custom graphic, trailing dot, or magnetic blob across the whole site.
**Why harmful:** Adds latency between intent and feedback, hides the real hit target, breaks precision, ignores OS cursor-size/contrast accessibility settings, and is meaningless on touch.
**Better:** Keep the native cursor. Communicate affordance through the element (hover, focus, `cursor: pointer`) not by hijacking the pointer itself.

## 7. Fake / fabricated loading
**What:** Artificial delays or fake progress bars that do not reflect real work — a spinner shown after data already arrived, a bar that fills on a timer, a skeleton kept up "to feel substantial."
**Why harmful:** Wastes the user's time deliberately, erodes trust when noticed, and decouples feedback from reality so genuine slowness is indistinguishable from theatre.
**Better:** Show loading only while real work is pending. Use determinate progress only when you can measure it; otherwise an honest indeterminate indicator. Render instantly when data is already available (and delay skeletons ~150–200ms to avoid flashes).

## 8. No reduced-motion fallback
**What:** Shipping transitions, parallax, or autoplay that ignore `prefers-reduced-motion`.
**Why harmful:** Triggers nausea, dizziness, and migraines for users with vestibular disorders, and violates WCAG. It is the most common and most serious motion-accessibility failure.
**Better:** Every motion grammar here defines a `reduced_motion` path: translate/scale/parallax/loop are removed and transitions collapse to an instant or single fast fade. Honour the OS setting globally and test with it on.

## 9. Disorienting / oversized transitions
**What:** Large-distance flies-across-screen, full-page zoom-and-spin, or 600ms+ transitions on routine route changes.
**Why harmful:** Long, big-travel motion delays the user, induces motion discomfort, and makes a fast app feel slow. Repeated dozens of times a day it is pure friction.
**Better:** Keep operational transitions short (≤240ms) and small-travel. Save longer, expressive choreography for first-impression marketing surfaces, never the daily workflow.

## 10. Animation that blocks interaction
**What:** Forcing the user to wait for an entrance/exit animation to finish before they can click, type, or dismiss.
**Why harmful:** Subordinates the user to the animation, making the interface feel unresponsive and disrespecting power users who already know what they want.
**Better:** Make UI interactive immediately; let motion be interruptible. A click during an entrance should land; a second open should not queue behind a closing animation.

## 11. Hover-dependent actions on touch
**What:** Putting essential actions or information behind hover-only reveals (menus that only appear on `:hover`, tooltips with no focus/tap path).
**Why harmful:** Hover does not exist on touch devices and is unreliable for keyboard users, so the action becomes unreachable.
**Better:** Provide tap and focus equivalents for every hover affordance (see the `touch` and `coarse-pointer` conditional states across `../states/`).

## 12. Autoplaying media with motion
**What:** Auto-playing video, animated heroes, or carousels that move on their own without user intent.
**Why harmful:** Steals attention and bandwidth, is a vestibular and distraction hazard, and can violate WCAG 2.2.2 when it runs longer than 5s with no control.
**Better:** Default to paused/poster, give explicit play controls, respect reduced-motion (show a static frame), and never auto-advance a carousel without an obvious pause.
