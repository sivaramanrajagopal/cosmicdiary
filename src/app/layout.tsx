import type { Metadata, Viewport } from "next";
import "./globals.css";
import Navigation from "@/components/Navigation";

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
            <h1 className="text-3xl sm:text-4xl font-bold mb-2 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
              Cosmic Diary
            </h1>
            <p className="text-slate-300 text-sm sm:text-base">Planetary Events Analysis</p>
          </header>
          <Navigation />
          <main>{children}</main>
        </div>
      </body>
    </html>
  );
}
