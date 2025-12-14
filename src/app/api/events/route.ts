import { NextRequest, NextResponse } from 'next/server';
import { getEvents, createEvent, getFilteredEvents, EventFilter } from '@/lib/database';
import { calculateAndStoreCorrelations } from '@/lib/storeCorrelations';
import { Event } from '@/lib/types';

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const date = searchParams.get('date') || undefined;

    // Check if filters are present
    const startDate = searchParams.get('startDate') || undefined;
    const endDate = searchParams.get('endDate') || undefined;
    const planets = searchParams.get('planets')?.split(',').filter(p => p) || undefined;
    const categories = searchParams.get('categories')?.split(',').filter(c => c) || undefined;
    const impactLevels = searchParams.get('impactLevels')?.split(',').filter(i => i) || undefined;
    const eventType = searchParams.get('eventType') as 'world' | 'personal' | undefined;

    // If any filters are present, use getFilteredEvents
    if (startDate || endDate || planets || categories || impactLevels || eventType) {
      const filters: EventFilter = {
        startDate,
        endDate,
        planets,
        categories,
        impactLevels,
        eventType,
      };

      const events = await getFilteredEvents(filters);
      return NextResponse.json(events);
    }

    // Otherwise use the simple getEvents
    const events = await getEvents(date);
    return NextResponse.json(events);
  } catch (error) {
    console.error('Error fetching events:', error);
    return NextResponse.json(
      { error: 'Failed to fetch events' },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    // Validate required fields
    if (!body.date || !body.title || !body.category) {
      return NextResponse.json(
        { error: 'Missing required fields: date, title, category' },
        { status: 400 }
      );
    }

    const eventData: Omit<Event, 'id' | 'created_at' | 'updated_at'> = {
      date: body.date,
      event_time: body.event_time || undefined,
      timezone: body.timezone || undefined,
      has_accurate_time: body.has_accurate_time ?? undefined,
      title: body.title,
      description: body.description || '',
      category: body.category || '',
      location: body.location || '',
      latitude: body.latitude ?? undefined,
      longitude: body.longitude ?? undefined,
      impact_level: body.impact_level || 'medium',
      event_type: body.event_type || 'world',
      tags: body.tags || [],
    };

    const event = await createEvent(eventData);
    
    if (!event) {
      return NextResponse.json(
        { error: 'Failed to create event' },
        { status: 500 }
      );
    }

    // Calculate and store planetary correlations asynchronously (non-blocking)
    if (event.id) {
      calculateAndStoreCorrelations(event).catch(error => {
        console.error('Error storing correlations (non-blocking):', error);
      });
    }

    return NextResponse.json(event, { status: 201 });
  } catch (error) {
    console.error('Error creating event:', error);
    return NextResponse.json(
      { error: 'Failed to create event' },
      { status: 500 }
    );
  }
}
