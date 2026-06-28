"""Aesthetic Convergence Detector (recalibrated).

Explainable, deterministic detection of generic-pattern concentration in real source files.
It does not ban colours or trends and it never claims a UI was produced by AI. It separates
signal presence from frequency, concentration, design-system provenance, and product context,
applies diminishing returns, and requires a combination of cliche signals for a high band.
A single rounded card, pill, gradient, or three-card layout is a weak signal; high aesthetic-
convergence risk requires several distinct, unjustified generic signals together.

Static-only evidence: confidence is capped at moderate.
"""
from __future__ import annotations
import re
import pathlib
from dataclasses import dataclass

EXT = {".html", ".jsx", ".tsx", ".vue", ".svelte", ".css", ".scss", ".astro"}

# (signal, tier, regex, message). Tiers: marketing (strongest tell), decorative (visual
# cliche), structural (common UI; weak on its own).
SIGNALS: list[tuple[str, str, str, str]] = [
    ("fake-metrics", "marketing", r"\b(?:10x|99\.9%|\+\d{2,}%|trusted by \d+)", "Placeholder/marketing metrics"),
    ("generic-copy", "marketing", r"(?i)supercharge your|take your .* to the next level|all-in-one platform|seamless(?:ly)?", "Generic marketing copy"),
    ("gradient-hero", "decorative", r"bg-gradient-to-[a-z]+\s+from-|linear-gradient\(", "Gradient-emphasis background"),
    ("glass-blur", "decorative", r"backdrop-blur|backdrop-filter\s*:\s*blur", "Glassmorphism blur"),
    ("glow-shadow", "decorative", r"shadow-(?:glow|2xl)|drop-shadow-\[", "Glow/oversized shadow"),
    ("gradient-text", "decorative", r"bg-clip-text[^\"']*text-transparent", "Gradient clipped text"),
    ("floating-nav", "decorative", r"fixed[^\"']*rounded-full|floating-nav", "Floating rounded navigation"),
    ("bento-grid", "decorative", r"grid-cols-\d+[^\"']*auto-rows|bento", "Bento-style grid"),
    ("pill-overuse", "structural", r"rounded-full[^\"']*px-\d", "Pill chips"),
    ("excessive-rounded", "structural", r"rounded-(?:2xl|3xl|full)", "Large rounded containers"),
    ("three-feature-cards", "structural", r"(?is)<(?:div|article)[^>]*card[^>]*>.*?</(?:div|article)>", "Card containers"),
]
_COMPILED = [(s, t, re.compile(p), m) for s, t, p, m in SIGNALS]
_TIER = {s: t for s, t, _p, _m in SIGNALS}

# base weights per tier and the diminishing-returns constant
_BASE = {"marketing": 26.0, "decorative": 15.0, "structural": 9.0}
_K = 4.0
# product forms where dense, repeated structure is functionally justified
_DENSE_FORMS = {"enterprise-app", "dashboard", "developer-tool", "gov-service", "ecommerce",
                "admin", "data-table", "analytics"}

# provenance markers
_VAR = re.compile(r"--[a-z0-9-]+\s*:")


@dataclass
class Finding:
    signal: str
    weight: int
    message: str
    path: str
    count: int


def audit_text(text: str, path: str = "") -> list[Finding]:
    out: list[Finding] = []
    for sig, tier, rx, msg in _COMPILED:
        n = len(rx.findall(text))
        if n:
            out.append(Finding(sig, int(_BASE[tier]), msg, path, n))
    return out


def _collect(target):
    """Single-pass scan: returns (findings, design_system_present)."""
    p = pathlib.Path(target)
    files = [p] if p.is_file() else [
        f for f in p.rglob("*") if f.is_file() and f.suffix.lower() in EXT
        and "node_modules" not in f.parts and ".git" not in f.parts and ".motif" not in f.parts]
    findings: list[Finding] = []
    ds_present = False
    for f in files:
        try:
            t = f.read_text(errors="replace")
        except OSError:
            continue
        findings.extend(audit_text(t, f.stem))
        if not ds_present and _VAR.search(t):
            ds_present = True
    if not ds_present and not p.is_file():
        ds_present = any((p / c).exists() for c in ("tailwind.config.js", "tailwind.config.ts"))
    return findings, ds_present


def _freq(count: int) -> float:
    """Diminishing returns: saturating in count (0..1)."""
    return count / (count + _K)


def audit(target, context: dict | None = None) -> dict:
    """Full, inspectable convergence audit. Returns overall score, band, confidence, and a
    per-signal breakdown with raw counts, weighted scores, context/provenance adjustments,
    affected routes, and explanations."""
    findings, ds_present = _collect(target)
    forms = set((context or {}).get("product_forms", []) or [])
    dense_context = bool(forms & _DENSE_FORMS)

    # aggregate per signal
    agg: dict[str, dict] = {}
    for f in findings:
        a = agg.setdefault(f.signal, {"count": 0, "routes": set()})
        a["count"] += f.count
        if f.path:
            a["routes"].add(f.path)

    signals = []
    decorative_present = 0
    overall = 0.0
    for sig, tier, _rx, msg in _COMPILED:
        if sig not in agg:
            continue
        count = agg[sig]["count"]
        routes = sorted(agg[sig]["routes"])
        base = _BASE[tier]
        # context adjustment: structure is justified in dense product forms; decorative
        # cliche is mildly excused there; marketing copy is never excused.
        if tier == "structural":
            ctx_adj = 0.35 if dense_context else 1.0
        elif tier == "decorative":
            ctx_adj = 0.7 if dense_context else 1.0
        else:
            ctx_adj = 1.0
        # provenance adjustment: structural patterns drawn from a design system are intentional
        prov_adj = 0.6 if (tier == "structural" and ds_present) else 1.0
        weighted = base * _freq(count) * ctx_adj * prov_adj
        overall += weighted
        if tier in ("marketing", "decorative"):
            decorative_present += 1
        signals.append({
            "name": sig, "tier": tier, "raw_count": count,
            "files_present": len(routes), "weighted_score": round(weighted, 2),
            "context_adjustment": ctx_adj, "provenance_adjustment": prov_adj,
            "affected_routes": routes[:12],
            "explanation": f"{msg}: {count} occurrence(s) across {len(routes)} file(s); "
                           f"tier={tier}, context x{ctx_adj}, provenance x{prov_adj}",
        })

    # combination gate: a high band needs several distinct marketing/decorative signals
    combo_bonus = (decorative_present - 2) * 10 if decorative_present >= 3 else 0
    score = int(min(100, round(overall + combo_bonus)))
    signals.sort(key=lambda s: -s["weighted_score"])

    if score >= 60:
        band = "high aesthetic-convergence risk (generic-pattern concentration; combined cliche signals)"
    elif score >= 30:
        band = "moderate aesthetic-convergence risk (review flagged generic-pattern signals)"
    else:
        band = "low aesthetic-convergence risk"
    # static-only evidence caps confidence at moderate
    confidence = "moderate" if score >= 30 else "low"

    return {
        "overall_score": score,
        "risk_band": band,
        "confidence": confidence,
        "signals": signals,
        "provenance": {"design_system_present": ds_present, "dense_product_context": dense_context,
                       "product_forms": sorted(forms)},
        "limitations": [
            "Static heuristic over source text; does not render or compare across projects.",
            "Common Tailwind structure is not evidence of generic design and is down-weighted.",
            "Cannot and does not determine whether a UI was produced by AI.",
            "Confidence is capped at moderate because only static evidence is available.",
        ],
    }


def audit_path(target: str | pathlib.Path) -> tuple[list[Finding], int, str]:
    """Backward-compatible entry point: returns (per-file findings, score, short band).

    Uses the recalibrated, non-saturating scorer with no product context (universal).
    """
    findings, _ds = _collect(target)
    r = audit(target)
    short = ("high convergence (generic-pattern concentration)" if r["overall_score"] >= 60
             else "moderate convergence (review flagged signals)" if r["overall_score"] >= 30
             else "low convergence")
    return findings, r["overall_score"], short
