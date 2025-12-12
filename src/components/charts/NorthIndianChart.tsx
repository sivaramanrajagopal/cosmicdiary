'use client';

import { useState } from 'react';
import { ChartData, ChartPlanet } from './chart-types';
import { PLANET_COLORS, PLANET_ABBREVIATIONS } from './chart-colors';
import { getPlanetsInHouse } from './chart-utils';
import PlanetDetailsModal from './PlanetDetailsModal';

interface NorthIndianChartProps {
  chartData: ChartData;
  onPlanetClick?: (planet: ChartPlanet) => void;
}

/**
 * North Indian Chart Component
 * 
 * Displays astrological chart in diamond/square layout with 12 houses.
 * House 1 (ascendant) is at the top, with houses arranged in a diamond pattern.
 */
export default function NorthIndianChart({ chartData, onPlanetClick }: NorthIndianChartProps) {
  const [selectedPlanet, setSelectedPlanet] = useState<ChartPlanet | null>(null);
  const [hoveredHouse, setHoveredHouse] = useState<number | null>(null);

  // Calculate house positions (diamond layout)
  // House positions are relative percentages
  const getHousePosition = (houseNumber: number): React.CSSProperties => {
    const positions: Record<number, React.CSSProperties> = {
      1: { top: 0, left: '50%', transform: 'translateX(-50%)' },           // House 1 (top)
      2: { top: '8%', right: '8%', transform: 'translate(50%, -50%)' },    // House 2
      3: { top: '25%', right: 0, transform: 'translateY(-50%)' },          // House 3
      4: { top: '42%', right: '8%', transform: 'translate(50%, -50%)' },   // House 4
      5: { top: '50%', right: '25%', transform: 'translate(50%, -50%)' },  // House 5
      6: { bottom: '25%', right: '25%', transform: 'translate(50%, 50%)' }, // House 6
      7: { bottom: 0, left: '50%', transform: 'translateX(-50%)' },         // House 7 (bottom)
      8: { bottom: '25%', left: '25%', transform: 'translate(-50%, 50%)' }, // House 8
      9: { top: '50%', left: '25%', transform: 'translate(-50%, -50%)' },   // House 9
      10: { top: '42%', left: '8%', transform: 'translate(-50%, -50%)' },   // House 10
      11: { top: '25%', left: 0, transform: 'translateY(-50%)' },           // House 11
      12: { top: '8%', left: '8%', transform: 'translate(-50%, -50%)' },    // House 12
    };
    return positions[houseNumber] || { top: 0, left: 0 };
  };

  const handlePlanetClick = (planet: ChartPlanet) => {
    setSelectedPlanet(planet);
    onPlanetClick?.(planet);
  };

  return (
    <div className="relative w-full aspect-square max-w-2xl mx-auto">
      {/* Chart Container */}
      <div className="relative w-full h-full border-2 border-purple-500 rounded-lg bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
        {/* Render 12 Houses */}
        {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12].map((houseNum) => {
          const position = getHousePosition(houseNum);
          const planets = getPlanetsInHouse(chartData, houseNum);
          const isAscendant = houseNum === 1;
          const isDustana = houseNum === 6 || houseNum === 8 || houseNum === 12;
          
          return (
            <div
              key={houseNum}
              className={`absolute p-2 min-w-[80px] border rounded transition-all cursor-pointer ${
                isAscendant
                  ? 'bg-purple-900/70 border-purple-400 shadow-lg shadow-purple-500/50'
                  : isDustana
                  ? 'bg-red-900/30 border-red-700/50'
                  : houseNum % 2 === 0
                  ? 'bg-slate-700/50 border-slate-600'
                  : 'bg-slate-800/50 border-slate-700'
              } ${hoveredHouse === houseNum ? 'ring-2 ring-purple-400 scale-105 z-10' : ''}`}
              style={position}
              onMouseEnter={() => setHoveredHouse(houseNum)}
              onMouseLeave={() => setHoveredHouse(null)}
              title={`House ${houseNum}`}
            >
              {/* House Number */}
              <div className="text-xs font-bold text-purple-300 mb-1 text-center">
                {houseNum}
              </div>
              
              {/* Ascendant Marker */}
              {isAscendant && (
                <div className="text-xs text-purple-400 mb-1 text-center font-semibold">
                  ↑ Lagna
                </div>
              )}
              
              {/* Planets in House */}
              <div className="flex flex-wrap gap-1 justify-center">
                {planets.length > 0 ? (
                  planets.map((planet) => (
                    <button
                      key={planet.name}
                      onClick={(e) => {
                        e.stopPropagation();
                        handlePlanetClick(planet);
                      }}
                      className="px-1.5 py-0.5 rounded text-xs font-medium hover:ring-2 hover:ring-white transition-all shadow-sm"
                      style={{ backgroundColor: PLANET_COLORS[planet.name] }}
                      title={`${planet.name} in ${planet.rasi.name} (House ${planet.house})`}
                    >
                      {PLANET_ABBREVIATIONS[planet.name]}
                      {planet.isRetrograde && (
                        <span className="text-red-400 ml-0.5 font-bold">R</span>
                      )}
                    </button>
                  ))
                ) : (
                  <span className="text-xs text-slate-500 italic">Empty</span>
                )}
              </div>
              
              {/* House Cusp Degree (optional, smaller text) */}
              <div className="text-xs text-slate-500 mt-1 text-center">
                {chartData.houseCusps[houseNum - 1]?.toFixed(1)}°
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

