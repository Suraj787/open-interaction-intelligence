"""Security scanners must catch the malicious fixtures and pass the clean one."""
from motif import scan as scan_mod
from motif.registry import ROOT

FIX = ROOT / "evals" / "fixtures"


def _codes(findings):
    return {f.code for f in findings}


def test_eval_button_rejected():
    findings = scan_mod.scan_all(FIX / "eval-button")
    codes = _codes(findings)
    assert "eval" in codes
    assert "cookies" in codes
    assert "no-license-file" in codes or "unknown-license" in codes
    assert scan_mod.verdict(findings) == "reject"


def test_postinstall_rejected():
    findings = scan_mod.scan_all(FIX / "postinstall-pkg")
    codes = _codes(findings)
    assert "lifecycle-script" in codes
    assert "typosquat" in codes
    assert scan_mod.verdict(findings) == "reject"


def test_remote_loader_flagged():
    findings = scan_mod.scan_all(FIX / "remote-loader")
    codes = _codes(findings)
    assert "remote-script" in codes
    assert "analytics" in codes or "beacon" in codes
    assert scan_mod.verdict(findings) in ("reject", "review")


def test_secret_leak_detected():
    findings = scan_mod.scan_all(FIX / "private-key-leak")
    codes = _codes(findings)
    assert "private-key" in codes
    assert "github-token" in codes
    assert scan_mod.verdict(findings) == "reject"


def test_safe_component_passes():
    findings = scan_mod.scan_all(FIX / "safe-component")
    # No critical/high findings; MIT detected.
    assert scan_mod.verdict(findings) == "pass"
    assert "license-detected" in _codes(findings)


def test_unknown_license_gate():
    from scanners import license_scanner
    bundleable, klass = license_scanner.classify("UNKNOWN")
    assert bundleable is False
    assert klass == "reference-only"


def test_commons_clause_not_permissive():
    from scanners import license_scanner
    spdx = license_scanner.detect_license("Commons Clause License Condition v1.0 ...")
    assert spdx == "LicenseRef-Commons-Clause"
    assert license_scanner.classify(spdx)[0] is False
