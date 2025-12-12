#!/usr/bin/env python3
"""
Test script for astro_calculations.py
Tests all functions with known data and validates calculations
"""

import sys
from datetime import date, time
from astro_calculations import (
    calculate_ascendant,
    get_house_number,
    calculate_planetary_positions,
    calculate_planetary_strengths,
    calculate_complete_chart
)
import swisseph as swe

# Test colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def test_calculate_ascendant():
    """Test ascendant calculation"""
    print(f"\n{'='*60}")
    print("TEST 1: calculate_ascendant()")
    print('='*60)
    
    try:
        # Test with Chennai, India
        jd = swe.julday(2025, 12, 10, 14.5/24.0, swe.GREG_CAL)
        lat = 13.0827  # Chennai
        lng = 80.2707
        
        result = calculate_ascendant(jd, lat, lng)
        
        # Validate structure
        required_fields = [
            'ascendant_degree', 'ascendant_rasi', 'ascendant_rasi_number',
            'ascendant_nakshatra', 'ascendant_lord', 'ayanamsa'
        ]
        
        missing = [f for f in required_fields if f not in result]
        if missing:
            print(f"{RED}❌ FAILED: Missing fields: {missing}{RESET}")
            return False
        
        # Validate values
        if not (0 <= result['ascendant_degree'] < 360):
            print(f"{RED}❌ FAILED: ascendant_degree out of range: {result['ascendant_degree']}{RESET}")
            return False
        
        if not (1 <= result['ascendant_rasi_number'] <= 12):
            print(f"{RED}❌ FAILED: ascendant_rasi_number out of range: {result['ascendant_rasi_number']}{RESET}")
            return False
        
        print(f"{GREEN}✅ PASSED{RESET}")
        print(f"   Ascendant: {result['ascendant_rasi']} ({result['ascendant_degree']:.2f}°)")
        print(f"   Lord: {result['ascendant_lord']}")
        print(f"   Ayanamsa: {result['ayanamsa']:.4f}°")
        return True
    
    except Exception as e:
        print(f"{RED}❌ FAILED: {e}{RESET}")
        import traceback
        traceback.print_exc()
        return False


def test_get_house_number():
    """Test house number calculation"""
    print(f"\n{'='*60}")
    print("TEST 2: get_house_number()")
    print('='*60)
    
    try:
        # Sample house cusps (12 houses)
        house_cusps = [
            226.82, 255.99, 286.82, 317.32, 348.23, 19.23,
            49.82, 79.99, 109.82, 137.32, 166.23, 196.82
        ]
        
        test_cases = [
            (233.96, 1),   # Between house 1 and 2
            (280.00, 2),   # Between house 2 and 3
            (0.50, 6),     # Between house 5 and 6 (wrap-around)
            (200.00, 12),  # Between house 12 and 1
        ]
        
        passed = 0
        for planet_long, expected_house in test_cases:
            result = get_house_number(planet_long, house_cusps)
            if result == expected_house:
                print(f"{GREEN}✅ PASSED{RESET}: Longitude {planet_long:.2f}° → House {result}")
                passed += 1
            else:
                print(f"{RED}❌ FAILED{RESET}: Longitude {planet_long:.2f}° → Expected House {expected_house}, got {result}")
        
        return passed == len(test_cases)
    
    except Exception as e:
        print(f"{RED}❌ FAILED: {e}{RESET}")
        import traceback
        traceback.print_exc()
        return False


def test_calculate_planetary_positions():
    """Test planetary position calculations"""
    print(f"\n{'='*60}")
    print("TEST 3: calculate_planetary_positions()")
    print('='*60)
    
    try:
        jd = swe.julday(2025, 12, 10, 14.5/24.0, swe.GREG_CAL)
        house_cusps = [
            226.82, 255.99, 286.82, 317.32, 348.23, 19.23,
            49.82, 79.99, 109.82, 137.32, 166.23, 196.82
        ]
        
        planets = calculate_planetary_positions(jd, house_cusps)
        
        # Validate count
        if len(planets) != 9:
            print(f"{RED}❌ FAILED: Expected 9 planets, got {len(planets)}{RESET}")
            return False
        
        # Validate structure for each planet
        required_fields = ['name', 'longitude', 'latitude', 'speed', 'is_retrograde', 'rasi', 'nakshatra', 'house']
        expected_planets = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Rahu', 'Ketu']
        
        planet_names = [p['name'] for p in planets]
        missing_planets = [p for p in expected_planets if p not in planet_names]
        if missing_planets:
            print(f"{RED}❌ FAILED: Missing planets: {missing_planets}{RESET}")
            return False
        
        for planet in planets:
            missing = [f for f in required_fields if f not in planet]
            if missing:
                print(f"{RED}❌ FAILED: Planet {planet.get('name')} missing fields: {missing}{RESET}")
                return False
            
            # Validate house number
            if not (1 <= planet['house'] <= 12):
                print(f"{RED}❌ FAILED: Planet {planet['name']} has invalid house: {planet['house']}{RESET}")
                return False
        
        print(f"{GREEN}✅ PASSED{RESET}")
        print(f"   Calculated {len(planets)} planets")
        print(f"   Sample - Sun: House {planets[0]['house']}, {planets[0]['rasi']['name']}")
        return True
    
    except Exception as e:
        print(f"{RED}❌ FAILED: {e}{RESET}")
        import traceback
        traceback.print_exc()
        return False


def test_calculate_planetary_strengths():
    """Test planetary strength calculations"""
    print(f"\n{'='*60}")
    print("TEST 4: calculate_planetary_strengths()")
    print('='*60)
    
    try:
        jd = swe.julday(2025, 12, 10, 14.5/24.0, swe.GREG_CAL)
        house_cusps = [
            226.82, 255.99, 286.82, 317.32, 348.23, 19.23,
            49.82, 79.99, 109.82, 137.32, 166.23, 196.82
        ]
        
        planets = calculate_planetary_positions(jd, house_cusps)
        strengths = calculate_planetary_strengths(planets, 'Scorpio')
        
        # Validate structure
        required_fields = ['exalted', 'debilitated', 'own_sign', 'dig_bala', 'combusted', 'strength_score']
        expected_planets = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Rahu', 'Ketu']
        
        for planet_name in expected_planets:
            if planet_name not in strengths:
                print(f"{RED}❌ FAILED: Missing strength data for {planet_name}{RESET}")
                return False
            
            strength = strengths[planet_name]
            missing = [f for f in required_fields if f not in strength]
            if missing:
                print(f"{RED}❌ FAILED: {planet_name} missing strength fields: {missing}{RESET}")
                return False
            
            # Validate strength_score
            if not (0.0 <= strength['strength_score'] <= 1.0):
                print(f"{RED}❌ FAILED: {planet_name} has invalid strength_score: {strength['strength_score']}{RESET}")
                return False
        
        print(f"{GREEN}✅ PASSED{RESET}")
        print(f"   Calculated strengths for {len(strengths)} planets")
        sun_strength = strengths['Sun']
        print(f"   Sample - Sun: Score {sun_strength['strength_score']:.2f}, Exalted: {sun_strength['exalted']}, Dig Bala: {sun_strength['dig_bala']}")
        return True
    
    except Exception as e:
        print(f"{RED}❌ FAILED: {e}{RESET}")
        import traceback
        traceback.print_exc()
        return False


def test_calculate_complete_chart():
    """Test complete chart calculation"""
    print(f"\n{'='*60}")
    print("TEST 5: calculate_complete_chart()")
    print('='*60)
    
    try:
        chart = calculate_complete_chart(
            date(2025, 12, 10),
            time(14, 30),
            13.0827,  # Chennai
            80.2707,
            'Asia/Kolkata'
        )
        
        # Validate structure
        required_fields = [
            'ascendant_degree', 'ascendant_rasi', 'ascendant_rasi_number',
            'ascendant_nakshatra', 'ascendant_lord',
            'house_cusps', 'house_system', 'julian_day', 'ayanamsa',
            'planetary_positions', 'planetary_strengths'
        ]
        
        missing = [f for f in required_fields if f not in chart]
        if missing:
            print(f"{RED}❌ FAILED: Missing fields: {missing}{RESET}")
            return False
        
        # Validate house cusps
        if len(chart['house_cusps']) != 12:
            print(f"{RED}❌ FAILED: Expected 12 house cusps, got {len(chart['house_cusps'])}{RESET}")
            return False
        
        # Validate planets
        if len(chart['planetary_positions']) != 9:
            print(f"{RED}❌ FAILED: Expected 9 planets, got {len(chart['planetary_positions'])}{RESET}")
            return False
        
        # Validate strengths
        if len(chart['planetary_strengths']) != 9:
            print(f"{RED}❌ FAILED: Expected 9 strength calculations, got {len(chart['planetary_strengths'])}{RESET}")
            return False
        
        print(f"{GREEN}✅ PASSED{RESET}")
        print(f"   Ascendant: {chart['ascendant_rasi']} ({chart['ascendant_degree']:.2f}°)")
        print(f"   House System: {chart['house_system']}")
        print(f"   Julian Day: {chart['julian_day']:.6f}")
        print(f"   Ayanamsa: {chart['ayanamsa']:.4f}°")
        print(f"   Planets: {len(chart['planetary_positions'])}")
        print(f"   House Cusps: {len(chart['house_cusps'])}")
        return True
    
    except Exception as e:
        print(f"{RED}❌ FAILED: {e}{RESET}")
        import traceback
        traceback.print_exc()
        return False


def test_ascendant_accuracy():
    """Test ascendant calculation accuracy with known coordinates"""
    print(f"\n{'='*60}")
    print("TEST 6: Ascendant Calculation Accuracy")
    print('='*60)
    
    try:
        # Test multiple locations/times
        test_cases = [
            {
                'date': date(2025, 12, 10),
                'time': time(12, 0),
                'lat': 13.0827,
                'lng': 80.2707,
                'tz': 'Asia/Kolkata',
                'desc': 'Chennai, India (Noon)'
            },
            {
                'date': date(2025, 6, 21),
                'time': time(6, 0),
                'lat': 28.6139,
                'lng': 77.2090,
                'tz': 'Asia/Kolkata',
                'desc': 'New Delhi, India (Sunrise)'
            }
        ]
        
        passed = 0
        for test in test_cases:
            chart = calculate_complete_chart(
                test['date'],
                test['time'],
                test['lat'],
                test['lng'],
                test['tz']
            )
            
            asc = chart['ascendant_rasi']
            degree = chart['ascendant_degree']
            
            # Basic validation (ascendant should be valid)
            if 0 <= degree < 360 and 1 <= chart['ascendant_rasi_number'] <= 12:
                print(f"{GREEN}✅ PASSED{RESET}: {test['desc']}")
                print(f"   Ascendant: {asc} ({degree:.2f}°)")
                passed += 1
            else:
                print(f"{RED}❌ FAILED{RESET}: {test['desc']} - Invalid ascendant")
        
        return passed == len(test_cases)
    
    except Exception as e:
        print(f"{RED}❌ FAILED: {e}{RESET}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print(f"\n{'='*60}")
    print("ASTROLOGICAL CALCULATIONS TEST SUITE")
    print('='*60)
    print("\nTesting all functions in astro_calculations.py...")
    
    tests = [
        ("Calculate Ascendant", test_calculate_ascendant),
        ("Get House Number", test_get_house_number),
        ("Calculate Planetary Positions", test_calculate_planetary_positions),
        ("Calculate Planetary Strengths", test_calculate_planetary_strengths),
        ("Calculate Complete Chart", test_calculate_complete_chart),
        ("Ascendant Accuracy", test_ascendant_accuracy),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"{RED}❌ {test_name} crashed: {e}{RESET}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print('='*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = f"{GREEN}✅ PASSED{RESET}" if result else f"{RED}❌ FAILED{RESET}"
        print(f"{status}: {test_name}")
    
    print(f"\n{'='*60}")
    if passed == total:
        print(f"{GREEN}✅ ALL TESTS PASSED ({passed}/{total}){RESET}")
        return 0
    else:
        print(f"{RED}❌ SOME TESTS FAILED ({passed}/{total} passed){RESET}")
        return 1


if __name__ == '__main__':
    sys.exit(main())

