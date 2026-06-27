"""Dependency inspection for a package.json in quarantine.

Flags lifecycle install scripts (the classic supply-chain RCE vector),
typosquat look-alikes of popular packages, and unexpected dependency growth.
Read-only, never runs `npm install`.
"""
from __future__ import annotations
import json
import pathlib
from . import Finding

LIFECYCLE = ("preinstall", "install", "postinstall", "preuninstall", "postuninstall", "prepare")

# A small popular-package set for a Levenshtein-1 typosquat heuristic.
POPULAR = {
    "react", "react-dom", "vue", "svelte", "lodash", "axios", "motion",
    "framer-motion", "gsap", "three", "tailwindcss", "next", "express",
    "chalk", "commander", "webpack", "vite", "@types/node",
}


def _lev1(a: str, b: str) -> bool:
    if a == b:
        return False
    if abs(len(a) - len(b)) > 1:
        return False
    # classic DP edit distance, early-exit at 2
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1] == 1


def scan_package_json(text: str, path: str = "package.json") -> list[Finding]:
    out: list[Finding] = []
    try:
        pkg = json.loads(text)
    except json.JSONDecodeError as e:
        return [Finding("dependency_scanner", "warn", "parse-error", f"Invalid package.json: {e}", path)]

    scripts = pkg.get("scripts", {}) or {}
    for hook in LIFECYCLE:
        if hook in scripts:
            out.append(Finding("dependency_scanner", "critical", "lifecycle-script",
                               f"Lifecycle script '{hook}': {scripts[hook]!r} runs on install", path))

    all_deps: dict[str, str] = {}
    for field in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        all_deps.update(pkg.get(field, {}) or {})

    for name in all_deps:
        bare = name.split("/")[-1]
        for pop in POPULAR:
            if _lev1(bare, pop.split("/")[-1]):
                out.append(Finding("dependency_scanner", "high", "typosquat",
                                   f"Dependency '{name}' looks like a typosquat of '{pop}'", path))
                break

    if len(all_deps) > 15:
        out.append(Finding("dependency_scanner", "warn", "dependency-growth",
                           f"{len(all_deps)} dependencies for an effect, review necessity", path))
    if not out:
        out.append(Finding("dependency_scanner", "info", "clean",
                           f"{len(all_deps)} deps, no lifecycle scripts detected", path))
    return out


def scan_path(target: str | pathlib.Path) -> list[Finding]:
    p = pathlib.Path(target)
    out: list[Finding] = []
    files = [p] if p.is_file() else list(p.rglob("package.json"))
    for f in files:
        try:
            out.extend(scan_package_json(f.read_text(errors="replace"), str(f)))
        except OSError:
            continue
    return out
