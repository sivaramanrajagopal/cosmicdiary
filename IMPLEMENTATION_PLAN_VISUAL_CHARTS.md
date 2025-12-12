# Implementation Plan: Visual Chart Display & Enhanced Analysis

**Date:** December 12, 2025  
**Priority:** P3 (Visual Charts) + P4 (Enhanced Analysis)  
**Status:** Planning Phase

---

## Table of Contents

1. [File Structure](#file-structure)
2. [Implementation Sequence](#implementation-sequence)
3. [Code Snippets & Key Logic](#code-snippets--key-logic)
4. [Integration Points](#integration-points)
5. [Testing Strategy](#testing-strategy)
6. [Migration Path](#migration-path)
7. [Database Schema Updates](#database-schema-updates)

---

## 1. File Structure

### P3: Visual Chart Components (Priority 3)

#### New Files to Create:

```
src/components/charts/
├── NorthIndianChart.tsx           # Diamond/square house layout
├── SouthIndianChart.tsx           # Circular rasi layout
├── ChartContainer.tsx             # Main container with tabs
├── PlanetDetailsModal.tsx         # Planet information modal
├── PlanetaryStrengthPanel.tsx     # Strength visualization
├── chart-utils.ts                 # Utility functions for chart calculations
├── chart-types.ts                 # TypeScript types for charts
└── chart-colors.ts                # Color scheme constants
```

#### Files to Update:

```
src/app/events/[id]/page.tsx       # Add chart displays
src/lib/database.ts                # Add chart data fetch functions
src/lib/types.ts                   # Add chart-related types
src/app/api/chart/calculate/route.ts  # New API endpoint for chart calculation
```

### P4: Enhanced Analysis (Priority 4)

#### New Files to Create:

```
database_migrations/
├── 004_add_location_accuracy.sql  # Add geocoding fields (if needed)
└── 005_migrate_existing_events.sql # Migration script for existing events
```

#### Files to Update:

```
src/lib/houseMapping.ts            # Add ascendant-based mapping
src/lib/storeCorrelations.ts       # Integrate chart calculations
astro_calculations.py              # Ensure all calculations are present
api_server.py                      # Verify chart endpoint exists
```

---

## 2. Implementation Sequence

### Phase 1: Foundation & Types (Day 1)

**Dependencies:** None  
**Testing Checkpoint:** Type definitions compile without errors

1. ✅ Create `src/components/charts/chart-types.ts`
2. ✅ Create `src/components/charts/chart-colors.ts`
3. ✅ Create `src/components/charts/chart-utils.ts`
4. ✅ Update `src/lib/types.ts` with chart data types
5. ✅ Test type imports across project

### Phase 2: Database & API (Day 1-2)

**Dependencies:** Phase 1  
**Testing Checkpoint:** API returns chart data correctly

1. ✅ Verify `event_chart_data` table exists (migration 002)
2. ✅ Create/verify API endpoint: `/api/chart/calculate`
3. ✅ Create database functions: `getEventChartData()`, `storeEventChartData()`
4. ✅ Test API with sample event
5. ✅ Test database queries

### Phase 3: Core Chart Components (Day 2-3)

**Dependencies:** Phase 1, 2  
**Testing Checkpoint:** Basic chart renders with mock data

1. ✅ Create `NorthIndianChart.tsx` (basic layout)
2. ✅ Create `SouthIndianChart.tsx` (basic layout)
3. ✅ Create `ChartContainer.tsx` (tab switching)
4. ✅ Test with hardcoded data
5. ✅ Test responsive design

### Phase 4: Interactivity & Details (Day 3-4)

**Dependencies:** Phase 3  
**Testing Checkpoint:** All interactions work correctly

1. ✅ Add planet rendering to both charts
2. ✅ Create `PlanetDetailsModal.tsx`
3. ✅ Add hover states and click handlers
4. ✅ Create `PlanetaryStrengthPanel.tsx`
5. ✅ Add export/print functionality
6. ✅ Test all user interactions

### Phase 5: Integration with Event Page (Day 4)

**Dependencies:** Phase 2, 3, 4  
**Testing Checkpoint:** Event page displays charts correctly

1. ✅ Update `src/app/events/[id]/page.tsx`
2. ✅ Add chart fetching logic
3. ✅ Integrate all chart components
4. ✅ Add loading states
5. ✅ Test with real events

### Phase 6: Enhanced Analysis (Day 5)

**Dependencies:** Phase 2  
**Testing Checkpoint:** House mappings use actual positions

1. ✅ Update `src/lib/houseMapping.ts` for ascendant-based mapping
2. ✅ Update `src/lib/storeCorrelations.ts` to store chart data
3. ✅ Test house mapping calculations
4. ✅ Test aspect calculations with actual houses

### Phase 7: Migration & Backfill (Day 5-6)

**Dependencies:** Phase 6  
**Testing Checkpoint:** Existing events have chart data

1. ✅ Create migration script for existing events
2. ✅ Run backfill script
3. ✅ Verify data integrity
4. ✅ Test with migrated events

### Phase 8: Polish & Testing (Day 6)

**Dependencies:** All phases  
**Testing Checkpoint:** All features work end-to-end

1. ✅ Add error boundaries
2. ✅ Improve loading states
3. ✅ Add accessibility features
4. ✅ Cross-browser testing
5. ✅ Performance optimization
6. ✅ Documentation updates

---

## 3. Code Snippets & Key Logic

### 3.1 Chart Types (`src/components/charts/chart-types.ts`)

```typescript
export interface ChartPlanet {
  name: string;
  abbreviation: string; // 'Su', 'Mo', 'Ma', etc.
  longitude: number;
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
  house: number; // 1-12
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

export interface ChartData {
  ascendant: {
    degree: number;
    rasi: string;
    rasiNumber: number;
    lord: string;
  };
  houseCusps: number[]; // [h1, h2, ..., h12] in degrees
  planets: ChartPlanet[];
  houseSystem: string; // 'Placidus'
  julianDay: number;
  ayanamsa: number;
  siderealTime: number;
}

export interface ChartDisplayProps {
  chartData: ChartData;
  eventId: number;
  eventDate: string;
  eventTime?: string;
  latitude?: number;
  longitude?: number;
}
```

### 3.2 Chart Colors (`src/components/charts/chart-colors.ts`)

```typescript
export const PLANET_COLORS: Record<string, string> = {
  Sun: '#FFD700',        // Gold
  Moon: '#C0C0C0',       // Silver
  Mars: '#FF4500',       // Red-orange
  Mercury: '#98D8C8',    // Teal
  Jupiter: '#FFA500',    // Orange
  Venus: '#FFDAB9',      // Peach
  Saturn: '#708090',     // Slate gray
  Rahu: '#8B0000',       // Dark red
  Ketu: '#4B0082',       // Indigo
};

export const PLANET_ABBREVIATIONS: Record<string, string> = {
  Sun: 'Su',
  Moon: 'Mo',
  Mars: 'Ma',
  Mercury: 'Me',
  Jupiter: 'Ju',
  Venus: 'Ve',
  Saturn: 'Sa',
  Rahu: 'Ra',
  Ketu: 'Ke',
};

export const HOUSE_COLORS = {
  odd: 'bg-slate-800/50',   // Odd houses (1,3,5,7,9,11)
  even: 'bg-slate-700/50',  // Even houses (2,4,6,8,10,12)
  ascendant: 'bg-purple-900/50', // 1st house (ascendant)
};
```

### 3.3 North Indian Chart Component (`src/components/charts/NorthIndianChart.tsx`)

```typescript
'use client';

import { useState } from 'react';
import { ChartData, ChartPlanet } from './chart-types';
import { PLANET_COLORS, PLANET_ABBREVIATIONS } from './chart-colors';
import PlanetDetailsModal from './PlanetDetailsModal';

interface NorthIndianChartProps {
  chartData: ChartData;
  onPlanetClick?: (planet: ChartPlanet) => void;
}

export default function NorthIndianChart({ chartData, onPlanetClick }: NorthIndianChartProps) {
  const [selectedPlanet, setSelectedPlanet] = useState<ChartPlanet | null>(null);
  const [hoveredHouse, setHoveredHouse] = useState<number | null>(null);

  // Calculate house positions (diamond layout)
  const getHousePosition = (houseNumber: number) => {
    const positions = [
      { top: 0, left: '50%', transform: 'translateX(-50%)' },      // House 1 (top)
      { top: '20%', right: 0, transform: 'translateY(-50%)' },     // House 2
      { top: '50%', right: 0, transform: 'translateY(-50%)' },     // House 3
      { bottom: '20%', right: 0, transform: 'translateY(-50%)' },  // House 4
      { bottom: 0, left: '50%', transform: 'translateX(-50%)' },   // House 5 (bottom)
      { bottom: '20%', left: 0, transform: 'translateY(-50%)' },   // House 6
      { top: '50%', left: 0, transform: 'translateY(-50%)' },      // House 7
      { top: '20%', left: 0, transform: 'translateY(-50%)' },      // House 8
      { top: '10%', left: '25%', transform: 'translate(-50%, -50%)' }, // House 9
      { top: '10%', right: '25%', transform: 'translate(50%, -50%)' }, // House 10
      { bottom: '10%', right: '25%', transform: 'translate(50%, 50%)' }, // House 11
      { bottom: '10%', left: '25%', transform: 'translate(-50%, 50%)' }, // House 12
    ];
    return positions[houseNumber - 1];
  };

  const getPlanetsInHouse = (houseNumber: number): ChartPlanet[] => {
    return chartData.planets.filter(p => p.house === houseNumber);
  };

  const handlePlanetClick = (planet: ChartPlanet) => {
    setSelectedPlanet(planet);
    onPlanetClick?.(planet);
  };

  return (
    <div className="relative w-full aspect-square max-w-2xl mx-auto">
      {/* Chart Container */}
      <div className="relative w-full h-full border-2 border-purple-500 rounded-lg bg-gradient-to-br from-slate-900 to-slate-800">
        {/* Render 12 Houses */}
        {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12].map((houseNum) => {
          const position = getHousePosition(houseNum);
          const planets = getPlanetsInHouse(houseNum);
          const isAscendant = houseNum === 1;
          
          return (
            <div
              key={houseNum}
              className={`absolute p-2 border border-slate-600 rounded transition-all ${
                isAscendant ? 'bg-purple-900/50 border-purple-400' : 
                houseNum % 2 === 0 ? 'bg-slate-700/50' : 'bg-slate-800/50'
              } ${hoveredHouse === houseNum ? 'ring-2 ring-purple-400' : ''}`}
              style={position}
              onMouseEnter={() => setHoveredHouse(houseNum)}
              onMouseLeave={() => setHoveredHouse(null)}
            >
              {/* House Number */}
              <div className="text-xs font-bold text-purple-300 mb-1">
                {houseNum}
              </div>
              
              {/* Ascendant Marker */}
              {isAscendant && (
                <div className="text-xs text-purple-400 mb-1">↑ Lagna</div>
              )}
              
              {/* Planets in House */}
              <div className="flex flex-wrap gap-1">
                {planets.map((planet) => (
                  <button
                    key={planet.name}
                    onClick={() => handlePlanetClick(planet)}
                    className="px-1 py-0.5 rounded text-xs font-medium hover:ring-2 hover:ring-white transition-all"
                    style={{ backgroundColor: PLANET_COLORS[planet.name] }}
                    title={`${planet.name} - ${planet.rasi.name}`}
                  >
                    {PLANET_ABBREVIATIONS[planet.name]}
                    {planet.isRetrograde && (
                      <span className="text-red-400 ml-0.5">R</span>
                    )}
                  </button>
                ))}
              </div>
              
              {/* Rasi Name */}
              <div className="text-xs text-slate-400 mt-1">
                {chartData.houseCusps[houseNum - 1]?.toFixed(0)}°
              </div>
            </div>
          );
        })}
      </div>

      {/* Planet Details Modal */}
      {selectedPlanet && (
        <PlanetDetailsModal
          planet={selectedPlanet}
          chartData={chartData}
          onClose={() => setSelectedPlanet(null)}
        />
      )}
    </div>
  );
}
```

### 3.4 South Indian Chart Component (`src/components/charts/SouthIndianChart.tsx`)

```typescript
'use client';

import { useState } from 'react';
import { ChartData, ChartPlanet } from './chart-types';
import { PLANET_COLORS, PLANET_ABBREVIATIONS } from './chart-colors';
import PlanetDetailsModal from './PlanetDetailsModal';

interface SouthIndianChartProps {
  chartData: ChartData;
  onPlanetClick?: (planet: ChartPlanet) => void;
}

const RASI_ORDER = [
  'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
];

export default function SouthIndianChart({ chartData, onPlanetClick }: SouthIndianChartProps) {
  const [selectedPlanet, setSelectedPlanet] = useState<ChartPlanet | null>(null);
  const [hoveredRasi, setHoveredRasi] = useState<string | null>(null);

  // Get house number for a rasi based on ascendant
  const getHouseForRasi = (rasiName: string): number => {
    const ascRasiNum = chartData.ascendant.rasiNumber;
    const rasiIndex = RASI_ORDER.indexOf(rasiName);
    const houseNum = ((rasiIndex - ascRasiNum + 1 + 12) % 12) || 12;
    return houseNum;
  };

  const getPlanetsInRasi = (rasiName: string): ChartPlanet[] => {
    return chartData.planets.filter(p => p.rasi.name === rasiName);
  };

  const handlePlanetClick = (planet: ChartPlanet) => {
    setSelectedPlanet(planet);
    onPlanetClick?.(planet);
  };

  // Calculate position for each rasi (circular layout)
  const getRasiPosition = (rasiIndex: number) => {
    const angle = (rasiIndex * 30) - 90; // Start from top (Aries = 0°)
    const radius = 40; // Percentage from center
    const x = 50 + radius * Math.cos((angle * Math.PI) / 180);
    const y = 50 + radius * Math.sin((angle * Math.PI) / 180);
    return { left: `${x}%`, top: `${y}%` };
  };

  return (
    <div className="relative w-full aspect-square max-w-2xl mx-auto">
      <div className="relative w-full h-full border-2 border-purple-500 rounded-full bg-gradient-to-br from-slate-900 to-slate-800">
        {/* Center - Ascendant Info */}
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center">
            <div className="text-lg font-bold text-purple-300">
              {chartData.ascendant.rasi}
            </div>
            <div className="text-xs text-slate-400">Lagna</div>
            <div className="text-xs text-slate-500">
              {chartData.ascendant.degree.toFixed(2)}°
            </div>
          </div>
        </div>

        {/* Render 12 Rasis */}
        {RASI_ORDER.map((rasi, index) => {
          const position = getRasiPosition(index);
          const houseNum = getHouseForRasi(rasi);
          const planets = getPlanetsInRasi(rasi);
          const isAscendant = rasi === chartData.ascendant.rasi;

          return (
            <div
              key={rasi}
              className={`absolute w-20 h-20 p-2 border rounded-lg transform -translate-x-1/2 -translate-y-1/2 transition-all ${
                isAscendant
                  ? 'bg-purple-900/50 border-purple-400'
                  : 'bg-slate-800/50 border-slate-600'
              } ${hoveredRasi === rasi ? 'ring-2 ring-purple-400 scale-110' : ''}`}
              style={position}
              onMouseEnter={() => setHoveredRasi(rasi)}
              onMouseLeave={() => setHoveredRasi(null)}
            >
              {/* Rasi Name */}
              <div className="text-xs font-bold text-purple-300 text-center mb-1">
                {rasi.substring(0, 3)}
              </div>

              {/* House Number */}
              <div className="text-xs text-slate-400 text-center mb-1">
                H{houseNum}
              </div>

              {/* Planets */}
              <div className="flex flex-wrap gap-0.5 justify-center">
                {planets.map((planet) => (
                  <button
                    key={planet.name}
                    onClick={() => handlePlanetClick(planet)}
                    className="px-1 py-0.5 rounded text-xs font-medium hover:ring-2 hover:ring-white transition-all"
                    style={{ backgroundColor: PLANET_COLORS[planet.name] }}
                    title={`${planet.name} - House ${planet.house}`}
                  >
                    {PLANET_ABBREVIATIONS[planet.name]}
                    {planet.isRetrograde && (
                      <span className="text-red-400 ml-0.5">R</span>
                    )}
                  </button>
                ))}
              </div>
            </div>
          );
        })}
      </div>

      {/* Planet Details Modal */}
      {selectedPlanet && (
        <PlanetDetailsModal
          planet={selectedPlanet}
          chartData={chartData}
          onClose={() => setSelectedPlanet(null)}
        />
      )}
    </div>
  );
}
```

### 3.5 Chart Container (`src/components/charts/ChartContainer.tsx`)

```typescript
'use client';

import { useState, useEffect } from 'react';
import { ChartData } from './chart-types';
import NorthIndianChart from './NorthIndianChart';
import SouthIndianChart from './SouthIndianChart';
import PlanetaryStrengthPanel from './PlanetaryStrengthPanel';

interface ChartContainerProps {
  chartData: ChartData;
  eventId: number;
  eventDate: string;
}

type ChartType = 'north' | 'south';

export default function ChartContainer({ chartData, eventId, eventDate }: ChartContainerProps) {
  const [chartType, setChartType] = useState<ChartType>('north');
  const [showStrengthPanel, setShowStrengthPanel] = useState(false);

  // Load preference from localStorage
  useEffect(() => {
    const saved = localStorage.getItem('preferredChartType') as ChartType;
    if (saved && (saved === 'north' || saved === 'south')) {
      setChartType(saved);
    }
  }, []);

  // Save preference to localStorage
  const handleChartTypeChange = (type: ChartType) => {
    setChartType(type);
    localStorage.setItem('preferredChartType', type);
  };

  const handleExportChart = () => {
    // Export logic using html2canvas or similar
    console.log('Export chart functionality');
  };

  return (
    <div className="space-y-4">
      {/* Tab Switcher */}
      <div className="flex gap-2 border-b border-slate-700">
        <button
          onClick={() => handleChartTypeChange('north')}
          className={`px-4 py-2 font-medium transition-colors ${
            chartType === 'north'
              ? 'border-b-2 border-purple-500 text-purple-400'
              : 'text-slate-400 hover:text-slate-300'
          }`}
        >
          North Indian
        </button>
        <button
          onClick={() => handleChartTypeChange('south')}
          className={`px-4 py-2 font-medium transition-colors ${
            chartType === 'south'
              ? 'border-b-2 border-purple-500 text-purple-400'
              : 'text-slate-400 hover:text-slate-300'
          }`}
        >
          South Indian
        </button>
      </div>

      {/* Chart Display */}
      <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
        {chartType === 'north' ? (
          <NorthIndianChart chartData={chartData} />
        ) : (
          <SouthIndianChart chartData={chartData} />
        )}
      </div>

      {/* Legend & Controls */}
      <div className="flex flex-wrap gap-4 items-center justify-between bg-slate-800/50 p-4 rounded-lg border border-slate-700">
        {/* Planet Legend */}
        <div className="flex flex-wrap gap-2">
          {Object.entries(chartData.planets).map(([key, planet]) => (
            <div key={planet.name} className="flex items-center gap-1 text-sm">
              <div
                className="w-4 h-4 rounded"
                style={{ backgroundColor: PLANET_COLORS[planet.name] }}
              />
              <span className="text-slate-300">{planet.abbreviation}</span>
            </div>
          ))}
        </div>

        {/* Action Buttons */}
        <div className="flex gap-2">
          <button
            onClick={() => setShowStrengthPanel(!showStrengthPanel)}
            className="px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg transition-colors text-sm"
          >
            {showStrengthPanel ? 'Hide' : 'Show'} Strength Panel
          </button>
          <button
            onClick={handleExportChart}
            className="px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg transition-colors text-sm"
          >
            Export Chart
          </button>
          <button
            onClick={() => window.print()}
            className="px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg transition-colors text-sm"
          >
            Print
          </button>
        </div>
      </div>

      {/* Planetary Strength Panel */}
      {showStrengthPanel && (
        <PlanetaryStrengthPanel planets={chartData.planets} />
      )}
    </div>
  );
}
```

### 3.6 Database Functions (`src/lib/database.ts` additions)

```typescript
// Add to existing database.ts

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
  planetary_positions: any; // JSONB
  planetary_strengths: any; // JSONB
  created_at?: string;
  updated_at?: string;
}

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
      ascendant_nakshatra: data.ascendant_nakshatra,
      ascendant_lord: data.ascendant_lord,
      house_cusps: Array.isArray(data.house_cusps) 
        ? data.house_cusps 
        : JSON.parse(data.house_cusps as string),
      house_system: data.house_system,
      julian_day: data.julian_day,
      sidereal_time: data.sidereal_time,
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
```

### 3.7 Updated House Mapping (`src/lib/houseMapping.ts` additions)

```typescript
// Add new function for ascendant-based mapping

import { ChartData } from '@/components/charts/chart-types';
import { Event, PlanetaryData } from './types';

export interface AscendantBasedHouseMapping {
  house_number: number; // 1-12 based on ascendant
  kalapurushan_house: number; // 1-12 based on Kalapurushan (Aries=1)
  rasi_name: string;
  actual_rasi: string; // The rasi actually containing the event house
  house_significations: string[];
  mapping_reason: string;
  calculation_method: 'ascendant-based';
}

/**
 * Map event to actual house based on ascendant and planetary positions
 */
export function mapEventToActualHouse(
  event: Event,
  chartData: ChartData | null
): AscendantBasedHouseMapping | null {
  if (!chartData) {
    // Fallback to Kalapurushan if no chart data
    return mapEventToHouse(event, null as any);
  }

  // Use event category to determine house significations
  const categoryLower = event.category.toLowerCase();
  
  // Map category to house significations (same logic as before)
  let targetHouseNum = 1; // Default to 1st house
  let mappingReason = 'Default mapping (1st house)';

  // Category-based mapping logic (simplified example)
  if (categoryLower.includes('health') || categoryLower.includes('medical')) {
    targetHouseNum = 6; // Health house
    mappingReason = 'Health-related event mapped to 6th house';
  } else if (categoryLower.includes('wealth') || categoryLower.includes('economic')) {
    targetHouseNum = 2; // Wealth house
    mappingReason = 'Wealth-related event mapped to 2nd house';
  }
  // ... more mappings

  // Get the rasi for this house number based on ascendant
  const ascRasiNum = chartData.ascendant.rasiNumber;
  const rasiIndex = (ascRasiNum + targetHouseNum - 2) % 12;
  const actualRasi = RASI_ORDER[rasiIndex];

  // Get Kalapurushan house (Aries = 1st house)
  const kalapurushanHouse = getKalapurushanHouse(actualRasi);

  return {
    house_number: targetHouseNum,
    kalapurushan_house: kalapurushanHouse,
    rasi_name: actualRasi,
    actual_rasi: actualRasi,
    house_significations: HOUSE_SIGNIFICATIONS[targetHouseNum] || [],
    mapping_reason: mappingReason,
    calculation_method: 'ascendant-based',
  };
}
```

### 3.8 API Endpoint (`src/app/api/chart/calculate/route.ts`)

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { getEventById } from '@/lib/database';

const FLASK_API_URL = process.env.FLASK_API_URL || 'http://localhost:8000';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { eventId } = body;

    if (!eventId) {
      return NextResponse.json(
        { error: 'eventId is required' },
        { status: 400 }
      );
    }

    // Get event with location and time
    const event = await getEventById(eventId);
    if (!event) {
      return NextResponse.json(
        { error: 'Event not found' },
        { status: 404 }
      );
    }

    // Check if event has required data
    if (!event.latitude || !event.longitude || !event.date) {
      return NextResponse.json(
        { error: 'Event missing required location or date data' },
        { status: 400 }
      );
    }

    // Prepare request for Flask API
    const chartRequest = {
      date: event.date,
      time: event.event_time || '12:00:00',
      latitude: event.latitude,
      longitude: event.longitude,
      timezone: event.timezone || 'UTC',
    };

    // Call Flask API
    const response = await fetch(`${FLASK_API_URL}/api/chart/calculate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(chartRequest),
    });

    if (!response.ok) {
      const errorData = await response.json();
      return NextResponse.json(
        { error: errorData.error || 'Failed to calculate chart' },
        { status: response.status }
      );
    }

    const chartData = await response.json();

    return NextResponse.json({
      success: true,
      chart: chartData.chart,
    });
  } catch (error) {
    console.error('Error calculating chart:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

---

## 4. Integration Points

### 4.1 Event Creation Flow

```
User fills form → POST /api/events → createEvent()
                                    ↓
                            Store event in DB
                                    ↓
                            calculateAndStoreCorrelations()
                                    ↓
                    Check if event has time & location
                                    ↓
                    If yes: Calculate chart → Store chart_data
                                    ↓
                            Map to actual house (ascendant-based)
                                    ↓
                            Calculate aspects using actual houses
```

### 4.2 Event Detail Page Flow

```
Load event page → Fetch event data
                        ↓
                 Fetch chart_data (if exists)
                        ↓
            If no chart_data: Show "Calculate Chart" button
                        ↓
            If chart_data exists: Display charts
                        ↓
            Fetch house_mappings (with actual_house_number)
                        ↓
            Fetch planetary_aspects
                        ↓
            Display all components
```

### 4.3 Chart Calculation Flow

```
User clicks "Calculate Chart" → POST /api/chart/calculate
                                        ↓
                                Validate event data
                                        ↓
                        Call Flask API: /api/chart/calculate
                                        ↓
                        Flask: calculate_complete_chart()
                                        ↓
                        Return chart data (JSON)
                                        ↓
                        Store in event_chart_data table
                                        ↓
                        Update house_mappings with actual_house_number
                                        ↓
                        Recalculate aspects with actual houses
                                        ↓
                        Refresh page to show charts
```

---

## 5. Testing Strategy

### 5.1 Unit Tests

#### Chart Utilities
```typescript
// tests/chart-utils.test.ts
describe('chart-utils', () => {
  test('converts degrees to rasi correctly', () => {
    expect(degreesToRasi(0)).toBe('Aries');
    expect(degreesToRasi(30)).toBe('Taurus');
    // ... more tests
  });

  test('calculates house cusps correctly', () => {
    const cusps = calculateHouseCusps(225.5, 13.08, 80.27);
    expect(cusps).toHaveLength(12);
    expect(cusps[0]).toBeCloseTo(225.5, 1); // Ascendant
  });
});
```

#### House Mapping
```typescript
// tests/houseMapping.test.ts
describe('mapEventToActualHouse', () => {
  test('maps health event to 6th house correctly', () => {
    const event = { category: 'Health', ... };
    const chartData = { ascendant: { rasiNumber: 1 }, ... };
    const mapping = mapEventToActualHouse(event, chartData);
    expect(mapping.house_number).toBe(6);
    expect(mapping.calculation_method).toBe('ascendant-based');
  });
});
```

### 5.2 Integration Tests

#### API Endpoints
```typescript
// tests/api/chart.test.ts
describe('POST /api/chart/calculate', () => {
  test('calculates chart for event with location', async () => {
    const event = await createTestEvent({
      latitude: 13.08,
      longitude: 80.27,
      date: '2025-12-12',
      event_time: '14:30:00',
    });
    
    const response = await fetch('/api/chart/calculate', {
      method: 'POST',
      body: JSON.stringify({ eventId: event.id }),
    });
    
    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data.chart.ascendant_rasi).toBe('Scorpio');
  });
});
```

### 5.3 Component Tests

```typescript
// tests/components/NorthIndianChart.test.tsx
describe('NorthIndianChart', () => {
  test('renders all 12 houses', () => {
    const { container } = render(<NorthIndianChart chartData={mockChartData} />);
    const houses = container.querySelectorAll('[data-house]');
    expect(houses).toHaveLength(12);
  });

  test('shows planets in correct houses', () => {
    const { getByText } = render(<NorthIndianChart chartData={mockChartData} />);
    expect(getByText('Su')).toBeInTheDocument();
  });
});
```

### 5.4 E2E Test Scenarios

1. **Create Event → Calculate Chart → View Chart**
   - Create event with location and time
   - Navigate to event detail page
   - Click "Calculate Chart"
   - Verify chart displays correctly
   - Verify planet positions are correct

2. **Switch Chart Types**
   - View North Indian chart
   - Switch to South Indian chart
   - Verify preference is saved
   - Refresh page and verify preference persists

3. **Planet Interactions**
   - Click on a planet in chart
   - Verify modal opens with correct planet data
   - Verify strength indicators display correctly

---

## 6. Migration Path

### 6.1 Database Migrations

#### Migration 004: Add Location Accuracy (if needed)
```sql
-- database_migrations/004_add_location_accuracy.sql
ALTER TABLE events
ADD COLUMN IF NOT EXISTS geocoding_confidence REAL,
ADD COLUMN IF NOT EXISTS geocoding_source TEXT;
```

#### Migration 005: Backfill Chart Data for Existing Events
```sql
-- database_migrations/005_backfill_chart_data.sql
-- This is a reference migration - actual backfill done via Python script
-- See: scripts/backfill_event_charts.py
```

### 6.2 Backfill Script

```python
# scripts/backfill_event_charts.py
"""
Backfill chart data for existing events that have location and time.
"""

import os
import sys
from dotenv import load_dotenv
from supabase import create_client
import requests
from typing import List, Dict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(SCRIPT_DIR, '.env.local'))

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
FLASK_API_URL = os.getenv('FLASK_API_URL', 'http://localhost:8000')

def get_events_needing_charts(supabase) -> List[Dict]:
    """Get events that need chart calculation."""
    response = supabase.table('events').select('*').execute()
    events = response.data
    
    # Filter events that have location but no chart data
    events_needing_charts = []
    for event in events:
        if (event.get('latitude') and event.get('longitude') and event.get('date')):
            # Check if chart data exists
            chart_response = supabase.table('event_chart_data').select('id').eq('event_id', event['id']).execute()
            if not chart_response.data:
                events_needing_charts.append(event)
    
    return events_needing_charts

def calculate_and_store_chart(supabase, event: Dict) -> bool:
    """Calculate and store chart for an event."""
    try:
        chart_request = {
            'date': event['date'],
            'time': event.get('event_time', '12:00:00'),
            'latitude': event['latitude'],
            'longitude': event['longitude'],
            'timezone': event.get('timezone', 'UTC'),
        }
        
        response = requests.post(
            f'{FLASK_API_URL}/api/chart/calculate',
            json=chart_request,
            timeout=30
        )
        
        if not response.ok:
            print(f"❌ Failed to calculate chart for event {event['id']}: {response.text}")
            return False
        
        chart_data = response.json()['chart']
        
        # Store in database
        chart_record = {
            'event_id': event['id'],
            'ascendant_degree': chart_data['ascendant_degree'],
            'ascendant_rasi': chart_data['ascendant_rasi'],
            'ascendant_rasi_number': chart_data['ascendant_rasi_number'],
            'ascendant_nakshatra': chart_data.get('ascendant_nakshatra'),
            'ascendant_lord': chart_data['ascendant_lord'],
            'house_cusps': chart_data['house_cusps'],
            'house_system': chart_data['house_system'],
            'julian_day': chart_data['julian_day'],
            'sidereal_time': chart_data.get('sidereal_time'),
            'ayanamsa': chart_data['ayanamsa'],
            'planetary_positions': chart_data['planetary_positions'],
            'planetary_strengths': chart_data['planetary_strengths'],
        }
        
        result = supabase.table('event_chart_data').upsert([chart_record], on_conflict='event_id').execute()
        
        if result.data:
            print(f"✅ Stored chart for event {event['id']}: {event.get('title', 'Untitled')}")
            return True
        else:
            print(f"❌ Failed to store chart for event {event['id']}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing event {event['id']}: {e}")
        return False

def main():
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Error: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set")
        sys.exit(1)
    
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    print("🔍 Finding events that need chart calculations...")
    events = get_events_needing_charts(supabase)
    
    if not events:
        print("✅ No events need chart calculations")
        return
    
    print(f"📊 Found {len(events)} events needing chart calculations")
    
    success_count = 0
    for i, event in enumerate(events, 1):
        print(f"\n[{i}/{len(events)}] Processing event {event['id']}...")
        if calculate_and_store_chart(supabase, event):
            success_count += 1
    
    print(f"\n✅ Completed: {success_count}/{len(events)} charts calculated successfully")

if __name__ == '__main__':
    main()
```

### 6.3 Backward Compatibility

1. **Events without chart data**: Show "Calculate Chart" button
2. **Events with only Kalapurushan mapping**: Keep existing data, add `calculation_method = 'kalapurushan'`
3. **Events without location**: Cannot calculate chart, show message
4. **Events without time**: Use 12:00:00 as default, set `has_accurate_time = false`

---

## 7. Database Schema Updates

### Existing Tables (Already Created via Migrations 001-003)

- ✅ `events` table with `event_time`, `timezone`, `has_accurate_time`
- ✅ `event_chart_data` table (migration 002)
- ✅ `event_house_mappings` with `actual_house_number`, `calculation_method` (migration 003)

### No Additional Migrations Required

All necessary schema changes are already in place from previous migrations.

---

## 8. Next Steps & Priority Order

### Immediate (Day 1-2):
1. Create type definitions and utilities
2. Set up database functions
3. Create basic chart components

### Short-term (Day 3-4):
1. Add interactivity
2. Integrate with event page
3. Test with real data

### Medium-term (Day 5-6):
1. Enhanced analysis updates
2. Migration and backfill
3. Performance optimization

### Long-term (Future):
1. AI interpretation integration
2. Chart export improvements
3. Additional chart types (D1, D9, etc.)

---

## 9. Success Criteria

✅ **Functional:**
- Both chart types render correctly
- Planets appear in correct houses/rasis
- Interactivity works (hover, click, modal)
- Chart calculation works for events with location/time
- House mappings use actual houses

✅ **Technical:**
- No TypeScript errors
- All API endpoints return correct data
- Database queries are optimized
- Components are responsive
- Loading states are appropriate

✅ **User Experience:**
- Charts are visually clear
- Interactions are intuitive
- Export/print functions work
- Mobile-responsive design
- Fast load times

---

**End of Implementation Plan**

