# Documentation Site, Documentation-Calm Profile

A worked example from **Motif**. PATTERNS before
EFFECTS; browser-native first; accessibility and reduced-motion mandatory.

## Context
- **Product type:** Technical documentation site (API/product docs, guides, reference).
- **Page/screen:** Doc page with left nav (tree), main content, right-hand on-page TOC,
  search, and code blocks.
- **Target user:** Developers and technical users, often mid-task, scanning for a specific
  answer, frequently arriving from search with a deep link.
- **Primary task:** Find and read the right information **fast**, copy code, navigate
  between pages. Readability and navigation feedback are everything; decoration is a liability.

## User problem
A previous theme added reveal-on-scroll to paragraphs, animated the sidebar, and used a
slow page-transition, all of which slow reading, delay code from appearing, and fight a
user who is scanning and using Find-in-page. Docs need a **near-zero decorative motion**
profile: motion only for genuine navigation/interaction feedback.

## Candidate approaches considered
1. **Marketing-style animated docs** (scroll reveals, animated nav, page transitions).
   Actively harms the core task: reading and scanning. Rejected.
2. **Zero motion whatsoever.** Mostly right, but a few tiny feedback cues (copy-confirmed,
   active-section in TOC) genuinely help and shouldn't be sacrificed. Slightly too strict.
3. **Documentation-calm:** no decorative animation at all; keep only functional micro-
   feedback, "Copied ✓" on code blocks, active-heading highlight in the TOC, expand/collapse
   for nav sections, smooth in-page anchor scroll (reduced-motion-aware). **Selected.**

## Selected pattern
**Functional navigation feedback only.** The page should feel instant. The only motion is the
minimum needed to confirm an interaction or show position in the document.

## Selected effect/technique
Simplest that works, native first:
- **Copy code:** button flips to "Copied ✓" for ~1.2s (text swap; no animation required).
- **TOC active section:** the current heading highlights as you scroll (IntersectionObserver
  toggling a class, a color/weight change, **no** movement).
- **Nav tree expand/collapse:** native `<details>` or a height toggle; instant or ≤120ms.
- **In-page anchors:** native `scroll-behavior: smooth`, disabled under reduced motion.
- Content paints immediately; **nothing** about the text reveal is animated.

## Rejected effects (and why)
- **Reveal-on-scroll for body text**, decoration that *delays reading*; the cardinal sin for docs.
- **Animated/sliding sidebar or page transitions**, adds latency to navigation between pages.
- **Continuous motion (gradients, spinners) behind content**, continuous motion behind dense
  text; harms legibility and battery.
- **Confetti / flourish on copy**, confetti for a frequent action; pure noise.

## Implementation sketch
Browser-native throughout; a tiny copy handler and a TOC observer. Works in any framework.

```js
// Copy button, text feedback, no animation
btn.addEventListener('click', async () => {
  await navigator.clipboard.writeText(codeEl.innerText)
  const prev = btn.textContent
  btn.textContent = 'Copied ✓'
  setTimeout(() => (btn.textContent = prev), 1200)
})

// TOC active-heading highlight, color/weight only, no movement
const io = new IntersectionObserver((entries) => {
  for (const e of entries) {
    const link = tocLinks.get(e.target.id)
    if (e.isIntersecting) link?.setAttribute('aria-current', 'true')
    else link?.removeAttribute('aria-current')
  }
}, { rootMargin: '0px 0px -70% 0px' })
document.querySelectorAll('h2[id], h3[id]').forEach(h => io.observe(h))
```
```css
.toc a { transition: color .1s ease; }
.toc a[aria-current="true"] { color: var(--accent); font-weight: 600; }
html { scroll-behavior: smooth; }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important;
    transition-duration: .01ms !important; scroll-behavior: auto !important; }
}
```

## Accessibility
- **Reduced motion:** global reset disables smooth scroll and the few transitions; active-TOC
  state is conveyed by `aria-current` + color/weight (no motion-only meaning).
- **Keyboard/focus:** nav tree, search, copy buttons, and anchors are all keyboard-operable;
  focus is visible; deep links land with the target heading focused/positioned.
- **Find-in-page:** all content is in the DOM and never gated behind a scroll animation.
- **Copy feedback** is a text change, readable by screen readers (or wrap in `role="status"`).

## Performance
- Effectively no animation cost; a single IntersectionObserver, no scroll-handler layout reads.
- No offscreen/continuous motion; code and prose paint immediately.
- Budget posture: docs should be among the fastest pages in the org, motion never competes
  with content paint or interactivity.

## Validation
- Body text appears instantly with no scroll-reveal; Find-in-page reaches everything.
- Copy shows "Copied ✓" and reverts; TOC highlights the section in view without moving.
- Reduce-motion → no smooth scroll, no transitions; navigation cues still clear.
- Navigating between pages feels instant (no page-transition animation).
