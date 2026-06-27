"""Transparent ranking of effect candidates.

Scores reward the priority order (usability → comprehension → feedback →
continuity → accessibility → performance → maintainability → product identity →
novelty) and apply explicit penalties. Every score ships with a human-readable
explanation of why a candidate was preferred or demoted. Nothing is a black box.
"""
from __future__ import annotations
from dataclasses import dataclass
from . import registry

# Quality-profile weighting: how much each profile cares about restraint.
PROFILES = {
    "enterprise-strict": {"distraction": 4.0, "perf": 2.0, "novelty": 0.2},
    "saas-balanced": {"distraction": 2.0, "perf": 1.5, "novelty": 1.0},
    "marketing-expressive": {"distraction": 1.0, "perf": 1.2, "novelty": 1.6},
    "accessibility-first": {"distraction": 4.0, "perf": 2.0, "novelty": 0.1},
    "low-power-device": {"distraction": 3.0, "perf": 4.0, "novelty": 0.2},
    "documentation-calm": {"distraction": 4.0, "perf": 2.0, "novelty": 0.2},
}
DEFAULT_PROFILE = "saas-balanced"

_COST = {"low": 0.0, "medium": 1.0, "high": 2.0}
_RISK = {"low": 0.0, "medium": 1.5, "high": 3.0}
_SUIT = {"recommended": 2.0, "conditional": 0.5, "discouraged": -2.0}


@dataclass
class Scored:
    record: registry.Record
    score: float
    reasons: list[str]

    @property
    def id(self) -> str:
        return self.record.data["id"]


def _is_marketing(profile: str) -> bool:
    return "marketing" in profile or "editorial" in profile or "portfolio" in profile


def score_effect(rec: registry.Record, profile: str) -> Scored:
    d = rec.data
    w = PROFILES.get(profile, PROFILES[DEFAULT_PROFILE])
    reasons: list[str] = []
    score = 0.0

    # Priority: product-fit / usability via enterprise|marketing suitability
    suit_key = "marketing_suitability" if _is_marketing(profile) else "enterprise_suitability"
    suit = d.get(suit_key, "conditional")
    score += _SUIT.get(suit, 0.0)
    reasons.append(f"{suit_key}={suit} ({_SUIT.get(suit, 0):+.1f})")

    # Accessibility risk penalty
    a11y = d.get("accessibility_risk", "medium")
    pen = _RISK.get(a11y, 1.5)
    score -= pen
    if pen:
        reasons.append(f"accessibility_risk={a11y} (-{pen:.1f})")

    # Performance / continuous-rendering penalty, weighted by profile
    cost = d.get("performance_cost", "medium")
    pen = _COST.get(cost, 1.0) * w["perf"]
    score -= pen
    if pen:
        reasons.append(f"performance_cost={cost} (-{pen:.1f} ×{w['perf']} profile)")

    # Distraction penalty: high-attention ambient categories
    if d.get("category") in ("backgrounds", "cards") and cost != "low":
        pen = w["distraction"]
        score -= pen
        reasons.append(f"high-attention/{d.get('category')} distraction (-{pen:.1f})")

    # Reduced-motion readiness reward (must have a real fallback)
    if d.get("reduced_motion_fallback", "").strip():
        score += 1.0
        reasons.append("has reduced-motion fallback (+1.0)")
    else:
        score -= 3.0
        reasons.append("MISSING reduced-motion fallback (-3.0)")

    # Dependency weight penalty
    if d.get("dependencies"):
        pen = 1.0 * len(d["dependencies"])
        score -= pen
        reasons.append(f"adds {len(d['dependencies'])} dependency(ies) (-{pen:.1f})")
    else:
        score += 0.5
        reasons.append("dependency-free (+0.5)")

    # Mobile suitability penalty
    if d.get("mobile_suitability") == "poor":
        score -= 1.5
        reasons.append("poor mobile suitability (-1.5)")

    # Novelty is the LOWEST priority and never decisive
    score += 0.2 * w["novelty"]

    return Scored(rec, round(score, 2), reasons)


def rank_candidates(candidate_ids: list[str], profile: str = DEFAULT_PROFILE) -> list[Scored]:
    by_id = {r.data["id"]: r for r in registry.load_records("effects")}
    scored = [score_effect(by_id[i], profile) for i in candidate_ids if i in by_id]
    return sorted(scored, key=lambda s: s.score, reverse=True)


def rank_for_pattern(pattern_id: str, profile: str = DEFAULT_PROFILE) -> tuple[list[Scored], list[Scored]]:
    """Rank a pattern's recommended effects; also surface its rejected effects."""
    pat = next((r for r in registry.load_records("patterns") if r.data["id"] == pattern_id), None)
    if pat is None:
        return [], []
    rec = rank_candidates(pat.data.get("recommended_effects", []), profile)
    rej = rank_candidates(pat.data.get("rejected_effects", []), profile)
    return rec, rej
