"""Dangerous-pattern static scanner for JS/TS source in quarantine.

Mirrors security/dangerous-patterns.yml. Detects dynamic code execution, remote
code loading, shell/child-process use, obfuscation and crypto-mining markers.
Read-only: the file is never executed.
"""
from __future__ import annotations
import re
import pathlib
from . import Finding

# (code, severity, regex, human message)
PATTERNS: list[tuple[str, str, str, str]] = [
    ("eval", "critical", r"\beval\s*\(", "Use of eval(), dynamic code execution"),
    ("new-function", "critical", r"\bnew\s+Function\s*\(", "new Function(), dynamic code execution"),
    ("settimeout-string", "high", r"set(?:Timeout|Interval)\s*\(\s*['\"]", "Timer called with a string body (implicit eval)"),
    ("child-process", "critical", r"require\(\s*['\"]child_process['\"]\s*\)|child_process", "child_process / shell execution"),
    ("node-exec", "critical", r"\bexecSync?\s*\(|\bspawnSync?\s*\(", "Process execution (exec/spawn)"),
    ("remote-script", "high", r"document\.createElement\(\s*['\"]script['\"]\s*\)", "Dynamic remote <script> injection"),
    ("import-remote", "high", r"import\s*\(\s*[`'\"]https?://", "Dynamic import() of a remote URL"),
    ("fetch-undocumented", "warn", r"\bfetch\s*\(|XMLHttpRequest|new\s+WebSocket\b", "Network call (fetch/XHR/WebSocket), verify it is documented"),
    ("inner-html", "warn", r"\.innerHTML\s*=", "Unsafe HTML insertion via innerHTML"),
    ("document-write", "high", r"document\.write\s*\(", "document.write, can inject arbitrary markup"),
    ("iframe-inject", "warn", r"createElement\(\s*['\"]iframe['\"]\s*\)", "Dynamic iframe injection"),
    ("obfuscation-hex", "high", r"(?:\\x[0-9a-fA-F]{2}){6,}", "Long hex escape run, possible obfuscation"),
    ("obfuscation-fromcharcode", "warn", r"String\.fromCharCode\s*\(", "String.fromCharCode, possible obfuscation"),
    ("atob", "warn", r"\batob\s*\(", "atob() base64 decode, verify decoded content"),
    ("crypto-mining", "critical", r"coinhive|cryptonight|CoinImp|miner\.start", "Crypto-mining marker"),
]

_COMPILED = [(c, s, re.compile(p), m) for c, s, p, m in PATTERNS]
_SOURCE_EXT = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".svelte", ".html"}


def scan_text(text: str, path: str = "") -> list[Finding]:
    findings: list[Finding] = []
    lines = text.splitlines()
    for i, line in enumerate(lines, 1):
        for code, sev, rx, msg in _COMPILED:
            if rx.search(line):
                findings.append(Finding("source_scanner", sev, code, msg, path, i))
    return findings


def scan_path(target: str | pathlib.Path) -> list[Finding]:
    p = pathlib.Path(target)
    findings: list[Finding] = []
    files = [p] if p.is_file() else [f for f in p.rglob("*") if f.is_file()]
    for f in files:
        if f.suffix.lower() not in _SOURCE_EXT:
            continue
        try:
            findings.extend(scan_text(f.read_text(errors="replace"), str(f)))
        except OSError:
            continue
    return findings
