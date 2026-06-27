# Workflow Model

The workflow model answers: **what concrete sequences of action must the product support
well?** It populates the `workflows` array (and informs `information.objects`) of the
[Product Context Manifest](../../schemas/product-context.schema.json).

Each workflow is a short, plain-language description of a *task as it actually unfolds* —
including the messy parts (interruption, error, retry), not just the happy path.

## What a good workflow line looks like

> "Resume after interruption: return to a half-finished administration and re-confirm
> state without double-dosing."

It names the trigger, the steps, and the failure mode the design must protect. Compare
the weak version: *"administer medication"* — which hides everything that makes the task
hard.

## How it is built

1. **Derive workflows from user goals.** Each ranked goal in the
   [user model](../user-model/README.md) becomes one or more workflows.
2. **Walk the task in time.** Trigger → steps → confirmation → result. Note where the user
   waits, switches device, or is interrupted.
3. **Include the unhappy paths that matter.** Payment failure, lost connectivity,
   interruption mid-task, a safety warning. These are where interaction design earns its
   keep, so they belong in the manifest.
4. **Extract the domain objects** the workflow touches (`task`, `dose`, `payment-method`,
   `order-total`) into `information.objects`, and set `information.density` from how many
   of these must be visible at once.
5. **Keep it about *what*, not *how*.** "Recover from a card error without losing data" is
   a workflow; "show a red toast" is a downstream design decision — leave it out.

## How it is validated

- Every primary user goal is covered by at least one workflow.
- At least the critical unhappy paths implied by the risk model appear here.
- `information.objects` is consistent with the objects named across the workflows.
- `information.density` matches reality (a high-density claim must be justified by the
  number of objects in view; a low-density claim must show progressive disclosure).

## Honesty rules

- A workflow assembled from how-it-*probably*-works, without observation, is an
  **inference** — flag it. Real task analysis (interviews, session replay) is what moves a
  workflow into `verified`.
- If you do not know whether a path exists (e.g. is offline administration permitted?),
  do not invent its steps — record the question in `unresolved`.
