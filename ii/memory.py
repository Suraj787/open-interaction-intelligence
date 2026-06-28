"""Scoped, auditable project memory.

Records facts, decisions, preferences, rejected approaches, and temporary assumptions
so future agents do not repeat rejected suggestions. Each memory carries source, scope,
date, confidence, author, and an expiry or invalidation rule.
"""
from __future__ import annotations
import json
import pathlib
from . import runtime

VALID_TYPES = ["factual", "decision", "preference", "rejected-approach", "temporary-assumption"]


def _dir(target):
    return runtime.state_root(target) / "memory"


def load(target) -> list[dict]:
    d = _dir(target)
    if not d.exists():
        return []
    return [json.loads(p.read_text()) for p in sorted(d.glob("*.json"))]


def add(target, mid: str, mtype: str, content: str, date: str, *, source="user",
        scope="project", confidence=0.8, author="user", expiry=None) -> tuple[bool, str]:
    if mtype not in VALID_TYPES:
        return False, f"type must be one of {VALID_TYPES}"
    runtime.ensure_state(target)
    rec = {"id": mid, "type": mtype, "content": content, "date": date,
           "source": source, "scope": scope, "confidence": confidence,
           "author": author, "status": "active"}
    if expiry:
        rec["expiry"] = expiry
    (_dir(target) / f"{mid}.json").write_text(json.dumps(rec, indent=2) + "\n")
    return True, str(_dir(target) / f"{mid}.json")


def invalidate(target, mid: str) -> bool:
    p = _dir(target) / f"{mid}.json"
    if not p.exists():
        return False
    d = json.loads(p.read_text())
    d["status"] = "invalidated"
    p.write_text(json.dumps(d, indent=2) + "\n")
    return True


def rejected_approaches(target) -> list[dict]:
    return [m for m in load(target) if m["type"] == "rejected-approach" and m.get("status") == "active"]
