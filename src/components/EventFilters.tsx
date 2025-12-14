'use client';

import { useState } from 'react';
import { Filter, X, ChevronDown, ChevronUp } from 'lucide-react';

const PLANETS = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu'];
const CATEGORIES = [
  'Natural Disaster',
  'War',
  'Economic',
  'Political',
  'Technology',
  'Health',
  'Personal',
  'Other'
];
const IMPACT_LEVELS = ['low', 'medium', 'high', 'critical'];

export interface FilterValues {
  startDate?: string;
  endDate?: string;
  planets?: string[];
  categories?: string[];
  impactLevels?: string[];
  eventType?: 'world' | 'personal';
}

interface EventFiltersProps {
  onFilterChange: (filters: FilterValues) => void;
  initialFilters?: FilterValues;
}

export default function EventFilters({ onFilterChange, initialFilters = {} }: EventFiltersProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [filters, setFilters] = useState<FilterValues>(initialFilters);

  const handleFilterChange = (key: keyof FilterValues, value: any) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  const toggleArrayFilter = (key: 'planets' | 'categories' | 'impactLevels', value: string) => {
    const currentArray = filters[key] || [];
    const newArray = currentArray.includes(value)
      ? currentArray.filter(item => item !== value)
      : [...currentArray, value];

    handleFilterChange(key, newArray.length > 0 ? newArray : undefined);
  };

  const clearFilters = () => {
    setFilters({});
    onFilterChange({});
  };

  const hasActiveFilters = Object.keys(filters).some(key => {
    const value = filters[key as keyof FilterValues];
    return value !== undefined && value !== '' && (!Array.isArray(value) || value.length > 0);
  });

  const getActiveFilterCount = () => {
    let count = 0;
    if (filters.startDate || filters.endDate) count++;
    if (filters.planets && filters.planets.length > 0) count++;
    if (filters.categories && filters.categories.length > 0) count++;
    if (filters.impactLevels && filters.impactLevels.length > 0) count++;
    if (filters.eventType) count++;
    return count;
  };

  return (
    <div className="bg-slate-800/50 rounded-lg border border-slate-700 mb-6">
      {/* Filter Header - Mobile Toggle */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between p-4 sm:p-6 text-left hover:bg-slate-700/30 transition-colors"
      >
        <div className="flex items-center gap-3">
          <Filter size={20} className="text-purple-400" />
          <span className="font-semibold text-base sm:text-lg">Filters</span>
          {hasActiveFilters && (
            <span className="bg-purple-600 text-white text-xs px-2 py-1 rounded-full">
              {getActiveFilterCount()}
            </span>
          )}
        </div>
        {isOpen ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
      </button>

      {/* Filter Content */}
      {isOpen && (
        <div className="p-4 sm:p-6 pt-0 space-y-6 border-t border-slate-700">
          {/* Date Range */}
          <div>
            <label className="block text-sm font-medium mb-3 text-purple-300">Date Range</label>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="block text-xs text-slate-400 mb-1">From</label>
                <input
                  type="date"
                  value={filters.startDate || ''}
                  onChange={(e) => handleFilterChange('startDate', e.target.value || undefined)}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>
              <div>
                <label className="block text-xs text-slate-400 mb-1">To</label>
                <input
                  type="date"
                  value={filters.endDate || ''}
                  onChange={(e) => handleFilterChange('endDate', e.target.value || undefined)}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>
            </div>
          </div>

          {/* Planets */}
          <div>
            <label className="block text-sm font-medium mb-3 text-purple-300">Filter by Planets</label>
            <div className="flex flex-wrap gap-2">
              {PLANETS.map((planet) => (
                <button
                  key={planet}
                  onClick={() => toggleArrayFilter('planets', planet)}
                  className={`px-3 py-1.5 rounded-lg text-sm transition-colors ${
                    filters.planets?.includes(planet)
                      ? 'bg-purple-600 text-white'
                      : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                  }`}
                >
                  {planet}
                </button>
              ))}
            </div>
          </div>

          {/* Categories */}
          <div>
            <label className="block text-sm font-medium mb-3 text-purple-300">Categories</label>
            <div className="flex flex-wrap gap-2">
              {CATEGORIES.map((category) => (
                <button
                  key={category}
                  onClick={() => toggleArrayFilter('categories', category)}
                  className={`px-3 py-1.5 rounded-lg text-sm transition-colors ${
                    filters.categories?.includes(category)
                      ? 'bg-purple-600 text-white'
                      : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                  }`}
                >
                  {category}
                </button>
              ))}
            </div>
          </div>

          {/* Impact Levels */}
          <div>
            <label className="block text-sm font-medium mb-3 text-purple-300">Impact Level</label>
            <div className="flex flex-wrap gap-2">
              {IMPACT_LEVELS.map((level) => (
                <button
                  key={level}
                  onClick={() => toggleArrayFilter('impactLevels', level)}
                  className={`px-3 py-1.5 rounded-lg text-sm capitalize transition-colors ${
                    filters.impactLevels?.includes(level)
                      ? level === 'critical' ? 'bg-red-900 text-white' :
                        level === 'high' ? 'bg-orange-900 text-white' :
                        level === 'medium' ? 'bg-yellow-900 text-white' :
                        'bg-green-900 text-white'
                      : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                  }`}
                >
                  {level}
                </button>
              ))}
            </div>
          </div>

          {/* Event Type */}
          <div>
            <label className="block text-sm font-medium mb-3 text-purple-300">Event Type</label>
            <div className="flex gap-2">
              <button
                onClick={() => handleFilterChange('eventType', filters.eventType === 'world' ? undefined : 'world')}
                className={`px-4 py-2 rounded-lg text-sm transition-colors ${
                  filters.eventType === 'world'
                    ? 'bg-purple-600 text-white'
                    : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                }`}
              >
                World Events
              </button>
              <button
                onClick={() => handleFilterChange('eventType', filters.eventType === 'personal' ? undefined : 'personal')}
                className={`px-4 py-2 rounded-lg text-sm transition-colors ${
                  filters.eventType === 'personal'
                    ? 'bg-purple-600 text-white'
                    : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                }`}
              >
                Personal Events
              </button>
            </div>
          </div>

          {/* Clear Filters Button */}
          {hasActiveFilters && (
            <button
              onClick={clearFilters}
              className="w-full sm:w-auto flex items-center justify-center gap-2 bg-red-900/50 hover:bg-red-900/70 px-4 py-2 rounded-lg text-sm transition-colors"
            >
              <X size={16} />
              Clear All Filters
            </button>
          )}
        </div>
      )}
    </div>
  );
}
