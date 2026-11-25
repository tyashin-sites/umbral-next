'use client';
import { useEffect, useRef, useState } from 'react';

/**
 * Signature 1 — the shadow clock. A window's mullion shadow lies on a limestone
 * wall where it would fall in the visitor's own room right now (local time sets
 * --sun 0..1 from 08:00 to 19:00); scrolling through the hero advances the
 * afternoon. Decorative only; the hero text never depends on it (LCP law).
 */
export function ShadowClock() {
  const ref = useRef<HTMLDivElement>(null);
  const [clock, setClock] = useState<string>('');

  useEffect(() => {
    const el = ref.current?.closest<HTMLElement>('[data-sun-root]');
    if (!el) return;
    const now = new Date();
    const hours = now.getHours() + now.getMinutes() / 60;
    // Night visitors see late afternoon: the shadow is the point.
    const base = hours >= 8 && hours <= 19 ? (hours - 8) / 11 : 0.72;
    setClock(now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }));
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    let raf = 0;
    const apply = () => {
      raf = 0;
      const rect = el.getBoundingClientRect();
      const progress = reduce ? 0 : Math.min(1, Math.max(0, -rect.top / Math.max(1, rect.height)));
      const sun = Math.min(1, base * 0.8 + progress * 0.55);
      el.style.setProperty('--sun', sun.toFixed(3));
    };
    apply();
    const onScroll = () => { if (!raf) raf = requestAnimationFrame(apply); };
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => { window.removeEventListener('scroll', onScroll); if (raf) cancelAnimationFrame(raf); };
  }, []);

  return (
    <div ref={ref} className="shadow-wall" aria-hidden="true">
      <div className="stone" />
      <svg className="shadow-cast" viewBox="0 0 1000 1000" preserveAspectRatio="xMidYMid slice">
        {/* Window shadow: outer frame + 3 mullions + 1 transom, drawn as the shadow it casts. */}
        <g>
          <rect x="250" y="80" width="500" height="16" />
          <rect x="250" y="80" width="16" height="840" />
          <rect x="734" y="80" width="16" height="840" />
          <rect x="250" y="904" width="500" height="16" />
          <rect x="371" y="80" width="7" height="840" />
          <rect x="496" y="80" width="7" height="840" />
          <rect x="621" y="80" width="7" height="840" />
          <rect x="250" y="300" width="500" height="7" />
          {/* the wall around the window is in shadow; the opening is lit */}
          <path fillRule="evenodd" d="M-600 -600 H1600 V1600 H-600 Z M250 80 V920 H750 V80 Z" />
        </g>
      </svg>

      {clock ? (
        <p className="t-num absolute bottom-6 right-[var(--gutter)] text-[0.7rem] tracking-[0.18em] text-[rgb(42_37_30/0.55)] hero-fade" style={{ ['--d' as string]: '1200ms' }}>
          {clock} · the light on this wall, now
        </p>
      ) : null}
    </div>
  );
}
