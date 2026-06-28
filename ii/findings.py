"""Unified Finding model and lifecycle.

One schema and lifecycle for every finding (accessibility, performance, security,
design-system drift, originality, state completeness, duplication, licence, etc.).
Findings are produced by the deterministic auditors (originality, debt, state, scanners,
design-system) and stored under <target>/.motif/findings/.
"""
from __future__ import annotations
import json
import re
import pathlib
from . import runtime, originality as orig_mod, debt as debt_mod

VALID_STATUS = ["open", "acknowledged", "accepted-risk", "planned", "fixed",
                "verified", "regressed", "false-positive"]


def _dir(target):
    return runtime.state_root(target) / "findings"


def load(target) -> list[dict]:
    d = _dir(target)
    if not d.exists():
        return []
    return [json.loads(p.read_text()) for p in sorted(d.glob("finding-*.json"))]


def save(target, finding: dict) -> pathlib.Path:
    runtime.ensure_state(target)
    out = _dir(target) / f"{finding['id']}.json"
    out.write_text(json.dumps(finding, indent=2) + "\n")
    return out


def _mk(idx, ftype, rule, severity, conf, recs, location, detected_by="static") -> dict:
    return {"id": f"finding-{idx:04d}", "type": ftype, "rule": rule, "severity": severity,
            "confidence": conf, "location": location, "recommendations": recs,
            "status": "open", "detected_by": detected_by, "evidence": {}, "impact": {}}


# Heuristic static finding rules over a component file's text.
_RULES = [
    ("accessibility", "status-colour-only", "high", 0.7,
     re.compile(r"(?i)status[^\n]*(?:bg|background|color)[-:][^\n]*(?:red|green|amber|yellow)"),
     ["Add a text label or icon so status is not conveyed by colour alone"]),
    ("accessibility", "focus-outline-removed", "high", 0.8,
     re.compile(r"outline:\s*none|outline-none"),
     ["Restore a visible focus indicator (focus-visible)"]),
    ("accessibility", "missing-reduced-motion", "medium", 0.6, None,
     ["Guard animation with @media (prefers-reduced-motion: reduce)"]),
    ("design-system", "arbitrary-value", "medium", 0.7,
     re.compile(r"(?:w|h|p|m|text|bg|top|left)-\[[^\]]+\]"),
     ["Replace arbitrary value with a design token"]),
    ("design-system", "hardcoded-hex", "medium", 0.7,
     re.compile(r"#[0-9a-fA-F]{3,8}\b"),
     ["Use a semantic colour token instead of a hard-coded hex"]),
]


def audit_file(target, path: pathlib.Path, start_idx: int) -> list[dict]:
    text = path.read_text(errors="replace")
    rel = str(path)
    out = []
    idx = start_idx
    has_anim = bool(re.search(r"@keyframes|transition:|animation:|\.animate\(|<transition", text))
    has_rm = "prefers-reduced-motion" in text
    for ftype, rule, sev, conf, rx, recs in _RULES:
        if rule == "missing-reduced-motion":
            if has_anim and not has_rm:
                out.append(_mk(idx, ftype, rule, sev, conf, recs, {"file": rel}))
                idx += 1
            continue
        if rx and rx.search(text):
            m = rx.search(text)
            line = text[:m.start()].count("\n") + 1
            out.append(_mk(idx, ftype, rule, sev, conf, recs, {"file": rel, "line": line}))
            idx += 1
    return out


def audit_project(target) -> list[dict]:
    """Run the deterministic auditors over a target and produce unified findings."""
    root = pathlib.Path(target)
    findings: list[dict] = []
    idx = 1
    exts = {".vue", ".jsx", ".tsx", ".css", ".scss", ".svelte", ".html"}
    for f in sorted(root.rglob("*")):
        if f.is_file() and f.suffix in exts and "node_modules" not in f.parts \
           and ".motif" not in f.parts and ".git" not in f.parts:
            new = audit_file(target, f, idx)
            findings.extend(new)
            idx += len(new)
    # Duplication: components with very similar names.
    comps = [f.stem for f in root.rglob("*.vue") if "node_modules" not in f.parts]
    modalish = [c for c in comps if "modal" in c.lower() or "dialog" in c.lower()]
    if len(modalish) >= 2:
        findings.append(_mk(idx, "duplication", "duplicate-component", "medium", 0.6,
                            ["Consolidate near-duplicate components into one"],
                            {"component": ", ".join(modalish)}))
        idx += 1
    # Originality convergence as a project-level finding.
    _f, score, _band = orig_mod.audit_path(target)
    if score >= 30:
        findings.append(_mk(idx, "originality", "aesthetic-convergence", "medium",
                            0.6, ["Ground originality in product reality, not generic patterns"],
                            {"route": "(project)"}))
        idx += 1
    return findings


def summarize(findings: list[dict]) -> dict:
    by_type: dict = {}
    by_sev: dict = {}
    for f in findings:
        by_type[f["type"]] = by_type.get(f["type"], 0) + 1
        by_sev[f["severity"]] = by_sev.get(f["severity"], 0) + 1
    return {"total": len(findings), "by_type": by_type, "by_severity": by_sev}


def set_status(target, fid: str, status: str, suppression: dict | None = None) -> bool:
    if status not in VALID_STATUS:
        return False
    p = _dir(target) / f"{fid}.json"
    if not p.exists():
        return False
    d = json.loads(p.read_text())
    d["status"] = status
    if suppression:
        d["suppression"] = suppression
    p.write_text(json.dumps(d, indent=2) + "\n")
    return True
