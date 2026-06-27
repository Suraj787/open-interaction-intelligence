# LEVEL 2, Product Types

This is the first real branch of Motif. Before any
effect, pattern, or recipe is considered, the agent must classify the product.

The single most important distinction is:

- **Web application**, a tool people use repeatedly to *get work done*. The
  interface is a workspace. Motion exists to support tasks, feedback, and
  spatial continuity. Default posture is **restrained**.
- **Website**, a destination people visit to *learn, evaluate, or be
  persuaded*. The interface is a message. Motion can carry brand and narrative.
  Default posture ranges from **balanced to expressive**.

> Rule of thumb: if the same person opens it five times a day, treat it as an
> application and protect their attention. If most visitors arrive once, you
> have more room to express, but never at the cost of comprehension or speed.

Each entry below gives: **user intent**, **motion posture** (on a
restrained → expressive scale), and **key risks**.

---

## Web applications

### Enterprise app (generic internal tool)
- **User intent:** Complete repeated operational tasks accurately and fast.
- **Motion posture:** Restrained. Motion only for feedback, state change, and continuity.
- **Key risks:** Decorative motion that slows power users; animations that replay on every visit; ignoring keyboard-first workflows.

### ERP
- **User intent:** Record and reconcile transactions across many linked entities; trust the numbers.
- **Motion posture:** Very restrained. Density and correctness dominate.
- **Key risks:** Animated number counters on financial figures (reads as imprecise); transitions that hide whether a save committed; layout jank in dense tables.

### CRM
- **User intent:** Track relationships, move deals through stages, log activity quickly.
- **Motion posture:** Restrained, with light expressiveness on pipeline/kanban moves.
- **Key risks:** Over-celebrating routine stage changes; reordering animations that lose the dragged card's position; notification motion that distracts from calls.

### Project management
- **User intent:** Plan, assign, and track work; see status at a glance.
- **Motion posture:** Restrained-to-balanced. Spatial continuity on board/list/timeline switches is valuable.
- **Key risks:** Confetti on every completed task; drag reorders that jank; view-switch transitions that disorient rather than orient.

### Financial app
- **User intent:** Make money decisions with confidence; verify amounts.
- **Motion posture:** Very restrained. Precision and trust above all.
- **Key risks:** Counters/odometers on balances; flashy charts that obscure values; any motion implying a change that did not actually persist.

### Analytics dashboard
- **User intent:** Monitor metrics and spot anomalies quickly.
- **Motion posture:** Restrained. Motion to draw the eye to a *meaningful* change only.
- **Key risks:** Continuously animating charts (CPU/battery + distraction); decorative data entrance animations on every refresh; motion-only status with no text/colour backup.

### Collaboration app
- **User intent:** Co-create and communicate with others in near real-time.
- **Motion posture:** Balanced. Presence and live updates benefit from subtle motion.
- **Key risks:** Distracting presence/typing animations; jarring insertion of remote edits; notification noise.

### Consumer SaaS
- **User intent:** Accomplish a personal task pleasantly and return often.
- **Motion posture:** Balanced. A little delight is welcome; the work still comes first.
- **Key risks:** Delight that becomes friction on repeat use; long onboarding animations; entrance animation on frequently-seen screens.

### AI app (chat / agent / generative)
- **User intent:** Get a useful generated result and understand what the system is doing.
- **Motion posture:** Balanced. Motion communicates "thinking", streaming, and provenance.
- **Key risks:** Fake/indeterminate loaders that misrepresent progress; streaming text so animated it's hard to read; hiding tool/agent steps behind decoration.

### Developer tool
- **User intent:** Work fast, precisely, often keyboard-driven.
- **Motion posture:** Very restrained. Speed and predictability win.
- **Key risks:** Any animation that adds latency to a command; custom cursors; transitions that block input; motion over information density.

### Marketplace (app side)
- **User intent:** Browse, compare, transact, and manage listings/orders.
- **Motion posture:** Balanced. Browsing can be lively; checkout must be calm and clear.
- **Key risks:** Distracting motion during checkout; layout shift while images load; over-animated cards that slow scanning.

### Creative tool (design / video / audio editors)
- **User intent:** Manipulate a canvas with direct, predictable control.
- **Motion posture:** Restrained chrome, **responsive** canvas. The canvas must feel direct; the UI around it stays quiet.
- **Key risks:** Easing on direct-manipulation handles (feels laggy); decorative panel animations; motion competing with the user's own content.

---

## Websites

### Corporate / brand site
- **User intent:** Understand who the company is and trust it.
- **Motion posture:** Balanced. Polished, confident, never gimmicky.
- **Key risks:** Scroll hijacking on the homepage; heavy hero animations that delay content; motion that reads as style-over-substance.

### SaaS marketing site
- **User intent:** Evaluate a product and decide to sign up / book a demo.
- **Motion posture:** Balanced-to-expressive. Motion can demonstrate the product.
- **Key risks:** Endless scroll-jacked feature reveals; animation that delays the CTA; demos that loop distractingly near forms.

### Product-launch / campaign page
- **User intent:** Get excited about one thing and act now.
- **Motion posture:** Expressive. This is where bold motion earns its place.
- **Key risks:** Spectacle that buries the offer/CTA; performance collapse on mobile; no reduced-motion fallback.

### E-commerce
- **User intent:** Find a product, trust it, and buy with minimal friction.
- **Motion posture:** Balanced browsing, **restrained** at cart/checkout.
- **Key risks:** Layout jank as images/prices load; motion that delays add-to-cart; distracting effects during checkout (kills conversion).

### Documentation
- **User intent:** Find an answer and apply it; reduce cognitive load.
- **Motion posture:** Calm / very restrained. Motion only to aid orientation (e.g. collapsing nav).
- **Key risks:** Scroll-triggered reveals that hide content from search/scan; animated code blocks; anything slowing the reader.

### Editorial / publication
- **User intent:** Read and stay engaged through a story.
- **Motion posture:** Restrained body, **expressive set-pieces** where the narrative calls for it.
- **Key risks:** Scroll hijacking that traps the reader; motion that interrupts reading flow; heavy assets on article load.

### Event site
- **User intent:** Learn what/when/where and register.
- **Motion posture:** Balanced-to-expressive. Energy is on-brand; logistics must stay legible.
- **Key risks:** Hiding date/venue/register behind animation; countdowns that distract; performance on mobile in poor venue connectivity.

### Agency site
- **User intent:** Judge craft and capability; decide to make contact.
- **Motion posture:** Expressive. The site *is* the portfolio of craft.
- **Key risks:** Showing off at the expense of usability; broken/janky "impressive" effects; contact path buried under spectacle.

### Portfolio
- **User intent:** Assess an individual's work and taste; reach out.
- **Motion posture:** Expressive, but intentional. Signature motion is the point.
- **Key risks:** Novelty over navigability; work samples slow to appear; no reduced-motion or mobile story.

### Immersive / experiential
- **User intent:** Be moved by an experience.
- **Motion posture:** Most expressive. WebGL/3D/canvas are legitimate here.
- **Key risks:** Excludes low-power devices; accessibility and reduced-motion become hard requirements, not afterthoughts; long load with no graceful fallback.

---

## How this level feeds the rest of Motif

The product type sets a **default motion posture** and a **starting quality
profile** (see `../quality-profiles/`). Later levels (page type, user intent,
interaction problem) refine it, but they should rarely *override* an
application's restraint without an explicit reason. When in doubt, inherit the
more conservative posture and let evidence justify more expression.
