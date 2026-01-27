# Pattern Updater - Quick Start Guide

This guide will help you start using the pattern-updater skill to automatically extract and maintain patterns from your engagement history.

## Prerequisites

1. Run `python setup.py` to configure the repository
2. Create engagements using the engagement-initiator skill
3. Ensure your OneDrive Engagements folder has a `patterns` directory

## Creating the Patterns Directory

If you haven't already created the patterns folder:

```bash
# Windows
mkdir "C:\Users\<username>\OneDrive - Microsoft\Engagements\patterns"

# macOS/Linux
mkdir -p "$HOME/OneDrive - Microsoft/Engagements/patterns"
```

Create an initial `success_patterns.json` file:

```json
{
  "version": "1.0",
  "last_updated": "2026-01-27",
  "sources": 0,
  "engagement_types": [],
  "success_patterns": [],
  "industry_patterns": [],
  "discovery_frameworks": []
}
```

## Using via Copilot Chat

The easiest way to use the pattern-updater is through Copilot:

```
"update patterns from my engagements"
"refresh the pattern knowledge base"
"extract patterns from recent engagements"
```

Copilot will:
1. Scan all engagement folders
2. Extract patterns from metadata
3. Update pattern files
4. Generate a changelog report
5. Show you a summary

## Manual Execution

You can also run the pattern updater manually:

```bash
# From the repository root
python .github/skills/pattern-updater/scripts/run_update.py
```

## What Gets Extracted

The pattern updater looks for these fields in `engagement_metadata.json`:

### Engagement Type
```json
{
  "engagement_type": "Discovery Session",
  "type": "Architecture Review",
  "session_type": "POC Kickoff"
}
```

### Industry
```json
{
  "industry": "Healthcare",
  "customer_industry": "Financial Services",
  "sector": "Manufacturing"
}
```

### Success Patterns
```json
{
  "success_factors": [
    "Strong executive sponsor",
    "Technical stakeholders present"
  ],
  "outcomes": [
    "Identified 3 high-priority use cases",
    "Proof of concept approved"
  ],
  "key_learnings": [
    "Early data assessment critical",
    "Compliance review needed upfront"
  ]
}
```

### Discovery Frameworks
```json
{
  "discovery_framework": "Design Thinking Discovery",
  "discovery_approach": [
    "Stakeholder interviews",
    "Technical assessment"
  ]
}
```

## Understanding the Output

### Updated Files

1. **success_patterns.json**: Main structured data file
   - Version bumped (1.0 → 1.1)
   - New patterns appended
   - Source count updated

2. **engagement_types.md**: Human-readable engagement types
   - New types appended with date stamp
   - Includes ID and description

3. **discovery_patterns.md**: Discovery frameworks
   - New frameworks appended with date stamp
   - Includes ID and details

### Changelog Report

Generated in `patterns/changelog/YYYY-MM.md`:

```markdown
# Pattern Update Report - January 2026

**Generated**: 2026-01-27 10:30:00

## Summary

- Total Patterns Added: 15
- Engagement Types: 4 added
- Industries: 2 added
- Success Patterns: 6 added
- Discovery Frameworks: 3 added
- Source Engagements Analyzed: 7

## New Engagement Types
...
```

## Automated Updates (Optional)

If you configured automated updates during setup, patterns will be automatically extracted on your chosen schedule (monthly or weekly).

### Check Scheduler Status

**Windows**:
```powershell
schtasks /query /tn "Copilot Pattern Updater"
```

**macOS**:
```bash
launchctl list | grep patternupdater
```

**Linux**:
```bash
crontab -l | grep pattern-updater
```

### View Logs

**Windows**: Check Task Scheduler history

**macOS**: 
```bash
cat ~/Library/Logs/pattern-updater.log
```

**Linux**:
```bash
cat ~/pattern-updater.log
```

## Best Practices

### 1. Run After Completing Engagements

Update patterns monthly or after major engagement milestones:
- After completing a set of engagements
- Before planning similar future engagements
- When you notice patterns emerging

### 2. Enrich Your Metadata

The more detailed your engagement metadata, the better the pattern extraction:

```json
{
  "customer": "Contoso Healthcare",
  "engagement_date": "2026-01-15",
  "engagement_type": "Discovery Session",
  "industry": "Healthcare",
  "success_factors": [
    "Executive sponsor attended all sessions",
    "Clear business objectives defined upfront",
    "Technical team had API access ready"
  ],
  "outcomes": [
    "Identified 5 use cases across 3 departments",
    "POC approved for Q2 implementation",
    "Security review completed successfully"
  ],
  "key_learnings": [
    "HIPAA compliance review should happen in discovery phase",
    "Data quality assessment revealed migration needs",
    "Department-specific demos were highly effective"
  ],
  "discovery_framework": "Healthcare Compliance-First Discovery",
  "discovery_approach": [
    "Stakeholder interviews by role",
    "Technical environment assessment",
    "Compliance requirements review",
    "Data quality analysis"
  ],
  "challenges": [
    "Legacy system integration complexity",
    "Data residency requirements"
  ],
  "next_steps": [
    "POC planning session scheduled",
    "Architecture design workshop"
  ]
}
```

### 3. Review and Refine

After pattern updates:
1. Review the changelog report
2. Manually enhance new entries in markdown files
3. Add examples and context
4. Share insights with your team

Example enhancement:

```markdown
### Healthcare Compliance-First Discovery
**ID**: `healthcare_compliance_first_discovery`

A discovery framework designed for healthcare engagements that prioritizes compliance and regulatory requirements from the start.

**Key Phases:**
1. Compliance requirements gathering (HIPAA, HITECH)
2. Data residency and sovereignty review
3. Security architecture assessment
4. Use case identification within compliance boundaries

**Best For:**
- Healthcare providers
- Health insurance companies
- Medical device manufacturers

**Success Indicators:**
- Compliance team engaged from day 1
- Security review completed in discovery
- Data handling procedures documented
```

### 4. Share Patterns

Patterns in OneDrive become searchable by Microsoft 365 Copilot:
- Use patterns to prep for similar engagements
- Share with team members for learning
- Reference in engagement planning

## Troubleshooting

### "No patterns found"

**Causes:**
- No engagement folders with metadata files
- Metadata format doesn't match expected structure
- engagements_base_path incorrect in config.json

**Solutions:**
1. Verify engagements exist: Check your OneDrive folder
2. Check metadata format: Ensure `engagement_metadata.json` exists
3. Verify config: Run `python setup.py` to reconfigure

### "Patterns directory not found"

**Solution:**
Create the patterns directory and initial success_patterns.json file (see "Creating the Patterns Directory" above).

### "All patterns are up to date"

This is normal! It means:
- No new patterns were found in recent engagements
- All existing patterns are already in the database

### Report Generation Failed

**Causes:**
- patterns/changelog/ directory doesn't exist
- Permission issues
- Disk space

**Solutions:**
```bash
# Windows
mkdir "C:\Users\<username>\OneDrive - Microsoft\Engagements\patterns\changelog"

# macOS/Linux
mkdir -p "$HOME/OneDrive - Microsoft/Engagements/patterns/changelog"
```

## Next Steps

1. **Start creating engagements** with rich metadata
2. **Run pattern updates** monthly
3. **Review and enhance** the generated patterns
4. **Use patterns** to improve future engagements
5. **Share insights** with your team

## Resources

- [Pattern Updater SKILL.md](SKILL.md) - Full skill documentation
- [Implementation Reference](references/implementation.md) - Technical details
- [Engagement Initiator](../engagement-initiator/SKILL.md) - Create engagements
- [Agenda Builder](../agenda-builder/SKILL.md) - Build agendas

## Support

For issues or questions:
1. Check the [implementation reference](references/implementation.md)
2. Review the [main README](../../../README.md)
3. Open an issue on GitHub

---

*Happy pattern mining! 🔍*
