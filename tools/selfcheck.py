#!/usr/bin/env python3
"""Dependency-free self-check — the local mirror of CI used by `make check`.

Runs the same assertions as the pytest suite without requiring pytest, so the
gate works on any stock Python 3.11+. CI additionally runs the full pytest suite.
"""
from __future__ import annotations
import json
import sys
import tempfile
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from motif import registry, scan as scan_mod, rank as rank_mod, install as install_mod, cli, jsonschema_min  # noqa: E402
from scanners import license_scanner  # noqa: E402

ROOT = registry.ROOT
FIX = ROOT / "evals" / "fixtures"
passed = 0
failed: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    global passed
    if cond:
        passed += 1
        print(f"  ok   {name}")
    else:
        failed.append(f"{name}: {detail}")
        print(f"  FAIL {name}: {detail}")


def codes(findings):
    return {f.code for f in findings}


# 1. Registry validates
res = registry.validate_all()
check("registry validates", res.ok, "; ".join(res.errors[:5]))
check(">=15 sources (v0.1.0 discipline)", len(registry.load_records("sources")) >= 15)
for kind in ("effects", "patterns", "recipes", "components"):
    check(f"{kind} >= 4", len(registry.load_records(kind)) >= 4)

# 2. Recipes point at real implementation files
for r in registry.load_records("recipes"):
    p = r.data.get("implementation_path")
    if p:
        check(f"impl exists: {p}", (ROOT / p).exists())

# 3. Eval cases match schema
eval_schema = json.loads((ROOT / "schemas" / "evaluation.schema.json").read_text())
for c in sorted((ROOT / "evals" / "cases").glob("*.json")):
    errs = jsonschema_min.validate(json.loads(c.read_text()), eval_schema)
    check(f"eval case valid: {c.name}", not errs, str(errs))

# 4. Scanners catch malicious fixtures, pass clean control
ev = scan_mod.scan_all(FIX / "eval-button")
check("eval-button -> reject", scan_mod.verdict(ev) == "reject")
check("eval-button finds eval+cookie", {"eval", "cookies"} <= codes(ev))
pi = scan_mod.scan_all(FIX / "postinstall-pkg")
check("postinstall -> reject", scan_mod.verdict(pi) == "reject")
check("postinstall finds lifecycle+typosquat", {"lifecycle-script", "typosquat"} <= codes(pi))
rl = scan_mod.scan_all(FIX / "remote-loader")
check("remote-loader flagged", scan_mod.verdict(rl) in ("reject", "review"))
check("remote-loader finds remote-script", "remote-script" in codes(rl))
sk = scan_mod.scan_all(FIX / "private-key-leak")
check("secret leak -> reject", scan_mod.verdict(sk) == "reject")
check("secret leak finds private-key+token", {"private-key", "github-token"} <= codes(sk))
safe = scan_mod.scan_all(FIX / "safe-component")
check("safe control -> pass", scan_mod.verdict(safe) == "pass")

# 5. Licence gate
check("unknown licence -> reference-only", license_scanner.classify("UNKNOWN") == (False, "reference-only"))
check("Commons Clause not permissive",
      license_scanner.classify("LicenseRef-Commons-Clause")[0] is False)

# 6. Transparent ranking
rec, _ = rank_mod.rank_for_pattern("skeleton-loading", "enterprise-strict")
check("ranking returns candidates", bool(rec))
check("enterprise ranks skeleton-shimmer first", rec and rec[0].id == "skeleton-shimmer")
check("ranking explains every candidate", all(s.reasons for s in rec))

# 7. Install gates
check("install refuses reference-only",
      install_mod.plan_install("aceternity-aurora-bg", "/tmp/x").refused is not None)
check("install refuses rejected component",
      install_mod.plan_install("uiverse-eval-button", "/tmp/y").refused is not None)
plan = install_mod.plan_install("shadcn-button", "/tmp/z")
check("install plans installable component", plan.refused is None and bool(plan.files))

# 8. Install + rollback roundtrip
with tempfile.TemporaryDirectory() as td:
    target = pathlib.Path(td) / "proj"
    target.mkdir()
    (target / "keep.txt").write_text("original")
    install_mod.snapshot(target)
    (target / "new.txt").write_text("added")
    install_mod.rollback(target)
    check("rollback removes added file", not (target / "new.txt").exists())
    check("rollback keeps original", (target / "keep.txt").read_text() == "original")

# 9. CLI smoke
check("cli validate rc=0", cli.main(["validate"]) == 0)
check("cli search rc=0", cli.main(["search", "save"]) == 0)
check("cli source scan eval-button rc=3", cli.main(["source", "scan", str(FIX / "eval-button")]) == 3)
check("cli retrieve refused offline rc=3", cli.main(["source", "retrieve"]) == 3)
check("cli generate-index rc=0", cli.main(["generate-index"]) == 0)

print()
print(f"self-check: {passed} passed, {len(failed)} failed")
sys.exit(1 if failed else 0)
