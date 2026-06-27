"""Registry loading + schema validation. Offline by default."""
from __future__ import annotations
import json
import pathlib
from dataclasses import dataclass, field

from . import jsonschema_min

# repo root = parent of the `motif` package dir
ROOT = pathlib.Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "registry"
SCHEMAS = ROOT / "schemas"

# registry subdir -> schema file (typed record kinds)
KINDS = {
    "sources": "source.schema.json",
    "components": "component.schema.json",
    "effects": "effect.schema.json",
    "patterns": "pattern.schema.json",
    "recipes": "recipe.schema.json",
}


@dataclass
class Record:
    kind: str
    path: pathlib.Path
    data: dict


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    counts: dict[str, int] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return not self.errors


def load_schema(kind: str) -> dict:
    return json.loads((SCHEMAS / KINDS[kind]).read_text())


def load_records(kind: str) -> list[Record]:
    out: list[Record] = []
    d = REGISTRY / kind
    if not d.exists():
        return out
    for p in sorted(d.glob("*.json")):
        out.append(Record(kind=kind, path=p, data=json.loads(p.read_text())))
    return out


def load_all() -> dict[str, list[Record]]:
    return {kind: load_records(kind) for kind in KINDS}


def validate_all() -> ValidationResult:
    res = ValidationResult()
    for kind in KINDS:
        schema = load_schema(kind)
        recs = load_records(kind)
        res.counts[kind] = len(recs)
        seen_ids: set[str] = set()
        for rec in recs:
            rel = rec.path.relative_to(ROOT)
            for err in jsonschema_min.validate(rec.data, schema):
                res.errors.append(f"{rel}: {err}")
            rid = rec.data.get("id")
            if rid is None:
                res.errors.append(f"{rel}: missing 'id'")
            elif rid in seen_ids:
                res.errors.append(f"{rel}: duplicate id '{rid}'")
            else:
                seen_ids.add(rid)
            if rid and rec.path.stem != rid:
                res.errors.append(f"{rel}: filename does not match id '{rid}'")
    res.errors.extend(_referential_checks())
    return res


def _referential_checks() -> list[str]:
    """Cross-record integrity: recipe.pattern must exist, component.source must exist."""
    errors: list[str] = []
    pattern_ids = {r.data["id"] for r in load_records("patterns")}
    source_ids = {r.data["id"] for r in load_records("sources")}
    effect_ids = {r.data["id"] for r in load_records("effects")}
    for r in load_records("recipes"):
        if r.data.get("pattern") not in pattern_ids:
            errors.append(f"{r.path.name}: recipe.pattern '{r.data.get('pattern')}' has no pattern record")
        for s in r.data.get("source_references", []):
            if s not in source_ids:
                errors.append(f"{r.path.name}: source_reference '{s}' has no source record")
    for r in load_records("components"):
        if r.data.get("source") not in source_ids:
            errors.append(f"{r.path.name}: component.source '{r.data.get('source')}' has no source record")
    for r in load_records("patterns"):
        for e in r.data.get("recommended_effects", []) + r.data.get("rejected_effects", []):
            if e not in effect_ids:
                errors.append(f"{r.path.name}: effect '{e}' referenced but has no effect record")
    return errors
