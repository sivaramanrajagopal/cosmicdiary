"""
Flask API Server for Cosmic Diary
Handles planetary position calculations using Swiss Ephemeris
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, date
import swisseph as swe
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

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


def is_retrograde(planet_num: int, jd: float) -> bool:
    """Check if planet is retrograde"""
    if planet_num in [swe.SUN, swe.MOON, swe.TRUE_NODE]:
        return False  # Sun, Moon, and nodes are never retrograde
    
    # Get planet speed
    result = swe.calc_ut(jd, planet_num, swe.FLG_SWIEPH)
    if result:
        speed = result[0][3]  # Speed in longitude
        return speed < 0
    return False


def calculate_planet_position(planet_name: str, jd: float) -> Optional[Dict]:
    """Calculate position for a single planet"""
    if planet_name not in PLANETS:
        return None
    
    planet_num = PLANETS[planet_name]
    
    # Special handling for Ketu (South Node)
    if planet_name == 'Ketu':
        # Ketu is 180 degrees opposite to Rahu
        rahu_result = swe.calc_ut(jd, PLANETS['Rahu'], swe.FLG_SWIEPH)
        if not rahu_result:
            return None
        
        rahu_long = rahu_result[0][0]
        ketu_long = (rahu_long + 180) % 360
        
        return {
            'name': 'Ketu',
            'longitude': round(ketu_long, 2),
            'latitude': 0.0,
            'is_retrograde': False,  # Nodes don't retrograde
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
    is_retro = is_retrograde(planet_num, jd)
    
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


if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 8000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Starting Cosmic Diary API Server on port {port}")
    print(f"📊 Swiss Ephemeris version: {swe.version}")
    print(f"🔮 Using Ayanamsa: Lahiri (SIDM_LAHIRI)")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
