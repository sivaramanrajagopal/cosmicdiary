/**
 * Color scheme and abbreviations for planetary chart visualization
 * 
 * Colors follow traditional Vedic astrology associations:
 * - Sun: Gold/Yellow (bright, radiant)
 * - Moon: Silver/White (calm, reflective)
 * - Mars: Red (fiery, energetic)
 * - Mercury: Green/Teal (communicative, adaptive)
 * - Jupiter: Orange/Yellow (expansive, wise)
 * - Venus: Pink/Peach (beautiful, harmonious)
 * - Saturn: Gray/Blue (disciplined, restrictive)
 * - Rahu: Dark Red (intense, unpredictable)
 * - Ketu: Indigo/Purple (mystical, spiritual)
 */

export const PLANET_COLORS: Record<string, string> = {
  Sun: '#FFD700',        // Gold
  Moon: '#C0C0C0',       // Silver
  Mars: '#FF4500',       // Red-orange
  Mercury: '#98D8C8',    // Teal
  Jupiter: '#FFA500',    // Orange
  Venus: '#FFDAB9',      // Peach
  Saturn: '#708090',     // Slate gray
  Rahu: '#8B0000',       // Dark red
  Ketu: '#4B0082',       // Indigo
};

export const PLANET_ABBREVIATIONS: Record<string, string> = {
  Sun: 'Su',
  Moon: 'Mo',
  Mars: 'Ma',
  Mercury: 'Me',
  Jupiter: 'Ju',
  Venus: 'Ve',
  Saturn: 'Sa',
  Rahu: 'Ra',
  Ketu: 'Ke',
};

export const PLANET_FULL_NAMES: Record<string, string> = {
  Su: 'Sun',
  Mo: 'Moon',
  Ma: 'Mars',
  Me: 'Mercury',
  Ju: 'Jupiter',
  Ve: 'Venus',
  Sa: 'Saturn',
  Ra: 'Rahu',
  Ke: 'Ketu',
};

export const HOUSE_COLORS = {
  odd: 'bg-slate-800/50',           // Odd houses (1,3,5,7,9,11)
  even: 'bg-slate-700/50',          // Even houses (2,4,6,8,10,12)
  ascendant: 'bg-purple-900/50',    // 1st house (ascendant)
  dustana: 'bg-red-900/30',         // Dustana houses (6, 8, 12)
};

export const RASI_COLORS: Record<string, string> = {
  Aries: '#FF6B6B',       // Red
  Taurus: '#4ECDC4',      // Teal
  Gemini: '#95E1D3',      // Mint
  Cancer: '#FFE66D',      // Yellow
  Leo: '#FFA07A',         // Light salmon
  Virgo: '#98D8C8',       // Aqua
  Libra: '#F7B731',       // Golden
  Scorpio: '#EB3B5A',     // Crimson
  Sagittarius: '#FD79A8', // Pink
  Capricorn: '#6C5CE7',   // Purple
  Aquarius: '#00B894',    // Green
  Pisces: '#00CEC9',      // Turquoise
};

export const STRENGTH_COLORS = {
  exalted: 'text-green-400 bg-green-900/30',
  debilitated: 'text-red-400 bg-red-900/30',
  ownSign: 'text-blue-400 bg-blue-900/30',
  digBala: 'text-yellow-400 bg-yellow-900/30',
  combusted: 'text-orange-400 bg-orange-900/30',
  neutral: 'text-slate-400 bg-slate-800/30',
};

export const RETROGRADE_INDICATOR = {
  symbol: 'R',
  color: 'text-red-400',
  title: 'Retrograde',
};

