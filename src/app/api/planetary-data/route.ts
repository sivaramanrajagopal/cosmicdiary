import { NextRequest, NextResponse } from 'next/server';
import { getPlanetaryData, createPlanetaryData } from '@/lib/database';

const FLASK_API_URL = process.env.FLASK_API_URL || 'http://localhost:8000';

async function fetchFromFlaskAPI(date: string) {
  try {
    const response = await fetch(`${FLASK_API_URL}/api/planets/daily?date=${date}`, {
      next: { revalidate: 0 } // Always fetch fresh data from Flask API
    });
    
    if (!response.ok) {
      return null;
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching from Flask API:', error);
    return null;
  }
}

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const date = searchParams.get('date');
    
    if (!date) {
      return NextResponse.json(
        { error: 'Date parameter is required' },
        { status: 400 }
      );
    }
    
    // First, try to get from database
    let planetaryData = await getPlanetaryData(date);
    
    // If not in database, fetch from Flask API (Swiss Ephemeris calculation)
    if (!planetaryData) {
      console.log(`📡 Planetary data not in database for ${date}, fetching from Flask API...`);
      const flaskData = await fetchFromFlaskAPI(date);
      
      if (flaskData) {
        // Store in database for future use (optional - can be async/non-blocking)
        try {
          await createPlanetaryData(flaskData);
          console.log(`✅ Stored planetary data for ${date} in database`);
        } catch (storeError) {
          // Non-blocking: continue even if storage fails
          console.warn('⚠️ Could not store planetary data (non-critical):', storeError);
        }
        
        return NextResponse.json(flaskData);
      } else {
        return NextResponse.json(
          { error: 'Planetary data not available. Flask API may not be running.' },
          { status: 503 }
        );
      }
    }

    return NextResponse.json(planetaryData);
  } catch (error) {
    console.error('Error fetching planetary data:', error);
    return NextResponse.json(
      { error: 'Failed to fetch planetary data' },
      { status: 500 }
    );
  }
}
