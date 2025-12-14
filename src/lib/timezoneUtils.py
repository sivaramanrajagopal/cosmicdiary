"""
Timezone utilities for normalizing timezone strings
Converts offset formats (UTC+5:30) to IANA timezone names (Asia/Kolkata)
"""

# Common timezone offset to IANA mapping
TIMEZONE_OFFSET_MAP = {
    'UTC+5:30': 'Asia/Kolkata',  # India Standard Time
    'IST': 'Asia/Kolkata',  # Indian Standard Time
    'UTC+5:30': 'Asia/Kolkata',
    '+05:30': 'Asia/Kolkata',
    'UTC+1': 'Europe/London',  # Approximate
    'UTC+2': 'Europe/Berlin',
    'UTC+5': 'Asia/Karachi',
    'UTC+6': 'Asia/Dhaka',
    'UTC+8': 'Asia/Shanghai',
    'UTC+9': 'Asia/Tokyo',
    'UTC-5': 'America/New_York',
    'UTC-8': 'America/Los_Angeles',
}

def normalize_timezone(timezone_str: str, latitude: float = None, longitude: float = None) -> str:
    """
    Normalize timezone string to IANA format.
    
    Args:
        timezone_str: Timezone string (can be offset like "UTC+5:30" or IANA like "Asia/Kolkata")
        latitude: Optional latitude for timezone detection
        longitude: Optional longitude for timezone detection
    
    Returns:
        IANA timezone string (e.g., "Asia/Kolkata")
    """
    if not timezone_str:
        # Try to detect from coordinates if available
        if latitude is not None and longitude is not None:
            try:
                from timezonefinder import TimezoneFinder
                tf = TimezoneFinder()
                detected = tf.timezone_at(lat=latitude, lng=longitude)
                if detected:
                    return detected
            except Exception:
                pass
        return 'UTC'
    
    timezone_str = timezone_str.strip()
    
    # If already in IANA format, return as-is (after basic validation)
    if '/' in timezone_str and not timezone_str.startswith('UTC'):
        # Looks like IANA format (e.g., "Asia/Kolkata")
        return timezone_str
    
    # Try offset mapping
    if timezone_str in TIMEZONE_OFFSET_MAP:
        return TIMEZONE_OFFSET_MAP[timezone_str]
    
    # Try case-insensitive match
    timezone_upper = timezone_str.upper()
    for offset, iana_tz in TIMEZONE_OFFSET_MAP.items():
        if offset.upper() == timezone_upper:
            return iana_tz
    
    # Try to parse UTC offset format (UTC+5:30, UTC-5:30, +05:30, etc.)
    import re
    offset_pattern = r'UTC([+-])(\d{1,2}):?(\d{2})?'
    match = re.match(offset_pattern, timezone_str, re.IGNORECASE)
    if match:
        sign = match.group(1)
        hours = int(match.group(2))
        minutes = int(match.group(3) or '0')
        
        # Common offsets for India
        if sign == '+' and hours == 5 and minutes == 30:
            return 'Asia/Kolkata'
        
        # Could add more mappings here
        # For now, default to UTC for unknown offsets
        return 'UTC'
    
    # If still not recognized, try timezonefinder if coordinates available
    if latitude is not None and longitude is not None:
        try:
            from timezonefinder import TimezoneFinder
            tf = TimezoneFinder()
            detected = tf.timezone_at(lat=latitude, lng=longitude)
            if detected:
                return detected
        except Exception:
            pass
    
    # Default fallback
    return 'UTC'

