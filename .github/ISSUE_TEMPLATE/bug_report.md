---
name: Bug report
about: Report a problem with the CLI, registry, scanners or pipeline
title: "bug: "
labels: [bug]
assignees: []
---

## Summary

A clear, concise description of the bug.

## Area

Which part of OII is affected?

- [ ] CLI (`python -m oii ...`)
- [ ] Registry / schema validation
- [ ] Ranking / selection
- [ ] Ingestion / connectors / quarantine
- [ ] Scanners (`scanners/`)
- [ ] Controlled install / rollback
- [ ] Adapters / implementations
- [ ] Skills / agents / workflows
- [ ] Docs
- [ ] Other

## Steps to reproduce

1. ...
2. ...
3. ...

## Expected behaviour

What you expected to happen.

## Actual behaviour

What actually happened. Include error output or logs (redact any secrets).

## `make check` output

Does `make check` pass? Paste relevant output if it fails.

```
(paste here)
```

## Environment

- OII version / commit:
- OS:
- Python version (`python --version`):

## Additional context

Anything else that helps, including whether AI assistance was involved in reproducing.
