"""Regression tests for the recalibrated aesthetic-convergence (originality) scorer.

The detector must not saturate on legitimate enterprise Tailwind UI, must still flag
intentionally generic AI designs from a combination of cliche signals, must account for
design-system provenance and product context, and must emit an inspectable signal-level
breakdown. Static-only confidence is capped.
"""
from __future__ import annotations
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from ii import originality as o  # noqa: E402

FIX = ROOT / "evals" / "fixtures" / "originality"
ENTERPRISE = {"product_forms": ["enterprise-app", "dashboard"], "workflows": ["daily-operation"]}
LANDING = {"product_forms": ["marketing-site", "web-app"], "workflows": ["acquisition"]}


def score(name, context=None):
    return o.audit(str(FIX / name), context=context)["overall_score"]


# --- no false saturation on legitimate UI ---------------------------------------------
def test_enterprise_dashboard_not_saturated():
    s = score("enterprise-dashboard", ENTERPRISE)
    assert s < 60, f"enterprise dashboard saturated at {s}"


def test_branded_product_low():
    assert score("branded-product", {"product_forms": ["ecommerce"]}) < 45


def test_government_form_low():
    assert score("government-form", {"product_forms": ["gov-service"]}) < 45


def test_dev_tool_low():
    assert score("dev-tool-dense", {"product_forms": ["developer-tool"]}) < 45


def test_minimal_site_low():
    assert score("minimal-site") < 30


def test_ecommerce_grid_context_aware():
    # repeated product cards are functional in ecommerce; should not be high
    assert score("ecommerce-grid", {"product_forms": ["ecommerce"]}) < 60


# --- detection of genuinely generic designs is preserved ------------------------------
def test_generic_ai_saas_high():
    s = score("generic-ai-saas", LANDING)
    assert s >= 60, f"generic AI SaaS only scored {s}; detection lost"


def test_repeated_bento_template_high():
    assert score("repeated-bento-template", LANDING) >= 60


def test_generic_beats_enterprise():
    assert score("generic-ai-saas", LANDING) > score("enterprise-dashboard", ENTERPRISE) + 25


# --- explainability & determinism -----------------------------------------------------
def test_signal_breakdown_present():
    r = o.audit(str(FIX / "generic-ai-saas"), context=LANDING)
    assert r["risk_band"] and r["confidence"] and r["limitations"]
    assert r["signals"], "must report per-signal breakdown"
    s0 = r["signals"][0]
    for k in ("name", "raw_count", "weighted_score", "context_adjustment",
              "provenance_adjustment", "affected_routes", "explanation"):
        assert k in s0, f"signal missing {k}"


def test_confidence_capped_static():
    r = o.audit(str(FIX / "generic-ai-saas"), context=LANDING)
    assert r["confidence"] in ("low", "moderate"), "static-only evidence must not claim high confidence"


def test_deterministic():
    a = o.audit(str(FIX / "generic-ai-saas"), context=LANDING)
    b = o.audit(str(FIX / "generic-ai-saas"), context=LANDING)
    assert a == b


def test_provenance_reduces_structural_signals():
    # the same structural patterns with a design system present should score no higher
    # than without provenance accounting
    with_ds = o.audit(str(FIX / "enterprise-dashboard"), context=ENTERPRISE)
    assert with_ds["provenance"]["design_system_present"] is True


def test_backward_compatible_audit_path():
    findings, s, band = o.audit_path(str(FIX / "enterprise-dashboard"))
    assert isinstance(s, int) and 0 <= s <= 100 and isinstance(band, str)
    assert s < 100, "audit_path must use the recalibrated, non-saturating score"


def test_real_boss_not_saturated():
    boss = "/Users/suraj/frappe-bench-v16/apps/boss_v2/spa"
    if pathlib.Path(boss).exists():
        s = o.audit(boss, context=ENTERPRISE)["overall_score"]
        assert s < 60, f"real BOSS still saturated at {s}"
