'use client';

import { useState, useEffect } from 'react';
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { getPlanetaryImpactAnalysis, type PlanetaryImpactSummary } from '@/lib/planetaryImpactAnalysis';
import { format } from 'date-fns';

const HOUSE_COLORS = [
  '#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#8dd1e1',
  '#d084d0', '#ffb347', '#87ceeb', '#dda0dd', '#98d8c8',
  '#f7dc6f', '#bb8fce'
];

const PLANET_COLORS: Record<string, string> = {
  'Sun': '#FFA500',
  'Moon': '#C0C0C0',
  'Mars': '#FF0000',
  'Mercury': '#808080',
  'Jupiter': '#FFD700',
  'Venus': '#FF69B4',
  'Saturn': '#0000FF',
  'Rahu': '#8B008B',
  'Ketu': '#2F4F4F',
};

export default function PlanetaryImpactVisualization() {
  const [period, setPeriod] = useState<'day' | 'week' | 'month'>('week');
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState<PlanetaryImpactSummary | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadData();
  }, [period]);

  async function loadData() {
    setLoading(true);
    setError(null);
    try {
      // Call API route instead of direct function (for client-side compatibility)
      const response = await fetch(`/api/planetary-impact?period=${period}`);
      if (!response.ok) {
        throw new Error(`Failed to fetch: ${response.statusText}`);
      }
      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load data');
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
        <div className="flex items-center justify-center h-64">
          <div className="text-slate-400">Loading planetary impact analysis...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
        <div className="text-red-400">Error: {error}</div>
      </div>
    );
  }

  if (!data || data.total_events === 0) {
    return (
      <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
        <h3 className="text-xl font-semibold mb-4">🔮 Planetary Impact Analysis</h3>
        <div className="text-slate-400 text-center py-8">
          No events found for the selected period.
        </div>
      </div>
    );
  }

  // Prepare data for charts (top 12 houses, all planets)
  const houseChartData = data.house_impacts
    .filter(h => h.event_count > 0)
    .map(h => ({
      name: `H${h.house_number}`,
      fullName: h.house_name,
      count: h.event_count,
    }));

  const planetChartData = data.planet_impacts.map(p => ({
    name: p.planet_name,
    count: p.event_count,
    aspects: p.aspect_count,
  }));

  return (
    <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700 space-y-6">
      {/* Header with period selector */}
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-xl font-semibold mb-2">🔮 Planetary Impact Analysis</h3>
          <p className="text-sm text-slate-400">
            {format(new Date(data.start_date), 'MMM dd')} - {format(new Date(data.end_date), 'MMM dd, yyyy')}
            {' '}• {data.total_events} events
          </p>
        </div>
        <div className="flex gap-2">
          {(['day', 'week', 'month'] as const).map((p) => (
            <button
              key={p}
              onClick={() => setPeriod(p)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                period === p
                  ? 'bg-purple-600 text-white'
                  : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
              }`}
            >
              {p.charAt(0).toUpperCase() + p.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* House Impact Bar Chart */}
        <div className="bg-slate-900/50 p-4 rounded-lg">
          <h4 className="text-lg font-semibold mb-4 text-center">Events by House (1-12)</h4>
          {houseChartData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={houseChartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis 
                  dataKey="name" 
                  stroke="#9CA3AF"
                  fontSize={12}
                />
                <YAxis 
                  stroke="#9CA3AF"
                  fontSize={12}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1F2937',
                    border: '1px solid #374151',
                    borderRadius: '8px',
                  }}
                  formatter={(value: number, payload: any) => {
                    const data = payload[0]?.payload;
                    return [
                      `${value} events`,
                      data?.fullName || ''
                    ];
                  }}
                  labelStyle={{ color: '#E5E7EB' }}
                />
                <Bar 
                  dataKey="count" 
                  fill="#8884d8"
                  radius={[8, 8, 0, 0]}
                >
                  {houseChartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={HOUSE_COLORS[index % HOUSE_COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="text-center text-slate-400 py-12">No house data available</div>
          )}
        </div>

        {/* Planet Impact Bar Chart */}
        <div className="bg-slate-900/50 p-4 rounded-lg">
          <h4 className="text-lg font-semibold mb-4 text-center">Events by Planet</h4>
          {planetChartData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={planetChartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis 
                  dataKey="name" 
                  stroke="#9CA3AF"
                  fontSize={12}
                />
                <YAxis 
                  stroke="#9CA3AF"
                  fontSize={12}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1F2937',
                    border: '1px solid #374151',
                    borderRadius: '8px',
                  }}
                  formatter={(value: number, payload: any) => {
                    const data = payload[0]?.payload;
                    return [
                      `${value} events`,
                      `Aspects: ${data?.aspects || 0}`
                    ];
                  }}
                  labelStyle={{ color: '#E5E7EB' }}
                />
                <Bar 
                  dataKey="count" 
                  radius={[8, 8, 0, 0]}
                >
                  {planetChartData.map((entry) => (
                    <Cell 
                      key={`cell-${entry.name}`} 
                      fill={PLANET_COLORS[entry.name] || '#8884d8'} 
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="text-center text-slate-400 py-12">No planet data available</div>
          )}
        </div>
      </div>

      {/* Summary Tables */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        {/* Top Houses Table */}
        <div className="bg-slate-900/50 p-4 rounded-lg">
          <h4 className="text-lg font-semibold mb-4">Top Houses (Event Count)</h4>
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {data.house_impacts
              .filter(h => h.event_count > 0)
              .slice(0, 6)
              .map((house) => (
                <div
                  key={house.house_number}
                  className="flex justify-between items-center p-2 bg-slate-800/50 rounded"
                >
                  <div className="flex-1">
                    <div className="font-medium text-slate-200">
                      House {house.house_number}: {house.house_name}
                    </div>
                    <div className="text-xs text-slate-400 mt-1">
                      {house.significations.slice(0, 2).join(', ')}
                    </div>
                  </div>
                  <div className="text-lg font-bold text-purple-400 ml-4">
                    {house.event_count}
                  </div>
                </div>
              ))}
            {data.house_impacts.filter(h => h.event_count > 0).length === 0 && (
              <div className="text-center text-slate-400 py-4">No house data available</div>
            )}
          </div>
        </div>

        {/* Top Planets Table */}
        <div className="bg-slate-900/50 p-4 rounded-lg">
          <h4 className="text-lg font-semibold mb-4">Top Planets (Event Count)</h4>
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {data.planet_impacts.slice(0, 9).map((planet) => (
              <div
                key={planet.planet_name}
                className="flex justify-between items-center p-2 bg-slate-800/50 rounded"
              >
                <div className="flex-1">
                  <div className="font-medium text-slate-200">{planet.planet_name}</div>
                  <div className="text-xs text-slate-400 mt-1">
                    {planet.aspect_count} aspects • Avg strength: {planet.avg_aspect_strength.toFixed(1)}
                  </div>
                </div>
                <div className="text-lg font-bold text-purple-400 ml-4">
                  {planet.event_count}
                </div>
              </div>
            ))}
            {data.planet_impacts.length === 0 && (
              <div className="text-center text-slate-400 py-4">No planet data available</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

