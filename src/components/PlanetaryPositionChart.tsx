'use client';

import { Planet } from '@/lib/types';
import { PLANET_ABBREVIATIONS } from './charts/chart-colors';

interface PlanetaryPositionChartProps {
  planets: Planet[];
  selectedDate: string;
}

// Rasi names (English and Tamil)
const RASI_NAMES: Record<number, { english: string; tamil: string }> = {
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

// Nakshatra names (for display)
const NAKSHATRA_NAMES: Record<number, string> = {
  1: 'Ashwini', 2: 'Bharani', 3: 'Krittika', 4: 'Rohini', 5: 'Mrigashira',
  6: 'Ardra', 7: 'Punarvasu', 8: 'Pushya', 9: 'Ashlesha', 10: 'Magha',
  11: 'Purva Phalguni', 12: 'Uttara Phalguni', 13: 'Hasta', 14: 'Chitra',
  15: 'Swati', 16: 'Vishakha', 17: 'Anuradha', 18: 'Jyeshtha', 19: 'Mula',
  20: 'Purva Ashadha', 21: 'Uttara Ashadha', 22: 'Shravana', 23: 'Dhanishta',
  24: 'Shatabhisha', 25: 'Purva Bhadrapada', 26: 'Uttara Bhadrapada', 27: 'Revati',
};

/**
 * Get nakshatra name from number
 */
function getNakshatraName(nakshatraNum: number): string {
  return NAKSHATRA_NAMES[nakshatraNum] || `N${nakshatraNum}`;
}

/**
 * Calculate nakshatra pada from longitude
 */
function getNakshatraPada(longitude: number): number {
  // Each nakshatra is 13.33 degrees (360/27)
  const nakshatraSize = 360.0 / 27;
  const nakshatraDegree = longitude % nakshatraSize;
  const pada = Math.floor((nakshatraDegree / (nakshatraSize / 4))) + 1;
  return Math.min(pada, 4); // Ensure 1-4 range
}

/**
 * Planetary Position Chart Component
 * 
 * Simplified South Indian chart for daily planetary positions.
 * Uses Kalapurushan method (fixed rasi to house mapping: Aries=1, Taurus=2, etc.)
 * Shows short planet names instead of symbols.
 */
export default function PlanetaryPositionChart({ planets, selectedDate }: PlanetaryPositionChartProps) {
  // Group planets by rashi number (Kalapurushan: rasi number = house number)
  const planetsByRashi: Record<number, Planet[]> = {};
  
  planets.forEach(planet => {
    if (!planet.rasi || !planet.rasi.number) return;
    const rashiNum = planet.rasi.number;
    if (!planetsByRashi[rashiNum]) {
      planetsByRashi[rashiNum] = [];
    }
    planetsByRashi[rashiNum].push(planet);
  });

  // Get planet color based on type and status
  const getPlanetColor = (planet: Planet) => {
    if (planet.name === 'Rahu' || planet.name === 'Ketu') return 'text-purple-700 font-bold';
    if (planet.is_retrograde) return 'text-blue-600 font-bold';
    return 'text-gray-800 font-semibold';
  };

  // Get degree display for planet (within sign: 0-30 degrees)
  const getDegreeDisplay = (planet: Planet): string => {
    const degreeInSign = planet.longitude % 30;
    return `${degreeInSign.toFixed(1)}°`;
  };

  // Get nakshatra display
  const getNakshatraDisplay = (planet: Planet): string => {
    // Calculate nakshatra from longitude (always calculate to be accurate)
    const nakshatraNum = Math.floor((planet.longitude % 360) / (360 / 27)) + 1;
    const pada = getNakshatraPada(planet.longitude);
    const nakshatraName = getNakshatraName(nakshatraNum);
    const shortName = nakshatraName.substring(0, 3);
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

  // Render planets in a house box
  const renderPlanets = (rashiNumber: number) => {
    const planetsInRashi = planetsByRashi[rashiNumber] || [];
    if (planetsInRashi.length === 0) return null;

    return (
      <div className="flex flex-col gap-1 mt-2">
        {planetsInRashi.map((planet) => (
          <div
            key={planet.name}
            className={`planet-entry text-xs ${getPlanetColor(planet)} border rounded px-1 py-0.5 bg-white bg-opacity-80`}
            title={`${planet.name} ${planet.is_retrograde ? '(Retrograde)' : ''} - ${planet.rasi.name} - ${getNakshatraDisplay(planet)}`}
          >
            <div className="flex items-center justify-between gap-1">
              <span className="font-bold">
                {PLANET_ABBREVIATIONS[planet.name] || planet.name.substring(0, 2)}
                {planet.is_retrograde && <span className="text-blue-600 ml-1">℞</span>}
              </span>
              <span className="text-xs font-mono">
                {getDegreeDisplay(planet)}
              </span>
            </div>
            {/* Show nakshatra info */}
            <div className="text-xs text-gray-600 leading-tight">
              {getNakshatraDisplay(planet)}
            </div>
          </div>
        ))}
      </div>
    );
  };

  // Render individual house box
  // In Kalapurushan method, rasi number = house number
  const renderHouseBox = (houseNum: number) => {
    const rashiData = RASI_NAMES[houseNum];
    if (!rashiData) return null;

    return (
      <div
        className={`border-2 chart-box min-h-24 p-2 relative rounded-lg ${getHouseColor(houseNum)}`}
      >
        <div className="text-xs text-center font-bold mb-1">{houseNum}</div>
        <div className="text-sm text-center font-bold mb-1 text-gray-800">
          {rashiData.tamil || rashiData.english}
        </div>
        {renderPlanets(houseNum)}
      </div>
    );
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 mb-6 border border-yellow-200">
      <h2 className="text-xl font-bold mb-4 text-indigo-800 text-center">
        D1 Rasi Chart – South Indian Style (Kalapurushan)
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
                Gocharam
              </div>
              <div className="text-sm text-indigo-600 mt-1">
                {selectedDate || new Date().toLocaleDateString()}
              </div>
              <div className="text-xs text-indigo-500 mt-1">
                Daily Planetary Positions
              </div>
              <div className="text-xs text-indigo-400 mt-1">
                Kalapurushan Method
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

      {/* Information Sections */}
      <div className="space-y-4">
        {/* Planet Abbreviations Legend */}
        <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
          <h3 className="font-medium text-sm mb-3 text-center text-gray-800">Planet Abbreviations</h3>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-2 text-xs">
            {Object.entries(PLANET_ABBREVIATIONS).map(([name, abbrev]) => (
              <div key={name} className="flex items-center justify-center gap-1">
                <span className="font-bold text-gray-800">{abbrev}</span>
                <span className="text-gray-700">- {name}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Retrograde Explanation */}
        <div className="bg-purple-50 p-4 rounded-lg border border-purple-200">
          <h3 className="font-medium text-sm mb-2 text-purple-800">Retrograde (℞) Explanation</h3>
          <div className="text-xs text-purple-700 leading-relaxed space-y-2">
            <p>
              <strong>Retrograde</strong> (℞) means the planet appears to move backward in the sky from Earth&apos;s view.
              During this period, the planet&apos;s energy is internalized or reversed.
            </p>
          </div>
        </div>

        {/* Nakshatra Information */}
        <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
          <h3 className="font-medium text-sm mb-2 text-blue-800">Nakshatra & Pada</h3>
          <p className="text-xs text-blue-700 leading-relaxed">
            Each planet shows its <strong>Nakshatra</strong> (lunar mansion) with its <strong>Pada</strong> (quarter).
            The format is: <strong>Nak-P</strong> (e.g., &quot;Ash-1&quot; means Ashwini 1st Pada).
            Each Nakshatra has 4 Padas, each spanning 3.33 degrees.
          </p>
        </div>

        {/* Kalapurushan Method Info */}
        <div className="bg-amber-50 p-4 rounded-lg border border-amber-200">
          <h3 className="font-medium text-sm mb-2 text-amber-800">Kalapurushan Method</h3>
          <p className="text-xs text-amber-700 leading-relaxed">
            This chart uses the <strong>Kalapurushan</strong> (Sign-based) method where Aries is always House 1,
            Taurus is House 2, and so on. This is a fixed mapping system used for general planetary transit analysis.
            For event-specific charts with ascendant-based houses, use the event detail page charts.
          </p>
        </div>
      </div>
    </div>
  );
}

