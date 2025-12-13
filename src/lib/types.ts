export interface Rasi {
  name: string;
  number: number;
  lord: {
    name: string;
  };
}

export interface Planet {
  name: string;
  longitude: number;
  latitude: number;
  is_retrograde: boolean;
  nakshatra: number;
  rasi: Rasi;
}

export interface Event {
  id?: number;  // BIGSERIAL, not UUID
  date: string;
  event_time?: string;  // TIME format (HH:MM:SS)
  timezone?: string;  // IANA timezone string (e.g., 'Asia/Kolkata')
  has_accurate_time?: boolean;  // Flag indicating if exact time is known
  title: string;
  description?: string;
  category: string;
  location?: string;
  latitude?: number;
  longitude?: number;
  impact_level: 'low' | 'medium' | 'high' | 'critical';
  event_type: 'world' | 'personal';
  tags: string[];
  sources?: string[];  // Array of source URLs/news sources
  created_at?: string;
  updated_at?: string;
}

export interface PlanetaryData {
  date: string;
  planetary_data: {
    planets: Planet[];
  };
}

export interface PlanetaryDataRow {
  id?: number;  // BIGSERIAL
  date: string;
  planetary_data: {
    planets: Planet[];
  };
  created_at?: string;
  updated_at?: string;
}

export interface EventPlanetaryCorrelation {
  id?: number;
  event_id: number;
  date: string;
  planet_name: string;
  planet_position?: Planet;
  correlation_score: number;  // 0.0 to 1.0
  reason?: string;
  created_at?: string;
  updated_at?: string;
}

export interface EventHouseMapping {
  id?: number;
  event_id: number;
  house_number: number;  // 1-12 (Kalapurushan house)
  actual_house_number?: number;  // 1-12 (Ascendant-based house)
  calculation_method?: 'kalapurushan' | 'ascendant-based';
  rasi_name: string;
  house_significations: string[];
  mapping_reason?: string;
  created_at?: string;
  updated_at?: string;
}

export interface EventPlanetaryAspect {
  id?: number;
  event_id: number;
  house_number: number;  // 1-12
  planet_name: string;
  aspect_type: 'conjunction' | 'drishti_3rd' | 'drishti_4th' | 'drishti_5th' | 'drishti_7th' | 'drishti_8th' | 'drishti_9th' | 'drishti_10th' | 'drishti_11th' | 'dustana';
  planet_longitude: number;
  planet_rasi: string;
  aspect_strength: 'strong' | 'moderate' | 'weak';
  created_at?: string;
  updated_at?: string;
}

// Chart-related types (re-exported from components/charts/chart-types.ts)
export interface EventChartData {
  id?: number;
  event_id: number;
  ascendant_degree: number;
  ascendant_rasi: string;
  ascendant_rasi_number: number;
  ascendant_nakshatra?: string;
  ascendant_lord: string;
  house_cusps: number[];
  house_system: string;
  julian_day: number;
  sidereal_time?: number;
  ayanamsa: number;
  planetary_positions: any; // JSONB - will be parsed
  planetary_strengths: any; // JSONB - will be parsed
  created_at?: string;
  updated_at?: string;
}
