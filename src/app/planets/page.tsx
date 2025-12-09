'use client';

import { useState, useEffect } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { format } from 'date-fns';
import TransitTable from '@/components/TransitTable';
import { PlanetaryData } from '@/lib/types';

export default function PlanetsPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const date = searchParams.get('date') || format(new Date(), 'yyyy-MM-dd');
  const [planetaryData, setPlanetaryData] = useState<PlanetaryData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      try {
        const response = await fetch(`/api/planetary-data?date=${date}`);
        if (response.ok) {
          const data = await response.json();
          setPlanetaryData(data);
        } else {
          setPlanetaryData(null);
        }
      } catch (error) {
        console.error('Error fetching planetary data:', error);
        setPlanetaryData(null);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, [date]);

  const handleDateChange = (newDate: string) => {
    router.push(`/planets?date=${newDate}`);
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold">Planetary Positions</h2>
        <input
          type="date"
          value={date}
          onChange={(e) => handleDateChange(e.target.value)}
          className="bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-white"
        />
      </div>

      {loading ? (
        <div className="text-center py-12 bg-slate-800/50 rounded-lg border border-slate-700">
          <p className="text-slate-400">Loading planetary data...</p>
        </div>
      ) : planetaryData?.planetary_data?.planets ? (
        <div>
          <p className="text-slate-400 mb-4">
            Planetary positions for {format(new Date(date), 'MMMM dd, yyyy')}
          </p>
          <TransitTable planets={planetaryData.planetary_data.planets} />
        </div>
      ) : (
        <div className="text-center py-12 bg-slate-800/50 rounded-lg border border-slate-700">
          <p className="text-slate-400">
            No planetary data available for {format(new Date(date), 'MMMM dd, yyyy')}
          </p>
        </div>
      )}
    </div>
  );
}
