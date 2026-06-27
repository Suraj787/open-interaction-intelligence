"""Environment + registry health checks. Never prints secrets."""
from __future__ import annotations
import shutil
import pathlib
from . import registry, yaml_min

ROOT = registry.ROOT


def _tool(name: str) -> tuple[bool, str]:
    path = shutil.which(name)
    return (bool(path), path or "missing")


def run() -> tuple[list[str], bool]:
    lines: list[str] = []
    ok = True

    lines.append("# Motif doctor")
    lines.append("")
    lines.append("## Tooling")
    for t in ("git", "python3", "node", "npm", "gh", "make"):
        present, where = _tool(t)
        lines.append(f"  [{'ok ' if present else 'WARN'}] {t}: {where}")

    lines.append("")
    lines.append("## Runtime mode")
    pol_path = ROOT / "security" / "domain-policy.yml"
    try:
        pol = yaml_min.load(pol_path.read_text())
        mode = pol.get("mode", "unknown")
        allow = pol.get("allowlist", []) or []
        lines.append(f"  default mode: {mode}")
        lines.append(f"  domain allowlist entries: {len(allow)}")
    except Exception as e:  # noqa: BLE001
        ok = False
        lines.append(f"  [FAIL] could not load domain-policy.yml: {e}")

    lines.append("")
    lines.append("## Quarantine layout")
    for d in ("quarantine", "reviewed", "approved", "rejected"):
        p = ROOT / ".motif" / d
        lines.append(f"  [{'ok ' if p.exists() else 'WARN'}] .motif/{d}")

    lines.append("")
    lines.append("## Registry")
    res = registry.validate_all()
    for kind, n in res.counts.items():
        lines.append(f"  {kind}: {n} record(s)")
    if res.ok:
        lines.append("  [ok ] registry validates against schemas")
    else:
        ok = False
        lines.append(f"  [FAIL] {len(res.errors)} validation error(s), run `motif validate`")

    return lines, ok
