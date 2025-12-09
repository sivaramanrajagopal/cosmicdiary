import { notFound } from 'next/navigation';
import Link from 'next/link';
import { getEventById, getPlanetaryDataForEvent } from '@/lib/database';
import { format } from 'date-fns';
import TransitTable from '@/components/TransitTable';
import { Event } from '@/lib/types';

async function PlanetaryDataSection({ event }: { event: Event }) {
  const planetaryData = await getPlanetaryDataForEvent(event);
  
  if (!planetaryData || !planetaryData.planetary_data?.planets || planetaryData.planetary_data.planets.length === 0) {
    return (
      <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
        <h3 className="text-2xl font-semibold mb-4">Planetary Positions</h3>
        <p className="text-slate-400">No planetary data available for this date.</p>
      </div>
    );
  }
  
  return (
    <div>
      <h3 className="text-2xl font-semibold mb-4">Planetary Positions</h3>
      <TransitTable planets={planetaryData.planetary_data.planets} />
    </div>
  );
}

export default async function EventDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const eventId = parseInt(id, 10);
  
  if (isNaN(eventId)) {
    notFound();
  }
  
  const event = await getEventById(eventId);

  if (!event) {
    notFound();
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start">
        <div>
          <Link
            href="/events"
            className="text-purple-400 hover:text-purple-300 mb-4 inline-block"
          >
            ← Back to Events
          </Link>
          <h2 className="text-3xl font-bold mb-2">{event.title}</h2>
          <p className="text-slate-400">
            {format(new Date(event.date), 'MMMM dd, yyyy')}
          </p>
        </div>
        <span className={`text-sm px-4 py-2 rounded font-semibold ${
          event.impact_level === 'critical' ? 'bg-red-950/70 text-red-100' :
          event.impact_level === 'high' ? 'bg-red-900/50 text-red-200' :
          event.impact_level === 'medium' ? 'bg-yellow-900/50 text-yellow-200' :
          'bg-green-900/50 text-green-200'
        }`}>
          {event.impact_level.toUpperCase()}
        </span>
      </div>

      <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
        <div className="space-y-4">
          {event.description && (
            <div>
              <h3 className="text-sm font-medium text-slate-400 mb-1">Description</h3>
              <p className="text-white">{event.description}</p>
            </div>
          )}

          <div className="grid grid-cols-2 gap-4">
            <div>
              <h3 className="text-sm font-medium text-slate-400 mb-1">Category</h3>
              <p className="text-white">{event.category}</p>
            </div>
            <div>
              <h3 className="text-sm font-medium text-slate-400 mb-1">Location</h3>
              <p className="text-white">{event.location}</p>
            </div>
            <div>
              <h3 className="text-sm font-medium text-slate-400 mb-1">Type</h3>
              <p className="text-white capitalize">{event.event_type}</p>
            </div>
            {(event.latitude !== undefined && event.longitude !== undefined) && (
              <div>
                <h3 className="text-sm font-medium text-slate-400 mb-1">Coordinates</h3>
                <p className="text-white">{event.latitude?.toFixed(4)}, {event.longitude?.toFixed(4)}</p>
              </div>
            )}
          </div>

          {event.tags.length > 0 && (
            <div>
              <h3 className="text-sm font-medium text-slate-400 mb-2">Tags</h3>
              <div className="flex flex-wrap gap-2">
                {event.tags.map((tag, idx) => (
                  <span
                    key={idx}
                    className="bg-purple-900/50 px-3 py-1 rounded text-sm"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      <PlanetaryDataSection event={event} />
    </div>
  );
}
