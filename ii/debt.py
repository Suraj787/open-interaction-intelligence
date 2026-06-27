"""Interface Debt analysis.

Scans a target project for explainable debt signals and produces a weighted
Interface Debt Score with a full breakdown and evidence. A score is never
produced without reasons. Heuristic and static; it estimates, it does not measure
runtime behaviour.
"""
from __future__ import annotations
import re
import pathlib
from dataclasses import dataclass, field

EXT = {".html", ".jsx", ".tsx", ".vue", ".svelte", ".css", ".scss", ".js", ".ts"}

# category -> (weight, regex, message)
SIGNALS = [
    ("arbitrary-value", 2, re.compile(r"(?:w|h|p|m|gap|text|bg|top|left)-\[[^\]]+\]"),
     "Arbitrary Tailwind value (bypasses design tokens)"),
    ("hex-colour-inline", 2, re.compile(r"#[0-9a-fA-F]{3,8}\b"),
     "Hard-coded hex colour (should use a semantic token)"),
    ("important", 2, re.compile(r"!important"),
     "!important override (specificity debt)"),
    ("inline-style", 1, re.compile(r"style=[\"']\s*[a-z-]+\s*:"),
     "Inline style (escapes the token/system)"),
    ("missing-reduced-motion", 3, None,
     "Animation present without a prefers-reduced-motion guard"),
    ("magic-zindex", 1, re.compile(r"z-\[?\d{3,}\]?|z-index\s*:\s*\d{3,}"),
     "Large/arbitrary z-index (stacking debt)"),
    ("todo-fixme", 1, re.compile(r"(?i)\b(?:TODO|FIXME|HACK)\b"),
     "Unresolved TODO/FIXME/HACK marker"),
]


@dataclass
class Debt:
    score: int = 0
    findings: list[dict] = field(default_factory=list)
    by_category: dict = field(default_factory=dict)
    files_scanned: int = 0


def _iter_files(root: pathlib.Path):
    if root.is_file():
        yield root
        return
    for f in root.rglob("*"):
        if f.is_file() and f.suffix.lower() in EXT and "node_modules" not in f.parts \
           and ".git" not in f.parts and ".motif" not in f.parts:
            yield f


def calculate(target: str | pathlib.Path) -> Debt:
    root = pathlib.Path(target)
    d = Debt()
    for f in _iter_files(root):
        d.files_scanned += 1
        try:
            text = f.read_text(errors="replace")
        except OSError:
            continue
        has_anim = bool(re.search(r"@keyframes|transition:|animation:|\.animate\(|motion\.", text))
        has_rm = "prefers-reduced-motion" in text
        for cat, weight, rx, msg in SIGNALS:
            if cat == "missing-reduced-motion":
                if has_anim and not has_rm:
                    _add(d, cat, weight, msg, str(f), 1)
                continue
            n = len(rx.findall(text))
            if n:
                _add(d, cat, weight, msg, str(f), n)
    # Normalise by files scanned so big repos are not penalised purely for size.
    raw = sum(x["weight"] * x["count"] for x in d.findings)
    denom = max(1, d.files_scanned)
    d.score = min(100, round(raw / denom * 10))
    return d


def _add(d: Debt, cat, weight, msg, path, count):
    d.findings.append({"category": cat, "weight": weight, "message": msg,
                       "path": path, "count": count})
    b = d.by_category.setdefault(cat, {"weight": weight, "occurrences": 0, "files": 0})
    b["occurrences"] += count
    b["files"] += 1


def band(score: int) -> str:
    if score >= 60:
        return "high interface debt"
    if score >= 30:
        return "moderate interface debt"
    return "low interface debt"
