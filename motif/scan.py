"""Aggregate scan over a quarantine path using all five scanners."""
from __future__ import annotations
import pathlib
from scanners import (
    Finding, worst, source_scanner, behaviour_scanner,
    dependency_scanner, license_scanner, secret_scanner,
)


def scan_all(target: str | pathlib.Path) -> list[Finding]:
    findings: list[Finding] = []
    findings += source_scanner.scan_path(target)
    findings += behaviour_scanner.scan_path(target)
    findings += dependency_scanner.scan_path(target)
    findings += license_scanner.scan_path(target)
    findings += secret_scanner.scan_path(target)
    return findings


def verdict(findings: list[Finding]) -> str:
    w = worst(findings)
    if w in ("critical", "high"):
        return "reject"
    if w == "warn":
        return "review"
    return "pass"
