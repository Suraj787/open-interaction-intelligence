"""Motif UX Evidence Graph: load, validate, index, and deterministically query.

A version-controlled evidence layer (flat JSON under ux-evidence/), not a graph database
and not a UX encyclopedia. The query engine takes a screen/workflow context vector and
returns applicable claims with explicit merge rules, conflicts, sources, and limitations.
Evidence never becomes authority without a matching context, a source, a tier, a
confidence, limitations, and a validation method.
"""
from __future__ import annotations
import json
import pathlib
import datetime
from motif import registry, jsonschema_min

ROOT = registry.ROOT
UXE = ROOT / "ux-evidence"
SCHEMAS = UXE / "schemas"

KINDS = {
    "claims": "evidence-claim.schema.json",
    "sources": "source.schema.json",
    "myths": "myth.schema.json",
    "contradictions": "contradiction.schema.json",
    "validations": "validation-method.schema.json",
    "packs": "evidence-pack.schema.json",
}

_DIMS = ("product_forms", "purposes", "workflows", "expertise", "abilities",
         "devices", "environments", "audience_roles")


def _load(kind):
    d = UXE / kind
    if not d.exists():
        return []
    return [json.loads(p.read_text()) for p in sorted(d.glob("*.json"))]


def load_claims():
    return _load("claims")


def _schema(name):
    return json.loads((SCHEMAS / name).read_text())


def validate() -> tuple[dict, list[str]]:
    counts, errors = {}, []
    for kind, schema_name in KINDS.items():
        schema = _schema(schema_name)
        recs = _load(kind)
        counts[kind] = len(recs)
        seen = set()
        for r in recs:
            rid = r.get("id", "?")
            for e in jsonschema_min.validate(r, schema):
                errors.append(f"{kind}/{rid}: {e}")
            if rid in seen:
                errors.append(f"{kind}/{rid}: duplicate id")
            seen.add(rid)
    # referential: claim sources exist; pack claim_ids/myths exist
    src_ids = {s["id"] for s in _load("sources")}
    claim_ids = {c["id"] for c in load_claims()}
    for c in load_claims():
        for s in c.get("evidence", {}).get("sources", []):
            if s not in src_ids:
                errors.append(f"claims/{c['id']}: source '{s}' not found")
    return counts, errors


def _today():
    return datetime.date.today().isoformat()


def is_stale(claim) -> bool:
    fr = claim.get("freshness", {})
    if fr.get("status") != "current":
        return True
    ra = fr.get("review_after")
    return bool(ra and ra < _today())


def _ctx_risks(ctx):
    out = set()
    for r in ctx.get("risks", []) or []:
        out.add(r["type"] if isinstance(r, dict) else r)
    return out


def applies(claim, ctx) -> tuple[bool, int]:
    """Return (applies, specificity).

    A claim narrows only on dimensions the context actually specifies: if the context is
    silent on a dimension, the claim still applies (it is simply less context-specific).
    A claim is excluded only when both the claim and the context constrain a dimension and
    they do not overlap. Specificity counts the dimensions that matched concretely.
    """
    ap = claim.get("applicability", {})
    spec = 0
    for dim in _DIMS:
        cv = set(ap.get(dim, []) or [])
        ctxv = set(ctx.get(dim, []) or [])
        if cv and ctxv:
            if not (cv & ctxv):
                return False, 0
            spec += 1
    cr = set(ap.get("risks", []) or [])
    ctxr = _ctx_risks(ctx)
    if cr and ctxr:
        if not (cr & ctxr):
            return False, 0
        spec += 1
    return True, spec


def _blocking(claim) -> bool:
    ev = claim.get("evidence", {})
    return (claim["claim"]["force"] == "normative" and ev.get("tier") == 1
            and ev.get("confidence") == "high" and not is_stale(claim))


def query(ctx: dict) -> dict:
    claims = load_claims()
    matched = []
    for c in claims:
        ok, spec = applies(c, ctx)
        if ok:
            matched.append((spec, c))
    matched.sort(key=lambda x: (-x[0], x[1]["evidence"]["tier"]))

    applicable, recs, warnings, blocked, validations, sources, limitations = [], [], [], [], set(), set(), []
    for spec, c in matched:
        force = c["claim"]["force"]
        stale = is_stale(c)
        applicable.append(c["id"])
        sources.update(c.get("evidence", {}).get("sources", []))
        limitations.extend(c.get("evidence", {}).get("limitations", []))
        validations.update(c.get("validation", {}).get("methods", []))
        do = c.get("recommendation", {}).get("do", [])
        if force == "hypothesis":
            warnings.append({"claim": c["id"], "why": "hypothesis (never blocks)"})
        elif stale:
            warnings.append({"claim": c["id"], "why": "stale claim cannot newly block"})
        if _blocking(c) and not stale:
            blocked.append({"claim": c["id"], "category": c["claim"]["category"],
                            "requirement": c["claim"]["statement"]})
        recs.append({"claim": c["id"], "force": force, "specificity": spec,
                     "tier": c["evidence"]["tier"], "do": do})

    # conflicts: contradictions whose topic-category appears among matched categories
    cats = {c[1]["claim"]["category"] for c in matched}
    conflicts = []
    for ct in _load("contradictions"):
        if any(cat in (ct.get("topic", "") + " ".join(ct.get("competing_claims", []))) for cat in cats):
            conflicts.append({"id": ct["id"], "topic": ct["topic"],
                              "resolution_type": ct.get("resolution_type"),
                              "human_decision_required": ct.get("human_decision_required", False)})

    # confidence: high if any tier-1 normative applies and no critical assumption
    assumptions = set(ctx.get("_assumptions", []) or [])
    critical_assumed = bool(assumptions & {"risks", "abilities"})
    has_norm = any(_blocking(c) for _, c in matched)
    overall = "high" if (has_norm and not critical_assumed) else ("medium" if matched else "low")

    return {
        "applicable_claims": applicable,
        "ranked_recommendations": recs[:30],
        "warnings": warnings,
        "blocked_patterns": blocked,
        "required_validations": sorted(validations),
        "confidence": {"overall": overall,
                       "note": "lowered: critical context (risk/abilities) is an assumption" if critical_assumed else ""},
        "conflicts": conflicts,
        "sources": sorted(sources),
        "limitations": limitations[:20],
    }


def explain(claim_id: str) -> dict:
    c = next((x for x in load_claims() if x["id"] == claim_id), None)
    if not c:
        return {"error": f"no claim '{claim_id}'"}
    return {
        "id": c["id"], "statement": c["claim"]["statement"],
        "force": c["claim"]["force"], "category": c["claim"]["category"],
        "tier": c["evidence"]["tier"], "sources": c["evidence"]["sources"],
        "confidence": c["evidence"]["confidence"], "stale": is_stale(c),
        "limitations": c["evidence"].get("limitations", []),
        "validation": c.get("validation", {}).get("methods", []),
        "blocking": _blocking(c),
        "legal": c.get("legal", {}),
    }


def check_myth(text: str) -> dict:
    t = text.lower().replace("-", " ")
    for m in _load("myths"):
        hay = (m["id"] + " " + m["statement"]).lower().replace("-", " ")
        if t in hay or any(w in hay for w in t.split() if len(w) > 4):
            return {"id": m["id"], "statement": m["statement"], "disposition": m["disposition"],
                    "replacement": m["replacement_principle"],
                    "evidence_against": m.get("evidence_against", []),
                    "still_applies_when": m.get("still_applies_when", [])}
    return {"match": None, "note": "no matching myth in the register"}


def stale_claims() -> list[str]:
    return [c["id"] for c in load_claims() if is_stale(c)]


def build_index() -> pathlib.Path:
    idx = {"counts": {k: len(_load(k)) for k in KINDS},
           "by_category": {}, "by_tier": {}, "by_force": {}}
    for c in load_claims():
        idx["by_category"].setdefault(c["claim"]["category"], []).append(c["id"])
        idx["by_tier"].setdefault(str(c["evidence"]["tier"]), []).append(c["id"])
        idx["by_force"].setdefault(c["claim"]["force"], []).append(c["id"])
    (UXE / "indexes").mkdir(parents=True, exist_ok=True)
    out = UXE / "indexes" / "index.json"
    out.write_text(json.dumps(idx, indent=2) + "\n")
    return out
