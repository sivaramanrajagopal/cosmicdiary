import Link from 'next/link';
import { getEvents } from '@/lib/database';
import { format } from 'date-fns';

export default async function EventsPage() {
  const events = await getEvents();

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold">All Events</h2>
        <Link
          href="/events/new"
          className="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg transition-colors"
        >
          Add New Event
        </Link>
      </div>

      {events.length === 0 ? (
        <div className="text-center py-12 bg-slate-800/50 rounded-lg border border-slate-700">
          <p className="text-slate-400 mb-4">No events found.</p>
          <Link
            href="/events/new"
            className="text-purple-400 hover:text-purple-300 underline"
          >
            Create your first event
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          {events.map((event) => (
            <Link
              key={event.id}
              href={`/events/${event.id}`}
              className="block bg-slate-800/50 hover:bg-slate-700/50 p-6 rounded-lg border border-slate-700 transition-colors"
            >
              <div className="flex justify-between items-start mb-3">
                <div className="flex-1">
                  <h3 className="text-xl font-semibold mb-2">{event.title}</h3>
                  {event.description && (
                    <p className="text-slate-400 mb-3">{event.description}</p>
                  )}
                  <div className="flex flex-wrap gap-2">
                    <span className="text-xs bg-purple-900/50 px-3 py-1 rounded">{event.category}</span>
                    <span className="text-xs bg-purple-900/50 px-3 py-1 rounded">{event.location}</span>
                    <span className="text-xs bg-purple-900/50 px-3 py-1 rounded">
                      {format(new Date(event.date), 'MMM dd, yyyy')}
                    </span>
                    {event.tags.map((tag, idx) => (
                      <span key={idx} className="text-xs bg-slate-700/50 px-3 py-1 rounded">
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
                <div className="ml-4 flex flex-col items-end gap-2">
                  <span className={`text-xs px-3 py-1 rounded font-semibold ${
                    event.impact_level === 'critical' ? 'bg-red-950/70 text-red-100' :
                    event.impact_level === 'high' ? 'bg-red-900/50 text-red-200' :
                    event.impact_level === 'medium' ? 'bg-yellow-900/50 text-yellow-200' :
                    'bg-green-900/50 text-green-200'
                  }`}>
                    {event.impact_level.toUpperCase()}
                  </span>
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
