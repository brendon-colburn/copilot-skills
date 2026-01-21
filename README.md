# Copilot Skills for Customer Engagements

A collection of GitHub Copilot skills that streamline customer engagement workflows from planning to execution. By storing engagements in OneDrive, you create a **skills layer for Microsoft 365 Copilot**, enabling AI-powered insights across your entire engagement lifecycle.

## Overview

These skills automate common engagement tasks:

- **engagement-initiator** - Creates engagement folder structures with task timelines and metadata
- **task-generator** - Generates task timelines with business day calculations (optionally integrates with Power Automate)
- **agenda-builder** - Creates professional engagement agendas from planning transcripts

## Prerequisites

- **GitHub Copilot** subscription (with Copilot Chat)
- **VS Code** version 1.108 or later
- **Agent Skills feature enabled** (currently in preview - see setup instructions below)
- **Python 3.7+** for running automation scripts (dependencies are automatically installed by the skills)
- **Microsoft OneDrive** (recommended) - Enables M365 Copilot to leverage engagement data as a skills layer

## Quick Start

### 1. Clone this Repository

```bash
git clone <your-repo-url>
cd copilot-skills
```

### 2. Configure Your Environment

Copy the example configuration file and customize it:

```bash
copy config.example.json config.json
```

Edit `config.json` with your OneDrive path:

```json
{
  "engagements_base_path": "C:\\Users\\<your-username>\\OneDrive - Microsoft\\Engagements"
}
```

> **Note**: `config.json` is gitignored and won't be committed to the repository.

### 3. Enable Agent Skills in VS Code

Agent Skills support is currently in preview. You must enable it in your VS Code settings:

1. Open VS Code Settings (`Ctrl+,` or `Cmd+,`)
2. Search for `chat.useAgentSkills`
3. Enable the **Chat: Use Agent Skills** setting

Alternatively, add this to your `settings.json`:

```json
{
  "chat.useAgentSkills": true
}
```

### 4. Open Workspace in VS Code

Open this folder in VS Code where GitHub Copilot is enabled. Skills will automatically load based on your prompts - you don't need to manually select them.

**How skills load**:
- Copilot always knows which skills are available by reading their metadata
- When your request matches a skill's description, it loads the detailed instructions
- Only relevant skills load into context, keeping things efficient

## Using the Skills

### Engagement Initiator

Creates a complete engagement folder structure with tasks, metadata, and README.

**Examples**:
```
"initiate an engagement for Contoso on 2026-03-15"
"create engagement for Fabrikam that kicks off in 30 days"
"new engagement for Acme Inc tomorrow"
```

**What it creates**:
```
OneDrive/Engagements/[Customer]-[Date]/
├── tasks.csv (15 tasks, T-28 to T+3)
├── engagement_metadata.json
└── README.md (timeline overview)
```

**Outputs**:
- **tasks.csv** - Task timeline with business day calculations (optionally triggers Power Automate)
- **Timeline status** - Shows overdue, current, and upcoming tasks
- **Metadata** - Customer info, dates, and engagement status
- **OneDrive location** - Creates a skills layer for M365 Copilot to provide engagement insights

### Task Generator

Standalone task timeline generation with business day calculations.

**Examples**:
```
"generate tasks for Project Phoenix on 2026-04-20"
"create task timeline for customer XYZ, engagement date 2026-05-10"
```

**Business day rules**:
- Excludes weekends (Saturday/Sunday)
- T-28 = 28 business days BEFORE engagement
- T+2 = 2 business days AFTER engagement

**Task timeline** (15 tasks):
- T-28: Schedule Internal Precall
- T-22: Research customer
- T-21: Execute Internal Precall
- T-20: Draft Agenda
- T-20: Schedule Customer Precall
- T-14: Execute Customer Precall
- T-14: Schedule internal resources
- T-10: Validate Agenda with ATU
- T-7: Validate Agenda with Customer
- T-7: Prep Demos
- T-3: Confirm Customer pre-work
- T-0: Send Satisfaction Survey
- T+2: Conduct MSFT Debrief
- T+2: Share Engagement Materials
- T+3: Complete Close-out form

### Agenda Builder

Transforms planning transcripts into professional DOCX agendas.

**Examples**:
```
"build agenda from planning_transcript.txt in the Contoso-2026-03-15 folder"
"create engagement agenda from the transcript file in ABC Group engagement"
"generate agenda for [customer] using [filename.txt]"
```

**Best practice**: Save transcripts to the engagement folder first, then reference them by filename. This approach:
- Handles long transcripts without context limits
- Keeps all engagement artifacts organized in one location
- Enables M365 Copilot to access transcripts for future queries

**How it works**:
1. Save planning transcript to engagement folder
2. Ask Copilot to build agenda from the transcript file
3. Copilot reads the file and extracts structured data (customer, date, topics, participants)
4. Shows preview for confirmation
5. **Automatically installs required Python packages** (no manual setup needed)
6. Generates professional DOCX agenda
7. Saves to engagement folder

**Session types supported**:
- Discovery Sessions
- Architecture Reviews
- Proof of Concepts (POCs)
- Executive Briefings
- Deep Dive Sessions
- Custom engagement types

## Workflow Example

Complete engagement workflow from planning to execution:

```
1. "initiate an engagement for Contoso on 2026-03-15"
   → Creates folder structure with tasks.csv in OneDrive
   → (Optional) Power Automate creates Planner tasks automatically

2. Save planning transcript to engagement folder
   → Store long transcripts as files for better AI processing
   → GitHub Copilot can now access this data along with its skills layer

3. "build agenda from [transcript file] in the Contoso-2026-03-15 folder"
   → Creates professional agenda document
   → Works better with file references than pasting long transcripts

4. Share agenda with customer and internal team
   → M365 Copilot can help summarize and analyze engagement data

5. Execute engagement on T-0 (March 15)

6. Complete T+2 and T+3 tasks (debrief, materials, close-out)
   → Store outputs in OneDrive engagement folder for AI access
```

## File Structure

```
copilot-skills/
├── .github/
│   └── skills/                    # Copilot skill definitions
│       ├── engagement-initiator/
│       │   ├── SKILL.md          # Skill instructions for Copilot
│       │   ├── scripts/          # Automation scripts
│       │   └── references/       # Documentation
│       ├── task-generator/
│       └── agenda-builder/
├── config.json                    # Your local config (gitignored)
├── config.example.json            # Template for configuration
└── README.md                      # This file
```

## Configuration Reference

### config.json

```json
{
  "engagements_base_path": "C:\\Users\\<username>\\OneDrive - Microsoft\\Engagements"
}
```

**Parameters**:
- `engagements_base_path` - Full path to your OneDrive Engagements folder (use double backslashes on Windows)

## Tips & Best Practices

### Timeline Management
- **T-28 to T-7**: Pre-engagement planning and customer alignment
- **T-3 to T-0**: Final prep and validation
- **T+2 to T+3**: Post-engagement follow-up and close-out

### Task Management
- **tasks.csv** is generated and saved to the engagement folder in OneDrive
- Contains all 15 engagement tasks (T-28 to T+3) with calculated business day dates
- **Optional**: Set up a Power Automate flow to automatically create Planner tasks from tasks.csv
- With automation, tasks appear in Planner within minutes of engagement creation
- Without automation, the CSV serves as a reference for manual task creation

### Agenda Building
- **Save planning transcripts to the engagement folder** - This works best since transcripts are often long
- Reference the transcript file directly: "build agenda from [filename] in the Contoso engagement folder"
- Copilot can read longer transcripts from files without hitting context limits
- Include specific customer context and terminology from the transcript
- Copilot extracts standard items (breaks, intro, wrap-up) automatically
- Review and edit the preview before generating DOCX

### OneDrive & M365 Copilot Skills Layer
- **Storing engagements in OneDrive creates a skills layer for M365 Copilot** - AI can access and analyze engagement data across your organization
- **M365 Copilot can help** with engagement prep, summarizing past engagements, finding relevant customer context, and more
- README.md in each folder provides quick timeline overview for both humans and AI
- Metadata JSON enables future automation and reporting
- **Power Automate integration** (optional) - Tasks.csv can trigger automated Planner task creation

## Contributing

Feel free to customize the skills for your specific workflow:

1. Edit skill SKILL.md files to adjust instructions
2. Modify Python scripts for different task templates
3. Update agenda templates for your organization's branding
4. Add new skills by creating similar folder structures

## Support

For questions or issues:
- Review skill documentation in `.github/skills/[skill-name]/references/`
- Check Copilot Chat for skill-specific help
- Consult Python script comments for technical details
- Learn more about Agent Skills at [agentskills.io](https://agentskills.io/)
- See [VS Code Agent Skills documentation](https://code.visualstudio.com/docs/copilot/customization/agent-skills)

---

**Version**: 1.0  
**Last Updated**: January 2026
