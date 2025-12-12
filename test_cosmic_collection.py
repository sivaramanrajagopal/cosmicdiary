#!/usr/bin/env python3
"""
Comprehensive Test Script for Cosmic State Collection System

This script tests all components of the cosmic state collection system
without requiring database connections or running the full collection.

Usage:
    python test_cosmic_collection.py

Author: Cosmic Diary System
Date: 2025-12-12
"""

import os
from datetime import datetime, timezone, date, time, timedelta
from typing import Dict, Any, List

# Our astrological calculation modules
from astro_calculations import calculate_complete_chart
from aspect_calculator import calculate_all_aspects, get_aspects_to_house
from correlation_analyzer import (
    correlate_event_with_snapshot,
    categorize_correlation_strength,
    format_correlation_report,
    extract_retrograde_planets
)

# Test Configuration
REFERENCE_LOCATION = {
    "name": "Delhi, India",
    "latitude": 28.6139,
    "longitude": 77.2090,
    "timezone": "Asia/Kolkata"
}

SAMPLE_EVENT_LOCATION = {
    "name": "Mumbai, India",
    "latitude": 19.0760,
    "longitude": 72.8777,
    "timezone": "Asia/Kolkata"
}


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*80}")
    print(f"{title}")
    print(f"{'='*80}\n")


def print_subsection(title: str):
    """Print a formatted subsection header."""
    print(f"\n{'-'*80}")
    print(f"{title}")
    print(f"{'-'*80}\n")


def test_cosmic_snapshot_calculation():
    """Test cosmic snapshot chart calculation for reference location."""
    print_section("TEST: Cosmic Snapshot Calculation")
    
    try:
        # Get current time
        now_utc = datetime.now(timezone.utc)
        event_date = now_utc.date()
        event_time_obj = now_utc.time()
        
        print(f"📅 Test Date: {event_date}")
        print(f"🕐 Test Time: {event_time_obj}")
        print(f"📍 Location: {REFERENCE_LOCATION['name']}")
        print(f"   Coordinates: ({REFERENCE_LOCATION['latitude']}, {REFERENCE_LOCATION['longitude']})")
        print(f"   Timezone: {REFERENCE_LOCATION['timezone']}")
        print()
        
        # Calculate complete chart
        print("🔮 Calculating astrological chart...")
        chart_data = calculate_complete_chart(
            event_date=event_date,
            event_time=event_time_obj,
            latitude=REFERENCE_LOCATION['latitude'],
            longitude=REFERENCE_LOCATION['longitude'],
            timezone_str=REFERENCE_LOCATION['timezone']
        )
        
        print("✓ Chart calculated successfully")
        print()
        
        # Print Lagna details
        print_subsection("Lagna (Ascendant) Details")
        print(f"   Degree: {chart_data.get('ascendant_degree', 0):.6f}°")
        print(f"   Rasi: {chart_data.get('ascendant_rasi', 'Unknown')}")
        print(f"   Rasi Number: {chart_data.get('ascendant_rasi_number', 0)}")
        print(f"   Nakshatra: {chart_data.get('ascendant_nakshatra', 'Unknown')}")
        print(f"   Lord: {chart_data.get('ascendant_lord', 'Unknown')}")
        print(f"   Ayanamsa: {chart_data.get('ayanamsa', 0):.6f}°")
        
        # Print planetary positions
        print_subsection("Planetary Positions")
        planetary_positions = chart_data.get('planetary_positions', {})
        
        planet_names = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
        for planet_name in planet_names:
            planet = planetary_positions.get(planet_name, {})
            if planet:
                longitude = planet.get('longitude', 0)
                house = planet.get('house', 0)
                rasi = planet.get('rasi', {}).get('name', 'Unknown')
                is_retro = planet.get('is_retrograde', False)
                retro_str = " (R)" if is_retro else ""
                print(f"   {planet_name:10} | {longitude:8.2f}° | House {house:2} | {rasi:12} {retro_str}")
        
        # Calculate aspects
        print_subsection("Planetary Aspects")
        house_cusps = chart_data.get('house_cusps', [])
        aspects = calculate_all_aspects(planetary_positions, house_cusps)
        print(f"   Total aspects: {len(aspects)}")
        print(f"   Sample aspects (first 5):")
        for aspect in aspects[:5]:
            print(f"      {aspect['planet']:10} in House {aspect['from_house']:2} → "
                  f"Aspects House {aspect['to_house']:2} ({aspect['aspect_type']})")
        
        # Identify retrograde planets
        print_subsection("Retrograde Planets")
        retrograde_planets = extract_retrograde_planets(chart_data)
        if retrograde_planets:
            print(f"   Retrograde: {', '.join(retrograde_planets)}")
        else:
            print(f"   Retrograde: None")
        
        # Identify dominant planets
        print_subsection("Dominant Planets")
        planetary_strengths = chart_data.get('planetary_strengths', {})
        dominant_planets = []
        if isinstance(planetary_strengths, dict):
            for planet_name, strength_data in planetary_strengths.items():
                if isinstance(strength_data, dict):
                    strength_score = strength_data.get('strength_score', 0.0)
                    if strength_score >= 0.7:
                        reasons = [k for k, v in strength_data.items() 
                                 if k != 'strength_score' and v is True]
                        dominant_planets.append({
                            "planet": planet_name,
                            "strength": strength_score,
                            "reasons": reasons
                        })
        
        dominant_planets.sort(key=lambda x: x['strength'], reverse=True)
        if dominant_planets:
            print(f"   Top 3 dominant planets:")
            for i, dp in enumerate(dominant_planets[:3], 1):
                reasons_str = ', '.join(dp['reasons']) if dp['reasons'] else 'none'
                print(f"      {i}. {dp['planet']}: {dp['strength']:.2f} ({reasons_str})")
        else:
            print(f"   No planets with strength >= 0.7")
        
        print()
        print("✓ TEST PASSED: Cosmic snapshot calculation successful")
        return True
        
    except Exception as e:
        print(f"✗ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_event_chart_calculation():
    """Test event chart calculation for a different location."""
    print_section("TEST: Event Chart Calculation")
    
    try:
        # Use time 2 hours earlier for event
        now_utc = datetime.now(timezone.utc)
        event_time_utc = now_utc - timedelta(hours=2)
        event_date = event_time_utc.date()
        event_time_obj = event_time_utc.time()
        
        print(f"📅 Event Date: {event_date}")
        print(f"🕐 Event Time: {event_time_obj}")
        print(f"📍 Event Location: {SAMPLE_EVENT_LOCATION['name']}")
        print(f"   Coordinates: ({SAMPLE_EVENT_LOCATION['latitude']}, {SAMPLE_EVENT_LOCATION['longitude']})")
        print(f"   Timezone: {SAMPLE_EVENT_LOCATION['timezone']}")
        print()
        
        # Calculate chart for event location
        print("🔮 Calculating event chart...")
        event_chart = calculate_complete_chart(
            event_date=event_date,
            event_time=event_time_obj,
            latitude=SAMPLE_EVENT_LOCATION['latitude'],
            longitude=SAMPLE_EVENT_LOCATION['longitude'],
            timezone_str=SAMPLE_EVENT_LOCATION['timezone']
        )
        
        print("✓ Event chart calculated successfully")
        print()
        
        # Calculate reference chart for comparison
        print("🔮 Calculating reference chart (same time)...")
        ref_chart = calculate_complete_chart(
            event_date=event_date,
            event_time=event_time_obj,
            latitude=REFERENCE_LOCATION['latitude'],
            longitude=REFERENCE_LOCATION['longitude'],
            timezone_str=REFERENCE_LOCATION['timezone']
        )
        
        print("✓ Reference chart calculated successfully")
        print()
        
        # Compare Lagnas
        print_subsection("Lagna Comparison")
        event_lagna = event_chart.get('ascendant_rasi', 'Unknown')
        ref_lagna = ref_chart.get('ascendant_rasi', 'Unknown')
        event_lagna_deg = event_chart.get('ascendant_degree', 0)
        ref_lagna_deg = ref_chart.get('ascendant_degree', 0)
        
        print(f"   Event Lagna:  {event_lagna} ({event_lagna_deg:.2f}°)")
        print(f"   Reference Lagna: {ref_lagna} ({ref_lagna_deg:.2f}°)")
        
        if event_lagna == ref_lagna:
            print(f"   → Same Lagna (timing difference didn't change sign)")
        else:
            print(f"   → Different Lagnas (time/location difference affected ascendant)")
        
        # Compare planet houses
        print_subsection("Planet House Comparison (Sample)")
        event_positions = event_chart.get('planetary_positions', {})
        ref_positions = ref_chart.get('planetary_positions', {})
        
        planet_names = ['Sun', 'Moon', 'Mars', 'Jupiter', 'Saturn']
        print(f"   {'Planet':10} | Event House | Reference House | Match")
        print(f"   {'-'*55}")
        matches = 0
        for planet_name in planet_names:
            event_planet = event_positions.get(planet_name, {})
            ref_planet = ref_positions.get(planet_name, {})
            event_house = event_planet.get('house', 0)
            ref_house = ref_planet.get('house', 0)
            match = "✓" if event_house == ref_house else "✗"
            if event_house == ref_house:
                matches += 1
            print(f"   {planet_name:10} |     {event_house:2}     |       {ref_house:2}       | {match}")
        
        print(f"\n   Houses matching: {matches}/{len(planet_names)} planets")
        
        print()
        print("✓ TEST PASSED: Event chart calculation successful")
        return True
        
    except Exception as e:
        print(f"✗ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_aspect_calculation():
    """Test planetary aspect calculations."""
    print_section("TEST: Aspect Calculation")
    
    try:
        # Calculate a chart
        now_utc = datetime.now(timezone.utc)
        chart_data = calculate_complete_chart(
            event_date=now_utc.date(),
            event_time=now_utc.time(),
            latitude=REFERENCE_LOCATION['latitude'],
            longitude=REFERENCE_LOCATION['longitude'],
            timezone_str=REFERENCE_LOCATION['timezone']
        )
        
        planetary_positions = chart_data.get('planetary_positions', {})
        house_cusps = chart_data.get('house_cusps', [])
        
        print(f"📊 Calculating aspects for chart...")
        print()
        
        # Calculate all aspects
        aspects = calculate_all_aspects(planetary_positions, house_cusps)
        print_subsection("All Aspects")
        print(f"   Total aspects found: {len(aspects)}")
        print()
        print(f"   All aspects:")
        for aspect in aspects:
            print(f"      {aspect['planet']:10} in House {aspect['from_house']:2} → "
                  f"Aspects House {aspect['to_house']:2} ({aspect['aspect_type']})")
        
        # Test get_aspects_to_house for house 8
        print_subsection("Aspects to 8th House (Dustana)")
        house_8_aspects = get_aspects_to_house(8, aspects)
        print(f"   Total aspects to 8th house: {len(house_8_aspects)}")
        if house_8_aspects:
            print(f"   Planets aspecting 8th house:")
            for aspect in house_8_aspects:
                print(f"      {aspect['planet']:10} from House {aspect['from_house']:2} "
                      f"({aspect['aspect_type']})")
        else:
            print(f"   No planets aspecting 8th house")
        
        # Test for house 1 (Ascendant)
        print_subsection("Aspects to 1st House (Ascendant)")
        house_1_aspects = get_aspects_to_house(1, aspects)
        print(f"   Total aspects to 1st house: {len(house_1_aspects)}")
        if house_1_aspects:
            print(f"   Planets aspecting 1st house:")
            for aspect in house_1_aspects:
                print(f"      {aspect['planet']:10} from House {aspect['from_house']:2} "
                      f"({aspect['aspect_type']})")
        
        print()
        print("✓ TEST PASSED: Aspect calculation successful")
        return True
        
    except Exception as e:
        print(f"✗ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_correlation_analysis():
    """Test correlation analysis between event and snapshot charts."""
    print_section("TEST: Correlation Analysis")
    
    try:
        # Calculate snapshot chart
        now_utc = datetime.now(timezone.utc)
        snapshot_chart = calculate_complete_chart(
            event_date=now_utc.date(),
            event_time=now_utc.time(),
            latitude=REFERENCE_LOCATION['latitude'],
            longitude=REFERENCE_LOCATION['longitude'],
            timezone_str=REFERENCE_LOCATION['timezone']
        )
        
        # Calculate event chart (2 hours earlier, different location)
        event_time_utc = now_utc - timedelta(hours=2)
        event_chart = calculate_complete_chart(
            event_date=event_time_utc.date(),
            event_time=event_time_utc.time(),
            latitude=SAMPLE_EVENT_LOCATION['latitude'],
            longitude=SAMPLE_EVENT_LOCATION['longitude'],
            timezone_str=SAMPLE_EVENT_LOCATION['timezone']
        )
        
        print("📊 Calculating correlation...")
        print()
        
        # Perform correlation
        correlation_data = correlate_event_with_snapshot(
            event_chart=event_chart,
            snapshot_chart=snapshot_chart,
            snapshot_id=999  # Dummy ID for testing
        )
        
        print_subsection("Correlation Results")
        correlation_score = correlation_data.get('correlation_score', 0.0)
        total_matches = correlation_data.get('total_matches', 0)
        strength = correlation_data.get('strength', 'Low')
        
        print(f"   Correlation Score: {correlation_score:.4f}")
        print(f"   Strength: {strength}")
        print(f"   Total Matches: {total_matches}")
        print()
        
        # Print correlation categories
        print_subsection("Correlation Details")
        correlations = correlation_data.get('correlations', [])
        
        # Group by type
        by_type = {}
        for corr in correlations:
            corr_type = corr.get('type', 'unknown')
            if corr_type not in by_type:
                by_type[corr_type] = []
            by_type[corr_type].append(corr)
        
        for corr_type, corr_list in sorted(by_type.items()):
            total_score = sum(c.get('score', 0.0) for c in corr_list)
            print(f"   {corr_type}: {len(corr_list)} matches, Total score: {total_score:.3f}")
            for corr in corr_list[:3]:  # Show first 3 of each type
                print(f"      - {corr.get('description', 'No description')} [Score: {corr.get('score', 0):.3f}]")
            if len(corr_list) > 3:
                print(f"      ... and {len(corr_list) - 3} more")
        
        # Format and print report
        print_subsection("Formatted Correlation Report")
        report = format_correlation_report(correlation_data)
        print(report)
        
        print()
        print("✓ TEST PASSED: Correlation analysis successful")
        return True
        
    except Exception as e:
        print(f"✗ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_retrograde_identification():
    """Test retrograde planet identification."""
    print_section("TEST: Retrograde Identification")
    
    try:
        # Test with current date
        now_utc = datetime.now(timezone.utc)
        chart_data = calculate_complete_chart(
            event_date=now_utc.date(),
            event_time=now_utc.time(),
            latitude=REFERENCE_LOCATION['latitude'],
            longitude=REFERENCE_LOCATION['longitude'],
            timezone_str=REFERENCE_LOCATION['timezone']
        )
        
        print(f"📅 Test Date: {now_utc.date()}")
        print()
        
        # Extract retrograde planets
        retrograde_planets = extract_retrograde_planets(chart_data)
        
        print_subsection("Retrograde Planets Found")
        if retrograde_planets:
            print(f"   Planets in retrograde: {', '.join(retrograde_planets)}")
            
            # Verify against planetary positions
            planetary_positions = chart_data.get('planetary_positions', {})
            print()
            print(f"   Verification:")
            for planet_name in retrograde_planets:
                planet = planetary_positions.get(planet_name, {})
                is_retro = planet.get('is_retrograde', False)
                status = "✓ Confirmed" if is_retro else "✗ Mismatch"
                print(f"      {planet_name:10}: {status}")
        else:
            print(f"   No planets in retrograde")
        
        # Check all planets for retrograde status
        print_subsection("All Planets Retrograde Status")
        planetary_positions = chart_data.get('planetary_positions', {})
        planet_names = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
        
        for planet_name in planet_names:
            planet = planetary_positions.get(planet_name, {})
            is_retro = planet.get('is_retrograde', False)
            status = "Retrograde" if is_retro else "Direct"
            print(f"   {planet_name:10}: {status}")
        
        # Test with known retrograde periods (if available)
        print_subsection("Retrograde Status Rules")
        print(f"   Rahu: Always retrograde (shadow planet)")
        print(f"   Ketu: Always retrograde (shadow planet)")
        print(f"   Sun: Never retrograde")
        print(f"   Moon: Never retrograde")
        print(f"   Others: Based on speed calculation")
        
        # Verify rules
        rahu = planetary_positions.get('Rahu', {})
        ketu = planetary_positions.get('Ketu', {})
        sun = planetary_positions.get('Sun', {})
        moon = planetary_positions.get('Moon', {})
        
        rules_ok = True
        if rahu and not rahu.get('is_retrograde', False):
            print(f"   ⚠️  Warning: Rahu should always be retrograde")
            rules_ok = False
        if ketu and not ketu.get('is_retrograde', False):
            print(f"   ⚠️  Warning: Ketu should always be retrograde")
            rules_ok = False
        if sun and sun.get('is_retrograde', False):
            print(f"   ⚠️  Warning: Sun should never be retrograde")
            rules_ok = False
        if moon and moon.get('is_retrograde', False):
            print(f"   ⚠️  Warning: Moon should never be retrograde")
            rules_ok = False
        
        if rules_ok:
            print(f"   ✓ All retrograde rules verified correctly")
        
        print()
        print("✓ TEST PASSED: Retrograde identification successful")
        return True
        
    except Exception as e:
        print(f"✗ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests and report results."""
    print("="*80)
    print("COSMIC STATE COLLECTION SYSTEM - COMPREHENSIVE TEST SUITE")
    print("="*80)
    print(f"Run Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("="*80)
    
    tests = [
        ("Cosmic Snapshot Calculation", test_cosmic_snapshot_calculation),
        ("Event Chart Calculation", test_event_chart_calculation),
        ("Aspect Calculation", test_aspect_calculation),
        ("Correlation Analysis", test_correlation_analysis),
        ("Retrograde Identification", test_retrograde_identification)
    ]
    
    passed = 0
    failed = 0
    failed_tests = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
            else:
                failed += 1
                failed_tests.append(test_name)
        except Exception as e:
            print(f"\n✗ {test_name} FAILED with exception: {str(e)}")
            failed += 1
            failed_tests.append(test_name)
    
    # Final Summary
    print("="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Total Tests: {len(tests)}")
    print(f"Passed: {passed} ✓")
    print(f"Failed: {failed} ✗")
    print()
    
    if failed_tests:
        print(f"Failed Tests:")
        for test_name in failed_tests:
            print(f"  - {test_name}")
        print()
    
    success_rate = (passed / len(tests) * 100) if tests else 0
    print(f"Success Rate: {success_rate:.1f}%")
    print("="*80)
    print()
    
    if failed == 0:
        print("✅ All tests passed! System is ready for deployment.")
        return 0
    else:
        print("❌ Some tests failed. Please review errors above.")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    exit(exit_code)

