'use client';

import { Planet } from '@/lib/types';

interface TransitTableProps {
  planets: Planet[];
}

export default function TransitTable({ planets }: TransitTableProps) {
  const nakshatras = [
    'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
    'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
    'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
    'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha',
    'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
  ];

  return (
    <div className="overflow-x-auto bg-slate-800/50 rounded-lg border border-slate-700">
      <table className="w-full">
        <thead>
          <tr className="border-b border-slate-700">
            <th className="text-left p-4 text-sm font-semibold">Planet</th>
            <th className="text-left p-4 text-sm font-semibold">Rasi</th>
            <th className="text-left p-4 text-sm font-semibold">Nakshatra</th>
            <th className="text-left p-4 text-sm font-semibold">Longitude</th>
            <th className="text-left p-4 text-sm font-semibold">Status</th>
          </tr>
        </thead>
        <tbody>
          {planets.map((planet, idx) => (
            <tr key={idx} className="border-b border-slate-700/50 hover:bg-slate-700/30">
              <td className="p-4">
                <span className="font-medium">{planet.name}</span>
              </td>
              <td className="p-4">
                <div>
                  <span className="text-purple-300">{planet.rasi.name}</span>
                  <span className="text-xs text-slate-500 ml-2">
                    (Lord: {planet.rasi.lord.name})
                  </span>
                </div>
              </td>
              <td className="p-4">
                <span className="text-blue-300">
                  {nakshatras[planet.nakshatra - 1] || `N${planet.nakshatra}`}
                </span>
              </td>
              <td className="p-4">
                <span className="text-slate-300">{planet.longitude.toFixed(2)}°</span>
              </td>
              <td className="p-4">
                {planet.is_retrograde ? (
                  <span className="text-red-400 text-sm font-medium">Retrograde</span>
                ) : (
                  <span className="text-green-400 text-sm">Direct</span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
