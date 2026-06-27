---
name: security-assurance
description: Use when a dependency, snippet, or external source enters the project and needs licence, supply-chain, and untrusted-code review before it is adopted.
---

# Security Assurance

**Responsibility:** Gate everything that enters the project from outside — dependencies,
recipes, and snippets — on licence, supply-chain, and execution safety.

## When to invoke

- Step 16 of the root workflow, and any time a new dependency or external source appears.

## Inputs

- Proposed dependencies; registry/external sources; any code fetched from the internet.

## Outputs

- A licence, security, and cost verdict per dependency or source.
- A supply-chain assessment (provenance, maintenance, known advisories).
- An adopt / reject / quarantine decision feeding the ledger.

## Engine data + CLI

- Reads `assurance/` security rules, `security/`, and `policies/` (licence policy).
- `ii assure --security`, `ii deps review`.

## Notes

Never add a dependency without a licence, security, and cost review. Never execute
unreviewed internet code. Never reconstruct premium or restricted components from
previews. When provenance is unclear, quarantine rather than adopt.
