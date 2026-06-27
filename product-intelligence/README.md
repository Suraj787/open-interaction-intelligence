# Product Intelligence

Product Intelligence is the layer of **Interface Intelligence OS** that establishes
*what the product is, who uses it, what they are trying to do, where they do it, and
what can go wrong* — **before** any pattern, effect, or pixel is chosen.

Everything downstream (interaction design, effect selection, assurance) is grounded in
the **Product Context Manifest** produced here. If this layer is wrong, every later
decision inherits the error. So this layer is built to be **honest about what it does
not know**.

## The Product Context Manifest

A manifest is a single JSON document conforming to
[`schemas/product-context.schema.json`](../schemas/product-context.schema.json).
Required top-level fields: `version`, `confidence`, `product`, `users`.

It is assembled from six sub-models, each documented in its own guide:

| Sub-model | Guide | Answers |
|-----------|-------|---------|
| Product model | [`product-model/`](product-model/README.md) | What is this and why does it exist? |
| User model | [`user-model/`](user-model/README.md) | Who acts, how expert, how often? |
| Workflows | [`workflows/`](workflows/README.md) | What sequences of action matter? |
| Environment model | [`environment-model/`](environment-model/README.md) | Devices, connectivity, locale. |
| Risk model | [`risk-model/`](risk-model/README.md) | What is the cost of getting it wrong? |
| Confidence model | [`confidence/`](confidence/README.md) | How much of the above is *known* vs *guessed*? |

Worked examples live in [`manifests/`](manifests/):

- `enterprise-project-management.json`
- `healthcare-medication-admin.json`
- `ecommerce-checkout.json`

Each splits its claims across `verified`, `inferred`, `assumptions`, and `unresolved`,
and carries a `confidence` that reflects that split honestly.

## Core principle: the system must not invent certainty

A manifest is only useful if a reader can tell **fact from guess**. Product Intelligence
therefore never promotes an inference to a verified fact, never hides an assumption, and
never reports high confidence to look authoritative. An empty `verified` list with an
honest 0.3 confidence is a *better* manifest than a confident-looking fabrication.

## The `ii` commands

Product Intelligence is exercised through the `ii` CLI surface. The four commands below
form the author → validate → explain loop.

### `ii inspect`

Reads available evidence about a target (a repository, a brief, a URL, telemetry) and
reports what *could* be established and what is missing. It does **not** assert a
manifest; it surfaces signals and gaps so you know how much can be grounded.

```
ii inspect <target>
```

Output: detected product/user/environment signals, and an explicit "insufficient
evidence for…" list that seeds the manifest's `unresolved` array.

### `ii model-product`

Builds (or updates) a Product Context Manifest from the inspected evidence plus any brief
you supply. Every claim it writes is filed into exactly one of `verified` / `inferred` /
`assumptions` / `unresolved`, and it computes an honest `confidence`.

```
ii model-product <target> --out product-intelligence/manifests/<id>.json
```

`<id>` is kebab-case. The command never invents evidence; unsupported claims land in
`assumptions` or `unresolved`, not `verified`.

### `ii product validate`

Validates a manifest against the schema **and** against the honesty rules: required
fields present, `confidence` in `[0,1]`, `audience` within enum, no claim double-filed,
and `confidence` consistent with the verified/inferred/assumption split (see
[`confidence/`](confidence/README.md)).

```
ii product validate product-intelligence/manifests/<id>.json
```

### `ii product explain`

Renders a human-readable account of a manifest: what we know, what we inferred and from
what, what we assumed, what remains unresolved, and the resulting confidence — plus how
those facts will constrain downstream interaction and effect decisions.

```
ii product explain product-intelligence/manifests/<id>.json
```

Use `explain` in review: if a stakeholder disagrees with an `inferred` or `assumptions`
line, that is the cheapest possible place to correct the system.

## Lifecycle

```
ii inspect  →  ii model-product  →  ii product validate  →  ii product explain
   (gather)        (author)             (check honesty)         (review + correct)
```

Re-run the loop whenever new evidence arrives. Promotion of a claim from `inferred` or
`assumptions` to `verified` requires *new evidence*, recorded in `evidence`, never just
increased confidence on the author's part.
