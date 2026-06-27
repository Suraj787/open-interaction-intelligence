# InterfaceBench — Human-Review Rubric

A reviewer scores each of the 15 capabilities on a **0–3** scale against the output of a
run (single case or full longitudinal scenario). Automated checks gate the result: a
hard automated failure caps the related capability at 0–1 regardless of the reviewer's
impression.

**Scale**
- **0 — Absent / harmful:** the capability is missing, or the agent did the wrong thing.
- **1 — Token / superficial:** gestured at but unreliable, incomplete, or generic.
- **2 — Solid:** done correctly for the common cases; minor gaps.
- **3 — Exemplary:** complete, deliberate, justified, and robust under pressure.

Score each block. The run total is the sum (max 45). Record one-line evidence per score.

---

## 1. Product understanding
- **0** Generic template; no sign of who uses it or why.
- **1** Names the domain but the structure ignores the real task.
- **2** Structure clearly fits the primary task and user.
- **3** Layout, density and defaults all trace to a specific, articulated user/task model.

## 2. Structural concept diversity
- **0** One default shape applied regardless of problem.
- **1** Variation only in colour/font; structure unchanged.
- **2** Structure chosen to fit; some real alternatives considered.
- **3** Distinct structural concepts weighed; the chosen one is defended against rejected ones.

## 3. Avoiding generic AI aesthetics
- **0** Purple-gradient/glass-card/decorative-blur default tell-tales throughout.
- **1** Some defaults remain unexamined.
- **2** Mostly free of generic tells; intentional choices.
- **3** Visibly authored from the product; no default aesthetic substituting for thought.

## 4. Preserving product identity
- **0** Change erases or contradicts the product's identity.
- **1** Identity survives by accident, inconsistently.
- **2** Identity preserved across the change.
- **3** Identity deliberately evolved through the token/system layer; recognisable and coherent.

## 5. Required-state completeness
- **0** Happy path only.
- **1** A couple of states; key ones (error, empty, partial) missing.
- **2** Full common state set present and correct.
- **3** Complete set incl. permission-denied, zero-results, partial/indeterminate, disabled, with async status surfaced.

## 6. Keyboard / assistive-technology support
- **0** Mouse-only; no roles/labels.
- **1** Partial keyboard; focus/labels unreliable.
- **2** Full keyboard, visible focus, correct roles/labels.
- **3** The above plus `aria-live` for async/bulk results and correct focus management in overlays.

## 7. 200% zoom
- **0** Layout breaks or traps horizontal scroll at 200%.
- **1** Usable but with clipping/overlap.
- **2** Reflows and stays usable at 200%.
- **3** Reflows cleanly with no loss of function or content at 200%+.

## 8. Reduced motion
- **0** Forces motion / defeats `prefers-reduced-motion`.
- **1** Honours it but loses meaning (blank where motion conveyed something).
- **2** Honours it with sensible static/instant fallbacks.
- **3** Motion is purposeful and degrades gracefully to a still-meaningful static state.

## 9. Performance budgets
- **0** No budget; unbounded render/bundle/motion cost.
- **1** Implicit awareness, no stated budget.
- **2** Explicit budgets and they are met for the common case.
- **3** Budgets stated, met and defended under scale (e.g. 1,000 records) with no decorative cost growth.

## 10. Framework adaptation
- **0** Pulls a foreign runtime in for an effect.
- **1** Mixes idioms awkwardly.
- **2** Implements techniques in the project's framework correctly.
- **3** Reproduces sourced techniques natively and idiomatically, with no foreign runtime.

## 11. Dependency discipline
- **0** Adds unjustified/unremovable/licence-unclear dependencies.
- **1** Dependencies present but unexamined.
- **2** Dependencies justified, minimal and licence-clean.
- **3** Dependencies minimal and removable; effects reproducible natively; removal demonstrated when asked.

## 12. Decision explanation
- **0** No rationale.
- **1** Post-hoc, vague rationale.
- **2** Clear reasons for the significant choices.
- **3** Reasons plus explicit rejected alternatives and the trade-offs behind each.

## 13. Provenance
- **0** Sourced techniques with no origin recorded.
- **1** Origins mentioned but copied/reference/reimplemented status unclear.
- **2** Origins recorded with copy-vs-reference status.
- **3** Full provenance: origin, licence status, and copied/reference-only/reimplemented, per source.

## 14. Effect rejection
- **0** Accepts every requested decorative/showcase effect.
- **1** Rejects only the most extreme requests.
- **2** Rejects effects that do not serve product/context/device, with reasons.
- **3** Consistently restrained; admits only effects justified by a real product moment and budget.

## 15. Coherence after repeated modifications
- **0** Patchwork; conflicting patterns; unbounded drift after edits.
- **1** Mostly holds but visible drift/duplication in corners.
- **2** Stays coherent; debt bounded and mostly tracked.
- **3** One coherent system after all rounds; debt named, bounded and remediable; no surviving stale assumptions.

---

### Gating rules (automated → rubric cap)
- Defeats `prefers-reduced-motion` → capability 8 capped at 0.
- Bundles unknown/incompatible-licence code → capabilities 11 and 13 capped at 1.
- Ships no error or empty state on an interactive surface → capability 5 capped at 1.
- Pulls a foreign framework runtime for an effect → capability 10 capped at 0.
- Renders all rows with no virtualisation/pagination at 1,000 records → capability 9 capped at 1.
