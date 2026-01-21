# Copilot Skills for Customer Engagements

Automate your customer engagement workflows with GitHub Copilot. Store engagements in OneDrive to create an AI-powered skills layer for Microsoft 365 Copilot.

## What You Can Do

- **Create engagement folders** with task timelines and metadata
- **Generate task schedules** with automatic business day calculations
- **Build professional agendas** from planning transcripts

## What You Need

- GitHub Copilot subscription with VS Code
- VS Code version 1.108 or later
- Python 3.7+ (dependencies install automatically)
- Microsoft OneDrive for storing engagements

## Setup

### Quick Setup (Recommended)

Run the interactive setup script that guides you through all configuration steps:

```bash
git clone <your-repo-url>
cd copilot-skills
python setup.py
```

The script will:
- ✓ Check Python version
- ✓ Create and configure `config.json`
- ✓ Install Python dependencies
- ✓ Provide VS Code setup instructions

### Manual Setup

If you prefer to configure manually:

**1. Clone and Configure**

```bash
git clone <your-repo-url>
cd copilot-skills
copy config.example.json config.json
```

Edit `config.json` with your OneDrive path:

```json
{
  "engagements_base_path": "C:\\Users\\<your-username>\\OneDrive - Microsoft\\Engagements"
}
```

**2. Install Dependencies**

```bash
pip install -r .github/skills/agenda-builder/requirements.txt
```

**3. Enable Agent Skills in VS Code**

1. Open VS Code Settings (`Ctrl+,` or `Cmd+,`)
2. Search for `chat.useAgentSkills`
3. Enable **Chat: Use Agent Skills**

**4. Add Workspace Folders**

For optimal functionality, add both folders to your VS Code workspace:

1. Open this repository folder in VS Code
2. Go to **File > Add Folder to Workspace**
3. Add your OneDrive Engagements folder (e.g., `C:\Users\<your-username>\OneDrive - Microsoft\Engagements`)

This allows Copilot to directly access and manage your engagement files.

### Start Using Skills

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

## Example Workflow

```
1. "initiate an engagement for Contoso on 2026-03-15"
2. Save planning transcript to the engagement folder
3. "build agenda from transcript.txt in the Contoso-2026-03-15 folder"
4. Share agenda with customer
5. Execute engagement and complete follow-up tasks
```

## Why OneDrive?

Storing engagements in OneDrive creates an AI skills layer for Microsoft 365 Copilot:
- M365 Copilot can help with engagement prep and summaries
- All engagement data is searchable and accessible to AI
- Optional: Connect tasks.csv to Power Automate for automatic Planner task creation

## Configuration

Your `config.json` tells the skills where to create engagements:

```json
{
  "engagements_base_path": "C:\\Users\\<username>\\OneDrive - Microsoft\\Engagements"
}
```

Use double backslashes (`\\`) on Windows.

## Need Help?

- Check `.github/skills/[skill-name]/references/` for skill documentation
- Visit [agentskills.io](https://agentskills.io/) for more about Agent Skills
- See [VS Code Agent Skills docs](https://code.visualstudio.com/docs/copilot/customization/agent-skills)

---

**Version**: 1.0  
**Last Updated**: January 2026
