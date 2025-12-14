#!/bin/bash
# NewsAPI Setup Helper Script
# This script helps you set up NewsAPI integration

echo "📰 NewsAPI Setup Helper"
echo "======================="
echo ""

# Check if NEWSAPI_KEY is already set
if grep -q "NEWSAPI_KEY=" .env.local 2>/dev/null; then
    echo "✅ NEWSAPI_KEY already exists in .env.local"
    echo ""
    echo "Current value:"
    grep "NEWSAPI_KEY=" .env.local
    echo ""
    read -p "Do you want to update it? (y/N): " update
    if [[ ! $update =~ ^[Yy]$ ]]; then
        echo "Keeping existing key."
        exit 0
    fi
fi

echo "📝 To get a FREE NewsAPI key:"
echo "   1. Visit: https://newsapi.org/register"
echo "   2. Sign up (free - takes 2 minutes)"
echo "   3. Copy your API key"
echo ""
echo "Free tier includes:"
echo "   • 100 requests per day"
echo "   • Access to 150+ news sources"
echo "   • Perfect for this project!"
echo ""

read -p "Enter your NewsAPI key (or press Enter to skip): " api_key

if [ -z "$api_key" ]; then
    echo "⚠️  No key entered. Skipping NewsAPI setup."
    echo "   You can add it later to .env.local"
    exit 0
fi

# Add to .env.local
if [ -f .env.local ]; then
    # Remove old key if exists
    sed -i '' '/NEWSAPI_KEY=/d' .env.local 2>/dev/null || sed -i '/NEWSAPI_KEY=/d' .env.local
fi

echo "NEWSAPI_KEY=$api_key" >> .env.local

echo ""
echo "✅ NewsAPI key added to .env.local"
echo ""
echo "🧪 Testing NewsAPI connection..."
echo ""

# Test the API key
python3 -c "
import os
import requests
from dotenv import load_dotenv

load_dotenv('.env.local')
api_key = os.getenv('NEWSAPI_KEY')

if not api_key:
    print('❌ Failed to load API key')
    exit(1)

url = f'https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}'
try:
    response = requests.get(url, timeout=10)
    data = response.json()

    if response.status_code == 200 and data.get('status') == 'ok':
        articles = data.get('articles', [])
        print(f'✅ SUCCESS! NewsAPI is working')
        print(f'   • Status: {data[\"status\"]}')
        print(f'   • Articles found: {len(articles)}')
        print(f'   • Requests remaining today: Check at https://newsapi.org/account')
        print('')
        print('Sample headlines:')
        for i, article in enumerate(articles[:3], 1):
            print(f'   {i}. {article[\"title\"][:70]}')
    else:
        print(f'❌ API Error: {data.get(\"message\", \"Unknown error\")}')
        print(f'   Status code: {response.status_code}')
        exit(1)
except Exception as e:
    print(f'❌ Connection error: {e}')
    exit(1)
"

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 NewsAPI setup complete!"
    echo ""
    echo "Next steps:"
    echo "   1. Run: python3 collect_events_with_cosmic_state.py --lookback-hours 2"
    echo "   2. You should see: '🔄 Attempting NewsAPI integration first...'"
    echo "   3. Events will now come from real-time news!"
    echo ""
    echo "⚙️  For GitHub Actions:"
    echo "   Add NEWSAPI_KEY to GitHub Secrets:"
    echo "   Repository → Settings → Secrets → New secret"
    echo "   Name: NEWSAPI_KEY"
    echo "   Value: $api_key"
else
    echo ""
    echo "⚠️  Setup completed but test failed."
    echo "   Please check your API key at: https://newsapi.org/account"
fi
