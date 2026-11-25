import Link from 'next/link';
import Image from 'next/image';
import type { System } from '@/data/collection';

export function SystemCard({ s, tall = false, priority = false }: { s: System; tall?: boolean; priority?: boolean }) {
  return (
    <Link href={`/systems/${s.slug}`} className="group block">
      <span className={`figure figure-hover block ${tall ? 'aspect-[4/5]' : 'aspect-[16/11]'}`}>
        <Image src={tall ? s.stills.front : s.stills.hero} alt={`${s.name} — ${s.summary.split('.')[0]}`} fill sizes="(min-width: 1024px) 40vw, 100vw" className="object-cover" priority={priority} />
      </span>
      <span className="mt-5 flex items-baseline justify-between gap-6">
        <span className="t-h3 transition-colors duration-300 group-hover:text-bronce">{s.name}</span>
        <span aria-hidden="true" className="h-px w-8 bg-current transition-all duration-500 group-hover:w-14" />
      </span>
      <span className="mt-2 block font-heading italic text-muted">{s.line}</span>
    </Link>
  );
}
