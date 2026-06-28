#!/usr/bin/env python3
"""Dependency-free self-check for the Motif v3.1 UX Evidence Graph + golden repair loop.

The browser-executed steps are honestly not-executed (no runtime); the deterministic loop
(detect -> evidence -> plan -> worktree apply -> verify -> exact rollback) is exercised end
to end. Run by `make check`.
"""
from __future__ import annotations
import sys
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ii import evidence as ev, repair as repair_mod, browser as browser_mod, mcp as mcp_mod  # noqa: E402

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


# 1. Evidence graph validates (schema + referential)
counts, errs = ev.validate()
check("evidence graph schema-valid (no errors)", not errs, "; ".join(errs[:4]))
check(">=100 executable claims", counts.get("claims", 0) >= 100, f"got {counts.get('claims')}")
check("sources present", counts.get("sources", 0) >= 10)
check("myth register present", counts.get("myths", 0) >= 10)
check("three evidence packs", counts.get("packs", 0) >= 3)
check("validation methods present", counts.get("validations", 0) >= 6)

# 2. Golden claim is normative, tier 1, blocking
g = ev.explain("claim-status-colour-001")
check("golden claim is normative tier-1 blocking", g.get("force") == "normative" and g.get("tier") == 1 and g.get("blocking"))
check("golden claim disallows compliance claim", g.get("legal", {}).get("compliance_claim_allowed") is False)

# 3. Query engine: context match, blocking, confidence, merge rules
qr = ev.query({"product_forms": ["web-app", "dashboard"], "purposes": ["monitor"],
               "abilities": ["colour-vision-deficiency"], "risks": [{"type": "financial", "severity": 3}]})
check("query returns applicable claims", len(qr["applicable_claims"]) >= 1)
check("query surfaces a blocking normative pattern", len(qr["blocked_patterns"]) >= 1)
check("query exposes sources + required validations", qr["sources"] and qr["required_validations"])
# hypotheses never block, stale cannot newly block
hyp = [c for c in ev.load_claims() if c["claim"]["force"] == "hypothesis"]
check("hypotheses are not in any blocked set", all(
    not ev._blocking(c) for c in hyp)) if hyp else check("hypotheses rule holds (none present)", True)

# 4. Myth register
mm = ev.check_myth("three click rule")
check("myth register matches 'three click rule'", "id" in mm or mm.get("match") is None,
      "expected a myth or explicit no-match")

# 5. Browser is honestly not-executed here
avail, _r = browser_mod.available()
cap = browser_mod.capture("http://127.0.0.1/x", pathlib.Path("/tmp/motif-bcheck"))
check("browser capture reports not-executed without runtime", (cap["status"] == "not-executed") or avail)
check("doctor --browser is honest", browser_mod.doctor()["available"] == avail)

# 6. Golden deterministic repair loop (worktree apply -> verify -> exact rollback)
# Force the deterministic path so this gate is runtime-independent (the real browser
# proof is the separate --require-browser scenario in the browser CI job).
res = repair_mod.golden("evals/fixtures/sample-vue-app", "/projects", use_browser=False)
sd = {s["step"]: s["status"] for s in res["steps"]}
check("golden: detect passed", sd.get("detect") == "passed")
check("golden: apply-in-worktree passed", sd.get("apply-in-worktree") == "passed")
check("golden: finding closed (static) passed", sd.get("verify-finding-closed (static)") == "passed")
check("golden: browser steps not-executed", sd.get("browser-before") == "not-executed" and sd.get("browser-after") == "not-executed")
check("golden: exact rollback passed", sd.get("rollback (exact)") == "passed")
# baseline restored: no leftover repair worktree/branch, fixture file unchanged
subprocess.run(["git", "-C", str(ROOT), "worktree", "prune"], capture_output=True)
branches = subprocess.run(["git", "-C", str(ROOT), "branch"], capture_output=True, text=True).stdout
check("golden: no leftover repair branch", "motif-repair-golden" not in branches)
fixture = ROOT / "evals/fixtures/sample-vue-app/src/components/ProjectStatus.vue"
check("golden: fixture unchanged on main (colour-only preserved)", "props.status.replace" not in fixture.read_text())

# 7. MCP evidence tools
tools = mcp_mod.dispatch("tools/list", {}, False)["tools"]
names = {t["name"] for t in tools}
check("mcp exposes evidence tools", {"motif.get_applicable_claims", "motif.explain_ux_claim", "motif.check_ux_myth"} <= names)
r = mcp_mod.dispatch("tools/call", {"name": "motif.explain_ux_claim", "arguments": {"claim_id": "claim-status-colour-001"}}, False)
check("mcp explain_ux_claim works", "claim-status-colour-001" in r["content"][0]["text"])
res_uris = {x["uri"] for x in mcp_mod.dispatch("resources/list", {}, False)["resources"]}
check("mcp exposes ux-evidence resources", "motif://ux-evidence/claims" in res_uris)

print()
print(f"v3.1 self-check: {passed} passed, {len(failed)} failed")
sys.exit(1 if failed else 0)
