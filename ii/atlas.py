"""Motif Atlas: a static, public catalogue generated from the validated registry.

Atlas is a product surface, not a second source of truth. It reads the same registry the
CLI/Studio/MCP use and emits a static site (index + per source/component/pattern pages +
a JSON index). Default output is .motif/atlas (gitignored); pass an --out for publishing.
"""
from __future__ import annotations
import html
import json
import pathlib
from motif import registry

CSS = """body{font:15px/1.5 system-ui,sans-serif;margin:0;color:#1a1a2e;background:#fafafc}
header{background:#11113a;color:#fff;padding:18px 28px}header a{color:#cdd}
main{max-width:1000px;margin:0 auto;padding:24px 28px}
.card{border:1px solid #e3e3ef;border-radius:10px;padding:14px 16px;margin:10px 0;background:#fff}
.tag{display:inline-block;font-size:12px;background:#eef;border-radius:6px;padding:1px 8px;margin:2px}
.muted{color:#667}a{color:#2a4ad6;text-decoration:none}a:hover{text-decoration:underline}
h1{margin:0}h2{border-bottom:1px solid #e3e3ef;padding-bottom:6px;margin-top:28px}
input{padding:8px 10px;border:1px solid #ccd;border-radius:8px;width:100%;margin:12px 0}"""


def _page(title: str, body: str, depth: int = 0) -> str:
    up = "../" * depth
    return (f"<!doctype html><html lang=en><head><meta charset=utf-8>"
            f"<meta name=viewport content='width=device-width,initial-scale=1'>"
            f"<title>{html.escape(title)} | Motif Atlas</title><style>{CSS}</style></head><body>"
            f"<header><a href='{up}index.html'><strong>Motif Atlas</strong></a> "
            f"<span class=muted>verified UI source catalogue</span></header><main>{body}"
            f"<p class=muted style='margin-top:40px'>Generated from the Motif registry. "
            f"Source metadata does not imply redistribution rights; see each record's licence.</p>"
            f"</main></body></html>")


def _esc(v) -> str:
    return html.escape(str(v))


def build(out: str | pathlib.Path | None = None) -> dict:
    out_dir = pathlib.Path(out) if out else (registry.ROOT / ".motif" / "atlas")
    for sub in ("sources", "components", "patterns"):
        (out_dir / sub).mkdir(parents=True, exist_ok=True)

    sources = [r.data for r in registry.load_records("sources")]
    components = [r.data for r in registry.load_records("components")]
    patterns = [r.data for r in registry.load_records("patterns")]

    counts = {"sources": len(sources), "components": len(components), "patterns": len(patterns)}

    # source pages
    for s in sources:
        comps = [c for c in components if c.get("source") == s["id"]]
        body = (f"<h1>{_esc(s['name'])}</h1>"
                f"<p class=muted>{_esc(s['category'])} · tier {s['trust_tier']} · "
                f"{_esc(s['redistribution'])} · {_esc(s['license'])}</p>"
                f"<p><a href='{_esc(s['homepage'])}'>homepage</a>"
                + (f" · <a href='{_esc(s['repository'])}'>repository</a>" if s.get('repository') else "")
                + f"</p><div class=card><strong>Strengths</strong><br>"
                + "<br>".join(_esc(x) for x in s.get('strengths', []) or ['n/a'])
                + "</div><div class=card><strong>Weaknesses</strong><br>"
                + "<br>".join(_esc(x) for x in s.get('weaknesses', []) or ['n/a'])
                + f"</div><p>confidence: {_esc(s['confidence'])} · status: {_esc(s['status'])} · "
                f"last reviewed: {_esc(s['last_reviewed'])}</p>"
                f"<h2>Components ({len(comps)})</h2>"
                + "".join(f"<div class=card><a href='../components/{_esc(c['id'])}.html'>{_esc(c['name'])}</a> "
                          f"<span class=tag>{_esc(c['usability_mode'])}</span></div>" for c in comps))
        (out_dir / "sources" / f"{s['id']}.html").write_text(_page(s["name"], body, 1))

    for c in components:
        body = (f"<h1>{_esc(c['name'])}</h1>"
                f"<p class=muted>source <a href='../sources/{_esc(c['source'])}.html'>{_esc(c['source'])}</a> · "
                f"{_esc(c['framework'])} · {_esc(c['license'])}</p>"
                f"<p><span class=tag>{_esc(c['usability_mode'])}</span>"
                f"<span class=tag>a11y: {_esc(c.get('accessibility_status'))}</span>"
                f"<span class=tag>reduced-motion: {_esc(c.get('reduced_motion_support'))}</span>"
                f"<span class=tag>perf: {_esc(c.get('performance_cost'))}</span></p>"
                + (f"<div class=card>{_esc(c.get('component_exceptions'))}</div>" if c.get('component_exceptions') else ""))
        (out_dir / "components" / f"{c['id']}.html").write_text(_page(c["name"], body, 1))

    for p in patterns:
        body = (f"<h1>{_esc(p['name'])}</h1><p class=muted>{_esc(p['problem'])}</p>"
                f"<div class=card><strong>Recommended effects</strong><br>"
                + ", ".join(_esc(x) for x in p.get('recommended_effects', []) or ['n/a'])
                + "</div><div class=card><strong>Rejected effects</strong><br>"
                + ", ".join(_esc(x) for x in p.get('rejected_effects', []) or ['n/a'])
                + "</div><div class=card><strong>Accessibility requirements</strong><br>"
                + "<br>".join(_esc(x) for x in p.get('accessibility_requirements', []))
                + "</div>")
        (out_dir / "patterns" / f"{p['id']}.html").write_text(_page(p["name"], body, 1))

    # index with client-side filter
    def _list(items, sub, label):
        return "".join(
            f"<div class=card data-name='{_esc(i.get('name','')).lower()}'>"
            f"<a href='{sub}/{_esc(i['id'])}.html'>{_esc(i.get('name', i['id']))}</a> "
            f"<span class=tag>{_esc(i.get('category') or i.get('usability_mode') or label)}</span></div>"
            for i in items)
    index_body = (
        f"<h1>Motif Atlas</h1><p class=muted>{counts['sources']} sources · "
        f"{counts['components']} components · {counts['patterns']} patterns, all from the validated registry.</p>"
        "<input id=q placeholder='filter by name...' oninput=\"f()\">"
        f"<h2>Sources</h2><div id=sources>{_list(sources,'sources','source')}</div>"
        f"<h2>Components</h2><div id=components>{_list(components,'components','component')}</div>"
        f"<h2>Patterns</h2><div id=patterns>{_list(patterns,'patterns','pattern')}</div>"
        "<script>function f(){var v=document.getElementById('q').value.toLowerCase();"
        "document.querySelectorAll('.card[data-name]').forEach(function(c){"
        "c.style.display=c.getAttribute('data-name').indexOf(v)>-1?'':'none'})}</script>")
    (out_dir / "index.html").write_text(_page("Home", index_body))

    index_json = {"counts": counts,
                  "sources": [{"id": s["id"], "name": s["name"], "category": s["category"],
                               "redistribution": s["redistribution"], "trust_tier": s["trust_tier"]} for s in sources],
                  "components": [{"id": c["id"], "name": c["name"], "usability_mode": c["usability_mode"]} for c in components],
                  "patterns": [{"id": p["id"], "name": p["name"]} for p in patterns]}
    (out_dir / "index.json").write_text(json.dumps(index_json, indent=2) + "\n")

    pages = counts["sources"] + counts["components"] + counts["patterns"] + 1
    return {"out": str(out_dir), "pages": pages, "counts": counts}
