"""Motif static scanners. Pure-stdlib, read-only, never execute scanned code.

Each scanner returns a list of Finding objects. Findings are advisory: not every
match is malicious, but every match must be reviewed before a source is approved.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict


@dataclass
class Finding:
    scanner: str
    severity: str   # info | warn | high | critical
    code: str
    message: str
    path: str = ""
    line: int = 0

    def to_dict(self) -> dict:
        return asdict(self)


SEVERITY_ORDER = {"info": 0, "warn": 1, "high": 2, "critical": 3}


def worst(findings: list["Finding"]) -> str:
    if not findings:
        return "none"
    return max(findings, key=lambda f: SEVERITY_ORDER[f.severity]).severity
