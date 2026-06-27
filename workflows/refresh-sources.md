# Workflow: Refresh Sources (Internet Retrieval)

This is the **only** workflow that reaches the internet. Normal usage stays offline. A
source-refresh discovers/updates external material, brings it through the secure ingestion
pipeline, and never executes it. Run it deliberately, not by default.

## Preconditions

- Explicit intent to refresh (this overrides the offline default).
- `python -m motif doctor` healthy. Load `skills/source-governance`.
- Domain allowlist and policies in `security/*.yml` are current.

## Steps

1. **Discover.** `python -m motif source discover <source>` — read public metadata and
   official component pages only. Connectors must not follow unknown domains, URL
   shorteners, IP hosts, localhost or private ranges.
2. **Verify official source.** Confirm homepage + repository; choose the retrieval path in
   priority order: tagged release → package registry → component registry → pinned commit
   → webpage (last resort).
3. **Retrieve into quarantine.** `python -m motif source retrieve <source>` lands material in
   `.motif/quarantine/`. **It is never executed.** No `npm install`, no lifecycle scripts,
   no shell-from-docs, no binaries.
4. **Pin + checksum.** Record version, tag, commit hash, retrieval date and SHA-256.
5. **Scan.** `python -m motif source scan <source>` runs the five scanners
   (`source`, `dependency`, `license`, `behaviour`, `secret`) against the policies. Review
   **every** flagged finding (not every occurrence is malicious, but each must be
   reviewed).
6. **Licence gate.** Identify the licence at its official location. Unknown licence ⇒
   `reference-only`, never bundled. Source-available/Commons-Clause/paid ≠ permissive.
7. **Dependency inspection.** Review direct/transitive/peer/optional deps, lifecycle
   scripts, maintainer identity, typosquatting, advisories, dependency growth.
8. **Behaviour + accessibility/performance review.** Confirm no undocumented network,
   storage, clipboard, or device access; assess accessibility and performance.
9. **Decide:** `python -m motif source approve <source>` or
   `python -m motif source reject <source>`. Approve → write/update the source record
   (`source.schema.json`) using [source-review.md](../docs/source-review.md). For
   restricted-but-useful sources, mark `adaptable-concept` and route to clean-room
   adaptation (retain no source).
10. **Record honestly.** Set `status` (`verified` / `pending-verification` / `rejected`),
    `confidence`, `evidence`, `last_reviewed`. **Do not fabricate.**
11. **Re-index + validate:** `python -m motif generate-index` and `python -m motif validate`.

## Done when

The source's material is quarantined, scanned, licence-gated, and either approved into the
registry with evidence or rejected — with nothing executed and the registry re-validated.
