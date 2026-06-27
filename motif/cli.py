"""Motif command-line interface. Offline by default; transparent output.

Run `python -m motif --help`. Internet retrieval only happens with an explicit
`source retrieve --refresh` against an allowlisted official host.
"""
from __future__ import annotations
import argparse
import json
import pathlib
import sys

from . import __version__, registry, search as search_mod, rank as rank_mod
from . import doctor as doctor_mod, completeness as comp_mod, install as install_mod
from . import scan as scan_mod, yaml_min


def _print(s: str = "") -> None:
    print(s)


# ---- validate / doctor ----------------------------------------------------

def cmd_validate(_args) -> int:
    res = registry.validate_all()
    for kind, n in res.counts.items():
        _print(f"  {kind}: {n}")
    if res.ok:
        _print("OK: registry valid (schemas + ids + references)")
        return 0
    _print(f"\nFAIL: {len(res.errors)} error(s):")
    for e in res.errors:
        _print(f"  - {e}")
    return 1


def cmd_doctor(_args) -> int:
    lines, ok = doctor_mod.run()
    _print("\n".join(lines))
    return 0 if ok else 1


# ---- search / rank --------------------------------------------------------

def cmd_search(args) -> int:
    kinds = [args.kind] if args.kind else None
    hits = search_mod.search(args.query, kinds)
    if not hits:
        _print("no matches")
        return 0
    for r in hits:
        d = r.data
        label = d.get("name", d["id"])
        extra = d.get("objective") or d.get("problem") or d.get("category", "")
        _print(f"  [{r.kind:9}] {d['id']:32} {label} — {extra}")
    _print(f"\n{len(hits)} result(s)")
    return 0


def cmd_rank(args) -> int:
    rec, rej = rank_mod.rank_for_pattern(args.pattern, args.profile)
    if not rec and not rej:
        _print(f"no pattern record '{args.pattern}'")
        return 1
    _print(f"# Ranking for pattern '{args.pattern}' (profile: {args.profile})")
    _print("\n## Recommended candidates (best first)")
    for s in rec:
        _print(f"  {s.score:+6.2f}  {s.id}")
        for why in s.reasons:
            _print(f"          · {why}")
    if rej:
        _print("\n## Effects this pattern explicitly rejects")
        for s in rej:
            _print(f"  {s.score:+6.2f}  {s.id}  (listed as rejected for this pattern)")
    if rec:
        _print(f"\nSelected: {rec[0].id} — simplest effective candidate with the highest transparent score.")
    return 0


def cmd_rank_sources(args) -> int:
    recs = registry.load_records("sources")
    _T = {"redistributable": 3, "adaptable-concept": 2, "reference-only": 1, "rejected": 0}
    _M = {"active": 2, "maintained": 1, "slow": 0, "stale": -1, "unknown": 0}

    def score(d):
        return (6 - d["trust_tier"]) + _T.get(d["redistribution"], 0) + _M.get(d["maintenance"], 0)

    rows = sorted(recs, key=lambda r: score(r.data), reverse=True)
    if args.category:
        rows = [r for r in rows if r.data["category"] == args.category]
    for r in rows:
        d = r.data
        _print(f"  {score(d):+3d}  tier{d['trust_tier']}  {d['id']:22} "
               f"{d['redistribution']:18} {d['maintenance']:10} {d['license']}")
    _print(f"\n{len(rows)} source(s). Higher score = more trustworthy + reusable.")
    return 0


# ---- source workflow ------------------------------------------------------

def cmd_source(args) -> int:
    if args.action == "completeness":
        rep = comp_mod.report()
        _print("# Component completeness by source\n")
        hdr = f"  {'source':22} disc  bnd  ins  adp  ref  rej  verified"
        _print(hdr)
        for sid, b in sorted(rep["per_source"].items()):
            if b["discovered"] == 0:
                continue
            _print(f"  {sid:22} {b['discovered']:4} {b['bundled']:4} {b['installable']:4} "
                   f"{b['adaptable']:4} {b['reference-only']:4} {b['rejected']:4} {b['verified']:9}")
        t = rep["totals"]
        _print(f"\n  totals: discovered={t['discovered']} bundled={t['bundled']} "
               f"installable={t['installable']} adaptable={t['adaptable']} "
               f"reference-only={t['reference-only']} rejected={t['rejected']}")
        _print("\nNote: v0.1.0 ships representative component records, not full coverage.")
        return 0

    if args.action == "scan":
        if not args.path:
            _print("usage: motif source scan <path>")
            return 2
        findings = scan_mod.scan_all(args.path)
        for f in findings:
            loc = f"{f.path}:{f.line}" if f.path else ""
            _print(f"  [{f.severity:8}] {f.scanner:18} {f.code:20} {f.message} {loc}")
        v = scan_mod.verdict(findings)
        _print(f"\nverdict: {v.upper()}  ({len(findings)} finding(s))")
        return 0 if v != "reject" else 3

    if args.action == "discover":
        pol = yaml_min.load((registry.ROOT / "security" / "domain-policy.yml").read_text())
        _print(f"runtime mode: {pol.get('mode')}")
        _print("approved official hosts (allowlist):")
        for h in pol.get("allowlist", []):
            _print(f"  - {h}")
        _print("\nUse `motif source retrieve --refresh <url>` to pull into quarantine (allowlisted only).")
        return 0

    if args.action in ("retrieve",):
        if not args.refresh:
            _print("refused: default mode is OFFLINE APPROVED REGISTRY.")
            _print("Internet retrieval requires the explicit --refresh flag and an allowlisted host.")
            return 3
        _print("retrieve --refresh: would pin version+SHA-256 into .motif/quarantine and scan before review.")
        _print("(Network retrieval is intentionally not performed in this offline build.)")
        return 0

    if args.action in ("approve", "reject"):
        _print(f"source {args.action}: moves a reviewed item between .motif/reviewed and "
               f".motif/{'approved' if args.action == 'approve' else 'rejected'} after human sign-off.")
        return 0

    _print(f"unknown source action: {args.action}")
    return 2


# ---- component workflow ---------------------------------------------------

def cmd_component(args) -> int:
    if args.action == "search":
        return cmd_search(argparse.Namespace(query=args.value or "", kind="components"))

    if args.action == "inspect":
        rec = next((r for r in registry.load_records("components") if r.data["id"] == args.value), None)
        if not rec:
            _print(f"no component '{args.value}'")
            return 1
        _print(json.dumps(rec.data, indent=2))
        return 0

    if args.action == "alternatives":
        alts = search_mod.alternatives(args.value)
        if not alts:
            _print("no alternatives in the same effect family (or unknown id)")
            return 0
        for r in alts:
            _print(f"  {r.data['id']:24} {r.data.get('name','')}")
        return 0

    if args.action == "plan-install":
        if not args.target:
            _print("usage: motif component plan-install <id> --target <dir>")
            return 2
        plan = install_mod.plan_install(args.value, args.target)
        _print(json.dumps(plan.to_dict(), indent=2))
        if plan.refused:
            _print(f"\nREFUSED: {plan.refused}")
            return 3
        _print("\nPlan only. Run `component install --approve` to apply with snapshot + provenance.")
        return 0

    if args.action == "install":
        if not args.target:
            _print("usage: motif component install <id> --target <dir> --approve")
            return 2
        target = pathlib.Path(args.target)
        plan = install_mod.plan_install(args.value, str(target))
        if plan.refused:
            _print(f"REFUSED: {plan.refused}")
            return 3
        if not args.approve:
            _print("refused: installation requires explicit --approve (controlled patch + rollback).")
            return 3
        install_mod.snapshot(target)
        target.mkdir(parents=True, exist_ok=True)
        for f in plan.files:
            if f["action"] == "create" and f.get("from"):
                src = registry.ROOT / f["from"]
                (target / pathlib.Path(f["path"]).name).write_text(src.read_text())
        manifest = install_mod.write_provenance(plan, target)
        _print(f"installed {args.value} → {target} (snapshot taken)")
        _print(f"provenance manifest: {manifest}")
        return 0

    if args.action == "rollback":
        if not args.target:
            _print("usage: motif component rollback --target <dir>")
            return 2
        ok = install_mod.rollback(pathlib.Path(args.target))
        _print("rolled back from snapshot" if ok else "no snapshot found")
        return 0 if ok else 1

    _print(f"unknown component action: {args.action}")
    return 2


# ---- generate-index -------------------------------------------------------

def cmd_generate_index(_args) -> int:
    allr = registry.load_all()
    index = {kind: [{"id": r.data["id"], "name": r.data.get("name", r.data["id"])}
                    for r in recs] for kind, recs in allr.items()}
    (registry.REGISTRY / "INDEX.json").write_text(json.dumps(index, indent=2) + "\n")
    lines = ["# Registry index", "", "_Generated by `python -m motif generate-index`._", ""]
    for kind, items in index.items():
        lines.append(f"## {kind} ({len(items)})")
        for it in items:
            lines.append(f"- `{it['id']}` — {it['name']}")
        lines.append("")
    (registry.REGISTRY / "INDEX.md").write_text("\n".join(lines))
    _print(f"wrote registry/INDEX.json and registry/INDEX.md "
           f"({sum(len(v) for v in index.values())} records)")
    return 0


# ---- parser ---------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="motif", description="Motif CLI (offline by default)")
    p.add_argument("--version", action="version", version=f"motif {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("validate", help="validate registry against schemas").set_defaults(fn=cmd_validate)
    sub.add_parser("doctor", help="environment + registry health").set_defaults(fn=cmd_doctor)

    sp = sub.add_parser("search", help="search registry records")
    sp.add_argument("query")
    sp.add_argument("--kind", choices=list(registry.KINDS))
    sp.set_defaults(fn=cmd_search)

    sp = sub.add_parser("rank", help="rank a pattern's effect candidates transparently")
    sp.add_argument("pattern")
    sp.add_argument("--profile", default=rank_mod.DEFAULT_PROFILE)
    sp.set_defaults(fn=cmd_rank)

    sp = sub.add_parser("rank-sources", help="rank sources by trust + reusability")
    sp.add_argument("--category")
    sp.set_defaults(fn=cmd_rank_sources)

    sp = sub.add_parser("source", help="source governance workflow")
    sp.add_argument("action", choices=["discover", "retrieve", "scan", "approve", "reject", "completeness"])
    sp.add_argument("path", nargs="?")
    sp.add_argument("--refresh", action="store_true")
    sp.set_defaults(fn=cmd_source)

    sp = sub.add_parser("component", help="component inspect / install workflow")
    sp.add_argument("action", choices=["search", "inspect", "alternatives", "plan-install", "install", "rollback"])
    sp.add_argument("value", nargs="?")
    sp.add_argument("--target")
    sp.add_argument("--approve", action="store_true")
    sp.set_defaults(fn=cmd_component)

    sub.add_parser("generate-index", help="write registry/INDEX.{json,md}").set_defaults(fn=cmd_generate_index)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv if argv is not None else sys.argv[1:])
    return args.fn(args)
