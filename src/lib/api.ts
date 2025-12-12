import { Event } from './types';

export async function fetchEvents(date?: string): Promise<Event[]> {
  try {
    const url = date ? `/api/events?date=${date}` : '/api/events';
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error('Failed to fetch events');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching events:', error);
    return [];
  }
}

export async function fetchEventById(id: string): Promise<Event | null> {
  try {
    const response = await fetch(`/api/events/${id}`);
    
    if (!response.ok) {
      throw new Error('Failed to fetch event');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching event:', error);
    return null;
  }
}

export async function createEvent(event: Omit<Event, 'id' | 'created_at' | 'updated_at'>): Promise<Event | null> {
  try {
    const response = await fetch('/api/events', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(event),
    });
    
    if (!response.ok) {
      throw new Error('Failed to create event');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error creating event:', error);
    return null;
  }
}

export async function fetchPlanetaryData(date: string) {
  try {
    const response = await fetch(`/api/planetary-data?date=${date}`);
    
    if (!response.ok) {
      return null;
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching planetary data:', error);
    return null;
  }
}
