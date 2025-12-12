#!/bin/bash

echo "🧪 Quick Test Suite for Cosmic Diary"
echo "===================================="
echo ""

# Test 1: API Health
echo -n "Test 1: Flask API Health Check... "
if curl -s http://localhost:8000/health 2>/dev/null | grep -q "healthy"; then
    echo "✅ PASS"
else
    echo "❌ FAIL (Is Flask API running on port 8000?)"
fi

# Test 2: Planetary Data
echo -n "Test 2: Planetary Data Calculation... "
if curl -s "http://localhost:8000/api/planets/daily?date=2025-12-10" 2>/dev/null | grep -q "planets"; then
    echo "✅ PASS"
else
    echo "❌ FAIL (Check Flask API)"
fi

# Test 3: Rahu/Ketu Fix
echo -n "Test 3: Rahu/Ketu 180° Verification... "
python3 << 'PYEOF' > /dev/null 2>&1
import sys
sys.path.insert(0, '.')
from api_server import calculate_planet_position
import swisseph as swe
jd = swe.julday(2025, 12, 10, 12.0/24.0, swe.GREG_CAL)
rahu = calculate_planet_position('Rahu', jd)
ketu = calculate_planet_position('Ketu', jd)
diff = abs(ketu['longitude'] - rahu['longitude'])
if diff > 180:
    diff = 360 - diff
if abs(diff - 180.0) < 0.1:
    print("✅ PASS")
    sys.exit(0)
else:
    print("❌ FAIL")
    sys.exit(1)
PYEOF
test $? -eq 0 && echo "✅ PASS" || echo "❌ FAIL"

# Test 4: Frontend
echo -n "Test 4: Next.js Frontend... "
if curl -s http://localhost:3002 2>/dev/null | grep -q "Cosmic Diary"; then
    echo "✅ PASS"
else
    echo "⚠️  SKIP (Frontend may be on different port or not running)"
fi

echo ""
echo "===================================="
echo "Test Summary Complete!"
echo ""
echo "🌐 URLs:"
echo "  • Frontend: http://localhost:3002"
echo "  • API: http://localhost:8000"
echo ""
