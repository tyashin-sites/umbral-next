'use client';
import Image from 'next/image';
import { useState } from 'react';

/**
 * Signature 3 — open it. Poster-first: the Thridify experience (configurable,
 * openable 3D) mounts only when asked, so it costs the page nothing until then.
 */
export function Experience({ name, poster, url }: { name: string; poster: string; url: string }) {
  const [live, setLive] = useState(false);
  return (
    <div className="relative aspect-[3/4] w-full overflow-hidden bg-[#ddd5c7] sm:aspect-[16/10]">
      {live && url ? (
        <iframe
          src={url}
          title={`${name} — configure and open in 3D`}
          className="absolute inset-0 h-full w-full border-0"
          allow="fullscreen; xr-spatial-tracking; accelerometer; gyroscope; camera"
          allowFullScreen
        />
      ) : (
        <>
          <Image src={poster} alt={`${name}, in late-afternoon light`} fill sizes="(min-width: 1024px) 66vw, 100vw" className="object-cover" />
          <div className="absolute inset-0 bg-gradient-to-t from-[rgb(22_20_15/0.55)] via-transparent to-transparent" />
          {url ? (
            <button type="button" onClick={() => setLive(true)} className="btn btn-primary absolute bottom-6 left-6" style={{ background: 'var(--u-cal)', color: 'var(--u-ink)' }}>
              Open it in 3D <span className="arrow" aria-hidden="true" />
            </button>
          ) : (
            <p className="absolute bottom-6 left-6 text-[0.8rem] uppercase tracking-[0.18em] text-cal">3D model in preparation</p>
          )}
        </>
      )}
    </div>
  );
}
