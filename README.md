# 🌙 Cosmic Diary

A full-stack astrological research application that correlates world events with planetary positions using Swiss Ephemeris calculations.

## 🎯 Features

- **Event Recording**: Manual and automated event collection with categories and impact levels
- **Planetary Calculations**: Accurate sidereal calculations using Swiss Ephemeris (Lahiri Ayanamsa)
- **House Mapping**: Automatic mapping of events to astrological houses (Kalapurushan method)
- **Planetary Aspects**: Calculation of planetary aspects (Drishti) to event houses
- **Data Correlation**: Link events with planetary positions, houses, and aspects for research
- **Analysis Dashboard**: Comprehensive astrological analysis with patterns and insights
- **Email Reports**: Daily summaries and weekly analysis (optional)
- **Modern UI**: Next.js 15 with TypeScript and Tailwind CSS

## 🏗️ Architecture

```
Frontend (Next.js) → Supabase Database
                    ↑
Backend (Flask API) → Swiss Ephemeris
                    ↓
Automation Scripts → Cron Jobs
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.9+
- Supabase account
- (Optional) OpenAI API key for automated events
- (Optional) Email credentials for reports

### 1. Clone and Install

```bash
cd CosmicDiary

# Install frontend dependencies
npm install

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Database Setup

1. Create a Supabase project
2. Run the schema SQL:
   ```bash
   # In Supabase SQL editor, run:
   cat database_schema.sql
   ```
3. Get your Supabase URL and keys from project settings

### 3. Environment Variables

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

Required variables:
- `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY`
- `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY`

Optional:
- `OPENAI_API_KEY` - For automated event collection
- `EMAIL_USER`, `EMAIL_PASSWORD`, `RECIPIENT_EMAIL` - For email reports

### 4. Start Services

**Terminal 1 - Flask API** (for planetary calculations):
```bash
python api_server.py
```

**Terminal 2 - Next.js Frontend**:
```bash
npm run dev
```

Visit `http://localhost:3000`

### 5. Setup Automation (Optional)

```bash
# Setup cron jobs
./setup_cron.sh

# Or manually run scripts
python daily_planetary_job.py           # Calculate today's planetary data
python import_automated_events.py       # Collect events for yesterday
python email_reports.py daily           # Send daily summary
```

## 📁 Project Structure

```
CosmicDiary/
├── src/                          # Next.js frontend
│   ├── app/                      # App Router pages
│   ├── components/               # React components
│   └── lib/                      # Utilities and types
├── api_server.py                 # Flask API for calculations
├── daily_planetary_job.py        # Daily planetary data job
├── import_automated_events.py    # Automated event collection
├── email_reports.py              # Email generation
├── database_schema.sql           # Database schema
├── setup_cron.sh                 # Cron job setup
└── requirements.txt              # Python dependencies
```

## 🧪 Testing

```bash
# Test Supabase connection
python test_supabase_connection.py

# Test full setup
python test_full_setup.py
```

## 📚 Documentation

**📖 Complete Documentation Available:**

- **[COMPLETE_SYSTEM_DOCUMENTATION.md](./COMPLETE_SYSTEM_DOCUMENTATION.md)** ⭐ **START HERE** - Complete end-to-end documentation covering requirements, architecture, database schema, APIs, and implementation
- **[CODE_STRUCTURE_GUIDE.md](./CODE_STRUCTURE_GUIDE.md)** - Code organization, file structure, and data flow
- **[QUICK_IMPLEMENTATION_GUIDE.md](./QUICK_IMPLEMENTATION_GUIDE.md)** - 5-step quick start guide
- **[DOCUMENTATION_INDEX.md](./DOCUMENTATION_INDEX.md)** - Index of all documentation files

**🔍 Quick References:**
- **Database Schema:** `database_schema.sql`
- **House Mapping Queries:** `QUERY_HOUSE_MAPPINGS.md`
- **Planetary Data Queries:** `QUERY_PLANETARY_DATA.md`
- **Environment Setup:** `.env.example`

**For detailed implementation, architecture, and API documentation, see [COMPLETE_SYSTEM_DOCUMENTATION.md](./COMPLETE_SYSTEM_DOCUMENTATION.md)**

## 🔧 Development

### Running Flask API
```bash
FLASK_PORT=8000 python api_server.py
```

### Running Next.js
```bash
npm run dev
```

### Database Migrations
Run SQL from `database_schema.sql` in Supabase SQL editor.

## 📝 License

MIT
