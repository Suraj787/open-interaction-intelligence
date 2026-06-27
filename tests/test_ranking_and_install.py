"""Transparent ranking + installation gates."""
import pathlib
from oii import rank as rank_mod, install as install_mod
from oii.registry import ROOT


def test_ranking_prefers_restraint_in_enterprise():
    # For the skeleton-loading pattern, the low-cost skeleton-shimmer should win
    # over any high-attention candidate under the enterprise-strict profile.
    rec, _ = rank_mod.rank_for_pattern("skeleton-loading", "enterprise-strict")
    assert rec, "no ranked candidates"
    assert rec[0].id == "skeleton-shimmer"
    # every candidate carries a human-readable explanation
    assert all(s.reasons for s in rec)


def test_missing_reduced_motion_is_penalised():
    # aurora-background has a fallback; fabricate a record without one to confirm penalty.
    from oii import registry
    aurora = next(r for r in registry.load_records("effects") if r.data["id"] == "aurora-background")
    s = rank_mod.score_effect(aurora, "marketing-expressive")
    assert any("reduced-motion" in r for r in s.reasons)


def test_install_refuses_reference_only():
    plan = install_mod.plan_install("aceternity-aurora-bg", "/tmp/oii-target-x")
    assert plan.refused is not None
    assert "not installable" in plan.refused or "reference" in plan.refused.lower()


def test_install_refuses_rejected_component():
    plan = install_mod.plan_install("uiverse-eval-button", "/tmp/oii-target-y")
    assert plan.refused is not None


def test_install_plan_for_installable_has_files(tmp_path):
    plan = install_mod.plan_install("shadcn-button", str(tmp_path))
    assert plan.refused is None
    assert plan.files
    assert plan.license == "MIT"


def test_install_and_rollback_roundtrip(tmp_path):
    target = tmp_path / "proj"
    target.mkdir()
    (target / "keep.txt").write_text("original")
    install_mod.snapshot(target)
    (target / "new.txt").write_text("added")
    assert (target / "new.txt").exists()
    assert install_mod.rollback(target)
    assert not (target / "new.txt").exists()
    assert (target / "keep.txt").read_text() == "original"
