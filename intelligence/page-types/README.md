# LEVEL 4, Page & Section Types

LEVEL 2 sets the product. LEVEL 3 sets the user's intent. This level names the
**screen or section** in front of the user and states, for each, the
**dominant interaction objective** and the **recommended / avoided motion**.

Two families: **web-app screens** (workspaces) and **website sections**
(messages). The split mirrors LEVEL 2: app screens default restrained; website
sections have more licence to express.

---

## Web-app screens

### Login / authentication
- **Objective:** Get the right user in quickly and securely.
- **Recommended:** Calm focus transitions; gentle inline validation; subtle loading on submit.
- **Avoid:** Elaborate hero animation; shaking error fields; anything that delays the credential entry.

### Onboarding
- **Objective:** Get the user to first value with minimal friction.
- **Recommended:** Progressive disclosure; step continuity; light, *one-time* delight at completion.
- **Avoid:** Long auto-playing sequences; motion that can't be skipped; replaying on every login.

### Dashboard / overview
- **Objective:** Convey current status at a glance.
- **Recommended:** Subtle transitions on value change; skeletons while loading; draw attention to anomalies.
- **Avoid:** Continuously animating widgets/charts; entrance animation on every refresh; motion-only status.

### List view
- **Objective:** Scan, filter, and select among many items.
- **Recommended:** Smooth filter/sort transitions; gentle item enter/leave; preserve scroll position.
- **Avoid:** Heavy staggered entrances; layout jank as rows load; reorder animations that lose selection.

### Table / data grid
- **Objective:** Read and compare dense structured data accurately.
- **Recommended:** Sticky headers; calm row highlight; smooth column resize; pagination continuity.
- **Avoid:** Animated cell values; row entrance animations; anything reducing density or scan speed.

### Form
- **Objective:** Capture accurate input with low effort.
- **Recommended:** Smooth focus/affordance cues; calm inline validation; clear progress on multi-step.
- **Avoid:** Fields shifting under the cursor; aggressive error shakes; motion-only validation.

### Record / detail view
- **Objective:** Understand one entity fully; act on it.
- **Recommended:** Shared-element continuity from list → detail; expand/collapse for sections; clear save feedback.
- **Avoid:** Re-animating the whole record on each visit; hiding key fields behind scroll reveals.

### Kanban board
- **Objective:** Move work through stages; see WIP at a glance.
- **Recommended:** Smooth drag, clear drop targets, layout/position continuity on reorder; subtle stage-change confirm.
- **Avoid:** Confetti on routine moves; cards that jump or lose place; janky column reflow.

### Timeline
- **Objective:** Understand sequence and chronology.
- **Recommended:** Smooth scroll/zoom; continuity when expanding an entry; reveal tied to user action.
- **Avoid:** Auto-scrolling spectacle; heavy parallax; motion that obscures dates/order.

### Calendar
- **Objective:** See and manage time-based events.
- **Recommended:** Smooth view switches (day/week/month) with continuity; calm event create/move feedback.
- **Avoid:** Disorienting view transitions; animated event entrances on every render.

### Command palette
- **Objective:** Reach any action fast, keyboard-first.
- **Recommended:** Instant open; quick fade/scale; smooth result list updates. Speed is the feature.
- **Avoid:** Slow open animation; transitions that delay typing or selection.

### Settings
- **Objective:** Find and change configuration confidently.
- **Recommended:** Predictable toggle/switch feedback; clear saved-state confirmation; smooth section nav.
- **Avoid:** Playful motion; ambiguous save states; motion implying a change that didn't persist.

### Notifications
- **Objective:** Inform without derailing the current task.
- **Recommended:** Gentle slide/fade in and out; stacking that's easy to scan; auto-dismiss with control.
- **Avoid:** Attention-grabbing motion for low-priority items; noisy continuous animation.

### Empty state
- **Objective:** Explain what goes here and prompt the first action.
- **Recommended:** Simple, friendly; a single clear CTA; minimal one-time motion.
- **Avoid:** Elaborate illustrations animating on every visit.

### Loading state
- **Objective:** Reassure that progress is happening; reduce perceived wait.
- **Recommended:** Skeletons matching final layout; honest progress where measurable; subtle shimmer.
- **Avoid:** Fake/indeterminate progress that misrepresents; spinners that never resolve context; layout shift on load.

### Error state
- **Objective:** Explain what went wrong and how to recover.
- **Recommended:** Calm, clear messaging; colour + text + icon; obvious recovery action.
- **Avoid:** Aggressive shaking; motion-only error signalling; blocking animations.

### Confirmation state
- **Objective:** Confirm an action completed (or ask before a risky one).
- **Recommended:** Brief, clear success acknowledgement; for destructive actions, a calm deliberate dialog.
- **Avoid:** Long celebration on routine actions; confetti on frequent tasks; dismissable-too-fast confirmations.

---

## Website sections

### Hero
- **Objective:** Communicate the core value proposition in seconds.
- **Recommended:** A confident entrance; one focal motion; fast path to content/CTA.
- **Avoid:** Long load before the headline appears; scroll hijacking; motion that obscures the value prop.

### Product demo
- **Objective:** Show the product working.
- **Recommended:** Purposeful motion that demonstrates real behaviour; user-controllable where possible.
- **Avoid:** Distracting loops near forms/CTAs; demos that misrepresent the product; heavy assets blocking the page.

### Features
- **Objective:** Explain what it does and why it matters.
- **Recommended:** Reveal-on-scroll in modest, accessible doses; cause/effect motion linking feature to benefit.
- **Avoid:** Every feature scroll-jacked; staggered entrances so slow the page feels broken.

### Social proof (logos / stats)
- **Objective:** Establish credibility quickly.
- **Recommended:** Subtle entrance; a single, honest count-up on a key stat is acceptable here.
- **Avoid:** Endless logo marquees that distract; counters on every number.

### Testimonials
- **Objective:** Build trust through real voices.
- **Recommended:** Calm carousel or grid; gentle transitions; readable at rest.
- **Avoid:** Auto-advancing too fast to read; flashy quote animations.

### Pricing
- **Objective:** Help the visitor choose a plan with confidence.
- **Recommended:** Smooth monthly/annual toggle; clear highlight of recommended plan; synchronised comparison.
- **Avoid:** Motion that obscures prices; distracting effects near the buy button; layout shift on toggle.

### Comparison
- **Objective:** Show how options differ.
- **Recommended:** Aligned, synchronised reveal; highlight differences; keep columns stable.
- **Avoid:** Staggering that makes side-by-side reading unstable.

### Case study
- **Objective:** Prove outcomes with a narrative.
- **Recommended:** Story-driven reveals tied to scroll position; expressive set-pieces for key results.
- **Avoid:** Scroll-jacking that traps the reader; motion burying the numbers.

### FAQ
- **Objective:** Answer objections and reduce support friction.
- **Recommended:** Smooth accordion expand/collapse; keep content searchable.
- **Avoid:** Hiding answers from page search behind heavy JS; jarring expand jumps.

### CTA section
- **Objective:** Convert, get the click.
- **Recommended:** Draw attention to the action; strengthen the button's affordance; calm surroundings.
- **Avoid:** Competing animations stealing focus; motion that delays the click.

### Navigation
- **Objective:** Let visitors get anywhere fast.
- **Recommended:** Smooth menu open/close; clear current location; sticky behaviour that doesn't jank.
- **Avoid:** Hiding essential links behind clever motion; mega-menus that lag; custom cursors.

### Footer
- **Objective:** Provide wayfinding, legal, and contact info.
- **Recommended:** Static and reliable; at most a gentle entrance.
- **Avoid:** Animation on dense link lists; anything that delays access to contact/legal.

---

Page type narrows recommended motion to a short list. The exact objective the
chosen motion must serve is enumerated in **interaction problems**
(`../interaction-problems/`), and the final ranking happens in
**selection policies** (`../selection-policies/`).
