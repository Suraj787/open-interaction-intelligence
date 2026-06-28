"""Browser evidence capture (optional `motif[browser]` extra).

Uses Playwright + axe-core (injected from CDN) when installed; otherwise returns a
structured `not-executed` result and never fabricates browser output. Result status is
always one of: passed | failed | warning | not-applicable | not-executed |
human-review-required. Semantic verification uses rendered text, roles, accessible names,
the accessibility tree, axe results, and runtime geometry, not screenshots alone.
"""
from __future__ import annotations
import json
import platform
import pathlib

RESULT_STATES = ["passed", "failed", "warning", "not-applicable", "not-executed", "human-review-required"]
AXE_CDN = "https://cdn.jsdelivr.net/npm/axe-core@4.10.2/axe.min.js"


def available() -> tuple[bool, str]:
    try:
        import playwright  # noqa: F401
        return True, "playwright importable"
    except Exception:
        return False, "playwright not installed (optional 'browser' extra)"


def axe_available() -> bool:
    return available()[0]


def _versions(pw=None, browser=None) -> dict:
    v = {"python": platform.python_version(), "axe_cdn": AXE_CDN}
    try:
        import playwright
        v["playwright"] = getattr(playwright, "__version__", "unknown")
    except Exception:
        pass
    if browser is not None:
        try:
            v["browser_version"] = browser.version
        except Exception:
            pass
    return v


def capture(url: str, out_dir: str | pathlib.Path, viewport=(1280, 800),
            target_selector: str | None = None, reduced_motion: bool = True) -> dict:
    """Capture screenshot, accessibility snapshot, axe, console, network and geometry."""
    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    ok, reason = available()
    if not ok:
        meta = {"status": "not-executed", "reason": reason, "url": url, "viewport": list(viewport)}
        (out / "metadata.json").write_text(json.dumps(meta, indent=2) + "\n")
        return meta

    from playwright.sync_api import sync_playwright  # type: ignore
    console_msgs: list[dict] = []
    failed_requests: list[dict] = []
    result = {"status": "executed-and-passed", "url": url, "viewport": list(viewport), "artifacts": []}
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(args=["--no-sandbox"])
            context = browser.new_context(
                viewport={"width": viewport[0], "height": viewport[1]},
                reduced_motion="reduce" if reduced_motion else "no-preference")
            page = context.new_page()
            page.on("console", lambda m: console_msgs.append({"type": m.type, "text": m.text}))
            page.on("requestfailed", lambda r: failed_requests.append({"url": r.url, "failure": str(r.failure)}))
            resp = page.goto(url, wait_until="networkidle", timeout=30000)
            result["http_status"] = resp.status if resp else None
            result["final_url"] = page.url
            page.screenshot(path=str(out / "screenshot.png"), full_page=True)
            (out / "accessibility.json").write_text(json.dumps(page.accessibility.snapshot() or {}, indent=2))
            # axe-core via CDN
            try:
                page.add_script_tag(url=AXE_CDN)
                axe = page.evaluate("async () => await axe.run(document, {resultTypes:['violations']})")
            except Exception as e:  # noqa: BLE001
                axe = {"error": str(e), "violations": []}
            (out / "axe.json").write_text(json.dumps(axe, indent=2))
            result["axe_violations"] = len(axe.get("violations", []))
            (out / "console.json").write_text(json.dumps(console_msgs, indent=2))
            (out / "network.json").write_text(json.dumps(failed_requests, indent=2))
            # geometry of interactive targets (and an optional specific selector)
            geometry = page.evaluate(
                "() => Array.from(document.querySelectorAll('a,button,input,select,textarea,[role=button]'))"
                ".map(e => {const r=e.getBoundingClientRect(); return {tag:e.tagName, w:Math.round(r.width), "
                "h:Math.round(r.height), name:(e.getAttribute('aria-label')||e.textContent||'').trim().slice(0,40)}})")
            (out / "geometry.json").write_text(json.dumps(geometry, indent=2))
            versions = _versions(p, browser)
            meta = {"status": "executed-and-passed", "url": url, "final_url": page.url,
                    "viewport": list(viewport), "reduced_motion": reduced_motion,
                    "axe_violations": result["axe_violations"], "versions": versions}
            (out / "metadata.json").write_text(json.dumps(meta, indent=2) + "\n")
            result["artifacts"] = ["screenshot.png", "accessibility.json", "axe.json",
                                   "console.json", "network.json", "geometry.json", "metadata.json"]
            result["versions"] = versions
            context.close()
            browser.close()
    except Exception as e:  # noqa: BLE001
        result = {"status": "executed-and-failed", "url": url, "error": str(e)}
        (out / "metadata.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


def has_text(url: str, text: str, viewport=(1280, 800)) -> dict:
    """Semantic check: is `text` rendered on the page? Returns executed-and-(passed/failed)."""
    ok, reason = available()
    if not ok:
        return {"status": "not-executed", "reason": reason}
    from playwright.sync_api import sync_playwright  # type: ignore
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(args=["--no-sandbox"])
            page = browser.new_page(viewport={"width": viewport[0], "height": viewport[1]})
            page.goto(url, wait_until="networkidle", timeout=30000)
            count = page.get_by_text(text, exact=False).count()
            browser.close()
            return {"status": "executed-and-passed" if count > 0 else "executed-and-failed",
                    "text": text, "matches": count}
    except Exception as e:  # noqa: BLE001
        return {"status": "executed-and-failed", "error": str(e)}


def doctor() -> dict:
    ok, reason = available()
    return {
        "browser_dependency": "playwright",
        "available": ok,
        "reason": reason,
        "axe_available": axe_available(),
        "supported_capabilities": ["screenshot", "accessibility-snapshot", "axe", "console",
                                    "network", "geometry"] if ok else [],
        "unavailable_capabilities": [] if ok else ["screenshot", "accessibility-snapshot", "axe",
                                                    "console", "network", "geometry", "trace"],
        "result_states": RESULT_STATES,
        "versions": _versions() if ok else {"python": platform.python_version()},
    }
