# Journey Promoter - Implementation Guide

## Core Function

Promote single-date engagements to customer journeys when follow-up sessions are confirmed.

## Process Flow

```
User: "promote [Customer] to journey"
                ↓
1. Parse customer name from input
                ↓
2. Search engagements folder for matching customer
   - Glob pattern: *[Customer]*
   - Handle multiple matches (ask user to confirm)
                ↓
3. Validate current state
   - Confirm folder exists
   - Check if already a journey (ends with "Customer-Journey")
   - Verify engagement_metadata.json exists
                ↓
4. Confirm with user
   - Show current folder name
   - Show proposed journey name
   - Ask for confirmation
                ↓
5. Query WorkIQ for session data (optional)
   - Find recent meetings with customer
   - Extract key outcomes, action items
   - Use for session log entry if available
                ↓
6. Rename folder
   - From: {Customer}-{YYYY-MM-DD}
   - To: {Customer}-{Year}-Customer-Journey
                ↓
7. Migrate metadata
   - Read existing engagement_metadata.json
   - Add journey-level fields
   - Preserve all existing fields
   - Write updated metadata
                ↓
8. Update README
   - Load journey README template
   - Populate with journey data
   - Preserve relevant existing content
                ↓
9. Create session summary (if not exists)
   - Check for existing summary file
   - If missing, create from WorkIQ data
                ↓
10. Display confirmation
    - Journey name
    - Sessions count
    - Next milestone
    - Open action items
```

## Folder Naming Convention

### Before (Single Engagement)
```
{Customer}-{YYYY-MM-DD}
Examples:
- Keller-Group-PLC-2026-01-29
- Booz-Allen-Hamilton-2026-01-28
- AstraZeneca-2026-01-20
```

### After (Customer Journey)
```
{Customer}-{Year}-Customer-Journey
Examples:
- Keller-Group-PLC-2026-Customer-Journey
- Booz-Allen-Hamilton-2026-Customer-Journey
- AstraZeneca-2026-Customer-Journey
```

### Edge Cases
- Already a journey: Skip rename, just update metadata
- Multiple years: Use the year of the first engagement
- Name conflicts: Append suffix or ask user

## Journey Metadata Schema

### New Fields (Added During Promotion)

```json
{
  // Journey-level fields
  "journey_status": "active",           // active, on-hold, completed, closed
  "promoted_to_journey": "2026-01-29",  // Date of promotion
  
  // Sessions tracking
  "sessions": [
    {
      "date": "2026-01-29",
      "type": "Agentic Envisioning",
      "status": "completed",            // completed, scheduled, cancelled
      "duration": "9:30 AM - 1:00 PM",
      "format": "Teams",                // Teams, In-person, Hybrid
      "location": "Microsoft Innovation Hub",
      "summary_file": "engagement_summary_2026-01-29.md",
      "key_outcomes": [
        "Prototype approach agreed",
        "Two-pillar architecture defined"
      ],
      "action_items_count": 6,
      "attendees": {
        "microsoft": ["Brendon Colburn", "Erick Morton"],
        "customer": ["Brandon Robinson", "Alexander Peither"],
        "partner": ["HSO"]
      }
    }
  ],
  
  // Milestones tracking
  "milestones": [
    {
      "name": "Initial Envisioning",
      "date": "2026-01-29",
      "status": "completed",            // completed, scheduled, planned, blocked
      "notes": "Prototype approach agreed"
    },
    {
      "name": "Prototype Session",
      "date": "2026-02-10",
      "status": "scheduled",
      "notes": "Two-day in-person session"
    },
    {
      "name": "Production Deployment",
      "date": null,
      "status": "planned",
      "notes": "Pending prototype outcomes"
    }
  ],
  
  // Journey health tracking
  "journey_health": {
    "momentum": "strong",               // strong, steady, stalled, at-risk
    "last_customer_contact": "2026-01-29",
    "days_since_contact": 0,
    "open_action_items": 6,
    "blockers": [],
    "next_touchpoint": "2026-02-10"
  }
}
```

### Preserved Fields (From Original Engagement)

All existing fields are preserved:
- `customer`, `engagement_type`, `created`, `updated`
- `lead_architect`, `supporting_engineer`
- `key_context`, `platform_for_success_initiative`
- `engagement_outcomes`, `action_items`
- `customer_precall_notes`, `fdd_document`, etc.

### Status Transitions

```
journey_status:
  active     → Customer engaged, sessions ongoing
  on-hold    → Paused (customer side or Microsoft side)
  completed  → All milestones achieved, success
  closed     → Ended without completion (lost, deprioritized)

session.status:
  scheduled  → Future session confirmed
  completed  → Session held, outcomes captured
  cancelled  → Session was cancelled

milestone.status:
  planned    → Future, not yet scheduled
  scheduled  → Date confirmed
  completed  → Achieved
  blocked    → Cannot proceed (blocker exists)
```

## WorkIQ Integration

### Query for Session Data

When promoting, query WorkIQ for recent meetings:

```
"Give me a summary of the [Customer] meeting from [date]. 
Include key topics, decisions, action items, and attendees."
```

### Extract and Map

From WorkIQ response, extract:
- `key_outcomes` → From "Decisions Made" section
- `action_items_count` → Count from action items list
- `attendees` → From attendees/participants section
- `duration` → From meeting time
- `format` → From meeting format (Teams/in-person)

### Fallback

If WorkIQ data unavailable:
- Prompt user for key outcomes
- Check for existing summary file
- Use metadata from engagement_outcomes if present

## README Template

See `journey_readme_template.md` for the full template.

Key sections:
1. Journey header with status badge
2. Sessions timeline (table with all sessions)
3. Current status and next milestone
4. Cumulative action items
5. Customer background (preserved)
6. Files list with session summaries

## Error Handling

| Scenario | Handling |
|----------|----------|
| Customer not found | Show available engagements, ask to clarify |
| Multiple matches | List matches, ask user to select |
| Already a journey | Confirm, offer to update metadata only |
| No metadata file | Create basic journey metadata from folder name |
| Rename fails | Check OneDrive sync, retry, report error |
| WorkIQ unavailable | Continue without, prompt for manual input |

## Future Enhancements

- `add session to [Customer] journey` - Add new session without full promotion
- `update [Customer] journey status` - Change journey_status or health
- `show journey status for [Customer]` - Display current state
- CE Hub integration - Sync journey status to CE Hub
