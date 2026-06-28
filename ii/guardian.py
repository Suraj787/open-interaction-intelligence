"""Motif Guardian: continuous governance over a diff.

`motif guard staged|branch` scans changed files for findings, checks the project policy,
and reports. Blocking findings produce a non-zero exit so CI can gate a pull request.
"""
from __future__ import annotations
import subprocess
import pathlib
from . import findings as findings_mod, policy as policy_mod, evidence as ev_mod

# Map deterministic finding rules to the applicable UX evidence claim (when one exists).
_RULE_TO_CLAIM = {
    "status-colour-only": "claim-status-colour-001",
    "hardcoded-hex": None,
    "arbitrary-value": None,
}


def _evidence_for(rule: str):
    cid = _RULE_TO_CLAIM.get(rule)
    if not cid:
        return None
    c = ev_mod.explain(cid)
    return None if "error" in c else c

_UI_EXT = {".vue", ".jsx", ".tsx", ".svelte", ".css", ".scss", ".html"}


def _changed(target, mode: str, base: str | None) -> list[str]:
    root = pathlib.Path(target)
    try:
        if mode == "staged":
            args = ["git", "-C", str(root), "diff", "--cached", "--name-only"]
        else:
            ref = base or "main"
            args = ["git", "-C", str(root), "diff", "--name-only", f"{ref}...HEAD"]
        out = subprocess.run(args, capture_output=True, text=True, check=True).stdout
        return [ln for ln in out.splitlines() if ln.strip()]
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []


def guard(target, mode: str = "branch", base: str | None = None) -> dict:
    root = pathlib.Path(target)
    changed = _changed(target, mode, base)
    ui = [c for c in changed if pathlib.Path(c).suffix in _UI_EXT]
    found: list[dict] = []
    idx = 1
    for rel in ui:
        p = root / rel
        if p.exists():
            new = findings_mod.audit_file(target, p, idx)
            # tag location with the relative path
            for f in new:
                f["location"]["file"] = rel
            found.extend(new)
            idx += len(new)
    pol = policy_mod.check(target, found)
    return {"mode": mode, "changed": len(changed), "ui_changed": len(ui),
            "findings": found, "summary": findings_mod.summarize(found),
            "violations": pol["violations"], "blocking": pol["blocking"]}


def report(result: dict, fmt: str = "text") -> str:
    s = result["summary"]
    if fmt == "markdown":
        lines = ["## Motif Guardian",
                 f"- changed files: {result['changed']} (UI: {result['ui_changed']})",
                 f"- findings: {s['total']}  by severity: {s['by_severity']}",
                 f"- policy violations (blocking): {len(result['violations'])}"]
        for f in result["findings"][:25]:
            loc = f["location"].get("file", "")
            lines.append(f"  - **{f['severity']}** `{f['rule']}` in `{loc}` "
                         f"({f['recommendations'][0] if f['recommendations'] else ''})")
            ev = _evidence_for(f["rule"])
            if ev:
                lines.append(f"    - Evidence: `{ev['id']}` tier {ev['tier']} "
                             f"(confidence {ev['confidence']}); required validation: "
                             f"{', '.join(ev.get('validation', [])) or 'n/a'}")
        lines.append("")
        lines.append("Blocking ❌" if result["blocking"] else "No blocking findings ✅")
        return "\n".join(lines)
    lines = [f"Motif Guardian: {result['changed']} changed ({result['ui_changed']} UI), "
             f"{s['total']} finding(s), {len(result['violations'])} blocking violation(s)"]
    for f in result["findings"][:25]:
        lines.append(f"  [{f['severity']:8}] {f['rule']:24} {f['location'].get('file','')}")
    lines.append("VERDICT: " + ("BLOCK" if result["blocking"] else "PASS"))
    return "\n".join(lines)
