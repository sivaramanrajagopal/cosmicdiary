'use client';

import { useState, useEffect } from 'react';
import { ChartData } from './chart-types';
import { PLANET_COLORS, PLANET_ABBREVIATIONS } from './chart-colors';
import NorthIndianChart from './NorthIndianChart';
import SouthIndianChart from './SouthIndianChart';
import PlanetaryStrengthPanel from './PlanetaryStrengthPanel';

interface ChartContainerProps {
  chartData: ChartData;
  eventId: number;
  eventDate: string;
}

type ChartType = 'north' | 'south';

/**
 * Chart Container Component
 * 
 * Main container for displaying astrological charts with tab switching,
 * legend, and controls for export/print.
 */
export default function ChartContainer({ chartData, eventId, eventDate }: ChartContainerProps) {
  const [chartType, setChartType] = useState<ChartType>('north');
  const [showStrengthPanel, setShowStrengthPanel] = useState(false);

  // Load preference from localStorage
  useEffect(() => {
    const saved = localStorage.getItem('preferredChartType') as ChartType;
    if (saved && (saved === 'north' || saved === 'south')) {
      setChartType(saved);
    }
  }, []);

  // Save preference to localStorage
  const handleChartTypeChange = (type: ChartType) => {
    setChartType(type);
    localStorage.setItem('preferredChartType', type);
  };

  const handleExportChart = () => {
    // TODO: Implement export functionality using html2canvas or similar
    alert('Chart export functionality coming soon!');
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="space-y-4">
      {/* Tab Switcher */}
      <div className="flex gap-2 border-b border-slate-700">
        <button
          onClick={() => handleChartTypeChange('north')}
          className={`px-6 py-3 font-medium transition-colors relative ${
            chartType === 'north'
              ? 'text-purple-400'
              : 'text-slate-400 hover:text-slate-300'
          }`}
        >
          North Indian
          {chartType === 'north' && (
            <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-purple-500" />
          )}
        </button>
        <button
          onClick={() => handleChartTypeChange('south')}
          className={`px-6 py-3 font-medium transition-colors relative ${
            chartType === 'south'
              ? 'text-purple-400'
              : 'text-slate-400 hover:text-slate-300'
          }`}
        >
          South Indian
          {chartType === 'south' && (
            <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-purple-500" />
          )}
        </button>
      </div>

      {/* Chart Display */}
      <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700 print:border-0 print:bg-white">
        {chartType === 'north' ? (
          <NorthIndianChart chartData={chartData} />
        ) : (
          <SouthIndianChart chartData={chartData} eventDate={eventDate} />
        )}
      </div>

      {/* Legend & Controls */}
      <div className="flex flex-wrap gap-4 items-center justify-between bg-slate-800/50 p-4 rounded-lg border border-slate-700 print:hidden">
        {/* Planet Legend */}
        <div className="flex flex-wrap gap-3">
          <span className="text-sm text-slate-400 font-medium">Planets:</span>
          {chartData.planets.map((planet) => (
            <div key={planet.name} className="flex items-center gap-2 text-sm">
              <div
                className="w-5 h-5 rounded shadow-sm"
                style={{ backgroundColor: PLANET_COLORS[planet.name] }}
              />
              <span className="text-slate-300 font-medium">{PLANET_ABBREVIATIONS[planet.name]}</span>
              <span className="text-slate-500">({planet.name})</span>
            </div>
          ))}
        </div>

        {/* Action Buttons */}
        <div className="flex gap-2">
          <button
            onClick={() => setShowStrengthPanel(!showStrengthPanel)}
            className="px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg transition-colors text-sm font-medium"
          >
            {showStrengthPanel ? 'Hide' : 'Show'} Strength Panel
          </button>
          <button
            onClick={handleExportChart}
            className="px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg transition-colors text-sm font-medium"
          >
            Export Chart
          </button>
          <button
            onClick={handlePrint}
            className="px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg transition-colors text-sm font-medium"
          >
            Print
          </button>
        </div>
      </div>

      {/* Planetary Strength Panel */}
      {showStrengthPanel && (
        <PlanetaryStrengthPanel planets={chartData.planets} />
      )}

      {/* Chart Info */}
      <div className="bg-slate-900/50 p-3 rounded-lg border border-slate-700 text-xs text-slate-400">
        <div className="flex flex-wrap gap-4">
          <span>House System: <span className="text-slate-300">{chartData.houseSystem}</span></span>
          <span>Ascendant: <span className="text-slate-300">{chartData.ascendant.rasi} ({chartData.ascendant.degree.toFixed(2)}°)</span></span>
          <span>Ayanamsa: <span className="text-slate-300">Lahiri ({chartData.ayanamsa.toFixed(4)}°)</span></span>
          <span>Event Date: <span className="text-slate-300">{eventDate}</span></span>
        </div>
      </div>
    </div>
  );
}

