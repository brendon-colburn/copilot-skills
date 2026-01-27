---
name: pattern-updater
description: Analyzes engagement metadata and updates pattern knowledge base (success_patterns.json, engagement_types.md, discovery_patterns.md). Generates changelog reports. Use when updating patterns, analyzing engagements for patterns, or when user mentions pattern updates, knowledge base updates, or pattern extraction.
---

# Pattern Updater

Automatically extracts patterns from engagement metadata and updates the patterns knowledge base in OneDrive.

## Quick Start

**Update patterns**:
```
"update patterns from my engagements"
"refresh the pattern knowledge base"
"extract patterns from recent engagements"
```

**View last update**:
```
"show latest pattern update report"
"when were patterns last updated"
```

## What It Does

1. **Scans** all engagement folders in OneDrive for metadata
2. **Extracts** patterns:
   - Engagement types (Discovery, Architecture Review, POC, etc.)
   - Industry patterns (Healthcare, Finance, Construction, etc.)
   - Success factors and learnings
   - Discovery frameworks and approaches
3. **Updates** pattern files:
   - `success_patterns.json` - Main structured data
   - `engagement_types.md` - Human-readable engagement type definitions
   - `discovery_patterns.md` - Discovery frameworks and techniques
   - `delivery_patterns.md` - Delivery patterns (manual updates recommended)
4. **Generates** changelog report in `patterns/changelog/YYYY-MM.md`

## Output Structure

```
C:\Users\brecol\OneDrive - Microsoft\Engagements\patterns/
├── success_patterns.json (updated automatically)
├── engagement_types.md (appended with new types)
├── discovery_patterns.md (appended with new frameworks)
├── delivery_patterns.md (manual updates)
└── changelog/
    ├── 2026-01.md
    └── 2026-02.md
```

## Configuration

**Configuration File**: `config.json` (root of workspace)

```json
{
  "engagements_base_path": "C:\\Users\\<username>\\OneDrive - Microsoft\\Engagements",
  "pattern_updater": {
    "auto_update": false,
    "schedule": "monthly"
  }
}
```

The `pattern_updater` section is optional. Patterns are updated on-demand via Copilot.

## Workflow

```
- [ ] Scan engagements folder for engagement_metadata.json files
- [ ] Extract patterns from metadata
- [ ] Compare with existing patterns in success_patterns.json
- [ ] Identify new patterns
- [ ] Update success_patterns.json (version bump, add new patterns)
- [ ] Append new types to engagement_types.md
- [ ] Append new frameworks to discovery_patterns.md
- [ ] Generate changelog report
- [ ] Display summary
```

## Engagement Metadata Format

The pattern extractor looks for these fields in `engagement_metadata.json`:

```json
{
  "customer": "string",
  "engagement_date": "YYYY-MM-DD",
  "engagement_type": "string",
  "industry": "string",
  "success_factors": ["list", "of", "factors"],
  "outcomes": ["list", "of", "outcomes"],
  "key_learnings": ["list", "of", "learnings"],
  "discovery_framework": "string or list",
  "discovery_approach": "string or list"
}
```

## Automation (Optional)

### Manual Execution

```bash
python .github/skills/pattern-updater/scripts/run_update.py
```

### Scheduled Execution

For automated monthly updates, configure a scheduler.

**If you haven't run setup yet:**
```bash
python setup.py
# Answer 'y' when asked about automated pattern updates
```

**If you already ran setup but want to enable scheduling now:**
```bash
# Option 1: Standalone script (recommended)
python configure_scheduler.py

# Option 2: Run setup with scheduler-only flag
python setup.py --scheduler-only
```

**Platform-specific commands:**

**Windows (Task Scheduler)**:
```powershell
# Manually create task (if needed)
schtasks /create /tn "Copilot Pattern Updater" /tr "python C:\path\to\repo\.github\skills\pattern-updater\scripts\run_update.py" /sc monthly /d 1 /st 09:00
```

**macOS (launchd)**:
```bash
# LaunchAgent plist created automatically by configure_scheduler.py
# Location: ~/Library/LaunchAgents/com.copilot.patternupdater.plist
```

**Linux (cron)**:
```bash
# Edit crontab
crontab -e
# Add this line for monthly updates (1st of month at 9 AM):
0 9 1 * * cd /path/to/repo && python .github/skills/pattern-updater/scripts/run_update.py >> ~/pattern-updater.log 2>&1
```

## Changelog Reports

Reports are generated in `patterns/changelog/` with the format `YYYY-MM.md`:

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

### Agentic Envisioning
**ID**: `agentic_envisioning`
...
```

## Standalone Script

The pattern updater can also be run as a standalone script:

```bash
# From repo root
python .github/skills/pattern-updater/scripts/run_update.py

# Or with custom paths
python scripts/pattern_extractor.py "/path/to/engagements"
python scripts/update_patterns.py "/path/to/patterns"
```

## Pattern Versioning

`success_patterns.json` uses semantic versioning:

- **Major version** (1.x): Breaking schema changes
- **Minor version** (x.1): New patterns added
- **Last updated**: Date of last update

Example:
```json
{
  "version": "3.0",
  "last_updated": "2026-01-27",
  "sources": 18
}
```

## Best Practices

1. **Run monthly** after completing engagements to capture fresh patterns
2. **Review reports** before committing changes to ensure accuracy
3. **Enrich metadata** - Add detailed metadata to engagements for better pattern extraction
4. **Manual refinement** - Edit generated markdown files to add context and examples
5. **Version control** - Consider tracking patterns in git for history

## Integration

- **engagement-initiator**: Creates engagement folders with metadata
- **agenda-builder**: Uses patterns for agenda generation
- **Microsoft 365 Copilot**: Patterns in OneDrive become searchable by M365 Copilot

## Next Steps

After updating patterns:
- Review changelog in `patterns/changelog/`
- Manually enhance new entries in markdown files
- Share insights with team
- Use patterns to inform future engagement planning

## Reference

See [references/implementation.md](references/implementation.md) for technical details.
