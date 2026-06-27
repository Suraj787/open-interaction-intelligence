# LEVEL 3 — User Intents

Once the product type is known (LEVEL 2), Motif asks: **what is this specific user
trying to do on this screen right now?** Intent is the bridge between *what the
product is* and *what interaction objective* (LEVEL 5) we must solve.

Each intent below maps to **motion implications**: what motion should do, and
where it must stay out of the way.

> Core principle: motion serves the intent. If an animation does not help the
> user accomplish what they came to do, it is a cost, not a feature.

---

### 1. Complete a task
The user wants to finish an action and move on (submit, approve, send, assign).
- **Motion implications:** Fast, confirming feedback. Sub-200ms acknowledgements. Clear, *brief* success states. Never block the next action with celebration. Reduce perceived waiting for any server round-trip.

### 2. Enter information
Filling forms, fields, structured data.
- **Motion implications:** Inline validation that appears calmly (not shaking aggressively). Smooth focus/affordance cues. Avoid motion that shifts fields under the cursor. Errors must use colour + text + icon, not motion alone.

### 3. Review information
Reading records, reports, details to understand state.
- **Motion implications:** Minimal motion. Preserve scan-ability and density. No entrance animations on data the user re-reads often. Motion only to orient (expand/collapse, drill-in continuity).

### 4. Compare options
Plans, products, configurations, variants side by side.
- **Motion implications:** Use motion to align and synchronise comparison views; highlight differences. Avoid motion that makes items hard to hold side-by-side or that staggers so comparison feels unstable.

### 5. Monitor status
Dashboards, queues, live ops, build/deploy states.
- **Motion implications:** Draw attention to *meaningful change* only. Subtle transitions on value updates. Avoid continuous animation (battery, distraction). Status must never be conveyed by motion alone.

### 6. Navigate
Moving between sections, records, or pages.
- **Motion implications:** Preserve spatial continuity. Shared-element / route transitions that show where you came from and where you are. Keep it fast; navigation motion that adds latency is friction.

### 7. Discover content
Browsing, exploring a catalogue, scanning a feed.
- **Motion implications:** Light reveal and hover affordances are welcome. Lazy-load without layout jank. Keep scanning fluid; avoid heavy staggered entrances that slow the browse.

### 8. Evaluate a product
Marketing/landing context — deciding whether something is worth it.
- **Motion implications:** Motion can demonstrate value and guide attention to proof and CTA. This is where expressiveness is licensed — but it must not delay the message or the call to action.

### 9. Purchase
Cart, checkout, payment, confirmation.
- **Motion implications:** Calm and trustworthy. Restrained motion. Clear, reassuring confirmation. Zero distraction near payment. No layout shift on totals. Reduce perceived waiting on processing without faking progress.

### 10. Learn
Docs, tutorials, onboarding, education.
- **Motion implications:** Motion to explain cause/effect and sequence (e.g. step-by-step reveals tied to user action, not auto-play). Never hide content from search/scan behind scroll triggers.

### 11. Collaborate
Co-editing, commenting, presence, shared boards.
- **Motion implications:** Subtle presence and live-update motion to show *who did what*. Smooth insertion of remote changes (preserve continuity, avoid jarring jumps). Keep notification motion low-noise.

### 12. Configure a system
Settings, admin, permissions, integrations.
- **Motion implications:** Predictable, reversible feedback. Make state changes obvious and confirm them. Avoid playful motion; this is a high-trust, low-frequency-but-high-stakes context. Strengthen affordance on toggles/switches.

---

## Intent × posture quick map

| Intent | Default motion posture |
|---|---|
| Complete a task | Restrained, fast feedback |
| Enter information | Restrained |
| Review information | Very restrained |
| Compare options | Restrained, synchronised |
| Monitor status | Very restrained, change-only |
| Navigate | Restrained, continuity-focused |
| Discover content | Balanced |
| Evaluate a product | Balanced → expressive |
| Purchase | Restrained near payment |
| Learn | Restrained, user-driven reveals |
| Collaborate | Balanced, presence-aware |
| Configure a system | Very restrained |

Intent narrows the field. The next level — **interaction problems**
(`../interaction-problems/`) — names the precise objective the chosen pattern
must solve.
