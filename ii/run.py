"""Flagship orchestration: init, run, create, improve, autopilot.

Coordinates the engines into the end-to-end Motif Live loop. Deterministic steps run;
steps that require a browser runtime (start app, capture, render twin, visual preview)
are recorded as experimental and skipped, never faked. Code changes only ever happen in
an isolated worktree via an explicit apply step, never on the user's main branch.
"""
from __future__ import annotations
import json
from . import runtime, findings as findings_mod, concepts as concepts_mod
from . import twin as twin_mod, system as system_mod, recommend as rec_mod
from . import debt as debt_mod, originality as orig_mod, policy as policy_mod


def _suggest_profile(pm) -> str:
    if pm.framework in ("vue", "frappe-vue", "react") and pm.dependency_count > 0:
        return "enterprise-strict" if pm.tailwind else "saas-balanced"
    return "saas-balanced"


def init(target, stamp: str) -> dict:
    runtime.ensure_state(target)
    pm = runtime.model_project(target)
    (runtime.state_root(target) / "project" / "model.json").write_text(
        json.dumps(pm.to_dict(), indent=2) + "\n")
    ds = system_mod.extract(target)
    system_mod.write(target, ds)
    twin_mod.write(target, twin_mod.build(target, stamp))
    fnd = findings_mod.audit_project(target)
    for f in fnd:
        findings_mod.save(target, f)
    policy_mod.init(target)
    profile = _suggest_profile(pm)
    summary = {
        "framework": pm.framework, "styling": "Tailwind CSS" if pm.tailwind else "CSS",
        "routes": len(pm.routes), "components": len(pm.components),
        "design_tokens": "partial" if ds["css_variables"] else "none",
        "profile": profile, "confidence": 0.82 if pm.framework != "unknown" else 0.4,
        "findings": findings_mod.summarize(fnd),
        "gaps": [f["rule"] for f in fnd[:6]],
    }
    _record(target, "audit", "first-run init", profile, stamp, fnd, [], "audit-only")
    return summary


def improve(target, goal: str, mode: str, profile: str, stamp: str) -> dict:
    pm = runtime.model_project(target)
    twin_mod.write(target, twin_mod.build(target, stamp))
    fnd = findings_mod.audit_project(target)
    for f in fnd:
        findings_mod.save(target, f)
    concepts = concepts_mod.generate(target, goal or "improve the interface", 3)
    concepts_mod.write(target, goal or "improve", concepts)
    d = debt_mod.calculate(target)
    _f, conv, _b = orig_mod.audit_path(target)
    pol = policy_mod.check(target, fnd, d.score, conv)
    _record(target, mode, goal, profile, stamp, fnd, concepts, "audit-only")
    return {
        "framework": pm.framework, "routes": len(pm.routes),
        "findings": findings_mod.summarize(fnd),
        "debt": d.score, "convergence": conv,
        "concepts": [c["id"] for c in concepts],
        "policy_blocking": pol["blocking"], "violations": pol["violations"],
        "note": "Audit + concepts are deterministic. Preview and apply require the runtime "
                "(experimental); use `motif compile plan` and the controlled installer to apply.",
    }


def create(goal: str, framework: str, profile: str, stamp: str, target=".") -> dict:
    runtime.ensure_state(target)
    manifest = {
        "version": 1, "confidence": 0.4,
        "product": {"type": "TODO-from-goal", "purpose": goal},
        "users": [{"role": "TODO", "expertise": "TODO", "frequency": "TODO"}],
        "workflows": [], "risks": [],
        "verified": [], "inferred": [f"target framework: {framework}"],
        "assumptions": [f"profile: {profile}"],
        "unresolved": ["confirm product type, users, and primary workflow with a human"],
    }
    out = runtime.state_root(target) / "project" / "create-context.json"
    out.write_text(json.dumps(manifest, indent=2) + "\n")
    concepts = concepts_mod.generate(target, goal, 3)
    concepts_mod.write(target, goal, concepts)
    _record(target, "create", goal, profile, stamp, [], concepts, "pending")
    return {"goal": goal, "framework": framework, "profile": profile,
            "context": str(out), "concepts": [c["id"] for c in concepts],
            "note": "Context is a low-confidence skeleton; the system never invents certainty. "
                    "Compile/preview of concepts is the next step (compile plan implemented; "
                    "visual preview experimental)."}


GATES = ["understanding", "diagnosis", "concepts", "plan", "preview", "assurance", "delivery"]


def autopilot(target, goal: str, profile: str, stamp: str) -> dict:
    pm = runtime.model_project(target)
    fnd = findings_mod.audit_project(target)
    gates = []
    for g in GATES:
        gate = {"gate": g, "confidence": 0.7,
                "known": [f"framework {pm.framework}", f"{len(pm.routes)} routes"],
                "inferred": [f"profile {profile}"],
                "unresolved": ["primary workflow needs human confirmation"] if g == "understanding" else [],
                "risks": ["browser preview/apply require runtime (experimental)"] if g in ("preview", "delivery") else [],
                "status": "stop-for-approval" if g in ("plan", "preview", "delivery") else "ready"}
        gates.append(gate)
    _record(target, "improve", goal, profile, stamp, fnd, [], "audit-only", gates=gates)
    return {"goal": goal, "gates": gates,
            "note": "Autopilot stops at plan, preview, and delivery gates for human approval. "
                    "High-risk domains always require human approval. No automatic apply."}


def _record(target, mode, goal, profile, stamp, findings, concepts, outcome, gates=None):
    rid = runtime.next_run_id(target, stamp)
    rec = {"id": rid, "mode": mode, "goal": goal or "", "started": stamp,
           "target": str(target), "policy_profile": profile,
           "findings": [f["id"] for f in findings], "concepts": [c["id"] for c in concepts],
           "selected_plan": None, "evidence": [], "outcome": outcome}
    if gates:
        rec["gates"] = gates
    runtime.write_run(target, rec)
    return rid
