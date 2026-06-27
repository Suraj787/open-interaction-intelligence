# Corporate Website — Calm, Credible, Minimal Motion

A worked example from **Motif**. PATTERNS before
EFFECTS; browser-native first; accessibility and reduced-motion mandatory.

## Context
- **Product type:** Corporate / institutional website (e.g. enterprise vendor, financial
  or professional-services firm).
- **Page/screen:** Home and key marketing/info pages — value statement, proof points,
  navigation to products, careers, investor/legal.
- **Target user:** Prospects, partners, press, candidates, regulators — many of them
  evaluating **trustworthiness**.
- **Primary task:** Find information and judge credibility. Calm and clarity outrank flair.

## User problem
A redesign added trendy motion — animated hero loops, scroll-triggered everything, hover
effects on every card — which made a serious institution feel gimmicky and slowed the
site. We need a **calm, credible** presence: motion only where it aids comprehension or
feedback, accessibility-first, fast.

## Candidate approaches considered
1. **Motion-rich "modern agency" treatment.** On-trend but undermines credibility and
   performance for an institutional brand. Rejected.
2. **Absolutely zero interaction feedback.** Credible but feels inert/unresponsive; users
   miss affordances (e.g. which nav item is active). Too austere.
3. **Minimal, functional motion:** quiet hover/focus states, a brief content fade on route
   change, smooth in-page anchor scrolling — and nothing decorative. **Selected.**

## Selected pattern
**Calm functional feedback only.** Every animation answers "did my action register?" or
"where am I?" — never "look how lively we are."

## Selected effect/technique
Simplest that works, native first:
- **Hover/focus states:** subtle color/underline/elevation changes via CSS `transition`
  (~120ms) on links, buttons, nav. Feedback, not flourish.
- **Route/section change:** a brief ~150ms content opacity fade so navigation doesn't snap.
- **In-page anchors:** native `scroll-behavior: smooth` (respecting reduced motion).
- That is the entire motion vocabulary. Hierarchy comes from typography, spacing, contrast.

## Rejected effects (and why)
- **Animated hero loops / background video** — decoration; harms credibility and load time.
- **Scroll-triggered reveals on every section** — continuous, attention-grabbing motion the
  content doesn't need; can feel manipulative on an institutional site.
- **Hover animations on every card** — decoration-only; visual noise.
- **Confetti / parallax / marquees** — all gimmick, zero informational value here.

## Implementation sketch
Browser-native CSS does almost everything; a tiny fade on route change if it's an SPA.

```css
a, .btn, .nav__link { transition: color .12s ease, background-color .12s ease,
  box-shadow .12s ease; }
.nav__link[aria-current="page"] { font-weight: 600; border-bottom: 2px solid currentColor; }

html { scroll-behavior: smooth; }

/* SPA route fade (optional) */
.route-enter-active, .route-leave-active { transition: opacity .15s ease; }
.route-enter-from, .route-leave-to { opacity: 0; }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important;
    transition-duration: .01ms !important; scroll-behavior: auto !important; }
}
```

## Accessibility
- **Accessibility-first:** strong color contrast, visible focus rings, real headings and
  landmarks, descriptive links. Motion never carries meaning.
- **Reduced motion:** the global reset above neutralizes transitions and smooth scroll;
  current-page state stays conveyed by weight + `aria-current`, not motion.
- **Keyboard/focus:** full keyboard navigation; focus states are clearly visible and are the
  same affordance as hover.

## Performance
- Motion limited to short `color`/`opacity`/`box-shadow` transitions — negligible cost.
- No background media, no scroll listeners, no offscreen/continuous animation.
- Budget posture: fast first paint, minimal JS; the site should feel instant and solid.

## Validation
- Every interactive element has a visible hover **and** focus state.
- Reduce-motion → no animation, no smooth scroll; navigation/active-state still clear.
- No section animates merely because it scrolled into view.
- Lighthouse performance/accessibility both strong; no layout shift.
