"""
Flask API Server for Cosmic Diary
Handles planetary position calculations using Swiss Ephemeris
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, date, time
import swisseph as swe
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv
from astro_calculations import calculate_complete_chart
from timezonefinder import TimezoneFinder

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for Next.js frontend

# Swiss Ephemeris settings
# Lahiri ayanamsa = 1
AYANAMSA = swe.SIDM_LAHIRI

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


def degrees_to_nakshatra(longitude: float) -> int:
    """Convert longitude to nakshatra number (1-27)"""
    # Normalize to 0-360
    lon = longitude % 360
    nakshatra = int(lon / NAKSHATRA_SIZE) + 1
    return min(nakshatra, 27)  # Ensure 1-27 range


def degrees_to_rasi(longitude: float) -> Dict:
    """Convert longitude to rasi (zodiac sign)"""
    # Normalize to 0-360
    lon = longitude % 360
    rasi_number = int(lon / 30) + 1
    rasi_name = RASI_NAMES[rasi_number - 1]
    
    return {
        'name': rasi_name,
        'number': rasi_number,
        'lord': {'name': RASI_LORDS[rasi_name]}
    }


def is_retrograde(planet_num: int, planet_name: str, jd: float) -> bool:
    """
    Check if planet is retrograde
    
    Vedic Astrology Rules:
    - Rahu and Ketu are ALWAYS retrograde (shadow planets always move backward)
    - Sun and Moon are NEVER retrograde (always move forward)
    - Other planets (Mercury, Venus, Mars, Jupiter, Saturn) are retrograde when speed < 0
    
    Note: The speed field from calc_ut() may be unreliable in sidereal mode,
    so we calculate speed by comparing positions over a time interval.
    """
    # Rahu and Ketu are always retrograde
    if planet_name in ['Rahu', 'Ketu']:
        return True
    
    # Sun and Moon are never retrograde
    if planet_num in [swe.SUN, swe.MOON]:
        return False
    
    # For other planets, calculate speed by comparing positions over time
    # Use same flags as position calculation (sidereal)
    flags = swe.FLG_SIDEREAL | swe.FLG_SWIEPH
    
    # Calculate position at current time
    result1 = swe.calc_ut(jd, planet_num, flags)
    if not result1:
        return False
    
    # Calculate position 6 hours later (0.25 days) to get accurate speed
    jd_future = jd + 0.25
    result2 = swe.calc_ut(jd_future, planet_num, flags)
    if not result2:
        return False
    
    # Get longitudes
    long1 = result1[0][0]
    long2 = result2[0][0]
    
    # Calculate speed (handle 360° wrap-around)
    diff = long2 - long1
    if diff > 180:
        diff -= 360
    elif diff < -180:
        diff += 360
    
    # Speed per day = diff / 0.25 days
    speed_per_day = diff / 0.25
    
    # Retrograde if speed is negative
    return speed_per_day < 0


def calculate_planet_position(planet_name: str, jd: float) -> Optional[Dict]:
    """Calculate position for a single planet"""
    if planet_name not in PLANETS:
        return None
    
    planet_num = PLANETS[planet_name]
    
    # Special handling for Ketu (South Node)
    if planet_name == 'Ketu':
        # Ketu is 180 degrees opposite to Rahu
        # CRITICAL: Use SIDEREAL mode (same as Rahu) to ensure exactly 180° separation
        rahu_result = swe.calc_ut(jd, PLANETS['Rahu'], swe.FLG_SIDEREAL | swe.FLG_SWIEPH)
        if not rahu_result:
            return None
        
        rahu_long = rahu_result[0][0]
        ketu_long = (rahu_long + 180) % 360
        
        return {
            'name': 'Ketu',
            'longitude': round(ketu_long, 2),
            'latitude': 0.0,
            'is_retrograde': True,  # Ketu is ALWAYS retrograde in Vedic astrology
            'nakshatra': degrees_to_nakshatra(ketu_long),
            'rasi': degrees_to_rasi(ketu_long)
        }
    
    # Calculate planet position
    # Use sidereal mode with Lahiri ayanamsa
    result = swe.calc_ut(jd, planet_num, swe.FLG_SIDEREAL | swe.FLG_SWIEPH)
    
    if not result:
        return None
    
    # Get sidereal longitude
    longitude = result[0][0]
    latitude = result[0][1]
    is_retro = is_retrograde(planet_num, planet_name, jd)
    
    return {
        'name': planet_name,
        'longitude': round(longitude, 2),
        'latitude': round(latitude, 2),
        'is_retrograde': is_retro,
        'nakshatra': degrees_to_nakshatra(longitude),
        'rasi': degrees_to_rasi(longitude)
    }


def calculate_daily_planetary_data(target_date: date) -> Dict:
    """Calculate all planetary positions for a given date"""
    # Convert date to Julian Day Number (at noon UTC)
    year = target_date.year
    month = target_date.month
    day = target_date.day
    
    # Calculate Julian Day for noon UTC
    jd = swe.julday(year, month, day, swe.GREG_CAL)
    
    planets_data = []
    
    # Calculate positions for all planets
    for planet_name in PLANETS.keys():
        planet_data = calculate_planet_position(planet_name, jd)
        if planet_data:
            planets_data.append(planet_data)
    
    return {
        'date': target_date.isoformat(),
        'planetary_data': {
            'planets': planets_data
        }
    }


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'cosmic-diary-api',
        'swiss_ephemeris_version': swe.version
    })


@app.route('/api/planets/daily', methods=['GET'])
def get_daily_planets():
    """Get planetary positions for a specific date"""
    try:
        date_str = request.args.get('date')
        
        if not date_str:
            # Default to today
            target_date = date.today()
        else:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        planetary_data = calculate_daily_planetary_data(target_date)
        
        return jsonify(planetary_data)
    
    except ValueError as e:
        return jsonify({'error': f'Invalid date format: {e}'}), 400
    except Exception as e:
        return jsonify({'error': f'Error calculating planetary data: {str(e)}'}), 500


@app.route('/api/planets/calculate', methods=['POST'])
def calculate_planets():
    """Calculate planetary positions for a date range"""
    try:
        data = request.json
        date_str = data.get('date')
        date_range = data.get('date_range')  # Optional: ['2025-01-01', '2025-12-31']
        
        if date_str:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            result = calculate_daily_planetary_data(target_date)
            return jsonify(result)
        
        elif date_range and len(date_range) == 2:
            start_date = datetime.strptime(date_range[0], '%Y-%m-%d').date()
            end_date = datetime.strptime(date_range[1], '%Y-%m-%d').date()
            
            results = []
            current_date = start_date
            while current_date <= end_date:
                result = calculate_daily_planetary_data(current_date)
                results.append(result)
                # Increment by one day
                from datetime import timedelta
                current_date += timedelta(days=1)
            
            return jsonify({'results': results})
        
        else:
            return jsonify({'error': 'Either date or date_range required'}), 400
    
    except ValueError as e:
        return jsonify({'error': f'Invalid date format: {e}'}), 400
    except Exception as e:
        return jsonify({'error': f'Error calculating planetary data: {str(e)}'}), 500


@app.route('/api/timezone/detect', methods=['GET'])
def detect_timezone():
    """
    Auto-detect timezone from latitude and longitude
    
    Query parameters:
    - lat: Latitude in degrees (required)
    - lng: Longitude in degrees (required)
    
    Returns timezone string (IANA format)
    """
    try:
        lat_str = request.args.get('lat')
        lng_str = request.args.get('lng')
        
        if not lat_str or not lng_str:
            return jsonify({
                'error': 'Missing required parameters',
                'required': ['lat', 'lng']
            }), 400
        
        try:
            latitude = float(lat_str)
            longitude = float(lng_str)
            
            if not (-90 <= latitude <= 90):
                return jsonify({'error': f'Latitude must be between -90 and 90. Got: {latitude}'}), 400
            
            if not (-180 <= longitude <= 180):
                return jsonify({'error': f'Longitude must be between -180 and 180. Got: {longitude}'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Latitude and longitude must be valid numbers'}), 400
        
        # Detect timezone
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lat=latitude, lng=longitude)
        
        if not timezone_str:
            # Fallback to UTC if detection fails
            timezone_str = 'UTC'
        
        return jsonify({
            'success': True,
            'latitude': latitude,
            'longitude': longitude,
            'timezone': timezone_str
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Error detecting timezone: {str(e)}'
        }), 500


@app.route('/api/chart/validate', methods=['GET'])
def validate_chart():
    """
    Health check and validation for chart calculation features
    
    Returns:
    - Swiss Ephemeris version
    - Available planets
    - Supported house systems
    - Ayanamsa setting
    """
    try:
        # Get Swiss Ephemeris version
        swiss_eph_version = swe.version
        
        # Available planets
        available_planets = list(PLANETS.keys())
        
        # Supported house systems
        house_systems = {
            'P': 'Placidus',
            'K': 'Koch',
            'E': 'Equal',
            'W': 'Whole Sign',
            'R': 'Regiomontanus',
            'C': 'Campanus',
            'A': 'Alcabitius',
            'B': 'Alcabitius',
            'X': 'Axial Rotation',
            'H': 'Azimuthal',
            'T': 'Polich/Page',
            'Y': 'APC houses'
        }
        
        # Current ayanamsa setting
        current_ayanamsa = 'Lahiri (SIDM_LAHIRI)'
        
        # Test calculation capability
        try:
            # Test with a sample date/time
            from datetime import date, time
            test_chart = calculate_complete_chart(
                date(2025, 1, 1),
                time(12, 0),
                13.0827,
                80.2707,
                'Asia/Kolkata'
            )
            calculation_status = 'working'
            test_result = {
                'ascendant_rasi': test_chart.get('ascendant_rasi'),
                'planets_calculated': len(test_chart.get('planetary_positions', {}))
            }
        except Exception as e:
            calculation_status = f'error: {str(e)}'
            test_result = None
        
        return jsonify({
            'success': True,
            'swiss_ephemeris_version': swiss_eph_version,
            'available_planets': available_planets,
            'planet_count': len(available_planets),
            'supported_house_systems': house_systems,
            'current_ayanamsa': current_ayanamsa,
            'current_house_system': 'Placidus',
            'calculation_status': calculation_status,
            'test_result': test_result,
            'features': {
                'ascendant_calculation': True,
                'house_cusps': True,
                'planetary_positions': True,
                'planetary_strengths': True,
                'sidereal_mode': True,
                'timezone_support': True
            }
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Error validating chart system: {str(e)}'
        }), 500


@app.route('/api/chart/calculate', methods=['POST'])
def calculate_chart():
    """
    Calculate complete astrological chart for an event
    
    Request body:
    {
        "date": "2025-12-10",           # Required: Event date (YYYY-MM-DD)
        "time": "14:30:00",             # Required: Event time (HH:MM:SS)
        "latitude": 13.0827,            # Required: Latitude in degrees
        "longitude": 80.2707,           # Required: Longitude in degrees
        "timezone": "Asia/Kolkata"      # Optional: Timezone (default: UTC)
    }
    
    Returns complete chart data including:
    - Ascendant (Lagna) information
    - House cusps
    - Planetary positions with house placements
    - Planetary strengths
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        # Required fields
        date_str = data.get('date')
        time_str = data.get('time')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if not all([date_str, time_str, latitude is not None, longitude is not None]):
            return jsonify({
                'error': 'Missing required fields',
                'required': ['date', 'time', 'latitude', 'longitude'],
                'optional': ['timezone']
            }), 400
        
        # Parse date
        try:
            event_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': f'Invalid date format: {date_str}. Use YYYY-MM-DD'}), 400
        
        # Parse time
        try:
            time_parts = time_str.split(':')
            if len(time_parts) == 3:
                hour, minute, second = map(int, time_parts)
            elif len(time_parts) == 2:
                hour, minute = map(int, time_parts)
                second = 0
            else:
                raise ValueError("Invalid time format")
            event_time = time(hour, minute, second)
        except (ValueError, IndexError):
            return jsonify({'error': f'Invalid time format: {time_str}. Use HH:MM:SS or HH:MM'}), 400
        
        # Validate coordinates
        try:
            latitude = float(latitude)
            longitude = float(longitude)
            
            if not (-90 <= latitude <= 90):
                return jsonify({'error': f'Latitude must be between -90 and 90. Got: {latitude}'}), 400
            
            if not (-180 <= longitude <= 180):
                return jsonify({'error': f'Longitude must be between -180 and 180. Got: {longitude}'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Latitude and longitude must be valid numbers'}), 400
        
        # Get timezone (optional, default to UTC)
        timezone_str = data.get('timezone', 'UTC')
        
        # Calculate complete chart
        chart_data = calculate_complete_chart(
            event_date=event_date,
            event_time=event_time,
            latitude=latitude,
            longitude=longitude,
            timezone_str=timezone_str
        )
        
        return jsonify({
            'success': True,
            'chart': chart_data
        })
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({
            'error': f'Error calculating chart: {str(e)}'
        }), 500


if __name__ == '__main__':
    # Railway sets PORT, fallback to FLASK_PORT or 8000
    port = int(os.getenv('PORT', os.getenv('FLASK_PORT', 8000)))
    host = os.getenv('HOST', '0.0.0.0')
    # Always False in production (Railway/Vercel set RAILWAY_ENVIRONMENT)
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true' and os.getenv('RAILWAY_ENVIRONMENT') is None
    
    print(f"🚀 Starting Cosmic Diary API Server on {host}:{port}")
    print(f"📊 Swiss Ephemeris version: {swe.version}")
    print(f"🔮 Using Ayanamsa: Lahiri (SIDM_LAHIRI)")
    
    app.run(host=host, port=port, debug=debug)
