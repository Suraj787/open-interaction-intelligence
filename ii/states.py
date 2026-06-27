"""State Completeness Engine.

Required states are inferred from component type (from the curated state-requirements
records). The engine builds a matrix, inspects a real component file for evidence of
each state, and fails validation when required states are absent.
"""
from __future__ import annotations
import re
import pathlib
from . import data

# Heuristic markers that evidence a state in source.
MARKERS = {
    "loading": [r"(?i)loading", r"isLoading", r"aria-busy", r"skeleton", r"spinner"],
    "empty": [r"(?i)empty", r"no (?:results|items|data|records)", r"emptyState"],
    "error": [r"(?i)\berror\b", r"hasError", r"role=[\"']alert", r"try\s*\{"],
    "success": [r"(?i)success", r"saved", r"role=[\"']status"],
    "disabled": [r"disabled", r"aria-disabled"],
    "focus": [r":focus", r"focus-visible", r"onFocus", r"@focus"],
    "hover": [r":hover", r"onMouseEnter", r"@mouseenter"],
    "selected": [r"(?i)selected", r"aria-selected", r"aria-current"],
    "offline": [r"(?i)offline", r"navigator\.onLine"],
    "permission-denied": [r"(?i)forbidden|permission|not authoris|403"],
    "stale": [r"(?i)stale|out of date|refetch"],
    "conflict": [r"(?i)conflict|version mismatch|409"],
    "reduced-motion": [r"prefers-reduced-motion"],
    "slow-network": [r"(?i)slow|timeout|retry"],
}


def required_map() -> dict[str, dict]:
    return {d["component_type"]: d for _, d in data.load_kind("state-requirements")}


def matrix() -> list[tuple[str, list[str]]]:
    return [(d["component_type"], d.get("required_states", []))
            for _, d in data.load_kind("state-requirements")]


def evidence_in_text(text: str) -> set[str]:
    found = set()
    for state, pats in MARKERS.items():
        if any(re.search(p, text) for p in pats):
            found.add(state)
    return found


def inspect_file(path: str | pathlib.Path, component_type: str) -> dict:
    reqs = required_map().get(component_type)
    if not reqs:
        return {"error": f"unknown component_type '{component_type}'",
                "known": sorted(required_map())}
    required = [s for s in reqs.get("required_states", []) if s in MARKERS]
    text = pathlib.Path(path).read_text(errors="replace")
    present = evidence_in_text(text)
    missing = [s for s in required if s not in present]
    return {
        "component_type": component_type,
        "required_checkable": required,
        "evidenced": sorted(present & set(required)),
        "missing": missing,
        "ok": not missing,
    }


def validate_states(component_type: str, present: list[str]) -> dict:
    reqs = required_map().get(component_type)
    if not reqs:
        return {"error": f"unknown component_type '{component_type}'",
                "known": sorted(required_map())}
    required = reqs.get("required_states", [])
    missing = [s for s in required if s not in present]
    return {"component_type": component_type, "required": required,
            "present": present, "missing": missing, "ok": not missing}
