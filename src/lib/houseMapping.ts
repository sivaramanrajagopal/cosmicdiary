/**
 * Traditional Vedic Astrology House Mapping & Planetary Aspects
 * Supports both Kalapurushan (Sign-based) and Ascendant-based methods
 */

import { Event, Planet, PlanetaryData, EventChartData } from './types';
import { ChartData } from '@/components/charts/chart-types';
import { getHouseForLongitude } from '@/components/charts/chart-utils';

export interface HouseMapping {
  event_id: number;
  house_number: number;  // Kalapurushan house (1-12)
  actual_house_number?: number;  // Ascendant-based house (1-12)
  calculation_method?: 'kalapurushan' | 'ascendant-based';
  rasi_name: string;
  house_significations: string[];
  mapping_reason: string;
}

export interface PlanetaryAspect {
  event_id: number;
  house_number: number;
  planet_name: string;
  aspect_type: 'conjunction' | 'drishti_3rd' | 'drishti_4th' | 'drishti_5th' | 'drishti_7th' | 'drishti_8th' | 'drishti_9th' | 'drishti_10th' | 'drishti_11th' | 'dustana';
  planet_longitude: number;
  planet_rasi: string;
  aspect_strength: 'strong' | 'moderate' | 'weak';
}

// House Significations (Kalapurushan - Sign-based)
const HOUSE_SIGNIFICATIONS: Record<number, { name: string; significations: string[] }> = {
  1: {
    name: 'Ascendant (Lagna)',
    significations: ['self', 'personality', 'body', 'health', 'reputation', 'appearance', 'ego', 'vitality'],
  },
  2: {
    name: 'Wealth (Dhana)',
    significations: ['wealth', 'family', 'speech', 'food', 'resources', 'possessions', 'savings', 'eyes'],
  },
  3: {
    name: 'Siblings (Sahaja)',
    significations: ['siblings', 'courage', 'communication', 'short journeys', 'hands', 'efforts', 'confidants'],
  },
  4: {
    name: 'Mother (Matru)',
    significations: ['mother', 'home', 'property', 'education', 'comforts', 'vehicles', 'happiness', 'land'],
  },
  5: {
    name: 'Children (Putra)',
    significations: ['children', 'creativity', 'education', 'speculation', 'intelligence', 'romance', 'mantras'],
  },
  6: {
    name: 'Enemies (Shatru)',
    significations: ['enemies', 'diseases', 'debts', 'service', 'conflicts', 'competition', 'legal issues', 'health issues'],
  },
  7: {
    name: 'Spouse (Kalatra)',
    significations: ['spouse', 'partnerships', 'business', 'marriage', 'public', 'trade', 'foreign relations'],
  },
  8: {
    name: 'Longevity (Ayush)',
    significations: ['longevity', 'transformation', 'secrets', 'sudden events', 'occult', 'inheritance', 'misfortunes'],
  },
  9: {
    name: 'Father (Pitru)',
    significations: ['father', 'dharma', 'higher education', 'long journeys', 'guru', 'philosophy', 'luck', 'religion'],
  },
  10: {
    name: 'Career (Karma)',
    significations: ['career', 'reputation', 'authority', 'profession', 'honor', 'status', 'government', 'karma'],
  },
  11: {
    name: 'Gains (Labha)',
    significations: ['gains', 'friends', 'aspirations', 'income', 'fulfillment', 'elder siblings', 'wishes'],
  },
  12: {
    name: 'Losses (Vyaya)',
    significations: ['losses', 'expenses', 'foreign lands', 'isolation', 'spirituality', 'moksha', 'hospitalization', 'imprisonment'],
  },
};

// Event Category to House Mapping (based on significations)
const EVENT_CATEGORY_TO_HOUSE: Record<string, number[]> = {
  // Health & Body
  'health': [1, 6],
  'disease': [6, 8],
  'medical': [6, 12],
  
  // Wealth & Economy
  'economic': [2, 11],
  'financial': [2, 11],
  'market': [2, 7, 11],
  'trade': [2, 7, 11],
  'wealth': [2, 11],
  
  // Conflicts & Wars
  'war': [6, 8],
  'conflict': [6, 8],
  'violence': [6, 8, 12],
  'military': [6, 10],
  
  // Natural Disasters
  'natural disaster': [6, 8, 12],
  'earthquake': [6, 8],
  'flood': [8, 12],
  'storm': [6, 8],
  
  // Relationships
  'relationship': [7],
  'marriage': [7],
  'partnership': [7],
  
  // Education & Knowledge
  'education': [4, 5, 9],
  'knowledge': [5, 9],
  'research': [5, 9],
  
  // Government & Authority
  'government': [10],
  'politics': [10],
  'authority': [10],
  'leadership': [1, 10],
  
  // Death & Transformation
  'death': [8],
  'accident': [6, 8],
  'sudden': [8],
  
  // Communication
  'communication': [3],
  'media': [3, 10],
  'news': [3, 10],
  
  // Home & Property
  'property': [4],
  'home': [4],
  'real estate': [4],
  
  // Travel & Foreign
  'travel': [3, 9, 12],
  'foreign': [7, 9, 12],
  
  // Spirituality
  'spiritual': [9, 12],
  'religion': [9],
};

// Rasi to House Number mapping (Kalapurushan)
const RASI_TO_HOUSE: Record<string, number> = {
  'Aries': 1,
  'Taurus': 2,
  'Gemini': 3,
  'Cancer': 4,
  'Leo': 5,
  'Virgo': 6,
  'Libra': 7,
  'Scorpio': 8,
  'Sagittarius': 9,
  'Capricorn': 10,
  'Aquarius': 11,
  'Pisces': 12,
};

const HOUSE_TO_RASI: Record<number, string> = {
  1: 'Aries',
  2: 'Taurus',
  3: 'Gemini',
  4: 'Cancer',
  5: 'Leo',
  6: 'Virgo',
  7: 'Libra',
  8: 'Scorpio',
  9: 'Sagittarius',
  10: 'Capricorn',
  11: 'Aquarius',
  12: 'Pisces',
};

/**
 * Map event to house based on category and significations
 */
export function mapEventToHouse(event: Event): HouseMapping {
  const category = event.category.toLowerCase();
  const eventTitle = event.title.toLowerCase();
  const eventDescription = (event.description || '').toLowerCase();
  const allText = `${category} ${eventTitle} ${eventDescription}`;
  
  // Find matching houses based on category
  let candidateHouses: number[] = [];
  
  // Check category mapping
  for (const [key, houses] of Object.entries(EVENT_CATEGORY_TO_HOUSE)) {
    if (category.includes(key) || allText.includes(key)) {
      candidateHouses.push(...houses);
    }
  }
  
  // If no match, check significations directly
  if (candidateHouses.length === 0) {
    for (const [houseNum, houseData] of Object.entries(HOUSE_SIGNIFICATIONS)) {
      const num = parseInt(houseNum);
      for (const sig of houseData.significations) {
        if (allText.includes(sig)) {
          candidateHouses.push(num);
          break;
        }
      }
    }
  }
  
  // Default house based on impact level if no match
  if (candidateHouses.length === 0) {
    if (event.impact_level === 'critical' || event.impact_level === 'high') {
      candidateHouses = [6, 8, 12]; // Dustana houses for critical events
    } else if (event.event_type === 'world') {
      candidateHouses = [10]; // Career/government for world events
    } else {
      candidateHouses = [1]; // Self for personal events
    }
  }
  
  // Use the first candidate house (most relevant)
  const primaryHouse = candidateHouses[0];
  const rasiName = HOUSE_TO_RASI[primaryHouse];
  const significations = HOUSE_SIGNIFICATIONS[primaryHouse].significations;
  
  // Build mapping reason
  const reason = candidateHouses.length > 1
    ? `Mapped to house ${primaryHouse} (${rasiName}) based on category "${event.category}" and significations. Also matched houses: ${candidateHouses.slice(1).join(', ')}`
    : `Mapped to house ${primaryHouse} (${rasiName}) based on category "${event.category}" and significations: ${significations.slice(0, 3).join(', ')}`;
  
  return {
    event_id: event.id!,
    house_number: primaryHouse,
    actual_house_number: undefined, // Will be set if chart data is available
    calculation_method: 'kalapurushan',
    rasi_name: rasiName,
    house_significations: significations.filter(sig => 
      category.includes(sig) || eventTitle.includes(sig) || eventDescription.includes(sig)
    ),
    mapping_reason: reason,
  };
}

/**
 * Map event to actual house based on ascendant and chart data
 * This function uses the actual planetary positions to determine the house
 */
export function mapEventToActualHouse(
  event: Event,
  chartData: ChartData | EventChartData | null
): HouseMapping {
  // First get the Kalapurushan mapping
  const kalapurushanMapping = mapEventToHouse(event);
  
  // If no chart data, return Kalapurushan mapping
  if (!chartData) {
    return kalapurushanMapping;
  }

  // Extract house cusps and ascendant from chart data
  const houseCusps = Array.isArray(chartData.house_cusps || chartData.houseCusps)
    ? (chartData.house_cusps || chartData.houseCusps)
    : [];
  
  if (houseCusps.length !== 12) {
    return kalapurushanMapping; // Invalid chart data, fallback to Kalapurushan
  }

  // Get the Kalapurushan house number
  const kalapurushanHouse = kalapurushanMapping.house_number;
  
  // Get the rasi for this Kalapurushan house
  const kalapurushanRasi = kalapurushanMapping.rasi_name;
  
  // Find the actual house based on which house contains planets related to this event
  // For now, we'll use a simpler approach: find which house has the most relevant planets
  // based on the event category, or use the Kalapurushan rasi to find the actual house
  
  // Get the ascendant rasi number
  const ascRasiNum = chartData.ascendant_rasi_number || 
    (typeof chartData.ascendant === 'object' ? chartData.ascendant.rasiNumber : 0);
  
  if (!ascRasiNum || ascRasiNum < 1 || ascRasiNum > 12) {
    return kalapurushanMapping; // Invalid ascendant, fallback
  }

  // Calculate which house the Kalapurushan rasi falls into based on ascendant
  // Rasi index (0-11): Aries=0, Taurus=1, ..., Pisces=11
  const rasiNames = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                      'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'];
  const kalapurushanRasiIndex = rasiNames.indexOf(kalapurushanRasi);
  
  if (kalapurushanRasiIndex === -1) {
    return kalapurushanMapping; // Invalid rasi name, fallback
  }

  // Calculate actual house: if ascendant is in rasi X, then that rasi is house 1
  // So rasi at index Y is house ((Y - X + 1 + 12) % 12) || 12
  const actualHouseNum = ((kalapurushanRasiIndex - (ascRasiNum - 1) + 1 + 12) % 12) || 12;

  // Get the rasi at the cusp of this actual house
  const actualHouseCusp = houseCusps[actualHouseNum - 1];
  const actualRasi = degreesToRasiForHouse(actualHouseCusp);

  return {
    ...kalapurushanMapping,
    actual_house_number: actualHouseNum,
    calculation_method: 'ascendant-based',
    mapping_reason: `${kalapurushanMapping.mapping_reason} (Ascendant-based: House ${actualHouseNum}, Rasi: ${actualRasi})`,
  };
}

/**
 * Helper: Convert degrees to rasi name
 */
function degreesToRasiForHouse(degrees: number): string {
  const rasiIndex = Math.floor((degrees % 360) / 30);
  const rasiNames = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                      'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'];
  return rasiNames[rasiIndex] || 'Aries';
}

/**
 * Calculate aspects using actual house positions from chart data
 */
export function calculatePlanetaryAspectsWithActualHouses(
  event: Event,
  houseMapping: HouseMapping,
  chartData: ChartData | EventChartData | null
): PlanetaryAspect[] {
  // Use actual house if available, otherwise fall back to Kalapurushan
  const targetHouse = houseMapping.actual_house_number || houseMapping.house_number;
  
  // If no chart data, fall back to regular aspect calculation
  if (!chartData) {
    // Need planetary data - this will be called from storeCorrelations with planetary data
    return [];
  }

  // Extract planetary positions from chart data
  const planetaryPositions = chartData.planetary_positions || 
    (typeof chartData === 'object' && 'planetaryPositions' in chartData ? chartData.planetaryPositions : {});
  
  const houseCusps = Array.isArray(chartData.house_cusps || chartData.houseCusps)
    ? (chartData.house_cusps || chartData.houseCusps)
    : [];

  if (!planetaryPositions || houseCusps.length !== 12) {
    return []; // Invalid chart data
  }

  const aspects: PlanetaryAspect[] = [];
  const planetNames = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu'];

  for (const planetName of planetNames) {
    const planetData = planetaryPositions[planetName];
    if (!planetData) continue;

    const planetLongitude = planetData.longitude || 0;
    const planetRasi = planetData.rasi?.name || planetData.rasi || 'Unknown';
    const planetHouse = planetData.house || getHouseForLongitude(planetLongitude, houseCusps);

    // Check conjunction (planet in target house)
    if (planetHouse === targetHouse) {
      aspects.push({
        event_id: event.id!,
        house_number: targetHouse,
        planet_name: planetName,
        aspect_type: 'conjunction',
        planet_longitude: planetLongitude,
        planet_rasi: planetRasi,
        aspect_strength: 'strong',
      });
      continue; // Skip other aspects for conjunction
    }

    // Calculate aspects based on actual house positions
    const aspectingHouses = calculateAspectingHousesFromActual(planetHouse, planetName);
    
    if (aspectingHouses.includes(targetHouse)) {
      const aspectType = getAspectTypeFromActual(planetHouse, planetName, targetHouse);
      
      if (!aspectType) continue;

      aspects.push({
        event_id: event.id!,
        house_number: targetHouse,
        planet_name: planetName,
        aspect_type: aspectType as PlanetaryAspect['aspect_type'],
        planet_longitude: planetLongitude,
        planet_rasi: planetRasi,
        aspect_strength: getAspectStrength(aspectType),
      });
    }
  }

  return aspects;
}

/**
 * Calculate which houses a planet aspects based on its actual house position
 */
function calculateAspectingHousesFromActual(planetHouse: number, planetName: string): number[] {
  const aspectingHouses: number[] = [];

  switch (planetName) {
    case 'Jupiter':
      aspectingHouses.push(
        ((planetHouse + 4) % 12) || 12,
        ((planetHouse + 6) % 12) || 12,
        ((planetHouse + 8) % 12) || 12
      );
      break;
    case 'Saturn':
      aspectingHouses.push(
        ((planetHouse + 2) % 12) || 12,
        ((planetHouse + 6) % 12) || 12,
        ((planetHouse + 9) % 12) || 12
      );
      break;
    case 'Mars':
      aspectingHouses.push(
        ((planetHouse + 3) % 12) || 12,
        ((planetHouse + 6) % 12) || 12,
        ((planetHouse + 7) % 12) || 12
      );
      break;
    case 'Rahu':
    case 'Ketu':
      aspectingHouses.push(
        ((planetHouse + 2) % 12) || 12,
        ((planetHouse + 6) % 12) || 12,
        ((planetHouse + 10) % 12) || 12,
        6, 8, 12 // Dustana houses
      );
      break;
    default:
      // Sun, Moon, Mercury, Venus: 7th only
      aspectingHouses.push(((planetHouse + 6) % 12) || 12);
  }

  return [...new Set(aspectingHouses)].sort((a, b) => a - b);
}

/**
 * Get aspect type based on actual house positions
 */
function getAspectTypeFromActual(planetHouse: number, planetName: string, targetHouse: number): string {
  switch (planetName) {
    case 'Jupiter':
      if (targetHouse === ((planetHouse + 4) % 12 || 12)) return 'drishti_5th';
      if (targetHouse === ((planetHouse + 6) % 12 || 12)) return 'drishti_7th';
      if (targetHouse === ((planetHouse + 8) % 12 || 12)) return 'drishti_9th';
      return '';
    case 'Saturn':
      if (targetHouse === ((planetHouse + 2) % 12 || 12)) return 'drishti_3rd';
      if (targetHouse === ((planetHouse + 6) % 12 || 12)) return 'drishti_7th';
      if (targetHouse === ((planetHouse + 9) % 12 || 12)) return 'drishti_10th';
      return '';
    case 'Mars':
      if (targetHouse === ((planetHouse + 3) % 12 || 12)) return 'drishti_4th';
      if (targetHouse === ((planetHouse + 6) % 12 || 12)) return 'drishti_7th';
      if (targetHouse === ((planetHouse + 7) % 12 || 12)) return 'drishti_8th';
      return '';
    case 'Rahu':
    case 'Ketu':
      if (targetHouse === ((planetHouse + 2) % 12 || 12)) return 'drishti_3rd';
      if (targetHouse === ((planetHouse + 6) % 12 || 12)) return 'drishti_7th';
      if (targetHouse === ((planetHouse + 10) % 12 || 12)) return 'drishti_11th';
      if ([6, 8, 12].includes(targetHouse)) return 'dustana';
      return '';
    default:
      if (targetHouse === ((planetHouse + 6) % 12 || 12)) return 'drishti_7th';
      return '';
  }
}

/**
 * Get aspect strength based on aspect type
 */
function getAspectStrength(aspectType: string): 'strong' | 'moderate' | 'weak' {
  if (aspectType === 'conjunction') return 'strong';
  if (['drishti_7th', 'dustana'].includes(aspectType)) return 'strong';
  if (['drishti_3rd', 'drishti_5th', 'drishti_9th', 'drishti_11th'].includes(aspectType)) return 'moderate';
  return 'weak';
}

/**
 * Calculate house number from planet's Rasi (for aspect calculation)
 */
function getHouseFromRasi(rasiName: string): number {
  return RASI_TO_HOUSE[rasiName] || 0;
}

/**
 * Calculate which house a planet aspects based on its position
 */
function getAspectingHouses(planet: Planet, planetName: string): number[] {
  const planetHouse = getHouseFromRasi(planet.rasi.name);
  if (planetHouse === 0) return [];
  
  const aspectingHouses: number[] = [];
  
  switch (planetName) {
    case 'Jupiter':
      // Aspects 5th, 7th, 9th
      aspectingHouses.push(
        ((planetHouse + 4) % 12) || 12,
        ((planetHouse + 6) % 12) || 12,
        ((planetHouse + 8) % 12) || 12
      );
      break;
      
    case 'Saturn':
      // Aspects 3rd, 7th, 10th
      aspectingHouses.push(
        ((planetHouse + 2) % 12) || 12,
        ((planetHouse + 6) % 12) || 12,
        ((planetHouse + 9) % 12) || 12
      );
      break;
      
    case 'Mars':
      // Aspects 4th, 7th, 8th
      aspectingHouses.push(
        ((planetHouse + 3) % 12) || 12,
        ((planetHouse + 6) % 12) || 12,
        ((planetHouse + 7) % 12) || 12
      );
      break;
      
    case 'Rahu':
    case 'Ketu':
      // Aspects 3rd, 7th, 11th from its position
      aspectingHouses.push(
        ((planetHouse + 2) % 12) || 12,
        ((planetHouse + 6) % 12) || 12,
        ((planetHouse + 10) % 12) || 12
      );
      // Also aspect dustana houses (6, 8, 12) as significant
      aspectingHouses.push(6, 8, 12);
      break;
      
    case 'Sun':
    case 'Moon':
    case 'Mercury':
    case 'Venus':
      // Aspects 7th only
      aspectingHouses.push(((planetHouse + 6) % 12) || 12);
      break;
  }
  
  return [...new Set(aspectingHouses)].sort((a, b) => a - b);
}

/**
 * Get aspect type for a planet aspecting a house
 */
function getAspectType(planet: Planet, planetName: string, aspectingHouses: number[], targetHouse: number): string {
  if (!aspectingHouses.includes(targetHouse)) return '';
  
  const planetHouse = getHouseFromRasi(planet.rasi.name);
  
  switch (planetName) {
    case 'Jupiter':
      if (targetHouse === ((planetHouse + 4) % 12 || 12)) return 'drishti_5th';
      if (targetHouse === ((planetHouse + 6) % 12 || 12)) return 'drishti_7th';
      if (targetHouse === ((planetHouse + 8) % 12 || 12)) return 'drishti_9th';
      return '';
      
    case 'Saturn':
      if (targetHouse === ((planetHouse + 2) % 12 || 12)) return 'drishti_3rd';
      if (targetHouse === ((planetHouse + 6) % 12 || 12)) return 'drishti_7th';
      if (targetHouse === ((planetHouse + 9) % 12 || 12)) return 'drishti_10th';
      return '';
      
    case 'Mars':
      if (targetHouse === ((planetHouse + 3) % 12 || 12)) return 'drishti_4th';
      if (targetHouse === ((planetHouse + 6) % 12 || 12)) return 'drishti_7th';
      if (targetHouse === ((planetHouse + 7) % 12 || 12)) return 'drishti_8th';
      return '';
      
    case 'Rahu':
    case 'Ketu':
      // Regular aspects: 3rd, 7th, 11th
      if (targetHouse === ((planetHouse + 2) % 12 || 12)) return 'drishti_3rd';
      if (targetHouse === ((planetHouse + 6) % 12 || 12)) return 'drishti_7th';
      if (targetHouse === ((planetHouse + 10) % 12 || 12)) return 'drishti_11th';
      // Dustana houses: 6, 8, 12
      if ([6, 8, 12].includes(targetHouse)) return 'dustana';
      return '';
      
    default:
      // Sun, Moon, Mercury, Venus: 7th only
      if (targetHouse === ((planetHouse + 6) % 12 || 12)) return 'drishti_7th';
      return '';
  }
}

/**
 * Calculate all planetary aspects for an event's house
 */
export function calculatePlanetaryAspects(
  event: Event,
  houseMapping: HouseMapping,
  planetaryData: PlanetaryData
): PlanetaryAspect[] {
  const aspects: PlanetaryAspect[] = [];
  const targetHouse = houseMapping.house_number;
  
  if (!planetaryData.planetary_data?.planets) {
    return aspects;
  }
  
  for (const planet of planetaryData.planetary_data.planets) {
    // Get houses this planet aspects
    const aspectingHouses = getAspectingHouses(planet, planet.name);
    
    // Check if planet is in the target house (conjunction)
    const planetHouse = getHouseFromRasi(planet.rasi.name);
    if (planetHouse === targetHouse) {
      aspects.push({
        event_id: event.id!,
        house_number: targetHouse,
        planet_name: planet.name,
        aspect_type: 'conjunction',
        planet_longitude: planet.longitude,
        planet_rasi: planet.rasi.name,
        aspect_strength: 'strong',
      });
    }
    
    // Check if planet aspects the target house
    if (aspectingHouses.includes(targetHouse)) {
      const aspectType = getAspectType(planet, planet.name, aspectingHouses, targetHouse) as PlanetaryAspect['aspect_type'];
      
      // Skip if aspect type is empty (shouldn't happen, but safety check)
      if (!aspectType) continue;
      
      // Determine aspect strength
      let aspectStrength: 'strong' | 'moderate' | 'weak' = 'moderate';
      if (aspectType === 'conjunction') {
        aspectStrength = 'strong';
      } else if (['drishti_7th', 'dustana'].includes(aspectType)) {
        aspectStrength = 'strong';
      } else if (['drishti_3rd', 'drishti_5th', 'drishti_9th', 'drishti_11th'].includes(aspectType)) {
        aspectStrength = 'moderate';
      } else {
        aspectStrength = 'weak';
      }
      
      // Check if already added as conjunction
      if (!aspects.some(a => a.planet_name === planet.name && a.aspect_type === 'conjunction')) {
        aspects.push({
          event_id: event.id!,
          house_number: targetHouse,
          planet_name: planet.name,
          aspect_type: aspectType,
          planet_longitude: planet.longitude,
          planet_rasi: planet.rasi.name,
          aspect_strength: aspectStrength,
        });
      }
    }
  }
  
  return aspects;
}

/**
 * Get house information
 */
export function getHouseInfo(houseNumber: number) {
  return HOUSE_SIGNIFICATIONS[houseNumber] || null;
}

/**
 * Get all house significations
 */
export function getAllHouseSignifications() {
  return HOUSE_SIGNIFICATIONS;
}

