// CLEAN CONTROL FIXTURE, should produce no high/critical findings.
// Browser-native, dependency-free, reduced-motion aware.
export function fadeIn(el) {
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce) {
    el.style.opacity = "1";
    return;
  }
  el.animate(
    [{ opacity: 0, transform: "translateY(8px)" }, { opacity: 1, transform: "none" }],
    { duration: 240, easing: "ease-out", fill: "forwards" }
  );
}
