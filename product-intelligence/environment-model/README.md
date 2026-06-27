# Environment Model

The environment model answers: **where, on what, and under what conditions is the product
used?** It populates the `environment` object of the
[Product Context Manifest](../../schemas/product-context.schema.json).

Context of use constrains the design as hard as the user does. A one-handed phone on a
flaky mobile network and a dual-monitor desktop on corporate wifi are different products
even if the data is identical.

## Fields

| Field | Meaning |
|-------|---------|
| `primary_device` | The device most usage happens on, with its physical constraints (touch, screen size, input). |
| `secondary_device` | The next most common device; often read-only or occasional. |
| `connectivity` | Network reality: stable, intermittent, dead zones, low tolerance. Drives offline and idempotency requirements. |
| `localisation` | Languages/locales (BCP-47 tags) the interface must serve. |

## How it is built

1. **Determine the primary device from where the work happens**, not from where it
   *could* happen. Bedside care → mobile/cart at the bedside. Portfolio triage → desktop.
2. **Capture the device's physical constraints**, because they are real design limits:
   thumb reach and small screen (mobile), density and keyboard (desktop), shared hardware
   needing fast user-switching (clinical carts).
3. **State connectivity as a contract.** "Intermittent with dead zones" obliges
   resumability and idempotent submits; "stable corporate network" relaxes them. This is
   one of the most consequential lines in the manifest.
4. **Set localisation from the audience and markets**, and note where it is unknown.

## How it is built into downstream behaviour

- Mobile-primary + low connectivity → idempotent, resumable steps; large touch targets;
  minimal keyboard. (See the e-commerce checkout manifest.)
- Shared mobile device + frequent use → fast re-auth, idle lock, no session bleed. (See the
  medication-admin manifest.)
- Desktop-primary + high density → keyboard-first navigation, saved views. (See the
  project-management manifest.)

## How it is validated

- `primary_device` is consistent with the user's `frequency` and the workflows (a daily
  high-density desktop task should not claim a phone as primary).
- `connectivity` claims are matched by constraints in the risk model (a "low connectivity
  tolerance" with no resumability constraint is an inconsistency).
- `localisation` tags are valid BCP-47 and consistent with `audience`.

## Honesty rules

- Device and connectivity are frequently **assumed** from product type rather than
  measured. Put those in `assumptions`, and the real device fleet / network survey in
  `unresolved` until confirmed.
- Do not assert a localisation footprint you have not been told; list the open question
  instead.
