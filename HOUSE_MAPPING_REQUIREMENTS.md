# House Mapping & Planetary Aspects - Requirements Understanding

## My Understanding (Please Confirm):

### 1. **House System (Bhavas - Parasara Method)**
- **Aries (Mesha) = 1st House** (Ascendant)
- **Taurus (Vrishabha) = 2nd House**
- **Gemini (Mithuna) = 3rd House**
- ... (continuing through signs)
- **Pisces (Meena) = 12th House**

Each Rasi maps directly to a house number (1-12).

### 2. **Event-to-House Mapping**
When an event occurs, determine which house it belongs to based on:
- **Event Category** (e.g., Natural Disaster, War, Economic Event)
- **Event Type** (world vs personal)
- **Traditional House Significations**:
  - 1st House: Self, personality, body, reputation
  - 2nd House: Wealth, family, speech, food
  - 3rd House: Siblings, courage, communication, short journeys
  - 4th House: Mother, home, property, education
  - 5th House: Children, creativity, education, speculation
  - 6th House: Enemies, diseases, debts, service
  - 7th House: Spouse, partnerships, business
  - 8th House: Longevity, transformation, secrets, sudden events
  - 9th House: Father, dharma, higher education, long journeys
  - 10th House: Career, reputation, authority, karma
  - 11th House: Gains, friends, aspirations, income
  - 12th House: Losses, expenses, foreign lands, isolation

### 3. **Planetary Aspects (Drishti)**
Calculate which planets aspect the event's house:

**Traditional Drishti System:**
- **Jupiter**: 5th, 7th, 9th houses from its position (trinal aspects)
- **Saturn**: 3rd, 7th, 10th houses from its position
- **Mars**: 4th, 7th, 8th houses from its position
- **Rahu/Ketu**: 5th, 7th, 9th houses (like Jupiter)
- **Sun/Moon**: 7th house only
- **Mercury/Venus**: 7th house only

### 4. **Data to Store:**
For each event, store:
- **Primary House** (1-12) that the event belongs to
- **House Significations** relevant to the event
- **Planets Aspecting the House** (with aspect type)
- **Planetary Significations** for that event
- **Aspect Strength/Type** (conjunction, trinal, etc.)

## Questions for Confirmation:

1. **House Determination Method:**
   - Should we map based on event category → house significations?
   - Or use event location/time to calculate actual house?
   - Or combination of both?

2. **Event Location:**
   - If event has latitude/longitude, should we calculate:
     - Ascendant (Lagna) for that location/time?
     - Which house the event represents in that chart?

3. **Planetary Aspects:**
   - Use full Drishti system (as above)?
   - Or specific to Parasara methods only?
   - Should we also consider:
     - Planetary conjunctions in the same house?
     - Planets in the house itself?

4. **Storage Structure:**
   - Add fields to existing `events` table?
   - Create new `event_house_mappings` table?
   - Enhance `event_planetary_correlations` table?

5. **Analysis Needs:**
   - Which specific analyses do you want?
   - Patterns like "Mars aspecting 6th house during wars"?
   - Historical correlations between house-aspects and event types?

## Proposed Implementation:

### New Database Structure:
```sql
-- Event House Mappings
CREATE TABLE event_house_mappings (
    id BIGSERIAL PRIMARY KEY,
    event_id BIGINT REFERENCES events(id),
    house_number INT CHECK (house_number BETWEEN 1 AND 12),
    rasi_name TEXT,  -- Aries, Taurus, etc.
    house_significations TEXT[],  -- Array of significations
    mapping_reason TEXT,  -- Why this house was selected
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Event Planetary Aspects
CREATE TABLE event_planetary_aspects (
    id BIGSERIAL PRIMARY KEY,
    event_id BIGINT REFERENCES events(id),
    house_number INT CHECK (house_number BETWEEN 1 AND 12),
    planet_name TEXT,
    aspect_type TEXT,  -- 'conjunction', 'drishti_3rd', 'drishti_7th', etc.
    planet_longitude REAL,
    aspect_strength TEXT,  -- 'strong', 'moderate', 'weak'
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Analysis Functions:
1. **Map Event to House**: Based on category + significations
2. **Calculate Aspects**: Which planets aspect the event's house
3. **Store Correlations**: House + Aspects + Event relationships
4. **Pattern Analysis**: Historical patterns of house-aspect-event correlations

---

**Please confirm if my understanding is correct, and answer the questions above so I can implement this accurately!**

