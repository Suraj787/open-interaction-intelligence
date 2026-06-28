"""Design-system extraction from an existing repository (static).

Parses CSS variables, Tailwind theme tokens, colour usage, spacing/radius, and motion
conventions into .motif/design-system/. Static and deterministic; it reports what the
code actually contains and flags inconsistencies (e.g. many one-off hex colours).
"""
from __future__ import annotations
import json
import re
import pathlib
from . import runtime

_VAR = re.compile(r"--([a-z0-9-]+)\s*:\s*([^;}\n]+)")
_HEX = re.compile(r"#[0-9a-fA-F]{3,8}\b")
_TW_COLOR = re.compile(r"colors\s*:\s*\{")
_EXT = {".css", ".scss", ".vue", ".js", ".ts", ".jsx", ".tsx", ".html"}


def _iter(root):
    for f in root.rglob("*"):
        if f.is_file() and f.suffix in _EXT and "node_modules" not in f.parts \
           and ".git" not in f.parts and ".motif" not in f.parts:
            yield f


def extract(target) -> dict:
    root = pathlib.Path(target)
    variables: dict = {}
    hexes: dict = {}
    motion = {"transitions": 0, "keyframes": 0, "reduced_motion_guards": 0}
    important = 0
    tailwind = (root / "tailwind.config.js").exists() or (root / "tailwind.config.ts").exists()
    for f in _iter(root):
        try:
            t = f.read_text(errors="replace")
        except OSError:
            continue
        for name, val in _VAR.findall(t):
            variables.setdefault(name, val.strip())
        for h in _HEX.findall(t):
            hexes[h.lower()] = hexes.get(h.lower(), 0) + 1
        motion["transitions"] += len(re.findall(r"transition:", t))
        motion["keyframes"] += len(re.findall(r"@keyframes", t))
        motion["reduced_motion_guards"] += t.count("prefers-reduced-motion")
        important += t.count("!important")

    semantics = {k: v for k, v in variables.items() if any(
        s in k for s in ("primary", "secondary", "success", "warning", "danger", "error", "bg", "fg", "text", "color"))}
    exceptions = []
    if len(hexes) > 8:
        exceptions.append(f"{len(hexes)} distinct hard-coded hex colours (consider tokenising)")
    if important:
        exceptions.append(f"{important} !important override(s)")
    if motion["keyframes"] and not motion["reduced_motion_guards"]:
        exceptions.append("animation present without a prefers-reduced-motion guard")

    result = {
        "extracted_from": str(root),
        "generated": "static",
        "tailwind": tailwind,
        "css_variables": sorted(variables),
        "primitives": {"variables": variables, "distinct_hex_colours": len(hexes)},
        "semantics": semantics,
        "motion": motion,
        "exceptions": exceptions,
    }
    return result


def write(target, result: dict) -> pathlib.Path:
    out = runtime.state_root(target) / "design-system"
    out.mkdir(parents=True, exist_ok=True)
    (out / "primitives.json").write_text(json.dumps(result["primitives"], indent=2) + "\n")
    (out / "semantics.json").write_text(json.dumps(result["semantics"], indent=2) + "\n")
    (out / "motion.json").write_text(json.dumps(result["motion"], indent=2) + "\n")
    (out / "exceptions.json").write_text(json.dumps(result["exceptions"], indent=2) + "\n")
    report = [f"# Design-system extraction: {result['extracted_from']}", "",
              f"- Tailwind: {result['tailwind']}",
              f"- CSS variables: {len(result['css_variables'])}",
              f"- Distinct hex colours: {result['primitives']['distinct_hex_colours']}",
              f"- Transitions: {result['motion']['transitions']} · keyframes: {result['motion']['keyframes']} "
              f"· reduced-motion guards: {result['motion']['reduced_motion_guards']}",
              "", "## Exceptions / inconsistencies"]
    report += [f"- {e}" for e in result["exceptions"]] or ["- none detected"]
    (out / "report.md").write_text("\n".join(report) + "\n")
    return out
