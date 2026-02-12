# Code App Builder — Styling Guide

Fluent Design System-inspired CSS template for Power Apps Code Apps.

Use this as the starting point for `App.css`. Adjust the `--color-primary` variable to match the customer's brand if known.

## CSS Variables

```css
:root {
  --color-primary: #0078d4;        /* Microsoft blue — change for customer brand */
  --color-primary-dark: #005a9e;
  --color-success: #107c10;
  --color-warning: #ff8c00;
  --color-danger: #d13438;
  --color-neutral-bg: #f3f2f1;
  --color-neutral-border: #e1dfdd;
  --color-text: #323130;
  --color-text-secondary: #605e5c;
  --radius: 6px;
  --shadow-card: 0 1.6px 3.6px rgba(0, 0, 0, 0.13),
    0 0.3px 0.9px rgba(0, 0, 0, 0.1);
}
```

## Full Template

Copy this entire block as the starting `App.css`:

```css
/* ── Reset & Base ───────────────────────────────────────── */
*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

:root {
  --color-primary: #0078d4;
  --color-primary-dark: #005a9e;
  --color-success: #107c10;
  --color-warning: #ff8c00;
  --color-danger: #d13438;
  --color-neutral-bg: #f3f2f1;
  --color-neutral-border: #e1dfdd;
  --color-text: #323130;
  --color-text-secondary: #605e5c;
  --radius: 6px;
  --shadow-card: 0 1.6px 3.6px rgba(0, 0, 0, 0.13),
    0 0.3px 0.9px rgba(0, 0, 0, 0.1);
}

html {
  font-size: 14px;
}

body {
  font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Oxygen,
    Ubuntu, Cantarell, 'Helvetica Neue', sans-serif;
  color: var(--color-text);
  background: var(--color-neutral-bg);
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

/* ── App Shell ──────────────────────────────────────────── */
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* ── Screen Containers ──────────────────────────────────── */
.screen {
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 24px 20px;
}

.screen-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 12px;
}

.screen-header h1 {
  font-size: 1.75rem;
  font-weight: 600;
}

/* ── Buttons ────────────────────────────────────────────── */
button,
.btn {
  cursor: pointer;
  border: none;
  border-radius: var(--radius);
  padding: 8px 16px;
  font-size: 0.9rem;
  font-weight: 600;
  transition: background-color 0.15s ease, box-shadow 0.15s ease;
}

.btn-primary {
  background: var(--color-primary);
  color: #fff;
}
.btn-primary:hover {
  background: var(--color-primary-dark);
}

.btn-success {
  background: var(--color-success);
  color: #fff;
}
.btn-success:hover {
  background: #0b5e0b;
}

.btn-danger {
  background: var(--color-danger);
  color: #fff;
}
.btn-danger:hover {
  background: #a4262c;
}

.btn-outline {
  background: transparent;
  border: 1px solid var(--color-neutral-border);
  color: var(--color-text);
}
.btn-outline:hover {
  background: var(--color-neutral-bg);
}

.btn-sm {
  padding: 4px 10px;
  font-size: 0.8rem;
}

/* ── Cards ──────────────────────────────────────────────── */
.card {
  background: #fff;
  border-radius: var(--radius);
  box-shadow: var(--shadow-card);
  padding: 16px;
}

/* ── Summary Row ────────────────────────────────────────── */
.summary-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 12px;
  margin-bottom: 20px;
}

/* ── Filter Bar ─────────────────────────────────────────── */
.filter-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: flex-end;
  padding: 12px 16px;
  background: #fff;
  border-radius: var(--radius);
  box-shadow: var(--shadow-card);
  margin-bottom: 16px;
}

.filter-bar label {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--color-text-secondary);
}

.filter-bar select,
.filter-bar input[type='text'] {
  padding: 6px 10px;
  border: 1px solid var(--color-neutral-border);
  border-radius: var(--radius);
  font-size: 0.85rem;
}

.filter-bar .checkbox-label {
  flex-direction: row;
  align-items: center;
  gap: 6px;
  padding-bottom: 6px;
}

/* ── List Items ─────────────────────────────────────────── */
.asset-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.asset-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 14px 16px;
  background: #fff;
  border-radius: var(--radius);
  box-shadow: var(--shadow-card);
  cursor: pointer;
  transition: box-shadow 0.15s ease;
}
.asset-card:hover {
  box-shadow: 0 3.2px 7.2px rgba(0, 0, 0, 0.18),
    0 0.6px 1.8px rgba(0, 0, 0, 0.11);
}

.asset-card .asset-id {
  font-weight: 700;
  font-family: 'Cascadia Code', 'Consolas', monospace;
  min-width: 110px;
}

.asset-card .asset-desc {
  flex: 1;
  color: var(--color-text-secondary);
}

/* ── Badges ─────────────────────────────────────────────── */
.badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
}

.badge-success {
  background: #dff6dd;
  color: #107c10;
}
.badge-warning {
  background: #fff4ce;
  color: #835c00;
}
.badge-danger {
  background: #fde7e9;
  color: #a4262c;
}
.badge-info {
  background: #e0f0ff;
  color: #004578;
}
.badge-neutral {
  background: #edebe9;
  color: #605e5c;
}

/* ── Split Layout (e.g., Approval Queue) ────────────────── */
.approval-layout {
  display: grid;
  grid-template-columns: 360px 1fr;
  gap: 16px;
  min-height: 60vh;
}

.approval-queue {
  display: flex;
  flex-direction: column;
  gap: 8px;
  overflow-y: auto;
  max-height: 70vh;
}

.approval-item {
  padding: 12px;
  background: #fff;
  border-radius: var(--radius);
  box-shadow: var(--shadow-card);
  cursor: pointer;
  border-left: 4px solid transparent;
  transition: border-color 0.15s;
}

.approval-item.selected {
  border-left-color: var(--color-primary);
  background: #f0f6ff;
}

.approval-item.urgent {
  border-left-color: var(--color-danger);
}

.approval-detail {
  background: #fff;
  border-radius: var(--radius);
  box-shadow: var(--shadow-card);
  padding: 24px;
}

/* ── Form ───────────────────────────────────────────────── */
.form-section {
  margin-bottom: 24px;
}

.form-section h2 {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 12px;
  border-bottom: 2px solid var(--color-primary);
  padding-bottom: 4px;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--color-text-secondary);
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 8px 10px;
  border: 1px solid var(--color-neutral-border);
  border-radius: var(--radius);
  font-size: 0.9rem;
  font-family: inherit;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 1px var(--color-primary);
}

.form-group .error {
  font-size: 0.78rem;
  color: var(--color-danger);
}

.form-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 20px;
}

/* ── Modal / Dialog ─────────────────────────────────────── */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: #fff;
  border-radius: var(--radius);
  padding: 24px;
  width: 100%;
  max-width: 440px;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.25);
}

.modal h3 {
  margin-bottom: 12px;
}

.modal textarea {
  width: 100%;
  min-height: 80px;
  padding: 8px;
  border: 1px solid var(--color-neutral-border);
  border-radius: var(--radius);
  font-family: inherit;
  font-size: 0.9rem;
  margin-bottom: 12px;
}

.modal-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

/* ── Empty State ────────────────────────────────────────── */
.empty-state {
  text-align: center;
  padding: 48px 24px;
  color: var(--color-text-secondary);
}

.empty-state p {
  font-size: 1rem;
}

/* ── Loading ────────────────────────────────────────────── */
.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px;
  color: var(--color-text-secondary);
}

/* ── Utilities ──────────────────────────────────────────── */
.text-secondary {
  color: var(--color-text-secondary);
}

.mt-1 { margin-top: 4px; }
.mt-2 { margin-top: 8px; }
.mt-3 { margin-top: 12px; }
.mb-2 { margin-bottom: 8px; }
.gap-row {
  display: flex;
  gap: 8px;
  align-items: center;
}

/* ── CUI Banner ─────────────────────────────────────────── */
.cui-banner {
  background: #fff4ce;
  color: #835c00;
  text-align: center;
  padding: 4px 12px;
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.5px;
}
```

## Customization Notes

- **Customer branding**: Change `--color-primary` and `--color-primary-dark` to match customer brand colors
- **CUI banner**: Include only if the app handles CUI-marked data
- **Approval layout**: The split-pane layout (`approval-layout`) is ideal for list+detail patterns
- **Forms**: Two-column grid with responsive behavior. Use `.full-width` for wide fields like textareas
- **Badges**: Five semantic variants (success, warning, danger, info, neutral) cover most status indicators
