# Engagement Closeout - Implementation Guide

## Core Function

Generate structured CE Hub closeout summaries from meeting transcripts using WorkIQ integration.

## Process Flow

```
User: "close out [Customer] engagement"
                ↓
1. Parse customer name and optional date from input
                ↓
2. Find engagement/journey folder
   - Search engagements folder for customer match
   - If journey folder exists, use that
   - If multiple matches, ask user to confirm
                ↓
3. Query WorkIQ for meeting data
   - Request: "Give me a detailed summary of the [Customer] 
     meeting from [date]. Include key topics discussed, 
     decisions made, action items, attendees, agenda, 
     outcomes, and any follow-up sessions scheduled."
                ↓
4. Extract PLAN section data
   - Map industry from customer context
   - Identify solution areas from topics discussed
   - Match motions from engagement objectives
   - Extract agenda from meeting structure
                ↓
5. Extract DEBRIEF section data
   - Identify outcomes achieved (from decisions/agreements)
   - Map use cases addressed (from topics)
   - Summarize discovery insights (first 1-2 hours)
   - Capture what worked/didn't work
   - List new opportunities (sales/consumption)
   - Identify next engagements (from follow-ups)
   - Summarize next steps and timeframes
                ↓
6. Generate closeout document
   - Format as structured markdown
   - Apply selection lists for categorical fields
   - Leave blank/N/A for missing information
                ↓
7. Save to engagement folder
   - Create closeout_summary_[date].md
   - Update engagement_metadata.json
                ↓
8. Display for review
   - Show formatted closeout
   - Offer to adjust before finalizing
```

## WorkIQ Integration

### Query Template

```
Give me a detailed summary of the [Customer] meeting from [Date].

Include:
1. Meeting agenda or structure
2. Key topics discussed
3. Decisions made and agreements
4. Outcomes achieved
5. What worked well
6. Any challenges or issues
7. New opportunities identified
8. Follow-up sessions scheduled
9. Action items with owners and timelines
10. Attendees from customer and Microsoft

I need this for CE Hub closeout, so focus on:
- Industry context
- Solution areas covered
- Microsoft motions addressed
- Use cases demonstrated
- Value delivered
```

### Mapping Logic

#### Industry Mapping
From meeting context, customer profile, or metadata:
```python
industry_keywords = {
    "government": ["federal", "agency", "public sector", "DOD", "DOI", "state"],
    "healthcare": ["hospital", "medical", "health system", "clinical", "patient"],
    "financial_services": ["bank", "insurance", "fintech", "trading", "investment"],
    "manufacturing": ["factory", "production", "supply chain", "OEM", "plant"],
    "defense": ["defense", "military", "intelligence", "security clearance", "SCIF"],
    # ... etc
}
```

#### Solution Area Mapping
From topics/technologies discussed:
```python
solution_keywords = {
    "AI Business Solution": ["copilot studio", "agents", "AI", "copilot", "LLM"],
    "Cloud and AI Platforms": ["azure", "fabric", "foundry", "infrastructure"],
    "Microsoft Unified": ["support", "unified", "premier"],
    "Security": ["security", "purview", "defender", "sentinel", "compliance"],
}
```

#### Motion Mapping
From engagement objectives and outcomes:
```python
motion_keywords = {
    "AI Transformation offer": ["AI transformation", "AI strategy"],
    "Copilots on every device": ["copilot adoption", "M365 copilot", "copilot rollout"],
    "Differentiated AI design": ["custom agents", "agentic", "copilot studio"],
    "Frontier AI Solutions": ["azure AI", "foundry", "custom models"],
    "M365 and D365 core execution": ["dynamics", "M365", "power platform"],
    "Migrations and modernization": ["migration", "modernization", "cloud adoption"],
    "Securing the Cyber Foundation": ["security", "zero trust", "compliance"],
}
```

## Selection List Validation

Only select items explicitly mentioned in the transcript. For each selection:

1. **Confirm explicit mention** - keyword or concept appears in transcript
2. **Don't infer** - if not explicitly discussed, don't include
3. **Use N/A** - if no items match, use "N/A"

## PLAN Section Details

### 1. Industry Focus
- Source: Customer profile, metadata, or explicit mention
- Multiple selections allowed
- Must be from the defined list

### 2. Relevant Solution Areas
- Source: Technologies discussed, solutions demonstrated
- Multiple selections allowed
- Map from product/technology mentions

### 3. Motion Alignment
- Source: Engagement objectives, outcomes achieved
- Multiple selections allowed
- Connect to Microsoft strategic motions

### 4. Content Items and Experiences Used
- Source: Demos shown, materials referenced
- Leave blank if not explicitly documented
- Examples: specific demos, decks, hands-on labs

### 5. Engagement Agenda
- Source: Meeting invite body OR inferred from transcript structure
- Include time blocks if available
- List major session segments

## DEBRIEF Section Details

### 1. Outcomes
- Source: "Decisions made", "Agreements", "What was accomplished"
- Only select from defined list
- Must have evidence in transcript

### 2. Use Cases
- Source: Topics discussed, scenarios demonstrated
- Map to the four use case categories
- Multiple selections allowed

### 3. Discovery and Insights
- Source: First 1-2 hours of session (typically discovery phase)
- Summarize key learnings about customer
- Include pain points, current state, priorities

### 4. What Worked Well
- Source: Positive feedback, successful demos, strong engagement
- Include prep work that paid off
- Note effective collaboration moments

### 5. What Did Not Work Well
- Source: Challenges, technical issues, gaps
- Be constructive, not critical
- Include suggestions for improvement

### 6. New Opportunities Discovered
- Source: Products/services mentioned as potential follow-ons
- Focus on sales/consumption opportunities
- Include specific Microsoft products/services

### 7. Customer Journey (Next Engagements)
- Source: "Follow-up sessions scheduled", "Next steps"
- Only select from defined list
- Must be explicitly agreed in meeting

### 8. Next Steps and Timeframe
- Source: Action items, timelines, follow-up dates
- Include owners where specified
- Be specific about dates/timeframes

## Output File Format

### Filename Convention
```
closeout_summary_YYYY-MM-DD.md
```

### Metadata Update
```json
{
  "closeout_generated": true,
  "closeout_date": "YYYY-MM-DD",
  "closeout_file": "closeout_summary_YYYY-MM-DD.md"
}
```

## Error Handling

| Scenario | Handling |
|----------|----------|
| Meeting not found in WorkIQ | Ask for date, try alternative queries |
| Transcript too short | Note limitations, extract what's available |
| Missing required info | Use N/A, don't fabricate |
| Customer folder not found | Create new folder or ask for location |
| Selection mismatch | Ask user to confirm/override |

## Quality Checks

Before finalizing closeout:

1. **All selections from valid lists** - no free-form in selection fields
2. **Evidence-based** - every claim traceable to transcript
3. **No fabrication** - missing info = N/A
4. **Professional tone** - suitable for manager/leader review
5. **Actionable next steps** - clear owners and timelines
