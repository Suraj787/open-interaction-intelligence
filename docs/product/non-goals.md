# Non-Goals — Interface Intelligence OS

Defining what IIOS **is not** is as important as defining what it is. These boundaries keep
the project honest and focused, and they prevent it from being mistaken for the simpler
things it is often confused with.

---

## IIOS is *not merely*…

- **…an animation bundle.** It does not ship a pile of motion to sprinkle on a page. It
  decides whether motion is warranted at all, and refuses motion that hurts usability,
  accessibility, or performance.
- **…a list of effect websites.** Galleries (Awwwards, Codrops, SiteInspire, …) are
  treated as `reference-only` inspiration, never as automatically reusable code.
- **…a prompt that adds "nice" UI.** It is a reasoning and governance system with
  deterministic tooling, schemas, and a decision ledger — not a single clever prompt.
- **…a component library.** It does not compete with Radix, shadcn/ui, or a design system;
  it reasons *over* such foundations and emits own-your-source implementations.
- **…a single design system.** It is design-system-neutral and can conform output to
  *yours* (via DTCG tokens) rather than imposing one.
- **…a UI generator.** It does not aim to be the fastest prompt→screenshot tool; it is the
  judgment, completeness, assurance, and governance layer *around* generation. It happily
  cooperates with generators (v0, Stitch, Figma Make) rather than replacing them.
- **…an accessibility scanner.** It uses axe-core-class scanning, but accessibility is one
  enforced dimension within a larger system, and IIOS is honest that automated checks cover
  only part of the problem.
- **…a test runner.** It uses Playwright/Storybook patterns for execution; it supplies the
  *what to assert*, not a new runner.
- **…a closed or hosted-only product.** The core is open-source (MIT), self-hostable, and
  dependency-free.

---

## Things IIOS deliberately does **not** try to do

1. **Guarantee third-party code is safe.** It reduces supply-chain risk substantially but
   cannot eliminate it. **Human review remains required.**
2. **Claim full WCAG compliance from automation.** Automated checks catch only part of
   accessibility issues; IIOS reports coverage honestly and flags the rest for humans.
3. **Replace human designers or reviewers.** It augments judgment and enforces floors; it
   does not make taste, brand, or product strategy decisions for the team.
4. **Bundle licence-encumbered code to look complete.** Unknown/restricted licences become
   `reference-only`; IIOS would rather re-implement a concept than ship a violation.
5. **Maximise source count.** It rejects "thousands of sources" theatre in favour of a
   small verified core plus a catalogued candidate set (see
   [research methodology](../research/research-methodology.md)).
6. **Pursue maximal visual flash.** Least-complexity-that-works beats impressiveness;
   gratuitous effects are a non-goal, not a feature.
7. **Lock users to one framework.** Browser-native, Vue, Frappe-Vue, React, and Svelte are
   all first-class; React-only is a non-goal.
8. **Depend on heavyweight runtime infrastructure.** The core uses only the standard
   library so it runs and can be audited anywhere.
9. **Ship features it can't stand behind.** Anything not responsibly completed is marked
   experimental or planned — never claimed as implemented. Inflating maturity is a non-goal.

---

## Out of scope (for now)

- Native mobile (iOS/Android) UI generation — web and web-app first.
- Visual design *rendering* (it is not a canvas/editor); it reasons and emits code/specs.
- Hosting, billing, or a SaaS control plane — IIOS is the open layer, not a service.

These may be revisited on the [roadmap](./roadmap.md), but they are explicitly not promised.
