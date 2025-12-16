'use client';

import { useState, useEffect } from 'react';
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { format, subDays, eachDayOfInterval } from 'date-fns';
import type { Event } from '@/lib/types';

const CATEGORY_COLORS: Record<string, string> = {
  'Natural Disaster': '#EF4444',
  'War': '#DC2626',
  'Economic': '#F59E0B',
  'Political': '#3B82F6',
  'Technology': '#8B5CF6',
  'Health': '#10B981',
  'Personal': '#EC4899',
  'Other': '#6B7280',
};

const IMPACT_COLORS: Record<string, string> = {
  'critical': '#DC2626',
  'high': '#F97316',
  'medium': '#FBBF24',
  'low': '#10B981',
};

interface EventsOverviewProps {
  events: Event[];
}

export default function EventsOverview({ events }: EventsOverviewProps) {
  const [period, setPeriod] = useState<7 | 30 | 90>(30);

  // Filter events by period
  const startDate = subDays(new Date(), period);
  const filteredEvents = events.filter(e => new Date(e.date) >= startDate);

  // Category distribution
  const categoryData = Object.entries(
    filteredEvents.reduce((acc, event) => {
      const cat = event.category || 'Other';
      acc[cat] = (acc[cat] || 0) + 1;
      return acc;
    }, {} as Record<string, number>)
  )
    .map(([name, value]) => ({
      name,
      value,
      color: CATEGORY_COLORS[name] || CATEGORY_COLORS['Other'],
    }))
    .sort((a, b) => b.value - a.value);

  // Impact level distribution
  const impactData = Object.entries(
    filteredEvents.reduce((acc, event) => {
      acc[event.impact_level] = (acc[event.impact_level] || 0) + 1;
      return acc;
    }, {} as Record<string, number>)
  )
    .map(([name, value]) => ({
      name: name.charAt(0).toUpperCase() + name.slice(1),
      value,
      color: IMPACT_COLORS[name] || '#6B7280',
    }))
    .sort((a, b) => {
      const order = { Critical: 0, High: 1, Medium: 2, Low: 3 };
      return (order[a.name as keyof typeof order] || 4) - (order[b.name as keyof typeof order] || 4);
    });

  // Daily event trend (last N days)
  const trendDays = period === 7 ? 7 : period === 30 ? 30 : 90;
  const dateRange = eachDayOfInterval({
    start: subDays(new Date(), trendDays - 1),
    end: new Date(),
  });

  const trendData = dateRange.map(date => {
    const dateStr = format(date, 'yyyy-MM-dd');
    const count = events.filter(e => e.date === dateStr).length;
    return {
      date: format(date, 'MMM dd'),
      count,
    };
  });

  // Top locations
  const locationData = Object.entries(
    filteredEvents.reduce((acc, event) => {
      const loc = event.location || 'Unknown';
      acc[loc] = (acc[loc] || 0) + 1;
      return acc;
    }, {} as Record<string, number>)
  )
    .map(([name, count]) => ({ name, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 10);

  return (
    <div className="space-y-6">
      {/* Period Selector */}
      <div className="flex items-center justify-between">
        <h3 className="text-2xl font-bold">📊 Events Overview</h3>
        <div className="flex gap-2">
          {([7, 30, 90] as const).map((p) => (
            <button
              key={p}
              onClick={() => setPeriod(p)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                period === p
                  ? 'bg-purple-600 text-white'
                  : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
              }`}
            >
              {p} Days
            </button>
          ))}
        </div>
      </div>

      <div className="text-sm text-slate-400">
        Showing {filteredEvents.length} events from last {period} days
      </div>

      {filteredEvents.length === 0 ? (
        <div className="bg-slate-800/50 p-8 rounded-lg border border-slate-700 text-center">
          <p className="text-slate-400 mb-4">No events found in the last {period} days.</p>
          <a
            href="/events/new"
            className="inline-block bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg transition-colors text-sm font-medium"
          >
            + Create Event
          </a>
        </div>
      ) : (
        <>
          {/* Two Column Layout for Charts */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Event Trend */}
            <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
              <h4 className="text-lg font-semibold mb-4">📈 Daily Event Trend</h4>
              <ResponsiveContainer width="100%" height={250}>
                <LineChart data={trendData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis
                    dataKey="date"
                    stroke="#9CA3AF"
                    fontSize={11}
                    angle={-45}
                    textAnchor="end"
                    height={80}
                  />
                  <YAxis stroke="#9CA3AF" fontSize={12} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#1F2937',
                      border: '1px solid #374151',
                      borderRadius: '8px',
                    }}
                    labelStyle={{ color: '#E5E7EB' }}
                  />
                  <Line
                    type="monotone"
                    dataKey="count"
                    stroke="#8B5CF6"
                    strokeWidth={2}
                    dot={{ fill: '#8B5CF6', r: 4 }}
                    activeDot={{ r: 6 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {/* Category Distribution */}
            <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
              <h4 className="text-lg font-semibold mb-4">🏷️ Events by Category</h4>
              {categoryData.length > 0 ? (
                <ResponsiveContainer width="100%" height={250}>
                  <PieChart>
                    <Pie
                      data={categoryData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) =>
                        percent > 0.05 ? `${name} ${(percent * 100).toFixed(0)}%` : ''
                      }
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {categoryData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip
                      contentStyle={{
                        backgroundColor: '#1F2937',
                        border: '1px solid #374151',
                        borderRadius: '8px',
                      }}
                    />
                  </PieChart>
                </ResponsiveContainer>
              ) : (
                <div className="flex items-center justify-center h-[250px] text-slate-400">
                  No category data
                </div>
              )}
            </div>

            {/* Impact Level Distribution */}
            <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
              <h4 className="text-lg font-semibold mb-4">⚡ Impact Level Distribution</h4>
              {impactData.length > 0 ? (
                <ResponsiveContainer width="100%" height={250}>
                  <BarChart data={impactData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                    <XAxis dataKey="name" stroke="#9CA3AF" fontSize={12} />
                    <YAxis stroke="#9CA3AF" fontSize={12} />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: '#1F2937',
                        border: '1px solid #374151',
                        borderRadius: '8px',
                      }}
                      labelStyle={{ color: '#E5E7EB' }}
                    />
                    <Bar dataKey="value" radius={[8, 8, 0, 0]}>
                      {impactData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <div className="flex items-center justify-center h-[250px] text-slate-400">
                  No impact data
                </div>
              )}
            </div>

            {/* Top Locations */}
            <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
              <h4 className="text-lg font-semibold mb-4">🌍 Top Locations</h4>
              <div className="space-y-3 max-h-[250px] overflow-y-auto">
                {locationData.length > 0 ? (
                  locationData.map((loc, idx) => (
                    <div key={idx} className="flex items-center justify-between">
                      <span className="text-slate-300 text-sm truncate flex-1 mr-2">
                        {idx + 1}. {loc.name}
                      </span>
                      <div className="flex items-center gap-2 flex-shrink-0">
                        <div className="w-24 bg-slate-700 rounded-full h-2">
                          <div
                            className="bg-blue-500 h-2 rounded-full"
                            style={{
                              width: `${(loc.count / filteredEvents.length) * 100}%`
                            }}
                          />
                        </div>
                        <span className="font-semibold text-blue-400 w-8 text-right text-sm">
                          {loc.count}
                        </span>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="text-center text-slate-400 py-12">
                    No location data
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Category Breakdown Table */}
          <div className="bg-slate-800/50 p-6 rounded-lg border border-slate-700">
            <h4 className="text-lg font-semibold mb-4">📋 Category Breakdown</h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {categoryData.map((cat, idx) => (
                <div
                  key={idx}
                  className="bg-slate-900/50 p-4 rounded-lg border border-slate-700 flex items-center gap-3"
                >
                  <div
                    className="w-3 h-3 rounded-full flex-shrink-0"
                    style={{ backgroundColor: cat.color }}
                  />
                  <div className="flex-1 min-w-0">
                    <div className="font-medium text-sm truncate">{cat.name}</div>
                    <div className="text-xs text-slate-400">
                      {cat.value} events ({((cat.value / filteredEvents.length) * 100).toFixed(1)}%)
                    </div>
                  </div>
                  <div className="text-2xl font-bold text-slate-300 flex-shrink-0">
                    {cat.value}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
