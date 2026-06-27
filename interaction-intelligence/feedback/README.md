# Feedback Guidance

How the interface tells the user what is happening. Pairs with `async-action`, `data-fetch-region`, `button`, and `form` state records in `../states/`.

## Acknowledge every action
- Respond to user-initiated actions within ~100ms (visible press/active state) even if the result is pending.
- For async work, move the trigger to **loading** and disable it to prevent double submission.
- Confirm completion with a persistent **success** cue, and surface failure with an explicit, recoverable **error**.

## Make feedback multi-channel (never motion- or colour-only)
- Pair every status change with text + icon, and announce it via `aria-live` / status messages (WCAG 4.1.3).
- Colour and motion may emphasise; they must never be the sole carrier of meaning (colour-blind, reduced-motion, screen-reader users).

## Match the channel to the weight of the message
- **Inline** (next to the field/region): validation, contextual errors, per-item status.
- **Toast / snackbar:** transient confirmations of background actions; auto-dismiss, with an undo where reversible.
- **Banner:** persistent, page-level conditions (offline, degraded, permission limits).
- **Modal / dialog:** only for blocking decisions and destructive confirmations.

## Loading and waiting
- 0–1s: no spinner needed; keep the trigger's active state.
- ~1s+: show feedback (skeleton or spinner); delay skeletons ~150–200ms to avoid flashes on fast responses.
- ~10s+ or slow-network: show **determinate** progress and, where possible, a cancel option.
- Use **skeletons** that mirror final layout to reduce shift; never fabricate fake progress.

## Errors that help
- Say what happened, why, and the next step (WCAG 3.3.1 / 3.3.3) — in plain language, not error codes alone.
- Keep the user's input intact; offer **retry** for transient failures.
- Distinguish error from empty: a failed fetch is not "no data".

## Honesty and restraint
- Feedback must reflect real system state — no theatre, no celebration for routine actions.
- Optimistic UI must mark provisional state (**stale**) and visibly roll back on conflict or rejection.
- Confirmations should be quiet and persistent for routine success; save celebration for rare milestones.
