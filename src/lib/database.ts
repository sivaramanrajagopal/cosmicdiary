import { supabase } from './supabase';
import { Event, PlanetaryData, EventPlanetaryCorrelation, EventHouseMapping, EventPlanetaryAspect, EventChartData } from './types';

export async function getEvents(date?: string): Promise<Event[]> {
  try {
    let query = supabase.from('events').select('*').order('date', { ascending: false });
    
    if (date) {
      query = query.eq('date', date);
    }
    
    const { data, error } = await query;
    
    if (error) {
      console.error('Error fetching events:', error);
      return [];
    }
    
    return (data || []).map(formatEvent);
  } catch (error) {
    console.error('Error fetching events:', error);
    return [];
  }
}

export async function getEventById(id: number): Promise<Event | null> {
  try {
    const { data, error } = await supabase
      .from('events')
      .select('*')
      .eq('id', id)
      .single();
    
    if (error) {
      console.error('Error fetching event:', error);
      return null;
    }
    
    return formatEvent(data);
  } catch (error) {
    console.error('Error fetching event:', error);
    return null;
  }
}

export async function createEvent(event: Omit<Event, 'id' | 'created_at' | 'updated_at'>): Promise<Event | null> {
  try {
    const { data, error } = await supabase
      .from('events')
      .insert([event])
      .select()
      .single();
    
    if (error) {
      console.error('Error creating event:', error);
      return null;
    }
    
    return formatEvent(data);
  } catch (error) {
    console.error('Error creating event:', error);
    return null;
  }
}

export async function getPlanetaryData(date: string): Promise<PlanetaryData | null> {
  try {
    const { data, error } = await supabase
      .from('planetary_data')
      .select('*')
      .eq('date', date)
      .maybeSingle(); // Use maybeSingle() instead of single() to avoid errors when no rows found
    
    if (error) {
      // PGRST116 means "no rows found" - this is expected, not an error
      if (error.code === 'PGRST116') {
        return null;
      }
      console.error('Error fetching planetary data:', error);
      return null;
    }
    
    if (!data) {
      return null;
    }
    
    // Transform the data to match PlanetaryData interface
    return {
      date: data.date,
      planetary_data: typeof data.planetary_data === 'string' 
        ? JSON.parse(data.planetary_data)
        : data.planetary_data,
    };
  } catch (error) {
    console.error('Error fetching planetary data:', error);
    return null;
  }
}

export async function getPlanetaryDataForEvent(event: Event): Promise<PlanetaryData | null> {
  // Get planetary data for the event's date
  return getPlanetaryData(event.date);
}

export async function createPlanetaryData(planetaryData: PlanetaryData): Promise<PlanetaryData | null> {
  try {
    const dataToStore = {
      date: planetaryData.date,
      planetary_data: planetaryData.planetary_data,
    };

    const { data, error } = await supabase
      .from('planetary_data')
      .insert([dataToStore])
      .select()
      .single();

    if (error) {
      // If it's a duplicate key error, that's okay - data already exists
      if (error.code === '23505') {
        console.log(`Planetary data for ${planetaryData.date} already exists`);
        return planetaryData;
      }
      console.error('Error creating planetary data:', error);
      return null;
    }

    return {
      date: data.date,
      planetary_data: typeof data.planetary_data === 'string'
        ? JSON.parse(data.planetary_data)
        : data.planetary_data,
    };
  } catch (error) {
    console.error('Error creating planetary data:', error);
    return null;
  }
}

export async function getEventCorrelations(eventId: number): Promise<EventPlanetaryCorrelation[]> {
  try {
    // Validate eventId
    if (!eventId || typeof eventId !== 'number' || isNaN(eventId)) {
      console.warn(`Invalid eventId for getEventCorrelations: ${eventId}`);
      return [];
    }

    const { data, error } = await supabase
      .from('event_planetary_correlations')
      .select('*')
      .eq('event_id', eventId)
      .order('correlation_score', { ascending: false });
    
    if (error) {
      // Enhanced error logging
      console.error('Error fetching correlations:', {
        error,
        eventId,
        errorCode: error.code,
        errorMessage: error.message,
        errorDetails: error.details,
        errorHint: error.hint,
      });
      // Return empty array instead of throwing - this is expected if table doesn't exist or has no data
      return [];
    }
    
    // Handle case where data might be null
    if (!data) {
      return [];
    }
    
    return data.map((corr: any) => {
      try {
        return {
          id: corr.id,
          event_id: corr.event_id,
          date: corr.date,
          planet_name: corr.planet_name,
          planet_position: corr.planet_position ? 
            (typeof corr.planet_position === 'string' ? JSON.parse(corr.planet_position) : corr.planet_position)
            : undefined,
          correlation_score: corr.correlation_score,
          reason: corr.reason,
          created_at: corr.created_at,
          updated_at: corr.updated_at,
        };
      } catch (parseError) {
        console.warn('Error parsing correlation data:', parseError, corr);
        // Return a basic version if parsing fails
        return {
          id: corr.id,
          event_id: corr.event_id,
          date: corr.date,
          planet_name: corr.planet_name,
          planet_position: undefined,
          correlation_score: corr.correlation_score || 0,
          reason: corr.reason,
          created_at: corr.created_at,
          updated_at: corr.updated_at,
        };
      }
    });
  } catch (error) {
    // Catch any unexpected errors
    console.error('Unexpected error fetching correlations:', {
      error,
      eventId,
      errorType: error instanceof Error ? error.constructor.name : typeof error,
      errorMessage: error instanceof Error ? error.message : String(error),
      stack: error instanceof Error ? error.stack : undefined,
    });
    return [];
  }
}

export async function createCorrelation(
  correlation: Omit<EventPlanetaryCorrelation, 'id' | 'created_at' | 'updated_at'>
): Promise<EventPlanetaryCorrelation | null> {
  try {
    const { data, error } = await supabase
      .from('event_planetary_correlations')
      .insert([{
        event_id: correlation.event_id,
        date: correlation.date,
        planet_name: correlation.planet_name,
        planet_position: correlation.planet_position,
        correlation_score: correlation.correlation_score,
        reason: correlation.reason,
      }])
      .select()
      .single();
    
    if (error) {
      console.error('Error creating correlation:', error);
      return null;
    }
    
    return {
      id: data.id,
      event_id: data.event_id,
      date: data.date,
      planet_name: data.planet_name,
      planet_position: data.planet_position,
      correlation_score: data.correlation_score,
      reason: data.reason,
      created_at: data.created_at,
      updated_at: data.updated_at,
    };
  } catch (error) {
    console.error('Error creating correlation:', error);
    return null;
  }
}

// House Mapping Functions
export async function createHouseMapping(
  mapping: Omit<EventHouseMapping, 'id' | 'created_at' | 'updated_at'>
): Promise<EventHouseMapping | null> {
  try {
    const { data, error } = await supabase
      .from('event_house_mappings')
      .upsert([{
        event_id: mapping.event_id,
        house_number: mapping.house_number,
        actual_house_number: mapping.actual_house_number ?? null,
        calculation_method: mapping.calculation_method || 'kalapurushan',
        rasi_name: mapping.rasi_name,
        house_significations: mapping.house_significations,
        mapping_reason: mapping.mapping_reason,
      }], {
        onConflict: 'event_id',
      })
      .select()
      .single();
    
    if (error) {
      console.error('Error creating house mapping:', error);
      return null;
    }
    
    return {
      id: data.id,
      event_id: data.event_id,
      house_number: data.house_number,
      actual_house_number: data.actual_house_number ?? undefined,
      calculation_method: data.calculation_method || 'kalapurushan',
      rasi_name: data.rasi_name,
      house_significations: Array.isArray(data.house_significations)
        ? data.house_significations
        : (data.house_significations ? JSON.parse(data.house_significations as string) : []),
      mapping_reason: data.mapping_reason || undefined,
      created_at: data.created_at,
      updated_at: data.updated_at,
    };
  } catch (error) {
    console.error('Error creating house mapping:', error);
    return null;
  }
}

export async function getHouseMapping(eventId: number): Promise<EventHouseMapping | null> {
  try {
    const { data, error } = await supabase
      .from('event_house_mappings')
      .select('*')
      .eq('event_id', eventId)
      .maybeSingle();
    
    if (error || !data) {
      return null;
    }
    
    return {
      id: data.id,
      event_id: data.event_id,
      house_number: data.house_number,
      actual_house_number: data.actual_house_number ?? undefined,
      calculation_method: data.calculation_method || 'kalapurushan',
      rasi_name: data.rasi_name,
      house_significations: Array.isArray(data.house_significations)
        ? data.house_significations
        : (data.house_significations ? JSON.parse(data.house_significations as string) : []),
      mapping_reason: data.mapping_reason || undefined,
      created_at: data.created_at,
      updated_at: data.updated_at,
    };
  } catch (error) {
    console.error('Error fetching house mapping:', error);
    return null;
  }
}

// Planetary Aspect Functions
export async function createPlanetaryAspect(
  aspect: Omit<EventPlanetaryAspect, 'id' | 'created_at' | 'updated_at'>
): Promise<EventPlanetaryAspect | null> {
  try {
    const { data, error } = await supabase
      .from('event_planetary_aspects')
      .insert([{
        event_id: aspect.event_id,
        house_number: aspect.house_number,
        planet_name: aspect.planet_name,
        aspect_type: aspect.aspect_type,
        planet_longitude: aspect.planet_longitude,
        planet_rasi: aspect.planet_rasi,
        aspect_strength: aspect.aspect_strength,
      }])
      .select()
      .single();
    
    if (error) {
      // Ignore duplicate key errors (UNIQUE constraint)
      if (error.code === '23505') {
        return null;
      }
      console.error('Error creating planetary aspect:', error);
      return null;
    }
    
    return {
      id: data.id,
      event_id: data.event_id,
      house_number: data.house_number,
      planet_name: data.planet_name,
      aspect_type: data.aspect_type,
      planet_longitude: data.planet_longitude,
      planet_rasi: data.planet_rasi,
      aspect_strength: data.aspect_strength,
      created_at: data.created_at,
      updated_at: data.updated_at,
    };
  } catch (error) {
    console.error('Error creating planetary aspect:', error);
    return null;
  }
}

export async function getPlanetaryAspects(eventId: number): Promise<EventPlanetaryAspect[]> {
  try {
    const { data, error } = await supabase
      .from('event_planetary_aspects')
      .select('*')
      .eq('event_id', eventId)
      .order('aspect_strength', { ascending: false });
    
    if (error || !data) {
      return [];
    }
    
    return data.map((asp: any) => ({
      id: asp.id,
      event_id: asp.event_id,
      house_number: asp.house_number,
      planet_name: asp.planet_name,
      aspect_type: asp.aspect_type,
      planet_longitude: asp.planet_longitude,
      planet_rasi: asp.planet_rasi,
      aspect_strength: asp.aspect_strength,
      created_at: asp.created_at,
      updated_at: asp.updated_at,
    }));
  } catch (error) {
    console.error('Error fetching planetary aspects:', error);
    return [];
  }
}

// ============================================================================
// Chart Data Functions
// ============================================================================

export async function getEventChartData(eventId: number): Promise<EventChartData | null> {
  try {
    const { data, error } = await supabase
      .from('event_chart_data')
      .select('*')
      .eq('event_id', eventId)
      .maybeSingle();

    if (error) {
      console.error('Error fetching chart data:', error);
      return null;
    }

    if (!data) return null;

    return {
      id: data.id,
      event_id: data.event_id,
      ascendant_degree: data.ascendant_degree,
      ascendant_rasi: data.ascendant_rasi,
      ascendant_rasi_number: data.ascendant_rasi_number,
      ascendant_nakshatra: data.ascendant_nakshatra || undefined,
      ascendant_lord: data.ascendant_lord,
      house_cusps: Array.isArray(data.house_cusps)
        ? data.house_cusps
        : (typeof data.house_cusps === 'string' ? JSON.parse(data.house_cusps) : []),
      house_system: data.house_system,
      julian_day: data.julian_day,
      sidereal_time: data.sidereal_time || undefined,
      ayanamsa: data.ayanamsa,
      planetary_positions: typeof data.planetary_positions === 'string'
        ? JSON.parse(data.planetary_positions)
        : data.planetary_positions,
      planetary_strengths: typeof data.planetary_strengths === 'string'
        ? JSON.parse(data.planetary_strengths)
        : data.planetary_strengths,
      created_at: data.created_at,
      updated_at: data.updated_at,
    };
  } catch (error) {
    console.error('Error in getEventChartData:', error);
    return null;
  }
}

export async function storeEventChartData(
  eventId: number,
  chartData: Omit<EventChartData, 'id' | 'event_id' | 'created_at' | 'updated_at'>
): Promise<EventChartData | null> {
  try {
    const { data, error } = await supabase
      .from('event_chart_data')
      .upsert([{
        event_id: eventId,
        ...chartData,
      }], {
        onConflict: 'event_id',
      })
      .select()
      .single();

    if (error) {
      console.error('Error storing chart data:', error);
      return null;
    }

    return getEventChartData(eventId);
  } catch (error) {
    console.error('Error in storeEventChartData:', error);
    return null;
  }
}

// Helper function to format event data (handle nulls and type conversions)
function formatEvent(data: any): Event {
  return {
    id: data.id,
    date: data.date,
    event_time: data.event_time || undefined,
    timezone: data.timezone || undefined,
    has_accurate_time: data.has_accurate_time ?? undefined,
    title: data.title,
    description: data.description || '',
    category: data.category,
    location: data.location || '',
    latitude: data.latitude ?? undefined,
    longitude: data.longitude ?? undefined,
    impact_level: data.impact_level || 'medium',
    event_type: data.event_type || 'world',
    tags: Array.isArray(data.tags) ? data.tags : (data.tags ? JSON.parse(data.tags) : []),
    created_at: data.created_at,
    updated_at: data.updated_at,
  };
}
