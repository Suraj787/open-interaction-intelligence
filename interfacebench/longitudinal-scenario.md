# InterfaceBench, The Longitudinal Scenario

One product, ten rounds, building on the same codebase. The point is not any single
round but the **trajectory**: does the interface stay correct, usable, accessible,
performant and coherent as real-world pressure accumulates? Each round below gives the
prompt, what a good agent does, the failure modes, and what is measured.

The product: an internal **project tracker** used by a services company. Round 1 starts
from nothing; every later round edits the artefact produced by the previous rounds.

---

## Round 1, Build the project list

**Prompt:** "Build the main screen: a list of projects the team can scan and act on."

**What a good agent does:** Establishes product context (who uses it, the primary
task: triage and act on projects). Chooses a structure that fits scanning real work, density, sort, the columns that matter (status, owner, due, health). Defines the
shared system (tokens, spacing, components) it will reuse later. Ships list states:
loading, empty, error, zero-results.

**Failure modes:** Generic SaaS dashboard with vanity stat cards; a beautiful empty
state but no loading/error; decorative gradients standing in for hierarchy; a structure
copied from a template rather than chosen from the task.

**Measured:** product understanding, structural concept diversity, avoiding generic AI
aesthetics, required-state completeness.

---

## Round 2, Add bulk actions

**Prompt:** "Let users select multiple projects and act on them at once (archive,
reassign, change status)."

**What a good agent does:** Adds selection as a first-class state, select one, select
all, partial/indeterminate, none. A contextual action bar appears only with a
selection, announces the count, and exposes destructive actions safely (confirm,
undo). Keyboard-selectable; selection survives sort.

**Failure modes:** Checkbox UI with no selected-count, no select-all/indeterminate, no
empty-selection state; destructive bulk action with no confirm/undo; mouse-only
selection.

**Measured:** required-state completeness (selection/partial/empty), usability,
keyboard support, consistency with the Round-1 system.

---

## Round 3, Client portal mode

**Prompt:** "Same data needs a read-only client-facing portal view."

**What a good agent does:** Reuses the system but adapts to a different audience and
permission model, read-only, reduced columns, no internal fields, clear
permission-denied and empty states. Differentiation comes from the audience's real
needs, not arbitrary restyling.

**Failure modes:** Fork that duplicates and diverges the codebase; internal-only data
leaking into the client view; a wholly different visual language that abandons product
identity; no permission-denied state.

**Measured:** preserving product identity, framework adaptation, state completeness
(permission-denied), consistency.

---

## Round 4, Dark mode

**Prompt:** "Support dark mode."

**What a good agent does:** Implements theming through the existing tokens (semantic
colour roles), not hand-edited per-component colours. Verifies contrast in both themes,
respects `prefers-color-scheme`, keeps status colours meaningful in both.

**Failure modes:** Hard-coded dark values scattered through components; broken contrast
on status/badges; an inverted theme that loses the product's identity; tokens forked
instead of extended.

**Measured:** coherence, dependency/system discipline, accessibility (contrast),
preserving product identity.

---

## Round 5, Change the status model

**Prompt:** "Status is changing from three states to a seven-state workflow with
transitions."

**What a good agent does:** Updates the status model in one place and lets it propagate, list badges, filters, bulk actions, portal view all reflect the new model. Detects
and flags everywhere the old model was assumed. Records the change as a decision.

**Failure modes:** New statuses added in the list but old three-state assumptions left
in filters/bulk/portal, the first real **drift**; colours reused ambiguously across
seven states; transitions not represented.

**Measured:** coherence after modification, drift detection, consistency, decision
explanation.

---

## Round 6, Accessibility requirements

**Prompt:** "This now has to meet accessibility requirements: keyboard, screen readers,
200% zoom, reduced motion."

**What a good agent does:** Audits and fixes, full keyboard paths, visible focus,
correct roles/labels, `aria-live` for async and bulk-action results, focus management
in any overlay, usable layout at 200% zoom, `prefers-reduced-motion` fallbacks. Treats
this as completing existing work, not bolting on a plugin.

**Failure modes:** An accessibility overlay widget instead of real fixes; focus traps;
labels missing on icon buttons; zoom breaking the layout; motion with no reduced
fallback.

**Measured:** keyboard/AT support, 200% zoom, reduced motion, required-state
completeness.

---

## Round 7, Support 1,000 records

**Prompt:** "Teams now have up to 1,000 projects; the list must stay fast."

**What a good agent does:** Introduces virtualisation/windowing or sensible pagination
so render cost is bounded; preserves keyboard nav, selection and AT semantics under
virtualisation; states a performance budget; avoids decorative motion that scales with
row count.

**Failure modes:** Rendering all 1,000 rows; virtualisation that breaks select-all,
keyboard nav or screen-reader row counts; adding infinite decorative animation that
makes the now-heavy list janky.

**Measured:** performance budgets, scale handling, accessibility preserved under
virtualisation, effect rejection.

---

## Round 8, Remove an animation dependency

**Prompt:** "Drop the third-party animation library we pulled in earlier; we're
trimming dependencies."

**What a good agent does:** Identifies what the library was doing, reproduces the
essential motion with native CSS/Web Animations (still reduced-motion aware), removes
the dependency cleanly, and confirms nothing regressed. Records the dependency removal.

**Failure modes:** Leaving dead imports; replacing one heavy library with another;
losing reduced-motion handling in the rewrite; breaking effects elsewhere that quietly
depended on it.

**Measured:** dependency discipline, framework adaptation, reduced motion preserved,
coherence.

---

## Round 9, Brand redesign

**Prompt:** "The company rebranded, new colours, type and tone. Apply it."

**What a good agent does:** Applies the new brand through the token layer so the change
is systemic and coherent across list, portal, dark mode and all states. Evolves the
product's identity rather than erasing what makes it recognisable; verifies contrast
and accessibility survive the new palette.

**Failure modes:** A one-screen reskin that leaves the portal/dark-mode/edge states on
the old brand (drift); a redesign that breaks contrast or identity; per-component colour
edits instead of token changes.

**Measured:** preserving product identity, coherence across surfaces, accessibility
(contrast), consistency.

---

## Round 10, Audit interface debt

**Prompt:** "Audit the interface debt accumulated over these rounds and report it."

**What a good agent does:** Produces an honest audit, duplicated components, divergent
patterns, missing states, dependency growth, accessibility gaps, places where the
status/brand changes left residue. Tracks provenance of sourced techniques. Proposes a
prioritised remediation path. Demonstrates that debt stayed bounded and known, not
hidden.

**Failure modes:** "Looks great, no debt"; an audit that misses the drift introduced in
Rounds 5 and 9; no provenance for sourced effects; no remediation plan.

**Measured:** coherence after repeated modifications, decision explanation, provenance,
maintainability, dependency growth.

---

## Trajectory metrics (scored across all ten rounds)

- **Correctness**, each round does what was asked.
- **Usability**, tasks stay fast and clear as features accrue.
- **Accessibility**, keyboard/AT/zoom/reduced-motion hold from Round 6 onward and are
  never regressed by later rounds.
- **Performance**, budgets defined in Round 7 are respected in Rounds 8-10.
- **State completeness**, the full state set is maintained, not eroded, as surfaces
  multiply.
- **Consistency / coherence**, one system, not a patchwork, after ten edits.
- **Drift**, old assumptions (status model, brand) do not survive in forgotten
  corners.
- **Debt**, interface debt stays bounded, named and remediable.
- **Dependency growth**, dependencies are justified and trend toward fewer, not more.
- **Provenance**, sourced techniques carry recorded origin and licence status.
- **Maintainability**, a new engineer could extend the result without fighting it.
