'use client';

import { useState } from 'react';
import { RefreshCw, AlertCircle } from 'lucide-react';

interface FetchPlanetaryDataButtonProps {
  eventId: number;
  eventDate: string;
  onSuccess?: () => void;
}

export default function FetchPlanetaryDataButton({ eventId, eventDate, onSuccess }: FetchPlanetaryDataButtonProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const handleFetch = async () => {
    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      const response = await fetch(`/api/events/${eventId}/fetch-planetary-data`, {
        method: 'POST',
      });

      const data = await response.json();

      if (!response.ok) {
        if (response.status === 503) {
          setError(data.message || 'Flask API is not running. Please start the Flask server with: python api_server.py');
        } else {
          setError(data.error || 'Failed to fetch planetary data');
        }
        return;
      }

      setSuccess(true);

      // Reload the page after a short delay to show the new data
      setTimeout(() => {
        if (onSuccess) {
          onSuccess();
        } else {
          window.location.reload();
        }
      }, 1500);

    } catch (err) {
      console.error('Error fetching planetary data:', err);
      setError('An unexpected error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-800/50 p-4 sm:p-6 rounded-lg border border-slate-700">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div className="flex-1">
          <h3 className="text-xl sm:text-2xl font-semibold mb-2 flex items-center gap-2">
            <AlertCircle size={24} className="text-yellow-500" />
            Planetary Positions
          </h3>
          <p className="text-slate-400 text-sm sm:text-base mb-2">
            No planetary data available for {eventDate}.
          </p>
          {!success && !error && (
            <p className="text-slate-500 text-xs sm:text-sm">
              Click the button to fetch planetary positions from the Swiss Ephemeris calculations.
            </p>
          )}

          {error && (
            <div className="mt-3 p-3 bg-red-900/30 border border-red-700/50 rounded-lg">
              <p className="text-red-300 text-sm">{error}</p>
              {error.includes('Flask API') && (
                <div className="mt-2 text-xs text-red-400">
                  <p className="font-mono bg-slate-900/50 p-2 rounded mt-1">
                    $ python api_server.py
                  </p>
                  <p className="mt-1">The Flask API server must be running to calculate planetary positions.</p>
                </div>
              )}
            </div>
          )}

          {success && (
            <div className="mt-3 p-3 bg-green-900/30 border border-green-700/50 rounded-lg">
              <p className="text-green-300 text-sm">✓ Planetary data fetched successfully! Reloading...</p>
            </div>
          )}
        </div>

        <button
          onClick={handleFetch}
          disabled={loading || success}
          className="bg-purple-600 hover:bg-purple-700 disabled:bg-slate-600 disabled:cursor-not-allowed px-6 py-3 rounded-lg transition-colors font-medium flex items-center justify-center gap-2 whitespace-nowrap"
        >
          <RefreshCw size={18} className={loading ? 'animate-spin' : ''} />
          {loading ? 'Fetching...' : success ? 'Success!' : 'Fetch Planetary Data'}
        </button>
      </div>
    </div>
  );
}
