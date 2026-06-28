"""Contextual recommendation engine.

Recommends a pattern/effect for a specific application context, never a universally
"best" source. Reuses the transparent ranking engine and returns an explainable record.
"""
from __future__ import annotations
from motif import rank as rank_mod, registry


def recommend(pattern_id: str, profile: str = "saas-balanced") -> dict:
    rec, rej = rank_mod.rank_for_pattern(pattern_id, profile)
    pat = next((r.data for r in registry.load_records("patterns") if r.data["id"] == pattern_id), None)
    if pat is None:
        return {"error": f"no pattern '{pattern_id}'"}
    best = rec[0] if rec else None
    confidence = 0.9 if best and best.score > 2 else 0.7 if best else 0.4
    return {
        "pattern": pattern_id,
        "selected_effect": best.id if best else None,
        "confidence": round(confidence, 2),
        "profile": profile,
        "reasons": (best.reasons if best else ["no ranked candidate"]),
        "alternatives": [s.id for s in rec[1:3]],
        "rejected": [s.id for s in rej],
        "accessibility_requirements": pat.get("accessibility_requirements", []),
    }
