# E-commerce, Product Page & Add-to-Cart Feedback

A worked example from **Motif**. PATTERNS before
EFFECTS; browser-native first; accessibility and reduced-motion mandatory.

## Context
- **Product type:** Online store product detail page (PDP).
- **Page/screen:** Product imagery, price, variant selectors, Add to Cart, and a cart
  indicator in the header.
- **Target user:** A shopper deciding whether to buy; mixed devices, often mobile.
- **Primary task:** Choose a variant and add to cart with **confidence** it worked, then
  keep shopping or check out. Conversion clarity beats spectacle.

## User problem
After tapping Add to Cart, nothing clearly confirms success, so shoppers tap again
(duplicate adds) or distrust the cart. A flashy redesign added a full-screen animation and
a flying-product arc that delayed the action and distracted from the price/CTA. We need
**subtle, unmistakable** add-to-cart feedback that never gets in the way of buying.

## Candidate approaches considered
1. **No feedback (current).** Causes double-adds and doubt. Rejected.
2. **Full-screen success animation / confetti per add.** Add-to-cart is frequent; confetti
   and takeovers interrupt the buying flow and annoy repeat shoppers. Rejected.
3. **Inline confirmation:** button transitions to "Added ✓" briefly, the header cart count
   updates with a small bump, plus a non-blocking toast offering "View cart." **Selected.**

## Selected pattern
**Inline action confirmation + cart-count update.** Confidence is delivered at the point of
action and reflected where the cart lives, no overlay, no detour.

## Selected effect/technique
Simplest that works, native first:
- **Button state:** Add to Cart → brief loading → "Added ✓" (~1.2s) → back to "Add to Cart".
  Disabled during the request to prevent double-submit.
- **Cart count:** the header badge updates and gives a single ~150ms scale "bump" (transform)
  so the eye is drawn to where the item went, spatial link between action and cart.
- **Toast:** a small, dismissible "Added to cart, View cart" with `role="status"`.

## Rejected effects (and why)
- **Confetti on every add**, confetti for a frequent action; trivializes and irritates.
- **Flying product arc to the cart**, decoration-only; delays the next action and is fragile
  across layouts/mobile.
- **Full-screen success modal**, blocks shopping; interrupts a routine, non-exceptional event.
- **Continuous pulsing CTA / animated price**, continuous motion behind the conversion point;
  reads as pushy and distracts from the actual price.

## Implementation sketch
Vue PDP; button reflects request state; cart badge bumps once; toast announces. CSS owns motion.

```vue
<script setup>
import { ref } from 'vue'
const status = ref('idle')   // 'idle' | 'loading' | 'added'
const cartCount = ref(0)
const bump = ref(false)

async function addToCart(variantId) {
  if (status.value === 'loading') return
  status.value = 'loading'
  try {
    await api.addToCart(variantId)
    cartCount.value++
    bump.value = true; setTimeout(() => (bump.value = false), 160)
    status.value = 'added'; setTimeout(() => (status.value = 'idle'), 1200)
    toast('Added to cart', { action: 'View cart' })
  } catch { status.value = 'idle'; toast('Could not add to cart, try again') }
}
</script>

<template>
  <button class="add" :disabled="status === 'loading'" @click="addToCart(selectedVariant)">
    <span v-if="status === 'loading'">Adding…</span>
    <span v-else-if="status === 'added'">Added ✓</span>
    <span v-else>Add to cart</span>
  </button>

  <span class="cart-badge" :class="{ bump }" aria-label="Items in cart">{{ cartCount }}</span>
  <span class="sr-only" role="status" aria-live="polite">
    {{ status === 'added' ? 'Item added to cart' : '' }}
  </span>
</template>

<style>
.cart-badge { transition: transform .15s ease; }
.cart-badge.bump { transform: scale(1.25); }
@media (prefers-reduced-motion: reduce) { .cart-badge { transition: none; } }
</style>
```

## Accessibility
- **Screen reader:** `role="status" aria-live="polite"` announces "Item added to cart" without
  stealing focus; the cart badge has an accessible label with the count.
- **Reduced motion:** the badge bump is removed; the **count change and "Added ✓" text** still
  confirm success, meaning is never motion-only.
- **Keyboard/focus:** button is keyboard-operable; focus stays on it after adding so a shopper
  can immediately add another or tab to "View cart" in the toast.
- **No double-submit:** disabled-while-loading protects assistive-tech and fast-tap users alike.

## Performance
- Animation limited to a single `transform` bump; button text swaps are free.
- No flying elements, no full-screen layers, no continuous motion near the CTA.
- Budget posture: PDP stays fast/conversion-focused; product images own the budget, not effects.

## Validation
- Add to cart → button shows Added ✓, badge increments and bumps once, toast appears.
- Rapid taps don't create duplicate adds (button disabled during request).
- Screen reader announces the add once; badge label reflects count.
- Reduce-motion → no bump, success still unmistakable via text + count.
