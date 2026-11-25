import Image from 'next/image';

/**
 * Signature 3 — open it. A declarative Thridify placement (Layer 0): the Tyashin
 * Thridify plugin (linked to doorswindows@thridify.com) edge-injects its loader
 * on pages carrying `data-thridify-product`, and the SDK mounts the published
 * experience for that pid.
 *
 * Mode `ready`: assets warm in the background and the live viewer presents when
 * the frame scrolls into view (governed — capped, evicted off-screen). Every
 * placement on this site is below the fold, so first paint never waits on 3D.
 * (`on-demand` needs the host to call handle.present() on tap, which a
 * declarative placement can't do.)
 *
 * The server-rendered still sits UNDER the SDK container as a fallback for when
 * the SDK is absent (direct workers.dev access); it must not be inside the mount
 * target or it would sit over the viewer and swallow input.
 */
export function Experience({ name, pid, poster }: { name: string; pid: string; poster: string }) {
  return (
    <div className="relative aspect-[3/4] w-full overflow-hidden bg-[#ddd5c7] sm:aspect-[16/10]">
      <Image src={poster} alt={`${name}, in late-afternoon light`} fill sizes="(min-width: 1024px) 66vw, 100vw" className="object-cover" />
      <div
        data-thridify-product={pid}
        data-thridify-mode="ready"
        data-thridify-poster={poster}
        className="absolute inset-0 z-[1] h-full w-full"
        role="region"
        aria-label={`${name} — configure and open in 3D`}
      />
    </div>
  );
}
