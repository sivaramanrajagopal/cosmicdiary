import Link from 'next/link';
import { getEvents } from '@/lib/database';

export default async function HomePage() {
  const recentEvents = await getEvents();
  const latestEvents = recentEvents.slice(0, 5);

  return (
    <div className="space-y-8">
      <div className="text-center py-8 sm:py-12">
        <h2 className="text-2xl sm:text-3xl font-bold mb-4 px-4">Welcome to Cosmic Diary</h2>
        <p className="text-slate-300 max-w-2xl mx-auto px-4 text-sm sm:text-base">
          Track world events and analyze their correlations with planetary positions.
          Discover the cosmic influences behind significant global events.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 mb-8">
        <Link 
          href="/events/new" 
          className="bg-purple-800/50 hover:bg-purple-700/50 p-6 rounded-lg border border-purple-700 transition-colors"
        >
          <h3 className="text-xl font-semibold mb-2">Add New Event</h3>
          <p className="text-slate-400">Record a new world event with planetary data</p>
        </Link>

        <Link 
          href="/events" 
          className="bg-purple-800/50 hover:bg-purple-700/50 p-6 rounded-lg border border-purple-700 transition-colors"
        >
          <h3 className="text-xl font-semibold mb-2">View All Events</h3>
          <p className="text-slate-400">Browse through all recorded events</p>
        </Link>

        <Link 
          href="/analysis" 
          className="bg-purple-800/50 hover:bg-purple-700/50 p-6 rounded-lg border border-purple-700 transition-colors"
        >
          <h3 className="text-xl font-semibold mb-2">Analysis</h3>
          <p className="text-slate-400">Analyze patterns and correlations</p>
        </Link>
      </div>

      {latestEvents.length > 0 && (
        <div>
          <h3 className="text-xl sm:text-2xl font-semibold mb-4">Recent Events</h3>
          <div className="space-y-4">
            {latestEvents.map((event) => (
              <Link
                key={event.id}
                href={`/events/${event.id}`}
                className="block bg-slate-800/50 hover:bg-slate-700/50 p-4 rounded-lg border border-slate-700 transition-colors"
              >
                <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-3">
                  <div className="flex-1">
                    <h4 className="font-semibold text-base sm:text-lg">{event.title}</h4>
                    {event.description && (
                      <p className="text-slate-400 text-sm mt-1 line-clamp-2">{event.description.substring(0, 100)}...</p>
                    )}
                    <div className="flex flex-wrap gap-2 mt-2">
                      <span className="text-xs bg-purple-900/50 px-2 py-1 rounded">{event.category}</span>
                      <span className="text-xs bg-purple-900/50 px-2 py-1 rounded">{event.location}</span>
                      <span className="text-xs bg-purple-900/50 px-2 py-1 rounded">{event.date}</span>
                    </div>
                  </div>
                  <span className={`text-xs px-2 py-1 rounded whitespace-nowrap self-start ${
                    event.impact_level === 'critical' ? 'bg-red-950/70' :
                    event.impact_level === 'high' ? 'bg-red-900/50' :
                    event.impact_level === 'medium' ? 'bg-yellow-900/50' :
                    'bg-green-900/50'
                  }`}>
                    {event.impact_level}
                  </span>
                </div>
              </Link>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
