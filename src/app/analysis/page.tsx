import { getEvents, getEventCorrelations } from '@/lib/database';
import { getPlanetaryData } from '@/lib/database';
import { analyzeEventPlanetaryCorrelation, analyzeAllEvents, getPlanetaryPatterns } from '@/lib/astrologyAnalysis';
import type { PlanetaryAnalysis } from '@/lib/astrologyAnalysis';
import Link from 'next/link';
import { format } from 'date-fns';

export default async function AnalysisPage() {
  const events = await getEvents();
  
  // Fetch planetary data for all event dates
  const uniqueDates = [...new Set(events.map(e => e.date))];
  const planetaryDataMap = new Map();
  
  for (const date of uniqueDates) {
    const pd = await getPlanetaryData(date);
    if (pd) {
      planetaryDataMap.set(date, pd);
    }
  }
  
  // Analyze all events
  const analyses = analyzeAllEvents(events, planetaryDataMap);
  const analysesArray = Array.from(analyses.values());
  
  // Get planetary patterns
  const patterns = getPlanetaryPatterns(analysesArray);
  
  // Check which events have stored correlations in database
  const eventsWithStoredCorrelations = await Promise.all(
    events.map(async (event) => {
      try {
        if (!event.id || typeof event.id !== 'number') {
          return { event, hasStored: false, correlationCount: 0 };
        }
        const stored = await getEventCorrelations(event.id);
        return { event, hasStored: stored.length > 0, correlationCount: stored.length };
      } catch (error) {
        // Silently handle errors - correlations might not exist for all events
        console.warn(`Error checking correlations for event ${event.id}:`, error);
        return { event, hasStored: false, correlationCount: 0 };
      }
    })
  );
  
  const storedCount = eventsWithStoredCorrelations.filter(e => e.hasStored).length;
  
  // Calculate statistics
  const eventsByCategory = events.reduce((acc, event) => {
    const category = event.category || 'Uncategorized';
    acc[category] = (acc[category] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  const eventsByImpact = events.reduce((acc, event) => {
    acc[event.impact_level] = (acc[event.impact_level] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  // Events with significant planetary correlations
  const eventsWithSignificantPlanets = analysesArray.filter(a => a.significantPlanets.length > 0);
  const eventsWithRetrograde = analysesArray.filter(a => a.retrogradePlanets.length > 0);

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold">Astrological Analysis</h2>
        <div className="text-sm text-slate-400">
          {storedCount > 0 && (
            <span className="bg-green-900/50 px-3 py-1 rounded">
              ✅ {storedCount} events with stored correlations
            </span>
          )}
        </div>
      </div>
      
      {storedCount === 0 && (
        <div className="bg-yellow-900/20 border border-yellow-700/50 p-4 rounded-lg">
          <p className="text-yellow-300">
            ⚠️ <strong>No correlations stored in database yet.</strong> New events will automatically store correlations. 
            <a href="/api/events/recalculate-correlations" className="ml-2 text-yellow-200 underline hover:text-yellow-100">
              Recalculate for existing events
            </a>
          </p>
        </div>
      )}
      
      {/* Overview Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
          <h3 className="text-sm font-medium text-slate-400 mb-2">Total Events</h3>
          <p className="text-3xl font-bold text-purple-400">{events.length}</p>
        </div>

        <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
          <h3 className="text-sm font-medium text-slate-400 mb-2">Planetary Correlations</h3>
          <p className="text-3xl font-bold text-blue-400">{eventsWithSignificantPlanets.length}</p>
          <p className="text-xs text-slate-500 mt-1">Events with planetary significance</p>
        </div>

        <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
          <h3 className="text-sm font-medium text-slate-400 mb-2">Retrograde Influence</h3>
          <p className="text-3xl font-bold text-red-400">{eventsWithRetrograde.length}</p>
          <p className="text-xs text-slate-500 mt-1">Events during retrograde</p>
        </div>

        <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
          <h3 className="text-sm font-medium text-slate-400 mb-2">Analyzed Dates</h3>
          <p className="text-3xl font-bold text-green-400">{uniqueDates.length}</p>
          <p className="text-xs text-slate-500 mt-1">Unique dates analyzed</p>
        </div>
      </div>

      {/* Planetary Patterns */}
      {patterns.mostActiveRasis.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
            <h3 className="text-lg font-semibold mb-4">🌙 Most Active Rasis</h3>
            <div className="space-y-3">
              {patterns.mostActiveRasis.map(({ rasi, count }) => (
                <div key={rasi} className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-2 h-2 rounded-full bg-purple-400"></div>
                    <span className="text-slate-300">{rasi}</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="w-24 bg-slate-700 rounded-full h-2">
                      <div 
                        className="bg-purple-500 h-2 rounded-full" 
                        style={{ width: `${(count / events.length) * 100}%` }}
                      ></div>
                    </div>
                    <span className="font-semibold text-purple-400 w-8 text-right">{count}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
            <h3 className="text-lg font-semibold mb-4">⭐ Most Active Nakshatras</h3>
            <div className="space-y-3">
              {patterns.mostActiveNakshatras.map(({ nakshatra, count }) => (
                <div key={nakshatra} className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-2 h-2 rounded-full bg-blue-400"></div>
                    <span className="text-slate-300">{nakshatra}</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="w-24 bg-slate-700 rounded-full h-2">
                      <div 
                        className="bg-blue-500 h-2 rounded-full" 
                        style={{ width: `${(count / events.length) * 100}%` }}
                      ></div>
                    </div>
                    <span className="font-semibold text-blue-400 w-8 text-right">{count}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Category-Planetary Links */}
      {Object.keys(patterns.categoryPlanetaryLinks).length > 0 && (
        <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
          <h3 className="text-lg font-semibold mb-4">🔮 Planetary Correlations by Event Category</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {Object.entries(patterns.categoryPlanetaryLinks).map(([category, planets]) => (
              <div key={category} className="bg-slate-900/50 p-4 rounded-lg">
                <h4 className="font-semibold text-purple-300 mb-2">{category}</h4>
                <div className="flex flex-wrap gap-2">
                  {planets.map(planet => (
                    <span key={planet} className="text-xs bg-purple-900/50 px-2 py-1 rounded">
                      {planet}
                    </span>
                  ))}
                </div>
                <p className="text-xs text-slate-500 mt-2">
                  {events.filter(e => e.category === category).length} event(s)
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Retrograde Analysis */}
      {Object.keys(patterns.retrogradeFrequency).length > 0 && (
        <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
          <h3 className="text-lg font-semibold mb-4">🔄 Retrograde Planet Frequency</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {Object.entries(patterns.retrogradeFrequency).map(([planet, count]) => (
              <div key={planet} className="text-center">
                <div className="text-2xl font-bold text-red-400">{count}</div>
                <div className="text-sm text-slate-400">{planet}</div>
                <div className="text-xs text-slate-500">retrograde events</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Detailed Event Analyses */}
      <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
        <h3 className="text-lg font-semibold mb-4">📊 Event Planetary Analysis</h3>
        <div className="space-y-6">
          {analysesArray.slice(0, 10).map((analysis) => (
            <EventAnalysisCard key={analysis.event.id} analysis={analysis} />
          ))}
        </div>
      </div>

      {/* Basic Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
          <h3 className="text-lg font-semibold mb-4">Events by Category</h3>
          <div className="space-y-2">
            {Object.entries(eventsByCategory)
              .sort(([, a], [, b]) => b - a)
              .map(([category, count]) => (
                <div key={category} className="flex justify-between items-center">
                  <span className="text-slate-300">{category}</span>
                  <span className="font-semibold">{count}</span>
                </div>
              ))}
          </div>
        </div>

        <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
          <h3 className="text-lg font-semibold mb-4">Events by Impact Level</h3>
          <div className="space-y-2">
            {Object.entries(eventsByImpact).map(([level, count]) => (
              <div key={level} className="flex justify-between items-center">
                <span className="text-slate-300 capitalize">{level}</span>
                <span className={`font-semibold ${
                  level === 'critical' ? 'text-red-400' :
                  level === 'high' ? 'text-orange-400' :
                  level === 'medium' ? 'text-yellow-400' :
                  'text-green-400'
                }`}>
                  {count}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function EventAnalysisCard({ analysis }: { analysis: PlanetaryAnalysis }) {
  if (!analysis.planetaryData) {
    return (
      <Link
        href={`/events/${analysis.event.id}`}
        className="block bg-slate-900/50 hover:bg-slate-900/70 p-4 rounded-lg border border-slate-700 transition-colors"
      >
        <div className="flex justify-between items-start">
          <div>
            <h4 className="font-semibold">{analysis.event.title}</h4>
            <p className="text-sm text-slate-400">{analysis.event.category} • {format(new Date(analysis.event.date), 'MMM dd, yyyy')}</p>
          </div>
          <span className="text-xs text-slate-500">No planetary data</span>
        </div>
      </Link>
    );
  }

  return (
    <Link
      href={`/events/${analysis.event.id}`}
      className="block bg-slate-900/50 hover:bg-slate-900/70 p-5 rounded-lg border border-slate-700 transition-colors"
    >
      <div className="space-y-3">
        <div className="flex justify-between items-start">
          <div className="flex-1">
            <h4 className="font-semibold text-lg">{analysis.event.title}</h4>
            <p className="text-sm text-slate-400 mt-1">
              {analysis.event.category} • {format(new Date(analysis.event.date), 'MMM dd, yyyy')} • 
              <span className={`ml-2 ${
                analysis.event.impact_level === 'critical' ? 'text-red-400' :
                analysis.event.impact_level === 'high' ? 'text-orange-400' :
                analysis.event.impact_level === 'medium' ? 'text-yellow-400' :
                'text-green-400'
              }`}>
                {analysis.event.impact_level.toUpperCase()}
              </span>
            </p>
          </div>
        </div>

        {/* Dominant Influences */}
        <div className="flex gap-4 text-sm">
          <div>
            <span className="text-slate-500">Dominant Rasi:</span>
            <span className="ml-2 text-purple-300 font-medium">{analysis.dominantRasi}</span>
          </div>
          <div>
            <span className="text-slate-500">Dominant Nakshatra:</span>
            <span className="ml-2 text-blue-300 font-medium">{analysis.dominantNakshatra}</span>
          </div>
        </div>

        {/* Significant Planets */}
        {analysis.significantPlanets.length > 0 && (
          <div>
            <h5 className="text-sm font-semibold text-slate-400 mb-2">🔮 Significant Planetary Influences:</h5>
            <div className="space-y-2">
              {analysis.significantPlanets.slice(0, 3).map((sp, idx) => (
                <div key={idx} className="bg-slate-800/50 p-3 rounded border border-slate-700">
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-medium text-purple-300">{sp.planet.name}</span>
                    <span className={`text-xs px-2 py-1 rounded ${
                      sp.impact === 'high' ? 'bg-red-900/50 text-red-200' :
                      sp.impact === 'medium' ? 'bg-yellow-900/50 text-yellow-200' :
                      'bg-green-900/50 text-green-200'
                    }`}>
                      {sp.impact.toUpperCase()}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400">{sp.significance}</p>
                  <p className="text-xs text-slate-500 mt-1 italic">{sp.reason}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Retrograde Planets */}
        {analysis.retrogradePlanets.length > 0 && (
          <div>
            <h5 className="text-sm font-semibold text-red-400 mb-2">🔄 Retrograde Planets:</h5>
            <div className="flex flex-wrap gap-2">
              {analysis.retrogradePlanets.map(planet => (
                <span key={planet.name} className="text-xs bg-red-900/50 px-3 py-1 rounded border border-red-800">
                  {planet.name} (in {planet.rasi.name})
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Correlations */}
        {analysis.correlations.length > 0 && (
          <div>
            <h5 className="text-sm font-semibold text-slate-400 mb-2">✨ Planetary Correlations:</h5>
            <div className="space-y-2">
              {analysis.correlations.slice(0, 2).map((corr, idx) => (
                <div key={idx} className="text-xs bg-slate-800/50 p-2 rounded">
                  <span className="font-medium text-blue-300">{corr.description}</span>
                  <p className="text-slate-500 mt-1">{corr.significance}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </Link>
  );
}
