---
name: framework-compiler
description: Use when selected patterns and components must be compiled into a concrete implementation plan in the project's detected native framework, reusing what already exists.
---

# Framework Compiler (Implementation Intelligence)

**Responsibility:** Translate the approved patterns, states, and components into a
**native-framework plan** for the detected stack — never by importing a foreign
framework for a single effect.

## When to invoke

- Steps 12-14 of the root workflow, after patterns and states are fixed.

## Inputs

- Detected framework/language/styling; approved patterns and required states;
  registry and project-component inventory.

## Outputs

- A native implementation plan (components, files, props, events, slots) in the target
  stack — Vue and Frappe-Vue first-class, plus React, Svelte, Angular, or plain web.
- An explicit reuse map: existing project components and dependencies used first,
  registry recipes second, new code last.
- A dependency proposal, if any, routed to Security Assurance for licence/cost review.

## Engine data + CLI

- Reads `compiler/` and `design-intelligence/framework-guidance`; queries
  `registry/` via search.
- `ii registry search`, `ii compile --framework <vue|frappe-vue|react|svelte|...>`.

## Notes

Prefer existing project components and dependencies before adding anything. Never install
React into a Vue/Svelte/Angular project for one effect. Never execute unreviewed internet
code; only compile from approved registry sources.
