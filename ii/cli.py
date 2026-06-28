"""Motif platform command-line interface.

The user-facing command is `motif` (short alias `ii`; legacy alias `oii`). Foundation
commands (source, component, search, rank) delegate to the validated interaction core;
the design, product, and governance commands are implemented here. Offline and
dependency-free.
"""
from __future__ import annotations
import argparse
import json
import sys
import datetime
import pathlib

from . import __version__, data, graph as graph_mod, originality as orig_mod
from . import states as states_mod, debt as debt_mod, genome as genome_mod
from motif import registry, project as project_mod, cli as motif_cli

ROOT = registry.ROOT
_DELEGATE = {"source", "component", "search", "rank", "rank-sources", "generate-index"}
EXPERIMENTAL = {
    "simulate": "Workflow simulation (Playwright integration) is planned/experimental in v2.0.0.",
    "compile-apply": "Live `compile apply` beyond the controlled installer is planned for v0.3.0.",
    "visual": "Visual-regression assurance is planned (needs a screenshot runtime).",
}


def _p(s: str = "") -> None:
    print(s)


# ---- validate / doctor ----------------------------------------------------

def cmd_validate(_a) -> int:
    res = registry.validate_all()
    counts, errs = data.validate_all_data()
    graph_errs = graph_mod.validate()
    _p("# Foundation registry")
    for k, n in res.counts.items():
        _p(f"  {k}: {n}")
    _p("# Interface Intelligence data")
    for k, n in counts.items():
        if n:
            _p(f"  {k}: {n}")
    all_errs = list(res.errors) + errs + [f"graph: {e}" for e in graph_errs]
    if not all_errs:
        _p("\nOK: foundation + engine data + graph valid")
        return 0
    _p(f"\nFAIL: {len(all_errs)} error(s)")
    for e in all_errs[:40]:
        _p(f"  - {e}")
    return 1


def cmd_doctor(_a) -> int:
    if getattr(_a, "browser", False):
        from . import browser as browser_mod
        _p(json.dumps(browser_mod.doctor(), indent=2))
        return 0
    from motif import doctor as md
    lines, ok = md.run()
    _p("\n".join(lines))
    counts, errs = data.validate_all_data()
    _p("\n## Interface Intelligence engines")
    for k, n in counts.items():
        _p(f"  {k}: {n}")
    _p(f"  engine-data errors: {len(errs)}")
    _p(f"\nMotif {__version__} (commands: motif, ii, oii)")
    return 0 if ok and not errs else 1


# ---- product context ------------------------------------------------------

def cmd_inspect(_a) -> int:
    info = project_mod.detect(".")
    _p(json.dumps(info.to_dict(), indent=2))
    _p("\nNext: `ii model-product` to scaffold a Product Context Manifest.")
    return 0


def cmd_model_product(_a) -> int:
    skeleton = {
        "version": 1, "confidence": 0.4,
        "product": {"type": "TODO", "purpose": "TODO"},
        "users": [{"role": "TODO", "expertise": "TODO", "frequency": "TODO"}],
        "workflows": [], "risks": [],
        "verified": [], "inferred": [], "assumptions": [], "unresolved": ["confirm product type with a human"],
    }
    _p(json.dumps(skeleton, indent=2))
    _p("\nFill this in and save to product-intelligence/manifests/<id>.json, then `ii context validate`.")
    return 0


def cmd_context(a) -> int:
    if a.action == "validate":
        n, errs = data.validate_kind("product-manifests")
        _p(f"product manifests: {n}")
        if errs:
            for e in errs:
                _p(f"  - {e}")
            return 1
        _p("OK: manifests valid (and uncertainty is explicit)")
        return 0
    if a.action == "explain":
        for p, d in data.load_kind("product-manifests"):
            if p.stem == a.value or a.value is None:
                _p(f"# {p.stem} (confidence {d.get('confidence')})")
                _p(f"  product: {d['product'].get('type')}, {d['product'].get('purpose')}")
                for grp in ("verified", "inferred", "assumptions", "unresolved"):
                    if d.get(grp):
                        _p(f"  {grp}: {', '.join(d[grp])}")
                if a.value:
                    return 0
        return 0
    _p("usage: ii context [validate|explain]")
    return 2


# ---- genome / graph / originality ----------------------------------------

def cmd_genome(a) -> int:
    if a.action == "validate":
        errs = genome_mod.validate(a.value) if a.value else \
            [e for _, d in data.load_kind("design-genomes") for e in genome_mod.validate(d.get("product"))]
        if errs and errs != [f"no genome '{a.value}'"]:
            for e in errs:
                _p(f"  - {e}")
            return 1
        _p("OK: genome(s) valid")
        return 0
    if a.action == "explain":
        _p("\n".join(genome_mod.explain(a.value)))
        return 0
    if a.action == "diff":
        if not a.value or not a.second:
            _p("usage: ii genome diff <a> <b>")
            return 2
        _p("\n".join(genome_mod.diff(a.value, a.second)))
        return 0
    _p("usage: ii genome [validate|explain|diff]")
    return 2


def cmd_graph(a) -> int:
    if a.action == "validate":
        errs = graph_mod.validate()
        nodes, edges = graph_mod.load()
        _p(f"nodes: {len(nodes)}  edges: {len(edges)}")
        if errs:
            for e in errs:
                _p(f"  - {e}")
            return 1
        _p("OK: graph referentially valid")
        return 0
    if a.action == "list-queries":
        for k, desc in graph_mod.QUERIES.items():
            _p(f"  {k}: {desc}")
        return 0
    if a.action == "query":
        if not a.value:
            _p("usage: ii graph query <query-name>  (see `ii graph list-queries`)")
            return 2
        try:
            hits = graph_mod.query(a.value)
        except KeyError:
            _p(f"unknown query '{a.value}'")
            return 2
        _p(f"# {a.value}: {graph_mod.QUERIES[a.value]}")
        if hits:
            for h in hits:
                _p(f"  - {h}")
            _p(f"\n{len(hits)} finding(s), gaps to address.")
        else:
            _p("  (no findings)")
        return 0
    _p("usage: ii graph [validate|query|list-queries]")
    return 2


def cmd_originality(a) -> int:
    if not a.path:
        _p("usage: ii originality audit <path>")
        return 2
    ctx = {"product_forms": a.product_form.split(",")} if getattr(a, "product_form", None) else None
    r = orig_mod.audit(a.path, context=ctx)
    _p(f"# Aesthetic Convergence Risk: {r['overall_score']}/100, {r['risk_band']}")
    _p(f"  confidence: {r['confidence']} (static-only)  "
       f"design-system: {r['provenance']['design_system_present']}  "
       f"dense-context: {r['provenance']['dense_product_context']}")
    for s in r["signals"]:
        _p(f"  [{s['raw_count']:3}x] {s['name']:20} score {s['weighted_score']:5}  "
           f"(ctx x{s['context_adjustment']}, provenance x{s['provenance_adjustment']}, "
           f"{s['files_present']} file(s))")
    if not r["signals"]:
        _p("  no generic-pattern signals detected")
    _p("\nAesthetic-convergence risk reflects generic-pattern concentration, not authorship; "
       "it cannot determine whether a UI was produced by AI. Ground originality in product reality.")
    return 0 if r["overall_score"] < 60 else 3


# ---- motion / density / states -------------------------------------------

def cmd_motion(a) -> int:
    n, errs = data.validate_kind("motion-grammars")
    _p(f"motion grammars: {n}")
    for e in errs:
        _p(f"  - {e}")
    return 0 if not errs else 1


def cmd_density(a) -> int:
    n, errs = data.validate_kind("density-grammars")
    _p(f"density grammars: {n}")
    for e in errs:
        _p(f"  - {e}")
    return 0 if not errs else 1


def cmd_states(a) -> int:
    if a.action == "matrix":
        for ct, states in states_mod.matrix():
            _p(f"  {ct:22} {', '.join(states)}")
        return 0
    if a.action == "validate":
        if not a.type or not a.present:
            _p("usage: ii states validate --type <component_type> --present a,b,c")
            return 2
        r = states_mod.validate_states(a.type, a.present.split(","))
        if "error" in r:
            _p(r["error"] + "  known: " + ", ".join(r["known"]))
            return 2
        _p(json.dumps(r, indent=2))
        return 0 if r["ok"] else 3
    if a.action == "inspect":
        if not a.value or not a.type:
            _p("usage: ii states inspect <file> --type <component_type>")
            return 2
        r = states_mod.inspect_file(a.value, a.type)
        if "error" in r:
            _p(r["error"] + "  known: " + ", ".join(r["known"]))
            return 2
        _p(json.dumps(r, indent=2))
        return 0 if r["ok"] else 3
    _p("usage: ii states [matrix|validate|inspect]")
    return 2


# ---- debt / decision ------------------------------------------------------

def cmd_debt(a) -> int:
    if a.action == "calculate":
        target = a.value or "."
        d = debt_mod.calculate(target)
        _p(f"# Interface Debt Score: {d.score}/100, {debt_mod.band(d.score)}")
        _p(f"  files scanned: {d.files_scanned}")
        for cat, b in sorted(d.by_category.items(), key=lambda x: -x[1]['occurrences']):
            _p(f"  [{b['occurrences']:4}x in {b['files']} file(s)] {cat}")
        if not d.by_category:
            _p("  no debt signals detected")
        _p("\nEvery point traces to a finding above (category x weight, normalised by files).")
        return 0
    if a.action == "explain":
        _p("Interface Debt categories and weights:")
        for cat, w, _rx, msg in debt_mod.SIGNALS:
            _p(f"  {cat} (weight {w}): {msg}")
        return 0
    _p("usage: ii debt [calculate|explain]")
    return 2


def cmd_decision(a) -> int:
    d = ROOT / "governance" / "decision-ledger"
    if a.action == "list":
        for p, rec in data.load_kind("decisions"):
            _p(f"  {rec['id']:34} {rec.get('status','active'):10} {rec['decision'][:60]}")
        return 0
    if a.action == "create":
        if not (a.id and a.problem and a.decision):
            _p("usage: ii decision create --id X --problem '...' --decision '...' [--rationale '...']")
            return 2
        rec = {"id": a.id, "problem": a.problem, "decision": a.decision,
               "rationale": a.rationale or "TODO", "date": datetime.date.today().isoformat(),
               "status": "active", "supersedes": None}
        out = d / f"{a.id}.json"
        out.write_text(json.dumps(rec, indent=2) + "\n")
        _p(f"wrote {out.relative_to(ROOT)}")
        return 0
    _p("usage: ii decision [create|list]")
    return 2


# ---- experimental / planned ----------------------------------------------

def cmd_experimental(a) -> int:
    key = a.cmd if a.cmd in EXPERIMENTAL else a.cmd
    _p(EXPERIMENTAL.get(key, f"`{a.cmd}` is planned/experimental in v2.0.0; see PROJECT_STATUS.md."))
    _p("This command is intentionally not claimed as implemented.")
    return 0


# ---- parser ---------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="motif", description="Motif: design judgment, interface engineering, and governance (offline, dependency-free)")
    p.add_argument("--version", action="version", version=f"Motif {__version__} (commands: motif, ii, oii)")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("validate", help="validate foundation + engine data + graph").set_defaults(fn=cmd_validate)
    sp = sub.add_parser("doctor", help="environment + engine health")
    sp.add_argument("--browser", action="store_true", help="report browser runtime status")
    sp.set_defaults(fn=cmd_doctor)
    sub.add_parser("inspect", help="detect the target project's framework/conventions").set_defaults(fn=cmd_inspect)
    sub.add_parser("model-product", help="scaffold a Product Context Manifest").set_defaults(fn=cmd_model_product)

    sp = sub.add_parser("context", help="product context manifest")
    sp.add_argument("action", choices=["validate", "explain"])
    sp.add_argument("value", nargs="?")
    sp.set_defaults(fn=cmd_context)

    sp = sub.add_parser("genome", help="product design genome")
    sp.add_argument("action", choices=["validate", "explain", "diff"])
    sp.add_argument("value", nargs="?")
    sp.add_argument("second", nargs="?")
    sp.set_defaults(fn=cmd_genome)

    sp = sub.add_parser("graph", help="interaction specification graph")
    sp.add_argument("action", choices=["validate", "query", "list-queries"])
    sp.add_argument("value", nargs="?")
    sp.set_defaults(fn=cmd_graph)

    sp = sub.add_parser("originality", help="aesthetic convergence audit")
    sp.add_argument("action", choices=["audit"])
    sp.add_argument("path", nargs="?")
    sp.add_argument("--product-form", dest="product_form",
                    help="comma-separated product forms for context-aware scoring")
    sp.set_defaults(fn=cmd_originality)

    sp = sub.add_parser("motion", help="validate motion grammars")
    sp.add_argument("action", choices=["validate"])
    sp.set_defaults(fn=cmd_motion)
    sp = sub.add_parser("density", help="validate density grammars")
    sp.add_argument("action", choices=["validate"])
    sp.set_defaults(fn=cmd_density)

    sp = sub.add_parser("states", help="state completeness")
    sp.add_argument("action", choices=["matrix", "validate", "inspect"])
    sp.add_argument("value", nargs="?")
    sp.add_argument("--type")
    sp.add_argument("--present")
    sp.set_defaults(fn=cmd_states)

    sp = sub.add_parser("debt", help="interface debt analysis")
    sp.add_argument("action", choices=["calculate", "explain"])
    sp.add_argument("value", nargs="?")
    sp.set_defaults(fn=cmd_debt)

    sp = sub.add_parser("decision", help="design decision ledger")
    sp.add_argument("action", choices=["create", "list"])
    sp.add_argument("--id")
    sp.add_argument("--problem")
    sp.add_argument("--decision")
    sp.add_argument("--rationale")
    sp.set_defaults(fn=cmd_decision)

    for name in ("simulate", "drift"):
        sp = sub.add_parser(name, help=f"{name} (experimental/planned)")
        sp.add_argument("rest", nargs="*")
        sp.set_defaults(fn=cmd_experimental)

    from . import cli_v3
    cli_v3.register(sub)

    return p


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] in _DELEGATE:
        return motif_cli.main(argv)
    ns = build_parser().parse_args(argv)
    return ns.fn(ns)


if __name__ == "__main__":
    sys.exit(main())
