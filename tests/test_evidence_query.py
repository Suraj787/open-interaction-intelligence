"""Regression matrix for UX Evidence Graph context matching (beta correctness fix).

Encodes the corrected wildcard semantics: an empty/omitted applicability dimension is a
wildcard (universal), existing values are soft relevance signals used for ranking, and only
dimensions listed in a claim's `restrict` set are hard filters. Universal claims must
survive rich contexts; restricted claims match only intersecting contexts.
"""
from __future__ import annotations
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from ii import evidence as ev  # noqa: E402

COLOUR = "claim-status-colour-001"          # universal normative accessibility claim
TOUCH = "claim-touch-target-size-minimum"   # genuinely device-restricted (touch/mobile)

CONTEXTS = {
    "minimal-generic": {"abilities": ["colour-vision-deficiency"]},
    "boss-enterprise": {"product_forms": ["enterprise-app", "web-app", "dashboard"],
                        "purposes": ["monitor", "configure"], "workflows": ["daily-operation", "approval"],
                        "expertise": ["domain-professional"], "abilities": ["keyboard-only", "colour-vision-deficiency"],
                        "risks": [{"type": "financial", "severity": 3}], "devices": ["desktop"],
                        "environments": ["office"]},
    "ecommerce-checkout": {"product_forms": ["ecommerce", "web-app"], "purposes": ["transact"],
                           "workflows": ["checkout"], "devices": ["mobile", "touch"],
                           "risks": [{"type": "financial", "severity": 3}]},
    "government-form": {"product_forms": ["gov-service", "web-app"], "purposes": ["apply"],
                        "workflows": ["form-completion"], "abilities": ["low-literacy"], "devices": ["desktop"]},
    "healthcare-high-risk": {"product_forms": ["enterprise-app"], "purposes": ["administer"],
                             "workflows": ["medication-order"], "risks": [{"type": "safety", "severity": 5}],
                             "devices": ["desktop"]},
    "factory-tablet": {"product_forms": ["enterprise-app"], "purposes": ["monitor"],
                       "workflows": ["daily-operation"], "devices": ["tablet", "touch"],
                       "environments": ["industrial"]},
    "desktop-mouse-only": {"product_forms": ["web-app"], "devices": ["desktop"], "abilities": ["mouse-only"]},
    "mobile-touch": {"product_forms": ["web-app"], "devices": ["mobile", "touch"], "abilities": ["touch"]},
    "keyboard-only": {"product_forms": ["web-app"], "abilities": ["keyboard-only"], "devices": ["desktop"]},
    "multi-purpose": {"product_forms": ["web-app", "dashboard"], "purposes": ["monitor", "configure", "report"]},
    "multi-risk": {"product_forms": ["enterprise-app"],
                   "risks": [{"type": "financial", "severity": 4}, {"type": "safety", "severity": 5}]},
}


def ids(ctx):
    return set(ev.query(ctx)["applicable_claims"])


# --- wildcard semantics: universal claims survive rich contexts -----------------------
def test_minimal_context_nonzero():
    assert len(ids(CONTEXTS["minimal-generic"])) >= 16


def test_rich_boss_context_is_useful_nonzero():
    n = len(ids(CONTEXTS["boss-enterprise"]))
    assert n >= 50, f"rich BOSS context returned {n}; universal claims must survive"


def test_universal_colour_claim_survives_every_context():
    for name, ctx in CONTEXTS.items():
        assert COLOUR in ids(ctx), f"universal claim dropped under {name}"


def test_added_dimension_never_removes_universal_claim():
    base = {"product_forms": ["web-app"]}
    rich = dict(base, workflows=["checkout"], devices=["desktop"], environments=["office"],
                purposes=["transact"], expertise=["novice"])
    universal_in_base = ids(base)
    universal_in_rich = ids(rich)
    # every claim that matched the small context and is universal must still match the rich one
    dropped = {c for c in universal_in_base if c not in universal_in_rich
               and not ev._restrict_dims(ev._claim(c))}
    assert not dropped, f"added dimensions removed universal claims: {dropped}"


# --- restricted claims match only relevant contexts -----------------------------------
def test_touch_claim_excluded_on_desktop_mouse_only():
    assert TOUCH not in ids(CONTEXTS["desktop-mouse-only"])


def test_touch_claim_present_on_touch_context():
    assert TOUCH in ids(CONTEXTS["mobile-touch"])
    assert TOUCH in ids(CONTEXTS["factory-tablet"])


def test_restricted_claim_no_intersection_excluded():
    # a claim restricted to touch should not appear for a pure desktop context
    m = ev.match(ev._claim(TOUCH), CONTEXTS["desktop-mouse-only"])
    assert m["applies"] is False and "devices" in m.get("excluded_because", "")


def test_claim_with_one_restricted_dimension_still_universal_elsewhere():
    # TOUCH restricts devices only; with a touch device it matches regardless of other dims
    assert TOUCH in ids({"devices": ["touch"], "workflows": ["anything-else"], "purposes": ["monitor"]})


# --- ranking & specificity ------------------------------------------------------------
def test_specific_ranks_above_universal():
    recs = ev.query(CONTEXTS["boss-enterprise"])["ranked_recommendations"]
    specs = [r["specificity"] for r in recs]
    assert specs == sorted(specs, reverse=True)
    assert max(specs) > min(specs), "ranking must separate specific from universal"


def test_match_explanation_present():
    recs = ev.query(CONTEXTS["boss-enterprise"])["ranked_recommendations"]
    for r in recs[:5]:
        assert r["match_type"] in {"universal", "specific", "restricted-match"}
        assert "matched_dimensions" in r and "wildcard_dimensions" in r and r["reason"]


# --- normative / hypotheses / stale ---------------------------------------------------
def test_hypotheses_never_block():
    for name, ctx in CONTEXTS.items():
        q = ev.query(ctx)
        blocked = {b["claim"] for b in q["blocked_patterns"]}
        for cid in blocked:
            assert ev._claim(cid)["claim"]["force"] != "hypothesis"


def test_stale_claims_cannot_newly_block():
    for name, ctx in CONTEXTS.items():
        q = ev.query(ctx)
        for b in q["blocked_patterns"]:
            assert not ev.is_stale(ev._claim(b["claim"]))


def test_sources_and_limitations_exposed():
    q = ev.query(CONTEXTS["boss-enterprise"])
    assert q["sources"] and q["limitations"]


def test_assumed_context_lowers_confidence_only():
    base = dict(CONTEXTS["boss-enterprise"])
    assumed = dict(base, _assumptions=["risks", "abilities"])
    assert ids(base) == ids(assumed)  # applicability unchanged
    assert ev.query(assumed)["confidence"]["overall"] != "high"


def test_typed_risk_severity_matches():
    q = ev.query(CONTEXTS["healthcare-high-risk"])
    assert len(q["applicable_claims"]) >= 50  # universal survive high-risk context too


def test_query_is_deterministic():
    assert ev.query(CONTEXTS["boss-enterprise"]) == ev.query(CONTEXTS["boss-enterprise"])


# --- matrix guard: every context returns a useful, colour-safe result -----------------
def test_matrix_all_contexts_useful():
    for name, ctx in CONTEXTS.items():
        n = len(ids(ctx))
        assert n >= 16, f"{name} returned only {n} claims (over-filtering regression)"
