import { Event, Planet, PlanetaryData } from './types';

export interface PlanetaryAnalysis {
  event: Event;
  planetaryData: PlanetaryData | null;
  significantPlanets: SignificantPlanet[];
  dominantRasi: string;
  dominantNakshatra: string;
  retrogradePlanets: Planet[];
  correlations: Correlation[];
}

export interface SignificantPlanet {
  planet: Planet;
  significance: string;
  impact: 'high' | 'medium' | 'low';
  reason: string;
}

export interface Correlation {
  type: 'retrograde' | 'rasi_lord' | 'nakshatra' | 'conjunction' | 'aspect';
  description: string;
  planets: string[];
  significance: string;
}

// Rasi characteristics for analysis
const RASI_CHARACTERISTICS: Record<string, { element: string; quality: string; nature: string }> = {
  'Aries': { element: 'Fire', quality: 'Cardinal', nature: 'Dynamic' },
  'Taurus': { element: 'Earth', quality: 'Fixed', nature: 'Stable' },
  'Gemini': { element: 'Air', quality: 'Mutable', nature: 'Changeable' },
  'Cancer': { element: 'Water', quality: 'Cardinal', nature: 'Emotional' },
  'Leo': { element: 'Fire', quality: 'Fixed', nature: 'Creative' },
  'Virgo': { element: 'Earth', quality: 'Mutable', nature: 'Analytical' },
  'Libra': { element: 'Air', quality: 'Cardinal', nature: 'Balanced' },
  'Scorpio': { element: 'Water', quality: 'Fixed', nature: 'Intense' },
  'Sagittarius': { element: 'Fire', quality: 'Mutable', nature: 'Expansive' },
  'Capricorn': { element: 'Earth', quality: 'Cardinal', nature: 'Disciplined' },
  'Aquarius': { element: 'Air', quality: 'Fixed', nature: 'Innovative' },
  'Pisces': { element: 'Water', quality: 'Mutable', nature: 'Intuitive' },
};

// Planet significations for event types
const PLANET_SIGNIFICATIONS: Record<string, { world: string[]; personal: string[] }> = {
  'Sun': { world: ['leadership', 'authority', 'government', 'power'], personal: ['ego', 'identity', 'father', 'health'] },
  'Moon': { world: ['public', 'emotions', 'masses', 'water'], personal: ['mind', 'mother', 'emotions', 'habits'] },
  'Mercury': { world: ['communication', 'media', 'trade', 'technology'], personal: ['intelligence', 'communication', 'siblings'] },
  'Venus': { world: ['relationships', 'arts', 'luxury', 'diplomacy'], personal: ['love', 'relationships', 'beauty', 'pleasure'] },
  'Mars': { world: ['conflict', 'war', 'accidents', 'fire'], personal: ['energy', 'courage', 'conflict', 'sports'] },
  'Jupiter': { world: ['expansion', 'philosophy', 'law', 'wealth'], personal: ['wisdom', 'growth', 'guru', 'religion'] },
  'Saturn': { world: ['restriction', 'delay', 'discipline', 'structures'], personal: ['karma', 'discipline', 'delay', 'aging'] },
  'Rahu': { world: ['chaos', 'disruption', 'technology', 'foreign'], personal: ['desires', 'materialism', 'obsessions'] },
  'Ketu': { world: ['isolation', 'spirituality', 'sudden'], personal: ['spirituality', 'detachment', 'moksha'] },
};

// Impact level planetary associations
const IMPACT_PLANET_ASSOCIATIONS: Record<string, string[]> = {
  'critical': ['Mars', 'Saturn', 'Rahu'],
  'high': ['Sun', 'Mars', 'Saturn'],
  'medium': ['Mercury', 'Venus', 'Jupiter'],
  'low': ['Moon', 'Venus', 'Mercury'],
};

export function analyzeEventPlanetaryCorrelation(event: Event, planetaryData: PlanetaryData | null): PlanetaryAnalysis {
  if (!planetaryData || !planetaryData.planetary_data?.planets) {
    return {
      event,
      planetaryData: null,
      significantPlanets: [],
      dominantRasi: 'Unknown',
      dominantNakshatra: 'Unknown',
      retrogradePlanets: [],
      correlations: [],
    };
  }

  const planets = planetaryData.planetary_data.planets;
  const retrogradePlanets = planets.filter(p => p.is_retrograde);
  
  // Find significant planets based on event characteristics
  const significantPlanets = findSignificantPlanets(event, planets);
  
  // Find dominant rasi (most planets in)
  const dominantRasi = findDominantRasi(planets);
  
  // Find dominant nakshatra (most planets in)
  const dominantNakshatra = findDominantNakshatra(planets);
  
  // Generate correlations
  const correlations = generateCorrelations(event, planets);

  return {
    event,
    planetaryData,
    significantPlanets,
    dominantRasi,
    dominantNakshatra,
    retrogradePlanets,
    correlations,
  };
}

function findSignificantPlanets(event: Event, planets: Planet[]): SignificantPlanet[] {
  const significant: SignificantPlanet[] = [];
  
  // Check retrograde planets (always significant)
  planets.forEach(planet => {
    if (planet.is_retrograde) {
      significant.push({
        planet,
        significance: 'Retrograde',
        impact: planet.name === 'Mars' || planet.name === 'Saturn' ? 'high' : 'medium',
        reason: `${planet.name} retrograde indicates intensified or reversed energy in ${getPlanetDomain(planet.name, event.event_type)}`,
      });
    }
  });
  
  // Check planets based on event category
  const categoryKeywords = event.category.toLowerCase().split(/\s+/);
  planets.forEach(planet => {
    const significations = PLANET_SIGNIFICATIONS[planet.name]?.[event.event_type] || [];
    const matches = significations.filter(sig => 
      categoryKeywords.some(kw => sig.includes(kw) || kw.includes(sig))
    );
    
    if (matches.length > 0) {
      significant.push({
        planet,
        significance: matches[0],
        impact: IMPACT_PLANET_ASSOCIATIONS[event.impact_level]?.includes(planet.name) ? 'high' : 'medium',
        reason: `${planet.name} governs ${matches[0]}, which aligns with this ${event.category.toLowerCase()} event`,
      });
    }
  });
  
  // Check for Mars/Saturn (conflict/structure indicators)
  if (event.impact_level === 'critical' || event.impact_level === 'high') {
    const mars = planets.find(p => p.name === 'Mars');
    const saturn = planets.find(p => p.name === 'Saturn');
    
    if (mars && !significant.find(s => s.planet.name === 'Mars')) {
      significant.push({
        planet: mars,
        significance: 'High Impact Indicator',
        impact: 'high',
        reason: 'Mars position indicates intensity and potential conflict or action in high-impact events',
      });
    }
    
    if (saturn && !significant.find(s => s.planet.name === 'Saturn')) {
      significant.push({
        planet: saturn,
        significance: 'Structural Impact',
        impact: 'high',
        reason: 'Saturn position suggests structural changes or karmic significance',
      });
    }
  }
  
  return significant.sort((a, b) => {
    const impactOrder = { high: 3, medium: 2, low: 1 };
    return impactOrder[b.impact] - impactOrder[a.impact];
  });
}

function findDominantRasi(planets: Planet[]): string {
  const rasiCounts: Record<string, number> = {};
  
  planets.forEach(planet => {
    const rasi = planet.rasi.name;
    rasiCounts[rasi] = (rasiCounts[rasi] || 0) + 1;
  });
  
  const dominant = Object.entries(rasiCounts).sort((a, b) => b[1] - a[1])[0];
  return dominant ? dominant[0] : 'Unknown';
}

function findDominantNakshatra(planets: Planet[]): string {
  const nakshatraCounts: Record<number, number> = {};
  
  planets.forEach(planet => {
    nakshatraCounts[planet.nakshatra] = (nakshatraCounts[planet.nakshatra] || 0) + 1;
  });
  
  const dominant = Object.entries(nakshatraCounts).sort((a, b) => b[1] - a[1])[0];
  if (dominant) {
    const nakshatras = [
      'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
      'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
      'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
      'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha',
      'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
    ];
    return nakshatras[parseInt(dominant[0]) - 1] || `N${dominant[0]}`;
  }
  return 'Unknown';
}

function generateCorrelations(event: Event, planets: Planet[]): Correlation[] {
  const correlations: Correlation[] = [];
  
  // Retrograde correlations
  const retrogradePlanets = planets.filter(p => p.is_retrograde);
  if (retrogradePlanets.length > 0) {
    correlations.push({
      type: 'retrograde',
      description: `${retrogradePlanets.length} planet(s) retrograde`,
      planets: retrogradePlanets.map(p => p.name),
      significance: `Retrograde planets amplify or reverse their natural energies, potentially intensifying ${event.category.toLowerCase()} events`,
    });
  }
  
  // Rasi lord correlations
  const rasiLords: Record<string, Planet[]> = {};
  planets.forEach(planet => {
    const lord = planet.rasi.lord.name;
    if (!rasiLords[lord]) rasiLords[lord] = [];
    rasiLords[lord].push(planet);
  });
  
  Object.entries(rasiLords).forEach(([lord, planetList]) => {
    if (planetList.length >= 2) {
      correlations.push({
        type: 'rasi_lord',
        description: `${lord} rules ${planetList.length} planetary positions`,
        planets: planetList.map(p => p.name),
        significance: `Strong ${lord} influence indicates ${getPlanetDomain(lord, event.event_type)} themes dominating this period`,
      });
    }
  });
  
  // Nakshatra clustering
  const nakshatraGroups: Record<number, Planet[]> = {};
  planets.forEach(planet => {
    if (!nakshatraGroups[planet.nakshatra]) nakshatraGroups[planet.nakshatra] = [];
    nakshatraGroups[planet.nakshatra].push(planet);
  });
  
  Object.entries(nakshatraGroups).forEach(([nakshatra, planetList]) => {
    if (planetList.length >= 3) {
      correlations.push({
        type: 'nakshatra',
        description: `${planetList.length} planets in same nakshatra`,
        planets: planetList.map(p => p.name),
        significance: `Planetary clustering in same nakshatra creates concentrated energy, amplifying event significance`,
      });
    }
  });
  
  // Same rasi clustering
  const rasiGroups: Record<string, Planet[]> = {};
  planets.forEach(planet => {
    const rasi = planet.rasi.name;
    if (!rasiGroups[rasi]) rasiGroups[rasi] = [];
    rasiGroups[rasi].push(planet);
  });
  
  Object.entries(rasiGroups).forEach(([rasi, planetList]) => {
    if (planetList.length >= 3) {
      const characteristics = RASI_CHARACTERISTICS[rasi];
      correlations.push({
        type: 'conjunction',
        description: `${planetList.length} planets in ${rasi}`,
        planets: planetList.map(p => p.name),
        significance: `Multiple planets in ${rasi} (${characteristics?.element} element, ${characteristics?.nature} nature) create a powerful conjunction affecting ${event.category.toLowerCase()} events`,
      });
    }
  });
  
  return correlations;
}

function getPlanetDomain(planetName: string, eventType: 'world' | 'personal'): string {
  const domains = PLANET_SIGNIFICATIONS[planetName];
  if (!domains) return 'various matters';
  
  const relevant = domains[eventType];
  return relevant && relevant.length > 0 ? relevant[0] : 'various matters';
}

export function analyzeAllEvents(events: Event[], planetaryDataMap: Map<string, PlanetaryData>): Map<number, PlanetaryAnalysis> {
  const analyses = new Map<number, PlanetaryAnalysis>();
  
  events.forEach(event => {
    const planetaryData = planetaryDataMap.get(event.date) || null;
    const analysis = analyzeEventPlanetaryCorrelation(event, planetaryData);
    if (event.id) {
      analyses.set(event.id, analysis);
    }
  });
  
  return analyses;
}

export function getPlanetaryPatterns(analyses: PlanetaryAnalysis[]): {
  mostActiveRasis: Array<{ rasi: string; count: number }>;
  mostActiveNakshatras: Array<{ nakshatra: string; count: number }>;
  retrogradeFrequency: Record<string, number>;
  categoryPlanetaryLinks: Record<string, string[]>;
} {
  const rasiCounts: Record<string, number> = {};
  const nakshatraCounts: Record<string, number> = {};
  const retrogradeCounts: Record<string, number> = {};
  const categoryLinks: Record<string, Set<string>> = {};
  
  analyses.forEach(analysis => {
    // Count rasis
    if (analysis.dominantRasi !== 'Unknown') {
      rasiCounts[analysis.dominantRasi] = (rasiCounts[analysis.dominantRasi] || 0) + 1;
    }
    
    // Count nakshatras
    if (analysis.dominantNakshatra !== 'Unknown') {
      nakshatraCounts[analysis.dominantNakshatra] = (nakshatraCounts[analysis.dominantNakshatra] || 0) + 1;
    }
    
    // Count retrograde planets
    analysis.retrogradePlanets.forEach(planet => {
      retrogradeCounts[planet.name] = (retrogradeCounts[planet.name] || 0) + 1;
    });
    
    // Link categories to planets
    const category = analysis.event.category;
    if (!categoryLinks[category]) categoryLinks[category] = new Set();
    analysis.significantPlanets.forEach(sp => {
      categoryLinks[category].add(sp.planet.name);
    });
  });
  
  return {
    mostActiveRasis: Object.entries(rasiCounts)
      .map(([rasi, count]) => ({ rasi, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 5),
    mostActiveNakshatras: Object.entries(nakshatraCounts)
      .map(([nakshatra, count]) => ({ nakshatra, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 5),
    retrogradeFrequency: retrogradeCounts,
    categoryPlanetaryLinks: Object.fromEntries(
      Object.entries(categoryLinks).map(([cat, planets]) => [cat, Array.from(planets)])
    ),
  };
}

