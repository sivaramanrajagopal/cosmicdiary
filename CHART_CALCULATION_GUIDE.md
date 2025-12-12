# 🔮 Chart Calculation Guide

**Complete astrological chart calculations using Swiss Ephemeris**

---

## 📋 Overview

The `astro_calculations.py` module provides functions for calculating complete Vedic astrological charts including:

- **Ascendant (Lagna)** calculation
- **House cusps** (12 houses)
- **Planetary positions** with house placements
- **Planetary strengths** (exaltation, debilitation, own sign, dig bala, combustion)

---

## 🎯 Functions

### 1. `calculate_ascendant(jd, lat, lng)`

Calculates the ascendant (Lagna) for a given time and location.

**Parameters:**
- `jd` (float): Julian Day number
- `lat` (float): Latitude in degrees
- `lng` (float): Longitude in degrees

**Returns:**
```python
{
    'ascendant_degree': 254.156,
    'ascendant_rasi': 'Sagittarius',
    'ascendant_rasi_number': 9,
    'ascendant_nakshatra': 'Mula',
    'ascendant_lord': 'Jupiter',
    'ayanamsa': 24.1234
}
```

---

### 2. `get_house_number(planet_longitude, house_cusps)`

Determines which house (1-12) a planet is in.

**Parameters:**
- `planet_longitude` (float): Planet's longitude (0-360°)
- `house_cusps` (List[float]): List of 12 house cusp degrees

**Returns:**
- `int`: House number (1-12)

---

### 3. `calculate_planetary_positions(jd, house_cusps)`

Calculates positions for all 9 planets with house placements.

**Parameters:**
- `jd` (float): Julian Day number
- `house_cusps` (List[float]): List of 12 house cusp degrees

**Returns:**
```python
[
    {
        'name': 'Sun',
        'longitude': 254.123456,
        'latitude': 0.0,
        'speed': 1.0,
        'is_retrograde': False,
        'rasi': {'name': 'Sagittarius', 'number': 9, 'lord': {'name': 'Jupiter'}},
        'nakshatra': {'name': 'Mula', 'number': 18, 'pada': 3},
        'house': 10
    },
    ... 8 more planets
]
```

---

### 4. `calculate_planetary_strengths(planets, asc_rasi)`

Calculates planetary strengths.

**Parameters:**
- `planets` (List[Dict]): List of planetary positions
- `asc_rasi` (str): Ascendant rasi name

**Returns:**
```python
{
    'Sun': {
        'exalted': False,
        'debilitated': False,
        'own_sign': False,
        'dig_bala': True,
        'combusted': False,
        'strength_score': 0.65
    },
    ... all 9 planets
}
```

**Strength Factors:**
- **Exaltation**: Planet within 5° of exaltation point (+0.3)
- **Debilitation**: Planet within 5° of debilitation point (-0.3)
- **Own Sign**: Planet in its own sign (+0.2)
- **Dig Bala**: Planet in directional strength house (+0.15)
- **Combustion**: Planet too close to Sun (-0.2)

---

### 5. `calculate_complete_chart(date, time, lat, lng, tz)`

Main function to calculate complete astrological chart.

**Parameters:**
- `event_date` (date): Event date
- `event_time` (time): Event time
- `latitude` (float): Latitude in degrees
- `longitude` (float): Longitude in degrees
- `timezone_str` (str): Timezone string (default: 'UTC')

**Returns:**
Complete chart data dictionary matching `event_chart_data` table structure.

---

## 🔌 API Endpoint

### `POST /api/chart/calculate`

Calculate complete astrological chart for an event.

**Request Body:**
```json
{
    "date": "2025-12-10",
    "time": "14:30:00",
    "latitude": 13.0827,
    "longitude": 80.2707,
    "timezone": "Asia/Kolkata"
}
```

**Response:**
```json
{
    "success": true,
    "chart": {
        "ascendant_degree": 254.156,
        "ascendant_rasi": "Sagittarius",
        "ascendant_rasi_number": 9,
        "ascendant_nakshatra": "Mula",
        "ascendant_lord": "Jupiter",
        "house_cusps": [254.16, 283.45, ...],
        "house_system": "Placidus",
        "julian_day": 2460385.104,
        "sidereal_time": 256.789,
        "ayanamsa": 24.1234,
        "planetary_positions": { ... },
        "planetary_strengths": { ... }
    }
}
```

---

## 📝 Usage Examples

### Python

```python
from datetime import date, time
from astro_calculations import calculate_complete_chart

# Calculate chart for Chennai, India
chart = calculate_complete_chart(
    date(2025, 12, 10),
    time(14, 30),
    13.0827,  # Latitude
    80.2707,  # Longitude
    'Asia/Kolkata'
)

print(f"Ascendant: {chart['ascendant_rasi']}")
print(f"House 1 cusp: {chart['house_cusps'][0]}°")
```

### API Call

```bash
curl -X POST http://localhost:8000/api/chart/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2025-12-10",
    "time": "14:30:00",
    "latitude": 13.0827,
    "longitude": 80.2707,
    "timezone": "Asia/Kolkata"
  }'
```

---

## ⚙️ Configuration

### Ayanamsa
- **Lahiri** (SIDM_LAHIRI) - Standard for Vedic astrology

### House System
- **Placidus** (default) - Most common in Western astrology
- Can be changed: 'P' (Placidus), 'K' (Koch), 'E' (Equal), 'W' (Whole Sign)

### Timezone
- Use IANA timezone strings (e.g., 'Asia/Kolkata', 'America/New_York')
- Defaults to UTC if not specified

---

## 🧪 Testing

```bash
# Test the module
python3 -c "from astro_calculations import calculate_complete_chart; from datetime import date, time; print(calculate_complete_chart(date(2025,12,10), time(14,30), 13.0827, 80.2707, 'Asia/Kolkata'))"

# Test API endpoint
curl -X POST http://localhost:8000/api/chart/calculate \
  -H "Content-Type: application/json" \
  -d '{"date":"2025-12-10","time":"14:30:00","latitude":13.0827,"longitude":80.2707,"timezone":"Asia/Kolkata"}'
```

---

## 📊 Data Structure

The chart data matches the `event_chart_data` table structure:

- **Ascendant**: Degree, Rasi, Nakshatra, Lord
- **House Cusps**: 12 cusp degrees (sidereal)
- **Planetary Positions**: All 9 planets with longitude, latitude, speed, rasi, nakshatra, house
- **Planetary Strengths**: Exaltation, debilitation, own sign, dig bala, combustion, strength score

---

## 🔍 Notes

- All calculations use **sidereal** zodiac (Lahiri ayanamsa)
- House cusps are converted from tropical to sidereal
- Planetary positions include house placements
- Strength calculations follow traditional Vedic principles
- All angles are in degrees (0-360)

---

**Ready to calculate charts!** 🌙✨

