"""Embedded-secret detector.

Catches credentials that must never ship inside a retrieved component, and is
also run before release against the repo itself. Read-only.
"""
from __future__ import annotations
import re
import pathlib
from . import Finding

SECRETS: list[tuple[str, str, str, str]] = [
    ("private-key", "critical", r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----", "Embedded private key"),
    ("aws-access-key", "critical", r"\bAKIA[0-9A-Z]{16}\b", "AWS access key id"),
    ("github-token", "critical", r"\bgh[posru]_[A-Za-z0-9]{36,}\b", "GitHub token"),
    ("slack-token", "high", r"\bxox[baprs]-[0-9A-Za-z-]{10,}\b", "Slack token"),
    ("google-api-key", "high", r"\bAIza[0-9A-Za-z_\-]{35}\b", "Google API key"),
    ("openai-key", "high", r"\bsk-[A-Za-z0-9]{20,}\b", "OpenAI-style secret key"),
    ("generic-bearer", "warn", r"(?i)authorization:\s*bearer\s+[A-Za-z0-9._\-]{16,}", "Hard-coded bearer token"),
    ("generic-secret", "warn", r"(?i)(?:api[_-]?key|secret|passwd|password|token)\s*[:=]\s*['\"][^'\"]{8,}['\"]", "Hard-coded secret-looking assignment"),
]

_COMPILED = [(c, s, re.compile(p), m) for c, s, p, m in SECRETS]
_SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".motif"}
_SKIP_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".woff", ".woff2", ".ttf", ".ico", ".pdf"}


def scan_text(text: str, path: str = "") -> list[Finding]:
    out: list[Finding] = []
    for i, line in enumerate(text.splitlines(), 1):
        for code, sev, rx, msg in _COMPILED:
            if rx.search(line):
                out.append(Finding("secret_scanner", sev, code, msg, path, i))
    return out


def scan_path(target: str | pathlib.Path) -> list[Finding]:
    p = pathlib.Path(target)
    out: list[Finding] = []
    if p.is_file():
        files = [p]
    else:
        files = [f for f in p.rglob("*")
                 if f.is_file() and not (_SKIP_DIRS & set(f.parts)) and f.suffix.lower() not in _SKIP_EXT]
    for f in files:
        try:
            out.extend(scan_text(f.read_text(errors="replace"), str(f)))
        except OSError:
            continue
    return out
