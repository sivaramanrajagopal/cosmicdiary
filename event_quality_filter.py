#!/usr/bin/env python3
"""
Event Quality Filter Module

Applies strict quality controls to filter out trivial events before database storage.
Uses configuration from config/event_filters.json for flexible filtering.

Author: Cosmic Diary System
Date: 2024-12-16
"""

import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from difflib import SequenceMatcher

# Load filter configuration
CONFIG_PATH = Path(__file__).parent / 'config' / 'event_filters.json'

def load_filter_config() -> Dict:
    """Load event filtering configuration from JSON file."""
    try:
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
        print(f"✓ Loaded event filter configuration from {CONFIG_PATH}")
        return config
    except FileNotFoundError:
        print(f"⚠️  Filter config not found at {CONFIG_PATH}, using defaults")
        return get_default_config()
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing filter config: {e}")
        print("   Using default configuration")
        return get_default_config()


def get_default_config() -> Dict:
    """Return default filter configuration if config file not found."""
    return {
        "filtering_mode": {"enabled": True, "mode": "balanced"},
        "impact_level_filters": {
            "minimum_impact_level": "medium",
            "allowed_levels": ["medium", "high", "critical"]
        },
        "quality_scoring": {"enabled": True, "minimum_research_score": 40},
        "deduplication": {"enabled": True, "similarity_threshold": 0.85},
        "collection_limits": {"max_events_per_run": 15}
    }


class EventQualityFilter:
    """
    Filters events based on quality, significance, and astrological relevance.
    """

    def __init__(self, config: Dict = None):
        """
        Initialize filter with configuration.

        Args:
            config: Filter configuration dict. If None, loads from file.
        """
        self.config = config or load_filter_config()
        self.filtering_enabled = self.config.get('filtering_mode', {}).get('enabled', True)
        self.mode = self.config.get('filtering_mode', {}).get('mode', 'balanced')

        print(f"🔍 Event Quality Filter initialized")
        print(f"   Mode: {self.mode}")
        print(f"   Filtering: {'ENABLED' if self.filtering_enabled else 'DISABLED'}")
        print("")

    def filter_events(self, events: List[Dict], existing_events: List[Dict] = None) -> Tuple[List[Dict], Dict]:
        """
        Apply all filtering rules to a list of events.

        Args:
            events: List of event dictionaries from OpenAI
            existing_events: List of recent events from database for deduplication

        Returns:
            Tuple of (filtered_events, filter_stats)
        """
        if not self.filtering_enabled:
            print("⚠️  Filtering is DISABLED - returning all events")
            return events, {"total": len(events), "filtered": len(events), "rejected": 0}

        print("=" * 80)
        print("APPLYING EVENT QUALITY FILTERS")
        print("=" * 80)
        print(f"Input: {len(events)} events from OpenAI")
        print(f"Mode: {self.mode.upper()}")
        print("")

        filtered_events = []
        filter_stats = {
            'total': len(events),
            'filtered': 0,
            'rejected': 0,
            'rejection_reasons': {}
        }

        for i, event in enumerate(events, 1):
            # Apply all filter checks
            passed, reason = self._apply_filters(event, existing_events)

            if passed:
                filtered_events.append(event)
                filter_stats['filtered'] += 1
            else:
                filter_stats['rejected'] += 1
                filter_stats['rejection_reasons'][reason] = \
                    filter_stats['rejection_reasons'].get(reason, 0) + 1

                # Log rejected events (first 5 only)
                if filter_stats['rejected'] <= 5:
                    print(f"  ✗ Rejected {i}/{len(events)}: {event.get('title', 'N/A')[:60]}")
                    print(f"    Reason: {reason}")

        # Check collection limits
        max_events = self.config.get('collection_limits', {}).get('max_events_per_run', 15)
        if len(filtered_events) > max_events:
            print(f"\n⚠️  {len(filtered_events)} events passed filters, limiting to {max_events}")
            filtered_events = self._prioritize_events(filtered_events)[:max_events]

        print("")
        print("=" * 80)
        print("FILTERING RESULTS")
        print("=" * 80)
        print(f"✓ Accepted: {len(filtered_events)} events")
        print(f"✗ Rejected: {filter_stats['rejected']} events")

        if filter_stats['rejection_reasons']:
            print("\n📊 Rejection Breakdown:")
            for reason, count in sorted(filter_stats['rejection_reasons'].items(),
                                       key=lambda x: x[1], reverse=True):
                print(f"   - {reason}: {count}")

        print("=" * 80)
        print("")

        return filtered_events, filter_stats

    def _apply_filters(self, event: Dict, existing_events: List[Dict] = None) -> Tuple[bool, str]:
        """
        Apply all filter rules to a single event.

        Returns:
            Tuple of (passed: bool, rejection_reason: str)
        """
        # 1. Impact Level Filter
        if not self._check_impact_level(event):
            return False, f"Impact level '{event.get('impact_level')}' below threshold"

        # 2. Category Filter
        if not self._check_category(event):
            return False, f"Category '{event.get('category')}' is disabled"

        # 3. Impact Metrics Filter
        if not self._check_impact_metrics(event):
            return False, "Impact metrics below threshold"

        # 4. Geographic Scope Filter
        if not self._check_geographic_scope(event):
            return False, "Geographic scope too narrow"

        # 5. Keyword Blacklist Filter
        if not self._check_keyword_blacklist(event):
            return False, "Contains blacklisted keywords"

        # 6. Quality Scoring Filter
        if not self._check_quality_score(event):
            return False, f"Research score {event.get('research_score', 0)} below threshold"

        # 7. Validation Rules
        if not self._check_validation_rules(event):
            return False, "Failed validation rules (missing required fields)"

        # 8. Time Window Filter
        if not self._check_time_window(event):
            return False, "Event too old"

        # 9. Deduplication Filter
        if existing_events and not self._check_deduplication(event, existing_events):
            return False, "Duplicate event (already in database)"

        return True, "Passed all filters"

    def _check_impact_level(self, event: Dict) -> bool:
        """Check if event meets minimum impact level requirement."""
        impact_config = self.config.get('impact_level_filters', {})
        min_level = impact_config.get('minimum_impact_level', 'medium')
        allowed_levels = impact_config.get('allowed_levels', ['medium', 'high', 'critical'])

        event_impact = event.get('impact_level', 'low')

        # Special rules: Always allow critical events
        special_rules = self.config.get('special_rules', {})
        if special_rules.get('always_allow_critical', True) and event_impact == 'critical':
            return True

        return event_impact in allowed_levels

    def _check_category(self, event: Dict) -> bool:
        """Check if event category is enabled."""
        category_config = self.config.get('category_filters', {})
        enabled_categories = category_config.get('enabled_categories', [])
        disabled_categories = category_config.get('disabled_categories', [])

        event_category = event.get('category', '')

        # Special rules: Always allow certain categories
        special_rules = self.config.get('special_rules', {})
        category_lower = event_category.lower()

        if special_rules.get('always_allow_natural_disasters', True) and 'disaster' in category_lower:
            return True
        if special_rules.get('always_allow_wars_conflicts', True) and ('war' in category_lower or 'conflict' in category_lower):
            return True
        if special_rules.get('always_allow_economic_crises', True) and 'economic' in category_lower and event.get('impact_level') in ['high', 'critical']:
            return True

        # Check if category is explicitly disabled
        if event_category in disabled_categories:
            # Allow if critical impact
            if event.get('impact_level') == 'critical':
                return True
            return False

        # If enabled_categories is empty, allow all (except disabled)
        if not enabled_categories:
            return True

        return event_category in enabled_categories

    def _check_impact_metrics(self, event: Dict) -> bool:
        """Check if event meets impact metric thresholds."""
        metrics_config = self.config.get('impact_metrics_thresholds', {})
        event_impact = event.get('impact_level', 'low')
        event_metrics = event.get('impact_metrics', {})

        # Get thresholds for this impact level
        level_key = f"{event_impact}_level"
        thresholds = metrics_config.get(level_key, {})

        if not thresholds:
            # No thresholds defined for this level, allow it
            return True

        # Check if event meets AT LEAST ONE threshold
        deaths = event_metrics.get('deaths') or 0
        injured = event_metrics.get('injured') or 0
        affected = event_metrics.get('affected') or 0
        financial = event_metrics.get('financial_impact_usd') or 0

        meets_deaths = deaths >= thresholds.get('deaths_min', float('inf'))
        meets_injured = injured >= thresholds.get('injured_min', float('inf'))
        meets_affected = affected >= thresholds.get('affected_min', float('inf'))
        meets_financial = financial >= thresholds.get('financial_impact_usd_min', float('inf'))

        # If any metric meets threshold, pass
        if meets_deaths or meets_injured or meets_affected or meets_financial:
            return True

        # For low impact, check if astrologically significant
        if event_impact == 'low':
            if thresholds.get('allow_if_astrologically_significant', False):
                astro = event.get('astrological_relevance', {})
                if astro.get('primary_houses') and astro.get('primary_planets'):
                    return True

        # If no metrics provided, allow (assume OpenAI judged it significant)
        if not any([deaths, injured, affected, financial]):
            return True

        return False

    def _check_geographic_scope(self, event: Dict) -> bool:
        """Check if event meets geographic scope requirements."""
        geo_config = self.config.get('geographic_filters', {})
        if not geo_config.get('enabled', True):
            return True

        event_metrics = event.get('impact_metrics', {})
        geo_scope = event_metrics.get('geographic_scope', 'unknown')
        min_scope = geo_config.get('minimum_geographic_scope', 'state')

        # Scope hierarchy: local < state < national < international
        scope_hierarchy = ['local', 'state', 'national', 'international']

        # Allow if critical impact
        if event.get('impact_level') == 'critical':
            return True

        # Unknown scope - allow if other metrics are good
        if geo_scope == 'unknown':
            return True

        try:
            event_scope_index = scope_hierarchy.index(geo_scope)
            min_scope_index = scope_hierarchy.index(min_scope)
            return event_scope_index >= min_scope_index
        except ValueError:
            # Invalid scope value, allow
            return True

    def _check_keyword_blacklist(self, event: Dict) -> bool:
        """Check if event contains blacklisted keywords."""
        keyword_config = self.config.get('keyword_filters', {}).get('blacklist', {})
        if not keyword_config.get('enabled', True):
            return True

        blacklist = keyword_config.get('keywords', [])
        if not blacklist:
            return True

        # Combine title and description for checking
        text = f"{event.get('title', '')} {event.get('description', '')}".lower()

        for keyword in blacklist:
            if keyword.lower() in text:
                # Allow if critical impact
                if event.get('impact_level') == 'critical':
                    return True
                return False

        return True

    def _check_quality_score(self, event: Dict) -> bool:
        """Check if event meets minimum research quality score."""
        scoring_config = self.config.get('quality_scoring', {})
        if not scoring_config.get('enabled', True):
            return True

        min_score = scoring_config.get('minimum_research_score', 40)
        event_score = event.get('research_score', 0)

        return event_score >= min_score

    def _check_validation_rules(self, event: Dict) -> bool:
        """Check if event meets basic validation rules."""
        validation_config = self.config.get('validation_rules', {})

        # Check required fields
        if validation_config.get('require_title', True) and not event.get('title'):
            return False
        if validation_config.get('require_date', True) and not event.get('date'):
            return False
        if validation_config.get('require_description', True) and not event.get('description'):
            return False
        if validation_config.get('require_location', True) and not event.get('location'):
            return False
        if validation_config.get('require_category', True) and not event.get('category'):
            return False

        # Check description length
        desc = event.get('description', '')
        min_desc = validation_config.get('min_description_length', 100)
        max_desc = validation_config.get('max_description_length', 1000)
        if len(desc) < min_desc or len(desc) > max_desc:
            return False

        # Check title length
        title = event.get('title', '')
        min_title = validation_config.get('min_title_length', 10)
        max_title = validation_config.get('max_title_length', 150)
        if len(title) < min_title or len(title) > max_title:
            return False

        return True

    def _check_time_window(self, event: Dict) -> bool:
        """Check if event is within acceptable time window."""
        time_config = self.config.get('time_window_filters', {})
        if not time_config.get('enabled', True):
            return True

        max_age_hours = time_config.get('max_event_age_hours', 72)
        event_date_str = event.get('date')

        if not event_date_str:
            return True  # No date to check

        try:
            event_date = datetime.strptime(event_date_str, '%Y-%m-%d')
            age_hours = (datetime.now() - event_date).total_seconds() / 3600
            return age_hours <= max_age_hours
        except ValueError:
            return True  # Invalid date format, allow

    def _check_deduplication(self, event: Dict, existing_events: List[Dict]) -> bool:
        """Check if event is a duplicate of existing events."""
        dedup_config = self.config.get('deduplication', {})
        if not dedup_config.get('enabled', True):
            return True

        if not existing_events:
            return True

        threshold = dedup_config.get('similarity_threshold', 0.85)
        check_hours = dedup_config.get('check_within_hours', 48)

        event_title = event.get('title', '').lower()
        event_date_str = event.get('date', '')

        try:
            event_date = datetime.strptime(event_date_str, '%Y-%m-%d')
        except ValueError:
            return True  # Can't check date, allow

        for existing in existing_events:
            # Check date proximity
            try:
                existing_date = datetime.strptime(existing.get('date', ''), '%Y-%m-%d')
                hours_diff = abs((event_date - existing_date).total_seconds() / 3600)

                if hours_diff <= check_hours:
                    # Check title similarity
                    existing_title = existing.get('title', '').lower()
                    similarity = SequenceMatcher(None, event_title, existing_title).ratio()

                    if similarity >= threshold:
                        return False  # Duplicate found
            except ValueError:
                continue

        return True  # Not a duplicate

    def _prioritize_events(self, events: List[Dict]) -> List[Dict]:
        """Sort events by priority (research score, impact level)."""
        # Priority order: critical > high > medium > low
        impact_priority = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}

        def get_priority(event):
            impact = impact_priority.get(event.get('impact_level', 'low'), 0)
            score = event.get('research_score', 0)
            return (impact * 100) + score

        return sorted(events, key=get_priority, reverse=True)


def apply_event_filters(events: List[Dict], existing_events: List[Dict] = None,
                       config: Dict = None) -> Tuple[List[Dict], Dict]:
    """
    Convenience function to apply event filters.

    Args:
        events: List of events from OpenAI
        existing_events: List of recent events from database for deduplication
        config: Optional filter configuration dict

    Returns:
        Tuple of (filtered_events, filter_stats)
    """
    filter_instance = EventQualityFilter(config=config)
    return filter_instance.filter_events(events, existing_events)


if __name__ == '__main__':
    # Test the filter with sample data
    print("=" * 80)
    print("EVENT QUALITY FILTER - TEST MODE")
    print("=" * 80)
    print("")

    sample_events = [
        {
            "title": "Major earthquake hits California",
            "date": "2024-12-15",
            "description": "A 7.2 magnitude earthquake struck Southern California, causing widespread damage and affecting over 500,000 residents. Multiple buildings collapsed and emergency services are responding.",
            "category": "Natural Disasters",
            "location": "Los Angeles, California, United States",
            "impact_level": "critical",
            "impact_metrics": {
                "deaths": 15,
                "injured": 200,
                "affected": 500000,
                "financial_impact_usd": 2000000000,
                "geographic_scope": "state"
            },
            "research_score": 85
        },
        {
            "title": "Celebrity spotted at coffee shop",
            "date": "2024-12-16",
            "description": "Famous actor seen enjoying coffee at local cafe. Fans were excited to see the star in casual attire. Photos went viral on social media.",
            "category": "Entertainment & Sports",
            "location": "Mumbai, Maharashtra, India",
            "impact_level": "low",
            "impact_metrics": {},
            "research_score": 15
        }
    ]

    filter_instance = EventQualityFilter()
    filtered, stats = filter_instance.filter_events(sample_events)

    print(f"\nFinal Results:")
    print(f"  Input: {len(sample_events)} events")
    print(f"  Output: {len(filtered)} events")
    print(f"  Rejected: {stats['rejected']} events")
