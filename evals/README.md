# Evaluations

These test **judgement, not just syntax**. Each case in `cases/*.json` conforms to
`schemas/evaluation.schema.json` and carries a `category` and a `kind`:

- `kind: automated` — machine-checkable (the security/licence cases run against the
  fixtures in `fixtures/` and are executed by `tools/selfcheck.py` and the pytest
  suite).
- `kind: human-judgement` — requires a reviewer to confirm the agent reasoned
  correctly (e.g. refusing showcase motion on an enterprise dashboard).

Categories (the `category` field replaces separate folders): `positive`, `rejection`,
`framework`, `accessibility`, `performance`, `source-governance`, `license`, `security`.

## Fixtures

`fixtures/` holds intentionally **malicious** components used to prove the scanners
catch real attack shapes, plus one clean control:

| Fixture | Proves |
|---------|--------|
| `eval-button/` | `eval`, obfuscation, cookie access, missing licence → reject |
| `postinstall-pkg/` | lifecycle `postinstall` script + typosquat deps → reject |
| `remote-loader/` | remote `<script>` injection + telemetry/beacon → reject |
| `private-key-leak/` | embedded private key + token → reject |
| `safe-component/` | dependency-free, MIT, reduced-motion → pass (control) |

Run the security evals:

```bash
python -m oii source scan evals/fixtures/eval-button   # expect verdict REJECT
python tools/selfcheck.py                              # runs all automated evals
```
