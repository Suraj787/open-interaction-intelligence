---
name: product-intelligence
description: Use when you need to model the product, its users, their workflows, risk, density, device, and environment before any interface decision is made.
---

# Product Intelligence

**Responsibility:** Establish *who* the interface is for and *what outcome* is at stake,
so every later decision is anchored in a real user need rather than aesthetics.

## When to invoke

- Steps 4-5 of the root workflow, before design or interaction choices.
- Whenever a request lacks a stated user, task, or outcome.

## Inputs

- The user request, repo signals, and any existing product docs or manifests.

## Outputs

- A **product model** (purpose, product type: website vs web app, domain).
- A **user model** (audiences, jobs-to-be-done, expertise).
- A **workflow model** (tasks, frequency, criticality, data density).
- A **risk model** and an **environment model** (device, connectivity, context of use).
- A **confidence level** for each inference, marked as inference not fact.

## Engine data + CLI

- Reads `product-intelligence/` (`product-model`, `user-model`, `workflows`,
  `risk-model`, `environment-model`, `confidence`, `manifests`).
- `ii classify`, `ii product model`, `ii product users`, `ii product workflows`.

## Notes

Never present a low-confidence inference as verified fact. State assumptions explicitly
and flag what must be confirmed with the user or with evidence.
