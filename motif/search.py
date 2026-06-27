"""Search across registry records — offline, substring + field match."""
from __future__ import annotations
from . import registry


def _haystack(rec: registry.Record) -> str:
    d = rec.data
    parts = [str(d.get(k, "")) for k in ("id", "name", "objective", "problem", "category")]
    for k in ("tags", "user_intent", "suitable_pages", "frameworks", "contexts"):
        v = d.get(k)
        if isinstance(v, list):
            parts.extend(map(str, v))
    return " ".join(parts).lower()


def search(query: str, kinds: list[str] | None = None) -> list[registry.Record]:
    q = query.lower().strip()
    kinds = kinds or list(registry.KINDS)
    hits: list[registry.Record] = []
    for kind in kinds:
        for rec in registry.load_records(kind):
            if not q or q in _haystack(rec):
                hits.append(rec)
    return hits


def alternatives(effect_or_component_id: str) -> list[registry.Record]:
    """Find records in the same effect category (the dedup/canonical surface)."""
    target = None
    for rec in registry.load_records("effects"):
        if rec.data["id"] == effect_or_component_id:
            target = rec
            break
    if target is None:
        return []
    cat = target.data.get("category")
    return [r for r in registry.load_records("effects")
            if r.data.get("category") == cat and r.data["id"] != effect_or_component_id]
