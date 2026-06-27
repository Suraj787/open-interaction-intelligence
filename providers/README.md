# Providers

Interface Intelligence OS treats every source of knowledge as a **provider** that is
normalised into internal schemas and never trusted blindly. Provider declarations live in
`registry/providers/*.json`; each declares identity, version, trust tier, licence, update
method, confidence, and evidence quality, and lists which record kinds it supplies.

Current providers (v0.2.0):

| Provider | Trust | Supplies | Status |
|---|---|---|---|
| `internal-design-intelligence` | 2 | styles, layouts, ux-principles, colour, typography, industry-packs | implemented |
| `internal-interaction-intelligence` | 2 | effects, patterns, recipes, sources, components | implemented |
| `approved-registry` | 2 | components (licence-verified) | implemented |
| `material-design` | 1 | motion tokens, components (reference) | partial |
| `ibm-carbon` | 2 | motion tokens, components (reference) | partial |

External provider results must be cross-checked and re-ranked against internal evidence,
not accepted as-is. Importing external datasets (for example a UI UX Pro Max-style dataset
as one provider, enriched with deeper schemas, validation, project context and governance)
is on the roadmap; the architecture and declaration format exist now.
