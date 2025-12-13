"""
Astrologically-Relevant Event Detection Prompts
Designed for research-grade event collection with planetary correlation
"""

from datetime import datetime, timedelta
from typing import Dict

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
    
    Since job runs every 2 hours, look back 8 hours to get more comprehensive coverage,
    including top Indian news as fallback.
    """
    now = datetime.utcnow()
    lookback_hours = 8  # Extended window for better coverage, including Indian news
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

PRIORITY 1: SIGNIFICANT GLOBAL/INDIAN EVENTS
Focus on these high-impact areas:
1. Natural Disasters: Major earthquakes, floods, cyclones, droughts (affecting 1000+ OR infrastructure damage)
2. Economic: Stock market movements >2%, GDP/inflation news, banking crises, currency events
3. Political: Elections, major policies, government crises (state/national level)
4. Health: Epidemics, disease outbreaks (100+ affected), major medical breakthroughs
5. Technology: Major launches, AI breakthroughs, space missions, cyber attacks
6. Business: Fortune 500 mergers/bankruptcies, IPOs >$1B, mass layoffs >500 people
7. Wars & Conflicts: International/state-level conflicts, attacks, military actions
8. Employment: Major strikes, labor laws, unemployment data
9. Women & Children: Major policy changes, large-scale welfare impacts
10. Entertainment: Deaths of cultural icons, world championships, major awards

PRIORITY 2: TOP 10 INDIAN NEWS (FALLBACK)
If fewer than 5 significant events found, also include:
- Top 10 news stories from India (any category: politics, economy, society, sports, entertainment)
- Include state-level and national-level Indian news
- News from major Indian states: Tamil Nadu, Karnataka, Maharashtra, Delhi, Gujarat, UP, West Bengal, Bihar, Rajasthan, Telangana, Andhra Pradesh, Kerala, etc.
- Can include business news, policy announcements, political developments, social issues, etc.

GEOGRAPHIC PRIORITY:
- India: All major states (state-level+ events)
- Global: G20 countries, international significance

EXCLUSIONS (only for Priority 1, relaxed for Priority 2):
- Local/district news (unless catastrophic or part of top 10 Indian news)
- Celebrity gossip (unless death/major cultural impact)
- Opinion pieces
- Routine announcements (unless part of top Indian news)

Return maximum 15 events in JSON format. For each event:
- Include all required fields (title, date, description, category, location, impact_level)
- For astrological_relevance: Try to map houses and planets based on event nature, even if not explicitly significant
- If exact time unknown, use "estimated" or approximate based on when news broke

Today's date: {current_date}
Analysis window: Past 8 hours (includes top Indian news fallback)
"""
    
    return prompt

# ============================================================================
# EXAMPLE RESPONSE VALIDATOR
# ============================================================================

def validate_event_response(event, lenient=False):
    """
    Validates that an event from OpenAI meets quality standards.
    
    Args:
        event: Event dictionary to validate
        lenient: If True, allows missing astrological mapping (will be auto-mapped later)
    
    Returns: (is_valid: bool, reason: str)
    """
    required_fields = ['title', 'date', 'category', 'description', 'impact_level']
    
    # Check required fields
    for field in required_fields:
        if field not in event:
            return False, f"Missing required field: {field}"
    
    # Check title length
    if len(event['title']) > 150:  # Increased from 100
        return False, "Title too long (>150 chars)"
    
    # Check description length (more lenient for news)
    desc_len = len(event['description'])
    if desc_len < 50 or desc_len > 800:  # More lenient range
        return False, f"Description length {desc_len} outside range 50-800"
    
    # Normalize category BEFORE validation
    # Map OpenAI category variations to our standard categories
    category_mapping = {
        'natural disaster': 'Natural Disasters',
        'natural disasters': 'Natural Disasters',
        'economic event': 'Economic Events',
        'economic events': 'Economic Events',
        'economic': 'Economic Events',
        'political event': 'Political Events',
        'political events': 'Political Events',
        'political': 'Political Events',
        'health crisis': 'Health & Medical',
        'health & medical': 'Health & Medical',
        'health': 'Health & Medical',
        'medical': 'Health & Medical',
        'technology': 'Technology & Innovation',
        'tech': 'Technology & Innovation',
        'technology & innovation': 'Technology & Innovation',
        'business': 'Business & Commerce',
        'commerce': 'Business & Commerce',
        'business & commerce': 'Business & Commerce',
        'war': 'Wars & Conflicts',
        'conflict': 'Wars & Conflicts',
        'wars & conflicts': 'Wars & Conflicts',
        'wars': 'Wars & Conflicts',
        'employment': 'Employment & Labor',
        'labor': 'Employment & Labor',
        'employment & labor': 'Employment & Labor',
        'women & children': 'Women & Children',
        'entertainment': 'Entertainment & Sports',
        'sports': 'Entertainment & Sports',
        'entertainment & sports': 'Entertainment & Sports',
    }
    
    valid_categories = list(EVENT_CATEGORIES.keys()) + ['Social', 'Cultural', 'Sports', 'Environment', 'Education']
    
    # Normalize category
    event_category = event.get('category', '')
    if not event_category:
        return False, "Missing category"
    
    event_category_lower = event_category.lower().strip()
    
    # Try to map to valid category
    if event_category_lower in category_mapping:
        event['category'] = category_mapping[event_category_lower]
    elif event_category not in valid_categories:
        # Check case-insensitive match
        valid_lower = {c.lower(): c for c in valid_categories}
        if event_category_lower in valid_lower:
            event['category'] = valid_lower[event_category_lower]
        else:
            # Allow any category if lenient, otherwise reject
            if not lenient:
                return False, f"Invalid category: {event_category}"
    
    # Check impact level
    if event['impact_level'] not in ['low', 'medium', 'high', 'critical']:
        return False, f"Invalid impact_level: {event['impact_level']}"
    
    # Check astrological relevance (lenient mode allows missing)
    astro = event.get('astrological_relevance', {})
    if not lenient:
        if not astro.get('primary_houses') or not astro.get('primary_planets'):
            return False, "Missing astrological house/planet mapping"
    
    # Validate houses are 1-12 (if provided)
    if astro.get('primary_houses'):
        houses = astro.get('primary_houses', [])
        if any(h < 1 or h > 12 for h in houses):
            return False, "Invalid house number (must be 1-12)"
    
    # Validate planets (if provided)
    if astro.get('primary_planets'):
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


# ============================================================================
# AUTO-MAPPING FUNCTION FOR EVENTS WITHOUT ASTROLOGICAL MAPPING
# ============================================================================

def auto_map_event_to_astrology(event: Dict) -> Dict:
    """
    Automatically maps an event to astrological houses and planets based on:
    - Category
    - Description keywords
    - Location (India vs global)
    - Impact level
    
    This is used for events that don't have astrological mapping from OpenAI.
    
    Returns: Updated event dictionary with astrological_relevance added/mapped
    """
    category = event.get('category', '').lower()
    description = event.get('description', '').lower()
    title = event.get('title', '').lower()
    location = event.get('location', '').lower()
    impact_level = event.get('impact_level', 'medium')
    
    # Combine all text for keyword matching
    all_text = f"{title} {description}".lower()
    
    # Default mappings
    primary_houses = []
    primary_planets = []
    keywords = []
    reasoning = []
    
    # Category-based mapping
    if 'natural disaster' in category or 'disaster' in category:
        primary_houses.extend([4, 8])  # Land, Sudden events
        primary_planets.extend(['Mars', 'Saturn', 'Rahu'])
        keywords.extend(['disaster', 'calamity', 'natural'])
        reasoning.append("Natural disasters affect land (4th house) and are sudden events (8th house)")
    
    if 'economic' in category or 'finance' in category or 'banking' in category:
        primary_houses.extend([2, 5, 11])  # Wealth, Speculation, Gains
        primary_planets.extend(['Jupiter', 'Mercury', 'Venus'])
        keywords.extend(['economy', 'finance', 'money', 'bank'])
        reasoning.append("Economic events relate to wealth (2nd), speculation (5th), and gains (11th)")
    
    if 'political' in category or 'election' in category or 'government' in category:
        primary_houses.extend([9, 10])  # Law, Government
        primary_planets.extend(['Sun', 'Jupiter', 'Saturn'])
        keywords.extend(['politics', 'government', 'election', 'policy'])
        reasoning.append("Political events relate to law (9th) and government (10th)")
    
    if 'health' in category or 'medical' in category or 'disease' in category:
        primary_houses.extend([6, 8, 12])  # Disease, Calamities, Hospitals
        primary_planets.extend(['Saturn', 'Rahu', 'Mars'])
        keywords.extend(['health', 'medical', 'disease', 'epidemic'])
        reasoning.append("Health events relate to disease (6th), sudden events (8th), and hospitals (12th)")
    
    if 'technology' in category or 'tech' in category or 'innovation' in category:
        primary_houses.extend([3, 5, 11])  # Communication, Intelligence, Mass adoption
        primary_planets.extend(['Mercury', 'Rahu'])
        keywords.extend(['technology', 'innovation', 'digital'])
        reasoning.append("Technology relates to communication (3rd), intelligence (5th), and mass adoption (11th)")
    
    if 'business' in category or 'commerce' in category or 'trade' in category:
        primary_houses.extend([2, 7, 10, 11])  # Wealth, Trade, Career, Gains
        primary_planets.extend(['Mercury', 'Venus', 'Jupiter'])
        keywords.extend(['business', 'commerce', 'trade'])
        reasoning.append("Business relates to wealth (2nd), trade (7th), career (10th), and gains (11th)")
    
    if 'war' in category or 'conflict' in category or 'military' in category:
        primary_houses.extend([6, 7, 8])  # Enemies, Open warfare, Death
        primary_planets.extend(['Mars', 'Sun', 'Saturn'])
        keywords.extend(['war', 'conflict', 'military'])
        reasoning.append("Wars relate to enemies (6th), open warfare (7th), and death (8th)")
    
    if 'employment' in category or 'labor' in category or 'job' in category:
        primary_houses.extend([6, 10])  # Service, Career
        primary_planets.extend(['Saturn', 'Mercury'])
        keywords.extend(['employment', 'labor', 'job'])
        reasoning.append("Employment relates to service (6th) and career (10th)")
    
    if 'women' in category or 'children' in category or 'education' in category:
        primary_houses.extend([5, 7])  # Children, Partnerships
        primary_planets.extend(['Moon', 'Venus', 'Jupiter'])
        keywords.extend(['women', 'children', 'education'])
        reasoning.append("Women/Children events relate to children (5th) and partnerships (7th)")
    
    if 'entertainment' in category or 'sports' in category:
        primary_houses.extend([5, 3])  # Entertainment, Media
        primary_planets.extend(['Venus', 'Mercury', 'Moon'])
        keywords.extend(['entertainment', 'sports'])
        reasoning.append("Entertainment relates to entertainment (5th) and media (3rd)")
    
    # Keyword-based additional mapping
    if 'flood' in all_text or 'cyclone' in all_text or 'rain' in all_text:
        primary_houses.append(4)  # Water resources
        primary_planets.append('Moon')
        keywords.append('water')
        reasoning.append("Water-related events map to Moon (water) and 4th house (water resources)")
    
    if 'earthquake' in all_text or 'volcano' in all_text:
        primary_houses.append(4)  # Land
        primary_planets.append('Mars')
        keywords.append('earth')
        reasoning.append("Earth-related events map to Mars (fire/earth) and 4th house (land)")
    
    if 'india' in location or 'indian' in all_text:
        keywords.append('india')
        reasoning.append("Indian event - may have additional regional significance")
    
    # Remove duplicates while preserving order
    primary_houses = list(dict.fromkeys(primary_houses))[:4]  # Max 4 houses
    primary_planets = list(dict.fromkeys(primary_planets))[:4]  # Max 4 planets
    
    # If no mapping found, use general defaults
    if not primary_houses:
        primary_houses = [10]  # Default to 10th house (general worldly matters)
        primary_planets = ['Jupiter']  # Default to Jupiter (general significator)
        reasoning.append("Default mapping to 10th house (general events) and Jupiter (significator)")
    
    # Ensure we have at least one house and planet
    if not primary_houses:
        primary_houses = [10]
    if not primary_planets:
        primary_planets = ['Jupiter']
    
    return {
        'primary_houses': primary_houses,
        'primary_planets': primary_planets,
        'keywords': list(set(keywords))[:10],  # Unique keywords, max 10
        'reasoning': ' | '.join(reasoning) if reasoning else 'Auto-mapped based on category and keywords'
    }

