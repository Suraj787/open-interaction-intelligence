#!/usr/bin/env python3
"""Dependency-free self-check for the Motif v3 (Live) layer. Run by `make check`.

Operates on a temp copy of the fixture app so it writes no runtime state into the repo.
"""
from __future__ import annotations
import sys
import json
import shutil
import tempfile
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ii import (run as run_mod, findings as findings_mod, twin as twin_mod,  # noqa: E402
                policy as policy_mod, memory as memory_mod, atlas as atlas_mod,
                system as system_mod, guardian as guardian_mod, mcp as mcp_mod,
                bench as bench_mod, recommend as rec_mod, concepts as concepts_mod,
                studio as studio_mod)

FIX = ROOT / "evals" / "fixtures" / "sample-vue-app"
passed = 0
failed: list[str] = []


def check(name, cond, detail=""):
    global passed
    if cond:
        passed += 1
        print(f"  ok   {name}")
    else:
        failed.append(name)
        print(f"  FAIL {name}: {detail}")


with tempfile.TemporaryDirectory() as td:
    proj = pathlib.Path(td) / "app"
    shutil.copytree(FIX, proj)
    stamp = "20260628"

    # init
    s = run_mod.init(proj, stamp)
    check("init detects vue framework", s["framework"] == "vue")
    check("init finds gaps (findings>0)", s["findings"]["total"] > 0)
    check("init wrote .motif state", (proj / ".motif" / "runs").exists())

    # findings audit + lifecycle
    fnd = findings_mod.audit_project(proj)
    check("findings audit returns findings", len(fnd) >= 3)
    types = {f["type"] for f in fnd}
    check("findings include accessibility + design-system", "accessibility" in types and "design-system" in types)
    findings_mod.save(proj, fnd[0])
    ok = findings_mod.set_status(proj, fnd[0]["id"], "accepted-risk",
                                 {"reason": "x", "scope": "finding", "author": "t", "expiry": "y"})
    check("finding status lifecycle works", ok)
    check("invalid status rejected", not findings_mod.set_status(proj, fnd[0]["id"], "bogus"))

    # twin
    m = twin_mod.build(proj, stamp)
    check("twin manifest has routes + components", m["routes"] and m["components"])
    check("twin honestly marks rendered=False", m["rendered"] is False)

    # policy
    policy_mod.init(proj)
    res = policy_mod.check(proj, fnd, debt_score=80, originality_score=70)
    check("policy blocks over-threshold debt/convergence", res["blocking"])

    # memory (rejected approach)
    ok, _ = memory_mod.add(proj, "no-glass-dashboard", "rejected-approach",
                           "glassmorphism rejected on dashboard: poor contrast", "2026-06-28")
    check("memory add rejected-approach", ok and len(memory_mod.rejected_approaches(proj)) == 1)
    check("memory invalid type rejected", not memory_mod.add(proj, "x", "bogus", "y", "z")[0])

    # design-system extraction
    ds = system_mod.extract(proj)
    check("system extract finds css variables", len(ds["css_variables"]) >= 1)
    check("system extract flags exceptions", len(ds["exceptions"]) >= 1)

    # twin + studio build
    studio_out = studio_mod.build(proj)
    check("studio builds an index.html", studio_out.exists())

    # bench
    b = bench_mod.run(proj)
    check("bench reports automated measures", "interface_debt" in b["automated_measures"])
    check("bench keeps model/human separate", "model_based_evaluation" in b and "human_rubric" in b)

# atlas (from the registry, to temp)
with tempfile.TemporaryDirectory() as td2:
    res = atlas_mod.build(td2)
    check("atlas builds >150 pages", res["pages"] > 150)
    check("atlas index.json present", (pathlib.Path(td2) / "index.json").exists())

# recommend
r = rec_mod.recommend("skeleton-loading", "enterprise-strict")
check("recommend returns explainable record", r.get("selected_effect") and r.get("reasons"))

# concepts
c = concepts_mod.generate(".", "improve the dashboard", 3)
check("concepts generates 3 materially different", len(c) == 3 and len({x["direction"] for x in c}) == 3)

# MCP server (read-only by default; write guarded)
check("mcp tools/list", len(mcp_mod.dispatch("tools/list", {}, False)["tools"]) >= 10)
check("mcp read tool works", "results" in json.loads(
    mcp_mod.dispatch("tools/call", {"name": "motif.search_atlas", "arguments": {"q": "dialog"}}, False)["content"][0]["text"]))
check("mcp write tool guarded without --allow-write",
      mcp_mod.dispatch("tools/call", {"name": "motif.plan_change", "arguments": {}}, False).get("isError"))
check("mcp resources/list", len(mcp_mod.dispatch("resources/list", {}, False)["resources"]) >= 3)

# guardian report formatting
rep = guardian_mod.report({"summary": {"total": 1, "by_severity": {"high": 1}},
                           "changed": 1, "ui_changed": 1, "findings": [
                               {"severity": "high", "rule": "x", "location": {"file": "a.vue"},
                                "recommendations": ["fix"]}], "violations": [{"x": 1}], "blocking": True}, "markdown")
check("guardian markdown report renders + blocks", "Block" in rep)

print()
print(f"v3 self-check: {passed} passed, {len(failed)} failed")
sys.exit(1 if failed else 0)
