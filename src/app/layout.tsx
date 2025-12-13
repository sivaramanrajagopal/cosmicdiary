import type { Metadata, Viewport } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Cosmic Diary - Planetary Events Analysis",
  description: "Record and analyze world events with planetary influences",
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 min-h-screen text-white" suppressHydrationWarning>
        <div className="container mx-auto px-4 py-8">
          <header className="mb-8">
            <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
              Cosmic Diary
            </h1>
            <p className="text-slate-300">Planetary Events Analysis</p>
          </header>
              <nav className="mb-8 border-b border-purple-800 pb-4">
                <div className="flex gap-4">
                  <a href="/dashboard" className="hover:text-purple-400 transition-colors">Dashboard</a>
                  <a href="/" className="hover:text-purple-400 transition-colors">Home</a>
                  <a href="/events" className="hover:text-purple-400 transition-colors">Events</a>
                  <a href="/planets" className="hover:text-purple-400 transition-colors">Planets</a>
                  <a href="/analysis" className="hover:text-purple-400 transition-colors">Analysis</a>
                  <a href="/house-analysis" className="hover:text-purple-400 transition-colors">Houses & Aspects</a>
                  <a href="/jobs" className="hover:text-purple-400 transition-colors">Jobs</a>
                </div>
              </nav>
          <main>{children}</main>
        </div>
      </body>
    </html>
  );
}
