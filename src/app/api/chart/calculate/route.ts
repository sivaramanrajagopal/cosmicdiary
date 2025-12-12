import { NextRequest, NextResponse } from 'next/server';
import { getEventById, storeEventChartData } from '@/lib/database';

const FLASK_API_URL = process.env.FLASK_API_URL || 'http://localhost:8000';

/**
 * POST /api/chart/calculate
 * 
 * Calculate astrological chart for an event.
 * 
 * Request body:
 *   { eventId: number }
 * 
 * Response:
 *   { success: true, chart: ChartData } on success
 *   { error: string } on error
 */
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { eventId } = body;

    if (!eventId || typeof eventId !== 'number') {
      return NextResponse.json(
        { error: 'eventId is required and must be a number' },
        { status: 400 }
      );
    }

    // Get event with location and time
    const event = await getEventById(eventId);
    if (!event) {
      return NextResponse.json(
        { error: 'Event not found' },
        { status: 404 }
      );
    }

    // Check if event has required data for chart calculation
    if (!event.latitude || !event.longitude || !event.date) {
      return NextResponse.json(
        { 
          error: 'Event missing required data for chart calculation',
          details: 'Event must have latitude, longitude, and date'
        },
        { status: 400 }
      );
    }

    // Prepare request for Flask API
    const chartRequest = {
      date: event.date,
      time: event.event_time || '12:00:00',
      latitude: event.latitude,
      longitude: event.longitude,
      timezone: event.timezone || 'UTC',
    };

    // Call Flask API for chart calculation
    let response;
    try {
      response = await fetch(`${FLASK_API_URL}/api/chart/calculate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(chartRequest),
        // Add timeout to prevent hanging
        signal: AbortSignal.timeout(30000), // 30 seconds
      });
    } catch (fetchError: any) {
      if (fetchError.name === 'AbortError') {
        return NextResponse.json(
          { error: 'Chart calculation request timed out' },
          { status: 504 }
        );
      }
      throw fetchError;
    }

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Unknown error' }));
      console.error('Flask API error:', errorData);
      return NextResponse.json(
        { 
          error: errorData.error || 'Failed to calculate chart',
          details: errorData.details || 'Chart calculation service returned an error'
        },
        { status: response.status }
      );
    }

    const chartData = await response.json();

    if (!chartData.success || !chartData.chart) {
      return NextResponse.json(
        { error: 'Invalid response from chart calculation service' },
        { status: 500 }
      );
    }

    // Store the chart data in the database
    const storedChartData = await storeEventChartData(eventId, chartData.chart);
    
    if (!storedChartData) {
      console.error('Failed to store chart data, but returning calculated chart anyway');
    }

    return NextResponse.json({
      success: true,
      chart: chartData.chart,
      stored: !!storedChartData,
    });
  } catch (error) {
    console.error('Error calculating chart:', error);
    return NextResponse.json(
      { 
        error: 'Internal server error',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}

