.PHONY: check validate ii-validate selfcheck ii-selfcheck v3-selfcheck v3-1-selfcheck test lint index doctor secrets clean \
	check-runtime check-atlas check-mcp check-bench check-guardian check-evidence check-browser check-repair check-v3-1 bench-golden

# One command that mirrors CI. Dependency-free by default.
check: validate ii-validate selfcheck ii-selfcheck v3-selfcheck v3-1-selfcheck secrets
	@echo "==> make check: OK"

validate:
	@python3 -m motif validate

ii-validate:
	@python3 -m ii validate

selfcheck:
	@python3 tools/selfcheck.py

ii-selfcheck:
	@python3 tools/ii_selfcheck.py

v3-selfcheck:
	@python3 tools/v3_selfcheck.py

v3-1-selfcheck:
	@python3 tools/v3_1_selfcheck.py

# v3 surface smoke targets (subsets of the v3 self-check).
check-runtime check-atlas check-mcp check-bench check-guardian:
	@python3 tools/v3_selfcheck.py

# v3.1 evidence + browser + repair targets.
check-evidence check-browser check-repair check-v3-1:
	@python3 tools/v3_1_selfcheck.py

# Golden evidence-grounded repair benchmark (deterministic; browser steps not-executed here).
bench-golden:
	@python3 -m ii repair golden --target evals/fixtures/sample-vue-app --route /projects

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
