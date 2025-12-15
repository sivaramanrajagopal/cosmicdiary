'use client';

import { useState } from 'react';
import { ChartPlanet } from './chart-types';
import { PLANET_COLORS, PLANET_ABBREVIATIONS, STRENGTH_COLORS } from './chart-colors';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

interface PlanetaryStrengthPanelProps {
  planets: ChartPlanet[];
}

type SortOption = 'name' | 'strength' | 'house';

/**
 * Planetary Strength Panel Component
 * 
 * Displays all planets with their strength scores in a visual bar chart
 * and detailed strength indicators.
 */
export default function PlanetaryStrengthPanel({ planets }: PlanetaryStrengthPanelProps) {
  const [sortBy, setSortBy] = useState<SortOption>('strength');

  // Sort planets based on selected option
  const sortedPlanets = [...planets].sort((a, b) => {
    switch (sortBy) {
      case 'strength':
        return b.strength.strengthScore - a.strength.strengthScore;
      case 'house':
        return a.house - b.house;
      case 'name':
      default:
        return a.name.localeCompare(b.name);
    }
  });

  // Prepare data for bar chart
  const chartData = sortedPlanets.map(planet => ({
    name: PLANET_ABBREVIATIONS[planet.name],
    strength: planet.strength.strengthScore * 100,
    fullName: planet.name,
    color: PLANET_COLORS[planet.name],
  }));

  return (
    <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-semibold text-purple-300">Planetary Strength Analysis</h3>
        
        {/* Sort Options */}
        <div className="flex gap-2">
          <span className="text-sm text-slate-400 self-center">Sort by:</span>
          <button
            onClick={() => setSortBy('strength')}
            className={`px-3 py-1 rounded text-sm transition-colors ${
              sortBy === 'strength'
                ? 'bg-purple-600 text-white'
                : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
            }`}
          >
            Strength
          </button>
          <button
            onClick={() => setSortBy('house')}
            className={`px-3 py-1 rounded text-sm transition-colors ${
              sortBy === 'house'
                ? 'bg-purple-600 text-white'
                : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
            }`}
          >
            House
          </button>
          <button
            onClick={() => setSortBy('name')}
            className={`px-3 py-1 rounded text-sm transition-colors ${
              sortBy === 'name'
                ? 'bg-purple-600 text-white'
                : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
            }`}
          >
            Name
          </button>
        </div>
      </div>

      {/* Bar Chart */}
      <div className="mb-6">
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis 
              dataKey="name" 
              tick={{ fill: '#cbd5e1' }}
              stroke="#64748b"
            />
            <YAxis 
              label={{ value: 'Strength %', angle: -90, position: 'insideLeft', fill: '#cbd5e1' }}
              tick={{ fill: '#cbd5e1' }}
              stroke="#64748b"
              domain={[0, 100]}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#1e293b',
                border: '1px solid #475569',
                borderRadius: '6px',
              }}
              labelStyle={{ color: '#cbd5e1' }}
              formatter={(value: any, name?: string, props?: any) => [
                `${typeof value === 'number' ? value.toFixed(1) : '0.0'}%`,
                props?.payload?.fullName || name || '',
              ]}
            />
            <Bar dataKey="strength" radius={[4, 4, 0, 0]}>
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Detailed Planet List */}
      <div className="space-y-2">
        {sortedPlanets.map((planet) => (
          <div
            key={planet.name}
            className="bg-slate-900/50 p-4 rounded-lg border border-slate-700 hover:border-purple-500/50 transition-colors"
          >
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-3">
                <div
                  className="w-10 h-10 rounded-full flex items-center justify-center font-bold text-white shadow-md"
                  style={{ backgroundColor: PLANET_COLORS[planet.name] }}
                >
                  {PLANET_ABBREVIATIONS[planet.name]}
                </div>
                <div>
                  <div className="font-semibold text-white">{planet.name}</div>
                  <div className="text-sm text-slate-400">
                    {planet.rasi.name} • House {planet.house}
                    {planet.isRetrograde && <span className="text-red-400 ml-2">(R)</span>}
                  </div>
                </div>
              </div>

              {/* Strength Score */}
              <div className="text-right">
                <div className="text-lg font-bold text-purple-300">
                  {(planet.strength.strengthScore * 100).toFixed(0)}%
                </div>
                <div className="w-24 h-2 bg-slate-700 rounded-full overflow-hidden mt-1">
                  <div
                    className="h-full bg-gradient-to-r from-purple-500 to-pink-500"
                    style={{ width: `${planet.strength.strengthScore * 100}%` }}
                  />
                </div>
              </div>
            </div>

            {/* Status Badges */}
            <div className="flex flex-wrap gap-2 mt-3">
              {planet.strength.exalted && (
                <span className={`px-2 py-1 rounded text-xs font-medium ${STRENGTH_COLORS.exalted}`}>
                  🌟 Exalted
                </span>
              )}
              {planet.strength.debilitated && (
                <span className={`px-2 py-1 rounded text-xs font-medium ${STRENGTH_COLORS.debilitated}`}>
                  🔻 Debilitated
                </span>
              )}
              {planet.strength.ownSign && (
                <span className={`px-2 py-1 rounded text-xs font-medium ${STRENGTH_COLORS.ownSign}`}>
                  🏠 Own Sign
                </span>
              )}
              {planet.strength.digBala && (
                <span className={`px-2 py-1 rounded text-xs font-medium ${STRENGTH_COLORS.digBala}`}>
                  💪 Dig Bala
                </span>
              )}
              {planet.strength.combusted && (
                <span className={`px-2 py-1 rounded text-xs font-medium ${STRENGTH_COLORS.combusted}`}>
                  🔥 Combusted
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

