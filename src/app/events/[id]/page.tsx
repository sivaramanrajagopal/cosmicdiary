import { notFound } from 'next/navigation';
import Link from 'next/link';
import { getEventById, getPlanetaryDataForEvent, getHouseMapping, getPlanetaryAspects } from '@/lib/database';
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

  // Get house mapping and aspects
  const houseMapping = await getHouseMapping(eventId);
  const aspects = await getPlanetaryAspects(eventId);

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

      {/* House Mapping Section */}
      {houseMapping && (
        <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
          <h3 className="text-2xl font-semibold mb-4">🏠 House Mapping</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h4 className="text-sm font-medium text-slate-400 mb-2">House Information</h4>
              <div className="space-y-2">
                <div>
                  <span className="text-slate-400">House Number: </span>
                  <span className="text-2xl font-bold text-purple-400">{houseMapping.house_number}</span>
                </div>
                <div>
                  <span className="text-slate-400">Rasi: </span>
                  <span className="text-lg font-semibold text-blue-400">{houseMapping.rasi_name}</span>
                </div>
              </div>
            </div>
            {houseMapping.house_significations && houseMapping.house_significations.length > 0 && (
              <div>
                <h4 className="text-sm font-medium text-slate-400 mb-2">Significations</h4>
                <div className="flex flex-wrap gap-2">
                  {houseMapping.house_significations.map((sig, idx) => (
                    <span key={idx} className="bg-purple-900/50 px-2 py-1 rounded text-xs">
                      {sig}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
          {houseMapping.mapping_reason && (
            <div className="mt-4 pt-4 border-t border-slate-700">
              <p className="text-sm text-slate-400 italic">{houseMapping.mapping_reason}</p>
            </div>
          )}
        </div>
      )}

      {/* Planetary Aspects Section */}
      {aspects.length > 0 && (
        <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
          <h3 className="text-2xl font-semibold mb-4">⭐ Planetary Aspects to Event House</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-700">
                  <th className="text-left py-2 px-4 font-semibold">Planet</th>
                  <th className="text-left py-2 px-4 font-semibold">Aspect Type</th>
                  <th className="text-left py-2 px-4 font-semibold">Planet Position</th>
                  <th className="text-left py-2 px-4 font-semibold">Strength</th>
                </tr>
              </thead>
              <tbody>
                {aspects.map((aspect) => (
                  <tr key={aspect.id} className="border-b border-slate-700/50">
                    <td className="py-2 px-4">
                      <span className="font-medium text-purple-300">{aspect.planet_name}</span>
                    </td>
                    <td className="py-2 px-4">
                      <span className="text-blue-300">
                        {aspect.aspect_type === 'conjunction' ? 'Conjunction' :
                         aspect.aspect_type === 'dustana' ? 'Dustana (6,8,12)' :
                         aspect.aspect_type.replace('drishti_', 'Drishti ').replace('_', 'th ')}
                      </span>
                    </td>
                    <td className="py-2 px-4">
                      <div className="text-slate-300">
                        <div>{aspect.planet_rasi}</div>
                        <div className="text-xs text-slate-500">{aspect.planet_longitude.toFixed(2)}°</div>
                      </div>
                    </td>
                    <td className="py-2 px-4">
                      <span className={`text-xs px-2 py-1 rounded ${
                        aspect.aspect_strength === 'strong' ? 'bg-red-900/50 text-red-200' :
                        aspect.aspect_strength === 'moderate' ? 'bg-yellow-900/50 text-yellow-200' :
                        'bg-green-900/50 text-green-200'
                      }`}>
                        {aspect.aspect_strength.toUpperCase()}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
