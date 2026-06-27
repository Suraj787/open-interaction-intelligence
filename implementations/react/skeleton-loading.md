# Skeleton Loading, React

Placeholder blocks with a left-to-right shimmer that occupy the layout while content
loads, then swap to the real children. Dependency-free; the shimmer is a CSS gradient
animated via `background-position` (no layout cost), and it disables itself under
`prefers-reduced-motion`.

File: [`SkeletonLoader.tsx`](./SkeletonLoader.tsx). Exports `SkeletonLoader`
(region wrapper) and `Skeleton` (single block).

## Usage

```tsx
import { SkeletonLoader, Skeleton } from "./SkeletonLoader";

function Profile({ user, loading }) {
  return (
    <SkeletonLoader loading={loading} lines={3} label="Loading profile">
      <h2>{user.name}</h2>
      <p>{user.bio}</p>
    </SkeletonLoader>
  );
}

// Or compose bespoke placeholders from primitives:
<div style={{ display: "flex", gap: 12 }}>
  <Skeleton variant="circle" width={48} height={48} />
  <Skeleton variant="text" width="40%" />
</div>;
```

## Algorithm

- `SkeletonLoader` renders a placeholder while `loading` is true, then its
  `children`. The default placeholder is `lines` text-skeletons with the last line
  ragged (60% width) for a natural paragraph look; pass `placeholder` to override.
- `Skeleton` is a single block. `variant` (`rect | text | circle`) plus `width`/
  `height` shape it; numbers are coerced to `px`.
- **Shimmer mechanics:** a `linear-gradient` sheen sits on a `200%`-wide background
  over a solid base colour. A keyframe slides `background-position` from `-150%` to
  `250%`, sweeping the sheen across. Animating `background-position` does **not**
  trigger layout or paint of surrounding content, it's cheap and transform-friendly
  in spirit (no width/height thrash).
- **Style injection:** the stylesheet is injected once (id-guarded, SSR-guarded) so
  the component is drop-in with no separate CSS import. Projects preferring a real
  CSS file can lift the rules out unchanged.

## Accessibility

- The wrapper sets **`aria-busy={loading}`** so assistive tech knows the region is
  updating. While loading it also gets `role="status"`, `aria-live="polite"`, and an
  `aria-label` (default "Loading") so screen-reader users are informed without focus
  movement; the label is dropped once content arrives.
- The skeleton blocks themselves are **`aria-hidden`**, they are purely decorative
  and must not be read out as content.
- No focus is moved or trapped; the placeholder is non-interactive.
- Because the placeholder occupies the same layout footprint, swapping to real
  content avoids a jarring reflow / layout shift.

## Reduced-motion behaviour

`@media (prefers-reduced-motion: reduce)` sets `animation: none` **and**
`background-image: none`, so the shimmer stops entirely and each block becomes a
calm, solid static placeholder. The placeholders still occupy layout and `aria-busy`
still communicates loading, only the motion is removed. This is a CSS-level
guarantee, so it holds even before/without JS hydration.

## Contract knobs

`SkeletonLoader`:

| Prop          | Type              | Purpose                                  |
| ------------- | ----------------- | ---------------------------------------- |
| `loading`     | boolean           | show placeholder vs children             |
| `lines`       | number            | default placeholder line count           |
| `label`       | string            | accessible busy-region label             |
| `placeholder` | ReactNode         | custom placeholder override              |
| `className`   | string            | wrapper class override                   |

`Skeleton`: `width`, `height`, `variant`, plus any `className`/`style` and standard
span attributes. Theme via CSS custom properties (override per-instance with
`style`):

| Variable                   | Default     | Meaning              |
| -------------------------- | ----------- | -------------------- |
| `--motif-skeleton-base`      | `#e2e8f0`   | block base colour    |
| `--motif-skeleton-sheen`     | `#f1f5f9`   | moving sheen colour  |
| `--motif-skeleton-radius`    | `0.375rem`  | corner radius        |
| `--motif-skeleton-duration`  | `1.4s`      | shimmer cycle length |

## Browser support

All evergreen browsers and Safari 12.1+ (CSS gradients + keyframes +
`background-position` animation are universally supported). The style-injection
effect and any `document` access are SSR-guarded (`typeof document`), so the
component renders its placeholder markup safely in Next.js/RSC client components.
Mark the file `'use client'` when used in an RSC tree.

## Provenance: original (clean-room).
