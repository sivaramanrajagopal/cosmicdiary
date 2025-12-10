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
  title: string;
  description?: string;
  category: string;
  location?: string;
  latitude?: number;
  longitude?: number;
  impact_level: 'low' | 'medium' | 'high' | 'critical';
  event_type: 'world' | 'personal';
  tags: string[];
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
  house_number: number;  // 1-12
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
