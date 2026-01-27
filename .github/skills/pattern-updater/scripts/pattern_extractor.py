#!/usr/bin/env python3
"""
Pattern Extractor - Extract patterns from engagement metadata
Reads engagement metadata files and identifies patterns for success_patterns.json
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Set


class PatternExtractor:
    """Extracts patterns from engagement metadata files"""
    
    def __init__(self, engagements_path: str):
        """
        Initialize pattern extractor
        
        Args:
            engagements_path: Path to engagements base directory
        """
        self.engagements_path = Path(engagements_path)
        
    def find_engagement_folders(self) -> List[Path]:
        """Find all engagement folders in the base path"""
        if not self.engagements_path.exists():
            return []
        
        # Engagement folders typically follow pattern: Customer-YYYY-MM-DD
        engagement_folders = []
        for item in self.engagements_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                # Check if folder has metadata file
                metadata_file = item / "engagement_metadata.json"
                if metadata_file.exists():
                    engagement_folders.append(item)
        
        return engagement_folders
    
    def read_metadata(self, folder_path: Path) -> Optional[Dict]:
        """Read engagement metadata from folder"""
        metadata_file = folder_path / "engagement_metadata.json"
        
        if not metadata_file.exists():
            return None
        
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error reading {metadata_file}: {e}")
            return None
    
    def extract_engagement_type(self, metadata: Dict) -> Optional[str]:
        """Extract engagement type from metadata"""
        # Try multiple field names
        for field in ['engagement_type', 'type', 'session_type']:
            if field in metadata:
                return metadata[field]
        return None
    
    def extract_industry(self, metadata: Dict) -> Optional[str]:
        """Extract industry from metadata"""
        for field in ['industry', 'customer_industry', 'sector']:
            if field in metadata:
                return metadata[field]
        return None
    
    def extract_success_indicators(self, metadata: Dict) -> List[str]:
        """Extract success indicators from metadata"""
        indicators = []
        
        # Check for explicit success factors
        if 'success_factors' in metadata:
            factors = metadata['success_factors']
            if isinstance(factors, list):
                indicators.extend(factors)
            elif isinstance(factors, str):
                indicators.append(factors)
        
        # Check for outcomes
        if 'outcomes' in metadata:
            outcomes = metadata['outcomes']
            if isinstance(outcomes, list):
                indicators.extend(outcomes)
            elif isinstance(outcomes, str):
                indicators.append(outcomes)
        
        # Check for key learnings
        if 'key_learnings' in metadata:
            learnings = metadata['key_learnings']
            if isinstance(learnings, list):
                indicators.extend(learnings)
            elif isinstance(learnings, str):
                indicators.append(learnings)
        
        return indicators
    
    def extract_discovery_frameworks(self, metadata: Dict) -> List[str]:
        """Extract discovery frameworks used from metadata"""
        frameworks = []
        
        if 'discovery_framework' in metadata:
            fw = metadata['discovery_framework']
            if isinstance(fw, list):
                frameworks.extend(fw)
            elif isinstance(fw, str):
                frameworks.append(fw)
        
        if 'discovery_approach' in metadata:
            approach = metadata['discovery_approach']
            if isinstance(approach, list):
                frameworks.extend(approach)
            elif isinstance(approach, str):
                frameworks.append(approach)
        
        return frameworks
    
    def extract_all_patterns(self) -> Dict:
        """
        Extract all patterns from engagement folders
        
        Returns:
            Dict with extracted patterns
        """
        engagement_folders = self.find_engagement_folders()
        
        extracted = {
            'engagement_types': set(),
            'industries': set(),
            'success_patterns': set(),
            'discovery_frameworks': set(),
            'sources': []
        }
        
        for folder in engagement_folders:
            metadata = self.read_metadata(folder)
            if not metadata:
                continue
            
            # Extract engagement type
            eng_type = self.extract_engagement_type(metadata)
            if eng_type:
                extracted['engagement_types'].add(eng_type)
            
            # Extract industry
            industry = self.extract_industry(metadata)
            if industry:
                extracted['industries'].add(industry)
            
            # Extract success indicators
            success = self.extract_success_indicators(metadata)
            for item in success:
                extracted['success_patterns'].add(item)
            
            # Extract discovery frameworks
            frameworks = self.extract_discovery_frameworks(metadata)
            for fw in frameworks:
                extracted['discovery_frameworks'].add(fw)
            
            # Add source
            extracted['sources'].append({
                'folder': folder.name,
                'customer': metadata.get('customer', 'Unknown'),
                'date': metadata.get('engagement_date', 'Unknown')
            })
        
        # Convert sets to sorted lists
        return {
            'engagement_types': sorted(list(extracted['engagement_types'])),
            'industries': sorted(list(extracted['industries'])),
            'success_patterns': sorted(list(extracted['success_patterns'])),
            'discovery_frameworks': sorted(list(extracted['discovery_frameworks'])),
            'sources': extracted['sources']
        }
    
    def get_new_patterns(self, existing_patterns: Dict, extracted_patterns: Dict) -> Dict:
        """
        Compare extracted patterns with existing ones to find new patterns
        
        Args:
            existing_patterns: Current patterns from success_patterns.json
            extracted_patterns: Newly extracted patterns
        
        Returns:
            Dict with new patterns only
        """
        new_patterns = {
            'engagement_types': [],
            'industries': [],
            'success_patterns': [],
            'discovery_frameworks': []
        }
        
        # Find new engagement types
        existing_types = set([t['id'] for t in existing_patterns.get('engagement_types', [])])
        for eng_type in extracted_patterns['engagement_types']:
            # Create id from type name
            type_id = eng_type.lower().replace(' ', '_').replace('-', '_')
            if type_id not in existing_types:
                new_patterns['engagement_types'].append({
                    'id': type_id,
                    'name': eng_type
                })
        
        # Find new industries
        existing_industries = set([i['id'] for i in existing_patterns.get('industry_patterns', [])])
        for industry in extracted_patterns['industries']:
            industry_id = industry.lower().replace(' ', '_').replace('-', '_')
            if industry_id not in existing_industries:
                new_patterns['industries'].append({
                    'id': industry_id,
                    'name': industry
                })
        
        # Find new success patterns
        existing_success = set([s['id'] for s in existing_patterns.get('success_patterns', [])])
        for pattern in extracted_patterns['success_patterns']:
            pattern_id = pattern.lower().replace(' ', '_').replace('-', '_')[:50]
            if pattern_id not in existing_success:
                new_patterns['success_patterns'].append({
                    'id': pattern_id,
                    'description': pattern
                })
        
        # Find new discovery frameworks
        existing_discovery = set([d['id'] for d in existing_patterns.get('discovery_frameworks', [])])
        for framework in extracted_patterns['discovery_frameworks']:
            framework_id = framework.lower().replace(' ', '_').replace('-', '_')[:50]
            if framework_id not in existing_discovery:
                new_patterns['discovery_frameworks'].append({
                    'id': framework_id,
                    'name': framework
                })
        
        return new_patterns


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python pattern_extractor.py <engagements_path>")
        sys.exit(1)
    
    engagements_path = sys.argv[1]
    
    extractor = PatternExtractor(engagements_path)
    patterns = extractor.extract_all_patterns()
    
    print("\n" + "=" * 70)
    print("EXTRACTED PATTERNS")
    print("=" * 70 + "\n")
    
    print(f"Engagement Types ({len(patterns['engagement_types'])}):")
    for et in patterns['engagement_types']:
        print(f"  - {et}")
    
    print(f"\nIndustries ({len(patterns['industries'])}):")
    for ind in patterns['industries']:
        print(f"  - {ind}")
    
    print(f"\nSuccess Patterns ({len(patterns['success_patterns'])}):")
    for sp in patterns['success_patterns'][:10]:  # Show first 10
        print(f"  - {sp}")
    if len(patterns['success_patterns']) > 10:
        print(f"  ... and {len(patterns['success_patterns']) - 10} more")
    
    print(f"\nDiscovery Frameworks ({len(patterns['discovery_frameworks'])}):")
    for df in patterns['discovery_frameworks']:
        print(f"  - {df}")
    
    print(f"\nSources: {len(patterns['sources'])} engagements analyzed")
