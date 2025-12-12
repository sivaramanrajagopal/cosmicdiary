# Implementation Plan Summary - Quick Reference

## Overview

**Priority 3:** Visual Chart Display Components  
**Priority 4:** Enhanced Analysis & Integration

---

## File Structure Quick View

### New Files to Create (8 files)
```
src/components/charts/
├── NorthIndianChart.tsx          ⬜
├── SouthIndianChart.tsx          ⬜
├── ChartContainer.tsx            ⬜
├── PlanetDetailsModal.tsx        ⬜
├── PlanetaryStrengthPanel.tsx    ⬜
├── chart-utils.ts                ⬜
├── chart-types.ts                ⬜
└── chart-colors.ts               ⬜

src/app/api/chart/calculate/
└── route.ts                      ⬜

scripts/
└── backfill_event_charts.py      ⬜
```

### Files to Update (4 files)
```
src/app/events/[id]/page.tsx      ✅ (Add chart displays)
src/lib/database.ts               ✅ (Add chart functions)
src/lib/types.ts                  ✅ (Add chart types)
src/lib/houseMapping.ts           ✅ (Add ascendant-based mapping)
src/lib/storeCorrelations.ts      ✅ (Integrate chart storage)
```

---

## Implementation Phases (6 Days)

### Phase 1: Foundation (Day 1)
- [ ] Create type definitions (`chart-types.ts`)
- [ ] Create color constants (`chart-colors.ts`)
- [ ] Create utility functions (`chart-utils.ts`)
- [ ] Update `src/lib/types.ts`

**Checkpoint:** Types compile without errors

---

### Phase 2: Database & API (Day 1-2)
- [ ] Verify `event_chart_data` table exists
- [ ] Create API endpoint `/api/chart/calculate`
- [ ] Add database functions: `getEventChartData()`, `storeEventChartData()`
- [ ] Test API with sample event

**Checkpoint:** API returns chart data correctly

---

### Phase 3: Core Components (Day 2-3)
- [ ] Create `NorthIndianChart.tsx` (diamond layout)
- [ ] Create `SouthIndianChart.tsx` (circular layout)
- [ ] Create `ChartContainer.tsx` (tabs + controls)
- [ ] Test with hardcoded data

**Checkpoint:** Basic charts render correctly

---

### Phase 4: Interactivity (Day 3-4)
- [ ] Add planet rendering to charts
- [ ] Create `PlanetDetailsModal.tsx`
- [ ] Create `PlanetaryStrengthPanel.tsx`
- [ ] Add export/print functionality
- [ ] Add hover states and click handlers

**Checkpoint:** All interactions work

---

### Phase 5: Integration (Day 4)
- [ ] Update `src/app/events/[id]/page.tsx`
- [ ] Add chart fetching logic
- [ ] Integrate all components
- [ ] Add loading states
- [ ] Test with real events

**Checkpoint:** Event page displays charts

---

### Phase 6: Enhanced Analysis (Day 5)
- [ ] Update `houseMapping.ts` for ascendant-based
- [ ] Update `storeCorrelations.ts` to store chart data
- [ ] Test house mapping calculations
- [ ] Test aspect calculations

**Checkpoint:** Mappings use actual houses

---

### Phase 7: Migration (Day 5-6)
- [ ] Create backfill script (`backfill_event_charts.py`)
- [ ] Run backfill for existing events
- [ ] Verify data integrity
- [ ] Test with migrated events

**Checkpoint:** Existing events have chart data

---

### Phase 8: Polish (Day 6)
- [ ] Add error boundaries
- [ ] Improve loading states
- [ ] Add accessibility
- [ ] Cross-browser testing
- [ ] Performance optimization

**Checkpoint:** Production-ready

---

## Key Functions to Implement

### Chart Calculation
```typescript
// API: POST /api/chart/calculate
// Input: { eventId }
// Output: { success: true, chart: ChartData }
```

### Database Functions
```typescript
getEventChartData(eventId: number): Promise<EventChartData | null>
storeEventChartData(eventId: number, chartData): Promise<EventChartData | null>
```

### House Mapping
```typescript
mapEventToActualHouse(event: Event, chartData: ChartData): AscendantBasedHouseMapping
```

---

## Testing Checklist

### Unit Tests
- [ ] Chart utility functions
- [ ] House mapping calculations
- [ ] Rasi/degree conversions

### Integration Tests
- [ ] API endpoint `/api/chart/calculate`
- [ ] Database queries
- [ ] Chart data storage

### Component Tests
- [ ] North Indian Chart renders
- [ ] South Indian Chart renders
- [ ] Planet interactions work
- [ ] Modal opens correctly

### E2E Tests
- [ ] Create event → Calculate chart → View chart
- [ ] Switch chart types
- [ ] Click planet → View details
- [ ] Export/print chart

---

## Migration Checklist

### Database
- [ ] Verify all migrations (001-003) are applied
- [ ] Check `event_chart_data` table exists
- [ ] Verify indexes are created

### Data Backfill
- [ ] Run `backfill_event_charts.py` script
- [ ] Verify chart data for existing events
- [ ] Check house mappings are updated

### Backward Compatibility
- [ ] Events without chart data show "Calculate" button
- [ ] Events without location show message
- [ ] Events without time use default (12:00:00)

---

## Dependencies

### Frontend
- React 18+
- Next.js 15
- Tailwind CSS 3.4
- Recharts (for strength panel)

### Backend
- Flask API running
- Swiss Ephemeris configured
- Chart calculation endpoint working

### Database
- Supabase PostgreSQL
- `event_chart_data` table created
- JSONB columns available

---

## Success Criteria

✅ Both chart types render correctly  
✅ Planets appear in correct houses/rasis  
✅ Interactivity works (hover, click, modal)  
✅ Chart calculation works end-to-end  
✅ House mappings use actual houses  
✅ Export/print functions work  
✅ Mobile-responsive  
✅ Fast load times (< 2s)  

---

## Quick Start Commands

```bash
# Run backfill script
python3 scripts/backfill_event_charts.py

# Test chart API
curl -X POST http://localhost:3002/api/chart/calculate \
  -H "Content-Type: application/json" \
  -d '{"eventId": 1}'

# Start development
npm run dev
# Flask API should be on port 8000
```

---

**See full plan:** `IMPLEMENTATION_PLAN_VISUAL_CHARTS.md`

