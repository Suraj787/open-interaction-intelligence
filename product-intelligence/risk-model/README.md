# Risk Model

The risk model answers: **what is the cost of getting it wrong, and where does that cost
concentrate?** It populates the `risks` array (and informs `constraints`) of the
[Product Context Manifest](../../schemas/product-context.schema.json).

Risk is what tells interaction design where to *spend* friction. A conversion-critical
checkout removes friction; a safety-critical administration *adds* deliberate friction at
the dangerous step. Both are correct because their risk profiles differ.

## Categories to consider

- **Safety / harm** — can a wrong action hurt a person? (medication administration)
- **Permission / authorization** — can someone act beyond their authority, or on the wrong
  record? Enforced server-side, never merely hidden in the UI.
- **Financial / conversion** — does an error cost a sale or a charge? (checkout)
- **Data integrity** — silent overwrite, double-submit, lost record.
- **Trust / perception** — hidden costs, misleading status, stale data.
- **Resilience** — interruption, connectivity loss, shared-device session bleed.
- **Compliance** — PCI-DSS, HIPAA, GDPR/CCPA consequences of mishandling data.

## How it is built

1. **For each workflow, ask "what is the worst credible outcome of failure here?"** That
   sentence is a risk line.
2. **Rank by severity × likelihood**, but record severity honestly — a rare catastrophic
   risk (wrong-patient dose) outranks a frequent annoyance.
3. **Derive constraints from risks.** A risk states the danger; a constraint states the
   non-negotiable the design must honour. Example:
   - Risk: "A fast bulk replan silently violates capacity or overwrites another manager's
     change."
   - Constraint: "Destructive or wide-reaching edits must be reversible or clearly
     confirmed."
4. **Locate the risk on the friction map.** Low-risk, high-frequency steps → strip
   friction. High-risk steps → add unambiguous confirmation, reversibility, or co-sign.

## How it is validated

- Each material risk traces back to a workflow and forward to a `constraint`.
- Safety- and permission-critical products name those risks explicitly (their absence is a
  defect).
- Constraints are testable by the assurance layer (`assurance/`), not vague aspirations.
- Regulatory risks are consistent with `product.regulatory_sensitivity`.

## Honesty rules

- A risk inferred from domain priors (alert fatigue, mobile abandonment) is an
  **inference** — record the prior, do not present it as measured.
- If the *magnitude* of a risk is unknown (no baseline conversion data, unknown override
  authority), put the unknown in `unresolved`; do not quantify what you have not measured.
- Never downplay a safety or permission risk to make a design look simpler.
