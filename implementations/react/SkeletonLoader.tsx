/* ============================================================================
 * Motif Recipe, Skeleton Loader (React, dependency-free)
 * ----------------------------------------------------------------------------
 * Placeholder blocks with a left-to-right shimmer that stand in for content
 * while it loads. The shimmer is a CSS gradient animated via background-position
 * (cheap, no layout), and is disabled under prefers-reduced-motion (static
 * placeholder). The wrapper exposes aria-busy so assistive tech knows the
 * region is loading, and the skeletons themselves are aria-hidden.
 *
 * No external dependencies. Styles are injected once from this module so the
 * component is drop-in (no separate CSS import required), but every class is
 * overridable via className for design-token theming.
 *
 * Provenance: original (clean-room).
 * ========================================================================== */
import React, { useEffect } from "react";

/* ---------------------------------------------------------------------------
 * One-time stylesheet injection.
 * Kept in-module so the component is self-contained. Guarded for SSR (only runs
 * in the browser) and idempotent (keyed by id). Projects that prefer a real CSS
 * file can delete this and ship the same rules in their stylesheet.
 * ------------------------------------------------------------------------- */
const STYLE_ID = "motif-skeleton-styles";
const STYLES = `
.motif-skeleton {
  /* Tunable knobs via custom properties (override per-instance with style). */
  --motif-skel-base: var(--motif-skeleton-base, #e2e8f0);
  --motif-skel-sheen: var(--motif-skeleton-sheen, #f1f5f9);
  --motif-skel-radius: var(--motif-skeleton-radius, 0.375rem);
  --motif-skel-duration: var(--motif-skeleton-duration, 1.4s);

  display: block;
  border-radius: var(--motif-skel-radius);
  background-color: var(--motif-skel-base);
  /* Moving sheen overlaid on the base. 200% width so it can slide across. */
  background-image: linear-gradient(
    90deg,
    transparent 0%,
    var(--motif-skel-sheen) 50%,
    transparent 100%
  );
  background-size: 200% 100%;
  background-repeat: no-repeat;
  background-position: -150% 0;
  animation: motif-skeleton-shimmer var(--motif-skel-duration) ease-in-out infinite;
}

@keyframes motif-skeleton-shimmer {
  to {
    background-position: 250% 0;
  }
}

/* Reduced motion: no shimmer. Show a calm static placeholder instead. */
@media (prefers-reduced-motion: reduce) {
  .motif-skeleton {
    animation: none !important;
    background-image: none !important;
  }
}
`;

function useSkeletonStyles(): void {
  useEffect(() => {
    if (typeof document === "undefined") return;
    if (document.getElementById(STYLE_ID)) return;
    const tag = document.createElement("style");
    tag.id = STYLE_ID;
    tag.textContent = STYLES;
    document.head.appendChild(tag);
    // Intentionally not removed on unmount: the stylesheet is shared across all
    // skeleton instances and harmless to leave in place.
  }, []);
}

/* ---------------------------------------------------------------------------
 * Single skeleton block.
 * ------------------------------------------------------------------------- */
export interface SkeletonProps
  extends React.HTMLAttributes<HTMLSpanElement> {
  /** Block width (CSS length). */
  width?: string | number;
  /** Block height (CSS length). */
  height?: string | number;
  /** Visual shape; `circle` forces a 1:1 round block (e.g. avatars). */
  variant?: "rect" | "text" | "circle";
}

const toCss = (v?: string | number) =>
  typeof v === "number" ? `${v}px` : v;

export function Skeleton({
  width,
  height,
  variant = "rect",
  className = "",
  style,
  ...rest
}: SkeletonProps) {
  useSkeletonStyles();

  const variantStyle: React.CSSProperties =
    variant === "circle"
      ? { borderRadius: "50%", width: width ?? 40, height: height ?? 40 }
      : variant === "text"
      ? { height: height ?? "1em", borderRadius: "0.25rem" }
      : {};

  return (
    <span
      className={`motif-skeleton ${className}`.trim()}
      aria-hidden="true"
      style={{
        width: toCss(width),
        height: toCss(height),
        ...variantStyle,
        ...style,
      }}
      {...rest}
    />
  );
}

/* ---------------------------------------------------------------------------
 * Loading region wrapper.
 * Renders skeletons while `loading`, then swaps to `children`. Sets aria-busy
 * so AT announces the region as busy and the skeletons (aria-hidden) add no
 * noise. Optionally announces completion politely.
 * ------------------------------------------------------------------------- */
export interface SkeletonLoaderProps {
  /** When true, show skeleton placeholders instead of children. */
  loading: boolean;
  /** Real content, shown once `loading` is false. */
  children: React.ReactNode;
  /** Number of repeated skeleton lines to render as the placeholder. */
  lines?: number;
  /** Accessible label for the busy region (e.g. "Loading profile"). */
  label?: string;
  /** Optional custom placeholder; overrides the default `lines` skeletons. */
  placeholder?: React.ReactNode;
  className?: string;
}

export function SkeletonLoader({
  loading,
  children,
  lines = 3,
  label = "Loading",
  placeholder,
  className = "",
}: SkeletonLoaderProps) {
  const defaultPlaceholder = (
    <div style={{ display: "grid", gap: "0.5rem" }}>
      {Array.from({ length: lines }).map((_, i) => (
        <Skeleton
          key={i}
          variant="text"
          // Last line shorter for a natural paragraph rag.
          width={i === lines - 1 ? "60%" : "100%"}
        />
      ))}
    </div>
  );

  return (
    <div
      className={className}
      aria-busy={loading}
      aria-live="polite"
      // Expose a label only while busy so AT can describe the loading region.
      {...(loading ? { "aria-label": label, role: "status" } : {})}
    >
      {loading ? placeholder ?? defaultPlaceholder : children}
    </div>
  );
}

export default SkeletonLoader;
