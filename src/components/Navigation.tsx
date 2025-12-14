'use client';

import { useState } from 'react';
import { Menu, X } from 'lucide-react';
import Link from 'next/link';

const navLinks = [
  { href: '/dashboard', label: 'Dashboard' },
  { href: '/', label: 'Home' },
  { href: '/events', label: 'Events' },
  { href: '/planets', label: 'Planets' },
  { href: '/analysis', label: 'Analysis' },
  { href: '/house-analysis', label: 'Houses & Aspects' },
  { href: '/jobs', label: 'Jobs' },
];

export default function Navigation() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="mb-8 border-b border-purple-800 pb-4">
      {/* Desktop Navigation */}
      <div className="hidden md:flex gap-4 flex-wrap">
        {navLinks.map((link) => (
          <Link
            key={link.href}
            href={link.href}
            className="hover:text-purple-400 transition-colors"
          >
            {link.label}
          </Link>
        ))}
      </div>

      {/* Mobile Navigation */}
      <div className="md:hidden">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="flex items-center gap-2 text-purple-400 hover:text-purple-300 transition-colors"
          aria-label="Toggle menu"
        >
          {isOpen ? <X size={24} /> : <Menu size={24} />}
          <span className="text-sm font-medium">Menu</span>
        </button>

        {/* Mobile Menu Dropdown */}
        {isOpen && (
          <div className="mt-4 flex flex-col gap-3 py-4 border-t border-purple-800/50">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="hover:text-purple-400 transition-colors py-2"
                onClick={() => setIsOpen(false)}
              >
                {link.label}
              </Link>
            ))}
          </div>
        )}
      </div>
    </nav>
  );
}
