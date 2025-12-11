# Database Migrations

This directory contains SQL migration files for evolving the Cosmic Diary database schema.

## Migration Files

### 001_add_time_to_events.sql
Adds time-related fields to the events table:
- `event_time` (TIME) - Time when event occurred
- `timezone` (TEXT) - Timezone string (IANA format)
- `has_accurate_time` (BOOLEAN) - Flag for time precision

**Status**: Ready to apply  
**Date**: 2025-12-11

### 002_create_event_chart_data_table.sql
Creates new table to store complete astrological chart data:
- `event_chart_data` table with 16 columns
- Stores ascendant, house cusps, planetary positions, and strengths
- 1:1 relationship with events table
- Includes 6 indexes (3 GIN indexes for JSONB fields)

**Status**: Ready to apply  
**Date**: 2025-12-11  
**Dependencies**: Requires migration 001 (time fields on events)

## How to Apply Migrations

### Method 1: Supabase Dashboard (Recommended)

1. Log in to your Supabase Dashboard
2. Navigate to **SQL Editor**
3. Click **New Query**
4. Copy the contents of the migration file
5. Paste into the editor
6. Click **Run** or press `Ctrl+Enter`
7. Verify success message

### Method 2: Command Line (psql)

```bash
psql -h your-db-host -U postgres -d postgres -f database_migrations/001_add_time_to_events.sql
```

### Method 3: Supabase CLI

```bash
supabase db push
# Or
supabase migration up
```

## Migration Order

Always apply migrations in numerical order:
- `001_add_time_to_events.sql` (first)
- `002_...sql` (next)
- etc.

## Verification

After applying a migration, verify it worked:

1. Check the **Table Editor** in Supabase
2. Verify new columns appear in the `events` table
3. Run verification queries included in migration file comments

## Rollback

Each migration may have a corresponding rollback file:
- `001_add_time_to_events_rollback.sql`

**⚠️ Warning**: Rollbacks will delete data. Backup first!

## Best Practices

1. **Test First**: Always test migrations on a development/staging database first
2. **Backup**: Create a database backup before applying migrations
3. **Review**: Read the migration file to understand what it does
4. **Verify**: Run verification queries after applying
5. **Document**: Update your documentation if schema changes affect application code

## Migration Naming Convention

- Format: `###_description.sql`
- Numbers: 001, 002, 003... (zero-padded, sequential)
- Description: Short, lowercase, underscore-separated
- Example: `001_add_time_to_events.sql`

## Notes

- All migrations use `IF NOT EXISTS` / `IF EXISTS` for idempotency
- Migrations are wrapped in transactions (`BEGIN`/`COMMIT`)
- Comments explain each change for future reference

