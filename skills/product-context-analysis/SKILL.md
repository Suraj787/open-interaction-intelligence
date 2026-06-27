---
name: product-context-analysis
description: Use when you need to establish the product purpose, product type, page/screen type, and the user with their primary task before any interaction or effect is considered.
---

# Product Context Analysis

**Responsibility:** Resolve the top four levels of the Motif reasoning model so every
later decision is grounded in context, not aesthetics.

## When to invoke

- At the start of any Motif task (steps 1-5 of the root workflow).
- Whenever the interaction objective is unclear or contested.

## Inputs

- The target repository (framework, routes, design tokens, existing components).
- The product brief or request.

## Outputs

- **Development purpose** — why the product exists.
- **Product type** — and a firm **website vs web application** classification.
- **Page/screen type** — landing, dashboard, list/table, form, detail, wizard, etc.
- **User + primary task** — who acts and what they are trying to accomplish.
- A short statement of the **interaction problem** to hand to `interaction-design`.

## How it connects

- Reads `intelligence/` taxonomies (product types, page types, user intents) to
  classify, not to prescribe effects.
- Does **not** touch `registry/` — context first, catalogue later.
- Hands its findings to `interaction-design`; records them in the decision log.

## Notes

Websites optimise persuasion and narrative; web applications optimise task throughput
and repeat use. Misclassifying here cascades into wrong patterns downstream, so make the
website/application call explicit and justify it.
