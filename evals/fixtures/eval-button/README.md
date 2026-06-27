# Fixture: eval-button (MALICIOUS, for scanner tests only)

This directory is intentionally unsafe. It is never installed; it exists so the
test suite can prove the scanners catch real attack shapes.

Expected detections:
- `source_scanner`: `eval`, obfuscation (hex run), `atob`
- `behaviour_scanner`: `document.cookie`
- `license_scanner`: no LICENSE file → unknown licence → reference-only/reject

There is deliberately **no LICENSE file** here.
