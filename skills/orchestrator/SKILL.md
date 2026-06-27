---
name: orchestrator
description: Use when any interface task begins and you need a single entry point that defers to the Interface Intelligence OS root orchestrator and its mandatory 18-step workflow.
---

# Orchestrator (thin entry)

This skill is a thin alias. It exists so callers can invoke "orchestrator" and be routed
to the authoritative root.

## When to invoke

- At the start of any design, build, improve, audit, or migration task.
- Whenever a sub-skill needs to re-anchor on the full workflow or the hard rules.

## What it does

- Defers to the root `SKILL.md` (`interface-intelligence-os`).
- Runs the mandatory 18-step workflow and enforces the hard-rule never-list.
- Loads engine knowledge selectively and delegates to the specialist skills.

## Inputs / outputs

- **Input:** the user request and the target repository.
- **Output:** routing into the root workflow; no independent logic of its own.

## CLI

`ii` (aliases `oii`, `motif`). Start with `ii inspect` then `ii classify`.

Do not duplicate workflow logic here. The root file is the single source of truth.
