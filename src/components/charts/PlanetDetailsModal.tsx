'use client';

import { ChartData, ChartPlanet } from './chart-types';
import { PLANET_COLORS, PLANET_ABBREVIATIONS, STRENGTH_COLORS } from './chart-colors';
import { formatDegreesToDMS } from './chart-utils';

interface PlanetDetailsModalProps {
  planet: ChartPlanet;
  chartData: ChartData;
  onClose: () => void;
}

/**
 * Planet Details Modal Component
 * 
 * Displays detailed information about a planet when clicked in the chart.
 */
export default function PlanetDetailsModal({ planet, chartData, onClose }: PlanetDetailsModalProps) {
  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div
      className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4"
      onClick={handleBackdropClick}
    >
      <div className="bg-slate-800 rounded-lg border-2 border-purple-500 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div
          className="p-4 border-b border-slate-700 flex items-center justify-between"
          style={{ backgroundColor: `${PLANET_COLORS[planet.name]}20` }}
        >
          <div className="flex items-center gap-3">
            <div
              className="w-12 h-12 rounded-full flex items-center justify-center font-bold text-white shadow-lg"
              style={{ backgroundColor: PLANET_COLORS[planet.name] }}
            >
              {PLANET_ABBREVIATIONS[planet.name]}
            </div>
            <div>
              <h3 className="text-xl font-bold text-white">{planet.name}</h3>
              <p className="text-sm text-slate-400">
                {planet.isRetrograde && '⚠️ Retrograde • '}
                House {planet.house}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white text-2xl font-bold w-8 h-8 flex items-center justify-center rounded hover:bg-slate-700 transition-colors"
          >
            ×
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Position Information */}
          <div>
            <h4 className="text-lg font-semibold text-purple-300 mb-3">Position</h4>
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-slate-900/50 p-3 rounded">
                <div className="text-sm text-slate-400">Longitude</div>
                <div className="text-lg font-mono text-white">
                  {formatDegreesToDMS(planet.longitude)}
                </div>
                <div className="text-xs text-slate-500 mt-1">
                  {planet.longitude.toFixed(4)}°
                </div>
              </div>
              <div className="bg-slate-900/50 p-3 rounded">
                <div className="text-sm text-slate-400">Latitude</div>
                <div className="text-lg font-mono text-white">
                  {planet.latitude.toFixed(4)}°
                </div>
              </div>
            </div>
          </div>

          {/* Rasi Information */}
          <div>
            <h4 className="text-lg font-semibold text-purple-300 mb-3">Rasi (Zodiac Sign)</h4>
            <div className="bg-slate-900/50 p-4 rounded">
              <div className="flex items-center justify-between mb-2">
                <div>
                  <div className="text-xl font-bold text-white">{planet.rasi.name}</div>
                  <div className="text-sm text-slate-400">Rasi #{planet.rasi.number}</div>
                </div>
                <div className="text-right">
                  <div className="text-sm text-slate-400">Lord</div>
                  <div className="text-lg font-semibold text-purple-300">{planet.rasi.lord}</div>
                </div>
              </div>
            </div>
          </div>

          {/* Nakshatra Information */}
          <div>
            <h4 className="text-lg font-semibold text-purple-300 mb-3">Nakshatra (Lunar Mansion)</h4>
            <div className="bg-slate-900/50 p-4 rounded">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-xl font-bold text-white">{planet.nakshatra.name}</div>
                  <div className="text-sm text-slate-400">Nakshatra #{planet.nakshatra.number}</div>
                </div>
                <div className="text-right">
                  <div className="text-sm text-slate-400">Pada</div>
                  <div className="text-lg font-semibold text-purple-300">{planet.nakshatra.pada}</div>
                </div>
              </div>
            </div>
          </div>

          {/* House Placement */}
          <div>
            <h4 className="text-lg font-semibold text-purple-300 mb-3">House Placement</h4>
            <div className="bg-slate-900/50 p-4 rounded">
              <div className="text-2xl font-bold text-white mb-1">
                House {planet.house}
              </div>
              <div className="text-sm text-slate-400">
                Based on ascendant: {chartData.ascendant.rasi}
              </div>
            </div>
          </div>

          {/* Strength Indicators */}
          <div>
            <h4 className="text-lg font-semibold text-purple-300 mb-3">Planetary Strength</h4>
            <div className="space-y-2">
              <div className="flex items-center justify-between bg-slate-900/50 p-3 rounded">
                <span className="text-slate-300">Strength Score</span>
                <div className="flex items-center gap-2">
                  <div className="w-32 h-2 bg-slate-700 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-purple-500 to-pink-500"
                      style={{ width: `${planet.strength.strengthScore * 100}%` }}
                    />
                  </div>
                  <span className="text-white font-semibold w-12 text-right">
                    {(planet.strength.strengthScore * 100).toFixed(0)}%
                  </span>
                </div>
              </div>

              {/* Status Badges */}
              <div className="flex flex-wrap gap-2 mt-3">
                {planet.strength.exalted && (
                  <span className={`px-3 py-1 rounded text-sm font-medium ${STRENGTH_COLORS.exalted}`}>
                    🌟 Exalted
                  </span>
                )}
                {planet.strength.debilitated && (
                  <span className={`px-3 py-1 rounded text-sm font-medium ${STRENGTH_COLORS.debilitated}`}>
                    🔻 Debilitated
                  </span>
                )}
                {planet.strength.ownSign && (
                  <span className={`px-3 py-1 rounded text-sm font-medium ${STRENGTH_COLORS.ownSign}`}>
                    🏠 Own Sign
                  </span>
                )}
                {planet.strength.digBala && (
                  <span className={`px-3 py-1 rounded text-sm font-medium ${STRENGTH_COLORS.digBala}`}>
                    💪 Dig Bala
                  </span>
                )}
                {planet.strength.combusted && (
                  <span className={`px-3 py-1 rounded text-sm font-medium ${STRENGTH_COLORS.combusted}`}>
                    🔥 Combusted
                  </span>
                )}
                {planet.isRetrograde && (
                  <span className="px-3 py-1 rounded text-sm font-medium bg-red-900/30 text-red-400">
                    ⚠️ Retrograde
                  </span>
                )}
                {!planet.strength.exalted && !planet.strength.debilitated && 
                 !planet.strength.ownSign && !planet.strength.digBala && 
                 !planet.strength.combusted && !planet.isRetrograde && (
                  <span className={`px-3 py-1 rounded text-sm font-medium ${STRENGTH_COLORS.neutral}`}>
                    Neutral
                  </span>
                )}
              </div>
            </div>
          </div>

          {/* Speed Information */}
          {planet.speed !== undefined && (
            <div>
              <h4 className="text-lg font-semibold text-purple-300 mb-3">Motion</h4>
              <div className="bg-slate-900/50 p-3 rounded">
                <div className="text-sm text-slate-400">Daily Speed</div>
                <div className="text-lg font-mono text-white">
                  {planet.speed > 0 ? '+' : ''}{planet.speed.toFixed(4)}° / day
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-slate-700 flex justify-end">
          <button
            onClick={onClose}
            className="px-6 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg transition-colors font-medium"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

