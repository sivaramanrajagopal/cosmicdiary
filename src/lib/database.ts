import { supabase } from './supabase';
import { Event, PlanetaryData, EventPlanetaryCorrelation } from './types';

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
    const { data, error } = await supabase
      .from('event_planetary_correlations')
      .select('*')
      .eq('event_id', eventId)
      .order('correlation_score', { ascending: false });
    
    if (error) {
      console.error('Error fetching correlations:', error);
      return [];
    }
    
    return (data || []).map((corr: any) => ({
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
    }));
  } catch (error) {
    console.error('Error fetching correlations:', error);
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

// Helper function to format event data (handle nulls and type conversions)
function formatEvent(data: any): Event {
  return {
    id: data.id,
    date: data.date,
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
