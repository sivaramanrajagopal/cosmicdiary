'use client';

import { useState } from 'react';
import { ChartData, ChartPlanet } from './chart-types';
import { PLANET_COLORS, PLANET_ABBREVIATIONS, RASI_COLORS } from './chart-colors';
import { getPlanetsInRasi, getRasiInfo } from './chart-utils';
import PlanetDetailsModal from './PlanetDetailsModal';

interface SouthIndianChartProps {
  chartData: ChartData;
  onPlanetClick?: (planet: ChartPlanet) => void;
}

const RASI_ORDER = [
  'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
];

/**
 * South Indian Chart Component
 * 
 * Displays astrological chart in circular layout with fixed rasi positions.
 * Aries is at top-right, with rasis arranged clockwise around the circle.
 * House numbers are shown in each rasi based on the ascendant.
 */
export default function SouthIndianChart({ chartData, onPlanetClick }: SouthIndianChartProps) {
  const [selectedPlanet, setSelectedPlanet] = useState<ChartPlanet | null>(null);
  const [hoveredRasi, setHoveredRasi] = useState<string | null>(null);

  const handlePlanetClick = (planet: ChartPlanet) => {
    setSelectedPlanet(planet);
    onPlanetClick?.(planet);
  };

  // Calculate position for each rasi (circular layout)
  const getRasiPosition = (rasiIndex: number): React.CSSProperties => {
    const angle = (rasiIndex * 30) - 90; // Start from top (Aries = 0°, at top)
    const radius = 38; // Percentage from center
    const x = 50 + radius * Math.cos((angle * Math.PI) / 180);
    const y = 50 + radius * Math.sin((angle * Math.PI) / 180);
    return {
      left: `${x}%`,
      top: `${y}%`,
      transform: 'translate(-50%, -50%)',
    };
  };

  return (
    <div className="relative w-full aspect-square max-w-2xl mx-auto">
      {/* Outer Container */}
      <div className="relative w-full h-full border-4 border-purple-500 rounded-full bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 overflow-visible">
        {/* Center - Ascendant Info */}
        <div className="absolute inset-0 flex items-center justify-center z-10">
          <div className="text-center bg-slate-900/90 rounded-full p-4 border-2 border-purple-400 shadow-lg">
            <div className="text-lg font-bold text-purple-300 mb-1">
              {chartData.ascendant.rasi}
            </div>
            <div className="text-xs text-purple-400 mb-1">Lagna</div>
            <div className="text-xs text-slate-400">
              {chartData.ascendant.degree.toFixed(2)}°
            </div>
            <div className="text-xs text-slate-500 mt-1">
              {chartData.ascendant.lord}
            </div>
          </div>
        </div>

        {/* Render 12 Rasis */}
        {RASI_ORDER.map((rasi, index) => {
          const position = getRasiPosition(index);
          const rasiInfo = getRasiInfo(chartData, rasi);
          const planets = rasiInfo?.planets || [];
          const houseNum = rasiInfo?.houseNumber || 0;
          const isAscendant = rasi === chartData.ascendant.rasi;
          const isDustana = houseNum === 6 || houseNum === 8 || houseNum === 12;

          return (
            <div
              key={rasi}
              className={`absolute w-24 h-24 p-2 border-2 rounded-lg transform transition-all cursor-pointer ${
                isAscendant
                  ? 'bg-purple-900/70 border-purple-400 shadow-lg shadow-purple-500/50 z-20'
                  : isDustana
                  ? 'bg-red-900/30 border-red-700/50'
                  : 'bg-slate-800/70 border-slate-600'
              } ${hoveredRasi === rasi ? 'ring-2 ring-purple-400 scale-110 z-30' : ''}`}
              style={position}
              onMouseEnter={() => setHoveredRasi(rasi)}
              onMouseLeave={() => setHoveredRasi(null)}
              title={`${rasi} - House ${houseNum}`}
            >
              {/* Rasi Name */}
              <div 
                className="text-xs font-bold text-center mb-1"
                style={{ color: RASI_COLORS[rasi] || '#fff' }}
              >
                {rasi.substring(0, 4)}
              </div>

              {/* House Number */}
              <div className="text-xs text-purple-300 text-center font-semibold mb-1">
                H{houseNum}
              </div>

              {/* Planets */}
              <div className="flex flex-wrap gap-0.5 justify-center">
                {planets.length > 0 ? (
                  planets.map((planet) => (
                    <button
                      key={planet.name}
                      onClick={(e) => {
                        e.stopPropagation();
                        handlePlanetClick(planet);
                      }}
                      className="px-1 py-0.5 rounded text-xs font-medium hover:ring-2 hover:ring-white transition-all shadow-sm"
                      style={{ backgroundColor: PLANET_COLORS[planet.name] }}
                      title={`${planet.name} - ${planet.rasi.name}`}
                    >
                      {PLANET_ABBREVIATIONS[planet.name]}
                      {planet.isRetrograde && (
                        <span className="text-red-400 ml-0.5 font-bold">R</span>
                      )}
                    </button>
                  ))
                ) : (
                  <span className="text-xs text-slate-500">—</span>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Planet Details Modal */}
      {selectedPlanet && (
        <PlanetDetailsModal
          planet={selectedPlanet}
          chartData={chartData}
          onClose={() => setSelectedPlanet(null)}
        />
      )}
    </div>
  );
}

