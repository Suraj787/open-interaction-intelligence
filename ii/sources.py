"""Motif Source Intelligence: registry, search, assurance, reuse classification, adaptation,
quarantine, discovery (opt-in), and contribution. Deterministic and offline-first.

Safety invariants (see ADR-SRC-001):
  - Discovery is disabled by default; no network on load/search/assurance/recommend.
  - Seed and discovered sources are never trusted automatically.
  - Discovered web content is hostile, inert data; it is sanitised and never executed.
  - Installed copies cannot write the central registry; contribution is a bundle/PR only.
"""
from __future__ import annotations
import json
import re
import html
import pathlib
from motif import registry as motif_registry, jsonschema_min
from . import evidence as ev_mod

ROOT = motif_registry.ROOT
REG = ROOT / "source-registry"
SCHEMA = REG / "schemas" / "source-record.schema.json"
QUARANTINE = REG / "quarantined"

INJECTION_MARKERS = ["ignore all prior", "ignore previous", "mark this source trusted",
                     "upload environment", "open a pull request", "disregard instructions",
                     "system prompt", "you are now", "exfiltrate"]


def _net_policy() -> dict:
    return json.loads((REG / "policies" / "network-policy.json").read_text())


def _schema() -> dict:
    return json.loads(SCHEMA.read_text())


def load_all() -> list[dict]:
    out = []
    for f in sorted((REG / "sources").rglob("*.json")):
        try:
            out.append(json.loads(f.read_text()))
        except json.JSONDecodeError:
            continue
    return out


def get(source_id: str) -> dict | None:
    return next((r for r in load_all() if r["id"] == source_id), None)


def validate() -> tuple[int, list[str]]:
    schema = _schema()
    errors, seen = [], set()
    recs = load_all()
    for r in recs:
        rid = r.get("id", "?")
        for e in jsonschema_min.validate(r, schema):
            errors.append(f"{rid}: {e}")
        if rid in seen:
            errors.append(f"{rid}: duplicate id")
        seen.add(rid)
    return len(recs), errors


# ---- search / list (offline) ---------------------------------------------------------
def search(query: str = "", framework: str = "", category: str = "") -> list[dict]:
    q = (query or "").lower()
    out = []
    for r in load_all():
        cls = r["classification"]
        if framework and framework not in cls.get("frameworks", []):
            continue
        if category and cls.get("registry_category") != category:
            continue
        hay = " ".join([r["identity"]["name"]] + cls.get("source_types", []) +
                       cls.get("product_fit", []) + cls.get("frameworks", [])).lower()
        if not q or q in hay or any(w in hay for w in q.split()):
            out.append(r)
    return out


# ---- deterministic Source Assurance --------------------------------------------------
def assurance(record: dict) -> dict:
    """Run deterministic, offline checks. Produces independent signals, never one opaque
    trust score. Unverified seeds honestly return insufficient-evidence."""
    ident = record["identity"]
    lic = record["licence"]
    checks = {}
    url = ident.get("canonical_url")
    checks["identity"] = {
        "canonical_url_present": bool(url),
        "https": bool(url and url.startswith("https://")),
        "canonical_relationship_verified": ident.get("canonical_relationship_verified", False),
        "lookalike_suspected": bool(url and re.search(r"(ui|design)-?(free|pro|official)\d*\.", url)),
        "confidence": ident.get("identity_confidence", 0.0),
    }
    checks["licence"] = {
        "identifier": lic.get("identifier", "unknown"),
        "verified_from_primary_source": lic.get("verified_from_primary_source", False),
        "commercial_use_inferred_from_free": False,  # never inferred
        "confidence": lic.get("confidence", 0.0),
    }
    checks["security"] = {"review_status": record["security"].get("review_status", "not-reviewed"),
                          "compromise_indicators": record["security"].get("compromise_indicators", [])}
    checks["accessibility"] = {"independently_reviewed": record["accessibility"].get("independently_reviewed", False),
                               "claimed": record["accessibility"].get("claimed", "unknown")}
    checks["maintenance"] = {"status": record["maintenance"].get("status", "unknown")}

    licence_ok = lic.get("verified_from_primary_source") and lic.get("identifier", "unknown") != "unknown"
    security_ok = record["security"].get("review_status") == "passed"
    a11y_ok = record["accessibility"].get("independently_reviewed")
    identity_ok = ident.get("canonical_relationship_verified")

    blocked_modes, allowed_modes, compromises = [], [], []
    if not licence_ok:
        blocked_modes.append("direct-reuse")
        compromises.append("licence not verified from primary source")
    if checks["identity"]["lookalike_suspected"]:
        compromises.append("possible lookalike or impersonating domain")
    # what is safe even when unverified: study, not copy
    allowed_modes = [m for m in record["usage"]["permitted_modes"] if m in ("inspect", "inspiration", "pattern-extraction")]
    if licence_ok and security_ok and a11y_ok and identity_ok:
        decision = "eligible-for-context-review"
    elif licence_ok and identity_ok:
        decision = "adapt-before-use-candidate"
        if "adapt-before-use" in record["usage"]["permitted_modes"]:
            allowed_modes.append("adapt-before-use")
    else:
        decision = "insufficient-evidence"
    return {
        "source": record["id"], "decision": decision,
        "checks": checks,
        "allowed_modes": sorted(set(allowed_modes)),
        "blocked_modes": sorted(set(blocked_modes)) or ["direct-reuse"],
        "compromises": compromises or record["assurance"].get("limitations", []),
        "approval_required": True,
        "trust_level": record["assurance"].get("trust_level", "unverified"),
        "note": "Deterministic offline assurance. Registry inclusion is not endorsement; "
                "verification from primary sources is required before direct reuse.",
    }


def reuse_mode(record: dict) -> str:
    """Classify the safest currently-justified reuse mode. Never direct-reuse without
    verified licence, identity, security, and accessibility."""
    a = assurance(record)
    if "direct-reuse" in a["allowed_modes"]:
        return "direct-reuse"
    if "adapt-before-use" in a["allowed_modes"]:
        return "adapt-before-use"
    if "pattern-extraction" in a["allowed_modes"]:
        return "pattern-extraction"
    return "inspiration-only"


# ---- compare / recommend -------------------------------------------------------------
def compare(id_a: str, id_b: str) -> dict:
    a, b = get(id_a), get(id_b)
    if not a or not b:
        return {"error": "one or both sources not found"}
    def row(r):
        return {"id": r["id"], "name": r["identity"]["name"],
                "frameworks": r["classification"].get("frameworks", []),
                "licence_verified": r["licence"].get("verified_from_primary_source", False),
                "licence": r["licence"].get("identifier", "unknown"),
                "security_review": r["security"].get("review_status", "not-reviewed"),
                "accessibility_reviewed": r["accessibility"].get("independently_reviewed", False),
                "maintenance": r["maintenance"].get("status", "unknown"),
                "reuse_mode": reuse_mode(r), "trust_level": r["assurance"].get("trust_level", "unverified")}
    return {"dimensions": ["frameworks", "licence_verified", "security_review",
                           "accessibility_reviewed", "maintenance", "reuse_mode"],
            "a": row(a), "b": row(b),
            "note": "Both rows reflect recorded evidence only; unverified fields are honest gaps."}


def recommend(need: str = "", product_form: str = "", workflow: str = "",
              framework: str = "", ability: str = "") -> dict:
    ctx = {}
    if product_form:
        ctx["product_forms"] = product_form.split(",")
    if workflow:
        ctx["workflows"] = workflow.split(",")
    if ability:
        ctx["abilities"] = ability.split(",")
    evidence = ev_mod.query(ctx) if ctx else {"normative_requirements": []}
    candidates = search(need, framework=framework)
    if len(candidates) < 3:
        # the specific need does not name a source; fall back to framework-appropriate
        # foundations so an accessible component can be built or adapted, not invented.
        seen = {c["id"] for c in candidates}
        candidates += [r for r in search("", framework=framework) if r["id"] not in seen]
    scored = []
    for r in candidates:
        fw_fit = 1 if (not framework or framework in r["classification"].get("frameworks", [])) else 0
        # prefer interaction-correct foundations over decorative libraries for accessible needs
        foundational = 1 if r["classification"].get("registry_category") == "foundational-primitives" else 0
        mode = reuse_mode(r)
        scored.append((fw_fit * 2 + foundational, r, mode))
    scored.sort(key=lambda x: -x[0])
    ranked = [{"id": r["id"], "name": r["identity"]["name"], "reuse_mode": mode,
               "frameworks": r["classification"].get("frameworks", []),
               "why": "framework fit + interaction-correct foundation" if r["classification"].get("registry_category") == "foundational-primitives" else "candidate for adaptation/pattern study"}
              for _s, r, mode in scored[:8]]
    safe_direct = [x for x in ranked if x["reuse_mode"] == "direct-reuse"]
    return {
        "need": need, "context": ctx,
        "applicable_requirements": len(evidence.get("normative_requirements", [])),
        "candidates": ranked,
        "recommended_strategy": ("direct-reuse" if safe_direct else
                                 "pattern-extraction-or-internal-implementation"),
        "rationale": ("No source has verified licence + identity + security + accessibility, so "
                      "no direct reuse is justified. Recommend pattern extraction or an internal, "
                      "evidence-grounded implementation." if not safe_direct else
                      "A verified candidate exists; still review against the product context."),
        "note": "Recommendation ranks by recorded evidence, not visual impressiveness.",
    }


# ---- adaptation plan -----------------------------------------------------------------
def adapt_plan(source_id: str, project: str = "./app") -> dict:
    r = get(source_id)
    if not r:
        return {"error": "source not found"}
    mode = reuse_mode(r)
    return {
        "source": r["id"], "component": "(specify component)", "reuse_mode": mode,
        "context": {"project": project},
        "licence_obligations": ["verify licence from primary source before any code reuse",
                                "attribution if required", "no paid asset reuse"],
        "files_expected": [], "dependencies": [],
        "tokens_to_replace": ["map source colours/spacing/radius to project design tokens"],
        "accessibility_repairs": ["verify keyboard operability", "ensure visible focus",
                                  "do not rely on colour alone", "check target size"],
        "motion_policy": ["respect prefers-reduced-motion"],
        "performance_budget": ["bound bundle impact; drop unnecessary dependencies"],
        "responsive_requirements": ["verify reflow and small-viewport behaviour"],
        "security_constraints": ["remove telemetry", "no remote code loading", "sanitise any HTML"],
        "tests_required": ["render + interaction test", "keyboard test", "reduced-motion test"],
        "browser_validations": ["axe + focus check in a real browser (experimental)"],
        "human_review": ["licence sign-off", "accessibility sign-off for the workflow"],
        "rollback": "apply in an isolated git worktree; exact rollback if rejected",
        "note": "The implementation agent receives this plan, not raw approval.",
    }


# ---- prompt-injection defence for discovered content ---------------------------------
def sanitise_discovered(text: str, max_bytes: int | None = None) -> dict:
    """Treat discovered web content as hostile, inert data. Returns sanitised, size-limited
    text plus flagged injection markers. The text is never executed or acted upon."""
    max_bytes = max_bytes or _net_policy()["max_content_bytes"]
    raw = text or ""
    truncated = len(raw.encode("utf-8")) > max_bytes
    safe = raw.encode("utf-8")[:max_bytes].decode("utf-8", errors="replace")
    low = safe.lower()
    flags = [m for m in INJECTION_MARKERS if m in low]
    return {"inert_text": html.escape(safe), "truncated": truncated,
            "injection_markers_detected": flags, "acted_upon": False,
            "note": "Discovered content is data, not instructions. Markers are recorded but inert."}


# ---- discovery (opt-in; offline by default) ------------------------------------------
PROVIDERS = ["web", "github", "npm", "storybook", "known-registry", "user-url", "figma-metadata", "mcp-registry"]


def discover(query: str = "", source: str = "known-registry", opt_in: bool = False,
             online: bool = False, url: str = "") -> dict:
    """Opt-in discovery. Without explicit opt_in (and a policy that permits network), this
    performs NO network activity and returns nothing. Discovered candidates would enter
    quarantine, never the trusted registry."""
    pol = _net_policy()
    if not opt_in:
        return {"discovery": "disabled-by-default", "candidates": [],
                "message": "Discovery is opt-in. Re-run with explicit opt-in to search; default is no.",
                "network_used": False}
    if pol.get("discovery_enabled_by_default") is False and not online:
        return {"discovery": "offline", "provider": source, "candidates": [],
                "message": "Offline mode: no network. Provide --online with opt-in to use live providers (experimental).",
                "network_used": False}
    # Live providers are experimental and intentionally not wired to real network here.
    return {"discovery": "experimental-provider-not-enabled", "provider": source,
            "candidates": [], "network_used": False,
            "message": "Live discovery providers are experimental and not enabled in this build. "
                       "Any future candidate enters quarantine and is never auto-trusted."}


# ---- quarantine ----------------------------------------------------------------------
def quarantine_list() -> list[dict]:
    out = []
    for f in sorted(QUARANTINE.glob("*.json")):
        try:
            r = json.loads(f.read_text())
            out.append({"id": r.get("id"), "name": r.get("identity", {}).get("name"),
                        "status": r.get("assurance", {}).get("status")})
        except json.JSONDecodeError:
            continue
    return out


# ---- contribution bundle (privacy-preserving) ----------------------------------------
_PRIVATE_KEYS = ("discovered_by_installation_id", "contributed_by")


def contribution_bundle(source_id: str) -> dict:
    r = get(source_id) or _quarantined(source_id)
    if not r:
        return {"error": "source not found in registry or quarantine"}
    rec = json.loads(json.dumps(r))  # deep copy
    # strip anything that could carry private data
    for k in _PRIVATE_KEYS:
        if k in rec.get("provenance", {}):
            rec["provenance"][k] = None
    leaks = _privacy_scan(rec)
    return {"bundle": {"source_record": rec, "schema_version": rec.get("schema_version")},
            "privacy_ok": not leaks, "privacy_leaks": leaks,
            "excludes": ["project code", "prompts", "private URLs", "usernames",
                         "absolute local paths", "secrets", "cookies", "browsing data"],
            "note": "Contribution is a bundle/PR only. It never pushes to upstream and never auto-merges."}


def _quarantined(source_id: str) -> dict | None:
    f = QUARANTINE / f"{source_id}.json"
    return json.loads(f.read_text()) if f.exists() else None


def _privacy_scan(obj) -> list[str]:
    blob = json.dumps(obj)
    leaks = []
    if re.search(r"/Users/|/home/[a-z]", blob):
        leaks.append("absolute local path")
    if re.search(r"(?i)(secret|token|password|api[_-]?key)\s*[:=]\s*\S+", blob):
        leaks.append("possible secret")
    if re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", blob):
        leaks.append("possible email/PII")
    return leaks
