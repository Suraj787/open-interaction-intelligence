# Evaluation Methodology

Motif's evals test **judgement, not syntax.** The risk Motif guards against is not "can the
agent write an animation", it is "does the agent choose the *right* interaction, refuse
the wrong one, respect framework/licence/safety boundaries, and ship accessible,
performant motion." Evals therefore reward correct decisions and correct *refusals*.

- **Schema:** `schemas/evaluation.schema.json`
- **Location:** `evals/`
- **Run:** as part of `make check` / CI.

## What a good eval measures

- Did the agent **search for a pattern before an effect**?
- Did it pick the **least complex** approach that fully serves the objective?
- Did it **distinguish website vs web application** correctly?
- Did it **reject** novelty, framework-mixing, licence-incompatible or unsafe requests?
- Did it produce a **reduced-motion path**, keyboard support and a performance budget?
- Did it record **provenance**?

A solution that compiles but reaches for WebGL where CSS suffices, or installs React into
a Vue project, **fails** even though the syntax is valid.

## Record fields

Required: `id`, `category`, `kind`, `prompt`, `expected_behaviour`, `judgement`.

| Field | Guidance |
|-------|----------|
| `id` | slug, `^[a-z0-9-]+$` |
| `category` | one of the eight categories below |
| `kind` | `automated` or `human-judgement` |
| `prompt` | the scenario presented to the agent |
| `context` | extra setup (e.g. "target repo is a Frappe-Vue ERP") |
| `expected_behaviour` | the decisions/refusals a correct answer must contain (≥1) |
| `must_reject` | true when the only correct answer is a refusal |
| `expected_pattern` | the pattern id a correct answer should select (or `null`) |
| `fixture` | a malicious/edge input the answer must handle (e.g. a quarantined sample) |
| `expected_findings` | for security/licence cases: what the scanners/agent must flag |
| `judgement` | how a reviewer decides pass/fail, the rubric |

## Automated vs human-judgement

- **`automated`**, deterministic checks: schema validation, scanner output against a
  fixture, "did the agent avoid installing a banned dependency," "is a reduced-motion
  fallback present," licence-gate behaviour. These run in CI.
- **`human-judgement`**, open-ended reasoning quality: was the *simplest effective*
  approach chosen, was the website/app distinction handled well, was the rejection
  rationale sound. The `judgement` field is the rubric a reviewer applies.

Both kinds are first-class; some categories mix them. Security/licence cases lean
automated (scanner findings); positive/framework cases often need human judgement.

## Eval categories

The `category` enum drives coverage. Every category must be represented:

| Category | Tests that the agent… |
|----------|------------------------|
| `positive` | selects the right pattern/effect for a genuine need (the simplest effective one). |
| `rejection` | refuses animation-for-novelty, gratuitous WebGL, decorative motion behind dense UIs, motion-only status. |
| `framework` | implements in the target stack and **never installs another framework** for an effect. |
| `accessibility` | provides keyboard/focus/semantics and a reduced-motion path; never hover-only essentials. |
| `performance` | animates transform/opacity, respects budgets, avoids jank and layout thrash. |
| `source-governance` | stays offline by default; uses source-refresh explicitly; quarantines untrusted material; never executes it. |
| `license` | applies the licence gate (unknown ⇒ reference-only), respects redistribution/attribution, never copies restricted code. |
| `security` | catches RCE/exfiltration/secret/supply-chain patterns via the scanners against malicious fixtures. |

## Malicious fixtures

`security` and `source-governance` evals reference fixtures (quarantined samples) proving
the controls catch `eval`, dynamic execution, remote script loading, undocumented network
calls, embedded secrets, dangerous dependencies, etc. The eval passes when
`expected_findings` are produced, i.e. the control fired. A regression that silences a
scanner is caught here.

## Writing a new eval

1. Pick the category and `kind`.
2. Write a realistic `prompt` (+ `context`).
3. State `expected_behaviour` as concrete decisions/refusals, and set `must_reject`
   where refusal is the only correct answer.
4. For security/licence, attach a `fixture` and list `expected_findings`.
5. Write a `judgement` rubric a reviewer can apply consistently.
6. Validate with `python -m motif validate`; ensure it runs under `make check`.
