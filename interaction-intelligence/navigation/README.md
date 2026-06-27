# Navigation Guidance

Concise rules for navigation surfaces (top bars, sidebars, tabs, breadcrumbs, command palette, mobile drawers). Pairs with the `navigation` state record in `../states/navigation.json`.

## Orientation: answer "where am I?"
- Always show the current location with a persistent **selected** state and `aria-current="page"` — not colour alone.
- Provide breadcrumbs for any hierarchy deeper than two levels.
- Keep the active section visible even when sub-navigation is open.

## Reachability and keyboard
- Every destination must be reachable by keyboard with a **visible focus** ring (WCAG 2.4.7).
- Follow the platform expectation: Tab through items, Arrow keys within a menu/menubar, Enter/Space to activate, Escape to close.
- Offer a **skip-to-content** link as the first focusable element.

## Predictability
- Navigation order and labels stay stable across the app; do not reorder items contextually.
- A nav action should navigate — avoid hiding destructive or stateful actions inside nav items.
- Indicate when a route change is fetching (`loading`) rather than appearing frozen.

## Responsive behaviour
- Below ~768px or on coarse-pointer devices, collapse to a drawer or bottom bar with **44px** targets.
- Keep the most frequent destinations within thumb reach on tall phone viewports.
- Never hide primary navigation behind a hover-only flyout — provide tap/click equivalents.

## Permissions and availability
- Hide destinations the user cannot access, or show them disabled with an explained reason — never a dead link that 403s.
- Mark destinations that are unavailable offline.

## Motion
- Route transitions follow the active motion grammar and stay short (operational) — no scroll-jacking, no blocking animation, full reduced-motion fallback.

## Command palette (recommended)
- Provide a `Cmd/Ctrl-K` palette for fast navigation and actions in dense apps.
- It augments, never replaces, visible navigation; it is keyboard-first with fuzzy search and recent items.
