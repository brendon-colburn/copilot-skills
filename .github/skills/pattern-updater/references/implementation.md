# Pattern Updater - Implementation Reference

## Architecture

The pattern-updater skill follows a hybrid approach combining:
- **Copilot Skill**: Interactive updates via Copilot chat
- **Standalone Scripts**: Can be run independently or scheduled
- **Modular Design**: Separate concerns (extraction, updating, reporting)

## Components

### 1. Pattern Extractor (`pattern_extractor.py`)

**Purpose**: Scans engagement folders and extracts patterns from metadata files.

**Key Functions**:
- `find_engagement_folders()` - Locates all engagement directories
- `read_metadata()` - Reads engagement_metadata.json files
- `extract_all_patterns()` - Extracts all pattern types
- `get_new_patterns()` - Identifies patterns not in existing database

**Extracted Fields**:
- Engagement types: `engagement_type`, `type`, `session_type`
- Industries: `industry`, `customer_industry`, `sector`
- Success patterns: `success_factors`, `outcomes`, `key_learnings`
- Discovery frameworks: `discovery_framework`, `discovery_approach`

### 2. Pattern Updater (`update_patterns.py`)

**Purpose**: Updates pattern files with newly discovered patterns.

**Key Functions**:
- `read_success_patterns()` - Load current patterns
- `write_success_patterns()` - Save updated patterns
- `update_success_patterns_json()` - Add new patterns to JSON
- `update_engagement_types_md()` - Append to markdown files
- `apply_updates()` - Orchestrate all updates

**Files Updated**:
- `success_patterns.json` - Main structured data (version bumped)
- `engagement_types.md` - Appended with new types
- `discovery_patterns.md` - Appended with new frameworks

### 3. Report Generator (`report_generator.py`)

**Purpose**: Creates changelog reports documenting pattern updates.

**Key Functions**:
- `generate_report()` - Create markdown changelog
- `generate_summary_text()` - Console summary for immediate feedback

**Report Format**: `patterns/changelog/YYYY-MM.md`

**Report Sections**:
- Summary statistics
- New engagement types (detailed)
- New industry patterns (detailed)
- New success patterns (list)
- New discovery frameworks (detailed)
- Source engagements (credited)

### 4. Main Orchestrator (`run_update.py`)

**Purpose**: Coordinates the entire update workflow.

**Workflow**:
1. Load config from `config.json`
2. Extract patterns from all engagements
3. Identify new patterns vs existing
4. Apply updates to pattern files
5. Generate changelog report
6. Display summary

## Data Structures

### success_patterns.json

```json
{
  "version": "3.0",
  "last_updated": "2026-01-27",
  "sources": 18,
  "engagement_types": [
    {
      "id": "discovery",
      "name": "Discovery Session",
      "description": "Initial exploration...",
      "typical_duration": "2-4 hours",
      "key_activities": ["..."]
    }
  ],
  "success_patterns": [
    {
      "id": "executive_sponsorship",
      "category": "stakeholder_engagement",
      "description": "Strong executive sponsor...",
      "indicators": ["..."],
      "anti_patterns": ["..."]
    }
  ],
  "industry_patterns": [
    {
      "id": "healthcare",
      "name": "Healthcare",
      "characteristics": ["..."],
      "common_use_cases": ["..."]
    }
  ],
  "discovery_frameworks": [
    {
      "id": "design_thinking",
      "name": "Design Thinking Discovery",
      "phases": ["..."],
      "key_questions": ["..."]
    }
  ]
}
```

### engagement_metadata.json

```json
{
  "customer": "Contoso Ltd",
  "engagement_date": "2026-01-15",
  "engagement_type": "Discovery Session",
  "industry": "Healthcare",
  "status": "completed",
  "success_factors": [
    "Clear objectives defined upfront",
    "Technical stakeholders present"
  ],
  "outcomes": [
    "Identified 3 high-priority use cases",
    "Technical proof of concept planned"
  ],
  "key_learnings": [
    "Early data quality assessment critical",
    "Need compliance review for healthcare data"
  ],
  "discovery_framework": "Design Thinking Discovery",
  "discovery_approach": "Stakeholder interviews + Technical assessment"
}
```

## Configuration

### config.json

```json
{
  "engagements_base_path": "C:\\Users\\<username>\\OneDrive - Microsoft\\Engagements",
  "pattern_updater": {
    "auto_update": false,
    "schedule": "monthly",
    "notification_email": "optional@email.com"
  }
}
```

**Note**: The `pattern_updater` section is optional. Currently only `engagements_base_path` is required.

## Usage Patterns

### Via Copilot Chat

```
User: "update patterns from my engagements"

Copilot: 
1. Loads config
2. Runs pattern extractor
3. Identifies new patterns
4. Updates files
5. Generates report
6. Shows summary
```

### Standalone Execution

```bash
# From repo root
python .github/skills/pattern-updater/scripts/run_update.py

# Individual components
python scripts/pattern_extractor.py "/path/to/engagements"
python scripts/update_patterns.py "/path/to/patterns"
python scripts/report_generator.py "/path/to/patterns"
```

### Scheduled Execution

Configure via `setup.py`:

```python
def configure_pattern_updater_schedule():
    """Set up monthly pattern update schedule"""
    system = platform.system()
    
    if system == "Windows":
        # Windows Task Scheduler
        setup_windows_scheduled_task()
    elif system == "Darwin":
        # macOS launchd
        setup_macos_launchd_job()
    else:
        # Linux cron
        setup_linux_cron_job()
```

## Error Handling

### Common Scenarios

1. **Config not found**: Guides user to run `setup.py`
2. **Patterns directory missing**: Instructs user to create it
3. **No metadata files**: Returns gracefully with "no patterns found"
4. **JSON parse errors**: Logs warning, skips file, continues
5. **File write errors**: Reports error, suggests permission check

### Graceful Degradation

- If markdown updates fail, JSON still updates
- If report generation fails, updates still applied
- Always provides console summary even if file operations fail

## Versioning Strategy

### success_patterns.json Version

- Format: `"version": "MAJOR.MINOR"`
- Increment MINOR when patterns are added
- Increment MAJOR for schema breaking changes
- `last_updated` timestamp on every update

### Changelog Files

- One file per month: `YYYY-MM.md`
- Multiple updates in same month append to same file
- Historical record of all pattern evolution

## Testing

### Manual Testing

```bash
# Test pattern extraction
python scripts/pattern_extractor.py "/path/to/test/engagements"

# Test report generation
python scripts/report_generator.py "/path/to/test/patterns"

# Full integration test
python scripts/run_update.py
```

### Test Data Structure

Create test engagement folder:
```
test-engagements/
├── Test-Customer-2026-01-15/
│   └── engagement_metadata.json
└── Another-Customer-2026-01-20/
    └── engagement_metadata.json
```

## Future Enhancements

### Potential Features

1. **AI-powered pattern synthesis**: Use Copilot to suggest pattern descriptions
2. **Pattern quality scoring**: Identify patterns supported by multiple engagements
3. **Trend analysis**: Track pattern adoption over time
4. **Pattern recommendations**: Suggest patterns for new engagements based on similarity
5. **Team collaboration**: Multi-user pattern contributions with merge handling
6. **Pattern search**: Full-text search across pattern database
7. **Export capabilities**: Generate reports in multiple formats (PDF, PowerPoint)

### Scheduler Integration

Future `setup.py` enhancement to add pattern updater scheduling:

```python
def setup_pattern_updater_scheduler():
    """Configure automated pattern updates (optional)"""
    print_step(6, "Pattern Updater Automation (Optional)")
    
    response = input("Enable monthly automated pattern updates? (y/n): ")
    
    if response.lower() == 'y':
        # Platform-specific scheduler configuration
        configure_scheduler()
```

## Integration Points

### With Other Skills

1. **engagement-initiator**: Creates metadata that pattern-updater reads
2. **agenda-builder**: Can use patterns to suggest agenda items
3. **M365 Copilot**: Patterns in OneDrive become part of Copilot's context

### With External Systems

1. **OneDrive**: Primary storage for patterns and engagements
2. **Version Control** (optional): Track pattern evolution in Git
3. **Power BI** (future): Visualize pattern trends over time

## Security Considerations

1. **No credentials stored**: Uses filesystem access only
2. **Local execution**: All processing happens locally
3. **Read-only extraction**: Doesn't modify engagement metadata
4. **Configurable paths**: User controls data location via config.json

## Performance

### Expected Performance

- **Small repos** (<50 engagements): <1 second
- **Medium repos** (50-200 engagements): 1-3 seconds
- **Large repos** (200+ engagements): 3-10 seconds

### Optimization Opportunities

1. **Caching**: Cache metadata reads between runs
2. **Incremental updates**: Only process new/modified engagements
3. **Parallel processing**: Process multiple engagements concurrently
4. **Lazy loading**: Load patterns on-demand vs all at once

## Maintenance

### Regular Tasks

1. **Monthly review**: Check changelog reports for accuracy
2. **Pattern cleanup**: Merge similar patterns, remove duplicates
3. **Schema evolution**: Update data structures as needs evolve
4. **Documentation**: Keep examples current with latest patterns

### Troubleshooting

**No patterns found**:
- Verify engagements have metadata files
- Check metadata format matches expected structure
- Ensure engagements_base_path is correct

**Report generation fails**:
- Check patterns/changelog/ directory exists and is writable
- Verify no file system permissions issues
- Check disk space

**Version conflicts**:
- Manually edit success_patterns.json version if needed
- Validate JSON syntax with `python -m json.tool success_patterns.json`

## Additional Resources

- **GitHub Copilot Agent Skills**: https://code.visualstudio.com/docs/copilot/customization/agent-skills
- **OneDrive for Business**: https://www.microsoft.com/microsoft-365/onedrive/onedrive-for-business
- **Python JSON**: https://docs.python.org/3/library/json.html
- **Python Path**: https://docs.python.org/3/library/pathlib.html
