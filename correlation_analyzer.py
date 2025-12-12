"""
Correlation Analyzer Module for Event-Cosmic Snapshot Matching

This module compares an event's astrological chart with cosmic snapshots
to find matching planetary patterns and calculate correlation scores.
Used for identifying which planetary states correlate with specific events.

Author: Cosmic Diary System
Date: 2025-12-12
"""

from typing import Dict, List, Tuple, Any, Optional
from aspect_calculator import calculate_all_aspects


def get_retrograde_planets(chart_data: Dict[str, Any]) -> List[str]:
    """
    Extract list of retrograde planets from chart data.
    
    Args:
        chart_data: Chart dictionary with planetary_positions key
            Format: {
                "planetary_positions": {
                    "Sun": {"is_retrograde": False, ...},
                    "Mars": {"is_retrograde": True, ...},
                    ...
                }
            }
    
    Returns:
        List of planet names that are retrograde
    
    Example:
        >>> chart = {
        ...     "planetary_positions": {
        ...         "Mars": {"is_retrograde": True},
        ...         "Jupiter": {"is_retrograde": True},
        ...         "Sun": {"is_retrograde": False}
        ...     }
        ... }
        >>> get_retrograde_planets(chart)
        ['Mars', 'Jupiter']
    """
    retrograde_planets = []
    planetary_positions = chart_data.get('planetary_positions', {})
    
    if isinstance(planetary_positions, dict):
        for planet_name, planet_data in planetary_positions.items():
            if isinstance(planet_data, dict) and planet_data.get('is_retrograde', False):
                retrograde_planets.append(planet_name)
    
    return retrograde_planets


def get_planet_house(planet_data: Dict[str, Any]) -> Optional[int]:
    """
    Extract house number for a planet.
    
    Args:
        planet_data: Planet data dictionary
    
    Returns:
        House number (1-12) or None if not available
    """
    house = planet_data.get('house')
    if house is not None and 1 <= house <= 12:
        return int(house)
    return None


def get_planet_rasi(planet_data: Dict[str, Any]) -> Optional[str]:
    """
    Extract rasi (zodiac sign) name for a planet.
    
    Args:
        planet_data: Planet data dictionary
    
    Returns:
        Rasi name (e.g., "Scorpio") or None if not available
    """
    rasi_data = planet_data.get('rasi')
    if isinstance(rasi_data, dict):
        return rasi_data.get('name')
    return None


def calculate_correlation_score(correlations: List[Dict[str, Any]]) -> float:
    """
    Calculate overall correlation score by summing individual correlation scores.
    
    The score is capped at 1.0 (maximum possible correlation).
    
    Args:
        correlations: List of correlation dictionaries, each with a "score" key
    
    Returns:
        Total correlation score between 0.0 and 1.0
    
    Example:
        >>> correlations = [
        ...     {"type": "lagna_match", "score": 0.3},
        ...     {"type": "retrograde_match", "score": 0.1},
        ...     {"type": "house_match", "score": 0.05}
        ... ]
        >>> calculate_correlation_score(correlations)
        0.45
    """
    total_score = sum(corr.get('score', 0.0) for corr in correlations)
    return min(total_score, 1.0)  # Cap at 1.0


def categorize_correlation_strength(score: float) -> str:
    """
    Categorize correlation strength based on score.
    
    Args:
        score: Correlation score between 0.0 and 1.0
    
    Returns:
        Strength category: "Very High", "High", "Medium", or "Low"
    
    Example:
        >>> categorize_correlation_strength(0.75)
        'Very High'
        >>> categorize_correlation_strength(0.45)
        'Medium'
    """
    if score >= 0.7:
        return "Very High"
    elif score >= 0.5:
        return "High"
    elif score >= 0.3:
        return "Medium"
    else:
        return "Low"


def correlate_event_with_snapshot(
    event_chart: Dict[str, Any],
    snapshot_chart: Dict[str, Any],
    snapshot_id: int
) -> Dict[str, Any]:
    """
    Analyze correlation between an event chart and a cosmic snapshot.
    
    This function performs multiple correlation checks to identify matching
    planetary patterns between the event and snapshot:
    - Lagna (Ascendant) matches
    - Retrograde planet matches
    - House position matches
    - Aspect matches
    - Rasi (zodiac sign) matches
    
    Args:
        event_chart: Event chart data from calculate_complete_chart() or event_chart_data
            Format: {
                "ascendant_rasi": "Scorpio",
                "ascendant_rasi_number": 8,
                "planetary_positions": {
                    "Sun": {"house": 3, "rasi": {"name": "Scorpio"}, "is_retrograde": False, ...},
                    "Mars": {"house": 1, "rasi": {"name": "Aries"}, "is_retrograde": False, ...},
                    ...
                },
                "house_cusps": [45.5, 75.2, ...],
                ...
            }
        snapshot_chart: Cosmic snapshot chart data
            Format: Same as event_chart
        snapshot_id: ID of the snapshot being compared
    
    Returns:
        Dictionary containing correlation analysis:
        {
            "snapshot_id": 123,
            "correlations": [
                {
                    "type": "lagna_match",
                    "description": "Both have Lagna in Scorpio",
                    "significance": "Very High",
                    "score": 0.3,
                    "details": {...}
                },
                ...
            ],
            "correlation_score": 0.75,
            "total_matches": 8,
            "strength": "High"
        }
    
    Example:
        >>> event = {
        ...     "ascendant_rasi": "Scorpio",
        ...     "planetary_positions": {
        ...         "Mars": {"house": 1, "rasi": {"name": "Aries"}, "is_retrograde": False}
        ...     }
        ... }
        >>> snapshot = {
        ...     "lagna_rasi": "Scorpio",
        ...     "planetary_positions": {
        ...         "Mars": {"house": 1, "rasi": {"name": "Aries"}, "is_retrograde": False}
        ...     }
        ... }
        >>> result = correlate_event_with_snapshot(event, snapshot, 123)
        >>> result['correlation_score']
        0.35  # Lagna match (0.3) + House match (0.05)
    """
    correlations = []
    
    # Get planetary positions from both charts
    event_positions = event_chart.get('planetary_positions', {})
    snapshot_positions = snapshot_chart.get('planetary_positions', {})
    
    # -------------------------------------------------------------------------
    # a) LAGNA MATCH (Score: 0.3 - Very High)
    # -------------------------------------------------------------------------
    event_lagna_rasi = event_chart.get('ascendant_rasi')
    snapshot_lagna_rasi = snapshot_chart.get('lagna_rasi')
    
    if event_lagna_rasi and snapshot_lagna_rasi:
        if event_lagna_rasi == snapshot_lagna_rasi:
            event_lagna_degree = event_chart.get('ascendant_degree', 0)
            snapshot_lagna_degree = snapshot_chart.get('lagna_degree', 0)
            
            correlations.append({
                "type": "lagna_match",
                "description": f"Both have Lagna in {event_lagna_rasi}",
                "significance": "Very High",
                "score": 0.3,
                "details": {
                    "lagna_rasi": event_lagna_rasi,
                    "event_lagna_degree": event_lagna_degree,
                    "snapshot_lagna_degree": snapshot_lagna_degree,
                    "degree_difference": abs(event_lagna_degree - snapshot_lagna_degree)
                }
            })
    
    # -------------------------------------------------------------------------
    # b) RETROGRADE PLANET MATCHES (Score: 0.1 per planet - High)
    # -------------------------------------------------------------------------
    event_retrograde = get_retrograde_planets(event_chart)
    snapshot_retrograde = get_retrograde_planets(snapshot_chart)
    
    matching_retrograde = set(event_retrograde) & set(snapshot_retrograde)
    
    for planet in matching_retrograde:
        correlations.append({
            "type": "retrograde_match",
            "description": f"{planet} retrograde in both charts",
            "significance": "High",
            "score": 0.1,
            "details": {
                "planet": planet,
                "event_retrograde": True,
                "snapshot_retrograde": True
            }
        })
    
    # -------------------------------------------------------------------------
    # c) HOUSE POSITION MATCHES (Score: 0.05 per planet - Medium)
    # -------------------------------------------------------------------------
    planet_names = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
    
    for planet_name in planet_names:
        event_planet = event_positions.get(planet_name, {})
        snapshot_planet = snapshot_positions.get(planet_name, {})
        
        if not event_planet or not snapshot_planet:
            continue
        
        event_house = get_planet_house(event_planet)
        snapshot_house = get_planet_house(snapshot_planet)
        
        if event_house and snapshot_house and event_house == snapshot_house:
            correlations.append({
                "type": "planetary_house_match",
                "description": f"{planet_name} in {event_house}{'st' if event_house == 1 else 'nd' if event_house == 2 else 'rd' if event_house == 3 else 'th'} house in both charts",
                "significance": "Medium",
                "score": 0.05,
                "details": {
                    "planet": planet_name,
                    "house": event_house,
                    "event_house": event_house,
                    "snapshot_house": snapshot_house
                }
            })
    
    # -------------------------------------------------------------------------
    # d) ASPECT MATCHES (Score: 0.15 per aspect - High)
    # -------------------------------------------------------------------------
    try:
        # Get house cusps for aspect calculation
        event_house_cusps = event_chart.get('house_cusps', [])
        snapshot_house_cusps = snapshot_chart.get('house_cusps', [])
        
        # Calculate aspects for both charts
        event_aspects = calculate_all_aspects(event_positions, event_house_cusps)
        snapshot_aspects = calculate_all_aspects(snapshot_positions, snapshot_house_cusps)
        
        # Find matching aspects (same planet, same target house, same type)
        aspect_matches = []
        for event_aspect in event_aspects:
            for snapshot_aspect in snapshot_aspects:
                if (event_aspect['planet'] == snapshot_aspect['planet'] and
                    event_aspect['to_house'] == snapshot_aspect['to_house'] and
                    event_aspect['aspect_type'] == snapshot_aspect['aspect_type']):
                    
                    # Check if we already added this match
                    match_key = (event_aspect['planet'], event_aspect['to_house'], event_aspect['aspect_type'])
                    if match_key not in aspect_matches:
                        aspect_matches.append(match_key)
                        
                        correlations.append({
                            "type": "aspect_match",
                            "description": f"{event_aspect['planet']} aspects {event_aspect['to_house']}{'st' if event_aspect['to_house'] == 1 else 'nd' if event_aspect['to_house'] == 2 else 'rd' if event_aspect['to_house'] == 3 else 'th'} house ({event_aspect['aspect_type']}) in both charts",
                            "significance": "High",
                            "score": 0.15,
                            "details": {
                                "planet": event_aspect['planet'],
                                "aspect_type": event_aspect['aspect_type'],
                                "target_house": event_aspect['to_house'],
                                "event_aspect": event_aspect,
                                "snapshot_aspect": snapshot_aspect
                            }
                        })
    except Exception as e:
        # If aspect calculation fails, skip aspect matching
        pass
    
    # -------------------------------------------------------------------------
    # e) RASI MATCHES (Score: 0.05 per planet - Medium)
    # -------------------------------------------------------------------------
    for planet_name in planet_names:
        event_planet = event_positions.get(planet_name, {})
        snapshot_planet = snapshot_positions.get(planet_name, {})
        
        if not event_planet or not snapshot_planet:
            continue
        
        event_rasi = get_planet_rasi(event_planet)
        snapshot_rasi = get_planet_rasi(snapshot_planet)
        
        if event_rasi and snapshot_rasi and event_rasi == snapshot_rasi:
            # Skip if we already matched this planet by house (avoid double counting)
            house_match_exists = any(
                corr.get('type') == 'planetary_house_match' and 
                corr.get('details', {}).get('planet') == planet_name
                for corr in correlations
            )
            
            if not house_match_exists:
                correlations.append({
                    "type": "planetary_rasi_match",
                    "description": f"{planet_name} in {event_rasi} in both charts",
                    "significance": "Medium",
                    "score": 0.05,
                    "details": {
                        "planet": planet_name,
                        "rasi": event_rasi,
                        "event_rasi": event_rasi,
                        "snapshot_rasi": snapshot_rasi
                    }
                })
    
    # Calculate total correlation score
    correlation_score = calculate_correlation_score(correlations)
    strength = categorize_correlation_strength(correlation_score)
    
    return {
        "snapshot_id": snapshot_id,
        "correlations": correlations,
        "correlation_score": correlation_score,
        "total_matches": len(correlations),
        "strength": strength
    }


def format_correlation_report(correlation_data: Dict[str, Any]) -> str:
    """
    Create a human-readable text report of correlations.
    
    Args:
        correlation_data: Correlation data dictionary from correlate_event_with_snapshot()
    
    Returns:
        Formatted text report string
    
    Example:
        >>> data = {
        ...     "snapshot_id": 123,
        ...     "correlation_score": 0.75,
        ...     "strength": "High",
        ...     "correlations": [...]
        ... }
        >>> report = format_correlation_report(data)
        >>> print(report)
    """
    snapshot_id = correlation_data.get('snapshot_id', 'Unknown')
    score = correlation_data.get('correlation_score', 0.0)
    strength = correlation_data.get('strength', 'Low')
    total_matches = correlation_data.get('total_matches', 0)
    correlations = correlation_data.get('correlations', [])
    
    # Group correlations by type
    by_type = {}
    for corr in correlations:
        corr_type = corr.get('type', 'unknown')
        if corr_type not in by_type:
            by_type[corr_type] = []
        by_type[corr_type].append(corr)
    
    # Build report
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append(f"CORRELATION REPORT - Snapshot ID: {snapshot_id}")
    report_lines.append("=" * 80)
    report_lines.append("")
    report_lines.append(f"Overall Correlation Score: {score:.2f} ({strength})")
    report_lines.append(f"Total Matching Factors: {total_matches}")
    report_lines.append("")
    
    # Group by significance
    significance_order = ["Very High", "High", "Medium", "Low"]
    for sig in significance_order:
        sig_correlations = [c for c in correlations if c.get('significance') == sig]
        if sig_correlations:
            report_lines.append(f"--- {sig} Significance ({len(sig_correlations)} matches) ---")
            for corr in sig_correlations:
                desc = corr.get('description', 'No description')
                score_val = corr.get('score', 0.0)
                report_lines.append(f"  • {desc} [Score: {score_val:.2f}]")
            report_lines.append("")
    
    # Summary by type
    report_lines.append("--- Summary by Correlation Type ---")
    for corr_type, corr_list in sorted(by_type.items()):
        type_score = sum(c.get('score', 0.0) for c in corr_list)
        report_lines.append(f"  {corr_type}: {len(corr_list)} matches, Total score: {type_score:.2f}")
    
    report_lines.append("")
    report_lines.append("=" * 80)
    
    return "\n".join(report_lines)


# Example usage
if __name__ == "__main__":
    # Example event chart
    example_event_chart = {
        "ascendant_rasi": "Scorpio",
        "ascendant_rasi_number": 8,
        "ascendant_degree": 232.5,
        "planetary_positions": {
            "Sun": {
                "house": 3,
                "rasi": {"name": "Scorpio"},
                "is_retrograde": False,
                "longitude": 232.5
            },
            "Mars": {
                "house": 1,
                "rasi": {"name": "Aries"},
                "is_retrograde": False,
                "longitude": 15.5
            },
            "Saturn": {
                "house": 7,
                "rasi": {"name": "Libra"},
                "is_retrograde": True,
                "longitude": 195.8
            }
        },
        "house_cusps": [232.5, 262.5, 292.5, 322.5, 352.5, 22.5, 52.5, 82.5, 112.5, 142.5, 172.5, 202.5]
    }
    
    # Example snapshot chart
    example_snapshot_chart = {
        "lagna_rasi": "Scorpio",
        "lagna_degree": 235.2,
        "planetary_positions": {
            "Sun": {
                "house": 3,
                "rasi": {"name": "Scorpio"},
                "is_retrograde": False,
                "longitude": 234.1
            },
            "Mars": {
                "house": 1,
                "rasi": {"name": "Aries"},
                "is_retrograde": False,
                "longitude": 16.2
            },
            "Saturn": {
                "house": 7,
                "rasi": {"name": "Libra"},
                "is_retrograde": True,
                "longitude": 196.5
            }
        },
        "house_cusps": [235.2, 265.2, 295.2, 325.2, 355.2, 25.2, 55.2, 85.2, 115.2, 145.2, 175.2, 205.2]
    }
    
    # Perform correlation
    print("Running correlation analysis...")
    result = correlate_event_with_snapshot(example_event_chart, example_snapshot_chart, 123)
    
    # Print report
    print("\n" + format_correlation_report(result))
    
    # Print JSON structure
    print("\n" + "=" * 80)
    print("JSON Structure:")
    print("=" * 80)
    import json
    print(json.dumps(result, indent=2))

