# Release Process

Motif releases are deliberately conservative: a tag means "a genuinely usable release,"
never "the build happened to pass today." This document covers commit discipline, the
local quality gate, and the versioning rules.

## Conventional commits

Every change uses a [Conventional Commits](https://www.conventionalcommits.org) message
and commits **only validated work**.

- Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `build`, `ci`.
- Commit at phase boundaries: inspect changed files → run validation → fix → update
  `PHASE_STATUS.md` → commit with a meaningful message.
- **Never push broken or partially validated work. Never force-push.** `main` is the
  default branch; never overwrite an unrelated remote.
- Never commit secrets, tokens, SSH keys or private configuration.

## `make check`, the single local gate

`make check` is the **one local mirror of CI**. It must pass before any tag. It runs on
the dependency-free core (Python standard library), so it works anywhere; optional tools
such as `jsonschema` are used if present but never required.

`make check` covers:

- **Schema validation**, every registry record validates against its schema
  (`python -m motif validate`).
- **Scanners**, `source`, `dependency`, `license`, `behaviour`, `secret` scanners run
  against the malicious fixtures and produce expected findings.
- **Evals**, automated eval cases pass (judgement, rejection, framework, accessibility,
  performance, source-governance, licence, security).
- **Doctor**, `python -m motif doctor` reports a healthy environment.
- **Index**, generated indexes are current.

Read recent `git log` and run `make check` at the start of any continuation session
before resuming the lowest-numbered incomplete phase (see `PHASE_STATUS.md`).

## Clean-checkout test

Before tagging, verify the release from a **fresh clone / clean checkout** (no local
build artefacts, no uncommitted files):

1. Clone or export the repo to a clean directory.
2. Run `make check` there, it must pass with no extra setup.
3. Exercise the CLI: `python -m motif doctor`, `python -m motif validate`,
   `python -m motif search`.

This proves the release is self-contained and that the offline-approved-registry default
works without network access.

## Secret scan

Run the secret scan over the clean checkout and confirm no secrets, tokens or credentials
are present in history or tree before tagging. A failed secret scan blocks the release.

## Tag only a genuinely usable release

A tag is a promise. Only tag when:

- `make check` passes on a clean checkout,
- the secret scan is clean,
- `PHASE_STATUS.md` reflects reality (no "complete" claims over partial work),
- the CHANGELOG entry is accurate, and
- the release does what it claims for the stated scope, **representative depth with
  high-confidence records beats fabricated breadth.**

Publication (pushing to a public remote) is intentionally left to an explicit human
go-ahead; exact publish commands are provided, never auto-run.

## Version discipline

Motif follows semantic versioning with a deliberate, honest progression:

| Version | Meaning |
|---------|---------|
| **v0.1.0** | Complete architecture + working secure pipeline; **representative**, high-confidence records (not exhaustive breadth). The system is real and safe to use within its stated scope. |
| **v0.2.0** | Broader verified coverage, more sources moved from `pending-verification` to `verified`, more catalogued components, more recipes, with no regressions to the pipeline or scanners. |
| **v1.0.0** | Stable, broadly verified registry and frozen schema/CLI surface; suitable for general adoption. Reserved until coverage and stability genuinely justify it. |

Do not inflate the version to imply coverage that does not exist. Moving a source from
`pending-verification` to `verified` is real progress and belongs in a minor bump; a major
bump asserts schema/CLI stability and broad verification.
