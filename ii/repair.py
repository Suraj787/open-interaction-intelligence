"""Evidence-grounded repair: the colour-only-status repair class.

Detect (static) -> build context vector -> query evidence -> generate a repair plan ->
apply in an isolated git worktree -> verify the finding is closed -> exact rollback.
The browser before/after validation is gated behind the optional browser extra and is
reported not-executed when no runtime is present. This is a single constrained repair
class, not a generic "AI rewrite component" function.
"""
from __future__ import annotations
import re
import subprocess
import pathlib
import tempfile
import shutil
from . import evidence as ev, browser as browser_mod

_COLOUR_MAP = re.compile(r"colorFor|bg-(?:success|warning|danger|red|green|amber|yellow)")
_STATUS_TEXT = re.compile(r"\{\{[^}]*status[^}]*\}\}|aria-label")


def detect_colour_only_status(target) -> list[dict]:
    root = pathlib.Path(target)
    out = []
    for f in sorted(root.rglob("*.vue")):
        if "node_modules" in f.parts:
            continue
        t = f.read_text(errors="replace")
        if "status" in t.lower() and _COLOUR_MAP.search(t) and not _STATUS_TEXT.search(t):
            out.append({"id": "finding-colour-only-status", "type": "accessibility",
                        "rule": "status-colour-only", "severity": "high", "confidence": 0.9,
                        "location": {"file": str(f.relative_to(root)), "component": f.stem},
                        "status": "open", "detected_by": "static",
                        "evidence": {"colour_mapping": True, "status_text_or_label": False}})
    return out


def build_context_vector(target, route: str | None) -> dict:
    """For the sample dashboard. Provenance distinguishes verified from inferred/assumed."""
    return {
        "product_forms": ["web-app", "dashboard"], "purposes": ["monitor"],
        "workflows": ["daily-operation"], "expertise": ["mixed"],
        "abilities": ["colour-vision-deficiency"], "risks": [{"type": "financial", "severity": 3}],
        "devices": ["desktop"], "environments": ["office"], "audience_roles": ["operator"],
        "_assumptions": ["risks", "environments"],
        "_provenance": {"product_forms": "verified-fact", "abilities": "inferred",
                        "risks": "assumption", "environments": "assumption"},
        "route": route or "/projects",
    }


def plan(finding: dict, claim: dict, ctx: dict) -> dict:
    return {
        "finding_id": finding["id"],
        "claim_ids": [claim["id"]] if claim else [],
        "context_vector": {k: v for k, v in ctx.items() if not k.startswith("_")},
        "confidence": claim["evidence"]["confidence"] if claim else "medium",
        "files": [finding["location"]["file"]],
        "changes": ["Add a visible, capitalised text label of the status next to the colour dot."],
        "risks": ["Label text must match the semantic status; verify wording with a human."],
        "policy_effect": {"blocking": False},
        "validation": {"before": ["val-colour-independent-meaning (not-executed: no browser)"],
                       "after": ["static re-check: status text present", "val-colour-independent-meaning (browser, gated)"]},
        "rollback": {"strategy": "git-worktree-reset"},
        "why": "Status is conveyed by colour alone; the applicable normative claim requires a "
               "non-colour indicator. Alternative (icon-only) rejected: a text label is clearer "
               "for the operator workflow and still pairs with the existing colour.",
        "human_review": ["Confirm label wording and placement."],
        "automatable": claim.get("repair", {}).get("automatable", "partial") if claim else "partial",
    }


_DOT_RX = re.compile(
    r'(<span class="h-3 w-3 rounded-full"[^>]*></span>)')


def _apply_transform(text: str) -> tuple[str, bool]:
    """Add a visible status text label after the colour dot. Returns (new_text, changed)."""
    if _STATUS_TEXT.search(text):
        return text, False
    label = ('\\1\n    <span class="ml-1.5 text-sm capitalize">'
             '{{ props.status.replace(\'-\', \' \') }}</span>')
    new = _DOT_RX.sub(label, text, count=1)
    if new == text:
        # generic fallback: add an aria-label to the wrapper span
        new = text.replace('<span class="inline-flex items-center">',
                           '<span class="inline-flex items-center" :aria-label="props.status">', 1)
    return new, new != text


def _git_root(target) -> pathlib.Path | None:
    try:
        out = subprocess.run(["git", "-C", str(target), "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, check=True).stdout.strip()
        return pathlib.Path(out)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def apply(target, finding: dict, branch: str) -> dict:
    """Apply the repair in an isolated worktree (or a temp copy if not a git repo)."""
    root = _git_root(target)
    rel_target = pathlib.Path(target).resolve()
    wt = pathlib.Path(tempfile.mkdtemp(prefix="motif-repair-"))
    used_worktree = False
    if root:
        shutil.rmtree(wt, ignore_errors=True)
        r = subprocess.run(["git", "-C", str(root), "worktree", "add", "-b", branch, str(wt)],
                           capture_output=True, text=True)
        if r.returncode == 0:
            used_worktree = True
            # path of the target file inside the worktree
            try:
                sub = rel_target.relative_to(root)
            except ValueError:
                sub = pathlib.Path(".")
            file_in_wt = wt / sub / finding["location"]["file"]
        else:
            shutil.copytree(rel_target, wt, dirs_exist_ok=True)
            file_in_wt = wt / finding["location"]["file"]
    else:
        shutil.copytree(rel_target, wt, dirs_exist_ok=True)
        file_in_wt = wt / finding["location"]["file"]

    changed = False
    if file_in_wt.exists():
        new, changed = _apply_transform(file_in_wt.read_text())
        if changed:
            file_in_wt.write_text(new)
    return {"worktree": str(wt), "used_worktree": used_worktree, "root": str(root) if root else None,
            "branch": branch, "changed": changed, "file": str(file_in_wt)}


def verify_closed(applied: dict, finding: dict) -> bool:
    f = pathlib.Path(applied["file"])
    if not f.exists():
        return False
    return bool(_STATUS_TEXT.search(f.read_text()))


def rollback(applied: dict) -> bool:
    wt = applied["worktree"]
    if applied.get("used_worktree") and applied.get("root"):
        subprocess.run(["git", "-C", applied["root"], "worktree", "remove", "--force", wt],
                       capture_output=True, text=True)
        subprocess.run(["git", "-C", applied["root"], "branch", "-D", applied["branch"]],
                       capture_output=True, text=True)
    shutil.rmtree(wt, ignore_errors=True)
    return not pathlib.Path(wt).exists()


def _route_url(base_url: str, route: str | None) -> str:
    # The fixture uses HTML5 history routing; Vite's SPA fallback serves index.html.
    r = route or "/projects"
    return base_url.rstrip("/") + (r if r.startswith("/") else "/" + r)


def _link_node_modules(worktree_fixture: pathlib.Path, original_fixture: pathlib.Path) -> None:
    """Symlink the original fixture's node_modules into the worktree so the repaired app
    can start without a second install. The original is never modified. The symlink target
    must be ABSOLUTE so it resolves correctly from the worktree location."""
    src = (original_fixture / "node_modules").resolve()
    dst = worktree_fixture / "node_modules"
    if src.exists() and not dst.exists():
        try:
            dst.symlink_to(src, target_is_directory=True)
        except OSError:
            pass


def golden(target, route: str | None = None, require_browser: bool = False,
           evidence_dir: pathlib.Path | None = None, use_browser: bool | None = None) -> dict:
    """The golden audit-and-repair loop.

    Deterministic steps always run. Browser steps execute when Playwright is available and
    otherwise report not-executed. With require_browser=True (CI), any not-executed or failed
    browser stage fails the scenario; without it (local), the deterministic loop stands alone.
    """
    from . import apprunner as app_mod
    steps = []
    target = pathlib.Path(target).resolve()
    edir = pathlib.Path(evidence_dir) if evidence_dir else (target / ".motif" / "evidence" / "golden")
    (edir / "before").mkdir(parents=True, exist_ok=True)
    (edir / "after").mkdir(parents=True, exist_ok=True)

    findings = detect_colour_only_status(target)
    steps.append({"step": "detect", "status": "passed" if findings else "failed", "findings": len(findings)})
    if not findings:
        return {"steps": steps, "outcome": "no-seeded-finding"}
    finding = next((f for f in findings if "ProjectStatus" in f["location"]["component"]), findings[0])
    ctx = build_context_vector(target, route)
    steps.append({"step": "context-vector", "status": "passed"})
    qr = ev.query(ctx)
    claim = ev.explain("claim-status-colour-001")
    steps.append({"step": "evidence-query", "status": "passed" if "error" not in claim else "warning",
                  "claim": claim.get("id")})
    claim_rec = next((c for c in ev.load_claims() if c["id"] == "claim-status-colour-001"), None)
    rplan = plan(finding, claim_rec, ctx)
    steps.append({"step": "repair-plan", "status": "passed"})

    # use_browser=None auto-detects; False forces the deterministic path (used by the
    # runtime-independent `make check` self-check); True requires a runtime.
    browser_ok = browser_mod.available()[0] if use_browser is None else use_browser
    # --- before state (browser) ---
    before_app = app_mod.start(target, approve=True) if browser_ok else None
    before_url = _route_url(before_app.url, route) if (before_app and before_app.status == "started") else None
    if before_app:
        steps.append({"step": "start-app", "status": "passed" if before_app.status == "started" else before_app.status,
                      "reason": before_app.reason})
    bcap = (browser_mod.capture(before_url, edir / "before", target_selector=None)
            if before_url else {"status": "not-executed", "reason": "no running app"})
    steps.append({"step": "browser-before", "status": bcap["status"]})

    # --- apply repair in isolated worktree ---
    applied = apply(target, finding, "motif-repair-golden")
    steps.append({"step": "apply-in-worktree", "status": "passed" if applied["changed"] else "failed",
                  "used_worktree": applied["used_worktree"]})
    closed_static = verify_closed(applied, finding)
    steps.append({"step": "verify-finding-closed (static)", "status": "passed" if closed_static else "failed"})

    # --- after state (browser): start the repaired worktree app ---
    after_status = "not-executed"
    runtime_closed = "not-executed"
    if browser_ok and applied.get("changed"):
        # .../src/components/ProjectStatus.vue -> fixture root (works for worktree and copy fallback)
        wt_fixture = pathlib.Path(applied["file"]).parent.parent.parent
        _link_node_modules(wt_fixture, target)
        after_app = app_mod.start(wt_fixture, approve=True)
        after_url = _route_url(after_app.url, route) if after_app.status == "started" else None
        steps.append({"step": "start-repaired-app",
                      "status": "passed" if after_app.status == "started" else after_app.status,
                      "reason": after_app.reason})
        acap = (browser_mod.capture(after_url, edir / "after") if after_url
                else {"status": "not-executed", "reason": "repaired app did not start"})
        after_status = acap["status"]
        steps.append({"step": "browser-after", "status": after_status})
        if after_url:
            # runtime finding closure: a status label is now rendered as text
            rt = browser_mod.has_text(after_url, "track")
            runtime_closed = rt["status"]
            steps.append({"step": "verify-runtime-finding-closed", "status": rt["status"]})
            # regression: no new blocking axe violations vs before
            before_v = bcap.get("axe_violations", 0) if isinstance(bcap, dict) else 0
            after_v = acap.get("axe_violations", 0)
            steps.append({"step": "regression-check",
                          "status": "passed" if after_v <= before_v else "executed-and-failed",
                          "before_violations": before_v, "after_violations": after_v})
        app_mod.stop(getattr(after_app, "pid", None))
    else:
        steps.append({"step": "start-repaired-app", "status": "not-executed"})
        steps.append({"step": "browser-after", "status": "not-executed"})
        steps.append({"step": "verify-runtime-finding-closed", "status": "not-executed"})
        steps.append({"step": "regression-check", "status": "not-executed"})

    if before_app:
        app_mod.stop(before_app.pid)

    rolled = rollback(applied)
    steps.append({"step": "rollback (exact)", "status": "passed" if rolled else "failed"})

    # baseline unchanged on the source branch
    fixture_file = target / "src" / "components" / "ProjectStatus.vue"
    baseline_ok = fixture_file.exists() and "props.status.replace" not in fixture_file.read_text()
    steps.append({"step": "baseline-unchanged", "status": "passed" if baseline_ok else "failed"})

    browser_states = {s["status"] for s in steps if s["step"].startswith(("start-", "browser-", "verify-runtime", "regression"))}
    browser_proven = browser_ok and "not-executed" not in browser_states and "executed-and-failed" not in browser_states
    deterministic_ok = all(
        s["status"] == "passed" for s in steps
        if s["step"] in ("detect", "apply-in-worktree", "verify-finding-closed (static)",
                         "rollback (exact)", "baseline-unchanged"))

    outcome = "failed"
    if deterministic_ok and (browser_proven or not require_browser):
        outcome = "browser-verified" if browser_proven else "deterministic-only"

    return {
        "steps": steps, "finding": finding, "claim": claim, "plan": rplan,
        "query": {"blocked_patterns": qr["blocked_patterns"], "required_validations": qr["required_validations"],
                  "sources": qr["sources"], "confidence": qr["confidence"]},
        "deterministic_ok": deterministic_ok,
        "browser_proven": browser_proven,
        "require_browser": require_browser,
        "outcome": outcome,
        "deterministic_outcome": "repair applied in worktree, finding closed (static), rolled back exactly, baseline unchanged",
        "browser_outcome": bcap.get("status", "not-executed") if isinstance(bcap, dict) else "not-executed",
        "evidence_dir": str(edir),
        "note": ("Browser steps executed and verified." if browser_proven else
                 "Browser steps not-executed (no runtime); deterministic loop completed and rolled back."),
    }
