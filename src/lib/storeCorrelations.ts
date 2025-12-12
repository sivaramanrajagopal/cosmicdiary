import { Event, PlanetaryData, EventPlanetaryCorrelation, EventChartData } from './types';
import { getPlanetaryData, createCorrelation, createHouseMapping, createPlanetaryAspect, getEventChartData } from './database';
import { analyzeEventPlanetaryCorrelation } from './astrologyAnalysis';
import { mapEventToHouse, mapEventToActualHouse, calculatePlanetaryAspects, calculatePlanetaryAspectsWithActualHouses } from './houseMapping';
import { ChartData } from '@/components/charts/chart-types';
import { transformChartDataFromDB } from '@/components/charts/chart-utils';

/**
 * Calculate and store planetary correlations for an event in the database
 */
export async function calculateAndStoreCorrelations(event: Event): Promise<EventPlanetaryCorrelation[]> {
  // Get planetary data for the event date
  const planetaryData = await getPlanetaryData(event.date);
  
  if (!planetaryData || !planetaryData.planetary_data?.planets) {
    console.log(`No planetary data available for ${event.date}, skipping correlation storage`);
    return [];
  }
  
  // Analyze the event
  const analysis = analyzeEventPlanetaryCorrelation(event, planetaryData);
  
  // Convert analysis to database correlations
  const correlations: EventPlanetaryCorrelation[] = [];
  
  // Store significant planet correlations
  for (const sp of analysis.significantPlanets) {
    const correlation: Omit<EventPlanetaryCorrelation, 'id' | 'created_at' | 'updated_at'> = {
      event_id: event.id!,
      date: event.date,
      planet_name: sp.planet.name,
      planet_position: sp.planet,
      correlation_score: sp.impact === 'high' ? 0.8 : sp.impact === 'medium' ? 0.6 : 0.4,
      reason: `${sp.significance}: ${sp.reason}`,
    };
    
    const stored = await createCorrelation(correlation);
    if (stored) {
      correlations.push(stored);
    }
  }
  
  // Store retrograde planet correlations
  for (const planet of analysis.retrogradePlanets) {
    // Skip if already stored as significant planet
    if (!correlations.find(c => c.planet_name === planet.name)) {
      const correlation: Omit<EventPlanetaryCorrelation, 'id' | 'created_at' | 'updated_at'> = {
        event_id: event.id!,
        date: event.date,
        planet_name: planet.name,
        planet_position: planet,
        correlation_score: 0.7,
        reason: `${planet.name} is retrograde, indicating intensified or reversed planetary energy`,
      };
      
      const stored = await createCorrelation(correlation);
      if (stored) {
        correlations.push(stored);
      }
    }
  }
  
  // Store correlation for dominant Rasi lord if applicable
  if (analysis.dominantRasi && analysis.dominantRasi !== 'Unknown') {
    const planets = planetaryData.planetary_data.planets;
    const rasiPlanets = planets.filter(p => p.rasi.name === analysis.dominantRasi);
    
    if (rasiPlanets.length > 0) {
      const lord = rasiPlanets[0].rasi.lord.name;
      const lordPlanet = planets.find(p => p.name === lord);
      
      if (lordPlanet && !correlations.find(c => c.planet_name === lord)) {
        const correlation: Omit<EventPlanetaryCorrelation, 'id' | 'created_at' | 'updated_at'> = {
          event_id: event.id!,
          date: event.date,
          planet_name: lord,
          planet_position: lordPlanet,
          correlation_score: 0.6,
          reason: `${lord} rules the dominant Rasi ${analysis.dominantRasi} with ${rasiPlanets.length} planet(s) positioned there`,
        };
        
        const stored = await createCorrelation(correlation);
        if (stored) {
          correlations.push(stored);
        }
      }
    }
  }
  
  // Get chart data if available (for ascendant-based mapping)
  let chartData: ChartData | null = null;
  const dbChartData = await getEventChartData(event.id!);
  if (dbChartData) {
    try {
      chartData = transformChartDataFromDB(dbChartData);
    } catch (err) {
      console.error('Error transforming chart data for house mapping:', err);
    }
  }

  // Calculate house mapping (use ascendant-based if chart data available)
  const houseMapping = chartData
    ? mapEventToActualHouse(event, chartData)
    : mapEventToHouse(event);
  
  const storedMapping = await createHouseMapping(houseMapping);
  
  // Calculate and store planetary aspects (use actual houses if chart data available)
  let aspects;
  if (chartData) {
    aspects = calculatePlanetaryAspectsWithActualHouses(event, houseMapping, chartData);
  } else {
    aspects = calculatePlanetaryAspects(event, houseMapping, planetaryData);
  }
  
  let aspectCount = 0;
  for (const aspect of aspects) {
    const stored = await createPlanetaryAspect(aspect);
    if (stored) {
      aspectCount++;
    }
  }
  
  const method = chartData ? 'ascendant-based' : 'kalapurushan';
  console.log(`✅ Stored for event ${event.id}: ${correlations.length} correlations, 1 house mapping (${method}), ${aspectCount} aspects`);
  return correlations;
}

/**
 * Recalculate and update correlations for all events (useful for migration)
 */
export async function recalculateAllCorrelations(events: Event[]): Promise<void> {
  console.log(`🔄 Recalculating correlations for ${events.length} events...`);
  
  let successCount = 0;
  let failCount = 0;
  
  for (const event of events) {
    if (!event.id) continue;
    
    try {
      const correlations = await calculateAndStoreCorrelations(event);
      if (correlations.length > 0) {
        successCount++;
      }
    } catch (error) {
      console.error(`Error calculating correlations for event ${event.id}:`, error);
      failCount++;
    }
  }
  
  console.log(`✅ Correlation recalculation complete: ${successCount} succeeded, ${failCount} failed`);
}

