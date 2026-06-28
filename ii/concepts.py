"""Breadth-first concept generation.

For important changes, generate materially different structural concepts (not colour
variants). Concepts are structured records, shared by CLI and Studio. Visual preview of
a concept against a running app is experimental (needs a browser runtime).
"""
from __future__ import annotations
import json
from . import runtime

DIRECTIONS = [
    ("conservative-repair", "Fix the concrete problems with minimal structural change",
     "low", "low"),
    ("workflow-first", "Reorganise around the primary workflow and decision the user makes",
     "high", "medium"),
    ("accessibility-first", "Lead with semantics, keyboard, focus, and non-colour status",
     "medium", "low"),
    ("information-dense-expert", "Optimise for expert scanning: table-first, high density",
     "medium", "medium"),
    ("progressive-disclosure", "Reveal complexity progressively to reduce cognitive load",
     "medium", "medium"),
    ("brand-distinctive", "Express product identity through motion and layout grounded in the genome",
     "high", "high"),
]


def generate(target, goal: str, n: int = 3) -> list[dict]:
    out = []
    for i, (key, summary, complexity, risk) in enumerate(DIRECTIONS[:n], 1):
        out.append({
            "id": f"concept-{i:02d}-{key}",
            "name": key.replace("-", " ").title(),
            "direction": summary,
            "information_architecture": f"{key}: structure derived from the goal '{goal}'",
            "layout": "TODO per direction", "navigation": "TODO per direction",
            "component_strategy": "prefer existing project components and approved recipes",
            "interaction_model": "patterns before effects; reduced-motion required",
            "motion": "restrained; honour the project's motion grammar",
            "accessibility": "WCAG 2.2 AA; keyboard + focus + non-colour status",
            "performance": "transform/opacity; no offscreen continuous motion",
            "implementation_complexity": complexity, "migration_risk": risk,
            "rationale": f"Materially different direction: {summary.lower()}",
        })
    return out


def write(target, goal: str, concepts: list[dict]) -> str:
    d = runtime.state_root(target) / "concepts"
    d.mkdir(parents=True, exist_ok=True)
    for c in concepts:
        (d / f"{c['id']}.json").write_text(json.dumps(c, indent=2) + "\n")
    return str(d)


def load(target) -> list[dict]:
    d = runtime.state_root(target) / "concepts"
    if not d.exists():
        return []
    return [json.loads(p.read_text()) for p in sorted(d.glob("concept-*.json"))]
