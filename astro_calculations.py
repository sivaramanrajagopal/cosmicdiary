"""
Astrological Calculations Module
Provides functions for calculating ascendant (Lagna), house cusps, 
planetary positions with house placements, and planetary strengths
using Swiss Ephemeris.
"""

import swisseph as swe
from datetime import datetime, date, time
from typing import Dict, List, Optional, Tuple
import pytz
from timezonefinder import TimezoneFinder

# Swiss Ephemeris settings
AYANAMSA = swe.SIDM_LAHIRI  # Lahiri ayanamsa
HOUSE_SYSTEM = b'P'  # Placidus house system

# Planet constants (Swiss Ephemeris planet numbers)
PLANETS = {
    'Sun': swe.SUN,
    'Moon': swe.MOON,
    'Mercury': swe.MERCURY,
    'Venus': swe.VENUS,
    'Mars': swe.MARS,
    'Jupiter': swe.JUPITER,
    'Saturn': swe.SATURN,
    'Rahu': swe.TRUE_NODE,  # North Node
    'Ketu': swe.TRUE_NODE + 1  # South Node (calculated from Rahu)
}

# Rasi (Zodiac signs) mapping
RASI_NAMES = [
    'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
]

RASI_LORDS = {
    'Aries': 'Mars',
    'Taurus': 'Venus',
    'Gemini': 'Mercury',
    'Cancer': 'Moon',
    'Leo': 'Sun',
    'Virgo': 'Mercury',
    'Libra': 'Venus',
    'Scorpio': 'Mars',
    'Sagittarius': 'Jupiter',
    'Capricorn': 'Saturn',
    'Aquarius': 'Saturn',
    'Pisces': 'Jupiter'
}

# Nakshatra boundaries (27 nakshatras, each ~13.33 degrees)
NAKSHATRA_SIZE = 360.0 / 27

# Exaltation degrees (planet: degree in zodiac)
EXALTATION = {
    'Sun': 10.0,      # Aries 10°
    'Moon': 3.0,      # Taurus 3°
    'Mercury': 15.0,  # Virgo 15°
    'Venus': 27.0,    # Pisces 27°
    'Mars': 28.0,     # Capricorn 28°
    'Jupiter': 5.0,   # Cancer 5°
    'Saturn': 20.0,   # Libra 20°
}

# Debilitation degrees (opposite of exaltation)
DEBILITATION = {
    'Sun': 190.0,     # Libra 10° (180° + 10°)
    'Moon': 213.0,    # Scorpio 3° (180° + 33°)
    'Mercury': 195.0, # Pisces 15° (180° + 15°)
    'Venus': 207.0,   # Virgo 27° (180° + 27°)
    'Mars': 208.0,    # Cancer 28° (180° + 28°)
    'Jupiter': 185.0, # Capricorn 5° (180° + 5°)
    'Saturn': 200.0,  # Aries 20° (180° + 20°)
}

# Own signs (rulership)
OWN_SIGNS = {
    'Sun': ['Leo'],
    'Moon': ['Cancer'],
    'Mercury': ['Gemini', 'Virgo'],
    'Venus': ['Taurus', 'Libra'],
    'Mars': ['Aries', 'Scorpio'],
    'Jupiter': ['Sagittarius', 'Pisces'],
    'Saturn': ['Capricorn', 'Aquarius'],
    'Rahu': [],  # Nodes don't have own signs
    'Ketu': []
}


def degrees_to_rasi(longitude: float) -> Dict:
    """Convert longitude to rasi (zodiac sign)"""
    lon = longitude % 360
    rasi_number = int(lon / 30) + 1
    rasi_name = RASI_NAMES[rasi_number - 1]
    
    return {
        'name': rasi_name,
        'number': rasi_number,
        'lord': {'name': RASI_LORDS[rasi_name]}
    }


def degrees_to_nakshatra(longitude: float) -> Dict:
    """Convert longitude to nakshatra"""
    lon = longitude % 360
    nakshatra_num = int(lon / NAKSHATRA_SIZE) + 1
    nakshatra_num = min(nakshatra_num, 27)  # Ensure 1-27 range
    pada = int((lon % NAKSHATRA_SIZE) / (NAKSHATRA_SIZE / 4)) + 1
    
    # Nakshatra names (simplified - you may want full names)
    nakshatra_names = [
        'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
        'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
        'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshta',
        'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha',
        'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
    ]
    
    return {
        'name': nakshatra_names[nakshatra_num - 1],
        'number': nakshatra_num,
        'pada': min(pada, 4)
    }


def calculate_ascendant(jd: float, lat: float, lng: float) -> Dict:
    """
    Calculate ascendant (Lagna) using swe.houses()
    
    Args:
        jd: Julian Day number
        lat: Latitude in degrees (positive = North, negative = South)
        lng: Longitude in degrees (positive = East, negative = West)
    
    Returns:
        Dictionary with ascendant information
    """
    try:
        # Set sidereal mode first
        swe.set_sid_mode(AYANAMSA)
        
        # Get ayanamsa value
        ayanamsa = swe.get_ayanamsa_ut(jd)
        
        # Calculate houses using Placidus system
        # swe.houses() returns: (cusps, ascmc) or raises exception
        # ascmc[0] = Ascendant, ascmc[1] = MC (Medium Coeli)
        # cusps[0] = Ascendant, cusps[1-12] = House cusps 1-12
        try:
            result = swe.houses(jd, lat, lng, HOUSE_SYSTEM)
            cusps, ascmc = result
        except Exception as e:
            raise ValueError(f"Error calculating houses: {str(e)}")
        
        # Ascendant is in ascmc[0] (tropical)
        ascendant_degree_tropical = ascmc[0]
        
        # Convert to sidereal (subtract ayanamsa)
        sidereal_asc = swe.degnorm(ascendant_degree_tropical - ayanamsa)
        
        # Convert to rasi
        asc_rasi = degrees_to_rasi(sidereal_asc)
        
        # Get nakshatra
        asc_nakshatra = degrees_to_nakshatra(sidereal_asc)
        
        return {
            'ascendant_degree': round(sidereal_asc, 6),
            'ascendant_rasi': asc_rasi['name'],
            'ascendant_rasi_number': asc_rasi['number'],
            'ascendant_nakshatra': asc_nakshatra['name'],
            'ascendant_lord': asc_rasi['lord']['name'],
            'ayanamsa': round(ayanamsa, 6)
        }
    
    except Exception as e:
        raise ValueError(f"Error calculating ascendant: {str(e)}")


def get_house_number(planet_longitude: float, house_cusps: List[float]) -> int:
    """
    Determine which house a planet is in based on house cusps
    
    Args:
        planet_longitude: Planet's longitude (0-360 degrees)
        house_cusps: List of 12 house cusp degrees [house1, house2, ..., house12]
    
    Returns:
        House number (1-12)
    """
    if len(house_cusps) != 12:
        raise ValueError("house_cusps must contain exactly 12 values")
    
    # Normalize planet longitude
    planet_long = planet_longitude % 360
    
    # Check each house
    for i in range(12):
        current_cusp = house_cusps[i] % 360
        next_cusp = house_cusps[(i + 1) % 12] % 360
        
        # Handle wrap-around (house 12 to house 1)
        if next_cusp < current_cusp:
            if planet_long >= current_cusp or planet_long < next_cusp:
                return i + 1
        else:
            if current_cusp <= planet_long < next_cusp:
                return i + 1
    
    # If we get here, assign to house 1 (shouldn't happen normally)
    return 1


def calculate_planetary_positions(jd: float, house_cusps: List[float]) -> List[Dict]:
    """
    Calculate positions for all 9 planets with house placements
    
    Args:
        jd: Julian Day number
        house_cusps: List of 12 house cusp degrees
    
    Returns:
        List of planetary position dictionaries
    """
    planets_data = []
    
    # Set sidereal mode
    swe.set_sid_mode(AYANAMSA)
    
    for planet_name in PLANETS.keys():
        try:
            planet_num = PLANETS[planet_name]
            
            # Special handling for Ketu
            if planet_name == 'Ketu':
                rahu_result = swe.calc_ut(jd, PLANETS['Rahu'], swe.FLG_SIDEREAL | swe.FLG_SWIEPH)
                if not rahu_result:
                    continue
                
                rahu_long = rahu_result[0][0]
                ketu_long = (rahu_long + 180) % 360
                
                planet_data = {
                    'name': 'Ketu',
                    'longitude': round(ketu_long, 6),
                    'latitude': 0.0,
                    'speed': 0.0,
                    'is_retrograde': True,  # Ketu is ALWAYS retrograde in Vedic astrology
                    'rasi': degrees_to_rasi(ketu_long),
                    'nakshatra': degrees_to_nakshatra(ketu_long),
                    'house': get_house_number(ketu_long, house_cusps)
                }
            else:
                # Calculate planet position (sidereal)
                result = swe.calc_ut(jd, planet_num, swe.FLG_SIDEREAL | swe.FLG_SWIEPH)
                
                if not result:
                    continue
                
                longitude = result[0][0]
                latitude = result[0][1]
                speed = result[0][3]  # Speed in longitude
                
                # Determine retrograde status based on Vedic astrology rules:
                # - Rahu and Ketu are ALWAYS retrograde (shadow planets)
                # - Sun and Moon are NEVER retrograde
                # - Other planets are retrograde when speed < 0
                if planet_name == 'Rahu':
                    is_retro = True  # Rahu is ALWAYS retrograde
                elif planet_name in ['Sun', 'Moon']:
                    is_retro = False  # Sun and Moon are NEVER retrograde
                else:
                    is_retro = speed < 0  # Other planets based on speed
                
                planet_data = {
                    'name': planet_name,
                    'longitude': round(longitude, 6),
                    'latitude': round(latitude, 6),
                    'speed': round(speed, 6),
                    'is_retrograde': is_retro,
                    'rasi': degrees_to_rasi(longitude),
                    'nakshatra': degrees_to_nakshatra(longitude),
                    'house': get_house_number(longitude, house_cusps)
                }
            
            planets_data.append(planet_data)
        
        except Exception as e:
            print(f"Warning: Error calculating {planet_name}: {e}")
            continue
    
    return planets_data


def calculate_planetary_strengths(planets: List[Dict], asc_rasi: str) -> Dict:
    """
    Calculate planetary strengths: exaltation, debilitation, own sign, dig bala
    
    Args:
        planets: List of planetary position dictionaries
        asc_rasi: Ascendant rasi name
    
    Returns:
        Dictionary with strength calculations for each planet
    """
    strengths = {}
    
    for planet in planets:
        planet_name = planet['name']
        longitude = planet['longitude']
        rasi_name = planet['rasi']['name']
        
        # Exaltation check (within 5 degrees of exaltation point)
        is_exalted = False
        if planet_name in EXALTATION:
            exalt_degree = EXALTATION[planet_name]
            diff = abs((longitude % 360) - (exalt_degree % 360))
            if diff > 180:
                diff = 360 - diff
            is_exalted = diff <= 5.0  # Within 5 degrees
        
        # Debilitation check
        is_debilitated = False
        if planet_name in DEBILITATION:
            debil_degree = DEBILITATION[planet_name]
            diff = abs((longitude % 360) - (debil_degree % 360))
            if diff > 180:
                diff = 360 - diff
            is_debilitated = diff <= 5.0
        
        # Own sign check
        is_own_sign = rasi_name in OWN_SIGNS.get(planet_name, [])
        
        # Dig Bala (Directional Strength) - based on house position
        # Planets are strong in specific houses:
        # Sun: 10th house, Moon: 4th house, Mars: 10th, Mercury: 1st, 
        # Jupiter: 1st, Venus: 4th, Saturn: 7th
        dig_bala = False
        house = planet.get('house', 0)
        
        dig_bala_rules = {
            'Sun': [10],
            'Moon': [4],
            'Mars': [10],
            'Mercury': [1],
            'Jupiter': [1],
            'Venus': [4],
            'Saturn': [7],
            'Rahu': [],
            'Ketu': []
        }
        
        if planet_name in dig_bala_rules:
            dig_bala = house in dig_bala_rules[planet_name]
        
        # Combustion check (planet too close to Sun)
        is_combusted = False
        if planet_name not in ['Sun', 'Rahu', 'Ketu']:
            sun_planet = next((p for p in planets if p['name'] == 'Sun'), None)
            if sun_planet:
                sun_long = sun_planet['longitude']
                diff = abs((longitude % 360) - (sun_long % 360))
                if diff > 180:
                    diff = 360 - diff
                # Combustion orb: Mercury/Venus = 7°, others = 8.5°
                orb = 7.0 if planet_name in ['Mercury', 'Venus'] else 8.5
                is_combusted = diff < orb
        
        # Calculate strength score (0.0 to 1.0)
        strength_score = 0.5  # Base score
        
        if is_exalted:
            strength_score += 0.3
        elif is_debilitated:
            strength_score -= 0.3
        
        if is_own_sign:
            strength_score += 0.2
        
        if dig_bala:
            strength_score += 0.15
        
        if is_combusted:
            strength_score -= 0.2
        
        # Normalize to 0.0-1.0 range
        strength_score = max(0.0, min(1.0, strength_score))
        
        strengths[planet_name] = {
            'exalted': is_exalted,
            'debilitated': is_debilitated,
            'own_sign': is_own_sign,
            'dig_bala': dig_bala,
            'combusted': is_combusted,
            'strength_score': round(strength_score, 4)
        }
    
    return strengths


def calculate_complete_chart(
    event_date: date,
    event_time: time,
    latitude: float,
    longitude: float,
    timezone_str: str = 'UTC'
) -> Dict:
    """
    Main function to calculate complete astrological chart
    
    Args:
        event_date: Event date
        event_time: Event time
        latitude: Latitude in degrees
        longitude: Longitude in degrees
        timezone_str: Timezone string (e.g., 'Asia/Kolkata')
    
    Returns:
        Complete chart data dictionary
    """
    try:
        # Convert to datetime
        dt = datetime.combine(event_date, event_time)
        
        # Set timezone
        try:
            tz = pytz.timezone(timezone_str)
            dt = tz.localize(dt)
        except Exception as e:
            raise ValueError(f"Invalid timezone: {timezone_str}. Error: {e}")
        
        # Convert to UTC
        dt_utc = dt.astimezone(pytz.UTC)
        
        # Calculate Julian Day
        year = dt_utc.year
        month = dt_utc.month
        day = dt_utc.day
        hour = dt_utc.hour
        minute = dt_utc.minute
        second = dt_utc.second
        
        # Calculate Julian Day with time
        jd = swe.julday(year, month, day, (hour + minute/60.0 + second/3600.0) / 24.0, swe.GREG_CAL)
        
        # Calculate ascendant and get ayanamsa
        asc_data = calculate_ascendant(jd, latitude, longitude)
        ayanamsa = asc_data['ayanamsa']
        
        # Get sidereal time
        sidereal_time = swe.sidtime(jd)  # Returns sidereal time in hours
        
        # Calculate house cusps (sidereal)
        swe.set_sid_mode(AYANAMSA)
        try:
            result = swe.houses(jd, latitude, longitude, HOUSE_SYSTEM)
            cusps, ascmc = result
        except Exception as e:
            raise ValueError(f"Error calculating house cusps: {str(e)}")
        
        # Extract house cusps (1-12) and convert to sidereal
        # swe.houses() returns cusps as a tuple with 12 elements (indices 0-11)
        # cusps[0] = House 1, cusps[1] = House 2, ..., cusps[11] = House 12
        house_cusps_sidereal = []
        for i in range(12):
            cusp_degree_tropical = float(cusps[i]) % 360
            sidereal_cusp = swe.degnorm(cusp_degree_tropical - ayanamsa)
            house_cusps_sidereal.append(round(sidereal_cusp, 6))
        
        # Calculate planetary positions with houses
        planets = calculate_planetary_positions(jd, house_cusps_sidereal)
        
        # Calculate planetary strengths
        strengths = calculate_planetary_strengths(planets, asc_data['ascendant_rasi'])
        
        # Format planetary positions for JSONB storage
        planetary_positions = {}
        for planet in planets:
            planetary_positions[planet['name']] = {
                'longitude': planet['longitude'],
                'latitude': planet['latitude'],
                'speed': planet['speed'],
                'is_retrograde': planet['is_retrograde'],
                'rasi': planet['rasi'],
                'nakshatra': planet['nakshatra'],
                'house': planet['house']
            }
        
        return {
            'ascendant_degree': asc_data['ascendant_degree'],
            'ascendant_rasi': asc_data['ascendant_rasi'],
            'ascendant_rasi_number': asc_data['ascendant_rasi_number'],
            'ascendant_nakshatra': asc_data['ascendant_nakshatra'],
            'ascendant_lord': asc_data['ascendant_lord'],
            'house_cusps': house_cusps_sidereal,
            'house_system': 'Placidus',
            'julian_day': round(jd, 8),
            'sidereal_time': round(sidereal_time * 15.0, 6),  # Convert hours to degrees
            'ayanamsa': ayanamsa,
            'planetary_positions': planetary_positions,
            'planetary_strengths': strengths
        }
    
    except Exception as e:
        raise ValueError(f"Error calculating complete chart: {str(e)}")

