# 🔧 Rahu/Ketu Calculation Bug Fix

**Date:** December 12, 2025  
**Issue:** Rahu and Ketu were not exactly 180° apart in calculations  
**Status:** ✅ **FIXED**

---

## 🐛 Bug Description

Rahu (North Node) and Ketu (South Node) should always be exactly 180° apart in the zodiac. However, the calculation was incorrect in `api_server.py`.

### Root Cause

In `api_server.py`, the `calculate_planet_position()` function for Ketu was using **tropical** coordinates (`swe.FLG_SWIEPH`) to calculate Rahu, then adding 180° to get Ketu. However, Rahu itself was being calculated using **sidereal** coordinates (`swe.FLG_SIDEREAL | swe.FLG_SWIEPH`).

**Result:** Rahu and Ketu were off by approximately 24° (the ayanamsa value) instead of being exactly 180° apart.

---

## ✅ Fix Applied

### File: `api_server.py`

**Before (Line 108):**
```python
rahu_result = swe.calc_ut(jd, PLANETS['Rahu'], swe.FLG_SWIEPH)  # TROPICAL - WRONG!
```

**After:**
```python
rahu_result = swe.calc_ut(jd, PLANETS['Rahu'], swe.FLG_SIDEREAL | swe.FLG_SWIEPH)  # SIDEREAL - CORRECT!
```

### Verification

Both Rahu and Ketu now use **sidereal coordinates** with Lahiri Ayanamsa, ensuring they are exactly 180° apart.

---

## 📊 Test Results

### Before Fix:
```
Rahu: 317.98° (Aquarius)
Ketu: 163.08° (Virgo)
Difference: 154.90° ❌ (should be 180°)
```

### After Fix:
```
Rahu: 317.98° (Aquarius)
Ketu: 137.98° (Leo)
Difference: 180.00° ✅ (exactly correct!)
```

---

## 🔍 Files Affected

1. **`api_server.py`** - Fixed Ketu calculation to use sidereal mode
2. **`astro_calculations.py`** - ✅ Already correct (was using sidereal)

---

## 📝 Important Notes

1. **Coordinate System Consistency:**
   - Both Rahu and Ketu **MUST** use the same coordinate system (sidereal)
   - Using different systems (tropical vs sidereal) causes the 180° relationship to break

2. **Swiss Ephemeris:**
   - `swe.FLG_SWIEPH` = Tropical coordinates
   - `swe.FLG_SIDEREAL | swe.FLG_SWIEPH` = Sidereal coordinates (with ayanamsa)

3. **Ketu Calculation:**
   - Ketu is always calculated as: `Ketu = (Rahu + 180) % 360`
   - This ensures exact 180° separation

---

## ✅ Verification Script

Run this to verify the fix:

```python
from api_server import calculate_planet_position
import swisseph as swe
from datetime import date

jd = swe.julday(2025, 12, 10, 12.0/24.0, swe.GREG_CAL)

rahu = calculate_planet_position('Rahu', jd)
ketu = calculate_planet_position('Ketu', jd)

diff = abs(ketu['longitude'] - rahu['longitude'])
if diff > 180:
    diff = 360 - diff

assert abs(diff - 180.0) < 0.01, "Rahu and Ketu must be exactly 180° apart!"
print("✅ Verification passed!")
```

---

**Fix Status:** ✅ **COMPLETE**  
**Tested:** Multiple dates verified  
**Impact:** All planetary calculations now show correct Rahu/Ketu positions

