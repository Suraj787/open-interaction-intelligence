# Timeline, Progressive Disclosure & Scroll Reveal (not hijacking)

A worked example from **Motif**. PATTERNS before
EFFECTS; browser-native first; accessibility and reduced-motion mandatory.

## Context
- **Product type:** Content/marketing or in-app history timeline (e.g. company history,
  release log, audit/event trail).
- **Page/screen:** A vertical timeline with dated entries; some entries have detail that
  can be expanded.
- **Target user:** A reader skimming chronology, occasionally diving into one entry.
- **Primary task:** Scan the sequence, read selectively. The user must stay in control of
  scrolling at all times.

## User problem
A previous version pinned the timeline and **hijacked scroll**, wheel/trackpad gestures
drove a scripted animation instead of the page, so users couldn't skim, jump, or use
Find-in-page. We need entries to reveal pleasantly as they enter view, plus expandable
detail, **without ever taking over scroll**.

## Candidate approaches considered
1. **Scroll-jacked cinematic timeline** (pin section, intercept wheel, drive a scrubber).
   Demos well, fights the user constantly, breaks keyboard/Find/screen readers. Rejected.
2. **Everything visible, no motion, all details expanded.** Honest and accessible but a
   wall of text; hard to scan. Acceptable fallback, not ideal default.
3. **Native scroll + gentle reveal-on-enter (IntersectionObserver) + click/keyboard
   progressive disclosure** for entry details. Scroll stays 100% the browser's.
   **Selected.**

## Selected pattern
**Reveal-on-scroll + progressive disclosure**, layered on *native* scrolling. The page
scrolls normally; entries fade/rise once as they appear; details expand on demand.

## Selected effect/technique
Simplest that works, native first:
- **Reveal:** each entry starts at `opacity:0; translateY(12px)` and transitions to visible
  the first time it crosses an IntersectionObserver threshold. One-shot per entry.
- **Disclosure:** entry detail is a `<details>`/disclosure button toggling height/opacity
  (~180ms). Collapsed by default to keep the scan light.
- The wheel, scrollbar, keyboard and Find-in-page are never intercepted.

## Rejected effects (and why)
- **Scroll hijacking / pinned scrubber**, the headline anti-pattern: steals control,
  breaks accessibility and Find-in-page.
- **Parallax layers moving continuously as you scroll**, continuous motion behind dense
  text; distracting and costly.
- **Re-animating entries every time they re-enter view**, decoration-only repetition;
  jittery on scroll-up.
- **Confetti / sparkle on each entry**, pure decoration, no information.

## Implementation sketch
Browser-native IntersectionObserver + CSS; framework-agnostic (works as a Vue directive too).

```js
const io = new IntersectionObserver((entries) => {
  for (const e of entries) {
    if (e.isIntersecting) {
      e.target.classList.add('revealed')
      io.unobserve(e.target)          // one-shot: never re-animate
    }
  }
}, { threshold: 0.2, rootMargin: '0px 0px -10% 0px' })

document.querySelectorAll('.tl-entry').forEach(el => io.observe(el))
```
```css
.tl-entry { opacity: 0; transform: translateY(12px);
  transition: opacity .35s ease, transform .35s ease; }
.tl-entry.revealed { opacity: 1; transform: none; }

@media (prefers-reduced-motion: reduce) {
  .tl-entry { opacity: 1; transform: none; transition: none; }  /* visible, no motion */
}
```
```html
<details class="tl-detail"><summary>Details</summary> … </details>
```

## Accessibility
- **No scroll hijacking**, wheel, keyboard (PageUp/Down, Space, arrows), scrollbar and
  browser Find all behave normally.
- **Reduced motion:** entries render fully visible with no fade/slide; nothing depends on
  the animation having played.
- **JS-off / observer-unsupported:** entries default to visible (progressive enhancement), the `revealed` styles should be the *enhancement*, not a gate on content.
- **Disclosure:** native `<details>` (or button + `aria-expanded`) is keyboard-operable and
  announced; content is in the DOM for Find-in-page even when collapsed-but-rendered.

## Performance
- Animate only `opacity`/`transform`; one-shot reveal then `unobserve`, no ongoing work.
- No parallax, no continuous/offscreen motion.
- Budget posture: a single shared IntersectionObserver; no scroll-event listeners doing
  layout reads on every frame.

## Validation
- Try to "scroll past" fast, the page never resists; Find-in-page jumps anywhere.
- Scroll up/down repeatedly, entries don't re-animate or flicker.
- Reduce-motion / JS-disabled, all content present and readable.
- Keyboard-only, expand/collapse details and traverse the whole timeline.
