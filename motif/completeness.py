"""Source-by-source component completeness report (Phase 3)."""
from __future__ import annotations
from . import registry

MODES = ["bundled", "installable", "adaptable", "reference-only", "rejected"]


def report() -> dict:
    comps = registry.load_records("components")
    sources = {r.data["id"]: r.data for r in registry.load_records("sources")}
    per_source: dict[str, dict] = {}
    for sid in sources:
        per_source[sid] = {"discovered": 0, **{m: 0 for m in MODES}, "verified": 0}
    for c in comps:
        d = c.data
        s = d["source"]
        bucket = per_source.setdefault(s, {"discovered": 0, **{m: 0 for m in MODES}, "verified": 0})
        bucket["discovered"] += 1
        mode = d.get("usability_mode")
        if mode in bucket:
            bucket[mode] += 1
        if d.get("quality_status") in ("high", "medium") and mode != "rejected":
            bucket["verified"] += 1
    totals = {"discovered": len(comps), **{m: sum(1 for c in comps if c.data.get("usability_mode") == m) for m in MODES}}
    return {"per_source": per_source, "totals": totals}
