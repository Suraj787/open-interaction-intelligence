# Motif Adapter — Angular

How Motif recipes map onto idiomatic Angular (standalone components, signals,
`DestroyRef`). Recipes stay CSS-first; Angular owns DI, change detection, and
deterministic teardown.

> Provenance: original (clean-room). No third-party source is copied.

## Idiomatic structure

Package a recipe as a **directive + (optional) component**:

- An **attribute directive** (`[oiiBlurReveal]`) is the idiomatic home for
  element-level observer wiring; inject `ElementRef`.
- A standalone component exposes knobs via `input()` signals and emits via
  `output()`.

Keep motion in component/`:host` CSS. Angular's `@angular/animations` is available
but **CSS-first is preferred** — only use the animations package for orchestration
it genuinely simplifies.

```ts
@Directive({ selector: '[oiiBlurReveal]', standalone: true })
export class BlurRevealDirective implements OnInit {
  intensity = input(1);
  // …observer wiring in ngOnInit, cleanup via DestroyRef
}
```

## Lifecycle handling

- `ngOnInit` / `afterNextRender` (v17+) to attach observers once the DOM exists;
  `afterNextRender` runs browser-only, which is ideal for SSR safety.
- Signals + `effect()` to react to knob changes.
- Run observer callbacks that update bindings inside `NgZone` (or use signals) so
  change detection fires; use `runOutsideAngular` for hot paths like `pointermove`.

## Cleanup

Use `DestroyRef` / `takeUntilDestroyed` — the modern, leak-proof pattern:

```ts
constructor() {
  const ref = inject(DestroyRef);
  const io = new IntersectionObserver(/* … */);
  io.observe(this.el.nativeElement);
  ref.onDestroy(() => io.disconnect()); // also abort listeners, cancel RAF
}
```

Always unsubscribe RxJS streams (`takeUntilDestroyed`) and disconnect observers.

## SSR

Angular Universal renders on the server. Guard browser APIs: inject `PLATFORM_ID`
and check `isPlatformBrowser`, or use `afterNextRender`/`afterRender` which only run
in the browser. Never touch `window`/`matchMedia`/`IntersectionObserver` during
construction or `ngOnInit` without that guard.

## Hydration

Angular's non-destructive hydration reuses server DOM. Don't produce different
markup on server vs client (no `window`-based branching in templates). Apply the
enhanced start state in `afterNextRender` or via CSS to avoid a hydration flash;
keep DOM structure stable so hydration doesn't re-render.

## Keyboard behaviour

- Use semantic elements and host `(keydown)` bindings; `@HostListener` for
  document-level keys with matching teardown.
- Don't remove focusability for animation.
- Use Angular CDK `A11yModule` (`FocusTrap`, `LiveAnnouncer`) for dialogs/menus and
  status messages; restore focus on close. Style `:focus-visible`.

## Pointer & coarse-pointer support

- Unify input via `(pointerdown)`/`(pointermove)` host bindings.
- Detect capability with `matchMedia` (wrapped in a service) and switch
  affordances; CDK `Platform` helps detect environment.
- Keep >=44px targets under `@media (pointer: coarse)`.

## Responsive behaviour

Prefer CSS media/container queries. For JS, CDK `BreakpointObserver` (or a
`matchMedia` service exposing signals) gives reactive breakpoints with managed
teardown.

## Reduced-motion strategy

Provide a `PrefersReducedMotion` service exposing a signal that tracks the media
query live. Components read it to skip `@angular/animations` transitions (or set
duration `0`) and jump to the end state. CDK respects an
`ANIMATION_MODULE_TYPE`/`NoopAnimations` option too. Always include the CSS
`@media (prefers-reduced-motion: reduce)` guard.

## Testing

- **TestBed + Jasmine/Karma** (or Jest) for component/directive behaviour and ARIA;
  CDK provides testing harnesses.
- Stub `IntersectionObserver`/`matchMedia` in the test setup.
- Assert `DestroyRef.onDestroy` cleanup runs (destroy the fixture, check spies).
- Playwright for reduced-motion / coarse-pointer E2E.

## Dependency trade-offs

`@angular/animations` and `@angular/cdk` are first-party and already in most Angular
apps — using them is not "adding a dependency" in the Motif sense. Still prefer CSS
for simple motion. Don't pull in third-party animation libs for effects CSS/WAAPI
cover; escalate only per the technique order.

## Normalised component contract knobs

| Knob                 | Angular surface                                         |
| -------------------- | ------------------------------------------------------- |
| class override       | `[class]` / `[ngClass]`                                 |
| style override       | `[style]`, `[style.--motif-*]` custom properties          |
| design tokens        | inherited CSS variables                                 |
| intensity            | `input<number>('intensity')`                            |
| duration             | `input('duration')`                                     |
| delay                | `input('delay')`                                        |
| easing               | `input('easing')`                                       |
| disable-animation    | `input<boolean>('disableAnimation')`                    |
| reduced-motion       | `reducedMotion` input + service signal                  |
| responsive controls  | media/container queries + `BreakpointObserver`          |
| accessible labels    | `aria-label`, `LiveAnnouncer`, `label` input            |
| event callbacks      | `output()` emitters (`reveal`, `stateChange`)           |
