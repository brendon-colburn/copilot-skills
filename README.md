# Copilot Skills for Customer Engagements

Automate customer engagement workflows with GitHub Copilot. Integrates with WorkIQ for M365 data access and stores engagements in OneDrive to create an AI-powered skills layer for Microsoft 365 Copilot.

## What You Can Do

- **Create engagement folders** with task timelines, metadata, and Planner-ready CSV
- **Build professional agendas** from planning transcripts
- **Promote to journeys** for ongoing customer relationships
- **Generate closeout summaries** with structured PLAN/DEBRIEF sections
- **Draft follow-up emails** from transcripts and closeout data
- **Scaffold Power Apps Code Apps** with React, Vite, and TypeScript

## What You Need

- GitHub Copilot subscription with VS Code
- VS Code version 1.108 or later
- Python 3.7+ (dependencies install automatically)
- OneDrive for storing engagements

## Setup

### 1. Clone and Configure

```bash
git clone https://github.com/brendon-colburn/copilot-skills.git
cd copilot-skills
python setup.py
```

The interactive script will configure everything for you.

### 2. Enable WorkIQ (Optional)

[WorkIQ](https://github.com/microsoft/work-iq-mcp) connects Copilot to your Microsoft 365 data — emails, meetings, documents, Teams messages, and more. The closeout, follow-up email, and journey promoter skills use WorkIQ to pull meeting transcripts directly into the workflow.

**Install as a VS Code MCP server (recommended):**

Click the button to install automatically:

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Server-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=workiq&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fworkiq%22%2C%22mcp%22%5D%7D)

Or add manually to your VS Code MCP settings:

```json
{
  "workiq": {
    "command": "npx",
    "args": ["-y", "@microsoft/workiq", "mcp"],
    "tools": ["*"]
  }
}
```

See [VS Code MCP server docs](https://code.visualstudio.com/docs/copilot/customization/mcp-servers) for where to place this configuration.

**First-time use:**

1. On first query, you'll be prompted to accept the EULA through your browser
2. A consent dialog will appear for M365 data access — if you're not a tenant admin, contact your admin to grant consent (see [Admin Enablement Guide](https://github.com/microsoft/work-iq-mcp/blob/main/ADMIN-INSTRUCTIONS.md))

**Requirements:** Microsoft 365 Copilot license and admin consent for organizational data access. Node.js 18+ (for npx).

## Skills Reference

Skills load automatically when you ask for them — just start chatting with Copilot.

### Engagement Initiator

Creates engagement folder structure in OneDrive with tasks, metadata, and timeline.

```
"create engagement for Contoso on March 15"
"initiate engagement for Fabrikam starting in 30 days"
```

**Creates:** Folder with 15-task timeline (T-28 to T+3) using business day calculations that exclude weekends, `engagement_metadata.json`, `tasks.csv`, and `README.md`. The CSV is Planner-ready — import directly via "Import plan from Excel."

### Agenda Builder

Transforms planning transcripts into professional DOCX agendas.

```
"build agenda from planning_transcript.txt in the Contoso folder"
```

**Supports:** Discovery, Architecture Reviews, POCs, Executive Briefings, and Deep Dives. Shows a preview for approval before generating the final document.

**Tip:** Save transcripts to your engagement folder first for better results.

### Journey Promoter

Converts a single engagement to a customer journey when follow-up sessions are confirmed.

```
"promote Contoso to journey"
"convert Booz Allen to customer journey"
```

**Does:** Renames folder (e.g., `Contoso-2026-03-15` → `Contoso-2026-Customer-Journey`), migrates metadata to journey schema with session tracking, creates session log, and queries WorkIQ for session summaries.

### Engagement Closeout

Generates structured closeout summaries for CE Hub from meeting transcripts.

```
"close out Contoso engagement"
"generate CE Hub debrief for Fabrikam"
```

**Requires WorkIQ.** Queries meeting transcripts and generates PLAN (industry, solution areas, motion, content used) and DEBRIEF (outcomes, use cases, insights, next steps) sections. Saves as `closeout_summary_[date].md`.

### Follow-Up Email

Generates conversational, human-sounding follow-up emails from closeout summaries and transcripts.

```
"write follow-up email for Contoso"
"draft thank-you email for Fabrikam engagement"
```

**Requires WorkIQ.** Always queries the meeting transcript for specific moments and detail, even when a closeout summary exists. Calibrates tone based on audience seniority. Saves as `followup_email_[date].html`.

### Code App Builder

Scaffolds Power Apps Code Apps using the real `@microsoft/power-apps` SDK.

```
"create a code app for Contoso that tracks asset inspections"
"here's the OData JSON from my Dataverse table, update the schema"
```

**Creates:** Complete React+Vite+TypeScript project with mock Dataverse services, screens, and components. Supports updating schema from real OData JSON. Deploys via PAC CLI.

## Example Workflow

```
1. "create engagement for Contoso on March 15"
2. Save planning transcript to engagement folder
3. "build agenda from transcript.txt in Contoso folder"
4. Share agenda with customer
5. Execute engagement
6. "close out Contoso engagement"
7. "write follow-up email for Contoso"
```

## Why OneDrive?

Storing engagements in OneDrive creates an AI skills layer for Microsoft 365 Copilot:
- M365 Copilot can help with engagement prep and summaries
- All engagement data is searchable and accessible to AI
- WorkIQ can query your meetings, emails, and files for richer context
- Optional: Connect `tasks.csv` to Power Automate for automatic Planner task creation

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

- Check `.github/skills/[skill-name]/SKILL.md` for detailed skill documentation
- Visit [agentskills.io](https://agentskills.io/) for more about Agent Skills
- See [VS Code Agent Skills docs](https://code.visualstudio.com/docs/copilot/customization/agent-skills)

---

**Version**: 2.0  
**Last Updated**: February 2026
