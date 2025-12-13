'use client';

import { useState } from 'react';
import { format } from 'date-fns';

interface JobResult {
  success: boolean;
  message: string;
  statistics?: {
    eventsDetected: number;
    eventsStored: number;
    correlationsCreated: number;
  };
  output?: string;
  error?: string;
  timestamp?: string;
}

export default function JobsPage() {
  const [running, setRunning] = useState(false);
  const [result, setResult] = useState<JobResult | null>(null);
  const [showOutput, setShowOutput] = useState(false);

  const runEventCollection = async () => {
    setRunning(true);
    setResult(null);
    setShowOutput(false);

    try {
      const response = await fetch('/api/jobs/run-event-collection', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const data = await response.json();
      setResult(data);
    } catch (error: any) {
      setResult({
        success: false,
        message: 'Failed to trigger job',
        error: error.message || 'Unknown error',
        timestamp: new Date().toISOString(),
      });
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold">Job Runner</h2>
          <p className="text-slate-400 mt-2">
            Run on-demand jobs to collect events and capture cosmic state
          </p>
        </div>
      </div>

      {/* Event Collection Job */}
      <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
        <h3 className="text-xl font-semibold mb-4 text-purple-300">
          Event Collection with Cosmic State
        </h3>
        
        <div className="space-y-4">
          <div className="bg-slate-900/50 p-4 rounded border border-slate-700">
            <p className="text-sm text-slate-300 mb-2">
              This job will:
            </p>
            <ul className="list-disc list-inside text-sm text-slate-400 space-y-1">
              <li>Capture current cosmic state (planetary positions, aspects)</li>
              <li>Detect world events via OpenAI</li>
              <li>Calculate astrological charts for each event</li>
              <li>Correlate events with cosmic state</li>
              <li>Store all data in the database</li>
            </ul>
          </div>

          <button
            onClick={runEventCollection}
            disabled={running}
            className={`px-6 py-3 rounded-lg font-medium transition-colors ${
              running
                ? 'bg-slate-600 cursor-not-allowed'
                : 'bg-purple-600 hover:bg-purple-700'
            }`}
          >
            {running ? (
              <span className="flex items-center gap-2">
                <span className="animate-spin">⏳</span>
                Running Job... (This may take 1-2 minutes)
              </span>
            ) : (
              '▶️ Run Event Collection Job'
            )}
          </button>

          {result && (
            <div className={`mt-4 p-4 rounded-lg border ${
              result.success
                ? 'bg-green-900/20 border-green-700'
                : 'bg-red-900/20 border-red-700'
            }`}>
              <div className="flex items-start justify-between mb-2">
                <div>
                  <h4 className={`font-semibold ${
                    result.success ? 'text-green-300' : 'text-red-300'
                  }`}>
                    {result.success ? '✅ Success' : '❌ Failed'}
                  </h4>
                  <p className="text-sm text-slate-400">
                    {result.message}
                  </p>
                  {result.timestamp && (
                    <p className="text-xs text-slate-500 mt-1">
                      {format(new Date(result.timestamp), 'PPpp')}
                    </p>
                  )}
                </div>
                {result.output && (
                  <button
                    onClick={() => setShowOutput(!showOutput)}
                    className="text-sm text-purple-400 hover:text-purple-300"
                  >
                    {showOutput ? 'Hide' : 'Show'} Output
                  </button>
                )}
              </div>

              {result.statistics && (
                <div className="grid grid-cols-3 gap-4 mt-4">
                  <div className="bg-slate-900/50 p-3 rounded">
                    <div className="text-xs text-slate-400">Events Detected</div>
                    <div className="text-2xl font-bold text-blue-400">
                      {result.statistics.eventsDetected}
                    </div>
                  </div>
                  <div className="bg-slate-900/50 p-3 rounded">
                    <div className="text-xs text-slate-400">Events Stored</div>
                    <div className="text-2xl font-bold text-green-400">
                      {result.statistics.eventsStored}
                    </div>
                  </div>
                  <div className="bg-slate-900/50 p-3 rounded">
                    <div className="text-xs text-slate-400">Correlations</div>
                    <div className="text-2xl font-bold text-purple-400">
                      {result.statistics.correlationsCreated}
                    </div>
                  </div>
                </div>
              )}

              {result.error && (
                <div className="mt-4 p-3 bg-red-900/30 rounded border border-red-800">
                  <p className="text-sm text-red-300 font-mono whitespace-pre-wrap">
                    {result.error}
                  </p>
                </div>
              )}

              {showOutput && result.output && (
                <div className="mt-4 p-4 bg-slate-900 rounded border border-slate-700">
                  <h5 className="text-sm font-semibold text-slate-300 mb-2">Job Output:</h5>
                  <pre className="text-xs text-slate-400 font-mono whitespace-pre-wrap overflow-auto max-h-96">
                    {result.output}
                  </pre>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Information Section */}
      <div className="bg-blue-900/20 p-4 rounded-lg border border-blue-800">
        <h4 className="text-blue-300 font-semibold mb-2">ℹ️ Information</h4>
        <ul className="text-sm text-blue-200 space-y-1">
          <li>• Jobs run on the server and may take 1-2 minutes to complete</li>
          <li>• The job uses OpenAI API to detect events (requires OPENAI_API_KEY)</li>
          <li>• Results are stored in Supabase database</li>
          <li>• Check the output for detailed logs and statistics</li>
        </ul>
      </div>
    </div>
  );
}

