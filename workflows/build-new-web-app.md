# Workflow: Build a New Web Application

For **web applications** (task completion, data density, repeated use), ERP, CRM,
dashboards, project management, SaaS tools. Motion here serves clarity and feedback, never
decoration. Vue and Frappe-Vue are first-class targets.

## Preconditions

- Target repo inspected (framework, design system, existing motion conventions).
- Default **offline approved registry** mode.

## Steps

1. **Frame the purpose.** Development purpose = *new web application*; product type
   (enterprise, ERP/CRM, dashboard, project-management, SaaS, dev tool).
   Load `skills/product-context-analysis`.
2. **Identify the user and primary task** per screen. Repeated, high-frequency tasks
   tolerate the least decorative motion.
3. **Map screen types:** list views, data tables, forms, detail/record pages, dashboards,
   empty/loading/error states.
4. **State the interaction objective**, usually feedback, orientation, state transition,
   or progressive disclosure. Load `skills/interaction-design`.
5. **Search patterns first:** `python -m motif search "<problem>"`. Strongly prefer effects
   with `enterprise_suitability: recommended`.
6. **Rank and select** the simplest effective approach (`skills/effect-selection`).
   **Never** run continuous decorative motion behind dense work UIs; never make enterprise
   apps resemble animation showcases.
7. **Implement in the app's framework** (`skills/framework-adaptation`). For Frappe-Vue,
   respect Frappe UI conventions; do not add a second animation engine for one effect.
   Follow the implementation hierarchy.
8. **Accessibility gate:** keyboard-first operation, visible focus, semantics, never rely
   on motion alone for status, reduced-motion path.
9. **Performance gate:** transform/opacity only; budgets respected even with many rows;
   no jank on scroll/virtualised lists.
10. **Responsiveness gate:** breakpoints + input modes; touch targets.
11. **Record decision + provenance**; install approved components via
    `python -m motif component install` (diff + rollback + manifest).
12. **Validate**, see [validate-experience.md](validate-experience.md).

## Done when

Every screen's motion is justified by a real task need, status is never motion-only, the
app does not resemble a showcase, and accessibility/performance/responsiveness pass with
recorded provenance.
