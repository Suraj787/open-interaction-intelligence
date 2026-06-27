.PHONY: check validate selfcheck test lint index doctor secrets clean

# One command that mirrors CI. Dependency-free by default.
check: validate selfcheck secrets
	@echo "==> make check: OK"

validate:
	@python3 -m motif validate

selfcheck:
	@python3 tools/selfcheck.py

# Full pytest suite (requires dev extras: pip install -e '.[dev]')
test:
	@python3 -m pytest -q || (echo "pytest not installed, run 'pip install -e .[dev]' (selfcheck already covers the gate)"; exit 0)

lint:
	@ruff check motif scanners tools tests || echo "ruff not installed, skipping (optional)"

index:
	@python3 -m motif generate-index

doctor:
	@python3 -m motif doctor

# Refuse to ship tracked secrets, scans the repo (excludes .git/node_modules/.motif).
secrets:
	@python3 -c "import sys,pathlib; sys.path.insert(0,'.'); from scanners import secret_scanner as s; \
f=[x for x in s.scan_path('.') if x.severity in ('high','critical')]; \
[print('  ',x.severity,x.code,x.path,x.line) for x in f if 'fixtures' not in x.path]; \
real=[x for x in f if 'fixtures' not in x.path]; \
print('secret scan:', 'CLEAN' if not real else f'{len(real)} FINDING(S)'); sys.exit(1 if real else 0)"

clean:
	@find . -type d -name __pycache__ -prune -exec rm -rf {} + 2>/dev/null || true
	@rm -rf .motif/snapshots
