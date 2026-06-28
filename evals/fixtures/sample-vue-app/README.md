# sample-vue-app

A small **Motif fixture app** used for static runtime inspection (routes, components,
design tokens, and findings). It mimics a tiny Vue 3 + Vite + Tailwind enterprise
dashboard so detectors have realistic structure to parse.

This is a **fixture, not a production app**. It is not built, installed, or run, it
exists only to be inspected statically by Motif's v3 runtime/twin/findings pipeline.

## Structure

- `src/router.js`, vue-router routes (`/`, `/projects`, `/projects/:id`, `/settings`)
- `src/components/`, list, detail, status, settings, nav, and two modal variants
- `tailwind.config.js` / `src/styles.css`, design tokens (theme colors + CSS variables)
