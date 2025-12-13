/**
 * Planetary Impact Analysis Utilities
 * Functions to aggregate event data by house and planet for visualization
 */

import { supabase } from './supabase';
import { startOfDay, startOfWeek, startOfMonth, format } from 'date-fns';

export interface HouseImpact {
  house_number: number;
  event_count: number;
  house_name: string;
  significations: string[];
}

export interface PlanetImpact {
  planet_name: string;
  event_count: number;
  aspect_count: number;
  avg_aspect_strength: number;
}

export interface PlanetaryImpactSummary {
  period: 'day' | 'week' | 'month';
  start_date: string;
  end_date: string;
  total_events: number;
  house_impacts: HouseImpact[];
  planet_impacts: PlanetImpact[];
}

/**
 * Get house names and significations (simplified)
 */
function getHouseInfo(houseNumber: number): { name: string; significations: string[] } {
  const houseInfo: Record<number, { name: string; significations: string[] }> = {
    1: { name: 'Lagna (Ascendant)', significations: ['Self', 'Personality', 'Body', 'Health'] },
    2: { name: 'Dhana (Wealth)', significations: ['Wealth', 'Family', 'Food', 'Speech'] },
    3: { name: 'Sahaja (Siblings)', significations: ['Siblings', 'Courage', 'Communication', 'Short Journeys'] },
    4: { name: 'Sukha (Happiness)', significations: ['Mother', 'Home', 'Education', 'Vehicles'] },
    5: { name: 'Putra (Children)', significations: ['Children', 'Education', 'Intelligence', 'Romance'] },
    6: { name: 'Ari (Enemies)', significations: ['Enemies', 'Diseases', 'Service', 'Competition'] },
    7: { name: 'Kalatra (Spouse)', significations: ['Spouse', 'Partnership', 'Business', 'Public'] },
    8: { name: 'Ayush (Longevity)', significations: ['Longevity', 'Obstacles', 'Transformation', 'Occult'] },
    9: { name: 'Dharma (Religion)', significations: ['Religion', 'Father', 'Higher Learning', 'Fortune'] },
    10: { name: 'Karma (Career)', significations: ['Career', 'Status', 'Authority', 'Honor'] },
    11: { name: 'Labha (Gains)', significations: ['Gains', 'Income', 'Friends', 'Hopes'] },
    12: { name: 'Vyaya (Losses)', significations: ['Losses', 'Expenses', 'Foreign Lands', 'Spiritual'] },
  };
  
  return houseInfo[houseNumber] || { name: `House ${houseNumber}`, significations: [] };
}

/**
 * Get planetary impact analysis for a date range
 */
export async function getPlanetaryImpactAnalysis(
  period: 'day' | 'week' | 'month' = 'week'
): Promise<PlanetaryImpactSummary | null> {
  try {
    // Calculate date range based on period
    const now = new Date();
    let startDate: Date;
    let endDate = now;

    switch (period) {
      case 'day':
        startDate = startOfDay(now);
        break;
      case 'week':
        startDate = startOfWeek(now, { weekStartsOn: 1 }); // Monday
        break;
      case 'month':
        startDate = startOfMonth(now);
        break;
    }

    const startDateStr = format(startDate, 'yyyy-MM-dd');
    const endDateStr = format(endDate, 'yyyy-MM-dd');

    // Get events in date range
    const { data: events, error: eventsError } = await supabase
      .from('events')
      .select('id, date')
      .gte('date', startDateStr)
      .lte('date', endDateStr);

    if (eventsError) {
      console.error('Error fetching events:', eventsError);
      return null;
    }

    if (!events || events.length === 0) {
      return {
        period,
        start_date: startDateStr,
        end_date: endDateStr,
        total_events: 0,
        house_impacts: [],
        planet_impacts: [],
      };
    }

    const eventIds = events.map((e: any) => e.id);

    // Get house mappings for these events
    const { data: houseMappings, error: houseError } = await supabase
      .from('event_house_mappings')
      .select('event_id, house_number, actual_house_number, calculation_method')
      .in('event_id', eventIds);

    if (houseError) {
      console.error('Error fetching house mappings:', houseError);
    }

    // Get planetary aspects for these events
    const { data: aspects, error: aspectsError } = await supabase
      .from('event_planetary_aspects')
      .select('event_id, planet_name, aspect_type, aspect_strength, house_number')
      .in('event_id', eventIds);

    if (aspectsError) {
      console.error('Error fetching planetary aspects:', aspectsError);
    }

    // Aggregate house impacts (prefer actual_house_number if available, else house_number)
    const houseCounts: Record<number, number> = {};
    
    if (houseMappings) {
      houseMappings.forEach((mapping: any) => {
        const houseNum = mapping.actual_house_number || mapping.house_number;
        if (houseNum >= 1 && houseNum <= 12) {
          houseCounts[houseNum] = (houseCounts[houseNum] || 0) + 1;
        }
      });
    }

    // Aggregate planet impacts
    const planetCounts: Record<string, { event_count: number; aspect_count: number; strength_sum: number; strength_count: number }> = {};
    
    if (aspects) {
      aspects.forEach((aspect: any) => {
        const planet = aspect.planet_name;
        if (!planetCounts[planet]) {
          planetCounts[planet] = {
            event_count: 0,
            aspect_count: 0,
            strength_sum: 0,
            strength_count: 0,
          };
        }
        planetCounts[planet].aspect_count += 1;
        
        // Calculate strength score (strong=3, moderate=2, weak=1)
        const strengthScore = aspect.aspect_strength === 'strong' ? 3 :
                            aspect.aspect_strength === 'moderate' ? 2 : 1;
        planetCounts[planet].strength_sum += strengthScore;
        planetCounts[planet].strength_count += 1;
      });

      // Count unique events per planet
      const planetEvents: Record<string, Set<number>> = {};
      aspects.forEach((aspect: any) => {
        if (!planetEvents[aspect.planet_name]) {
          planetEvents[aspect.planet_name] = new Set();
        }
        planetEvents[aspect.planet_name].add(aspect.event_id);
      });

      Object.keys(planetEvents).forEach((planet) => {
        if (planetCounts[planet]) {
          planetCounts[planet].event_count = planetEvents[planet].size;
        }
      });
    }

    // Build house impacts array
    const houseImpacts: HouseImpact[] = [];
    for (let i = 1; i <= 12; i++) {
      const info = getHouseInfo(i);
      houseImpacts.push({
        house_number: i,
        event_count: houseCounts[i] || 0,
        house_name: info.name,
        significations: info.significations,
      });
    }

    // Build planet impacts array
    const planetImpacts: PlanetImpact[] = Object.entries(planetCounts).map(([planet, data]) => ({
      planet_name: planet,
      event_count: data.event_count,
      aspect_count: data.aspect_count,
      avg_aspect_strength: data.strength_count > 0 ? data.strength_sum / data.strength_count : 0,
    }));

    // Sort by event count descending
    houseImpacts.sort((a, b) => b.event_count - a.event_count);
    planetImpacts.sort((a, b) => b.event_count - a.event_count);

    return {
      period,
      start_date: startDateStr,
      end_date: endDateStr,
      total_events: events.length,
      house_impacts: houseImpacts,
      planet_impacts: planetImpacts,
    };
  } catch (error) {
    console.error('Error in getPlanetaryImpactAnalysis:', error);
    return null;
  }
}

