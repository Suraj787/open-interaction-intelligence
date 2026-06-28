"""Motif Studio (local-first).

Generates a static local dashboard from the same source of truth the CLI uses (the
project's .motif/ state plus the registry) and serves it over the stdlib HTTP server.
It does not duplicate business logic; it renders what the engines produced. Interactive
apply/rollback from the UI is experimental (needs the runtime); the viewer is read-only.
"""
from __future__ import annotations
import html
import json
import pathlib
import functools
import http.server
import socketserver
from . import runtime, findings as findings_mod, twin as twin_mod

CSS = """body{font:14px/1.5 system-ui,sans-serif;margin:0;background:#0e0e23;color:#e9e9f5}
header{padding:14px 22px;background:#16163a;font-weight:600}
.grid{display:grid;grid-template-columns:240px 1fr 300px;gap:1px;background:#222;min-height:90vh}
.col{background:#13132e;padding:16px;overflow:auto}
.b{font-size:11px;text-transform:uppercase;color:#8a8ac0;margin:14px 0 6px}
.item{padding:6px 8px;border-radius:6px;margin:2px 0;background:#1b1b3d}
.sev-high{border-left:3px solid #ff5d6c}.sev-medium{border-left:3px solid #ffb454}
.sev-low{border-left:3px solid #6ad}.muted{color:#9898c8}"""


def _h(v):
    return html.escape(str(v))


def build(target) -> pathlib.Path:
    root = pathlib.Path(target)
    runtime.ensure_state(target)
    model_p = runtime.state_root(target) / "project" / "model.json"
    model = json.loads(model_p.read_text()) if model_p.exists() else {}
    fnd = findings_mod.load(target)
    tw = twin_mod.load(target) or {}

    left = "<div class=b>Routes</div>" + "".join(
        f"<div class=item>{_h(r)}</div>" for r in model.get("routes", []) or ["(none)"])
    left += "<div class=b>Components</div>" + "".join(
        f"<div class=item>{_h(c)}</div>" for c in (model.get("components", []) or [])[:30])

    centre = (f"<div class=b>Project</div><div class=item>{_h(model.get('framework','?'))} · "
              f"{len(model.get('routes', []))} routes · {len(model.get('components', []))} components</div>"
              f"<div class=b>Visual Twin</div><div class=item>"
              f"rendered: {tw.get('rendered', False)} (static twin; screenshots need a browser runtime)</div>"
              f"<div class=b>Before / after</div><div class=item muted>"
              f"Visual canvas + interaction replay are experimental (require the runtime).</div>")

    summary = findings_mod.summarize(fnd)
    right = (f"<div class=b>Findings ({summary['total']})</div>"
             + "".join(f"<div class='item sev-{_h(f['severity'])}'>"
                       f"<strong>{_h(f['rule'])}</strong><br>"
                       f"<span class=muted>{_h(f['location'].get('file') or f['location'].get('component',''))}</span>"
                       f"</div>" for f in fnd[:40])
             + (f"<div class=item muted>by severity: {_h(summary['by_severity'])}</div>" if fnd else
                "<div class=item muted>run `motif init` or `motif improve` to populate findings</div>"))

    page = (f"<!doctype html><html lang=en><head><meta charset=utf-8>"
            f"<meta name=viewport content='width=device-width,initial-scale=1'>"
            f"<title>Motif Studio</title><style>{CSS}</style></head><body>"
            f"<header>Motif Studio <span class=muted>local · read-only · same registry as CLI/MCP</span></header>"
            f"<div class=grid><div class=col>{left}</div><div class=col>{centre}</div>"
            f"<div class=col>{right}</div></div></body></html>")

    out = runtime.state_root(target) / "studio"
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(page)
    return out / "index.html"


def serve(target, port: int = 7777) -> int:
    out = build(target).parent
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(out))
    with socketserver.TCPServer(("127.0.0.1", port), handler) as httpd:
        print(f"Motif Studio: http://127.0.0.1:{port}  (Ctrl-C to stop)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
    return 0
