---
name: code-app-builder
description: Scaffolds Power Apps Code Apps with React, Vite, and TypeScript. Creates complete project structure with mock Dataverse services, screens, and components. Can also update schema from real OData JSON. Use when user says "create code app", "new code app demo", "scaffold power apps code app", "build a code app", "code app for [customer]", or mentions Power Apps Code Apps SDK.
---

# Code App Builder

Scaffolds Power Apps Code Apps using the **real SDK** (`@microsoft/power-apps`). AI analyzes requirements → creates React+Vite project with mock Dataverse layer → deploys via PAC CLI.

⚠️ Before generating any code, read [references/pitfalls.md](references/pitfalls.md) for critical gotchas (fictional packages, deployment failures, schema surprises).

## Quick Start

```
"Create a code app for [Customer] that tracks [domain]"
"Here's the OData JSON from my Dataverse table, update the schema"
```

## Official Documentation

When in doubt, **fetch these URLs** rather than relying on training data:

| Resource | URL |
|---|---|
| Code Apps docs hub | https://learn.microsoft.com/en-us/power-apps/developer/code-apps/ |
| Quickstart: Create an app | https://learn.microsoft.com/en-us/power-apps/developer/code-apps/how-to/create-an-app-from-scratch |
| Connect to Dataverse | https://learn.microsoft.com/en-us/power-apps/developer/code-apps/how-to/connect-to-dataverse |
| Architecture | https://learn.microsoft.com/en-us/power-apps/developer/code-apps/architecture |
| ALM (lifecycle mgmt) | https://learn.microsoft.com/en-us/power-apps/developer/code-apps/how-to/alm |
| Troubleshoot data sources | https://learn.microsoft.com/en-us/power-apps/developer/code-apps/troubleshoot-add-datasource |
| GitHub repo (samples/templates) | https://github.com/microsoft/PowerAppsCodeApps |
| npm: `@microsoft/power-apps` | https://www.npmjs.com/package/@microsoft/power-apps |
| npm: `@microsoft/power-apps-vite` | https://www.npmjs.com/package/@microsoft/power-apps-vite |
| PAC CLI reference | https://learn.microsoft.com/en-us/power-platform/developer/cli/introduction |

## Workflow

```
- [ ] Gather requirements (customer, domain, key entities, Dataverse table/prefix)
- [ ] Create project folder: C:\Projects\demos\[Customer]-[Date]\[AppName]\
- [ ] Scaffold config files (Step 1 templates below)
- [ ] Create data layer: model → generated service → types → service wrapper
- [ ] Build screens, components, App.tsx, App.css
- [ ] npm install && npm run build (must succeed with 0 errors)
- [ ] ⚠️ CHECKPOINT: Show user the running app via npm run dev
- [ ] Deploy (see references/implementation.md for PAC CLI workflow)
```

## Step 1: Project Scaffold

Create these files exactly as shown. See [references/pitfalls.md](references/pitfalls.md) for why specific choices (like `base: './'` and `HashRouter`) are mandatory.

### package.json

```json
{
  "name": "[app-name-kebab-case]",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "description": "Power Apps Code App for [Description] — [Customer] Demo",
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "lint": "eslint .",
    "preview": "vite preview"
  },
  "dependencies": {
    "@microsoft/power-apps": "^1.0.3",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "react-router-dom": "^7.1.0"
  },
  "devDependencies": {
    "@eslint/js": "^9.18.0",
    "@microsoft/power-apps-vite": "^1.0.2",
    "@types/node": "^22.12.0",
    "@types/react": "^19.0.8",
    "@types/react-dom": "^19.0.3",
    "@vitejs/plugin-react": "^4.3.4",
    "eslint": "^9.18.0",
    "eslint-plugin-react-hooks": "^5.1.0",
    "eslint-plugin-react-refresh": "^0.4.18",
    "globals": "^15.14.0",
    "typescript": "~5.7.3",
    "typescript-eslint": "^8.22.0",
    "vite": "^6.1.0"
  },
  "engines": { "node": ">=18.0.0" }
}
```

### vite.config.ts

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { powerApps } from '@microsoft/power-apps-vite'; // Named import, NOT default

export default defineConfig({
  base: './',  // Required — absolute paths 404 on Power Platform
  plugins: [react(), powerApps()],
});
```

### main.tsx

```tsx
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { HashRouter } from 'react-router-dom'; // NOT BrowserRouter — breaks in iframe

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <HashRouter><App /></HashRouter>
  </StrictMode>,
);
```

### index.html

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>[App Title] — [Customer]</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

### tsconfig.json

```json
{ "files": [], "references": [{ "path": "./tsconfig.app.json" }, { "path": "./tsconfig.node.json" }] }
```

### tsconfig.app.json

```jsonc
{
  "compilerOptions": {
    "tsBuildInfoFile": "./node_modules/.tmp/tsconfig.app.tsbuildinfo",
    "target": "ES2022", "lib": ["ES2023", "DOM", "DOM.Iterable"], "module": "ESNext",
    "skipLibCheck": true, "moduleResolution": "bundler", "allowImportingTsExtensions": true,
    "isolatedModules": true, "moduleDetection": "force", "noEmit": true, "jsx": "react-jsx",
    "strict": true, "noUnusedLocals": true, "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true, "noUncheckedSideEffectImports": true
  },
  "include": ["src"]
}
```

### tsconfig.node.json

```jsonc
{
  "compilerOptions": {
    "tsBuildInfoFile": "./node_modules/.tmp/tsconfig.node.tsbuildinfo",
    "target": "ES2022", "lib": ["ES2023"], "module": "ESNext",
    "skipLibCheck": true, "moduleResolution": "bundler", "allowImportingTsExtensions": true,
    "isolatedModules": true, "moduleDetection": "force", "noEmit": true,
    "strict": true, "noUnusedLocals": true, "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true, "noUncheckedSideEffectImports": true
  },
  "include": ["vite.config.ts"]
}
```

### .gitignore

```
node_modules/
dist/
*.tsbuildinfo
.vite/
```

## Step 2: Data Layer

See [references/implementation.md](references/implementation.md) for architecture diagram and data flow.

Every entity needs **four files** — two in `src/generated/` (disposable, replaced by `pac code add-data-source`) and two in `src/` (persistent app logic):

| File | Location | Role |
|------|----------|------|
| Model | `src/generated/models/[Entity]Model.ts` | TypeScript interface matching Dataverse table columns |
| Generated Service | `src/generated/services/[Entity]Service.ts` | Mock CRUD with OData `$filter`/`$orderby`/`$top` support |
| Types | `src/types/[Entity].ts` | App-level types, choice mappings (`Record<number, string>`), validation rules |
| Service Wrapper | `src/services/[Entity]Service.ts` | `toApp()`/`toDataverse()` mapping, business logic |

**Model conventions**: prefix matches environment (`bac_`, `cr_`, etc.), choices are `number`, dates are `string` (ISO), nullable fields are `string | null`, PK is `[prefix]_[tablename]id`.

**Mock service**: Use `Map<string, Entity>` storage. OData filter regex must use `([^\s]+)` for field names, not `\w+`. Load real OData records as mock data when available.

## Step 3: UI Layer

- **Screens** = full-page views with state. **Components** = stateless props-driven UI.
- No component libraries — vanilla CSS with Fluent-inspired styling. See [references/styling-guide.md](references/styling-guide.md).
- Detail views: use inline expand/collapse, not route navigation (avoids iframe issues).
- App.tsx uses `Routes` / `Route` / `Navigate` from `react-router-dom`.

## Step 4: Build, Verify, Deploy

```bash
npm install && npm run build   # Must succeed with 0 errors
npm run dev                    # Show user the app at localhost:5173
```

For deployment workflow (`pac code init` → `pac code push`), see [references/implementation.md](references/implementation.md).

For troubleshooting blank screens, 404s, or admin errors, see [references/pitfalls.md](references/pitfalls.md).

## Schema Update from OData JSON

When user provides real OData JSON from their environment:

1. Identify column prefix and table name from `@odata.context` URL
2. Map each field (type, nullable, choice values, sentinel values)
3. Update all 4 data layer files + any affected UI components
4. See "Schema Issues" in [references/pitfalls.md](references/pitfalls.md) for common surprises

## Reference Files

- [references/implementation.md](references/implementation.md) — Architecture, data flow, deploy workflow
- [references/styling-guide.md](references/styling-guide.md) — Full App.css template
- [references/pitfalls.md](references/pitfalls.md) — All known gotchas with solutions
