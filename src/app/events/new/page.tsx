'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { createEvent } from '@/lib/api';
import { Event } from '@/lib/types';

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

const TAG_SUGGESTIONS = [
  'climate', 'pandemic', 'election', 'crash', 'earthquake',
  'flood', 'conflict', 'summit', 'policy', 'innovation',
  'breakthrough', 'celebration', 'mourning', 'festival', 'ceremony'
];

export default function NewEventPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [detectingTimezone, setDetectingTimezone] = useState(false);
  
  // Get current time in HH:MM:SS format
  const getCurrentTime = () => {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    return `${hours}:${minutes}:${seconds}`;
  };

  const [formData, setFormData] = useState<Omit<Event, 'id' | 'created_at' | 'updated_at'>>({
    date: new Date().toISOString().split('T')[0],
    event_time: getCurrentTime(),
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone || 'UTC',
    has_accurate_time: false,
    title: '',
    description: '',
    category: '',
    location: '',
    latitude: undefined,
    longitude: undefined,
    impact_level: 'medium',
    event_type: 'world',
    tags: [],
  });

  const [tagInput, setTagInput] = useState('');

  // Detect timezone when latitude/longitude change
  useEffect(() => {
    const detectTimezone = async () => {
      if (formData.latitude !== undefined && formData.longitude !== undefined) {
        setDetectingTimezone(true);
        try {
          const response = await fetch(
            `/api/timezone/detect?lat=${formData.latitude}&lng=${formData.longitude}`
          );
          if (response.ok) {
            const data = await response.json();
            if (data.timezone) {
              setFormData(prev => ({ ...prev, timezone: data.timezone }));
            }
          }
        } catch (error) {
          console.error('Error detecting timezone:', error);
        } finally {
          setDetectingTimezone(false);
        }
      }
    };

    detectTimezone();
  }, [formData.latitude, formData.longitude]);

  // Auto-detect user's location (browser geolocation)
  const detectUserLocation = () => {
    if (!navigator.geolocation) {
      alert('Geolocation is not supported by your browser. Please enter coordinates manually.');
      return;
    }

    // Show loading state
    const originalButton = document.activeElement as HTMLElement;
    if (originalButton) {
      originalButton.textContent = '🔄 Detecting...';
      originalButton.setAttribute('disabled', 'true');
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        setFormData(prev => ({
          ...prev,
          latitude: parseFloat(position.coords.latitude.toFixed(6)),
          longitude: parseFloat(position.coords.longitude.toFixed(6)),
        }));
        
        // Reset button
        if (originalButton) {
          originalButton.textContent = '📍 Detect My Location';
          originalButton.removeAttribute('disabled');
        }
      },
      (error) => {
        console.error('Geolocation error:', error);
        
        // Reset button
        if (originalButton) {
          originalButton.textContent = '📍 Detect My Location';
          originalButton.removeAttribute('disabled');
        }

        // Provide specific error messages
        let errorMessage = 'Could not detect your location. ';
        switch (error.code) {
          case error.PERMISSION_DENIED:
            errorMessage += 'Location access was denied. Please enable location permissions in your browser settings or enter coordinates manually.';
            break;
          case error.POSITION_UNAVAILABLE:
            errorMessage += 'Location information is unavailable. Please enter coordinates manually.';
            break;
          case error.TIMEOUT:
            errorMessage += 'Location request timed out. Please try again or enter coordinates manually.';
            break;
          default:
            errorMessage += 'An unknown error occurred. Please enter coordinates manually.';
            break;
        }
        alert(errorMessage);
      },
      {
        enableHighAccuracy: true,
        timeout: 10000, // 10 seconds
        maximumAge: 0 // Don't use cached position
      }
    );
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const eventData: Omit<Event, 'id' | 'created_at' | 'updated_at'> = {
        ...formData,
      };

      const result = await createEvent(eventData);
      if (result) {
        router.push(`/events/${result.id}`);
      }
    } catch (error) {
      console.error('Error creating event:', error);
      alert('Failed to create event. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const addTag = () => {
    if (tagInput.trim() && !formData.tags.includes(tagInput.trim())) {
      setFormData({
        ...formData,
        tags: [...formData.tags, tagInput.trim()],
      });
      setTagInput('');
    }
  };

  const removeTag = (tag: string) => {
    setFormData({
      ...formData,
      tags: formData.tags.filter((t) => t !== tag),
    });
  };

  const setQuickTime = (time: string) => {
    setFormData(prev => ({ ...prev, event_time: time }));
  };

  const getMaxDate = () => {
    return new Date().toISOString().split('T')[0];
  };

  return (
    <div className="max-w-3xl mx-auto">
      <h2 className="text-2xl sm:text-3xl font-bold mb-6">Create New Event</h2>

      <form onSubmit={handleSubmit} className="space-y-6 sm:space-y-8">
        {/* ============================================================
            SECTION 1: EVENT DETAILS
            ============================================================ */}
        <div className="bg-slate-800/50 p-4 sm:p-6 rounded-lg border border-slate-700">
          <h3 className="text-lg sm:text-xl font-semibold mb-4 text-purple-300">Event Details</h3>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">
                Title <span className="text-red-400">*</span>
              </label>
              <input
                type="text"
                required
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                placeholder="Enter event title"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Description</label>
              <textarea
                value={formData.description || ''}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                rows={4}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                placeholder="Enter event description (optional)"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2">
                  Category <span className="text-red-400">*</span>
                </label>
                <select
                  required
                  value={formData.category}
                  onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                >
                  <option value="">Select category...</option>
                  {CATEGORIES.map((cat) => (
                    <option key={cat} value={cat}>{cat}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Location</label>
                <input
                  type="text"
                  value={formData.location || ''}
                  onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                  placeholder="e.g., Chicago, USA"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2">Event Type</label>
                <div className="flex gap-4">
                  <label className="flex items-center cursor-pointer">
                    <input
                      type="radio"
                      name="event_type"
                      value="world"
                      checked={formData.event_type === 'world'}
                      onChange={(e) => setFormData({ ...formData, event_type: e.target.value as 'world' | 'personal' })}
                      className="mr-2"
                    />
                    <span>World Event</span>
                  </label>
                  <label className="flex items-center cursor-pointer">
                    <input
                      type="radio"
                      name="event_type"
                      value="personal"
                      checked={formData.event_type === 'personal'}
                      onChange={(e) => setFormData({ ...formData, event_type: e.target.value as 'world' | 'personal' })}
                      className="mr-2"
                    />
                    <span>Personal Event</span>
                  </label>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Impact Level</label>
                <div className="flex gap-2 flex-wrap">
                  {(['low', 'medium', 'high', 'critical'] as const).map((level) => (
                    <label key={level} className="flex items-center cursor-pointer">
                      <input
                        type="radio"
                        name="impact_level"
                        value={level}
                        checked={formData.impact_level === level}
                        onChange={(e) => setFormData({ ...formData, impact_level: e.target.value as 'low' | 'medium' | 'high' | 'critical' })}
                        className="mr-2"
                      />
                      <span className="capitalize">{level}</span>
                    </label>
                  ))}
                </div>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Tags</label>
              <div className="flex gap-2 mb-2">
                <input
                  type="text"
                  value={tagInput}
                  onChange={(e) => setTagInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addTag())}
                  list="tag-suggestions"
                  className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                  placeholder="Add a tag and press Enter"
                />
                <datalist id="tag-suggestions">
                  {TAG_SUGGESTIONS.map((tag) => (
                    <option key={tag} value={tag} />
                  ))}
                </datalist>
                <button
                  type="button"
                  onClick={addTag}
                  className="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg transition-colors"
                >
                  Add
                </button>
              </div>
              <div className="flex flex-wrap gap-2">
                {formData.tags.map((tag) => (
                  <span
                    key={tag}
                    className="bg-purple-900/50 px-3 py-1 rounded text-sm flex items-center gap-2"
                  >
                    {tag}
                    <button
                      type="button"
                      onClick={() => removeTag(tag)}
                      className="hover:text-red-400"
                    >
                      ×
                    </button>
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* ============================================================
            SECTION 2: DATE & TIME SELECTION
            ============================================================ */}
        <div className="bg-slate-800/50 p-4 sm:p-6 rounded-lg border border-slate-700">
          <h3 className="text-lg sm:text-xl font-semibold mb-4 text-purple-300">Date & Time</h3>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">
                Date <span className="text-red-400">*</span>
              </label>
              <input
                type="date"
                required
                max={getMaxDate()}
                value={formData.date}
                onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
              />
              <p className="text-xs text-slate-400 mt-1">Maximum date: Today (no future dates)</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2">Time (HH:MM:SS)</label>
                <input
                  type="time"
                  step="1"
                  value={formData.event_time || '12:00:00'}
                  onChange={(e) => {
                    // Convert to HH:MM:SS format
                    const timeValue = e.target.value;
                    const timeParts = timeValue.split(':');
                    if (timeParts.length === 2) {
                      setFormData({ ...formData, event_time: `${timeValue}:00` });
                    } else {
                      setFormData({ ...formData, event_time: timeValue });
                    }
                  }}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Quick Time Buttons</label>
                <div className="flex flex-wrap gap-2">
                  <button
                    type="button"
                    onClick={() => setQuickTime(getCurrentTime())}
                    className="bg-slate-700 hover:bg-slate-600 px-3 py-1 rounded text-sm transition-colors"
                  >
                    Now
                  </button>
                  <button
                    type="button"
                    onClick={() => setQuickTime('08:00:00')}
                    className="bg-slate-700 hover:bg-slate-600 px-3 py-1 rounded text-sm transition-colors"
                  >
                    Morning (8 AM)
                  </button>
                  <button
                    type="button"
                    onClick={() => setQuickTime('12:00:00')}
                    className="bg-slate-700 hover:bg-slate-600 px-3 py-1 rounded text-sm transition-colors"
                  >
                    Noon
                  </button>
                  <button
                    type="button"
                    onClick={() => setQuickTime('18:00:00')}
                    className="bg-slate-700 hover:bg-slate-600 px-3 py-1 rounded text-sm transition-colors"
                  >
                    Evening (6 PM)
                  </button>
                  <button
                    type="button"
                    onClick={() => setQuickTime('00:00:00')}
                    className="bg-slate-700 hover:bg-slate-600 px-3 py-1 rounded text-sm transition-colors"
                  >
                    Midnight
                  </button>
                </div>
              </div>
            </div>

            <div>
              <label className="flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={formData.has_accurate_time || false}
                  onChange={(e) => setFormData({ ...formData, has_accurate_time: e.target.checked })}
                  className="mr-2 w-4 h-4"
                />
                <span className="text-sm">
                  I know the exact time
                  {formData.has_accurate_time && (
                    <span className="text-green-400 ml-2">✓ (Confidence: 100%)</span>
                  )}
                  {!formData.has_accurate_time && (
                    <span className="text-yellow-400 ml-2">(Estimated - Confidence: 70%)</span>
                  )}
                </span>
              </label>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Timezone</label>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={formData.timezone || 'UTC'}
                  onChange={(e) => setFormData({ ...formData, timezone: e.target.value })}
                  className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                  placeholder="e.g., Asia/Kolkata"
                />
                {detectingTimezone && (
                  <span className="text-sm text-slate-400 self-center">Detecting...</span>
                )}
              </div>
              <p className="text-xs text-slate-400 mt-1">
                {formData.latitude !== undefined && formData.longitude !== undefined
                  ? `Detected from location (${formData.latitude.toFixed(4)}, ${formData.longitude.toFixed(4)})`
                  : 'Enter IANA timezone (e.g., Asia/Kolkata, America/New_York) or it will be detected from coordinates'}
              </p>
            </div>
          </div>
        </div>

        {/* ============================================================
            SECTION 3: LOCATION COORDINATES
            ============================================================ */}
        <div className="bg-slate-800/50 p-4 sm:p-6 rounded-lg border border-slate-700">
          <h3 className="text-lg sm:text-xl font-semibold mb-4 text-purple-300">Location Coordinates</h3>
          
          <div className="space-y-4">
            <div>
              <button
                type="button"
                onClick={detectUserLocation}
                className="bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 disabled:cursor-not-allowed px-4 py-2 rounded-lg transition-colors text-sm mb-4"
              >
                📍 Detect My Location
              </button>
              <p className="text-xs text-slate-400 mt-1">
                Your browser will ask for permission to access your location
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2">Latitude</label>
                <input
                  type="number"
                  step="any"
                  min="-90"
                  max="90"
                  value={formData.latitude ?? ''}
                  onChange={(e) => setFormData({ ...formData, latitude: e.target.value ? parseFloat(e.target.value) : undefined })}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                  placeholder="Optional (for chart calculation)"
                />
                <p className="text-xs text-slate-400 mt-1">Range: -90 to 90</p>
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-2">Longitude</label>
                <input
                  type="number"
                  step="any"
                  min="-180"
                  max="180"
                  value={formData.longitude ?? ''}
                  onChange={(e) => setFormData({ ...formData, longitude: e.target.value ? parseFloat(e.target.value) : undefined })}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                  placeholder="Optional (for chart calculation)"
                />
                <p className="text-xs text-slate-400 mt-1">Range: -180 to 180</p>
              </div>
            </div>

            {formData.latitude !== undefined && formData.longitude !== undefined && (
              <div className="bg-slate-900/50 p-3 rounded border border-slate-700">
                <p className="text-sm text-slate-300">
                  ✓ Coordinates set: {formData.latitude.toFixed(6)}, {formData.longitude.toFixed(6)}
                </p>
                <p className="text-xs text-slate-400 mt-1">
                  Chart calculations will use these coordinates for accurate ascendant and house calculations.
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Submit Buttons */}
        <div className="flex flex-col sm:flex-row gap-4">
          <button
            type="submit"
            disabled={loading}
            className="bg-purple-600 hover:bg-purple-700 disabled:bg-slate-600 px-6 py-2 rounded-lg transition-colors font-medium w-full sm:w-auto"
          >
            {loading ? 'Creating...' : 'Create Event'}
          </button>
          <button
            type="button"
            onClick={() => router.back()}
            className="bg-slate-700 hover:bg-slate-600 px-6 py-2 rounded-lg transition-colors w-full sm:w-auto"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}
