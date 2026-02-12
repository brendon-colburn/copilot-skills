# Code App Builder — Implementation Guide

## Architecture

```
┌──────────────────────────────────────────────────────┐
│                  React App (Vite)                      │
│  ┌──────────┐  ┌──────────┐  ┌─────────────────────┐ │
│  │ Screens  │→ │Components│  │      App.css         │ │
│  └────┬─────┘  └──────────┘  └─────────────────────┘ │
│       │                                                │
│  ┌────▼────────────────────────────────────────────┐  │
│  │        Service Wrapper (src/services/)           │  │
│  │  toApp(): Dataverse → app types                  │  │
│  │  toDataverse(): app → Dataverse types            │  │
│  │  Business logic (summaries, filters)             │  │
│  └────┬────────────────────────────────────────────┘  │
│       │                                                │
│  ┌────▼────────────────────────────────────────────┐  │
│  │       Generated Layer (src/generated/)           │  │
│  │  Model: TypeScript interface for Dataverse table │  │
│  │  Service: CRUD + OData-style filtering           │  │
│  │  ⚠️ Replaced by pac code add-data-source later  │  │
│  └─────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────┘
```

**Data flow**: Screen → service wrapper → generated service → mock data (or real Dataverse via SDK). The service wrapper maps `toApp()` on every record: choice integers become display strings, ISO datetimes become date-only strings.

## Why Four Files Per Entity

The `src/generated/` layer is **disposable** — `pac code add-data-source` overwrites it with real Dataverse bindings. The `src/types/` and `src/services/` layers **persist** because they contain app-specific logic (choice labels, validation, business rules). This separation means switching from mock to real data only changes the generated layer; the rest of the app is untouched.

## Deploy Workflow

### Prerequisites

1. PAC CLI: `winget install Microsoft.PowerAppsCLI`
2. Auth: `pac auth create --environment https://[org].crm.dynamics.com/`
3. Admin toggle: Power Platform admin center → Settings → Features → enable Code Apps (may take 5-10 min to propagate)

### Commands

```bash
pac code init --environment [id] --displayName "[Name]"     # Creates power.config.json
pac code add-data-source -a dataverse -t [table_name]        # Optional: replaces mock generated/
npm run build                                                 # Produces dist/ with relative paths
pac code push                                                 # Uploads to Power Platform
```

`pac code init` must run before `pac code add-data-source` — it creates the `power.config.json` that the other commands depend on.
