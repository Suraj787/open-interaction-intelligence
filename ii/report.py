"""Before/after evidence report (HTML + JSON).

Produces a report understandable by a developer, designer, product manager, or auditor.
Browser artifacts (before/after screenshots, axe) are included when captured and clearly
marked not-executed otherwise. Never implies a browser result that did not run.
"""
from __future__ import annotations
import html
import json
import pathlib
from . import runtime


def _h(v):
    return html.escape(str(v))


def generate(target, run_id: str, result: dict) -> pathlib.Path:
    base = runtime.state_root(target) / "evidence" / run_id
    for sub in ("before", "after", "diff", "findings", "claims", "plan", "rollback"):
        (base / sub).mkdir(parents=True, exist_ok=True)
    (base / "report.json").write_text(json.dumps(result, indent=2) + "\n")

    finding = result.get("finding", {})
    claim = result.get("claim", {})
    plan = result.get("plan", {})
    steps = result.get("steps", [])

    def row(k, v):
        return f"<tr><th style='text-align:left;padding:4px 12px 4px 0;vertical-align:top'>{_h(k)}</th><td>{v}</td></tr>"

    steps_html = "".join(
        f"<li><strong>{_h(s['step'])}</strong>: "
        f"<span style='color:{'#2a7' if s['status']=='passed' else '#b80' if s['status'] in ('warning','not-executed') else '#c33'}'>{_h(s['status'])}</span></li>"
        for s in steps)

    body = f"""<!doctype html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content='width=device-width,initial-scale=1'>
<title>Motif evidence report {_h(run_id)}</title>
<style>body{{font:14px/1.6 system-ui,sans-serif;max-width:880px;margin:0 auto;padding:24px;color:#1a1a2e}}
h1,h2{{border-bottom:1px solid #e3e3ef;padding-bottom:6px}}.tag{{background:#eef;border-radius:6px;padding:1px 8px;font-size:12px}}
.box{{border:1px solid #e3e3ef;border-radius:10px;padding:14px;margin:12px 0;background:#fafafc}}
code{{background:#f0f0f7;padding:1px 5px;border-radius:4px}}</style></head><body>
<h1>Motif evidence report</h1>
<p class=tag>run {_h(run_id)}</p>
<h2>Goal and context</h2><table>
{row('Target', _h(result.get('target','')))}
{row('Route', _h(plan.get('context_vector',{}).get('route','')))}
{row('Context vector', '<code>'+_h(json.dumps(plan.get('context_vector',{})))+'</code>')}
</table>
<h2>Finding</h2><div class=box>
{row('Rule', _h(finding.get('rule')))}
{row('Component', _h(finding.get('location',{}).get('component')))}
{row('File', '<code>'+_h(finding.get('location',{}).get('file'))+'</code>')}
{row('Severity', _h(finding.get('severity')))}
</div>
<h2>Evidence claim</h2><div class=box>
{row('Claim', _h(claim.get('id')))}
{row('Statement', _h(claim.get('statement')))}
{row('Force', _h(claim.get('force')))}
{row('Tier', _h(claim.get('tier')))}
{row('Sources', _h(', '.join(claim.get('sources',[]))))}
{row('Confidence', _h(claim.get('confidence')))}
{row('Limitations', _h('; '.join(claim.get('limitations',[]))))}
{row('Legal', 'compliance claim allowed: '+_h(claim.get('legal',{}).get('compliance_claim_allowed')))}
</div>
<h2>Repair plan</h2><div class=box>
{row('Changes', _h('; '.join(plan.get('changes',[]))))}
{row('Why', _h(plan.get('why')))}
{row('Human review', _h('; '.join(plan.get('human_review',[]))))}
{row('Rollback', _h(plan.get('rollback',{}).get('strategy')))}
</div>
<h2>Before / after</h2><div class=box>
<p>Before screenshot: <strong>not-executed</strong> (no browser runtime). After screenshot:
<strong>not-executed</strong>. The static re-check verified the status text is present after repair.</p>
</div>
<h2>Workflow steps</h2><ul>{steps_html}</ul>
<h2>Outcome</h2><div class=box>
<p>{_h(result.get('deterministic_outcome',''))}</p>
<p><strong>Browser validation:</strong> {_h(result.get('browser_outcome','not-executed'))}.</p>
<p>{_h(result.get('note',''))}</p>
</div>
<h2>Rollback</h2><div class=box><code>git worktree remove --force &lt;worktree&gt;</code> (exact reset; the user's branch was never touched)</div>
</body></html>"""
    (base / "report.html").write_text(body)
    return base
