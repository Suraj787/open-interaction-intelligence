"""Motif Runtime: project state, run records, detection, isolated worktrees.

Deterministic and dependency-free. Browser orchestration and safe live-process start
are part of the runtime contract but require a browser runtime (Playwright); those steps
are marked experimental and are not executed here. Code modification always happens in an
isolated git worktree, never on the user's main branch without an explicit apply step.
"""
from __future__ import annotations
import json
import pathlib
import subprocess
from dataclasses import dataclass, field
from motif import project as project_mod

STATE_DIRS = ["project", "twin", "findings", "concepts", "previews", "decisions",
              "evidence", "baselines", "policies", "runs", "rollback", "design-system",
              "memory"]


def state_root(target: str | pathlib.Path) -> pathlib.Path:
    return pathlib.Path(target) / ".motif"


def ensure_state(target: str | pathlib.Path) -> pathlib.Path:
    root = state_root(target)
    for d in STATE_DIRS:
        (root / d).mkdir(parents=True, exist_ok=True)
    return root


@dataclass
class ProjectModel:
    target: str
    framework: str
    typescript: bool
    tailwind: bool
    dependency_count: int
    routes: list[str] = field(default_factory=list)
    start_command: str | None = None
    build_command: str | None = None
    package_manager: str | None = None
    components: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return self.__dict__


_ROUTE_RX = [r"path:\s*['\"]([^'\"]+)['\"]", r"<Route\s+path=['\"]([^'\"]+)['\"]"]


def _detect_routes(root: pathlib.Path) -> list[str]:
    import re
    routes: set[str] = set()
    for f in root.rglob("*"):
        if f.is_file() and f.suffix in (".js", ".ts", ".jsx", ".tsx", ".vue") \
           and "node_modules" not in f.parts and ("rout" in f.name.lower() or "App" in f.name):
            try:
                txt = f.read_text(errors="replace")
            except OSError:
                continue
            for rx in _ROUTE_RX:
                routes.update(re.findall(rx, txt))
    return sorted(r for r in routes if r.startswith("/"))


def _detect_components(root: pathlib.Path) -> list[str]:
    comps = []
    for f in root.rglob("*"):
        if f.is_file() and f.suffix in (".vue", ".jsx", ".tsx") and "node_modules" not in f.parts:
            comps.append(f.stem)
    return sorted(set(comps))


def model_project(target: str | pathlib.Path) -> ProjectModel:
    root = pathlib.Path(target)
    info = project_mod.detect(target)
    pm = "pnpm" if (root / "pnpm-lock.yaml").exists() else \
         "yarn" if (root / "yarn.lock").exists() else \
         "npm" if (root / "package-lock.json").exists() or info.dependencies else None
    scripts = {}
    pkg = root / "package.json"
    if pkg.exists():
        try:
            scripts = json.loads(pkg.read_text()).get("scripts", {})
        except (OSError, json.JSONDecodeError):
            scripts = {}
    start = next((scripts[k] and f"{pm or 'npm'} run {k}" for k in ("dev", "start", "serve") if k in scripts), None)
    build = next((f"{pm or 'npm'} run {k}" for k in ("build",) if k in scripts), None)
    return ProjectModel(
        target=str(root), framework=info.framework, typescript=info.typescript,
        tailwind=info.tailwind, dependency_count=len(info.dependencies),
        routes=_detect_routes(root), start_command=start, build_command=build,
        package_manager=pm, components=_detect_components(root))


def create_worktree(target: str | pathlib.Path, branch: str) -> tuple[bool, str]:
    """Create an isolated git worktree for safe modification. Returns (ok, path-or-msg)."""
    root = pathlib.Path(target).resolve()
    wt = state_root(target) / "rollback" / branch
    try:
        subprocess.run(["git", "-C", str(root), "worktree", "add", "-b", branch, str(wt)],
                       check=True, capture_output=True, text=True)
        return True, str(wt)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        return False, getattr(e, "stderr", str(e))


def next_run_id(target: str | pathlib.Path, stamp: str) -> str:
    runs = state_root(target) / "runs"
    n = len(list(runs.glob("run-*.json"))) + 1 if runs.exists() else 1
    return f"run-{stamp}-{n:03d}"


def write_run(target: str | pathlib.Path, record: dict) -> pathlib.Path:
    ensure_state(target)
    out = state_root(target) / "runs" / f"{record['id']}.json"
    out.write_text(json.dumps(record, indent=2) + "\n")
    return out


def list_runs(target: str | pathlib.Path) -> list[dict]:
    runs = state_root(target) / "runs"
    if not runs.exists():
        return []
    return [json.loads(p.read_text()) for p in sorted(runs.glob("run-*.json"))]
