#!/usr/bin/env python3
"""
Report Generator - Generate changelog reports for pattern updates
Creates markdown reports in patterns/changelog/ directory
"""

import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List


class ReportGenerator:
    """Generates changelog reports for pattern updates"""
    
    def __init__(self, patterns_path: str):
        """
        Initialize report generator
        
        Args:
            patterns_path: Path to patterns directory
        """
        self.patterns_path = Path(patterns_path)
        self.changelog_path = self.patterns_path / "changelog"
        
        # Create changelog directory if it doesn't exist
        self.changelog_path.mkdir(parents=True, exist_ok=True)
    
    def generate_report(self, 
                       update_stats: Dict, 
                       new_patterns: Dict,
                       extracted_sources: List[Dict],
                       report_date: datetime = None) -> str:
        """
        Generate changelog report
        
        Args:
            update_stats: Statistics from update operation
            new_patterns: New patterns that were added
            extracted_sources: Source engagements analyzed
            report_date: Date for the report (defaults to now)
        
        Returns:
            Path to generated report file
        """
        if report_date is None:
            report_date = datetime.now()
        
        # Generate filename: YYYY-MM.md
        filename = f"{report_date.strftime('%Y-%m')}.md"
        report_path = self.changelog_path / filename
        
        # Build report content
        content = self._build_report_content(
            report_date, 
            update_stats, 
            new_patterns, 
            extracted_sources
        )
        
        # Write report
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return str(report_path)
        except IOError as e:
            print(f"Error writing report: {e}")
            return None
    
    def _build_report_content(self,
                             report_date: datetime,
                             update_stats: Dict,
                             new_patterns: Dict,
                             extracted_sources: List[Dict]) -> str:
        """Build markdown content for the report"""
        
        lines = []
        
        # Header
        lines.append(f"# Pattern Update Report - {report_date.strftime('%B %Y')}")
        lines.append(f"\n**Generated**: {report_date.strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Summary section
        lines.append("## Summary\n")
        
        total_added = sum([
            update_stats.get('engagement_types_added', 0),
            update_stats.get('industries_added', 0),
            update_stats.get('success_patterns_added', 0),
            update_stats.get('discovery_frameworks_added', 0)
        ])
        
        lines.append(f"- **Total Patterns Added**: {total_added}")
        lines.append(f"- **Engagement Types**: {update_stats.get('engagement_types_added', 0)} added")
        lines.append(f"- **Industries**: {update_stats.get('industries_added', 0)} added")
        lines.append(f"- **Success Patterns**: {update_stats.get('success_patterns_added', 0)} added")
        lines.append(f"- **Discovery Frameworks**: {update_stats.get('discovery_frameworks_added', 0)} added")
        lines.append(f"- **Source Engagements Analyzed**: {len(extracted_sources)}\n")
        
        # Detail sections
        if new_patterns.get('engagement_types'):
            lines.append("## New Engagement Types\n")
            for eng_type in new_patterns['engagement_types']:
                lines.append(f"### {eng_type.get('name', eng_type['id'])}")
                lines.append(f"**ID**: `{eng_type['id']}`\n")
                if 'description' in eng_type:
                    lines.append(f"{eng_type['description']}\n")
        
        if new_patterns.get('industries'):
            lines.append("## New Industry Patterns\n")
            for industry in new_patterns['industries']:
                lines.append(f"### {industry.get('name', industry['id'])}")
                lines.append(f"**ID**: `{industry['id']}`\n")
                if 'description' in industry:
                    lines.append(f"{industry['description']}\n")
        
        if new_patterns.get('success_patterns'):
            lines.append("## New Success Patterns\n")
            for pattern in new_patterns['success_patterns']:
                lines.append(f"- **{pattern['id']}**: {pattern.get('description', 'N/A')}")
        
        if new_patterns.get('discovery_frameworks'):
            lines.append("\n## New Discovery Frameworks\n")
            for framework in new_patterns['discovery_frameworks']:
                lines.append(f"### {framework.get('name', framework['id'])}")
                lines.append(f"**ID**: `{framework['id']}`\n")
                if 'description' in framework:
                    lines.append(f"{framework['description']}\n")
        
        # Source engagements section
        if extracted_sources:
            lines.append("## Source Engagements\n")
            lines.append("Patterns extracted from the following engagements:\n")
            for source in extracted_sources:
                customer = source.get('customer', 'Unknown')
                date = source.get('date', 'Unknown')
                folder = source.get('folder', 'Unknown')
                lines.append(f"- **{customer}** ({date}) - `{folder}`")
        
        # Footer
        lines.append("\n---\n")
        lines.append("*This report was automatically generated by the pattern-updater skill.*\n")
        
        return "\n".join(lines)
    
    def generate_summary_text(self, update_stats: Dict) -> str:
        """
        Generate a brief text summary for console output
        
        Args:
            update_stats: Statistics from update operation
        
        Returns:
            Summary text
        """
        total_added = sum([
            update_stats.get('engagement_types_added', 0),
            update_stats.get('industries_added', 0),
            update_stats.get('success_patterns_added', 0),
            update_stats.get('discovery_frameworks_added', 0)
        ])
        
        lines = [
            "=" * 70,
            "PATTERN UPDATE SUMMARY",
            "=" * 70,
            "",
            f"Total patterns added: {total_added}",
            "",
            f"  Engagement Types: {update_stats.get('engagement_types_added', 0)}",
            f"  Industries: {update_stats.get('industries_added', 0)}",
            f"  Success Patterns: {update_stats.get('success_patterns_added', 0)}",
            f"  Discovery Frameworks: {update_stats.get('discovery_frameworks_added', 0)}",
            ""
        ]
        
        if total_added == 0:
            lines.append("✓ All patterns are up to date - no new patterns found")
        else:
            lines.append(f"✓ Successfully added {total_added} new patterns")
        
        lines.append("=" * 70)
        
        return "\n".join(lines)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python report_generator.py <patterns_path>")
        sys.exit(1)
    
    patterns_path = sys.argv[1]
    
    # Test report generation
    generator = ReportGenerator(patterns_path)
    
    # Sample data
    test_stats = {
        'engagement_types_added': 2,
        'industries_added': 1,
        'success_patterns_added': 3,
        'discovery_frameworks_added': 1
    }
    
    test_patterns = {
        'engagement_types': [
            {'id': 'test_type', 'name': 'Test Type', 'description': 'A test type'}
        ]
    }
    
    test_sources = [
        {'customer': 'Test Customer', 'date': '2026-01-01', 'folder': 'Test-2026-01-01'}
    ]
    
    report_path = generator.generate_report(test_stats, test_patterns, test_sources)
    
    if report_path:
        print(f"\n✓ Test report generated: {report_path}\n")
        print(generator.generate_summary_text(test_stats))
    else:
        print("\n✗ Failed to generate test report")
