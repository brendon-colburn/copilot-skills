# Code App Builder — Pitfalls & Solutions

All known gotchas from real Code App development. SKILL.md references this file — this is the single source for troubleshooting.

## Fictional Packages

AI models hallucinate these. **None exist on npm**:

- `@microsoft/power-apps-component-framework` → use `@microsoft/power-apps`
- `@microsoft/powerapps-code-app` → use `@microsoft/power-apps`
- `@microsoft/pcf-scripts` / `pcf-scripts` → use `@microsoft/power-apps-vite`
- `@microsoft/power-apps/sdk` → use `@microsoft/power-apps` (flat, no subpath)

## Build Issues

### `Module has no default export` for power-apps-vite
Named import: `import { powerApps } from '@microsoft/power-apps-vite'` — **not** a default export.

## Deployment Issues

### Blank screen — asset 404s (CSS MIME type error, JS not found)
Vite's default `base: '/'` produces absolute asset paths. Power Platform serves apps from nested URLs, so `/assets/...` resolves to the wrong location.
**Fix**: `base: './'` in `vite.config.ts`.

### Routes don't work in deployed app
`BrowserRouter` uses `history.pushState`, which breaks in Power Platform's sandboxed iframe.
**Fix**: Use `HashRouter`.

### `power.config.json not found`
Ran `pac code add-data-source` before `pac code init`.
**Fix**: Run `pac code init --environment [id] --displayName "[Name]"` first.

### "environment does not allow this operation"
Code Apps not enabled in admin center, or still propagating (takes up to 10 min). Developer Plan environments may not support Code Apps at all.

## Runtime Issues

### Click on list item causes flash/redirect loop
Navigating to a route like `/asset/:id` that doesn't exist, triggering the catch-all redirect.
**Fix**: Use inline expand/collapse (`useState<string | null>`) instead of route navigation for detail views.

### OData filter silently fails — no records match
Filter regex uses `\w+` for field names, but OData paths can contain `@` and `.`.
**Fix**: Use `([^\s]+)` instead of `(\w+)` in the filter regex.

### Date fields show full ISO timestamp
Dataverse returns `2026-01-15T05:00:00Z`. **Fix**: `isoString.slice(0, 10)` in the service wrapper's `toApp()`.

## Schema Issues

These arise when real OData JSON differs from assumptions:

- **Column prefix varies** per environment (`bac_`, `cr_`, `new_`). Never assume `cr_`.
- **Choice fields may be plain strings** (e.g., `cuimarking` returning `"CUI//SP-CTI"` instead of an integer).
- **Date fields may contain sentinels** (e.g., `"OVERDUE"` instead of a date). Handle explicitly.
- **Assumed fields may not exist** (e.g., `approvedBy`). Always validate against real OData JSON.

## Console Errors (Ignorable)

These come from the **Power Platform host**, not your app:

- `login.microsoftonline.com/.../token` 400 — Host OAuth refresh. Normal.
- `componentWillReceiveProps` warnings — Power Platform's own React. Not your code.
- `graph.microsoft.com/v1.0/me/photo/$value` 404 — No profile photo. Cosmetic.
- `iframe sandbox` warnings — Expected for Code Apps.
- `ECS - Config fetch complete` — Telemetry. Normal.
- `appExtendedMetadata` 404 — Transient during app load.
