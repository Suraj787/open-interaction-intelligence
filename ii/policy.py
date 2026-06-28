"""Policy as code.

A project policy (motif-policy.yml) sets blocking thresholds for accessibility,
dependencies, originality, performance, interface debt, and human-review domains.
Policies affect the CLI, Guardian, compiler, and Atlas recommendations through one
deterministic checker.
"""
from __future__ import annotations
import json
import pathlib
from motif import yaml_min

DEFAULT = {
    "version": 1,
    "policies": {
        "accessibility": {"minimum": "wcag-2.2-aa", "blocking_severity": ["critical", "high"]},
        "dependencies": {"new_runtime_dependencies": "approval-required"},
        "originality": {"maximum_convergence_score": 55},
        "performance": {"max_ui_bundle_delta_kb": 20, "max_inp_ms": 200},
        "interface_debt": {"maximum_score": 30},
        "human_review": {"required_for": ["healthcare", "financial-approval", "destructive-bulk-action"]},
    },
}


def policy_path(target) -> pathlib.Path:
    return pathlib.Path(target) / "motif-policy.yml"


def load(target) -> dict:
    p = policy_path(target)
    if p.exists():
        try:
            return yaml_min.load(p.read_text()) or DEFAULT
        except Exception:  # noqa: BLE001
            return DEFAULT
    return DEFAULT


def init(target) -> pathlib.Path:
    p = policy_path(target)
    if not p.exists():
        p.write_text(_DEFAULT_YAML)
    return p


def check(target, findings: list[dict], debt_score: int | None = None,
          originality_score: int | None = None) -> dict:
    pol = load(target).get("policies", {})
    blocking_sev = set(pol.get("accessibility", {}).get("blocking_severity", ["critical", "high"]))
    violations: list[dict] = []
    warnings: list[dict] = []

    for f in findings:
        if f.get("status") in ("accepted-risk", "false-positive", "fixed", "verified"):
            continue
        if f.get("type") == "accessibility" and f.get("severity") in blocking_sev:
            violations.append({"policy": "accessibility.blocking_severity", "finding": f["id"],
                               "detail": f"{f['severity']} {f.get('rule')}"})
        elif f.get("severity") in ("critical", "high"):
            warnings.append({"policy": "severity", "finding": f["id"]})

    if debt_score is not None:
        cap = pol.get("interface_debt", {}).get("maximum_score", 100)
        if debt_score > cap:
            violations.append({"policy": "interface_debt.maximum_score",
                               "detail": f"debt {debt_score} > {cap}"})
    if originality_score is not None:
        cap = pol.get("originality", {}).get("maximum_convergence_score", 100)
        if originality_score > cap:
            violations.append({"policy": "originality.maximum_convergence_score",
                               "detail": f"convergence {originality_score} > {cap}"})

    return {"violations": violations, "warnings": warnings,
            "blocking": bool(violations), "policy": pol}


def explain(target) -> list[str]:
    pol = load(target).get("policies", {})
    out = ["# Active policy"]
    for area, rules in pol.items():
        out.append(f"  {area}:")
        for k, v in (rules.items() if isinstance(rules, dict) else []):
            out.append(f"    {k}: {v}")
    return out


_DEFAULT_YAML = """# Motif policy as code. Affects CLI, Guardian, compiler, and Atlas recommendations.
version: 1
policies:
  accessibility:
    minimum: wcag-2.2-aa
    blocking_severity:
      - critical
      - high
  dependencies:
    new_runtime_dependencies: approval-required
  originality:
    maximum_convergence_score: 55
  performance:
    max_ui_bundle_delta_kb: 20
    max_inp_ms: 200
  interface_debt:
    maximum_score: 30
  human_review:
    required_for:
      - healthcare
      - financial-approval
      - destructive-bulk-action
"""
