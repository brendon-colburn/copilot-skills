#!/usr/bin/env python3
"""
Pattern Updater - Update pattern files with new patterns
Updates success_patterns.json and related markdown files
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List


class PatternUpdater:
    """Updates pattern files with newly extracted patterns"""
    
    def __init__(self, patterns_path: str):
        """
        Initialize pattern updater
        
        Args:
            patterns_path: Path to patterns directory
        """
        self.patterns_path = Path(patterns_path)
        self.success_patterns_file = self.patterns_path / "success_patterns.json"
        self.engagement_types_file = self.patterns_path / "engagement_types.md"
        self.discovery_patterns_file = self.patterns_path / "discovery_patterns.md"
        self.delivery_patterns_file = self.patterns_path / "delivery_patterns.md"
    
    def read_success_patterns(self) -> Dict:
        """Read current success_patterns.json"""
        if not self.success_patterns_file.exists():
            return {
                "version": "1.0",
                "last_updated": datetime.now().strftime("%Y-%m-%d"),
                "sources": [],
                "engagement_types": [],
                "success_patterns": [],
                "industry_patterns": [],
                "discovery_frameworks": []
            }
        
        try:
            with open(self.success_patterns_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error reading success_patterns.json: {e}")
            return None
    
    def write_success_patterns(self, patterns: Dict) -> bool:
        """Write updated success_patterns.json"""
        try:
            with open(self.success_patterns_file, 'w', encoding='utf-8') as f:
                json.dump(patterns, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error writing success_patterns.json: {e}")
            return False
    
    def update_success_patterns_json(self, new_patterns: Dict, extracted_sources: List[Dict]) -> Dict:
        """
        Update success_patterns.json with new patterns
        
        Args:
            new_patterns: New patterns to add
            extracted_sources: List of source engagements
        
        Returns:
            Dict with update statistics
        """
        current = self.read_success_patterns()
        if current is None:
            return {'error': 'Failed to read current patterns'}
        
        stats = {
            'engagement_types_added': 0,
            'industries_added': 0,
            'success_patterns_added': 0,
            'discovery_frameworks_added': 0
        }
        
        # Update engagement types
        if new_patterns.get('engagement_types'):
            current.setdefault('engagement_types', [])
            for new_type in new_patterns['engagement_types']:
                current['engagement_types'].append(new_type)
                stats['engagement_types_added'] += 1
        
        # Update industry patterns
        if new_patterns.get('industries'):
            current.setdefault('industry_patterns', [])
            for new_industry in new_patterns['industries']:
                current['industry_patterns'].append(new_industry)
                stats['industries_added'] += 1
        
        # Update success patterns
        if new_patterns.get('success_patterns'):
            current.setdefault('success_patterns', [])
            for new_pattern in new_patterns['success_patterns']:
                current['success_patterns'].append(new_pattern)
                stats['success_patterns_added'] += 1
        
        # Update discovery frameworks
        if new_patterns.get('discovery_frameworks'):
            current.setdefault('discovery_frameworks', [])
            for new_framework in new_patterns['discovery_frameworks']:
                current['discovery_frameworks'].append(new_framework)
                stats['discovery_frameworks_added'] += 1
        
        # Update metadata
        current['last_updated'] = datetime.now().strftime("%Y-%m-%d")
        
        # Update version (increment minor version)
        if 'version' in current:
            version_parts = current['version'].split('.')
            if len(version_parts) >= 2:
                try:
                    minor = int(version_parts[1])
                    current['version'] = f"{version_parts[0]}.{minor + 1}"
                except ValueError:
                    pass
        
        # Update sources count
        current['sources'] = len(extracted_sources)
        
        # Write updated patterns
        if self.write_success_patterns(current):
            return stats
        else:
            return {'error': 'Failed to write updated patterns'}
    
    def update_engagement_types_md(self, new_types: List[Dict]) -> bool:
        """Update engagement_types.md with new types"""
        if not new_types:
            return True
        
        if not self.engagement_types_file.exists():
            print(f"Warning: {self.engagement_types_file} does not exist")
            return False
        
        try:
            with open(self.engagement_types_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Use consistent timestamp
            update_date = datetime.now().strftime('%Y-%m-%d')
            
            # Find the section to append new types
            # This is simplified - in a real implementation, you'd parse the markdown structure
            new_content = f"\n\n## Newly Added Types ({update_date})\n\n"
            
            for eng_type in new_types:
                new_content += f"### {eng_type.get('name', eng_type.get('id'))}\n\n"
                new_content += f"**ID**: `{eng_type['id']}`\n\n"
                if 'description' in eng_type:
                    new_content += f"{eng_type['description']}\n\n"
                else:
                    new_content += "Description to be added.\n\n"
            
            # Append to file
            with open(self.engagement_types_file, 'a', encoding='utf-8') as f:
                f.write(new_content)
            
            return True
        except IOError as e:
            print(f"Error updating engagement_types.md: {e}")
            return False
    
    def update_discovery_patterns_md(self, new_frameworks: List[Dict]) -> bool:
        """Update discovery_patterns.md with new frameworks"""
        if not new_frameworks:
            return True
        
        if not self.discovery_patterns_file.exists():
            print(f"Warning: {self.discovery_patterns_file} does not exist")
            return False
        
        try:
            # Use consistent timestamp
            update_date = datetime.now().strftime('%Y-%m-%d')
            
            new_content = f"\n\n## Newly Added Frameworks ({update_date})\n\n"
            
            for framework in new_frameworks:
                new_content += f"### {framework.get('name', framework.get('id'))}\n\n"
                new_content += f"**ID**: `{framework['id']}`\n\n"
                if 'description' in framework:
                    new_content += f"{framework['description']}\n\n"
                else:
                    new_content += "Framework details to be added.\n\n"
            
            # Append to file
            with open(self.discovery_patterns_file, 'a', encoding='utf-8') as f:
                f.write(new_content)
            
            return True
        except IOError as e:
            print(f"Error updating discovery_patterns.md: {e}")
            return False
    
    def apply_updates(self, new_patterns: Dict, extracted_sources: List[Dict]) -> Dict:
        """
        Apply all pattern updates
        
        Args:
            new_patterns: New patterns to add
            extracted_sources: List of source engagements
        
        Returns:
            Dict with comprehensive update statistics
        """
        results = {
            'success': True,
            'stats': {},
            'files_updated': []
        }
        
        # Update success_patterns.json
        stats = self.update_success_patterns_json(new_patterns, extracted_sources)
        if 'error' in stats:
            results['success'] = False
            results['error'] = stats['error']
            return results
        
        results['stats'] = stats
        results['files_updated'].append('success_patterns.json')
        
        # Update engagement_types.md
        if new_patterns.get('engagement_types'):
            if self.update_engagement_types_md(new_patterns['engagement_types']):
                results['files_updated'].append('engagement_types.md')
        
        # Update discovery_patterns.md
        if new_patterns.get('discovery_frameworks'):
            if self.update_discovery_patterns_md(new_patterns['discovery_frameworks']):
                results['files_updated'].append('discovery_patterns.md')
        
        return results


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python update_patterns.py <patterns_path>")
        sys.exit(1)
    
    patterns_path = sys.argv[1]
    
    # This is a test - normally called from main script
    print(f"Pattern updater initialized for: {patterns_path}")
    print("This script is meant to be called from the main pattern update workflow.")
