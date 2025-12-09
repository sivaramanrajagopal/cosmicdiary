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
