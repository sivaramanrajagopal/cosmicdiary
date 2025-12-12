import { NextRequest, NextResponse } from 'next/server';

const FLASK_API_URL = process.env.FLASK_API_URL || 'http://localhost:8000';

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const lat = searchParams.get('lat');
    const lng = searchParams.get('lng');

    if (!lat || !lng) {
      return NextResponse.json(
        { error: 'Missing required parameters: lat, lng' },
        { status: 400 }
      );
    }

    const latitude = parseFloat(lat);
    const longitude = parseFloat(lng);

    if (isNaN(latitude) || isNaN(longitude)) {
      return NextResponse.json(
        { error: 'Invalid coordinates: lat and lng must be numbers' },
        { status: 400 }
      );
    }

    if (latitude < -90 || latitude > 90) {
      return NextResponse.json(
        { error: 'Invalid latitude: must be between -90 and 90' },
        { status: 400 }
      );
    }

    if (longitude < -180 || longitude > 180) {
      return NextResponse.json(
        { error: 'Invalid longitude: must be between -180 and 180' },
        { status: 400 }
      );
    }

    // Call Flask API for timezone detection
    try {
      const response = await fetch(
        `${FLASK_API_URL}/api/timezone/detect?lat=${latitude}&lng=${longitude}`,
        {
          next: { revalidate: 0 } // Always fetch fresh data
        }
      );

      if (!response.ok) {
        // Fallback to UTC if Flask API fails
        return NextResponse.json({
          success: true,
          latitude,
          longitude,
          timezone: 'UTC',
          source: 'fallback'
        });
      }

      const data = await response.json();
      return NextResponse.json(data);
    } catch (error) {
      console.error('Error calling Flask API for timezone detection:', error);
      // Fallback to UTC
      return NextResponse.json({
        success: true,
        latitude,
        longitude,
        timezone: 'UTC',
        source: 'fallback'
      });
    }
  } catch (error) {
    console.error('Error in timezone detection:', error);
    return NextResponse.json(
      { error: 'Failed to detect timezone' },
      { status: 500 }
    );
  }
}

