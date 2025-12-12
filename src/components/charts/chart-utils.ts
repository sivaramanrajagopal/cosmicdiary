/**
 * Utility functions for chart calculations and transformations
 */

import { ChartData, ChartPlanet, HouseInfo, RasiInfo } from './chart-types';

const RASI_NAMES = [
  'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
];

const RASI_LORDS: Record<string, string> = {
  'Aries': 'Mars',
  'Taurus': 'Venus',
  'Gemini': 'Mercury',
  'Cancer': 'Moon',
  'Leo': 'Sun',
  'Virgo': 'Mercury',
  'Libra': 'Venus',
  'Scorpio': 'Mars',
  'Sagittarius': 'Jupiter',
  'Capricorn': 'Saturn',
  'Aquarius': 'Saturn',
  'Pisces': 'Jupiter',
};

/**
 * Convert longitude (0-360 degrees) to rasi name and number
 */
export function degreesToRasi(longitude: number): { name: string; number: number; lord: string } {
  const rasiNumber = Math.floor(longitude / 30) + 1;
  const rasiIndex = rasiNumber - 1;
  const rasiName = RASI_NAMES[rasiIndex] || RASI_NAMES[0];
  return {
    name: rasiName,
    number: rasiNumber,
    lord: RASI_LORDS[rasiName] || '',
  };
}

/**
 * Get rasi name from rasi number (1-12)
 */
export function getRasiName(rasiNumber: number): string {
  if (rasiNumber < 1 || rasiNumber > 12) {
    return RASI_NAMES[0];
  }
  return RASI_NAMES[rasiNumber - 1];
}

/**
 * Get house number for a given longitude based on house cusps
 */
export function getHouseForLongitude(longitude: number, houseCusps: number[]): number {
  if (houseCusps.length !== 12) {
    return 1; // Fallback
  }

  // Normalize longitude to 0-360
  const normalizedLong = ((longitude % 360) + 360) % 360;

  for (let i = 0; i < 12; i++) {
    const currentCusp = ((houseCusps[i] % 360) + 360) % 360;
    const nextCusp = ((houseCusps[(i + 1) % 12] % 360) + 360) % 360;

    if (currentCusp <= nextCusp) {
      // Normal case (no wrap-around)
      if (normalizedLong >= currentCusp && normalizedLong < nextCusp) {
        return i + 1;
      }
    } else {
      // Wrap-around case (e.g., 350° to 10°)
      if (normalizedLong >= currentCusp || normalizedLong < nextCusp) {
        return i + 1;
      }
    }
  }

  return 1; // Fallback
}

/**
 * Get all planets in a specific house
 */
export function getPlanetsInHouse(chartData: ChartData, houseNumber: number): ChartPlanet[] {
  return chartData.planets.filter(planet => planet.house === houseNumber);
}

/**
 * Get all planets in a specific rasi
 */
export function getPlanetsInRasi(chartData: ChartData, rasiName: string): ChartPlanet[] {
  return chartData.planets.filter(planet => planet.rasi.name === rasiName);
}

/**
 * Get house information including all planets in that house
 */
export function getHouseInfo(chartData: ChartData, houseNumber: number): HouseInfo | null {
  if (houseNumber < 1 || houseNumber > 12) {
    return null;
  }

  const cuspDegree = chartData.houseCusps[houseNumber - 1];
  const rasi = degreesToRasi(cuspDegree);
  const planets = getPlanetsInHouse(chartData, houseNumber);

  return {
    number: houseNumber,
    cuspDegree,
    rasi: rasi.name,
    rasiNumber: rasi.number,
    planets,
  };
}

/**
 * Get rasi information including all planets and house number
 */
export function getRasiInfo(chartData: ChartData, rasiName: string): RasiInfo | null {
  const rasiIndex = RASI_NAMES.indexOf(rasiName);
  if (rasiIndex === -1) {
    return null;
  }

  const rasiNumber = rasiIndex + 1;
  const startDegree = rasiIndex * 30;
  const endDegree = (rasiIndex + 1) * 30;
  const planets = getPlanetsInRasi(chartData, rasiName);

  // Calculate house number based on ascendant
  const ascRasiNum = chartData.ascendant.rasiNumber;
  const houseNum = ((rasiIndex - ascRasiNum + 1 + 12) % 12) || 12;

  return {
    name: rasiName,
    number: rasiNumber,
    lord: RASI_LORDS[rasiName] || '',
    houseNumber: houseNum,
    planets,
    startDegree,
    endDegree,
  };
}

/**
 * Convert chart data from database format to ChartData format
 */
export function transformChartDataFromDB(dbData: any): ChartData {
  const planetaryPositions = typeof dbData.planetary_positions === 'string'
    ? JSON.parse(dbData.planetary_positions)
    : dbData.planetary_positions;

  const planetaryStrengths = typeof dbData.planetary_strengths === 'string'
    ? JSON.parse(dbData.planetary_strengths)
    : dbData.planetary_strengths;

  const houseCusps = Array.isArray(dbData.house_cusps)
    ? dbData.house_cusps
    : JSON.parse(dbData.house_cusps as string);

  // Transform planetary positions to ChartPlanet format
  const planets: ChartPlanet[] = Object.entries(planetaryPositions).map(([name, data]: [string, any]) => {
    const strength = planetaryStrengths[name] || {};
    const rasi = typeof data.rasi === 'string' 
      ? degreesToRasi(data.longitude)
      : data.rasi;
    
    const nakshatra = typeof data.nakshatra === 'string'
      ? { name: data.nakshatra, number: 0, pada: 0 }
      : data.nakshatra;

    return {
      name,
      abbreviation: getPlanetAbbreviation(name),
      longitude: data.longitude,
      latitude: data.latitude || 0,
      speed: data.speed || 0,
      rasi: {
        name: rasi.name || rasi,
        number: rasi.number || 0,
        lord: rasi.lord || '',
      },
      nakshatra: {
        name: nakshatra.name || '',
        number: nakshatra.number || 0,
        pada: nakshatra.pada || 0,
      },
      house: data.house || 1,
      isRetrograde: data.is_retrograde || false,
      strength: {
        exalted: strength.exalted || false,
        debilitated: strength.debilitated || false,
        ownSign: strength.own_sign || false,
        digBala: strength.dig_bala || false,
        combusted: strength.combusted || false,
        strengthScore: strength.strength_score || 0,
      },
    };
  });

  // Calculate house for each planet if not already set
  planets.forEach(planet => {
    if (!planet.house || planet.house < 1 || planet.house > 12) {
      planet.house = getHouseForLongitude(planet.longitude, houseCusps);
    }
  });

  return {
    ascendant: {
      degree: dbData.ascendant_degree,
      rasi: dbData.ascendant_rasi,
      rasiNumber: dbData.ascendant_rasi_number,
      nakshatra: dbData.ascendant_nakshatra,
      lord: dbData.ascendant_lord,
    },
    houseCusps,
    planets,
    houseSystem: dbData.house_system || 'Placidus',
    julianDay: dbData.julian_day,
    siderealTime: dbData.sidereal_time,
    ayanamsa: dbData.ayanamsa,
  };
}

/**
 * Get planet abbreviation from full name
 */
export function getPlanetAbbreviation(planetName: string): string {
  const abbreviations: Record<string, string> = {
    'Sun': 'Su',
    'Moon': 'Mo',
    'Mars': 'Ma',
    'Mercury': 'Me',
    'Jupiter': 'Ju',
    'Venus': 'Ve',
    'Saturn': 'Sa',
    'Rahu': 'Ra',
    'Ketu': 'Ke',
  };
  return abbreviations[planetName] || planetName.substring(0, 2);
}

/**
 * Format degrees to degrees, minutes, seconds
 */
export function formatDegreesToDMS(degrees: number): string {
  const deg = Math.floor(degrees);
  const minutesFloat = (degrees - deg) * 60;
  const min = Math.floor(minutesFloat);
  const sec = Math.round((minutesFloat - min) * 60);
  
  return `${deg}° ${min}' ${sec}"`;
}

/**
 * Check if a house is a dustana house (6th, 8th, or 12th)
 */
export function isDustanaHouse(houseNumber: number): boolean {
  return houseNumber === 6 || houseNumber === 8 || houseNumber === 12;
}

/**
 * Check if a house is a trine house (1st, 5th, or 9th)
 */
export function isTrineHouse(houseNumber: number): boolean {
  return houseNumber === 1 || houseNumber === 5 || houseNumber === 9;
}

/**
 * Check if a house is an angle house (1st, 4th, 7th, or 10th)
 */
export function isAngleHouse(houseNumber: number): boolean {
  return houseNumber === 1 || houseNumber === 4 || houseNumber === 7 || houseNumber === 10;
}

