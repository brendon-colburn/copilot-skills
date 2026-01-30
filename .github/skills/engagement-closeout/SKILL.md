---
name: engagement-closeout
description: Generates CE Hub closeout summaries from meeting transcripts via WorkIQ. Creates structured PLAN and DEBRIEF sections for manager/leader review. Use when closing out engagements, generating debrief summaries, or when user says "close out", "generate closeout", "debrief summary", or "CE Hub closeout".
---

# Engagement Closeout

Generates structured closeout summaries for CE Hub from meeting transcripts and engagement context.

## Quick Start

**Basic:**
```
"close out Keller engagement"
"generate closeout for BAH session"
```

**With context:**
```
"close out [Customer] - session was [date]"
"generate CE Hub debrief for [Customer]"
```

## When to Use

Use this skill when:
- An engagement session has been completed and needs CE Hub closeout
- Manager/leader review is required
- You need to document outcomes, insights, and next steps

## What It Does

1. **Queries WorkIQ** for meeting transcript and chat from the engagement
2. **Extracts structured data** into PLAN and DEBRIEF sections
3. **Generates closeout summary** for CE Hub submission
4. **Saves to engagement folder** as closeout file

## Output Structure

The closeout generates two main sections:

### PLAN Section
- Industry focus (selection list)
- Relevant solution areas (selection list)
- Motion alignment (selection list)
- Content items and experiences used
- Engagement agenda

### DEBRIEF Section
- Outcomes achieved (selection list)
- Use cases addressed (selection list)
- Discovery and insights summary
- What worked well
- What did not work well
- New opportunities discovered
- Customer journey / next engagements (selection list)
- Guidance on next steps and timeframe

## Workflow Checklist

```
- [ ] Identify customer and engagement date
- [ ] Query WorkIQ for meeting transcript
- [ ] Extract PLAN section data from transcript
- [ ] Extract DEBRIEF section data from transcript
- [ ] Format as structured closeout summary
- [ ] Save to engagement folder
- [ ] Display summary for review
- [ ] Update engagement_metadata.json (closeout_generated: true)
```

## Selection Lists

### Industries
- Automotive Mobility & Transportation
- Defense & Intelligence
- Education
- Energy & Resources
- Financial Services
- Government
- Healthcare
- Industrials & Manufacturing
- Professional Services
- Retail & Consumer Goods
- Sustainability
- Telecommunications & Media
- Travel Transport & Hospitality

### Solution Areas
- AI Business Solution
- Cloud and AI Platforms
- Microsoft Unified
- Security
- N/A

### Motions
- AI Transformation offer
- Copilots on every device across every role
- Differentiated AI design solutions with every customer
- Frontier AI Solutions
- M365 and D365 core execution
- MACC
- Migrations and modernization
- Securing the Cyber Foundation
- N/A

### Outcomes
- Use cases + prioritization matrix
- Solution mapping
- Architecture
- Code + configuration
- Next steps

### Use Cases
- Enriching employee experiences
- Reinventing customer engagement
- Reshaping business processes
- Bending the curve on innovation

### Customer Journey (Next Engagements)
- Architecture Design
- Business Envisioning
- Executive Briefing
- Hackathon
- Immersive Experience
- Rapid Prototype
- Solution Envisioning
- Experience Center
- IEC
- GBB Support Hand Over
- Other

## Key Principles

1. **Only use details from meeting transcript** - never invent or use external information
2. **Leave blank or N/A** if information is missing for a section
3. **Maintain clarity, professionalism, and enthusiasm**
4. **Focus on achievements, milestones, and value delivered**
5. **Provide actionable insights and next steps**

## Output Format

```markdown
# [Customer] Engagement Closeout

**Date:** [Engagement Date]
**Lead:** [Architect Name]

---

## PLAN

### 1. Industry Focus
- [Industry 1]
- [Industry 2]

### 2. Relevant Solution Areas
- [Solution Area 1]

### 3. Motion Alignment
- [Motion 1]

### 4. Content Items and Experiences Used
[Description or N/A]

### 5. Engagement Agenda
[Agenda from meeting]

---

## DEBRIEF

### 1. Outcomes
- [Outcome 1]
- [Outcome 2]

### 2. Use Cases
- [Use Case 1]

### 3. Discovery and Insights
[Summary of insights from discovery phase]

### 4. What Worked Well
[Summary]

### 5. What Did Not Work Well
[Summary]

### 6. New Opportunities Discovered
[List of opportunities]

### 7. Customer Journey (Next Engagements)
- [Next Engagement Type 1]

### 8. Next Steps and Timeframe
[Summary of next steps, action items, timelines]
```

## Files Created

```
[Customer]-[Date]/
├── closeout_summary_[date].md    (generated closeout)
└── engagement_metadata.json      (updated with closeout_generated: true)
```

## Related Skills

- **journey-promoter**: Promotes engagements to customer journeys
- **engagement-initiator**: Creates initial engagement folders
- **agenda-builder**: Builds session agendas

## Reference

See [references/implementation.md](references/implementation.md) for technical details.
See [references/closeout_template.md](references/closeout_template.md) for full template.
