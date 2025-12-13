import { NextRequest, NextResponse } from 'next/server';
import { getPlanetaryImpactAnalysis } from '@/lib/planetaryImpactAnalysis';

/**
 * GET /api/planetary-impact?period=day|week|month
 * 
 * Get planetary impact analysis for a given time period
 */
export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const period = searchParams.get('period') as 'day' | 'week' | 'month' || 'week';

    if (!['day', 'week', 'month'].includes(period)) {
      return NextResponse.json(
        { error: 'Invalid period. Must be: day, week, or month' },
        { status: 400 }
      );
    }

    const analysis = await getPlanetaryImpactAnalysis(period);

    if (!analysis) {
      return NextResponse.json(
        { error: 'Failed to generate analysis' },
        { status: 500 }
      );
    }

    return NextResponse.json(analysis);
  } catch (error) {
    console.error('Error in planetary impact API:', error);
    return NextResponse.json(
      { 
        error: 'Internal server error',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}

