'use client';
import { useEffect } from 'react';
import { usePathname } from 'next/navigation';

declare global {
  interface Window { Thridify?: { scan?: (root?: ParentNode) => number } }
}

const API_URL = process.env.NEXT_PUBLIC_TYASHIN_API_URL || 'https://website-api.tyashin.com';
const API_KEY = process.env.NEXT_PUBLIC_TYASHIN_API_KEY || '';

/**
 * The Tyashin Thridify loader runs once per FULL page load and only fetches the
 * SDK if a [data-thridify-product] placement exists at that moment. A visitor who
 * reaches a system page by client-side navigation (home → collection → system)
 * never gets it, so the placement stays an empty poster. On every route change:
 * SDK present → scan() (idempotent: mounted placements are skipped); SDK absent →
 * re-run the plugin loader, which now sees the placement and loads the SDK (the
 * SDK scans on boot). Platform issue: the loader should handle SPA navigation.
 */
export function ThridifyScan() {
  const pathname = usePathname();
  useEffect(() => {
    const placements = document.querySelectorAll('[data-thridify-product]:not([data-thridify-mounted])');
    if (!placements.length) return;
    if (window.Thridify?.scan) {
      window.Thridify.scan();
      return;
    }
    if (document.querySelector('script[src*="/sdk/v1/thridify.js"]') || !API_KEY) return;
    const s = document.createElement('script');
    s.src = `${API_URL}/api/v1/public/plugins/thridify.js?key=${encodeURIComponent(API_KEY)}&nav=${Date.now()}`;
    s.async = true;
    document.head.appendChild(s);
  }, [pathname]);
  return null;
}
