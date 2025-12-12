/**
 * TypeScript types for astrological chart components
 * 
 * These types define the structure of chart data used throughout
 * the chart visualization components.
 */

export interface ChartPlanet {
  name: string;
  abbreviation: string; // 'Su', 'Mo', 'Ma', etc.
  longitude: number;
  latitude: number;
  speed: number;
  rasi: {
    name: string;
    number: number;
    lord: string;
  };
  nakshatra: {
    name: string;
    number: number;
    pada: number;
  };
  house: number; // 1-12 based on ascendant
  isRetrograde: boolean;
  strength: {
    exalted: boolean;
    debilitated: boolean;
    ownSign: boolean;
    digBala: boolean;
    combusted: boolean;
    strengthScore: number; // 0-1
  };
}

export interface ChartAscendant {
  degree: number;
  rasi: string;
  rasiNumber: number;
  nakshatra?: string;
  lord: string;
}

export interface ChartData {
  ascendant: ChartAscendant;
  houseCusps: number[]; // [h1, h2, ..., h12] in degrees (0-360)
  planets: ChartPlanet[];
  houseSystem: string; // 'Placidus', 'Koch', 'Equal', 'Whole Sign'
  julianDay: number;
  siderealTime?: number; // In degrees
  ayanamsa: number;
}

export interface ChartDisplayProps {
  chartData: ChartData;
  eventId: number;
  eventDate: string;
  eventTime?: string;
  latitude?: number;
  longitude?: number;
}

export interface HouseInfo {
  number: number; // 1-12
  cuspDegree: number;
  rasi: string;
  rasiNumber: number;
  planets: ChartPlanet[];
}

export interface RasiInfo {
  name: string;
  number: number;
  lord: string;
  houseNumber?: number; // Based on ascendant
  planets: ChartPlanet[];
  startDegree: number;
  endDegree: number;
}

