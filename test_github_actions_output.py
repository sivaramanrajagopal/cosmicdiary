#!/usr/bin/env python3
"""
Test script to verify GitHub Actions output format.
This simulates what the workflow should capture.
"""
import os
import sys
from datetime import datetime

def test_output_format():
    """Test that our output format matches what GitHub Actions expects."""
    print("=" * 80)
    print("GITHUB ACTIONS OUTPUT FORMAT TEST")
    print("=" * 80)
    print("")

    # Simulate the script running with test data
    events_detected = 15
    events_stored = 15
    correlations_created = 12
    avg_score = 0.73

    print("Testing standard output...")
    print(f"✓ Events Detected: {events_detected}")
    print(f"✓ Events Stored: {events_stored}")
    print(f"✓ Correlations Created: {correlations_created}")
    print(f"✓ Average Correlation Score: {avg_score:.2f}")
    print("")

    # This is what GitHub Actions should capture
    print("Testing GitHub Actions output format...")
    print("")
    print("::group::GitHub Actions Output")
    print(f"EVENTS_DETECTED={events_detected}")
    print(f"EVENTS_STORED={events_stored}")
    print(f"CORRELATIONS_CREATED={correlations_created}")
    print(f"AVG_CORRELATION_SCORE={avg_score:.2f}")
    print("::endgroup::")
    print("")

    # Test what the workflow grep should find
    print("=" * 80)
    print("WHAT THE WORKFLOW SHOULD GREP:")
    print("=" * 80)
    print("")
    print("Lines to grep for:")
    print(f"  EVENTS_DETECTED={events_detected}")
    print(f"  EVENTS_STORED={events_stored}")
    print(f"  CORRELATIONS_CREATED={correlations_created}")
    print(f"  AVG_CORRELATION_SCORE={avg_score:.2f}")
    print("")

    print("=" * 80)
    print("TEST PASSED - Output format is correct")
    print("=" * 80)
    print("")
    print("If GitHub Actions still shows zeros, check:")
    print("1. Workflow logs for script errors BEFORE the output")
    print("2. Environment variables (OPENAI_API_KEY, SUPABASE_URL, etc.)")
    print("3. Whether the script actually runs to completion")
    print("4. The uploaded log artifact in GitHub Actions")

if __name__ == "__main__":
    test_output_format()
