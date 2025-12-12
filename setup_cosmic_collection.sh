#!/bin/bash
# Cosmic Diary - Cosmic Collection System Setup Script
#
# This script sets up everything needed for the cosmic state collection system.
#
# Make this script executable:
#   chmod +x setup_cosmic_collection.sh
#
# Run with:
#   ./setup_cosmic_collection.sh
#
# Prerequisites:
#   - Python 3.9+ installed
#   - .env.local file with required environment variables
#   - Supabase database access

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=================================================="
echo "Cosmic Diary - Cosmic Collection Setup"
echo "=================================================="
echo ""

# ============================================================================
# STEP 1: Check Python Version
# ============================================================================
echo -e "${BLUE}STEP 1: Checking Python version...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 is not installed${NC}"
    echo "Please install Python 3.9 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 9 ]); then
    echo -e "${RED}✗ Python 3.9+ required, found Python $PYTHON_VERSION${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python version: $PYTHON_VERSION${NC}"
echo ""

# ============================================================================
# STEP 2: Check Environment Variables
# ============================================================================
echo -e "${BLUE}STEP 2: Checking environment variables...${NC}"

# Load .env.local if it exists
if [ -f ".env.local" ]; then
    echo "Loading .env.local..."
    set -a
    source .env.local
    set +a
elif [ -f ".env" ]; then
    echo "Loading .env..."
    set -a
    source .env
    set +a
else
    echo -e "${YELLOW}⚠️  No .env.local or .env file found${NC}"
fi

MISSING_VARS=()

if [ -z "$OPENAI_API_KEY" ]; then
    MISSING_VARS+=("OPENAI_API_KEY")
fi

if [ -z "$SUPABASE_URL" ]; then
    MISSING_VARS+=("SUPABASE_URL")
fi

if [ -z "$SUPABASE_SERVICE_ROLE_KEY" ]; then
    MISSING_VARS+=("SUPABASE_SERVICE_ROLE_KEY")
fi

if [ ${#MISSING_VARS[@]} -gt 0 ]; then
    echo -e "${RED}✗ Missing required environment variables:${NC}"
    for var in "${MISSING_VARS[@]}"; do
        echo -e "${RED}   - $var${NC}"
    done
    echo ""
    echo "Please set these in .env.local file:"
    echo "  OPENAI_API_KEY=your_key_here"
    echo "  SUPABASE_URL=your_url_here"
    echo "  SUPABASE_SERVICE_ROLE_KEY=your_key_here"
    exit 1
fi

echo -e "${GREEN}✓ All required environment variables found${NC}"
echo ""

# ============================================================================
# STEP 3: Install Python Dependencies
# ============================================================================
echo -e "${BLUE}STEP 3: Installing Python dependencies...${NC}"

# Check if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing from requirements.txt..."
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt --break-system-packages 2>/dev/null || \
    python3 -m pip install -r requirements.txt --user 2>/dev/null || \
    python3 -m pip install -r requirements.txt
else
    echo "requirements.txt not found, installing dependencies directly..."
    python3 -m pip install --upgrade pip
    python3 -m pip install openai supabase python-dotenv pyswisseph pytz timezonefinder --break-system-packages 2>/dev/null || \
    python3 -m pip install openai supabase python-dotenv pyswisseph pytz timezonefinder --user 2>/dev/null || \
    python3 -m pip install openai supabase python-dotenv pyswisseph pytz timezonefinder
fi

echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# ============================================================================
# STEP 4: Run Database Migrations
# ============================================================================
echo -e "${BLUE}STEP 4: Database Migrations${NC}"
echo ""
echo "The following database migrations need to be run in Supabase SQL Editor:"
echo ""
echo "  1. database_migrations/008_create_cosmic_snapshots.sql"
echo "     - Creates cosmic_snapshots table"
echo ""
echo "  2. database_migrations/009_create_event_cosmic_correlations.sql"
echo "     - Creates event_cosmic_correlations table"
echo ""
echo "Instructions:"
echo "  1. Go to your Supabase Dashboard"
echo "  2. Navigate to SQL Editor"
echo "  3. Copy and paste each migration file"
echo "  4. Execute each migration"
echo "  5. Verify tables were created in Table Editor"
echo ""

read -p "Have you run both migrations? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}⚠️  Please run the migrations first, then re-run this script.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Migrations confirmed${NC}"
echo ""

# ============================================================================
# STEP 5: Test Calculation Modules
# ============================================================================
echo -e "${BLUE}STEP 5: Testing calculation modules...${NC}"
echo ""

if [ ! -f "test_cosmic_collection.py" ]; then
    echo -e "${YELLOW}⚠️  test_cosmic_collection.py not found, skipping calculation tests${NC}"
else
    if python3 test_cosmic_collection.py; then
        echo -e "${GREEN}✓ Calculation tests passed${NC}"
    else
        echo -e "${RED}✗ Calculation tests failed${NC}"
        echo "Please review the test output above and fix any issues"
        exit 1
    fi
fi
echo ""

# ============================================================================
# STEP 6: Test Database Connection
# ============================================================================
echo -e "${BLUE}STEP 6: Testing database connection...${NC}"
echo ""

if [ ! -f "test_supabase_connection.py" ]; then
    echo -e "${YELLOW}⚠️  test_supabase_connection.py not found, skipping database test${NC}"
else
    if python3 test_supabase_connection.py; then
        echo -e "${GREEN}✓ Database connection successful${NC}"
    else
        echo -e "${RED}✗ Database connection failed${NC}"
        echo "Please check your SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY"
        exit 1
    fi
fi
echo ""

# ============================================================================
# STEP 7: Verify Required Files
# ============================================================================
echo -e "${BLUE}STEP 7: Verifying required files...${NC}"

REQUIRED_FILES=(
    "collect_events_with_cosmic_state.py"
    "astro_calculations.py"
    "aspect_calculator.py"
    "correlation_analyzer.py"
)

MISSING_FILES=()
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        MISSING_FILES+=("$file")
    fi
done

if [ ${#MISSING_FILES[@]} -gt 0 ]; then
    echo -e "${RED}✗ Missing required files:${NC}"
    for file in "${MISSING_FILES[@]}"; do
        echo -e "${RED}   - $file${NC}"
    done
    exit 1
fi

echo -e "${GREEN}✓ All required files present${NC}"
echo ""

# ============================================================================
# STEP 8: Dry Run (Optional)
# ============================================================================
echo -e "${BLUE}STEP 8: System Verification${NC}"
echo ""
echo "Verifying system components..."

# Check if modules can be imported
echo "  - Testing module imports..."
python3 -c "
from astro_calculations import calculate_complete_chart
from aspect_calculator import calculate_all_aspects
from correlation_analyzer import correlate_event_with_snapshot
print('    ✓ All modules imported successfully')
" 2>&1

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Module import failed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ System verification complete${NC}"
echo ""

# ============================================================================
# SUCCESS MESSAGE
# ============================================================================
echo ""
echo "=================================================="
echo -e "${GREEN}✓ Setup Complete!${NC}"
echo "=================================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Test manually (recommended):"
echo "   python3 collect_events_with_cosmic_state.py"
echo ""
echo "2. Deploy GitHub Actions workflow:"
echo "   - The workflow is already configured in .github/workflows/event-collection.yml"
echo "   - Ensure GitHub secrets are set:"
echo "     * OPENAI_API_KEY"
echo "     * SUPABASE_URL"
echo "     * SUPABASE_SERVICE_ROLE_KEY"
echo ""
echo "3. Monitor first few runs:"
echo "   - Check GitHub Actions tab for workflow runs"
echo "   - Verify cosmic_snapshots table is being populated"
echo "   - Verify event_cosmic_correlations table has data"
echo ""
echo "4. Schedule (if using cron instead of GitHub Actions):"
echo "   - The system runs every 2 hours at :30 past the hour"
echo "   - Cron: 30 */2 * * *"
echo ""
echo "=================================================="
echo ""
echo -e "${GREEN}System is ready for cosmic state collection!${NC}"
echo ""

