import Link from 'next/link';
import { getEvents, getPlanetaryData } from '@/lib/database';
import { format, subDays } from 'date-fns';
import PlanetaryImpactVisualization from '@/components/dashboard/PlanetaryImpactVisualization';

/**
 * Simplified Dashboard View
 * Shows overview statistics and latest events in a clean, simple format
 */
export default async function DashboardPage() {
  // Get latest events (already sorted by created_at DESC)
  const allEvents = await getEvents();
  const latestEvents = allEvents.slice(0, 10); // Latest 10 events
  
  // Get events from last 7 days
  const sevenDaysAgo = subDays(new Date(), 7).toISOString().split('T')[0];
  const recentEvents = allEvents.filter(e => e.date >= sevenDaysAgo);
  
  // Calculate statistics
  const totalEvents = allEvents.length;
  const todayEvents = allEvents.filter(e => {
    const eventDate = new Date(e.date).toISOString().split('T')[0];
    const today = new Date().toISOString().split('T')[0];
    return eventDate === today;
  }).length;
  
  const eventsByCategory = allEvents.reduce((acc, event) => {
    const category = event.category || 'Other';
    acc[category] = (acc[category] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);
  
  const eventsByImpact = allEvents.reduce((acc, event) => {
    acc[event.impact_level] = (acc[event.impact_level] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);
  
  // Get most active categories (top 5)
  const topCategories = Object.entries(eventsByCategory)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 5);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
            Dashboard
          </h1>
          <p className="text-slate-400 mt-2">Overview of events, correlations, and astrological analysis</p>
        </div>
        <div className="flex gap-3">
          <Link
            href="/events/new"
            className="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg transition-colors text-sm font-medium"
          >
            + New Event
          </Link>
          <Link
            href="/jobs"
            className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg transition-colors text-sm font-medium"
          >
            Run Collection
          </Link>
        </div>
      </div>

      {/* Key Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-gradient-to-br from-purple-800/50 to-purple-900/50 p-6 rounded-lg border border-purple-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-purple-300 mb-1">Total Events</p>
              <p className="text-3xl font-bold text-white">{totalEvents}</p>
            </div>
            <div className="text-4xl opacity-50">📅</div>
          </div>
          <p className="text-xs text-purple-200 mt-2">{todayEvents} today</p>
        </div>

        <div className="bg-gradient-to-br from-blue-800/50 to-blue-900/50 p-6 rounded-lg border border-blue-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-blue-300 mb-1">Recent Events</p>
              <p className="text-3xl font-bold text-white">{recentEvents.length}</p>
            </div>
            <div className="text-4xl opacity-50">⚡</div>
          </div>
          <p className="text-xs text-blue-200 mt-2">Last 7 days</p>
        </div>

        <div className="bg-gradient-to-br from-green-800/50 to-green-900/50 p-6 rounded-lg border border-green-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-green-300 mb-1">Categories</p>
              <p className="text-3xl font-bold text-white">{Object.keys(eventsByCategory).length}</p>
            </div>
            <div className="text-4xl opacity-50">🏷️</div>
          </div>
          <p className="text-xs text-green-200 mt-2">Event types tracked</p>
        </div>

        <div className="bg-gradient-to-br from-yellow-800/50 to-yellow-900/50 p-6 rounded-lg border border-yellow-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-yellow-300 mb-1">High Impact</p>
              <p className="text-3xl font-bold text-white">
                {(eventsByImpact['high'] || 0) + (eventsByImpact['critical'] || 0)}
              </p>
            </div>
            <div className="text-4xl opacity-50">🔥</div>
          </div>
          <p className="text-xs text-yellow-200 mt-2">High/Critical events</p>
        </div>
      </div>

      {/* Two Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Latest Events - Takes 2 columns */}
        <div className="lg:col-span-2 space-y-4">
          <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-2xl font-semibold">📋 Latest Events</h2>
              <Link
                href="/events"
                className="text-sm text-purple-400 hover:text-purple-300"
              >
                View All →
              </Link>
            </div>
            
            {latestEvents.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-slate-400 mb-4">No events yet.</p>
                <Link
                  href="/events/new"
                  className="text-purple-400 hover:text-purple-300 underline"
                >
                  Create your first event
                </Link>
              </div>
            ) : (
              <div className="space-y-3">
                {latestEvents.map((event) => (
                  <Link
                    key={event.id}
                    href={`/events/${event.id}`}
                    className="block bg-slate-900/50 hover:bg-slate-900/70 p-4 rounded-lg border border-slate-700 transition-colors"
                  >
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <h3 className="font-semibold text-lg">{event.title}</h3>
                          <span className={`text-xs px-2 py-1 rounded font-medium ${
                            event.impact_level === 'critical' ? 'bg-red-900/50 text-red-200' :
                            event.impact_level === 'high' ? 'bg-orange-900/50 text-orange-200' :
                            event.impact_level === 'medium' ? 'bg-yellow-900/50 text-yellow-200' :
                            'bg-green-900/50 text-green-200'
                          }`}>
                            {event.impact_level.toUpperCase()}
                          </span>
                        </div>
                        <div className="flex flex-wrap items-center gap-3 text-sm text-slate-400">
                          <span>{format(new Date(event.date), 'MMM dd, yyyy')}</span>
                          {event.location && (
                            <>
                              <span>•</span>
                              <span>{event.location}</span>
                            </>
                          )}
                          <span>•</span>
                          <span className="text-purple-300">{event.category}</span>
                          {event.created_at && (
                            <>
                              <span>•</span>
                              <span className="text-xs text-slate-500">
                                {format(new Date(event.created_at), 'MMM dd, HH:mm')}
                              </span>
                            </>
                          )}
                        </div>
                        {event.description && (
                          <p className="text-sm text-slate-300 mt-2 line-clamp-2">
                            {event.description}
                          </p>
                        )}
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Sidebar - Quick Stats and Actions */}
        <div className="space-y-4">
          {/* Top Categories */}
          <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
            <h3 className="text-lg font-semibold mb-4">📊 Top Categories</h3>
            <div className="space-y-3">
              {topCategories.length === 0 ? (
                <p className="text-sm text-slate-400">No categories yet</p>
              ) : (
                topCategories.map(([category, count]) => (
                  <div key={category} className="flex items-center justify-between">
                    <span className="text-slate-300 text-sm">{category}</span>
                    <div className="flex items-center gap-2">
                      <div className="w-24 bg-slate-700 rounded-full h-2">
                        <div
                          className="bg-purple-500 h-2 rounded-full"
                          style={{ width: `${(count / totalEvents) * 100}%` }}
                        ></div>
                      </div>
                      <span className="font-semibold text-purple-400 w-8 text-right text-sm">
                        {count}
                      </span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* Impact Distribution */}
          <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
            <h3 className="text-lg font-semibold mb-4">⚡ Impact Levels</h3>
            <div className="space-y-2">
              {(['critical', 'high', 'medium', 'low'] as const).map((level) => {
                const count = eventsByImpact[level] || 0;
                const percentage = totalEvents > 0 ? (count / totalEvents) * 100 : 0;
                return (
                  <div key={level} className="flex items-center justify-between">
                    <span className={`text-sm capitalize ${
                      level === 'critical' ? 'text-red-400' :
                      level === 'high' ? 'text-orange-400' :
                      level === 'medium' ? 'text-yellow-400' :
                      'text-green-400'
                    }`}>
                      {level}
                    </span>
                    <div className="flex items-center gap-2">
                      <div className="w-20 bg-slate-700 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full ${
                            level === 'critical' ? 'bg-red-500' :
                            level === 'high' ? 'bg-orange-500' :
                            level === 'medium' ? 'bg-yellow-500' :
                            'bg-green-500'
                          }`}
                          style={{ width: `${percentage}%` }}
                        ></div>
                      </div>
                      <span className="font-semibold text-slate-300 w-8 text-right text-sm">
                        {count}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Quick Actions */}
          <div className="bg-gradient-to-br from-purple-800/30 to-blue-800/30 p-6 rounded-lg border border-purple-700/50">
            <h3 className="text-lg font-semibold mb-4">🚀 Quick Actions</h3>
            <div className="space-y-2">
              <Link
                href="/events/new"
                className="block w-full bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg transition-colors text-center text-sm font-medium"
              >
                ➕ Add New Event
              </Link>
              <Link
                href="/analysis"
                className="block w-full bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg transition-colors text-center text-sm font-medium"
              >
                🔮 View Analysis
              </Link>
              <Link
                href="/house-analysis"
                className="block w-full bg-green-600 hover:bg-green-700 px-4 py-2 rounded-lg transition-colors text-center text-sm font-medium"
              >
                🏠 House & Aspects
              </Link>
              <Link
                href="/jobs"
                className="block w-full bg-yellow-600 hover:bg-yellow-700 px-4 py-2 rounded-lg transition-colors text-center text-sm font-medium"
              >
                ⚙️ Run Job
              </Link>
            </div>
          </div>

          {/* Recent Activity Summary */}
          <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
            <h3 className="text-lg font-semibold mb-4">📈 Activity Summary</h3>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between">
                <span className="text-slate-400">Last 7 days</span>
                <span className="font-semibold text-blue-400">{recentEvents.length} events</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Today</span>
                <span className="font-semibold text-green-400">{todayEvents} events</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Latest event</span>
                <span className="font-semibold text-purple-400">
                  {latestEvents[0] 
                    ? format(new Date(latestEvents[0].created_at || latestEvents[0].date), 'MMM dd')
                    : 'None'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Planetary Impact Analysis Section */}
      <div className="mt-6">
        <PlanetaryImpactVisualization />
      </div>
    </div>
  );
}

