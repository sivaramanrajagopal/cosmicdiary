import { getEvents } from '@/lib/database';
import EventsList from '@/components/EventsList';

export default async function EventsPage() {
  const events = await getEvents();

  return <EventsList initialEvents={events} />;
}
