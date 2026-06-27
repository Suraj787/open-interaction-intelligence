# Workflow: Select an Effect for a Known Problem

Use when the pattern/problem is already clear and you need to choose the specific effect
and rank candidates transparently. Always confirm a pattern fits **before** picking an
effect.

## Preconditions

- The interaction problem and product context are known.
- Default **offline approved registry** mode.

## Steps

1. **Restate the objective.** What must the user understand, feel or accomplish? Confirm
   website vs web application.
2. **Confirm the pattern.** `python -m motif search "<problem>"`; verify a pattern in
   `registry/patterns/` matches. If none does, step back to interaction design, do not
   force an effect.
3. **Discover candidates.** Load `skills/effect-discovery`; list the pattern's
   `recommended_effects` and any close alternatives:
   `python -m motif component alternatives <id>`.
4. **Screen each candidate** against context:
   - `enterprise_suitability` / `marketing_suitability`;
   - `complexity`, `performance_cost`, `accessibility_risk`, `mobile_suitability`;
   - dependency weight (implementation hierarchy);
   - presence of a `reduced_motion_fallback`.
5. **Rank transparently** (`skills/effect-selection`). State the criteria and the score
   for each candidate; show why others were rejected (`rejected_effects` reasoning).
6. **Pick the simplest fully effective option.** Never let novelty outrank usability;
   never add a dependency without a licence + cost review; never combine multiple
   high-attention effects without explicit justification.
7. **Record the choice and rationale** (`schemas/decision.schema.json`): selected effect,
   alternatives considered, accessibility/performance/dependency impact, reduced-motion
   strategy.

## Hand-off

Pass the selected effect to [implement-pattern.md](implement-pattern.md) or a build/
improve workflow for framework adaptation and validation.

## Done when

One effect is selected with a transparent ranking, an explicit rejection rationale for the
alternatives, and a recorded decision.
