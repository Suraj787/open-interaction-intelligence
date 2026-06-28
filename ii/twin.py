"""Visual Twin (static).

A persistent machine-readable representation of a project. The static layers (routes,
screens, component fingerprints, design tokens via design-system extraction) are built
deterministically from source. The rendered layers (screenshots, accessibility tree,
computed styles, traces, baseline performance) require a browser runtime (Playwright)
and are marked not-rendered here, never fabricated.
"""
from __future__ import annotations
import json
import hashlib
import pathlib
from . import runtime, system as system_mod


def _fingerprint(path: pathlib.Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()[:12]
    except OSError:
        return ""


def build(target, stamp: str) -> dict:
    root = pathlib.Path(target)
    pm = runtime.model_project(target)
    comp_files = [f for f in root.rglob("*.vue") if "node_modules" not in f.parts] + \
                 [f for f in root.rglob("*.tsx") if "node_modules" not in f.parts]
    components = [{"name": f.stem, "file": str(f.relative_to(root)),
                   "fingerprint": _fingerprint(f)} for f in sorted(comp_files)]
    ds = system_mod.extract(target)
    manifest = {
        "project": root.name, "generated": stamp, "framework": pm.framework,
        "routes": pm.routes,
        "screens": [{"route": r, "rendered": False} for r in pm.routes],
        "components": components,
        "viewport_variants": ["desktop", "tablet", "mobile"],
        "rendered": False,
        "tokens": {"variables": len(ds["css_variables"]), "tailwind": ds["tailwind"]},
        "notes": ["Static twin. Screenshots, accessibility tree, computed styles, traces "
                  "and baseline performance require a browser runtime (Playwright) and are "
                  "not rendered in this build."],
    }
    return manifest


def write(target, manifest: dict) -> pathlib.Path:
    d = runtime.state_root(target) / "twin"
    d.mkdir(parents=True, exist_ok=True)
    out = d / "manifest.json"
    out.write_text(json.dumps(manifest, indent=2) + "\n")
    return out


def load(target) -> dict | None:
    p = runtime.state_root(target) / "twin" / "manifest.json"
    return json.loads(p.read_text()) if p.exists() else None
