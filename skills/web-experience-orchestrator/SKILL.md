---
name: web-experience-orchestrator
description: Use as a convenience entry point for web experience and interaction-design requests; it immediately defers to the open-interaction-intelligence root orchestrator.
---

# Web Experience Orchestrator (alias)

**Responsibility:** Thin alias / entry point. It holds no logic of its own; it routes to
the root `open-interaction-intelligence` skill.

## When to invoke

- When a request arrives phrased as "web experience", "interaction design", or
  "motion/effect" work and you want a familiar entry point.

## What it does

1. Defers to the root `open-interaction-intelligence` orchestrator.
2. Runs the same 16-step workflow and Hard rules.
3. Loads the same specialist skills and `python -m oii` CLI.

## How it connects

- Adds nothing to `registry/` or `intelligence/`; it only forwards.

## Notes

Do not duplicate orchestration logic here. If behaviour needs to change, change the root
skill. This file exists only so multiple natural entry phrases reach the same governance.
