# SaaS Website, Premium Hero That Explains the Product

A worked example from **Motif**. PATTERNS before
EFFECTS; browser-native first; accessibility and reduced-motion mandatory.

## Context
- **Product type:** Marketing site for a SaaS product.
- **Page/screen:** Above-the-fold hero, headline, subhead, primary CTA, and a product
  visual.
- **Target user:** A prospect deciding in seconds whether this is worth their time.
- **Primary task:** Understand *what the product does* and click the CTA. Conversion
  clarity and load speed beat spectacle.

## User problem
> "Make this hero feel premium and explain the product."

The brief invites over-design. The real job: convey quality and communicate the value
prop **fast**, without an effects pile-up that delays the headline, hurts LCP, or buries
the CTA. We want exactly **one** controlled ambient effect plus a tasteful staged reveal
of the text and product visual.

## Candidate approaches considered
1. **Big autoplay background video + parallax layers + animated counters.** Reads
   "premium" for a second, wrecks LCP/CLS, distracts from the CTA, fails reduced-motion.
   Rejected.
2. **Static hero, zero motion.** Fast and safe but the brief asked for premium feel and a
   guided reveal; acceptable as the reduced-motion baseline, not the default.
3. **One restrained ambient effect** (a slow, GPU-cheap gradient sheen *or* a subtle
   product-shadow lift) **+ a short staged entrance** of headline → subhead → CTA →
   product image. **Selected.**

## Selected pattern
**Staged entrance + a single ambient accent.** Hierarchy leads the eye headline-first to
the CTA; the ambient touch signals craft without competing with the message.

## Selected effect/technique
Simplest that works, native first:
- **Staged reveal:** headline, subhead, CTA, then product visual fade/rise in sequence,
  each ~250ms with ~80ms stagger, completes in well under a second, once, on load.
- **One ambient effect:** a slow, low-contrast gradient sheen drifting across the product
  card (CSS `@keyframes` on `background-position`/`transform`, long duration, low
  amplitude), *or* a gentle hover-lift on the product card. Pick **one**.
- Headline is real text rendered immediately (good LCP); animation is opacity-only on top.

## Rejected effects (and why)
- **Autoplay background video**, heavy LCP/bandwidth cost; competes with the message.
- **Parallax scroll layers**, continuous motion + jank; distracts from the value prop.
- **Animated stat counters**, decoration-only; delays reading the actual numbers.
- **Multiple simultaneous ambient effects**, an "animation showcase"; dilutes premium feel
  and conversion focus. Strictly one.

## Implementation sketch
Browser-native CSS staged reveal (no JS needed for the entrance); optional one ambient loop.

```html
<section class="hero">
  <h1 class="reveal" style="--d:0ms">Ship support workflows in a day</h1>
  <p  class="reveal" style="--d:80ms">A help desk your team actually enjoys using.</p>
  <a  class="reveal cta" style="--d:160ms" href="/signup">Start free</a>
  <figure class="reveal product" style="--d:240ms"><img src="/app.webp" alt="Product dashboard" /></figure>
</section>
```
```css
.reveal { opacity: 0; transform: translateY(12px);
  animation: rise .25s ease forwards; animation-delay: var(--d); }
@keyframes rise { to { opacity: 1; transform: none; } }

/* the ONE ambient effect: slow, cheap sheen on the product card */
.product { position: relative; overflow: hidden; }
.product::after { content:""; position:absolute; inset:0;
  background: linear-gradient(110deg, transparent 40%, rgba(255,255,255,.12) 50%, transparent 60%);
  transform: translateX(-30%); animation: sheen 8s ease-in-out infinite; }
@keyframes sheen { 50% { transform: translateX(30%); } }

@media (prefers-reduced-motion: reduce) {
  .reveal { opacity: 1; transform: none; animation: none; }
  .product::after { animation: none; display: none; }   /* no ambient motion */
}
```

## Accessibility
- **Reduced motion:** the staged reveal renders content immediately (no transform) and the
  ambient sheen is disabled, the hero is fully premium-static.
- **No motion-only meaning:** all value-prop info is in real text/markup; nothing depends on
  the animation playing.
- **Keyboard/focus:** CTA is a real focusable link, reachable first; no animation blocks
  interaction. The product `<img>` has descriptive `alt`.

## Performance
- Headline is server-rendered text → strong **LCP**; reveal is `opacity`/`transform` only.
- The single ambient loop is low-amplitude `transform` on a small element; pause/disable it
  when offscreen or under reduced motion. **No** video, no parallax, no per-scroll work.
- Budget posture: hero ships within performance budget; image is `webp`/sized; effect count = 1.

## Validation
- Lighthouse: good LCP/CLS; hero text paints before any animation.
- The CTA is obvious and reachable within the first second.
- Reduce-motion → static premium hero, message intact.
- Confirm only one ambient effect exists and it stops when offscreen.
