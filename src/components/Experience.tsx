import Image from 'next/image';

/**
 * Signature 3 — open it. A declarative Thridify placement (Layer 0): the Tyashin
 * Thridify plugin (linked to doorswindows@thridify.com) edge-injects its loader
 * on pages carrying `data-thridify-product`, and the SDK mounts the published
 * experience for that pid here. `on-demand` = nothing is downloaded until the
 * visitor taps, so the page pays nothing for 3D until it is wanted. The poster
 * is server-rendered and stays if the SDK is absent (e.g. direct workers.dev).
 */
export function Experience({ name, pid, poster }: { name: string; pid: string; poster: string }) {
  return (
    <div className="relative aspect-[3/4] w-full overflow-hidden bg-[#ddd5c7] sm:aspect-[16/10]">
      <div
        data-thridify-product={pid}
        data-thridify-mode="on-demand"
        data-thridify-poster={poster}
        className="absolute inset-0 h-full w-full"
        aria-label={`${name} — configure and open in 3D`}
      >
        <Image src={poster} alt={`${name}, in late-afternoon light`} fill sizes="(min-width: 1024px) 66vw, 100vw" className="object-cover" />
      </div>
    </div>
  );
}
