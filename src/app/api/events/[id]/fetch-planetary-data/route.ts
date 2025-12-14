import { NextRequest, NextResponse } from 'next/server';
import { getEventById } from '@/lib/database';
import { calculateAndStoreCorrelations } from '@/lib/storeCorrelations';

export async function POST(
  request: NextRequest,
  context: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await context.params;
    const eventId = parseInt(id, 10);

    if (isNaN(eventId)) {
      return NextResponse.json(
        { error: 'Invalid event ID' },
        { status: 400 }
      );
    }

    const event = await getEventById(eventId);

    if (!event) {
      return NextResponse.json(
        { error: 'Event not found' },
        { status: 404 }
      );
    }

    // Fetch planetary data for the event date
    const flaskUrl = process.env.FLASK_API_URL || 'http://localhost:8000';
    const planetaryResponse = await fetch(`${flaskUrl}/api/planets/daily?date=${event.date}`);

    if (!planetaryResponse.ok) {
      return NextResponse.json(
        {
          error: 'Flask API not available',
          message: 'Please ensure the Flask API server is running on ' + flaskUrl,
          instructions: 'Run: python api_server.py'
        },
        { status: 503 }
      );
    }

    const planetaryData = await planetaryResponse.json();

    // Store the planetary data in database
    const storageResponse = await fetch(`${request.nextUrl.origin}/api/planetary-data`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(planetaryData),
    });

    if (!storageResponse.ok) {
      console.error('Failed to store planetary data');
    }

    // Calculate and store correlations
    try {
      await calculateAndStoreCorrelations(event);
    } catch (corrError) {
      console.error('Error calculating correlations:', corrError);
    }

    return NextResponse.json({
      success: true,
      message: 'Planetary data fetched and stored successfully',
      data: planetaryData,
    });

  } catch (error) {
    console.error('Error fetching planetary data:', error);
    return NextResponse.json(
      { error: 'Failed to fetch planetary data', details: String(error) },
      { status: 500 }
    );
  }
}
