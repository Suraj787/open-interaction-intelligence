"""Motif v3 ("Motif Live") CLI commands, registered onto the main parser.

Deterministic commands run; browser-runtime commands report their experimental status
honestly rather than faking output.
"""
from __future__ import annotations
import json
import datetime
import pathlib

from . import run as run_mod, twin as twin_mod, findings as findings_mod
from . import policy as policy_mod, memory as memory_mod, atlas as atlas_mod
from . import system as system_mod, guardian as guardian_mod, mcp as mcp_mod
from . import bench as bench_mod, studio as studio_mod, recommend as rec_mod
from . import concepts as concepts_mod, runtime as runtime_mod
from . import evidence as ev_mod, apprunner as app_mod, browser as browser_mod
from . import repair as repair_mod, report as report_mod
from motif import install as install_mod, project as project_mod


def _stamp() -> str:
    return datetime.date.today().isoformat().replace("-", "")


def _p(s=""):
    print(s)


def _jp(obj):
    print(json.dumps(obj, indent=2))


# ---- init / run / create / improve / autopilot ----------------------------

def cmd_init(a) -> int:
    s = run_mod.init(a.target or ".", _stamp())
    _p("Motif found:\n")
    _p(f"  Framework       {s['framework']}")
    _p(f"  Styling         {s['styling']}")
    _p(f"  Routes          {s['routes']}")
    _p(f"  Components       {s['components']}")
    _p(f"  Design tokens   {s['design_tokens']}")
    _p(f"  Profile         {s['profile']}")
    _p(f"  Confidence      {int(s['confidence']*100)}%")
    _p("\nImportant gaps:")
    for g in s["gaps"]:
        _p(f"  - {g}")
    _p(f"\nFindings: {s['findings']['total']}  by severity: {s['findings']['by_severity']}")
    _p("State written to .motif/. Next: `motif studio` or `motif improve --goal ...`")
    return 0


def cmd_run(a) -> int:
    mode = a.mode or "improve"
    if mode in ("improve", "audit", "repair", "redesign"):
        _jp(run_mod.improve(a.target or ".", a.goal, mode, a.profile, _stamp()))
    elif mode == "create":
        _jp(run_mod.create(a.goal or "", a.framework or "vue", a.profile, _stamp(), a.target or "."))
    elif mode == "govern":
        r = guardian_mod.guard(a.target or ".", "branch", a.base)
        _p(guardian_mod.report(r))
    elif mode == "benchmark":
        _jp(bench_mod.run(a.target or "."))
    else:
        _p(f"unknown mode {mode}")
        return 2
    return 0


def cmd_create(a) -> int:
    _jp(run_mod.create(a.goal or "", a.framework or "vue", a.profile, _stamp(), a.target or "."))
    return 0


def cmd_improve(a) -> int:
    _jp(run_mod.improve(a.target or ".", a.goal, a.mode or "improve", a.profile, _stamp()))
    return 0


def cmd_autopilot(a) -> int:
    r = run_mod.autopilot(a.target or ".", a.goal or "", a.profile, _stamp())
    for g in r["gates"]:
        _p(f"  gate {g['gate']:14} [{g['status']}] confidence {g['confidence']}")
    _p("\n" + r["note"])
    return 0


# ---- twin / findings / policy / memory ------------------------------------

def cmd_twin(a) -> int:
    t = a.target or "."
    if a.action == "build":
        out = twin_mod.write(t, twin_mod.build(t, _stamp()))
        _p(f"twin manifest: {out}")
        return 0
    if a.action in ("inspect", "validate"):
        m = twin_mod.load(t)
        if not m:
            _p("no twin; run `motif twin build`")
            return 1
        _jp({"project": m["project"], "framework": m.get("framework"),
             "routes": len(m.get("routes", [])), "components": len(m.get("components", [])),
             "rendered": m.get("rendered")})
        return 0
    _p("usage: motif twin [build|inspect|validate]")
    return 2


def cmd_findings(a) -> int:
    t = a.target or "."
    if a.action == "audit":
        fnd = findings_mod.audit_project(t)
        for f in fnd:
            findings_mod.save(t, f)
        _p(f"{len(fnd)} finding(s) written. {findings_mod.summarize(fnd)['by_severity']}")
        return 0
    if a.action == "list":
        for f in findings_mod.load(t):
            _p(f"  [{f['severity']:8}] {f['id']} {f['type']:14} {f['rule']:24} "
               f"{f['location'].get('file') or f['location'].get('component','')}  ({f['status']})")
        return 0
    if a.action == "show":
        f = next((x for x in findings_mod.load(t) if x["id"] == a.value), None)
        if not f:
            _p("not found")
            return 1
        _jp(f)
        return 0
    if a.action in ("accept", "fix", "verify", "suppress"):
        status = {"accept": "accepted-risk", "fix": "fixed", "verify": "verified", "suppress": "false-positive"}[a.action]
        supp = None
        if a.action in ("accept", "suppress"):
            if not a.reason:
                _p("--reason required for accept/suppress")
                return 2
            supp = {"reason": a.reason, "scope": a.scope or "finding", "author": "user",
                    "expiry": a.expiry or "review-in-90-days"}
        ok = findings_mod.set_status(t, a.value, status, supp)
        _p(f"{a.value} -> {status}" if ok else "not found / invalid")
        return 0 if ok else 1
    _p("usage: motif findings [audit|list|show|accept|fix|verify|suppress] <id>")
    return 2


def cmd_policy(a) -> int:
    t = a.target or "."
    if a.action == "init":
        _p(f"wrote {policy_mod.init(t)}")
        return 0
    if a.action == "explain":
        _p("\n".join(policy_mod.explain(t)))
        return 0
    if a.action in ("validate", "check"):
        fnd = findings_mod.load(t)
        from . import debt as debt_mod, originality as orig_mod
        d = debt_mod.calculate(t).score
        _f, conv, _b = orig_mod.audit_path(t)
        res = policy_mod.check(t, fnd, d, conv)
        _jp({"blocking": res["blocking"], "violations": res["violations"],
             "debt": d, "convergence": conv})
        return 0 if not res["blocking"] else 3
    _p("usage: motif policy [init|validate|check|explain]")
    return 2


def cmd_memory(a) -> int:
    t = a.target or "."
    if a.action == "list":
        for m in memory_mod.load(t):
            _p(f"  {m['id']:28} {m['type']:20} [{m.get('status','active')}] {m['content'][:60]}")
        return 0
    if a.action == "add":
        if not (a.id and a.type and a.content):
            _p("usage: motif memory add --id X --type rejected-approach --content '...'")
            return 2
        ok, msg = memory_mod.add(t, a.id, a.type, a.content, datetime.date.today().isoformat(),
                                 expiry=a.expiry)
        _p(msg)
        return 0 if ok else 2
    if a.action == "invalidate":
        ok = memory_mod.invalidate(t, a.value)
        _p("invalidated" if ok else "not found")
        return 0 if ok else 1
    if a.action == "explain":
        for m in memory_mod.rejected_approaches(t):
            _p(f"  rejected: {m['content']}")
        return 0
    _p("usage: motif memory [list|add|invalidate|explain]")
    return 2


# ---- atlas / system / guard / mcp / bench / studio ------------------------

def cmd_atlas(a) -> int:
    if a.action in ("build", "publish"):
        res = atlas_mod.build(a.out)
        _p(f"Atlas built: {res['pages']} pages -> {res['out']}  {res['counts']}")
        if a.action == "publish":
            _p("publish: copy the generated static site to your host (e.g. GitHub Pages).")
        return 0
    _p("usage: motif atlas [build|publish] [--out DIR]")
    return 2


def cmd_system(a) -> int:
    t = a.target or "."
    if a.action == "extract":
        res = system_mod.extract(t)
        out = system_mod.write(t, res)
        _p(f"design system extracted -> {out}")
        _jp({"variables": len(res["css_variables"]), "tailwind": res["tailwind"],
             "exceptions": res["exceptions"]})
        return 0
    if a.action == "violations":
        res = system_mod.extract(t)
        for e in res["exceptions"]:
            _p(f"  - {e}")
        if not res["exceptions"]:
            _p("  none detected")
        return 0
    _p("usage: motif system [extract|violations]")
    return 2


def cmd_guard(a) -> int:
    r = guardian_mod.guard(a.target or ".", a.action, a.base)
    _p(guardian_mod.report(r, a.format or "text"))
    return 3 if r["blocking"] else 0


def cmd_mcp(a) -> int:
    if a.action == "serve":
        return mcp_mod.serve(allow_write=a.allow_write)
    _p("usage: motif mcp serve [--allow-write]")
    return 2


def cmd_bench(a) -> int:
    if getattr(a, "scenario", None) in ("vue-dashboard-evidence-repair", "golden"):
        t = a.target or "evals/fixtures/sample-vue-app"
        req = getattr(a, "require_browser", False)
        result = repair_mod.golden(t, "/projects", require_browser=req)
        result["target"] = t
        report_mod.generate(t, "bench-golden", result)
        steps = {s["step"]: s["status"] for s in result["steps"]}
        det_pass = all(steps.get(k) == "passed" for k in
                       ("detect", "apply-in-worktree", "verify-finding-closed (static)",
                        "rollback (exact)", "baseline-unchanged"))
        _jp({"scenario": "vue-dashboard-evidence-repair",
             "deterministic_steps": {k: v for k, v in steps.items()},
             "deterministic_pass": det_pass,
             "browser_proven": result.get("browser_proven"),
             "outcome": result.get("outcome"),
             "require_browser": req,
             "metrics": {"seeded_issue_detected": steps.get("detect") == "passed",
                         "repair_success_static": steps.get("verify-finding-closed (static)") == "passed",
                         "runtime_finding_closed": steps.get("verify-runtime-finding-closed"),
                         "rollback_exact": steps.get("rollback (exact)") == "passed",
                         "baseline_unchanged": steps.get("baseline-unchanged") == "passed",
                         "regression": steps.get("regression-check")},
             "note": "Deterministic and browser metrics kept separate; not merged into one score."})
        return 0 if result.get("outcome") != "failed" else 3
    _jp(bench_mod.run(a.target or "."))
    return 0


def cmd_studio(a) -> int:
    if a.build_only:
        out = studio_mod.build(a.target or ".")
        _p(f"Studio built: {out}")
        return 0
    return studio_mod.serve(a.target or ".", a.port or 7777)


# ---- compile / compare / recommend / concepts -----------------------------

def cmd_compile(a) -> int:
    if a.action == "plan":
        if not (a.component and a.target):
            _p("usage: motif compile plan --component <id> --target <dir>")
            return 2
        plan = install_mod.plan_install(a.component, a.target)
        _jp(plan.to_dict())
        return 0 if plan.refused is None else 3
    if a.action in ("preview",):
        _p("compile preview: rendering a static/interactive preview requires the runtime "
           "(experimental in v3.0.0). Use `motif compile plan` for the deterministic plan.")
        return 0
    if a.action in ("apply", "rollback", "pr"):
        _p(f"compile {a.action}: controlled apply/rollback is provided by the installer "
           f"(`motif component install/rollback`); full screen-compiler {a.action} is planned for v3.1.")
        return 0
    _p("usage: motif compile [plan|preview|apply|rollback|pr]")
    return 2


def cmd_compare(a) -> int:
    _p("motif compare: pixel/structural/semantic visual comparison requires rendered "
       "screenshots from the runtime (experimental in v3.0.0). The schema and levels are "
       "defined; runtime rendering is planned.")
    return 0


def cmd_recommend(a) -> int:
    _jp(rec_mod.recommend(a.pattern, a.profile or "saas-balanced"))
    return 0


def cmd_concepts(a) -> int:
    t = a.target or "."
    if a.action == "generate":
        c = concepts_mod.generate(t, a.goal or "improve", 3)
        concepts_mod.write(t, a.goal or "improve", c)
        for x in c:
            _p(f"  {x['id']}: {x['direction']}")
        return 0
    if a.action in ("compare", "select", "preview"):
        loaded = concepts_mod.load(t)
        if a.action == "preview":
            _p("concept preview against a running app is experimental (needs the runtime).")
            return 0
        for x in loaded:
            _p(f"  {x['id']}  complexity={x['implementation_complexity']} risk={x['migration_risk']}")
        return 0
    _p("usage: motif concepts [generate|compare|select|preview]")
    return 2


# ---- v3.1: evidence / app / repair ----------------------------------------

def cmd_evidence(a) -> int:
    act = a.action
    if act == "validate":
        counts, errs = ev_mod.validate()
        for k, n in counts.items():
            _p(f"  {k}: {n}")
        if errs:
            for e in errs[:30]:
                _p(f"  - {e}")
            return 1
        _p("OK: evidence graph valid")
        return 0
    if act == "index":
        _p(f"wrote {ev_mod.build_index()}")
        return 0
    if act == "query":
        ctx = {}
        for dim, vals in (("product_forms", a.product_form), ("purposes", a.purpose),
                          ("workflows", a.workflow), ("expertise", a.expertise),
                          ("abilities", a.ability), ("devices", a.device),
                          ("environments", a.environment)):
            if vals:
                ctx[dim] = vals.split(",")
        if a.risk:
            ctx["risks"] = [{"type": r.split(":")[0], "severity": int(r.split(":")[1]) if ":" in r else 3}
                            for r in a.risk.split(",")]
        explain = getattr(a, "explain_matching", False)
        _jp(ev_mod.query(ctx, explain=explain))
        return 0
    if act == "explain":
        _jp(ev_mod.explain(a.value or ""))
        return 0
    if act == "sources":
        for s in ev_mod._load("sources"):
            _p(f"  tier{s['tier']}  {s['id']:28} {s['title']}")
        return 0
    if act == "check-myth":
        _jp(ev_mod.check_myth(a.value or ""))
        return 0
    if act == "contradictions":
        for c in ev_mod._load("contradictions"):
            _p(f"  {c['id']:34} {c['topic']}  ({c.get('resolution_type')})")
        return 0
    if act == "stale":
        st = ev_mod.stale_claims()
        _p("\n".join(f"  {s}" for s in st) or "  no stale claims")
        return 0
    if act == "pack":
        p = next((x for x in ev_mod._load("packs") if x["id"] == a.value), None)
        _jp(p or {"error": "pack not found"})
        return 0 if p else 1
    _p("usage: motif evidence [validate|index|query|explain|sources|check-myth|contradictions|stale|pack]")
    return 2


def cmd_app(a) -> int:
    t = a.target or "."
    if a.action == "start":
        h = app_mod.start(t, a.port, a.cmd, approve=a.approve)
        _jp({"status": h.status, "url": h.url, "pid": h.pid, "command": h.command, "reason": h.reason})
        return 0 if h.status == "started" else 3
    if a.action == "status":
        pm = runtime_mod.model_project(t)
        _jp({"start_command": pm.start_command, "build_command": pm.build_command,
             "package_manager": pm.package_manager, "routes": pm.routes})
        return 0
    if a.action == "stop":
        _p("stopped" if app_mod.stop(a.pid) else "no pid / not running")
        return 0
    _p("usage: motif app [start|status|stop]")
    return 2


def cmd_repair(a) -> int:
    if a.action == "golden":
        t = a.target or "evals/fixtures/sample-vue-app"
        result = repair_mod.golden(t, a.route, require_browser=getattr(a, "require_browser", False))
        result["target"] = t
        rid = "repair-" + (a.route or "projects").strip("/").replace("/", "-")
        rdir = report_mod.generate(t, rid, result)
        for s in result["steps"]:
            _p(f"  {s['step']:34} {s['status']}")
        _p(f"\noutcome: {result.get('outcome')}")
        _p(f"browser proven: {result.get('browser_proven')}")
        _p(f"report: {rdir}/report.html")
        return 0 if result.get("outcome") != "failed" else 3
    _p("usage: motif repair golden [--target ... --route /projects] [--require-browser]")
    return 2


def register(sub) -> None:
    def add(name, fn, help, args=()):
        sp = sub.add_parser(name, help=help)
        for a_args, a_kw in args:
            sp.add_argument(*a_args, **a_kw)
        sp.set_defaults(fn=fn)
        return sp

    T = (("--target",), {})
    G = (("--goal",), {})
    PR = (("--profile",), {"default": "saas-balanced"})

    add("init", cmd_init, "first-run: inspect, create .motif/, first audit", [T])
    add("run", cmd_run, "flagship loop (create/improve/audit/...)",
        [T, G, PR, (("--mode",), {}), (("--framework",), {}), (("--base",), {})])
    add("create", cmd_create, "create a new interface from a goal/spec",
        [T, G, PR, (("--framework",), {}), (("--spec",), {})])
    add("improve", cmd_improve, "improve an existing interface",
        [T, G, PR, (("--mode",), {}), (("--route",), {})])
    add("autopilot", cmd_autopilot, "gated end-to-end run (stops for approval)", [T, G, PR])

    sp = add("twin", cmd_twin, "Visual Twin (static)", [T]); sp.add_argument("action", choices=["build", "inspect", "validate"])
    sp = add("findings", cmd_findings, "unified findings", [T, (("--reason",), {}), (("--scope",), {}), (("--expiry",), {})])
    sp.add_argument("action", choices=["audit", "list", "show", "accept", "fix", "verify", "suppress"])
    sp.add_argument("value", nargs="?")
    sp = add("policy", cmd_policy, "policy as code", [T]); sp.add_argument("action", choices=["init", "validate", "check", "explain"])
    sp = add("memory", cmd_memory, "project memory",
             [T, (("--id",), {}), (("--type",), {}), (("--content",), {}), (("--expiry",), {})])
    sp.add_argument("action", choices=["list", "add", "invalidate", "explain"]); sp.add_argument("value", nargs="?")
    sp = add("atlas", cmd_atlas, "build the static Atlas catalogue", [(("--out",), {})]); sp.add_argument("action", choices=["build", "publish"])
    sp = add("system", cmd_system, "design-system extraction", [T]); sp.add_argument("action", choices=["extract", "violations"])
    sp = add("guard", cmd_guard, "Guardian: scan a diff", [T, (("--base",), {}), (("--format",), {})]); sp.add_argument("action", choices=["staged", "branch"])
    sp = add("mcp", cmd_mcp, "MCP server", [(("--allow-write",), {"action": "store_true"})]); sp.add_argument("action", choices=["serve"])
    add("bench", cmd_bench, "InterfaceBench runner (automated measures or golden scenario)",
        [T, (("--scenario",), {}), (("--require-browser",), {"action": "store_true", "dest": "require_browser"})])
    add("studio", cmd_studio, "local Studio viewer", [T, (("--port",), {"type": int}), (("--build-only",), {"action": "store_true"})])
    sp = add("compile", cmd_compile, "compiler (plan implemented; apply via installer)",
             [(("--component",), {}), (("--target",), {})]); sp.add_argument("action", choices=["plan", "preview", "apply", "rollback", "pr"])
    add("compare", cmd_compare, "semantic visual comparison (experimental)", [(("--baseline",), {}), (("--candidate",), {})])
    add("recommend", cmd_recommend, "contextual recommendation", [(("pattern",), {}), PR])
    sp = add("concepts", cmd_concepts, "breadth-first concepts", [T, G]); sp.add_argument("action", choices=["generate", "compare", "select", "preview"])

    # v3.1 evidence-grounded runtime
    sp = add("evidence", cmd_evidence, "UX Evidence Graph",
             [(("--product-form",), {"dest": "product_form"}), (("--purpose",), {}),
              (("--workflow",), {}), (("--expertise",), {}), (("--ability",), {}),
              (("--risk",), {}), (("--device",), {}), (("--environment",), {}),
              (("--explain-matching",), {"action": "store_true", "dest": "explain_matching"})])
    sp.add_argument("action", choices=["validate", "index", "query", "explain", "sources",
                                       "check-myth", "contradictions", "stale", "pack"])
    sp.add_argument("value", nargs="?")
    sp = add("app", cmd_app, "safe application runner",
             [T, (("--port",), {"type": int}), (("--cmd",), {}), (("--pid",), {"type": int}),
              (("--approve",), {"action": "store_true"})])
    sp.add_argument("action", choices=["start", "status", "stop"])
    sp = add("repair", cmd_repair, "evidence-grounded repair (golden loop)",
             [T, (("--route",), {}), (("--require-browser",), {"action": "store_true", "dest": "require_browser"})])
    sp.add_argument("action", choices=["golden"])
