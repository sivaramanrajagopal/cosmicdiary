import { NextRequest, NextResponse } from 'next/server';

/**
 * API endpoint to run event collection job on-demand
 * POST /api/jobs/run-event-collection
 * 
 * This endpoint calls the Railway backend API which has Python installed
 * and can execute the collect_events_with_cosmic_state.py script.
 */
export async function POST(request: NextRequest) {
  try {
    // Get Railway backend URL from environment
    const flaskApiUrl = process.env.FLASK_API_URL || 'http://localhost:8000';
    
    console.log(`🚀 Triggering event collection job via Railway backend: ${flaskApiUrl}`);
    
    // Call Railway backend endpoint
    const response = await fetch(`${flaskApiUrl}/api/jobs/run-event-collection`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      // Increase timeout for long-running jobs
      signal: AbortSignal.timeout(900000), // 15 minutes
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Unknown error' }));
      throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    
    return NextResponse.json({
      success: data.success || false,
      message: data.message || 'Job completed',
      statistics: data.statistics || {
        eventsDetected: 0,
        eventsStored: 0,
        correlationsCreated: 0,
      },
      output: data.output || '',
      error: data.error || undefined,
      timestamp: data.timestamp || new Date().toISOString(),
    });
    
  } catch (error: any) {
    console.error('Error running event collection job:', error);
    
    // Handle timeout errors
    if (error.name === 'TimeoutError' || error.message?.includes('timeout')) {
      return NextResponse.json(
        {
          success: false,
          message: 'Job request timed out',
          error: 'The job is taking longer than expected. It may still be running on the backend.',
          timestamp: new Date().toISOString(),
        },
        { status: 504 }
      );
    }
    
    // Handle network errors
    if (error.message?.includes('fetch') || error.code === 'ECONNREFUSED') {
      return NextResponse.json(
        {
          success: false,
          message: 'Cannot connect to backend',
          error: `Failed to connect to Railway backend. Please check FLASK_API_URL is set correctly. Error: ${error.message}`,
          timestamp: new Date().toISOString(),
        },
        { status: 503 }
      );
    }
    
    return NextResponse.json(
      {
        success: false,
        message: 'Failed to run event collection job',
        error: error.message || 'Unknown error',
        timestamp: new Date().toISOString(),
      },
      { status: 500 }
    );
  }
}

// Also allow GET for simple testing
export async function GET() {
  return NextResponse.json({
    message: 'Event Collection Job API',
    usage: 'POST to this endpoint to trigger the event collection job',
    example: 'POST /api/jobs/run-event-collection',
  });
}

