"""Unified data loading + schema validation for the Interface Intelligence OS engines.

Reuses the Motif foundation (registry + minimal JSON-Schema validator) and extends
validation to the new engine data directories. Offline and dependency-free.
"""
from __future__ import annotations
import json
import pathlib
from motif import registry as _reg
from motif import jsonschema_min

ROOT = _reg.ROOT
SCHEMAS = _reg.SCHEMAS

# logical kind -> (glob relative to ROOT, schema file in schemas/)
DATA_KINDS: dict[str, tuple[str, str]] = {
    "styles": ("design-intelligence/styles/*.json", "style.schema.json"),
    "layouts": ("design-intelligence/layout/*.json", "layout.schema.json"),
    "ux-principles": ("design-intelligence/ux-principles/*.json", "ux-principle.schema.json"),
    "colour-systems": ("design-intelligence/colour/*.json", "colour-system.schema.json"),
    "typography-systems": ("design-intelligence/typography/*.json", "typography-system.schema.json"),
    "industry-packs": ("design-intelligence/industry-packs/*.json", "industry-pack.schema.json"),
    "product-manifests": ("product-intelligence/manifests/*.json", "product-context.schema.json"),
    "design-genomes": ("governance/design-genome/*.json", "design-genome.schema.json"),
    "graph-nodes": ("governance/interaction-graph/nodes/*.json", "graph-node.schema.json"),
    "graph-edges": ("governance/interaction-graph/edges/*.json", "graph-edge.schema.json"),
    "decisions": ("governance/decision-ledger/*.json", "decision-ledger.schema.json"),
    "debt-findings": ("governance/debt/*.json", "debt-finding.schema.json"),
    "motion-grammars": ("interaction-intelligence/motion/*.json", "motion-grammar.schema.json"),
    "density-grammars": ("interaction-intelligence/density/*.json", "density-grammar.schema.json"),
    "state-requirements": ("interaction-intelligence/states/*.json", "state-requirements.schema.json"),
    "bench-cases": ("interfacebench/cases/*.json", "evaluation.schema.json"),
    "interface-specs": ("specifications/*.json", "interface-spec.schema.json"),
}


def load_kind(kind: str) -> list[tuple[pathlib.Path, dict]]:
    glob, _ = DATA_KINDS[kind]
    base, pattern = glob.rsplit("/", 1)
    out: list[tuple[pathlib.Path, dict]] = []
    for p in sorted((ROOT / base).glob(pattern)):
        out.append((p, json.loads(p.read_text())))
    return out


def _schema(name: str) -> dict:
    return json.loads((SCHEMAS / name).read_text())


def validate_kind(kind: str) -> tuple[int, list[str]]:
    glob, schema_name = DATA_KINDS[kind]
    schema = _schema(schema_name)
    errors: list[str] = []
    records = load_kind(kind)
    seen: set[str] = set()
    for path, data in records:
        rel = path.relative_to(ROOT)
        for e in jsonschema_min.validate(data, schema):
            errors.append(f"{rel}: {e}")
        rid = data.get("id")
        if rid:
            if rid in seen:
                errors.append(f"{rel}: duplicate id '{rid}'")
            seen.add(rid)
    return len(records), errors


def validate_all_data() -> tuple[dict[str, int], list[str]]:
    counts: dict[str, int] = {}
    errors: list[str] = []
    for kind in DATA_KINDS:
        try:
            n, errs = validate_kind(kind)
        except FileNotFoundError:
            n, errs = 0, []
        counts[kind] = n
        errors.extend(errs)
    return counts, errors
