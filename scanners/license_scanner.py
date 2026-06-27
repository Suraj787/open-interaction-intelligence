"""Licence detection + the LICENCE GATE.

Determines a redistribution class from detected licence text. The hard rule:
an unknown / unrecognised licence is `reference-only`, never `bundled`.
Source-available / Commons-Clause terms are NOT treated as permissive OSS.
"""
from __future__ import annotations
import re
import pathlib
from . import Finding

# spdx id -> (bundleable, redistribution-class)
KNOWN = {
    "MIT": (True, "redistributable"),
    "Apache-2.0": (True, "redistributable"),
    "BSD-2-Clause": (True, "redistributable"),
    "BSD-3-Clause": (True, "redistributable"),
    "ISC": (True, "redistributable"),
    "MPL-2.0": (True, "redistributable"),
    "CC-BY-4.0": (False, "adaptable-concept"),
    "GPL-3.0": (False, "adaptable-concept"),
    "AGPL-3.0": (False, "reference-only"),
    "LicenseRef-GSAP-Standard": (False, "reference-only"),
}

_SIGNS = [
    ("MIT", r"\bMIT License\b|Permission is hereby granted, free of charge"),
    ("Apache-2.0", r"Apache License,?\s+Version 2\.0"),
    ("BSD-3-Clause", r"Redistribution and use in source and binary forms.*Neither the name"),
    ("BSD-2-Clause", r"Redistribution and use in source and binary forms"),
    ("ISC", r"\bISC License\b"),
    ("MPL-2.0", r"Mozilla Public License Version 2\.0"),
    ("GPL-3.0", r"GNU GENERAL PUBLIC LICENSE\s+Version 3"),
    ("AGPL-3.0", r"GNU AFFERO GENERAL PUBLIC LICENSE"),
    ("CC-BY-4.0", r"Creative Commons Attribution 4\.0"),
]
_COMMONS_CLAUSE = re.compile(r"Commons Clause", re.I)


def detect_license(text: str) -> str:
    if _COMMONS_CLAUSE.search(text):
        return "LicenseRef-Commons-Clause"
    for spdx, sign in _SIGNS:
        if re.search(sign, text, re.I | re.S):
            return spdx
    m = re.search(r"SPDX-License-Identifier:\s*([\w.\-]+)", text)
    if m:
        return m.group(1)
    return "UNKNOWN"


def classify(spdx: str) -> tuple[bool, str]:
    if spdx in KNOWN:
        return KNOWN[spdx]
    return (False, "reference-only")  # LICENCE GATE: unknown ⇒ reference-only


def scan_text(text: str, path: str = "") -> list[Finding]:
    spdx = detect_license(text)
    bundleable, klass = classify(spdx)
    if spdx == "UNKNOWN":
        return [Finding("license_scanner", "high", "unknown-license",
                        "No recognised licence, gate to reference-only, never bundle", path)]
    if spdx == "LicenseRef-Commons-Clause":
        return [Finding("license_scanner", "high", "commons-clause",
                        "Commons Clause is source-available, NOT permissive OSS, not redistributable", path)]
    sev = "info" if bundleable else "warn"
    return [Finding("license_scanner", sev, "license-detected",
                    f"Detected {spdx} → {klass} (bundleable={bundleable})", path)]


def scan_path(target: str | pathlib.Path) -> list[Finding]:
    p = pathlib.Path(target)
    candidates: list[pathlib.Path]
    if p.is_file():
        candidates = [p]
    else:
        candidates = [f for f in p.rglob("*")
                      if f.is_file() and re.match(r"licen[cs]e", f.name, re.I)]
    if not candidates:
        return [Finding("license_scanner", "high", "no-license-file",
                        "No LICENSE file found, gate to reference-only", str(p))]
    out: list[Finding] = []
    for f in candidates:
        try:
            out.extend(scan_text(f.read_text(errors="replace"), str(f)))
        except OSError:
            continue
    return out
