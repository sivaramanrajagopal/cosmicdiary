# Real-Time News API Integration Guide

**Purpose**: Replace or supplement OpenAI with actual real-time news sources for accurate event collection

---

## 🎯 Why You Need a News API

**Current Limitation**: OpenAI's `gpt-4o-mini` does **NOT** have access to real-time news. It only knows events up to its training cutoff (January 2025).

**What OpenAI Does**: It generates plausible events based on patterns it learned during training, not actual current news.

**Solution**: Integrate a real-time news API to fetch actual current events.

---

## 📰 Recommended News APIs

### 1. **NewsAPI.org** (Best for Getting Started)

**Pros**:
- Free tier: 100 requests/day
- Simple REST API
- Covers 150+ sources globally
- Good for India news (Times of India, Hindustan Times, etc.)

**Cons**:
- Free tier limited to 100 requests/day
- Paid tier: $449/month (expensive)

**Setup**:
```bash
# Get API key from https://newsapi.org/register
# Add to .env.local:
NEWSAPI_KEY=your_api_key_here
```

**Example Code**:
```python
import requests
from datetime import datetime, timedelta

def fetch_news_from_newsapi(hours_back=2):
    """Fetch news from NewsAPI"""
    api_key = os.getenv('NEWSAPI_KEY')
    url = 'https://newsapi.org/v2/everything'

    # Time window
    from_time = (datetime.utcnow() - timedelta(hours=hours_back)).isoformat()

    params = {
        'apiKey': api_key,
        'from': from_time,
        'language': 'en',
        'sortBy': 'publishedAt',
        'pageSize': 20,
        'q': '(India OR earthquake OR economy OR technology OR politics) -sports -entertainment'
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data['status'] == 'ok':
        return data['articles']
    return []

# Then process articles into your event format
def convert_newsapi_to_event(article):
    return {
        'title': article['title'],
        'description': article['description'] or article['content'][:300],
        'date': article['publishedAt'][:10],  # YYYY-MM-DD
        'time': article['publishedAt'][11:19],  # HH:MM:SS
        'timezone': 'UTC',
        'location': 'Unknown',  # Would need geocoding
        'category': classify_article(article),  # Your logic
        'impact_level': 'medium',
        'sources': [article['url']],
        'tags': []
    }
```

---

### 2. **Google News API** (via SerpAPI)

**Pros**:
- Real-time Google News results
- Free tier: 100 searches/month
- Great coverage, especially for India

**Cons**:
- Requires additional parsing
- Paid tier: $50-$250/month

**Setup**:
```bash
# Get API key from https://serpapi.com/
pip install google-search-results
```

**Example Code**:
```python
from serpapi import GoogleSearch

def fetch_google_news(query="India news", hours=2):
    params = {
        'api_key': os.getenv('SERPAPI_KEY'),
        'engine': 'google_news',
        'q': query,
        'gl': 'in',  # India
        'hl': 'en',
        'tbm': 'nws',  # News
        'tbs': f'qdr:h{hours}'  # Last N hours
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    return results.get('news_results', [])
```

---

### 3. **EventRegistry** (Best for Research)

**Pros**:
- Academic/research focused
- 300+ million articles
- Good event categorization
- Free tier: 2,000 articles/day

**Cons**:
- More complex API
- Requires learning curve

**Setup**:
```bash
pip install eventregistry
# Get API key from https://eventregistry.org/
```

**Example Code**:
```python
from eventregistry import *

er = EventRegistry(apiKey=os.getenv('EVENTREGISTRY_KEY'))

q = QueryArticlesIter(
    keywords=QueryItems.OR(["India", "earthquake", "economy"]),
    dateStart=datetime.utcnow() - timedelta(hours=2),
    dateEnd=datetime.utcnow(),
    lang="eng"
)

for article in q.execQuery(er, sortBy="date", maxItems=20):
    # Process article
    pass
```

---

### 4. **GNews API** (Good Free Alternative)

**Pros**:
- FREE tier: 100 requests/day
- Simple API
- Good India coverage

**Cons**:
- Limited features on free tier

**Setup**:
```bash
pip install gnews
```

**Example Code**:
```python
from gnews import GNews

google_news = GNews(
    language='en',
    country='IN',  # India
    period='2h',  # Last 2 hours
    max_results=20
)

news = google_news.get_news('India OR technology OR earthquake')
```

---

## 🔧 Integration Strategy

### Option 1: Replace OpenAI (Recommended for Production)
```python
def detect_events_newsapi(lookback_hours=2):
    """Replace OpenAI with NewsAPI"""
    articles = fetch_news_from_newsapi(lookback_hours)

    events = []
    for article in articles:
        # Convert article to event format
        event = convert_newsapi_to_event(article)

        # Use OpenAI ONLY for categorization/enhancement
        event = enhance_event_with_openai(event)

        events.append(event)

    return events
```

### Option 2: Hybrid Approach (Best of Both Worlds)
```python
def detect_events_hybrid(lookback_hours=2):
    """Combine NewsAPI + OpenAI"""

    # Get real news from API
    news_events = fetch_news_from_newsapi(lookback_hours)

    # Get broader context from OpenAI
    openai_events = detect_events_openai(lookback_hours=12)  # Longer window

    # Merge and deduplicate
    all_events = deduplicate_events(news_events + openai_events)

    return all_events
```

### Option 3: Fallback Chain
```python
def detect_events_with_fallback(lookback_hours=2):
    """Try NewsAPI first, fallback to OpenAI"""

    try:
        events = fetch_news_from_newsapi(lookback_hours)
        if len(events) >= 5:
            return events
    except Exception as e:
        print(f"NewsAPI failed: {e}")

    # Fallback to OpenAI
    return detect_events_openai(lookback_hours)
```

---

## 📝 Implementation Template

Here's a complete template you can use:

```python
# Add to collect_events_with_cosmic_state.py

import requests
import os
from datetime import datetime, timedelta

def fetch_newsapi_events(lookback_hours=2):
    """
    Fetch real-time news from NewsAPI
    Returns list of event dictionaries
    """
    api_key = os.getenv('NEWSAPI_KEY')
    if not api_key:
        print("⚠️  NEWSAPI_KEY not set, skipping NewsAPI")
        return []

    print(f"📰 Fetching news from NewsAPI (past {lookback_hours} hours)...")

    try:
        # Calculate time window
        from_time = (datetime.utcnow() - timedelta(hours=lookback_hours)).isoformat()

        # NewsAPI request
        url = 'https://newsapi.org/v2/everything'
        params = {
            'apiKey': api_key,
            'from': from_time,
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': 50,  # Get more, filter later
            'q': '(India OR earthquake OR flood OR economy OR stock OR politics OR technology OR health) -sports -celebrity'
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data['status'] != 'ok':
            print(f"❌ NewsAPI error: {data.get('message', 'Unknown error')}")
            return []

        articles = data.get('articles', [])
        print(f"✅ Found {len(articles)} articles from NewsAPI")

        # Convert to event format
        events = []
        for article in articles[:20]:  # Limit to top 20
            event = {
                'title': article['title'][:100],
                'description': (article.get('description') or article.get('content') or '')[:500],
                'date': article['publishedAt'][:10],
                'time': article['publishedAt'][11:19],
                'timezone': 'UTC',
                'location': article.get('source', {}).get('name', 'Unknown'),
                'category': categorize_news(article),
                'impact_level': assess_impact(article),
                'sources': [article['url']],
                'tags': extract_tags(article)
            }
            events.append(event)

        return events

    except requests.exceptions.RequestException as e:
        print(f"❌ NewsAPI request failed: {e}")
        return []
    except Exception as e:
        print(f"❌ NewsAPI error: {e}")
        return []

def categorize_news(article):
    """Simple categorization based on title/description"""
    text = (article.get('title', '') + ' ' + article.get('description', '')).lower()

    if any(word in text for word in ['earthquake', 'flood', 'cyclone', 'disaster']):
        return 'Natural Disasters'
    elif any(word in text for word in ['stock', 'market', 'economy', 'gdp', 'inflation']):
        return 'Economic Events'
    elif any(word in text for word in ['election', 'government', 'minister', 'policy']):
        return 'Political Events'
    elif any(word in text for word in ['disease', 'health', 'medical', 'hospital']):
        return 'Health & Medical'
    elif any(word in text for word in ['tech', 'ai', 'space', 'innovation']):
        return 'Technology & Innovation'
    else:
        return 'Other'

def assess_impact(article):
    """Simple impact assessment"""
    text = (article.get('title', '') + ' ' + article.get('description', '')).lower()

    if any(word in text for word in ['crisis', 'emergency', 'disaster', 'major']):
        return 'high'
    elif any(word in text for word in ['significant', 'important', 'critical']):
        return 'medium'
    else:
        return 'low'

def extract_tags(article):
    """Extract simple tags"""
    # You could enhance this with NLP
    return []

# Modify detect_events_openai to try NewsAPI first
def detect_events(lookback_hours=2):
    """
    Detect events using NewsAPI first, then OpenAI as fallback/enhancement
    """
    # Try NewsAPI first
    newsapi_events = fetch_newsapi_events(lookback_hours)

    if len(newsapi_events) >= 5:
        print(f"✅ Using {len(newsapi_events)} events from NewsAPI")

        # Optionally enhance with OpenAI for astrological mapping
        for event in newsapi_events:
            if not event.get('astrological_relevance'):
                event['astrological_relevance'] = auto_map_event_to_astrology(event)

        return newsapi_events

    # Fallback to OpenAI if NewsAPI didn't return enough
    print(f"⚠️  NewsAPI returned only {len(newsapi_events)} events, falling back to OpenAI")
    return detect_events_openai(lookback_hours)
```

---

## 🚀 Quick Start

### Step 1: Get API Key
1. Go to https://newsapi.org/register
2. Sign up (free)
3. Copy your API key

### Step 2: Add to Environment
```bash
# In .env.local
NEWSAPI_KEY=your_api_key_here
```

### Step 3: Test It
```bash
python3 -c "
import os
import requests
from dotenv import load_dotenv

load_dotenv('.env.local')
api_key = os.getenv('NEWSAPI_KEY')

url = f'https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}'
response = requests.get(url)
print(f'Status: {response.status_code}')
print(f'Articles: {len(response.json().get(\"articles\", []))}')
"
```

---

## 💰 Cost Comparison

| Service | Free Tier | Paid Tier | Best For |
|---------|-----------|-----------|----------|
| NewsAPI | 100 req/day | $449/mo | Small projects |
| GNews | 100 req/day | N/A | Free projects |
| SerpAPI | 100 searches/mo | $50-250/mo | Google News |
| EventRegistry | 2,000 articles/day | €149/mo | Research |

**Recommendation**: Start with **NewsAPI or GNews** on free tier, upgrade if needed.

---

## 🎯 Next Steps

1. **Get NewsAPI key** (5 minutes): https://newsapi.org/register
2. **Add to .env.local**: `NEWSAPI_KEY=your_key`
3. **Copy integration code** from template above
4. **Test**: Should get real-time news instead of OpenAI guesses

---

**Questions? Check**:
- NewsAPI Docs: https://newsapi.org/docs
- GNews Docs: https://github.com/ranahaani/GNews
- EventRegistry Docs: https://eventregistry.org/documentation
