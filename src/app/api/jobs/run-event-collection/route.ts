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
    
    // Validate URL is set
    if (!flaskApiUrl || flaskApiUrl === 'http://localhost:8000') {
      console.error('❌ FLASK_API_URL not set or using default localhost');
      return NextResponse.json(
        {
          success: false,
          message: 'Backend URL not configured',
          error: 'FLASK_API_URL environment variable is not set in Vercel. Please set it to your Railway backend URL (e.g., https://cosmicdiary-production.up.railway.app)',
          timestamp: new Date().toISOString(),
        },
        { status: 500 }
      );
    }
    
    const backendUrl = `${flaskApiUrl}/api/jobs/run-event-collection`;
    console.log(`📡 Calling: ${backendUrl}`);
    
    // Call Railway backend endpoint
    let response: Response;
    try {
      response = await fetch(backendUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        // Increase timeout for long-running jobs
        signal: AbortSignal.timeout(900000), // 15 minutes
      });
    } catch (fetchError: any) {
      console.error('❌ Fetch error:', fetchError);
      
      // Handle timeout
      if (fetchError.name === 'TimeoutError' || fetchError.message?.includes('timeout')) {
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
      return NextResponse.json(
        {
          success: false,
          message: 'Cannot connect to backend',
          error: `Failed to connect to Railway backend at ${backendUrl}. Error: ${fetchError.message}. Please verify: 1) Railway backend is running, 2) FLASK_API_URL is set correctly in Vercel, 3) CORS is configured on Railway.`,
          details: {
            url: backendUrl,
            errorType: fetchError.name,
            errorMessage: fetchError.message,
          },
          timestamp: new Date().toISOString(),
        },
        { status: 503 }
      );
    }
    
    // Parse response
    let data: any;
    try {
      const responseText = await response.text();
      console.log(`📥 Response status: ${response.status}`);
      console.log(`📥 Response body (first 200 chars): ${responseText.substring(0, 200)}`);
      
      try {
        data = JSON.parse(responseText);
      } catch (parseError) {
        // If JSON parse fails, return the text
        return NextResponse.json(
          {
            success: false,
            message: 'Invalid response from backend',
            error: `Backend returned non-JSON response. Status: ${response.status}. Response: ${responseText.substring(0, 500)}`,
            timestamp: new Date().toISOString(),
          },
          { status: 500 }
        );
      }
    } catch (parseError: any) {
      return NextResponse.json(
        {
          success: false,
          message: 'Failed to parse backend response',
          error: `Error parsing response: ${parseError.message}`,
          timestamp: new Date().toISOString(),
        },
        { status: 500 }
      );
    }
    
    // Check if response is OK
    if (!response.ok) {
      return NextResponse.json(
        {
          success: false,
          message: data.message || 'Backend request failed',
          error: data.error || `HTTP ${response.status}: ${response.statusText}`,
          details: data.details || data,
          timestamp: data.timestamp || new Date().toISOString(),
        },
        { status: response.status }
      );
    }
    
    // Return success response
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
    console.error('❌ Unexpected error running event collection job:', error);
    console.error('Error stack:', error.stack);
    
    return NextResponse.json(
      {
        success: false,
        message: 'Failed to run event collection job',
        error: error.message || 'Unknown error',
        errorType: error.name || 'Unknown',
        stack: process.env.NODE_ENV === 'development' ? error.stack : undefined,
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

