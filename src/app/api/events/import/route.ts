import { NextRequest, NextResponse } from 'next/server';
import { createEvent } from '@/lib/database';
import { Event } from '@/lib/types';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    // Support both single event and array of events
    const events = Array.isArray(body) ? body : [body];
    const results = [];

    for (const eventData of events) {
      // Validate required fields
      if (!eventData.date || !eventData.title || !eventData.category) {
        results.push({
          success: false,
          error: 'Missing required fields: date, title, category',
          data: eventData,
        });
        continue;
      }

      const event: Omit<Event, 'id' | 'created_at' | 'updated_at'> = {
        date: eventData.date,
        title: eventData.title,
        description: eventData.description || '',
        category: eventData.category || '',
        location: eventData.location || '',
        latitude: eventData.latitude ?? undefined,
        longitude: eventData.longitude ?? undefined,
        impact_level: eventData.impact_level || 'medium',
        event_type: eventData.event_type || 'world',
        tags: eventData.tags || [],
      };

      const created = await createEvent(event);
      
      if (created) {
        results.push({
          success: true,
          data: created,
        });
      } else {
        results.push({
          success: false,
          error: 'Failed to create event',
          data: eventData,
        });
      }
    }

    const successCount = results.filter((r) => r.success).length;
    
    return NextResponse.json({
      imported: successCount,
      total: events.length,
      results,
    });
  } catch (error) {
    console.error('Error importing events:', error);
    return NextResponse.json(
      { error: 'Failed to import events' },
      { status: 500 }
    );
  }
}
