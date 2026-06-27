"""Aesthetic Convergence Detector.

Heuristic, explainable detection of generic AI-aesthetic signals in real source
files. It does not ban colours or trends; it flags overuse and formulaic patterns
and explains each finding. Findings are advisory and product-grounded.
"""
from __future__ import annotations
import re
import pathlib
from dataclasses import dataclass

EXT = {".html", ".jsx", ".tsx", ".vue", ".svelte", ".css", ".scss", ".astro"}

# (signal, weight, regex, message)
SIGNALS: list[tuple[str, int, str, str]] = [
    ("gradient-hero", 2, r"bg-gradient-to-[a-z]+\s+from-|linear-gradient\(", "Gradient-emphasis background (overused in AI hero sections)"),
    ("excessive-rounded", 1, r"rounded-(?:2xl|3xl|full)", "Large rounded containers (generic when applied broadly)"),
    ("glass-blur", 2, r"backdrop-blur|backdrop-filter\s*:\s*blur", "Glassmorphism blur (legibility + performance cost; often decorative)"),
    ("glow-shadow", 1, r"shadow-(?:glow|2xl)|drop-shadow-\[", "Glow/oversized shadow (decorative cliche)"),
    ("bento-grid", 1, r"grid-cols-\d+[^\"']*auto-rows|bento", "Bento-style grid (formulaic without product justification)"),
    ("pill-overuse", 1, r"rounded-full[^\"']*px-\d", "Pill chips (overused as decoration)"),
    ("floating-nav", 1, r"fixed[^\"']*rounded-full|floating-nav", "Floating rounded navigation (generic AI pattern)"),
    ("gradient-text", 1, r"bg-clip-text[^\"']*text-transparent", "Gradient clipped text (overused heading treatment)"),
    ("fake-metrics", 2, r"\b(?:10x|99\.9%|\+\d{2,}%|trusted by \d+)", "Fake/placeholder metrics (generic marketing copy)"),
    ("generic-copy", 1, r"(?i)supercharge your|take your .* to the next level|all-in-one platform|seamless(?:ly)?", "Generic AI marketing copy"),
    ("three-feature-cards", 1, r"(?is)<(?:div|article)[^>]*card[^>]*>.*?</(?:div|article)>", "Card-heavy hierarchy (check for the formulaic three-glowing-cards block)"),
]
_COMPILED = [(s, w, re.compile(p), m) for s, w, p, m in SIGNALS]


@dataclass
class Finding:
    signal: str
    weight: int
    message: str
    path: str
    count: int


def audit_text(text: str, path: str = "") -> list[Finding]:
    out: list[Finding] = []
    for sig, w, rx, msg in _COMPILED:
        n = len(rx.findall(text))
        if n:
            out.append(Finding(sig, w, msg, path, n))
    return out


def audit_path(target: str | pathlib.Path) -> tuple[list[Finding], int, str]:
    p = pathlib.Path(target)
    files = [p] if p.is_file() else [
        f for f in p.rglob("*") if f.is_file() and f.suffix.lower() in EXT
        and "node_modules" not in f.parts and ".git" not in f.parts]
    findings: list[Finding] = []
    for f in files:
        try:
            findings.extend(audit_text(f.read_text(errors="replace"), str(f)))
        except OSError:
            continue
    # Convergence score 0-100: weighted, saturating. Higher = more generic.
    raw = sum(f.weight * min(f.count, 5) for f in findings)
    score = min(100, raw * 4)
    if score >= 60:
        band = "high convergence (likely generic; ground originality in product reality)"
    elif score >= 30:
        band = "moderate convergence (review flagged signals)"
    else:
        band = "low convergence"
    return findings, score, band
