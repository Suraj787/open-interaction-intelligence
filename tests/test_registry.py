"""Registry + schema integrity."""
import json
import pathlib
from motif import registry, jsonschema_min

ROOT = registry.ROOT


def test_registry_validates():
    res = registry.validate_all()
    assert res.ok, "registry validation errors:\n" + "\n".join(res.errors)


def test_minimum_source_count():
    # v0.1.0 discipline: 15-20 deeply reviewed sources.
    assert res_count("sources") >= 15


def test_has_core_record_kinds():
    for kind in ("effects", "patterns", "recipes", "components"):
        assert res_count(kind) >= 4, f"{kind} too sparse"


def test_recipes_point_at_real_implementations():
    for r in registry.load_records("recipes"):
        path = r.data.get("implementation_path")
        if path:
            assert (ROOT / path).exists(), f"missing implementation file: {path}"


def test_eval_cases_match_schema():
    schema = json.loads((ROOT / "schemas" / "evaluation.schema.json").read_text())
    cases = sorted((ROOT / "evals" / "cases").glob("*.json"))
    assert cases, "no eval cases"
    for c in cases:
        errs = jsonschema_min.validate(json.loads(c.read_text()), schema)
        assert not errs, f"{c.name}: {errs}"


def res_count(kind: str) -> int:
    return len(registry.load_records(kind))
