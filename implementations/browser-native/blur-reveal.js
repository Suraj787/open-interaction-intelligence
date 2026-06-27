/* ============================================================================
 * Motif Recipe, Blur Reveal on Scroll (browser-native, progressive enhancement)
 * ----------------------------------------------------------------------------
 * Reveals elements ([data-motif="blur-reveal"]) as they scroll into view by
 * toggling [data-motif-reveal="shown"], which blur-reveal.css animates.
 *
 * Strategy (cheapest accessible technique first):
 *   1. If the browser supports CSS scroll-driven animations AND the user has
 *      NOT requested reduced motion, hand the whole job to CSS (add the
 *      `motif-css-scroll` class) and attach NO JS observers. Zero runtime cost.
 *   2. Otherwise, use IntersectionObserver to toggle the shown state once.
 *   3. If the user prefers reduced motion, reveal everything immediately and
 *      observe nothing, content is shown with no blur, no movement.
 *   4. If IntersectionObserver is unavailable, reveal everything immediately
 *      (graceful degradation, never leave content hidden).
 *
 * SSR/no-JS safe: the markup is readable before this runs; we only add the
 * `motif-js` class (which arms the resting state) once we are confident we can
 * also remove it again via reveal. We fire a CustomEvent('motif:reveal') per
 * element for consumers.
 *
 * Provenance: original (clean-room).
 * ========================================================================== */

/**
 * Initialise blur-reveal within a root.
 * @param {ParentNode} [root=document] - subtree to scan (re-runnable for SPA inserts).
 * @returns {{ dispose: () => void }} teardown handle.
 */
export function initBlurReveal(root = document) {
  // Guard against non-browser evaluation (SSR bundlers).
  if (typeof window === "undefined" || typeof document === "undefined") {
    return { dispose() {} };
  }

  const reduceMotion = window.matchMedia
    ? window.matchMedia("(prefers-reduced-motion: reduce)")
    : { matches: false, addEventListener() {}, removeEventListener() {} };

  const supportsScrollTimeline =
    typeof CSS !== "undefined" &&
    typeof CSS.supports === "function" &&
    CSS.supports("animation-timeline: view()");

  const docEl = document.documentElement;
  const elements = Array.from(root.querySelectorAll('[data-motif="blur-reveal"]'));
  elements.forEach((el) => el.classList.add("motif-reveal"));

  /** Mark an element revealed and announce it. */
  const reveal = (el) => {
    if (el.dataset.oiiReveal === "shown") return;
    el.dataset.oiiReveal = "shown";
    el.dispatchEvent(
      new CustomEvent("motif:reveal", { bubbles: true, detail: { element: el } })
    );
  };

  // ----- Path 3: reduced motion, reveal instantly, no observers. ----------
  if (reduceMotion.matches) {
    docEl.classList.add("motif-js");
    elements.forEach(reveal);
    return makeDisposer(() => {});
  }

  // ----- Path 1: native CSS scroll-driven animation. -----------------------
  // CSS owns the motion; we just opt the document in. No JS observers needed.
  if (supportsScrollTimeline) {
    docEl.classList.add("motif-js", "motif-css-scroll");
    // The CSS keyframes are authoritative; mark shown so the contract
    // ([data-motif-reveal="shown"]) and the event still fire for consumers.
    elements.forEach(reveal);
    return makeDisposer(() => {});
  }

  // ----- Path 4: no IntersectionObserver, reveal instantly. ---------------
  if (typeof IntersectionObserver === "undefined") {
    docEl.classList.add("motif-js");
    elements.forEach(reveal);
    return makeDisposer(() => {});
  }

  // ----- Path 2: IntersectionObserver timed fallback. ----------------------
  docEl.classList.add("motif-js"); // arms the resting (blurred) state in CSS

  const observer = new IntersectionObserver(
    (entries, obs) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          reveal(entry.target);
          obs.unobserve(entry.target); // one-shot: reveal then stop watching
        }
      }
    },
    {
      // Trigger slightly before fully on-screen for a natural feel.
      rootMargin: "0px 0px -10% 0px",
      threshold: 0.15,
    }
  );

  elements.forEach((el) => observer.observe(el));

  // If the user flips to reduced motion mid-session, reveal everything now.
  const onPrefChange = (e) => {
    if (e.matches) {
      elements.forEach(reveal);
      observer.disconnect();
    }
  };
  reduceMotion.addEventListener?.("change", onPrefChange);

  return makeDisposer(() => {
    observer.disconnect();
    reduceMotion.removeEventListener?.("change", onPrefChange);
  });
}

/** Wrap a teardown fn in the standard dispose handle. */
function makeDisposer(teardown) {
  return { dispose: teardown };
}

/* Auto-init on DOM ready when loaded as a plain module/script.
 * Consumers integrating via a framework should import initBlurReveal instead
 * and call it from their lifecycle hook so they control teardown. */
if (typeof document !== "undefined") {
  const boot = () => initBlurReveal(document);
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot, { once: true });
  } else {
    boot();
  }
}

export default initBlurReveal;
