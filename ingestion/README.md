# Ingestion pipeline

Ingestion turns an untrusted public source into either an approved registry entry,
an adaptable concept, a reference-only note, or a rejection — **without ever executing
the retrieved code**.

```
discover
  → verify official source        (connectors/, security/domain-policy.yml)
  → retrieve into quarantine       (.motif/quarantine/, pinned version + SHA-256)
  → identify licence               (scanners/license_scanner.py — LICENCE GATE)
  → static security analysis       (scanners/source_scanner.py)
  → dependency inspection          (scanners/dependency_scanner.py)
  → behaviour classification       (scanners/behaviour_scanner.py)
  → secret scan                    (scanners/secret_scanner.py)
  → accessibility + performance review
  → approve · adapt · reference · reject
  → controlled installation        (motif/install.py — plan, snapshot, patch, rollback)
```

Stages map to the subdirectories here:

| Stage | Directory | Responsibility |
|-------|-----------|----------------|
| discovery | `discovery/` | enumerate official component/effect pages via a connector |
| retrieval | `retrieval/` | pull text into `.motif/quarantine/`, pin version + checksum |
| quarantine | `quarantine/` | holding area; nothing here is trusted or executed |
| normalisation | `normalisation/` | turn a reviewed item into a schema-valid registry record |

Run the scanners over a quarantined path:

```bash
python -m motif source scan .motif/quarantine/<item>
```

A `reject` verdict (any high/critical finding) blocks promotion. A `review` verdict
requires human sign-off. Only items that reach `approved/` with a verified permissive
licence and trust tier ≥ 3 may be bundled; everything else is `adaptable` or
`reference-only`. See [`docs/threat-model.md`](../docs/threat-model.md).
