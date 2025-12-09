import { createClient, SupabaseClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || '';
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '';

// Validate that we have the required credentials
if (!supabaseUrl || !supabaseAnonKey) {
  const errorMessage = '❌ Supabase credentials not configured!\n\n' +
    'Please create a .env.local file in the CosmicDiary directory with:\n' +
    'NEXT_PUBLIC_SUPABASE_URL=your_supabase_url\n' +
    'NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key\n\n' +
    'Then restart the dev server.';
  
  if (typeof window === 'undefined') {
    // Server-side: throw error to prevent invalid client creation
    throw new Error(errorMessage);
  } else {
    // Client-side: log error
    console.error(errorMessage);
  }
}

// Create Supabase client with actual credentials
export const supabase: SupabaseClient = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    persistSession: false
  }
});
