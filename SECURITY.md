# Security Policy

Motif's core purpose includes governance: helping AI coding agents discover, select, adapt
and validate interaction code **without** taking the tempting-but-dangerous path of
scraping a site, running its install script and copying its code into your project. This
document describes the threat posture, how to report a vulnerability, and what the
built-in scanners do and do not guarantee.

## Threat posture

Motif is designed so that the unsafe path is the hard path:

- **Offline approved registry is the default.** Normal use reads the committed local
  registry and never touches the network. Internet retrieval happens only through an
  explicit `python -m motif source retrieve --refresh` against an allowlisted official host
  (`security/domain-policy.yml`).
- **Untrusted-by-default ingestion.** Retrieved material lands in `.motif/quarantine/` and
  is **never executed, imported or evaluated**. It is reviewed statically and moves
  through `.motif/quarantine/ → reviewed/ → approved/ | rejected/`.
- **Licence gate.** Unknown licence ⇒ `reference-only`, never bundled. Source-available
  and Commons-Clause terms are not treated as permissive OSS.
- **Trust tiers 1–5.** Tier 5 is reference-only / rejected. Bundling requires a verified
  permissive licence **and** trust tier ≥ 3.
- **Controlled installation.** Plan → snapshot → controlled patch → validate →
  auto-rollback on failure → provenance manifest. Third-party installers are never run
  against your project.

Policies live in `security/*.yml` (`dangerous-patterns.yml`, `dependency-policy.yml`,
`domain-policy.yml`, `network-policy.yml`, `sandbox-policy.yml`, `trust-policy.yml`).
The full analysis is in [`docs/threat-model.md`](docs/threat-model.md).

> **Motif reduces risk but cannot guarantee that third-party code is completely safe.**
> Static analysis has limits, licences change, and upstream sources can be compromised.
> Human review remains required before any external material is adopted.

## Reporting a vulnerability

Please report security issues **privately**. Do not open a public issue for an
unfixed vulnerability.

- **Open a private security advisory on GitHub** for this repository
  (the repository's *Security → Advisories → Report a vulnerability* flow / GitHub
  private vulnerability reporting).

Include: affected version, a description of the issue, reproduction steps or a proof of
concept, and the impact you observed. We will acknowledge the report, investigate, and
coordinate a fix and disclosure timeline with you. Please give us reasonable time to
remediate before any public disclosure.

There is no published security email address for this project — use GitHub's private
advisory mechanism.

## What the scanners do

Five static scanners in [`scanners/`](scanners/) review quarantined and candidate
material before anything is approved. They never execute the code they inspect.

| Scanner | Purpose |
|---------|---------|
| `source_scanner.py` | Flags dangerous source patterns (per `security/dangerous-patterns.yml`) such as risky dynamic evaluation, obfuscation and unsafe APIs. |
| `behaviour_scanner.py` | Flags suspicious browser behaviour (exfiltration-shaped network calls, unexpected DOM/storage access, etc.). |
| `dependency_scanner.py` | Reviews declared dependencies against `security/dependency-policy.yml`. |
| `license_scanner.py` | Checks licence signals and enforces the licence gate (unknown ⇒ reference-only). |
| `secret_scanner.py` | Detects committed secrets/credentials; wired into `make check` to refuse tracked secrets. |

## Limits of the scanners

The scanners are a defence-in-depth aid, not a guarantee:

- They perform **static** analysis only. They do not run, sandbox-execute or
  dynamically trace code, so behaviour that only manifests at runtime can be missed.
- They are **heuristic**. They will produce false positives and can miss novel,
  heavily obfuscated or logic-bomb-style threats.
- **Licence detection is best-effort.** Licence facts are confidence-rated and must be
  re-verified online; a clean licence scan is not legal advice.
- They do not assess upstream account compromise, supply-chain tampering before
  retrieval, or the trustworthiness of an allowlisted host beyond policy.

Treat a clean scan as "no known issues found", not "proven safe". Human review and the
controlled-install diff + rollback remain part of the process.

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | ✅ Supported |
| < 0.1.0 | ❌ Not supported |

Security fixes target the latest 0.1.x release. As later versions ship, this table will
be updated to reflect the supported window.
