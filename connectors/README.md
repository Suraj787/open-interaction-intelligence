# Connectors

A connector is a **read-only metadata + retrieval definition** for one source (or a
strict generic GitHub fallback). Connectors describe *where* official material lives
and *what may be done with it*. They do not contain scrapers that execute code.

In this offline-by-default build, connectors are declarative (`connector.yml`). The
network retrieval step is only performed through the explicit `source refresh`
workflow against an allowlisted host (`security/domain-policy.yml`), and everything
retrieved goes to `.motif/quarantine/` for static review, it is never executed.

## A connector MAY

- read public metadata;
- discover public component/effect pages;
- retrieve code **only** from approved official locations;
- identify the official package/registry installation method;
- collect licence and attribution information;
- store retrieved material in quarantine (pinned version + SHA-256).

## A connector MUST NOT

- execute downloaded code or run install/lifecycle scripts;
- modify a target project;
- follow unknown domains or redirects;
- access local secrets, SSH keys or GitHub credentials;
- download or open arbitrary binaries.

## Operating modes

1. **Catalogue-only**, metadata + references only; no source retrieval.
2. **Review**, retrieve untrusted text into disposable quarantine for static review.
3. **Approved installation**, only approved registry entries may be applied to a
   target project, through a controlled patch with snapshot + rollback.

Default runtime mode: **offline approved registry**.

## Layout

```
connectors/
├── generic-github/        # strict official-GitHub fallback (tags/releases only)
└── source-specific/
    ├── react-bits/
    ├── magic-ui/
    ├── aceternity-ui/
    ├── motion-primitives/
    └── uiverse/
```
