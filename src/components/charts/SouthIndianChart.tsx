'use client';

import { useState } from 'react';
import { ChartData, ChartPlanet } from './chart-types';
import { PLANET_COLORS, PLANET_ABBREVIATIONS } from './chart-colors';
import { getPlanetsInRasi } from './chart-utils';
import PlanetDetailsModal from './PlanetDetailsModal';

interface SouthIndianChartProps {
  chartData: ChartData;
  eventDate?: string;
  onPlanetClick?: (planet: ChartPlanet) => void;
}

// Rasi names (English and Tamil if needed)
const RASI_NAMES: Record<number, { english: string; tamil?: string }> = {
  1: { english: 'Aries', tamil: 'Mesham' },
  2: { english: 'Taurus', tamil: 'Rishabam' },
  3: { english: 'Gemini', tamil: 'Mithunam' },
  4: { english: 'Cancer', tamil: 'Kadagam' },
  5: { english: 'Leo', tamil: 'Simham' },
  6: { english: 'Virgo', tamil: 'Kanni' },
  7: { english: 'Libra', tamil: 'Thulam' },
  8: { english: 'Scorpio', tamil: 'Vrischikam' },
  9: { english: 'Sagittarius', tamil: 'Dhanusu' },
  10: { english: 'Capricorn', tamil: 'Makaram' },
  11: { english: 'Aquarius', tamil: 'Kumbam' },
  12: { english: 'Pisces', tamil: 'Meenam' },
};

// Planet symbols removed - using PLANET_ABBREVIATIONS instead (same as North Indian chart)

/**
 * Get rashi number from rasi name (1-12)
 */
function getRashiNumber(rasiName: string): number {
  const entry = Object.entries(RASI_NAMES).find(
    ([_, value]) => value.english.toLowerCase() === rasiName.toLowerCase()
  );
  return entry ? parseInt(entry[0]) : 0;
}

/**
 * South Indian Chart Component
 * 
 * Based on the existing Gocharam implementation with 4x4 grid layout:
 * - Row 1: 12, 1, 2, 3
 * - Row 2: 11, CENTER (2x2), 4
 * - Row 3: 10, (CENTER CONTINUES), 5
 * - Row 4: 9, 8, 7, 6
 */
export default function SouthIndianChart({ chartData, eventDate, onPlanetClick }: SouthIndianChartProps) {
  const [selectedPlanet, setSelectedPlanet] = useState<ChartPlanet | null>(null);

  // Group planets by rashi number
  const planetsByRashi: Record<number, ChartPlanet[]> = {};
  chartData.planets.forEach(planet => {
    const rashiNum = planet.rasi.number;
    if (!planetsByRashi[rashiNum]) {
      planetsByRashi[rashiNum] = [];
    }
    planetsByRashi[rashiNum].push(planet);
  });

  // Find Lagna (Ascendant) position
  const lagnaRashi = chartData.ascendant.rasiNumber;

  // Get planet color based on type and status
  const getPlanetColor = (planet: ChartPlanet) => {
    if (planet.name === 'Rahu' || planet.name === 'Ketu') return 'text-purple-700 font-bold';
    if (planet.isRetrograde) return 'text-blue-600 font-bold';
    return 'text-gray-800 font-semibold';
  };

  // Get degree display for planet (within sign: 0-30 degrees)
  const getDegreeDisplay = (planet: ChartPlanet): string => {
    const degreeInSign = planet.longitude % 30;
    return `${degreeInSign.toFixed(1)}°`;
  };

  // Get nakshatra display
  const getNakshatraDisplay = (planet: ChartPlanet): string => {
    if (!planet.nakshatra.name) return '';
    const shortName = planet.nakshatra.name.substring(0, 3);
    const pada = planet.nakshatra.pada || 1;
    return `${shortName}-${pada}`;
  };

  // Helper function to get house colors
  const getHouseColor = (houseNum: number): string => {
    const colors: Record<number, string> = {
      1: 'border-red-400 bg-red-50',
      2: 'border-green-400 bg-green-50',
      3: 'border-blue-400 bg-blue-50',
      4: 'border-pink-400 bg-pink-50',
      5: 'border-emerald-400 bg-emerald-50',
      6: 'border-rose-400 bg-rose-50',
      7: 'border-teal-400 bg-teal-50',
      8: 'border-gray-400 bg-gray-50',
      9: 'border-yellow-400 bg-yellow-50',
      10: 'border-indigo-400 bg-indigo-50',
      11: 'border-purple-400 bg-purple-50',
      12: 'border-orange-400 bg-orange-50',
    };
    return colors[houseNum] || 'border-gray-300 bg-gray-50';
  };

  // Helper function to get Lagna highlight (rashiNum is the rashi number, not house number)
  const getLagnaHighlight = (rashiNum: number): string => {
    return lagnaRashi === rashiNum ? 'ring-4 ring-yellow-400 ring-opacity-70' : '';
  };

  // Get house number for a rashi based on ascendant
  const getHouseForRashi = (rashiNum: number): number => {
    // If ascendant is in rasi X, then that rasi is house 1
    // So rasi at index Y is house ((Y - X + 1 + 12) % 12) || 12
    if (!lagnaRashi) return rashiNum; // Fallback if no ascendant
    const houseNum = ((rashiNum - lagnaRashi + 1 + 12) % 12) || 12;
    return houseNum;
  };

  // Render planets in a house box
  const renderPlanets = (rashiNumber: number) => {
    const planets = planetsByRashi[rashiNumber] || [];
    if (planets.length === 0) return null;

    return (
      <div className="flex flex-col gap-1 mt-2">
        {planets.map((planet) => (
          <button
            key={planet.name}
            onClick={(e) => {
              e.stopPropagation();
              setSelectedPlanet(planet);
              onPlanetClick?.(planet);
            }}
            className={`planet-entry text-xs ${getPlanetColor(planet)} border rounded px-1 py-0.5 bg-white bg-opacity-80 hover:bg-opacity-100 hover:ring-2 hover:ring-purple-400 transition-all cursor-pointer text-left w-full`}
            title={`${planet.name} ${planet.isRetrograde ? '(Retrograde)' : ''} - ${planet.rasi.name} - ${getNakshatraDisplay(planet)}`}
          >
            <div className="flex items-center justify-between gap-1">
              <span className="font-bold">
                {PLANET_ABBREVIATIONS[planet.name] || planet.name}
                {planet.isRetrograde && <span className="text-blue-600 ml-1">R</span>}
              </span>
              <span className="text-xs font-mono">
                {getDegreeDisplay(planet)}
              </span>
            </div>
            {/* Show nakshatra info */}
            <div className="text-xs text-gray-600 leading-tight">
              {getNakshatraDisplay(planet)}
            </div>
          </button>
        ))}
      </div>
    );
  };

  // Render individual house box
  // Note: houseNum parameter here is actually the rashi number (1-12)
  // We use it to render the box for that rashi, then calculate the actual house number
  const renderHouseBox = (rashiNum: number) => {
    const rashiData = RASI_NAMES[rashiNum];
    if (!rashiData) return null;

    const actualHouseNum = getHouseForRashi(rashiNum);

    return (
      <div
        className={`border-2 chart-box min-h-24 p-2 relative rounded-lg ${getHouseColor(actualHouseNum)} ${getLagnaHighlight(rashiNum)}`}
      >
        {/* Lagna indicator */}
        {lagnaRashi === rashiNum && (
          <div className="absolute top-0 right-0 bg-yellow-500 text-white text-xs px-1 rounded-bl font-bold z-10">
            Lagna ↑
          </div>
        )}

        <div className="text-xs text-center font-bold mb-1">{actualHouseNum}</div>
        <div className="text-sm text-center font-bold mb-1 text-gray-800">
          {rashiData.tamil || rashiData.english}
        </div>
        {renderPlanets(rashiNum)}
      </div>
    );
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 mb-6 border border-yellow-200">
      <h2 className="text-xl font-bold mb-4 text-indigo-800 text-center">
        D1 Rasi Chart – South Indian Style
      </h2>

      {/* South Indian Chart Layout - 4x4 Grid */}
      <div className="max-w-4xl mx-auto mb-6">
        <div className="grid grid-cols-4 gap-2">
          {/* Row 1: 12, 1, 2, 3 */}
          {renderHouseBox(12)} {/* Meenam (Pisces) */}
          {renderHouseBox(1)}  {/* Mesham (Aries) */}
          {renderHouseBox(2)}  {/* Rishabam (Taurus) */}
          {renderHouseBox(3)}  {/* Mithunam (Gemini) */}

          {/* Row 2: 11, CENTER (2x2), 4 */}
          {renderHouseBox(11)} {/* Kumbam (Aquarius) */}

          {/* Center section spanning 2x2 */}
          <div className="col-span-2 row-span-2 border-4 border-indigo-500 bg-gradient-to-br from-yellow-100 to-orange-100 flex items-center justify-center rounded-lg">
            <div className="text-center">
              <div className="text-lg font-bold text-indigo-800">
                {chartData.ascendant.rasi}
              </div>
              <div className="text-sm text-indigo-600 mt-1">
                {eventDate || new Date().toLocaleDateString()}
              </div>
              <div className="text-xs text-indigo-500 mt-1">
                Lagna: {chartData.ascendant.degree.toFixed(2)}°
              </div>
              <div className="text-xs text-indigo-400 mt-1">
                {chartData.ascendant.lord}
              </div>
            </div>
          </div>

          {renderHouseBox(4)}  {/* Kadagam (Cancer) */}

          {/* Row 3: 10, (CENTER CONTINUES), 5 */}
          {renderHouseBox(10)} {/* Makaram (Capricorn) */}
          {/* Center continues from above */}
          {renderHouseBox(5)}  {/* Simham (Leo) */}

          {/* Row 4: 9, 8, 7, 6 */}
          {renderHouseBox(9)}  {/* Dhanusu (Sagittarius) */}
          {renderHouseBox(8)}  {/* Vrischikam (Scorpio) */}
          {renderHouseBox(7)}  {/* Thulam (Libra) */}
          {renderHouseBox(6)}  {/* Kanni (Virgo) */}
        </div>
      </div>

      {/* Comprehensive Information Sections */}
      <div className="space-y-4">
        {/* Planet Abbreviations Legend */}
        <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
          <h3 className="font-medium text-sm mb-3 text-center text-gray-800">Planet Names</h3>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-2 text-xs">
            {Object.entries(PLANET_ABBREVIATIONS).map(([name, abbreviation]) => (
              <div key={name} className="flex items-center justify-center gap-1">
                <span className="font-bold">{abbreviation}</span>
                <span className="text-gray-700">{name}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Retrograde Explanation */}
        <div className="bg-purple-50 p-4 rounded-lg border border-purple-200">
          <h3 className="font-medium text-sm mb-2 text-purple-800">Retrograde (℞) Explanation</h3>
          <div className="text-xs text-purple-700 leading-relaxed space-y-2">
            <p>
              <strong>Retrograde</strong> (R) means the planet appears to move backward in the sky from Earth&apos;s view.
              During this period, the planet&apos;s energy is internalized or reversed.
            </p>
            <ul className="list-disc list-inside space-y-1 ml-2">
              <li><strong>Mercury R</strong> can bring communication or travel delays.</li>
              <li><strong>Saturn R</strong> can create karmic tests or delays in structure and discipline.</li>
              <li><strong>Venus R</strong> may cause relationship reassessments or value changes.</li>
              <li><strong>Jupiter R</strong> encourages inner wisdom development and spiritual growth.</li>
              <li><strong>Mars R</strong> redirects energy inward, requiring patience in actions.</li>
            </ul>
            <p className="font-medium">
              Use this phase for <strong>reflection, revision, and deeper learning</strong> in that planet&apos;s domain.
            </p>
          </div>
        </div>

        {/* Degree Significance */}
        <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
          <h3 className="font-medium text-sm mb-2 text-blue-800">Planet Degree Significance</h3>
          <p className="text-xs text-blue-700 leading-relaxed">
            <strong>Planet degrees</strong> indicate the exact position within a sign (0° to 29°59&apos;).
            This helps identify planetary strength, conjunctions, and aspects with other planets.
            Early degrees (0-10°) show new energy, middle degrees (10-20°) show peak strength,
            and late degrees (20-30°) show completion energy.
          </p>
        </div>

        {/* Lagna Information */}
        <div className="bg-amber-50 p-4 rounded-lg border border-amber-200">
          <h3 className="font-medium text-sm mb-2 text-amber-800">Lagna (Ascendant) Information</h3>
          <p className="text-xs text-amber-700 leading-relaxed">
            The <strong>Lagna ↑</strong> marking shows your rising sign at the event time.
            It&apos;s highlighted with a yellow ring and &quot;Lagna ↑&quot; label. The Lagna determines
            the personality, physical appearance, and overall approach for the event. It&apos;s the most
            important reference point in Vedic astrology chart interpretation.
          </p>
        </div>
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
