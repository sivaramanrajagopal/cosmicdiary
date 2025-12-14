# Planetary Data Setup Guide

## Issue: "No planetary data available for this date"

If you see this message when viewing events, it means the planetary positions haven't been calculated yet. This guide will help you fix it.

## Solution

### Quick Fix (Recommended)

1. **Start the Flask API Server**
   ```bash
   python api_server.py
   ```

   This starts the Swiss Ephemeris calculation server on `http://localhost:8000`

2. **Fetch Planetary Data**
   - Go to any event page that shows "No planetary data available"
   - Click the "Fetch Planetary Data" button
   - Wait for the data to be fetched and stored
   - The page will automatically reload with the planetary positions

### How It Works

The Cosmic Diary app uses a two-part architecture:

1. **Next.js Frontend** (Port 3000) - The web interface
2. **Flask API** (Port 8000) - Planetary calculations using Swiss Ephemeris

```
User creates event → Next.js saves event → Flask API calculates planets → Data stored in DB
```

### Automatic Setup for New Events

When you create a new event:
1. The event is saved immediately
2. If the Flask API is running, planetary data is fetched automatically
3. If the Flask API is NOT running, you'll see the "Fetch Planetary Data" button

### Starting the Flask API Automatically

To ensure planetary data is always available, start both servers:

```bash
# Terminal 1: Start Flask API
python api_server.py

# Terminal 2: Start Next.js
npm run dev
```

### Requirements

The Flask API requires these Python packages:
- `flask`
- `flask-cors`
- `pyswisseph` (Swiss Ephemeris)
- `python-dotenv`
- `timezonefinder`

Install them with:
```bash
pip install flask flask-cors pyswisseph python-dotenv timezonefinder
```

### Troubleshooting

**Error: "Flask API is not running"**
- Start the Flask server: `python api_server.py`
- Check if port 8000 is already in use
- Verify `FLASK_API_URL=http://localhost:8000` in `.env.local`

**Error: "Module not found: swisseph"**
```bash
pip install pyswisseph
```

**Port 8000 already in use**
```bash
# Find the process
lsof -i :8000

# Kill it (replace PID with actual process ID)
kill -9 <PID>

# Or change the port in api_server.py and .env.local
```

### Production Deployment

For production, you'll need to:
1. Deploy the Flask API separately (e.g., on Railway, Render, or Heroku)
2. Update `FLASK_API_URL` in your environment variables to point to the deployed Flask API
3. Ensure both services can communicate (check CORS settings)

### Manual Data Population

To fetch planetary data for existing events:
1. Start the Flask API server
2. Visit each event page
3. Click "Fetch Planetary Data"

Or use the bulk recalculation API:
```bash
curl -X POST http://localhost:3000/api/events/recalculate-correlations
```

## Summary

- **Problem**: Planetary data requires the Flask API to calculate positions
- **Solution**: Start Flask API with `python api_server.py`
- **Quick Fix**: Use the "Fetch Planetary Data" button on event pages
- **Long-term**: Keep both Next.js and Flask running together
