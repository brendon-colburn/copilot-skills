---
name: task-generator  
description: Generates engagement task timelines (T-28 to T+3) with business day calculations excluding weekends. Outputs Planner-ready CSV files. Use when generating tasks, creating timelines, or when user mentions task lists, Planner import, or business day calculations.
---

# Task Generator

Generates 15-task timelines with business day calculations.

## Usage

### Initial Engagement (single session)
```bash
python scripts/business_days.py "[Customer]" "YYYY-MM-DD"
```

### Journey Follow-on Session
```bash
python scripts/business_days.py "[Customer]" "YYYY-MM-DD" --followon --label "Session 2 - Topic"
```

### Multiple Journey Sessions at Once
```bash
python scripts/business_days.py "[Customer]" "2026-03-12" "2026-03-31" --followon \
  --labels "Session 2 - Envisioning" "Session 3 - Prototype" \
  --output /path/to/journey/folder
```

## Task Templates

### Initial Engagement (15 tasks, T-28 to T+3)

```
T-28: Schedule Internal Precall
T-22: Research customer
T-21: Execute Internal Precall
T-20: Draft Agenda
T-20: Schedule Customer Precall
T-14: Execute Customer Precall
T-14: Schedule internal resources
T-10: Validate Agenda with ATU
T-7: Validate Agenda with Customer
T-7: Prep Demos
T-3: Confirm all Customer pre-work
T-0: Send Satisfaction Survey
T+2: Conduct MSFT Debrief
T+2: Share Engagement Materials
T+3: Complete Engagement Close out form
```

### Journey Follow-on Session (14 tasks, T-21 to T+3)

Streamlined template for sessions where customer relationship is already
established. Shorter lead time, no research task.

```
T-21: Schedule Internal Session Prep
T-14: Execute Internal Session Prep
T-14: Draft Session Agenda
T-14: Schedule Customer Precall
T-10: Execute Customer Precall
T-10: Schedule internal resources
T-7: Validate Agenda with ATU
T-5: Validate Agenda with Customer
T-5: Prep Demos / Session Materials
T-3: Confirm all Customer pre-work
T-0: Send Satisfaction Survey
T+2: Conduct MSFT Debrief
T+2: Share Session Materials
T+3: Complete Session Close out
```

## Business Day Rules

- Excludes weekends (Saturday/Sunday)
- T-28 = 28 business days BEFORE engagement
- T+2 = 2 business days AFTER engagement

Example (Engagement: Monday, Jan 20, 2026):
- T-28 → Wednesday, Dec 11, 2025
- T+2 → Wednesday, Jan 22, 2026

## CSV Output Format

```csv
Task Name,Assignment,Start date,Due date,Bucket,Progress,Priority,Labels
[Customer] - Draft Agenda,Brendon Colburn,12/23/2025,12/23/2025,2026-01-20 - [Customer],Not started,Medium,Add label
```

Import to Planner: "..." → "Import plan from Excel"

## Journey Task Workflow

When a customer engagement becomes a journey with multiple sessions:

### File Naming Convention
```
[Journey Folder]/
├── tasks.csv                    # Original session 1 tasks (preserved as-is)
├── tasks_2026-03-12.csv         # Session 2 tasks (per-date naming)
├── tasks_2026-03-31.csv         # Session 3 tasks
└── tasks_all_sessions.csv       # Combined CSV for reference
```

### Planner Import Strategy
- Each session gets its own **Bucket** in Planner: `2026-03-12 - Customer - Session Label`
- Import per-session CSVs individually to add new session tasks to existing plan
- Existing session 1 tasks in Planner are not affected by importing session 2+
- The `tasks_all_sessions.csv` can be used for a fresh plan if preferred

### Key Differences from Initial Engagement
| Aspect | Initial | Follow-on |
|--------|---------|-----------|
| Template | 15 tasks (T-28 to T+3) | 14 tasks (T-21 to T+3) |
| Lead time | 28 business days | 21 business days |
| Research task | Included | Omitted (customer known) |
| File name | `tasks.csv` | `tasks_YYYY-MM-DD.csv` |
| Bucket label | `{date} - {customer}` | `{date} - {customer} - {session label}` |

## Timeline Status

Shows current position:
- T-40+: Early (no tasks yet)
- T-28 to T-14: Active planning
- T-14 to T-0: Final prep
- T+1 to T+3: Follow-up
- T+4+: Complete

## Integration

Called by: engagement-initiator  
Standalone: Generate tasks without full engagement setup

## Reference

See [references/power_automate_flow.json](references/power_automate_flow.json) for original automation template.
