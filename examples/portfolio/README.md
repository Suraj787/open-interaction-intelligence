# Portfolio, Expressive but Accessible

A worked example from **Motif**. PATTERNS before
EFFECTS; browser-native first; accessibility and reduced-motion mandatory.

## Context
- **Product type:** Personal/creative portfolio site (designer, developer, studio).
- **Page/screen:** Landing + project grid + case-study detail.
- **Target user:** Prospective clients/employers judging both the **work** and the maker's
  taste and craft, including whether they get the fundamentals (accessibility, performance) right.
- **Primary task:** Browse work, gauge quality, get in touch. Here, expressive motion is
  *on-brief*, but it must still degrade gracefully and never block content.

## User problem
Portfolios are where motion is most tempting and most often overdone, entrances on every
element, custom cursors, scroll-jacked storytelling, which ironically signals *poor*
judgement to discerning viewers and breaks on reduced-motion or slower devices. We want
**expressive, characterful motion that is also demonstrably accessible**, the craft flex
*is* doing both well.

## Candidate approaches considered
1. **Maximalist motion:** scroll-jacked narrative, custom cursor, animated everything.
   Impressive demo, hostile UX, fails reduced-motion. Rejected as default, it signals the
   wrong thing.
2. **No motion at all.** Safe but undersells a creative brand and wastes a legitimate canvas.
   Used as the reduced-motion baseline, not the default.
3. **Curated expressive motion:** a few signature moments, a staged hero reveal, project
   tiles that rise/scale subtly on hover/focus, image crossfades in case studies, all
   native-scroll, all with a first-class reduced-motion design. **Selected.**

## Selected pattern
**Curated signature moments + graceful degradation.** Motion is a deliberate accent in a few
places, not an ambient state everywhere, and the reduced-motion version is *designed*, not
an afterthought.

## Selected effect/technique
Simplest that works, native first:
- **Hero:** one staged entrance (name → tagline → featured work), ~250ms each, once on load.
- **Project tiles:** on hover/focus, a small `transform: scale/translateY` lift + image
  reveal (~180ms), expressive but cheap.
- **Case study:** image crossfades and reveal-on-enter (IntersectionObserver, one-shot) using
  native scrolling.
- A signature accent (e.g. an accent-color sweep on tile hover), kept to one motif.

## Rejected effects (and why)
- **Scroll hijacking / pinned narrative**, steals control, breaks keyboard/Find; the classic
  anti-pattern even creative sites should avoid.
- **Custom JS cursor with trailing animation**, continuous motion; hurts performance and
  accessibility, breaks on touch.
- **Entrance animation on literally every element**, decoration-only overload; dilutes the
  few moments that should land.
- **Autoplay audio/video backdrops**, heavy and intrusive.

## Implementation sketch
Native CSS for hero + hover; one-shot IntersectionObserver for case-study reveals.

```css
/* staged hero */
.hero > .reveal { opacity: 0; transform: translateY(14px);
  animation: rise .25s ease forwards; animation-delay: var(--d); }
@keyframes rise { to { opacity: 1; transform: none; } }

/* expressive but cheap project tile */
.tile { transition: transform .18s ease, box-shadow .18s ease; }
.tile:hover, .tile:focus-within { transform: translateY(-4px) scale(1.01);
  box-shadow: 0 10px 30px rgba(0,0,0,.18); }
.tile__img { transition: opacity .18s ease, transform .18s ease; }

/* case-study reveal-on-enter (one-shot, see timeline example for the JS) */
.cs-block { opacity: 0; transform: translateY(16px);
  transition: opacity .4s ease, transform .4s ease; }
.cs-block.revealed { opacity: 1; transform: none; }

@media (prefers-reduced-motion: reduce) {
  .hero > .reveal, .cs-block { opacity: 1; transform: none; animation: none; transition: none; }
  .tile { transition: none; }
  .tile:hover, .tile:focus-within { transform: none; box-shadow: 0 6px 18px rgba(0,0,0,.16); }
}
```

## Accessibility
- **Reduced motion is a designed state:** entrances/reveals show content immediately; the tile
  "lift" becomes a static elevation/outline change so hover/focus still reads. Nothing is lost.
- **Keyboard/focus:** tiles are links/buttons reachable by keyboard; `:focus-within` mirrors the
  hover treatment so keyboard users get the same affordance. Visible focus rings throughout.
- **No motion-only meaning:** project info (title, role, year) is real text; motion is accent only.
- **No scroll hijacking**, native scroll, Find-in-page works.

## Performance
- Animate only `opacity`/`transform`/`box-shadow`; reveals are one-shot then unobserved.
- No custom cursor loop, no autoplay media, no continuous/offscreen motion.
- Budget posture: images sized/lazy-loaded; the expressive moments are few and short, so the
  site still loads fast, itself part of the craft signal.

## Validation
- Reduce-motion → a deliberate, still-characterful static design (not a broken one).
- Keyboard-only browsing gets the same tile affordances as mouse; focus always visible.
- No scroll resistance; Find-in-page reaches all case-study text.
- Performance stays strong despite the expressive accents.
