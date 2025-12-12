"""
Aspect Calculator Module for Vedic Astrology

This module calculates all active planetary aspects (Drishti) based on
traditional Vedic astrology rules. Aspects are directional glances that
planets cast on houses from their position.

Vedic Astrology Aspect Rules:
- Jupiter aspects 5th, 7th, and 9th houses from itself
- Saturn aspects 3rd, 7th, and 10th houses from itself
- Mars aspects 4th, 7th, and 8th houses from itself
- Rahu and Ketu aspect 3rd, 7th, and 11th houses from themselves
- Sun, Moon, Mercury, and Venus aspect only the 7th house (opposite)

Author: Cosmic Diary System
Date: 2025-12-12
"""

from typing import Dict, List, Optional, Any, Union


# Aspect rules for each planet in Vedic astrology
ASPECT_RULES: Dict[str, List[int]] = {
    'Jupiter': [5, 7, 9],    # Jupiter aspects 5th, 7th, 9th houses from itself
    'Saturn': [3, 7, 10],    # Saturn aspects 3rd, 7th, 10th houses from itself
    'Mars': [4, 7, 8],       # Mars aspects 4th, 7th, 8th houses from itself
    'Rahu': [3, 7, 11],      # Rahu aspects 3rd, 7th, 11th houses from itself
    'Ketu': [3, 7, 11],      # Ketu aspects 3rd, 7th, 11th houses from itself
    'Sun': [7],              # Sun aspects only 7th house (opposite)
    'Moon': [7],             # Moon aspects only 7th house (opposite)
    'Mercury': [7],          # Mercury aspects only 7th house (opposite)
    'Venus': [7]             # Venus aspects only 7th house (opposite)
}


def calculate_target_house(from_house: int, offset: int) -> int:
    """
    Calculate target house number from a given house with an offset.
    Handles circular house numbering (1-12).
    
    Args:
        from_house: Starting house number (1-12)
        offset: Number of houses to move forward (1-11)
    
    Returns:
        Target house number (1-12)
    
    Examples:
        >>> calculate_target_house(1, 6)  # 7th house from 1st
        7
        >>> calculate_target_house(10, 5)  # 3rd house from 10th (wraps around)
        3
        >>> calculate_target_house(12, 7)  # 7th house from 12th
        7
    """
    if not (1 <= from_house <= 12):
        raise ValueError(f"from_house must be between 1 and 12, got {from_house}")
    if not (1 <= offset <= 11):
        raise ValueError(f"offset must be between 1 and 11, got {offset}")
    
    target = (from_house + offset - 1) % 12
    return target if target != 0 else 12


def get_aspect_type_name(planet_name: str, offset: int) -> str:
    """
    Generate aspect type name based on planet and offset.
    
    Args:
        planet_name: Name of the planet casting the aspect
        offset: Number of houses from planet position
    
    Returns:
        Aspect type string (e.g., "drishti_7th", "drishti_9th")
    
    Examples:
        >>> get_aspect_type_name("Jupiter", 7)
        'drishti_7th'
        >>> get_aspect_type_name("Mars", 4)
        'drishti_4th'
    """
    # Map offset to ordinal suffix
    ordinal_map = {
        3: '3rd', 4: '4th', 5: '5th', 6: '6th', 7: '7th',
        8: '8th', 9: '9th', 10: '10th', 11: '11th'
    }
    
    if offset == 7:
        return 'drishti_7th'  # Common 7th house aspect
    elif offset in ordinal_map:
        return f'drishti_{ordinal_map[offset]}'
    else:
        return f'drishti_{offset}th'


def calculate_all_aspects(
    planets: Dict[str, Dict[str, Any]],
    house_cusps: Optional[List[float]] = None
) -> List[Dict[str, Any]]:
    """
    Calculate all active planetary aspects (Drishti) based on Vedic astrology rules.
    
    This function iterates through all planets and calculates which houses
    each planet aspects based on traditional Vedic astrology rules.
    
    Args:
        planets: Dictionary of planetary positions from calculate_complete_chart()
            Format: {
                "Sun": {
                    "longitude": 232.5,
                    "house": 3,
                    "rasi": {"name": "Scorpio", "number": 8, "lord": "Mars"},
                    "is_retrograde": False,
                    ...
                },
                "Moon": {...},
                ...
            }
            Each planet must have a "house" key (1-12) indicating its position.
        house_cusps: Optional list of 12 house cusp degrees. Currently not used
            but kept for future enhancements (e.g., conjunction detection).
    
    Returns:
        List of all active aspects, each as a dictionary:
        [
            {
                "planet": "Mars",
                "from_house": 1,
                "to_house": 8,
                "aspect_type": "drishti_8th",
                "planet_rasi": "Aries",
                "planet_longitude": 15.5,
                "planet_strength": 0.75,  # Optional, if available
                "is_retrograde": False
            },
            {
                "planet": "Jupiter",
                "from_house": 5,
                "to_house": 9,
                "aspect_type": "drishti_9th",
                "planet_rasi": "Cancer",
                "planet_longitude": 95.2,
                "planet_strength": None,
                "is_retrograde": False
            },
            ...
        ]
    
    Raises:
        ValueError: If planet house number is not 1-12
        KeyError: If planet name is not in ASPECT_RULES
    
    Example:
        >>> planets = {
        ...     "Mars": {"house": 1, "rasi": {"name": "Aries"}, "longitude": 15.5, "is_retrograde": False},
        ...     "Jupiter": {"house": 5, "rasi": {"name": "Cancer"}, "longitude": 95.2, "is_retrograde": False},
        ...     "Saturn": {"house": 7, "rasi": {"name": "Libra"}, "longitude": 195.8, "is_retrograde": True}
        ... }
        >>> aspects = calculate_all_aspects(planets)
        >>> len(aspects)
        7  # Mars: 3 aspects, Jupiter: 3 aspects, Saturn: 3 aspects (but 7th overlaps)
        >>> aspects[0]['planet']
        'Mars'
        >>> aspects[0]['to_house']
        8  # Mars in 1st house aspects 8th house
    """
    all_aspects: List[Dict[str, Any]] = []
    
    for planet_name, planet_data in planets.items():
        # Validate planet name
        if planet_name not in ASPECT_RULES:
            continue  # Skip unknown planets
        
        # Get planet's current house
        planet_house = planet_data.get('house')
        if planet_house is None:
            continue  # Skip planets without house information
        
        # Validate house number
        if not (1 <= planet_house <= 12):
            raise ValueError(
                f"Planet {planet_name} has invalid house number: {planet_house}. "
                f"House must be between 1 and 12."
            )
        
        # Get aspect rules for this planet
        aspect_offsets = ASPECT_RULES[planet_name]
        
        # Get planet's rasi name (handle nested structure)
        planet_rasi_data = planet_data.get('rasi', {})
        if isinstance(planet_rasi_data, dict):
            planet_rasi = planet_rasi_data.get('name', 'Unknown')
        else:
            planet_rasi = str(planet_rasi_data)
        
        # Get planet's longitude
        planet_longitude = planet_data.get('longitude', 0.0)
        
        # Get planet's retrograde status
        is_retrograde = planet_data.get('is_retrograde', False)
        
        # Get planet's strength if available
        planet_strength = planet_data.get('strength', planet_data.get('strength_score', None))
        
        # Calculate aspects for each offset
        for offset in aspect_offsets:
            target_house = calculate_target_house(planet_house, offset)
            aspect_type = get_aspect_type_name(planet_name, offset)
            
            # Create aspect entry
            aspect = {
                "planet": planet_name,
                "from_house": planet_house,
                "to_house": target_house,
                "aspect_type": aspect_type,
                "planet_rasi": planet_rasi,
                "planet_longitude": float(planet_longitude),
                "is_retrograde": bool(is_retrograde)
            }
            
            # Add strength if available
            if planet_strength is not None:
                aspect["planet_strength"] = float(planet_strength)
            
            all_aspects.append(aspect)
    
    return all_aspects


def get_aspects_to_house(house_number: int, aspects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filter aspects to find all aspects pointing to a specific house.
    
    This is useful for analyzing which planets are influencing a specific
    house through their aspects (Drishti).
    
    Args:
        house_number: Target house number (1-12) to filter aspects
        aspects: List of aspect dictionaries from calculate_all_aspects()
    
    Returns:
        List of all aspects pointing to the specified house:
        [
            {
                "planet": "Mars",
                "from_house": 1,
                "to_house": 8,
                "aspect_type": "drishti_8th",
                ...
            },
            {
                "planet": "Saturn",
                "from_house": 2,
                "to_house": 8,
                "aspect_type": "drishti_7th",
                ...
            },
            ...
        ]
    
    Raises:
        ValueError: If house_number is not 1-12
    
    Example:
        >>> aspects = [
        ...     {"planet": "Mars", "from_house": 1, "to_house": 8, "aspect_type": "drishti_8th"},
        ...     {"planet": "Jupiter", "from_house": 5, "to_house": 9, "aspect_type": "drishti_9th"},
        ...     {"planet": "Saturn", "from_house": 2, "to_house": 8, "aspect_type": "drishti_7th"}
        ... ]
        >>> house_8_aspects = get_aspects_to_house(8, aspects)
        >>> len(house_8_aspects)
        2
        >>> house_8_aspects[0]['planet']
        'Mars'
    """
    if not (1 <= house_number <= 12):
        raise ValueError(f"house_number must be between 1 and 12, got {house_number}")
    
    return [aspect for aspect in aspects if aspect.get('to_house') == house_number]


def get_planet_aspects(planet_name: str, aspects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filter aspects to find all aspects cast by a specific planet.
    
    This is useful for analyzing what a specific planet is influencing
    through its aspects (Drishti).
    
    Args:
        planet_name: Name of the planet (e.g., "Mars", "Jupiter")
        aspects: List of aspect dictionaries from calculate_all_aspects()
    
    Returns:
        List of all aspects cast by the specified planet:
        [
            {
                "planet": "Mars",
                "from_house": 1,
                "to_house": 5,
                "aspect_type": "drishti_4th",
                ...
            },
            {
                "planet": "Mars",
                "from_house": 1,
                "to_house": 8,
                "aspect_type": "drishti_7th",
                ...
            },
            {
                "planet": "Mars",
                "from_house": 1,
                "to_house": 9,
                "aspect_type": "drishti_8th",
                ...
            }
        ]
    
    Example:
        >>> aspects = [
        ...     {"planet": "Mars", "from_house": 1, "to_house": 5, "aspect_type": "drishti_4th"},
        ...     {"planet": "Jupiter", "from_house": 5, "to_house": 9, "aspect_type": "drishti_9th"},
        ...     {"planet": "Mars", "from_house": 1, "to_house": 8, "aspect_type": "drishti_7th"}
        ... ]
        >>> mars_aspects = get_planet_aspects("Mars", aspects)
        >>> len(mars_aspects)
        2
        >>> mars_aspects[0]['planet']
        'Mars'
    """
    return [aspect for aspect in aspects if aspect.get('planet') == planet_name]


def get_aspect_strength(aspect: Dict[str, Any]) -> str:
    """
    Determine aspect strength based on aspect type and planet state.
    
    In Vedic astrology, certain aspects are considered stronger:
    - 7th house aspects (opposition) are generally strongest
    - Aspects from retrograde planets may have different effects
    - Special aspects (like Mars 8th, Jupiter 9th) have specific significances
    
    Args:
        aspect: Aspect dictionary from calculate_all_aspects()
    
    Returns:
        Strength indicator: "strong", "moderate", or "weak"
    
    Example:
        >>> aspect = {"aspect_type": "drishti_7th", "is_retrograde": False}
        >>> get_aspect_strength(aspect)
        'strong'
    """
    aspect_type = aspect.get('aspect_type', '')
    is_retrograde = aspect.get('is_retrograde', False)
    
    # 7th house aspects (opposition) are generally strongest
    if aspect_type == 'drishti_7th':
        return 'strong'
    
    # Special aspects from malefic planets on dustana houses
    planet = aspect.get('planet', '')
    to_house = aspect.get('to_house', 0)
    
    if planet in ['Mars', 'Saturn'] and to_house in [6, 8, 12]:
        return 'strong'
    
    # Aspects from retrograde planets may be considered stronger in some contexts
    if is_retrograde and aspect_type in ['drishti_8th', 'drishti_10th']:
        return 'moderate'
    
    # Default strength
    return 'moderate'


# Example usage and testing
if __name__ == "__main__":
    # Example planets data structure
    example_planets = {
        "Sun": {
            "longitude": 232.5,
            "house": 3,
            "rasi": {"name": "Scorpio", "number": 8, "lord": "Mars"},
            "is_retrograde": False,
            "strength_score": 0.65
        },
        "Moon": {
            "longitude": 147.32,
            "house": 11,
            "rasi": {"name": "Leo", "number": 5, "lord": "Sun"},
            "is_retrograde": False,
            "strength_score": 0.72
        },
        "Mars": {
            "longitude": 15.5,
            "house": 1,
            "rasi": {"name": "Aries", "number": 1, "lord": "Mars"},
            "is_retrograde": False,
            "strength_score": 0.85
        },
        "Jupiter": {
            "longitude": 95.2,
            "house": 5,
            "rasi": {"name": "Cancer", "number": 4, "lord": "Moon"},
            "is_retrograde": True,
            "strength_score": 0.78
        },
        "Saturn": {
            "longitude": 195.8,
            "house": 7,
            "rasi": {"name": "Libra", "number": 7, "lord": "Venus"},
            "is_retrograde": True,
            "strength_score": 0.68
        }
    }
    
    # Calculate all aspects
    print("Calculating all planetary aspects...")
    all_aspects = calculate_all_aspects(example_planets)
    
    print(f"\nTotal aspects found: {len(all_aspects)}")
    print("\nAll Aspects:")
    print("=" * 80)
    for aspect in all_aspects:
        strength = get_aspect_strength(aspect)
        print(f"{aspect['planet']:10} in House {aspect['from_house']:2} -> "
              f"Aspects House {aspect['to_house']:2} ({aspect['aspect_type']:12}) "
              f"[{strength}]")
    
    # Find aspects to a specific house
    print("\n" + "=" * 80)
    print("Aspects to House 8:")
    print("=" * 80)
    house_8_aspects = get_aspects_to_house(8, all_aspects)
    for aspect in house_8_aspects:
        print(f"{aspect['planet']} in House {aspect['from_house']} aspects House 8 "
              f"({aspect['aspect_type']})")
    
    # Find aspects from a specific planet
    print("\n" + "=" * 80)
    print("Aspects from Mars:")
    print("=" * 80)
    mars_aspects = get_planet_aspects("Mars", all_aspects)
    for aspect in mars_aspects:
        print(f"Mars in House {aspect['from_house']} aspects House {aspect['to_house']} "
              f"({aspect['aspect_type']})")

