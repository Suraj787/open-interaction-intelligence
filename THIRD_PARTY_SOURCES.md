# Third-Party Sources

Motif catalogues external libraries, design systems and references as **source metadata** in
[`registry/sources/`](registry/sources/). This document summarises that metadata and the
rules that govern it.

> **Cataloguing a source does not imply any right to redistribute it.** A record in
> `registry/sources/` describes a source and our review of it. It is *not* a grant of
> licence and *not* a statement that the source's code or assets may be copied into your
> project.

## How to read this

- **The registry is the source of truth.** This file is a human-readable summary; the
  authoritative, machine-readable records (with `license`, `license_reference`,
  `redistribution`, `trust_tier`, `confidence`, `status` and `evidence`) live in
  `registry/sources/` and are validated against `schemas/source.schema.json`.
- **Licence facts are confidence-rated and must be re-verified online.** Each record
  carries a `confidence` level and a `status` (`verified` / `pending-verification`).
  Licences change; re-verify through `python -m motif source retrieve --refresh` before
  relying on them.
- **Bundling requires a verified permissive licence _and_ trust tier ≥ 3.** See the
  LICENCE GATE and redistribution classes in [`LICENSE_POLICY.md`](LICENSE_POLICY.md).
  Unknown licence ⇒ `reference-only`, never bundled. Source-available / Commons-Clause
  terms are not permissive OSS.

## v0.1.0 sources by redistribution class

22 reviewed sources. Trust tiers shown are 1-5 (lower can be high-quality guidance that is
simply not redistributable, e.g. official design guidelines).

### Redistributable (14), verified permissive OSS or open standards

Concepts may be implemented and original implementations bundled (trust tier ≥ 3 and a
verified licence still required), preserving attribution and notices.

| Source | Licence | Trust tier | Confidence |
|--------|---------|:----------:|:----------:|
| Anime.js | MIT | 2 | medium |
| AutoAnimate | MIT | 2 | medium |
| CSS Scroll-driven Animations | Browser standard (no licence needed) | 1 | high |
| Headless UI | MIT | 2 | medium |
| Lenis | MIT | 3 | medium |
| Web Animations API (MDN) | Browser standard (no licence needed) | 1 | high |
| Motion (Framer Motion) | MIT | 2 | medium |
| Radix UI | MIT | 2 | medium |
| React Aria | Apache-2.0 | 2 | medium |
| Reka UI | MIT | 3 | medium |
| Rough Notation | MIT | 3 | medium |
| shadcn/ui | MIT | 2 | medium |
| Three.js | MIT | 2 | medium |
| tsParticles | MIT | 3 | medium |

### Adaptable-concept (4), learn the concept, write clean-room original code

The licence/terms permit learning from the concept but not wholesale redistribution of the
source's code or assets. Implement from scratch and record provenance; never copy.

| Source | Licence | Trust tier | Confidence | Notes |
|--------|---------|:----------:|:----------:|-------|
| GSAP | GSAP-Standard (now free) | 2 | low | `pending-verification`, re-verify current terms before bundling. |
| IBM Carbon | Apache-2.0 | 2 | medium | Design system; adapt concepts, mind trademark/assets. |
| Magic UI | MIT | 3 | low | Re-verify per-component provenance. |
| React Bits | MIT | 3 | low | Re-verify per-component provenance. |

### Reference-only (4), cite only, never bundle or reconstruct

Unknown, guidance-only, or community/per-element terms. Reference and cite; never copy,
never reconstruct from previews.

| Source | Licence | Trust tier | Confidence | Notes |
|--------|---------|:----------:|:----------:|-------|
| Apple Human Interface Guidelines | Guidance (Apple terms) | 1 | high | Official guidance; not redistributable. |
| Material Design | Guidance (CC-BY / Google terms) | 1 | high | Official guidance; mind asset/trademark terms. |
| Aceternity UI | Unknown / per-component | 4 | low | `pending-verification`, licence unclear per component. |
| Uiverse | MIT (community-submitted; verify per element) | 4 | low | `pending-verification`, verify each element's provenance. |

### Rejected (0)

No source in v0.1.0 is classified `rejected`. A rejected source would be excluded as a
usable source and retained only as a documented rejection. (A rejected **component**
fixture exists in the registry to exercise the rejection path.)

## Verifying for yourself

```bash
python -m motif source completeness          # coverage by source
python -m motif source retrieve --refresh    # re-verify against the allowlisted official host
make check                                 # validate the registry
```

Always confirm the current licence and redistribution class against the official source
before bundling. When in doubt, treat the source as `reference-only`.
