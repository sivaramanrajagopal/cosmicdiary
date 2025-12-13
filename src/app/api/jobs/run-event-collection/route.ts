import { NextRequest, NextResponse } from 'next/server';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

/**
 * API endpoint to run event collection job on-demand
 * POST /api/jobs/run-event-collection
 */
export async function POST(request: NextRequest) {
  try {
    // Optional: Add authentication/authorization check here
    // For now, we'll allow it but you should secure this in production
    
    // Get the script path (assuming we're in the repository root)
    const scriptPath = process.cwd() + '/collect_events_with_cosmic_state.py';
    
    console.log(`🚀 Starting on-demand event collection job...`);
    
    // Run the Python script
    // Note: This runs in the server environment, so it has access to environment variables
    const { stdout, stderr } = await execAsync(
      `cd ${process.cwd()} && python3 collect_events_with_cosmic_state.py`,
      {
        env: {
          ...process.env,
          // Ensure environment variables are passed
          SUPABASE_URL: process.env.SUPABASE_URL,
          SUPABASE_SERVICE_ROLE_KEY: process.env.SUPABASE_SERVICE_ROLE_KEY,
          OPENAI_API_KEY: process.env.OPENAI_API_KEY,
          FLASK_API_URL: process.env.FLASK_API_URL || 'http://localhost:8000',
        },
        maxBuffer: 10 * 1024 * 1024, // 10MB buffer for output
        timeout: 900000, // 15 minutes timeout
      }
    );
    
    // Parse output to extract statistics
    const output = stdout;
    const errorOutput = stderr;
    
    // Extract statistics from output
    const eventsDetectedMatch = output.match(/Events Detected:\s*(\d+)/i);
    const eventsStoredMatch = output.match(/Events Stored:\s*(\d+)/i);
    const correlationsMatch = output.match(/Correlations Created:\s*(\d+)/i);
    
    const eventsDetected = eventsDetectedMatch ? parseInt(eventsDetectedMatch[1]) : 0;
    const eventsStored = eventsStoredMatch ? parseInt(eventsStoredMatch[1]) : 0;
    const correlationsCreated = correlationsMatch ? parseInt(correlationsMatch[1]) : 0;
    
    // Check for errors
    const hasErrors = output.includes('✗') || output.includes('ERROR') || errorOutput.length > 0;
    
    return NextResponse.json({
      success: !hasErrors,
      message: hasErrors ? 'Job completed with errors' : 'Job completed successfully',
      statistics: {
        eventsDetected,
        eventsStored,
        correlationsCreated,
      },
      output: output.substring(Math.max(0, output.length - 5000)), // Last 5000 chars
      error: errorOutput || undefined,
      timestamp: new Date().toISOString(),
    });
    
  } catch (error: any) {
    console.error('Error running event collection job:', error);
    
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

