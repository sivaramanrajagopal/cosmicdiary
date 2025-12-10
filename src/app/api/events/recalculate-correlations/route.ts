import { NextRequest, NextResponse } from 'next/server';
import { getEvents } from '@/lib/database';
import { recalculateAllCorrelations } from '@/lib/storeCorrelations';

/**
 * API endpoint to recalculate and store correlations for all events
 * GET/POST /api/events/recalculate-correlations
 */
export async function GET(request: NextRequest) {
  try {
    const events = await getEvents();
    
    // Recalculate correlations for all events (in background)
    recalculateAllCorrelations(events).catch(error => {
      console.error('Error in background correlation recalculation:', error);
    });
    
    return NextResponse.json({
      message: `Started recalculating correlations for ${events.length} events. This will run in the background.`,
      eventCount: events.length,
      status: 'processing',
    });
  } catch (error) {
    console.error('Error initiating correlation recalculation:', error);
    return NextResponse.json(
      { error: 'Failed to initiate correlation recalculation' },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const events = await getEvents();
    
    // Recalculate correlations for all events (in background)
    recalculateAllCorrelations(events).catch(error => {
      console.error('Error in background correlation recalculation:', error);
    });
    
    return NextResponse.json({
      message: `Started recalculating correlations for ${events.length} events. This will run in the background.`,
      eventCount: events.length,
      status: 'processing',
    });
  } catch (error) {
    console.error('Error initiating correlation recalculation:', error);
    return NextResponse.json(
      { error: 'Failed to initiate correlation recalculation' },
      { status: 500 }
    );
  }
}

