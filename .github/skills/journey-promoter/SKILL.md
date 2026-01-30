---
name: journey-promoter
description: Promotes single engagements to customer journeys when follow-up sessions are confirmed. Renames folders, migrates metadata, creates session logs, and captures summaries via WorkIQ. Use when user says "promote to journey", "convert to journey", or mentions transitioning an engagement to ongoing customer work.
---

# Journey Promoter

Promotes single-date engagements to customer journeys with session tracking, milestones, and WorkIQ integration.

## Quick Start

**Basic:**
```
"promote Keller to journey"
"convert Booz Allen to customer journey"
```

**With context:**
```
"promote [Customer] to journey - follow-up scheduled for [Date]"
"[Customer] is now a journey, next session [Date]"
```

## When to Use

Use this skill when:
- A follow-up session has been confirmed after an initial engagement
- Customer relationship is transitioning from one-off to ongoing
- You need to track multiple sessions under one customer folder

## What It Does

1. **Renames folder** from date-based to journey-based naming
   - Before: `Keller-Group-PLC-2026-01-29`
   - After: `Keller-Group-PLC-2026-Customer-Journey`

2. **Migrates metadata** to journey schema
   - Preserves all existing engagement fields
   - Adds `sessions[]` array with completed session(s)
   - Adds `milestones[]` from follow-up info
   - Adds `journey_health` tracking

3. **Creates session log** tracking all engagements
   - Date, type, status, outcomes, action items
   - Links to session summary files

4. **Captures session summary** via WorkIQ
   - Queries recent meetings for the customer
   - Auto-generates summary if not already created

5. **Updates README** to journey format
   - Journey overview instead of single engagement
   - Sessions timeline with links
   - Current status and next milestone

## Workflow Checklist

```
- [ ] Find engagement folder matching customer name
- [ ] Confirm folder and new journey name with user
- [ ] Query WorkIQ for recent session data (if available)
- [ ] Rename folder to journey format
- [ ] Migrate metadata to journey schema
- [ ] Create/update sessions log
- [ ] Add milestones from follow-up session
- [ ] Update README to journey format
- [ ] Create session summary file (if not exists)
- [ ] Display journey status confirmation
```

## Output Structure

```
C:\Users\brecol\OneDrive - Microsoft\Engagements\[Customer]-[Year]-Customer-Journey/
├── engagement_metadata.json    (migrated to journey schema)
├── README.md                   (updated to journey format)
├── engagement_summary_[date].md (session summaries)
├── [existing files preserved]
└── [future session files]
```

## Configuration

Uses same config as engagement-initiator:

**Configuration File**: `config.json` (root of workspace)

```json
{
  "engagements_base_path": "C:\\Users\\<username>\\OneDrive - Microsoft\\Engagements"
}
```

## Journey Schema

The promoted metadata includes:

```json
{
  "journey_status": "active",
  "promoted_to_journey": "2026-01-29",
  
  "sessions": [
    {
      "date": "2026-01-29",
      "type": "Agentic Envisioning",
      "status": "completed",
      "summary_file": "engagement_summary_2026-01-29.md",
      "key_outcomes": ["Prototype approach agreed"],
      "action_items_count": 6
    }
  ],
  
  "milestones": [
    {"name": "Initial Envisioning", "date": "2026-01-29", "status": "completed"},
    {"name": "Prototype Session", "date": "2026-02-10", "status": "scheduled"}
  ],
  
  "journey_health": {
    "momentum": "strong",
    "last_customer_contact": "2026-01-29",
    "open_action_items": 6,
    "blockers": []
  }
}
```

## Status Display

After promotion:
```
✅ Promoted to journey: Keller-Group-PLC-2026-Customer-Journey

📊 Journey Status: Active
📅 Sessions: 1 completed, 1 scheduled
🎯 Next Milestone: Prototype Session (Feb 10, 2026)

Sessions Log:
1. ✅ Jan 29 - Agentic Envisioning (completed)
2. 📅 Feb 10 - Rapid Prototype Session (scheduled)

📋 Open Action Items: 6
```

## Related Skills

- **engagement-initiator**: Creates initial engagement folder (use first)
- **agenda-builder**: Builds agendas for sessions
- **task-generator**: Generates task timelines

## Reference

See [references/implementation.md](references/implementation.md) for technical details.
See [references/journey_readme_template.md](references/journey_readme_template.md) for README format.
