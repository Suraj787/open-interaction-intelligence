"""InterfaceBench runner (automated measures).

Turns the benchmark definitions in interfacebench/ into an executable runner over a
target project. It reports objective automated measures and keeps model-based evaluation
and the human rubric clearly separate; it does not merge them into one opaque score.
"""
from __future__ import annotations
import pathlib
from . import debt as debt_mod, originality as orig_mod, findings as findings_mod
from . import states as states_mod, runtime


def run(target) -> dict:
    root = pathlib.Path(target)
    d = debt_mod.calculate(target)
    _f, conv, _b = orig_mod.audit_path(target)
    fnd = findings_mod.audit_project(target)
    pm = runtime.model_project(target)

    # State coverage: of the component files present, how many evidence their required states.
    coverage = {"checked": 0, "complete": 0}
    for comp in root.rglob("*.vue"):
        if "node_modules" in comp.parts:
            continue
        # treat each as a generic 'data-fetch-region' candidate only if it fetches
        text = comp.read_text(errors="replace")
        if "fetch" in text or "axios" in text or "useQuery" in text or "onMounted" in text:
            coverage["checked"] += 1
            r = states_mod.inspect_file(comp, "data-fetch-region")
            if r.get("ok"):
                coverage["complete"] += 1

    automated = {
        "interface_debt": d.score,
        "originality_convergence": conv,
        "findings_total": len(fnd),
        "findings_by_severity": findings_mod.summarize(fnd)["by_severity"],
        "routes": len(pm.routes),
        "components": len(pm.components),
        "state_coverage": coverage,
        "dependency_count": pm.dependency_count,
    }
    return {
        "target": str(root),
        "automated_measures": automated,
        "model_based_evaluation": "not run (requires a model-eval pass; kept separate by design)",
        "human_rubric": "see interfacebench/rubric.md (0-3 per capability)",
        "note": "Automated measures only. Visual quality, workflow completion under a real "
                "browser, and longitudinal coherence require the runtime layers (experimental).",
    }
