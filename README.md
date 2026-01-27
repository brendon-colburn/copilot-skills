# Copilot Skills for Customer Engagements

Automate your customer engagement workflows with GitHub Copilot. Store engagements in OneDrive to create an AI-powered skills layer for Microsoft 365 Copilot.

## What You Can Do

- **Create engagement folders** with task timelines and metadata
- **Generate task schedules** with automatic business day calculations
- **Build professional agendas** from planning transcripts
- **Extract and update patterns** from your engagement history

## What You Need

- GitHub Copilot subscription with VS Code
- VS Code version 1.108 or later
- Python 3.7+ (dependencies install automatically)
- Microsoft OneDrive for storing engagements

## Setup

Clone the repository and run the setup script:

```bash
git clone https://github.com/brendon-colburn/copilot-skills.git
cd copilot-skills
python setup.py
```

The interactive script will configure everything for you.

## Start Using Skills

Skills load automatically when you ask for them - just start chatting with Copilot!

## Using the Skills

### Create an Engagement

```
"initiate an engagement for Contoso on 2026-03-15"
"create engagement for Fabrikam that kicks off in 30 days"
```

Creates a folder with:
- Task timeline (15 tasks from T-28 to T+3)
- Engagement metadata
- Timeline overview

### Generate Tasks

```
"generate tasks for Project Phoenix on 2026-04-20"
```

Creates a task timeline with business day calculations (excludes weekends).

### Build an Agenda

```
"build agenda from planning_transcript.txt in the Contoso-2026-03-15 folder"
```

Transforms planning transcripts into professional agendas. Supports Discovery, Architecture Reviews, POCs, Executive Briefings, and more.

**Tip**: Save transcripts to your engagement folder first for better results.

### Update Patterns

```
"update patterns from my engagements"
"refresh the pattern knowledge base"
"extract patterns from recent engagements"
```

Automatically extracts patterns from your engagement history and updates the knowledge base:
- Engagement types (Discovery, Architecture Review, POC, etc.)
- Industry patterns (Healthcare, Finance, Construction, etc.)
- Success factors and key learnings
- Discovery frameworks and approaches

Generates a changelog report showing what patterns were added.

**Optional automation**: Enable scheduled updates with `python configure_scheduler.py`

## Example Workflow

```
1. "initiate an engagement for Contoso on 2026-03-15"
2. Save planning transcript to the engagement folder
3. "build agenda from transcript.txt in the Contoso-2026-03-15 folder"
4. Share agenda with customer
5. Execute engagement and complete follow-up tasks
6. "update patterns from my engagements" (monthly or as needed)
```

## Why OneDrive?

Storing engagements in OneDrive creates an AI skills layer for Microsoft 365 Copilot:
- M365 Copilot can help with engagement prep and summaries
- All engagement data is searchable and accessible to AI
- Optional: Connect tasks.csv to Power Automate for automatic Planner task creation

## Power Automate Integration

The included Power Automate solution (`EngagementTaskAutomation_1_0_0_0.zip`) provides intelligent task scheduling with calendar conflict resolution:

### What It Does

1. **Monitors** your OneDrive Engagements folder for new `tasks.csv` files
2. **Retrieves** 2 months of calendar events from your Office 365 calendar
3. **Analyzes** conflicts using AI Builder's custom prompt model
4. **Creates** a Planner bucket named after your engagement
5. **Schedules** tasks with due dates that avoid your existing commitments

### Setup

1. Import the solution to your Power Automate environment
2. Configure connections:
   - OneDrive for Business (monitoring engagement folder)
   - Office 365 (reading calendar)
   - Dataverse (AI Builder model)
   - Planner (creating tasks)
3. Update the AI Builder model ID and Planner plan ID in the flow
4. Enable the flow

This automation bridges the gap between planning and execution, ensuring your engagement tasks integrate seamlessly with your existing schedule.

## Need Help?

- Check `.github/skills/[skill-name]/references/` for skill documentation
- Visit [agentskills.io](https://agentskills.io/) for more about Agent Skills
- See [VS Code Agent Skills docs](https://code.visualstudio.com/docs/copilot/customization/agent-skills)

---

**Version**: 1.0  
**Last Updated**: January 2026
