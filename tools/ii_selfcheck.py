#!/usr/bin/env python3
"""Dependency-free self-check for the Interface Intelligence OS layer.

Complements tools/selfcheck.py (the Motif foundation gate). Run by `make check`.
"""
from __future__ import annotations
import sys
import tempfile
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from ii import cli, data, graph, originality, states, debt, genome  # noqa: E402

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


# 1. Unified validation
check("ii validate rc=0", cli.main(["validate"]) == 0)
counts, errs = data.validate_all_data()
check("engine data has no schema errors", not errs, "; ".join(errs[:3]))
check("design data present (styles>=10, layouts>=10)",
      counts.get("styles", 0) >= 10 and counts.get("layouts", 0) >= 10)
check("industry packs present (>=10)", counts.get("industry-packs", 0) >= 10)
check("state requirements present (>=10)", counts.get("state-requirements", 0) >= 10)

# 2. Interaction graph + queries
check("graph referentially valid", not graph.validate())
gaps = graph.query("screens-without-error-recovery")
check("graph query surfaces seeded gap", len(gaps) >= 1, "expected a screen lacking error recovery")
check("all named queries run", all(isinstance(graph.query(q), list) for q in graph.QUERIES))

# 3. State completeness
m = dict(states.matrix())
check("states matrix non-empty", len(m) >= 10)
r = states.validate_states("data-fetch-region", ["loading", "success"])
check("state validate flags missing required states", not r["ok"] and "error" in r["missing"])

# 4. Originality detector
with tempfile.TemporaryDirectory() as td:
    g = pathlib.Path(td) / "hero.html"
    g.write_text('<div class="bg-gradient-to-r from-purple-500 backdrop-blur rounded-3xl">Supercharge your workflow</div>')
    findings, score, _band = originality.audit_path(g)
    check("originality flags generic snippet", score > 0 and bool(findings))
    c = pathlib.Path(td) / "plain.html"
    c.write_text('<table><tr><td>Invoice</td></tr></table>')
    _f, clean_score, _b = originality.audit_path(c)
    check("originality clean on plain markup", clean_score == 0)

# 5. Interface debt
with tempfile.TemporaryDirectory() as td:
    f = pathlib.Path(td) / "c.css"
    f.write_text(".x{color:#ff0033 !important;width:var(--w)}\n.y{top:13px}")
    d = debt.calculate(td)
    check("debt detects hex + important", d.score > 0 and "hex-colour-inline" in d.by_category)

# 6. Genome
check("genome validates", not [e for e in genome.validate("enterprise-pm-genome") if "no genome" not in e])
check("genome explain returns lines", len(genome.explain("enterprise-pm-genome")) > 1)

# 7. Motion / density / context via CLI
check("ii motion validate rc=0", cli.main(["motion", "validate"]) == 0)
check("ii density validate rc=0", cli.main(["density", "validate"]) == 0)
check("ii context validate rc=0", cli.main(["context", "validate"]) == 0)
check("ii doctor runs", cli.main(["doctor"]) in (0, 1))
check("delegation to motif works (search)", cli.main(["search", "save"]) == 0)

print()
print(f"ii self-check: {passed} passed, {len(failed)} failed")
sys.exit(1 if failed else 0)
