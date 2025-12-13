import { getEvents } from '@/lib/database';
import { getHouseMapping, getPlanetaryAspects } from '@/lib/database';
import { getPlanetaryData } from '@/lib/database';
import Link from 'next/link';
import { format } from 'date-fns';

interface EventAnalysis {
  event: any;
  houseMapping: any;
  aspects: any[];
}

export default async function HouseAnalysisPage() {
  const events = await getEvents(); // Already sorted by created_at DESC (latest first)
  
  // Get analysis for all events
  const eventAnalyses: EventAnalysis[] = [];
  
  for (const event of events) {
    if (!event.id) continue;
    
    const houseMapping = await getHouseMapping(event.id);
    const aspects = await getPlanetaryAspects(event.id);
    
    if (houseMapping || aspects.length > 0) {
      eventAnalyses.push({
        event,
        houseMapping,
        aspects,
      });
    }
  }
  
  // Explicitly sort by created_at DESC to ensure latest events first
  // (This adds redundancy but ensures correct order even if DB query changes)
  eventAnalyses.sort((a, b) => {
    const dateA = a.event.created_at ? new Date(a.event.created_at).getTime() : 0;
    const dateB = b.event.created_at ? new Date(b.event.created_at).getTime() : 0;
    return dateB - dateA; // Latest first (descending)
  });
  
  // Group by house number
  const eventsByHouse: Record<number, EventAnalysis[]> = {};
  eventAnalyses.forEach(analysis => {
    if (analysis.houseMapping) {
      const houseNum = analysis.houseMapping.house_number;
      if (!eventsByHouse[houseNum]) {
        eventsByHouse[houseNum] = [];
      }
      eventsByHouse[houseNum].push(analysis);
    }
  });
  
  // Count aspects by type
  const aspectCounts: Record<string, number> = {};
  eventAnalyses.forEach(analysis => {
    analysis.aspects.forEach(aspect => {
      const key = `${aspect.aspect_type}_${aspect.planet_name}`;
      aspectCounts[key] = (aspectCounts[key] || 0) + 1;
    });
  });

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold">House & Aspect Analysis</h2>
          <p className="text-slate-400 mt-2">
            Traditional Vedic Astrology House Mappings and Planetary Aspects
            <span className="ml-3 text-xs bg-purple-900/50 px-2 py-1 rounded">
              Latest events first
            </span>
          </p>
        </div>
        <Link
          href="/analysis"
          className="text-purple-400 hover:text-purple-300"
        >
          ← Back to Analysis
        </Link>
      </div>

      {/* Summary Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
          <h3 className="text-sm font-medium text-slate-400 mb-2">Total Events Analyzed</h3>
          <p className="text-3xl font-bold text-purple-400">{eventAnalyses.length}</p>
        </div>
        <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
          <h3 className="text-sm font-medium text-slate-400 mb-2">House Mappings</h3>
          <p className="text-3xl font-bold text-blue-400">
            {Object.keys(eventsByHouse).length}
          </p>
          <p className="text-xs text-slate-500 mt-1">Unique houses</p>
        </div>
        <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
          <h3 className="text-sm font-medium text-slate-400 mb-2">Planetary Aspects</h3>
          <p className="text-3xl font-bold text-green-400">
            {eventAnalyses.reduce((sum, a) => sum + a.aspects.length, 0)}
          </p>
          <p className="text-xs text-slate-500 mt-1">Total aspects recorded</p>
        </div>
        <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
          <h3 className="text-sm font-medium text-slate-400 mb-2">Events with Aspects</h3>
          <p className="text-3xl font-bold text-yellow-400">
            {eventAnalyses.filter(a => a.aspects.length > 0).length}
          </p>
          <p className="text-xs text-slate-500 mt-1">Events with planetary aspects</p>
        </div>
      </div>

      {/* House Distribution */}
      {Object.keys(eventsByHouse).length > 0 && (
        <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
          <h3 className="text-lg font-semibold mb-4">📊 Events by House Distribution</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
            {Array.from({ length: 12 }, (_, i) => i + 1).map(houseNum => {
              const houseEvents = eventsByHouse[houseNum] || [];
              const rasiNames = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                               'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'];
              
              return (
                <div key={houseNum} className="text-center">
                  <div className="text-2xl font-bold text-purple-400">{houseEvents.length}</div>
                  <div className="text-sm text-slate-300">House {houseNum}</div>
                  <div className="text-xs text-slate-500">{rasiNames[houseNum - 1]}</div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Main Analysis Table */}
      <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
        <h3 className="text-lg font-semibold mb-4">🔮 Event House Mappings & Planetary Aspects</h3>
        
        {eventAnalyses.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-slate-400 mb-4">No house mappings found.</p>
            <p className="text-sm text-slate-500">
              House mappings are calculated automatically when events are created.
            </p>
            <Link
              href="/api/events/recalculate-correlations"
              className="mt-4 inline-block text-purple-400 hover:text-purple-300 underline"
            >
              Recalculate for existing events
            </Link>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-700">
                  <th className="text-left py-3 px-4 font-semibold">Event</th>
                  <th className="text-left py-3 px-4 font-semibold">Date</th>
                  <th className="text-left py-3 px-4 font-semibold">House</th>
                  <th className="text-left py-3 px-4 font-semibold">Rasi</th>
                  <th className="text-left py-3 px-4 font-semibold">Planetary Aspects</th>
                  <th className="text-left py-3 px-4 font-semibold">Captured</th>
                  <th className="text-left py-3 px-4 font-semibold">Action</th>
                </tr>
              </thead>
              <tbody>
                {eventAnalyses.map(({ event, houseMapping, aspects }) => (
                  <tr key={event.id} className="border-b border-slate-700/50 hover:bg-slate-700/30">
                    <td className="py-3 px-4">
                      <div>
                        <div className="font-medium">{event.title}</div>
                        <div className="text-xs text-slate-400">{event.category}</div>
                      </div>
                    </td>
                    <td className="py-3 px-4 text-slate-300">
                      {format(new Date(event.date), 'MMM dd, yyyy')}
                    </td>
                    <td className="py-3 px-4">
                      {houseMapping ? (
                        <div>
                          <span className="font-semibold text-purple-300">House {houseMapping.house_number}</span>
                          {houseMapping.house_significations && houseMapping.house_significations.length > 0 && (
                            <div className="text-xs text-slate-400 mt-1">
                              {houseMapping.house_significations.slice(0, 2).join(', ')}
                            </div>
                          )}
                        </div>
                      ) : (
                        <span className="text-slate-500">-</span>
                      )}
                    </td>
                    <td className="py-3 px-4">
                      {houseMapping ? (
                        <span className="text-blue-300">{houseMapping.rasi_name}</span>
                      ) : (
                        <span className="text-slate-500">-</span>
                      )}
                    </td>
                    <td className="py-3 px-4">
                      {aspects.length > 0 ? (
                        <div className="space-y-1">
                          {aspects.slice(0, 3).map((aspect, idx) => (
                            <div key={idx} className="flex items-center gap-2">
                              <span className={`text-xs px-2 py-1 rounded ${
                                aspect.aspect_strength === 'strong' ? 'bg-red-900/50' :
                                aspect.aspect_strength === 'moderate' ? 'bg-yellow-900/50' :
                                'bg-green-900/50'
                              }`}>
                                {aspect.planet_name}
                              </span>
                              <span className="text-xs text-slate-400">
                                {aspect.aspect_type.replace('drishti_', '')}
                              </span>
                            </div>
                          ))}
                          {aspects.length > 3 && (
                            <div className="text-xs text-slate-500">+{aspects.length - 3} more</div>
                          )}
                        </div>
                      ) : (
                        <span className="text-slate-500">No aspects</span>
                      )}
                    </td>
                    <td className="py-3 px-4 text-xs text-slate-400">
                      {event.created_at ? (
                        <div>
                          <div>{format(new Date(event.created_at), 'MMM dd, yyyy')}</div>
                          <div className="text-slate-500">{format(new Date(event.created_at), 'HH:mm')}</div>
                        </div>
                      ) : (
                        <span className="text-slate-500">-</span>
                      )}
                    </td>
                    <td className="py-3 px-4">
                      <Link
                        href={`/events/${event.id}`}
                        className="text-purple-400 hover:text-purple-300 text-sm"
                      >
                        View →
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Aspect Type Summary */}
      {Object.keys(aspectCounts).length > 0 && (
        <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
          <h3 className="text-lg font-semibold mb-4">⭐ Aspect Type Distribution</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {Object.entries(aspectCounts)
              .sort(([, a], [, b]) => b - a)
              .slice(0, 12)
              .map(([key, count]) => {
                const [type, planet] = key.split('_');
                return (
                  <div key={key} className="flex items-center justify-between">
                    <span className="text-slate-300 text-sm">
                      {planet} ({type.replace('drishti_', '')})
                    </span>
                    <span className="font-semibold text-purple-400">{count}</span>
                  </div>
                );
              })}
          </div>
        </div>
      )}
    </div>
  );
}

