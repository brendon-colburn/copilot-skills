#!/usr/bin/env python3
"""
Pattern Updater - Main orchestrator script
Extracts patterns from engagements and updates pattern files
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from pattern_extractor import PatternExtractor
from update_patterns import PatternUpdater
from report_generator import ReportGenerator


def load_config() -> dict:
    """Load configuration from config.json"""
    # Look for config.json in repo root (3 levels up from scripts/)
    config_path = Path(__file__).parent.parent.parent.parent.parent / "config.json"
    
    if not config_path.exists():
        print(f"Error: config.json not found at {config_path}")
        print("Please run setup.py to create the configuration file.")
        sys.exit(1)
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading config.json: {e}")
        sys.exit(1)


def main():
    """Main workflow for pattern updating"""
    print("\n" + "=" * 70)
    print("PATTERN UPDATER")
    print("=" * 70 + "\n")
    
    # Load configuration
    config = load_config()
    
    engagements_path = config.get('engagements_base_path')
    if not engagements_path:
        print("Error: engagements_base_path not found in config.json")
        sys.exit(1)
    
    patterns_path = Path(engagements_path) / "patterns"
    
    if not patterns_path.exists():
        print(f"Error: Patterns directory not found at {patterns_path}")
        print("Please create the patterns directory in your OneDrive Engagements folder.")
        sys.exit(1)
    
    print(f"Engagements path: {engagements_path}")
    print(f"Patterns path: {patterns_path}\n")
    
    # Step 1: Extract patterns from engagements
    print("[1/4] Extracting patterns from engagement metadata...")
    extractor = PatternExtractor(engagements_path)
    extracted = extractor.extract_all_patterns()
    
    print(f"  ✓ Found {len(extracted['sources'])} engagements")
    print(f"  ✓ Extracted {len(extracted['engagement_types'])} engagement types")
    print(f"  ✓ Extracted {len(extracted['industries'])} industries")
    print(f"  ✓ Extracted {len(extracted['success_patterns'])} success patterns")
    print(f"  ✓ Extracted {len(extracted['discovery_frameworks'])} discovery frameworks\n")
    
    # Step 2: Compare with existing patterns
    print("[2/4] Identifying new patterns...")
    updater = PatternUpdater(str(patterns_path))
    existing_patterns = updater.read_success_patterns()
    
    if existing_patterns is None:
        print("  ✗ Failed to read existing patterns")
        sys.exit(1)
    
    new_patterns = extractor.get_new_patterns(existing_patterns, extracted)
    
    new_count = sum([
        len(new_patterns['engagement_types']),
        len(new_patterns['industries']),
        len(new_patterns['success_patterns']),
        len(new_patterns['discovery_frameworks'])
    ])
    
    if new_count == 0:
        print("  ✓ No new patterns found - all patterns are up to date!\n")
        
        # Still generate a report showing the check was performed
        generator = ReportGenerator(str(patterns_path))
        stats = {
            'engagement_types_added': 0,
            'industries_added': 0,
            'success_patterns_added': 0,
            'discovery_frameworks_added': 0
        }
        report_path = generator.generate_report(stats, {}, extracted['sources'])
        
        print("[3/4] Skipping pattern updates (no changes)")
        print(f"[4/4] Generated report: {report_path}\n")
        print(generator.generate_summary_text(stats))
        return
    
    print(f"  ✓ Found {new_count} new patterns to add:")
    if new_patterns['engagement_types']:
        print(f"    - {len(new_patterns['engagement_types'])} new engagement types")
    if new_patterns['industries']:
        print(f"    - {len(new_patterns['industries'])} new industries")
    if new_patterns['success_patterns']:
        print(f"    - {len(new_patterns['success_patterns'])} new success patterns")
    if new_patterns['discovery_frameworks']:
        print(f"    - {len(new_patterns['discovery_frameworks'])} new discovery frameworks")
    print()
    
    # Step 3: Apply updates
    print("[3/4] Updating pattern files...")
    results = updater.apply_updates(new_patterns, extracted['sources'])
    
    if not results['success']:
        print(f"  ✗ Update failed: {results.get('error', 'Unknown error')}")
        sys.exit(1)
    
    for file in results['files_updated']:
        print(f"  ✓ Updated {file}")
    print()
    
    # Step 4: Generate report
    print("[4/4] Generating changelog report...")
    generator = ReportGenerator(str(patterns_path))
    report_path = generator.generate_report(
        results['stats'],
        new_patterns,
        extracted['sources']
    )
    
    if report_path:
        print(f"  ✓ Report generated: {report_path}\n")
    else:
        print("  ⚠ Warning: Failed to generate report\n")
    
    # Print summary
    print(generator.generate_summary_text(results['stats']))
    
    print("\n✅ Pattern update complete!\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPattern update cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
