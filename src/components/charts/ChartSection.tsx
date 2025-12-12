'use client';

import { useState, useEffect } from 'react';
import { ChartData } from './chart-types';
import { transformChartDataFromDB } from './chart-utils';
import ChartContainer from './ChartContainer';

interface ChartSectionProps {
  eventId: number;
  eventDate: string;
  eventTime?: string;
  hasLocation: boolean;
  initialChartData?: any; // EventChartData from database
}

/**
 * Client component for chart calculation and display
 * Handles chart calculation on demand and displays the chart when available
 */
export default function ChartSection({ 
  eventId, 
  eventDate, 
  eventTime,
  hasLocation,
  initialChartData 
}: ChartSectionProps) {
  const [chartData, setChartData] = useState<ChartData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [calculating, setCalculating] = useState(false);

  // Transform initial chart data if provided
  useEffect(() => {
    if (initialChartData) {
      try {
        const transformed = transformChartDataFromDB(initialChartData);
        setChartData(transformed);
      } catch (err) {
        console.error('Error transforming chart data:', err);
        setError('Failed to load chart data');
      }
    }
  }, [initialChartData]);

  const handleCalculateChart = async () => {
    if (!hasLocation) {
      setError('Event must have location coordinates to calculate chart');
      return;
    }

    setCalculating(true);
    setError(null);

    try {
      const response = await fetch('/api/chart/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ eventId }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to calculate chart');
      }

      const result = await response.json();
      
      if (result.success && result.chart) {
        // Transform the chart data to match our ChartData format
        const transformed = transformChartDataFromDB(result.chart);
        setChartData(transformed);
        
        // Refresh the page to show the chart in the server component
        // This ensures the chart data is persisted in the database
        setTimeout(() => {
          window.location.reload();
        }, 1000);
      } else {
        throw new Error('Invalid response from server');
      }
    } catch (err) {
      console.error('Error calculating chart:', err);
      setError(err instanceof Error ? err.message : 'Failed to calculate chart');
    } finally {
      setCalculating(false);
    }
  };

  if (!hasLocation) {
    return (
      <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
        <h3 className="text-2xl font-semibold mb-4">🔮 Astrological Chart</h3>
        <div className="bg-yellow-900/30 border border-yellow-700/50 p-4 rounded-lg">
          <p className="text-yellow-200 mb-2">
            ⚠️ Chart calculation requires location coordinates
          </p>
          <p className="text-sm text-yellow-300/80">
            Please add latitude and longitude to this event to calculate the astrological chart.
          </p>
        </div>
      </div>
    );
  }

  if (chartData) {
    return (
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-2xl font-semibold">🔮 Astrological Chart</h3>
          <button
            onClick={handleCalculateChart}
            disabled={calculating}
            className="px-4 py-2 bg-purple-600 hover:bg-purple-700 disabled:bg-slate-600 rounded-lg transition-colors text-sm font-medium"
          >
            {calculating ? 'Recalculating...' : 'Recalculate Chart'}
          </button>
        </div>
        <ChartContainer 
          chartData={chartData} 
          eventId={eventId} 
          eventDate={eventDate}
        />
      </div>
    );
  }

  return (
    <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
      <h3 className="text-2xl font-semibold mb-4">🔮 Astrological Chart</h3>
      
      {error && (
        <div className="bg-red-900/30 border border-red-700/50 p-4 rounded-lg mb-4">
          <p className="text-red-200 mb-2">❌ Error</p>
          <p className="text-sm text-red-300/80">{error}</p>
        </div>
      )}

      <div className="bg-slate-900/50 p-6 rounded-lg border border-slate-700 text-center">
        <p className="text-slate-300 mb-4">
          Chart has not been calculated yet. Click the button below to calculate the astrological chart for this event.
        </p>
        <button
          onClick={handleCalculateChart}
          disabled={calculating || loading}
          className="px-6 py-3 bg-purple-600 hover:bg-purple-700 disabled:bg-slate-600 disabled:cursor-not-allowed rounded-lg transition-colors font-medium text-lg"
        >
          {calculating ? (
            <>
              <span className="inline-block animate-spin mr-2">⏳</span>
              Calculating Chart...
            </>
          ) : (
            <>
              🎯 Calculate Chart
            </>
          )}
        </button>
        {calculating && (
          <p className="text-sm text-slate-400 mt-4">
            This may take a few seconds. Please wait...
          </p>
        )}
      </div>

      <div className="mt-4 p-4 bg-slate-900/30 rounded-lg">
        <p className="text-xs text-slate-400 mb-2">Chart calculation includes:</p>
        <ul className="text-xs text-slate-500 space-y-1 list-disc list-inside">
          <li>Ascendant (Lagna) calculation</li>
          <li>House cusps (Placidus system)</li>
          <li>Planetary positions with house placements</li>
          <li>Planetary strengths (exaltation, debilitation, etc.)</li>
          <li>North Indian and South Indian chart views</li>
        </ul>
      </div>
    </div>
  );
}

