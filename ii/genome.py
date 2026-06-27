"""Product Design Genome: validate, explain, diff.

The genome captures a product's visual and interaction identity. Generation and
extraction from a live repository are part of the orchestrator workflow; here we
provide the deterministic validate/explain/diff operations over genome records.
"""
from __future__ import annotations
import json
from . import data
from motif import jsonschema_min


def _all():
    return {d["product"] if "product" in d else p.stem: (p, d)
            for p, d in data.load_kind("design-genomes")}


def load(name: str):
    for p, d in data.load_kind("design-genomes"):
        if p.stem == name or d.get("product") == name:
            return d
    return None


def validate(name: str) -> list[str]:
    d = load(name)
    if d is None:
        return [f"no genome '{name}'"]
    schema = json.loads((data.SCHEMAS / "design-genome.schema.json").read_text())
    return jsonschema_min.validate(d, schema)


_KEYS = ["brand_traits", "prohibited_traits", "motion_character", "density",
         "accessibility_posture", "performance_posture", "content_tone"]


def explain(name: str) -> list[str]:
    d = load(name)
    if d is None:
        return [f"no genome '{name}'"]
    out = [f"# Genome: {name} (v{d.get('version')})"]
    for k in _KEYS:
        if k in d:
            v = d[k]
            out.append(f"  {k}: {', '.join(v) if isinstance(v, list) else v}")
    return out


def diff(a: str, b: str) -> list[str]:
    da, db = load(a), load(b)
    if da is None or db is None:
        return ["one or both genomes not found"]
    out = [f"# diff {a} -> {b}"]
    keys = sorted(set(da) | set(db))
    for k in keys:
        va, vb = da.get(k), db.get(k)
        if va != vb:
            out.append(f"  ~ {k}: {va!r} -> {vb!r}")
    if len(out) == 1:
        out.append("  (no differences)")
    return out
