import { NextRequest, NextResponse } from 'next/server';
import { getEvents, createEvent } from '@/lib/database';
import { calculateAndStoreCorrelations } from '@/lib/storeCorrelations';
import { Event } from '@/lib/types';

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const date = searchParams.get('date') || undefined;
    
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
