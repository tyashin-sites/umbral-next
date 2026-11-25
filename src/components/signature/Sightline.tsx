'use client';
import { useId, useState } from 'react';

/**
 * Signature 2 — the sightline. Drag a two-panel sliding opening from a
 * conventional frame to the system's own sightline; the view through the
 * drawing widens and the numbers run. Pure SVG + a native range input.
 */
export function Sightline({ target = 19, opening = 6000, label = 'Horizonte 19' }: { target?: number; opening?: number; label?: string }) {
  const id = useId();
  const [t, setT] = useState(0.35);
  const conventional = 86; // a good conventional aluminium slider profile, per stile
  const outerMm = conventional * (1 - t); // outer stiles retreat into the wall
  const meetMm = conventional + (target - conventional) * t; // meeting stile thins to the interlock
  const frameTotal = Math.round(outerMm * 2 + meetMm);
  const glassPct = ((opening - frameTotal) / opening) * 100;
  const s = 1000 / opening; // drawn true to scale: 1000 units across the opening
  const outer = outerMm * s;
  const meet = meetMm * s;

  return (
    <div className="on-night grain">
      <div className="wrap section">
        <div className="grid gap-14 lg:grid-cols-12 lg:items-end">
          <div className="lg:col-span-4">
            <p className="eyebrow">The sightline</p>
            <h2 className="t-h2 mt-6">Every millimetre of frame is a millimetre of shadow.</h2>
            <p className="t-body mt-6">Drag the drawing. On the left, a good conventional slider. On the right, {label}: the frame is in the floor, the ceiling and the wall, and what is left is the line where two panes meet.</p>
          </div>
          <div className="lg:col-span-8">
            <svg viewBox="0 0 1000 420" className="w-full" role="img" aria-label={`Elevation of a ${opening / 1000} metre opening showing ${frameTotal} millimetres of visible frame`}>
              <defs>
                <linearGradient id={`${id}-sky`} x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0" stopColor="#c9cdc7" />
                  <stop offset="0.62" stopColor="#e3d9c6" />
                  <stop offset="0.63" stopColor="#8d8270" />
                  <stop offset="1" stopColor="#5f574a" />
                </linearGradient>
              </defs>
              <rect x="0" y="20" width="1000" height="380" fill={`url(#${id}-sky)`} opacity="0.92" />
              {/* outer stiles shrink into the wall */}
              <rect x="0" y="20" width={outer} height="380" fill="#16140f" />
              <rect x={1000 - outer} y="20" width={outer} height="380" fill="#16140f" />
              {/* head & sill */}
              <rect x="0" y="20" width="1000" height={Math.max(2, 26 * (1 - t))} fill="#16140f" />
              <rect x="0" y={400 - Math.max(2, 26 * (1 - t))} width="1000" height={Math.max(2, 26 * (1 - t))} fill="#16140f" />
              {/* meeting interlock */}
              <rect x={500 - meet / 2} y="20" width={meet} height="380" fill="#16140f" />
              {/* dimension line */}
              <g stroke="#b6916a" strokeWidth="1" opacity="0.8">
                <line x1="0" y1="414" x2="1000" y2="414" />
                <line x1="0" y1="408" x2="0" y2="420" />
                <line x1="1000" y1="408" x2="1000" y2="420" />
              </g>
            </svg>
            <label htmlFor={id} className="sr-only">Frame thickness</label>
            <input id={id} type="range" min={0} max={1} step={0.001} value={t} onChange={(e) => setT(parseFloat(e.target.value))} className="sightline-range mt-6" />
            <dl className="mt-8 grid grid-cols-3 gap-6 border-t border-[rgb(236_231_222/0.12)] pt-6">
              <div><dt className="text-[0.7rem] uppercase tracking-[0.2em] text-[#a99f8f]">Frame in view</dt><dd className="t-num mt-2 text-2xl md:text-3xl">{frameTotal} mm</dd></div>
              <div><dt className="text-[0.7rem] uppercase tracking-[0.2em] text-[#a99f8f]">Glass</dt><dd className="t-num mt-2 text-2xl md:text-3xl">{glassPct.toFixed(1)}%</dd></div>
              <div><dt className="text-[0.7rem] uppercase tracking-[0.2em] text-[#a99f8f]">Opening</dt><dd className="t-num mt-2 text-2xl md:text-3xl">{(opening / 1000).toFixed(1)} m</dd></div>
            </dl>
          </div>
        </div>
      </div>
    </div>
  );
}
