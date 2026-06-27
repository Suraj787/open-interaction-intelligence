"""Minimal JSON Schema (draft-07 subset) validator — zero dependencies.

Supports the keywords used by Motif schemas: type, required, properties,
additionalProperties, enum, pattern, minimum, maximum, minItems, minLength,
items, and a light `format` check for "date" and "uri". If the real
`jsonschema` package is installed it is used instead for full coverage.
"""
from __future__ import annotations
import re
from typing import Any

try:  # prefer the real validator when available
    import jsonschema as _js  # type: ignore

    def validate(instance: Any, schema: dict) -> list[str]:
        v = _js.Draft7Validator(schema)
        return [f"{'/'.join(map(str, e.path))}: {e.message}" for e in v.iter_errors(instance)]

except Exception:  # pragma: no cover - fallback path is the common one here
    _TYPES = {
        "object": dict, "array": list, "string": str,
        "integer": int, "number": (int, float), "boolean": bool, "null": type(None),
    }
    _DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    _URI = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://")

    def _type_ok(value: Any, t: str) -> bool:
        if t == "integer" and isinstance(value, bool):
            return False
        if t == "number" and isinstance(value, bool):
            return False
        return isinstance(value, _TYPES[t])

    def _check(value: Any, schema: dict, path: str, errors: list[str]) -> None:
        t = schema.get("type")
        if t is not None:
            types = t if isinstance(t, list) else [t]
            if not any(_type_ok(value, x) for x in types):
                errors.append(f"{path or '<root>'}: expected type {t}, got {type(value).__name__}")
                return
        if "enum" in schema and value not in schema["enum"]:
            errors.append(f"{path or '<root>'}: {value!r} not in enum {schema['enum']}")
        if isinstance(value, str):
            if "pattern" in schema and not re.search(schema["pattern"], value):
                errors.append(f"{path}: {value!r} does not match pattern {schema['pattern']}")
            if "minLength" in schema and len(value) < schema["minLength"]:
                errors.append(f"{path}: shorter than minLength {schema['minLength']}")
            fmt = schema.get("format")
            if fmt == "date" and not _DATE.match(value):
                errors.append(f"{path}: {value!r} is not an ISO date")
            if fmt == "uri" and not _URI.match(value):
                errors.append(f"{path}: {value!r} is not a URI")
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            if "minimum" in schema and value < schema["minimum"]:
                errors.append(f"{path}: {value} < minimum {schema['minimum']}")
            if "maximum" in schema and value > schema["maximum"]:
                errors.append(f"{path}: {value} > maximum {schema['maximum']}")
        if isinstance(value, list):
            if "minItems" in schema and len(value) < schema["minItems"]:
                errors.append(f"{path}: fewer than minItems {schema['minItems']}")
            if "items" in schema:
                for i, item in enumerate(value):
                    _check(item, schema["items"], f"{path}[{i}]", errors)
        if isinstance(value, dict):
            props = schema.get("properties", {})
            for req in schema.get("required", []):
                if req not in value:
                    errors.append(f"{path or '<root>'}: missing required property '{req}'")
            if schema.get("additionalProperties") is False:
                for key in value:
                    if key not in props:
                        errors.append(f"{path or '<root>'}: additional property '{key}' not allowed")
            for key, sub in props.items():
                if key in value:
                    _check(value[key], sub, f"{path}/{key}" if path else key, errors)

    def validate(instance: Any, schema: dict) -> list[str]:
        errors: list[str] = []
        _check(instance, schema, "", errors)
        return errors
