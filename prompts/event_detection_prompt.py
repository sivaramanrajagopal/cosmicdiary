"""
Astrologically-Relevant Event Detection Prompts
Designed for research-grade event collection with planetary correlation
"""

from datetime import datetime, timedelta

# ============================================================================
# ASTROLOGICAL HOUSE & PLANET SIGNIFICATIONS REFERENCE
# ============================================================================

HOUSE_SIGNIFICATIONS = {
    1: ["Self", "Identity", "Leadership", "Personality", "Health", "Physical body"],
    2: ["Wealth", "Money", "Family", "Speech", "Food", "Resources", "Possessions", "Banking"],
    3: ["Communication", "Media", "Courage", "Siblings", "Short travel", "Technology", "Social media"],
    4: ["Property", "Land", "Home", "Mother", "Agriculture", "Real estate", "Vehicles", "Emotions", "Water resources"],
    5: ["Children", "Education", "Entertainment", "Speculation", "Stock market", "Creativity", "Intelligence", "Sports"],
    6: ["Health", "Disease", "Enemies", "Litigation", "Service", "Employment", "Debts", "Accidents"],
    7: ["Partnerships", "Marriage", "Trade", "Business", "Foreign relations", "Public", "Contracts"],
    8: ["Death", "Transformation", "Sudden events", "Occult", "Hidden wealth", "Insurance", "Natural disasters", "Calamities"],
    9: ["Religion", "Philosophy", "Higher education", "Long distance travel", "Fortune", "Gurus", "Law", "Courts"],
    10: ["Career", "Government", "Authority", "Reputation", "Politics", "Status", "Power", "Father"],
    11: ["Gains", "Income", "Friends", "Achievements", "Social causes", "Technology adoption", "Mass movements"],
    12: ["Losses", "Expenses", "Foreign lands", "Isolation", "Spirituality", "Hospitals", "Prisons", "Expenditure"]
}

PLANET_SIGNIFICATIONS = {
    "Sun": ["Government", "Authority", "Leaders", "Politics", "Power", "Father figures", "Kings", "Fame"],
    "Moon": ["Public", "Masses", "Emotions", "Water", "Women", "Mother", "Mind", "Agriculture"],
    "Mars": ["War", "Conflicts", "Military", "Police", "Surgery", "Sports", "Energy", "Accidents", "Fire"],
    "Mercury": ["Business", "Trade", "Communication", "Media", "Education", "Commerce", "Technology"],
    "Jupiter": ["Finance", "Banking", "Law", "Religion", "Education", "Children", "Wisdom", "Prosperity"],
    "Venus": ["Arts", "Entertainment", "Women", "Marriage", "Luxury", "Beauty", "Relationships", "Vehicles"],
    "Saturn": ["Delays", "Losses", "Labor", "Working class", "Justice", "Karma", "Elderly", "Diseases"],
    "Rahu": ["Technology", "Innovation", "Foreign", "Unexpected events", "Epidemics", "Confusion", "Mass movements"],
    "Ketu": ["Spirituality", "Liberation", "Sudden events", "Accidents", "Separation", "Technology failures"]
}

# ============================================================================
# EVENT CATEGORIES WITH ASTROLOGICAL MAPPING
# ============================================================================

EVENT_CATEGORIES = {
    "Natural Disasters": {
        "houses": [4, 8, 12],  # Land, Sudden events, Losses
        "planets": ["Mars", "Saturn", "Rahu", "Ketu"],
        "keywords": ["earthquake", "flood", "tsunami", "hurricane", "cyclone", "drought", "landslide", "wildfire"],
        "impact_threshold": "affects 1000+ people OR major infrastructure damage"
    },
    
    "Economic Events": {
        "houses": [2, 5, 11],  # Wealth, Speculation, Gains
        "planets": ["Jupiter", "Mercury", "Venus"],
        "keywords": ["stock market", "GDP", "inflation", "recession", "economic crisis", "currency", "trade policy", "banking"],
        "impact_threshold": "national/international significance OR market movement >2%"
    },
    
    "Political Events": {
        "houses": [9, 10],  # Law, Government
        "planets": ["Sun", "Jupiter", "Saturn"],
        "keywords": ["election", "government policy", "political crisis", "law passed", "summit", "diplomatic"],
        "impact_threshold": "state/national level only, no local politics"
    },
    
    "Health & Medical": {
        "houses": [6, 8, 12],  # Disease, Calamities, Hospitals
        "planets": ["Saturn", "Rahu", "Mars"],
        "keywords": ["epidemic", "disease outbreak", "medical breakthrough", "health crisis", "pandemic"],
        "impact_threshold": "affects 100+ people OR major medical discovery"
    },
    
    "Technology & Innovation": {
        "houses": [3, 5, 11],  # Communication, Intelligence, Mass adoption
        "planets": ["Mercury", "Rahu"],
        "keywords": ["AI", "breakthrough", "launch", "technology", "innovation", "space", "cyber attack"],
        "impact_threshold": "industry-changing OR affects millions"
    },
    
    "Women & Children": {
        "houses": [5, 7],  # Children, Partnerships
        "planets": ["Moon", "Venus", "Jupiter"],
        "keywords": ["women rights", "child welfare", "education reform", "marriage law", "maternity"],
        "impact_threshold": "policy change OR affects 10,000+ women/children"
    },
    
    "Business & Commerce": {
        "houses": [2, 7, 10, 11],  # Wealth, Trade, Career, Gains
        "planets": ["Mercury", "Venus", "Jupiter"],
        "keywords": ["merger", "acquisition", "bankruptcy", "IPO", "major deal", "company closure"],
        "impact_threshold": "Fortune 500 OR valuation >$1B OR affects 1000+ jobs"
    },
    
    "Employment & Labor": {
        "houses": [6, 10],  # Service, Career
        "planets": ["Saturn", "Mercury"],
        "keywords": ["layoffs", "strike", "labor law", "unemployment", "job creation", "wage"],
        "impact_threshold": "affects 500+ workers OR major policy change"
    },
    
    "Wars & Conflicts": {
        "houses": [6, 7, 8],  # Enemies, Open warfare, Death
        "planets": ["Mars", "Sun", "Saturn"],
        "keywords": ["war", "conflict", "attack", "military", "ceasefire", "invasion"],
        "impact_threshold": "international OR state-level conflict"
    },
    
    "Entertainment & Sports": {
        "houses": [5, 3],  # Entertainment, Media
        "planets": ["Venus", "Mercury", "Moon"],
        "keywords": ["major award", "box office record", "sports championship", "celebrity death"],
        "impact_threshold": "national/international fame level only"
    }
}

# ============================================================================
# GEOGRAPHIC FOCUS
# ============================================================================

GEOGRAPHIC_PRIORITIES = {
    "India": {
        "states": ["Tamil Nadu", "Karnataka", "Maharashtra", "Delhi", "Gujarat", "Uttar Pradesh"],
        "focus": "state-level or higher events, not district/city unless major impact"
    },
    "Global": {
        "focus": "G20 countries, major economies, international significance"
    }
}

# ============================================================================
# TIME WINDOWS FOR EVENT DETECTION
# ============================================================================

def get_time_window():
    """
    Returns time window for event search based on run schedule.
    
    Since job runs every 2 hours, look back 3 hours to ensure overlap.
    """
    now = datetime.utcnow()
    lookback_hours = 3  # Slight overlap to avoid missing events
    start_time = now - timedelta(hours=lookback_hours)
    
    return {
        "start": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end": now.strftime("%Y-%m-%d %H:%M:%S"),
        "timezone": "UTC"
    }

# ============================================================================
# MAIN OPENAI SYSTEM PROMPT
# ============================================================================

SYSTEM_PROMPT = """You are an expert event analyst for astrological research, specializing in identifying significant world events that correlate with Vedic planetary positions and house significations.

YOUR ROLE:
Scan news from the past 3 hours and identify ONLY high-impact, research-worthy events that match specific astrological categories and significance thresholds.

CRITICAL FILTERING RULES:

1. SIGNIFICANCE THRESHOLD - Only include events that are:
   ✓ State/National/International level
   ✓ Affect 100+ people OR have major policy/economic impact
   ✓ Newsworthy for 48+ hours (not just breaking news cycle)
   ✗ Local/district level events (unless catastrophic)
   ✗ Celebrity gossip (unless death/major cultural impact)
   ✗ Minor business news (unless Fortune 500 or $1B+ valuation)
   ✗ Routine political announcements (only major policy/crises)

2. ASTROLOGICAL RELEVANCE - Events must clearly relate to:
   - House significations (1-12 houses of Vedic astrology)
   - Planetary significations (9 planets: Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu)
   - Examples:
     * Earthquake = House 4 (land), House 8 (sudden), Mars/Saturn/Rahu
     * Stock crash = House 2 (wealth), House 5 (speculation), Jupiter/Mercury
     * Government policy = House 10 (authority), Sun/Jupiter
     * Disease outbreak = House 6 (disease), Saturn/Rahu

3. GEOGRAPHIC PRIORITIES:
   - India: Focus on Tamil Nadu, Karnataka, and other major states (state-level+)
   - Global: G20 countries, major economies, international events
   - Skip: Small town/district news unless major disaster

4. CATEGORIES TO SCAN (in priority order):
   HIGH PRIORITY:
   - Natural Disasters (earthquake, flood, cyclone, drought)
   - Economic Events (stock market, GDP, inflation, banking crisis)
   - Political Events (elections, major policies, government crisis)
   - Health Crises (epidemics, major outbreaks, medical breakthroughs)
   
   MEDIUM PRIORITY:
   - Technology Breakthroughs (AI, space, major launches)
   - Wars & Conflicts (international/state-level)
   - Business (Fortune 500 mergers, major bankruptcies)
   - Employment (mass layoffs 500+, major strikes)
   
   LOW PRIORITY (only if extraordinary):
   - Women & Children (major policy changes, large-scale impact)
   - Entertainment & Sports (deaths of icons, world championships)

5. TIME ACCURACY:
   - Prefer events with specific time mentioned (for accurate chart calculation)
   - If no exact time: Note approximate time based on:
     * "morning" = ~08:00
     * "afternoon" = ~14:00
     * "evening" = ~18:00
     * "night" = ~22:00
   - Include timezone if mentioned

6. EXCLUSIONS - Do NOT include:
   ✗ Opinion pieces, editorials, analysis (we want factual events)
   ✗ Rumors, unconfirmed reports
   ✗ Celebrity news (unless death/major cultural impact)
   ✗ Sports results (unless championships/records)
   ✗ Minor crimes (unless mass casualty or state-level impact)
   ✗ Routine government functions
   ✗ Small business news
   ✗ Local protests (unless state/national scale)

RESEARCH PERSPECTIVE:
We're studying planetary transits and their correlation with world events. We need:
- Events that represent archetypal manifestations of planetary/house energies
- Clear cause-effect that can be studied statistically
- Events measurable in impact (deaths, money, people affected)
- Events with precise timing for accurate chart calculation

OUTPUT FORMAT:
Return a JSON array of events (maximum 15 events per run to maintain quality).

For each event:
{
  "title": "Concise, factual title (max 100 chars)",
  "date": "YYYY-MM-DD",
  "time": "HH:MM:SS or 'estimated' with approximate time",
  "timezone": "timezone name or 'UTC'",
  "location": "City, State/Province, Country",
  "category": "Exact category from: Natural Disaster, Economic Event, Political Event, etc.",
  "description": "Factual summary (150-300 words) including: what happened, when, where, who affected, impact scale, current status",
  "impact_level": "low/medium/high/critical",
  "impact_metrics": {
    "deaths": number or null,
    "injured": number or null,
    "affected": number or null,
    "financial_impact_usd": number or null,
    "geographic_scope": "local/state/national/international"
  },
  "astrological_relevance": {
    "primary_houses": [house numbers 1-12],
    "primary_planets": ["planet names"],
    "keywords": ["keyword1", "keyword2"],
    "reasoning": "Brief explanation why this event is astrologically significant"
  },
  "sources": ["source1 URL", "source2 URL"],
  "confidence": "high/medium/low (in event accuracy and timing)"
}

IMPACT LEVEL GUIDELINES:
- Critical: Deaths >100 OR economic impact >$1B OR affects >1M people OR constitutional/international crisis
- High: Deaths 10-100 OR economic impact $100M-$1B OR affects 100K-1M people OR state-level crisis
- Medium: Deaths 1-10 OR economic impact $10M-$100M OR affects 10K-100K people OR major city impact
- Low: Significant but contained impact

QUALITY OVER QUANTITY:
- Better to return 5 high-quality, research-worthy events than 20 minor news items
- Each event should be something a researcher would want to study
- Each event should have clear astrological correlation potential

Remember: You are filtering for RESEARCH SIGNIFICANCE, not news coverage. Ask yourself:
"Would an astrological researcher studying planetary transits want this event in their database?"
"""

# ============================================================================
# USER PROMPT GENERATOR
# ============================================================================

def generate_user_prompt(time_window=None):
    """
    Generates the user prompt for OpenAI based on current time window.
    
    Args:
        time_window: Optional dict with 'start' and 'end' datetime strings
                    If None, uses get_time_window()
    
    Returns:
        String containing the user prompt
    """
    if time_window is None:
        time_window = get_time_window()
    
    current_date = datetime.utcnow().strftime("%Y-%m-%d")
    
    prompt = f"""Scan news sources for significant world events from {time_window['start']} to {time_window['end']} UTC.

FOCUS AREAS:
1. Natural Disasters: Major earthquakes, floods, cyclones, droughts (affecting 1000+ OR infrastructure damage)
2. Economic: Stock market movements >2%, GDP/inflation news, banking crises, currency events
3. Political: Elections, major policies, government crises (state/national level only)
4. Health: Epidemics, disease outbreaks (100+ affected), major medical breakthroughs
5. Technology: Major launches, AI breakthroughs, space missions, cyber attacks
6. Business: Fortune 500 mergers/bankruptcies, IPOs >$1B, mass layoffs >500 people
7. Wars & Conflicts: International/state-level conflicts, attacks, military actions
8. Employment: Major strikes, labor laws, unemployment data
9. Women & Children: Major policy changes, large-scale welfare impacts
10. Entertainment: Deaths of cultural icons, world championships, major awards

GEOGRAPHIC PRIORITY:
- India: Tamil Nadu, Karnataka, Maharashtra, Delhi, Gujarat, UP (state-level+ events)
- Global: G20 countries, international significance

EXCLUSIONS:
- Local/district news (unless catastrophic)
- Celebrity gossip
- Opinion pieces
- Routine announcements
- Minor crimes
- Small business news

Return maximum 15 events in JSON format with complete astrological mapping.

Today's date: {current_date}
Analysis window: Past 3 hours (to align with 2-hour job schedule)
"""
    
    return prompt

# ============================================================================
# EXAMPLE RESPONSE VALIDATOR
# ============================================================================

def validate_event_response(event):
    """
    Validates that an event from OpenAI meets quality standards.
    
    Returns: (is_valid: bool, reason: str)
    """
    required_fields = [
        'title', 'date', 'category', 'description', 
        'impact_level', 'astrological_relevance'
    ]
    
    # Check required fields
    for field in required_fields:
        if field not in event:
            return False, f"Missing required field: {field}"
    
    # Check title length
    if len(event['title']) > 100:
        return False, "Title too long (>100 chars)"
    
    # Check description length
    desc_len = len(event['description'])
    if desc_len < 150 or desc_len > 500:
        return False, f"Description length {desc_len} outside range 150-500"
    
    # Check category validity
    valid_categories = list(EVENT_CATEGORIES.keys())
    if event['category'] not in valid_categories:
        return False, f"Invalid category: {event['category']}"
    
    # Check impact level
    if event['impact_level'] not in ['low', 'medium', 'high', 'critical']:
        return False, f"Invalid impact_level: {event['impact_level']}"
    
    # Check astrological relevance
    astro = event.get('astrological_relevance', {})
    if not astro.get('primary_houses') or not astro.get('primary_planets'):
        return False, "Missing astrological house/planet mapping"
    
    # Validate houses are 1-12
    houses = astro.get('primary_houses', [])
    if any(h < 1 or h > 12 for h in houses):
        return False, "Invalid house number (must be 1-12)"
    
    # Validate planets
    valid_planets = list(PLANET_SIGNIFICATIONS.keys())
    planets = astro.get('primary_planets', [])
    if any(p not in valid_planets for p in planets):
        return False, f"Invalid planet name in: {planets}"
    
    return True, "Valid"

# ============================================================================
# SCORING SYSTEM FOR EVENT PRIORITIZATION
# ============================================================================

def calculate_research_score(event):
    """
    Calculate research worthiness score (0-100) for an event.
    
    Higher scores = more valuable for astrological research
    """
    score = 0
    
    # Impact level scoring (0-40 points)
    impact_scores = {
        'critical': 40,
        'high': 30,
        'medium': 20,
        'low': 10
    }
    score += impact_scores.get(event.get('impact_level', 'low'), 0)
    
    # Time accuracy (0-20 points)
    if event.get('time') and event['time'] != 'estimated':
        score += 20  # Exact time known
    elif 'morning' in event.get('description', '').lower() or \
         'afternoon' in event.get('description', '').lower():
        score += 10  # Approximate time available
    else:
        score += 5   # Only date known
    
    # Location specificity (0-15 points)
    location = event.get('location', '')
    if ',' in location and len(location.split(',')) >= 3:  # City, State, Country
        score += 15
    elif ',' in location:  # At least State, Country
        score += 10
    else:
        score += 5
    
    # Astrological clarity (0-15 points)
    astro = event.get('astrological_relevance', {})
    houses = astro.get('primary_houses', [])
    planets = astro.get('primary_planets', [])
    if len(houses) >= 2 and len(planets) >= 2:
        score += 15  # Clear multi-planet/house correlation
    elif houses and planets:
        score += 10  # Basic correlation
    else:
        score += 5
    
    # Measurable impact (0-10 points)
    metrics = event.get('impact_metrics', {})
    measurable_fields = ['deaths', 'injured', 'affected', 'financial_impact_usd']
    measurable_count = sum(1 for field in measurable_fields if metrics.get(field))
    score += min(measurable_count * 3, 10)
    
    return min(score, 100)  # Cap at 100

