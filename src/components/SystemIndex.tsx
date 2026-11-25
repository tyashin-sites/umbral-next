import Link from 'next/link';
import Image from 'next/image';
import type { System } from '@/data/collection';
import { getFamily } from '@/data/collection';

/** The collection as an editorial index: thumbnail, name, what it does, the number that matters. */
export function SystemIndex({ systems }: { systems: System[] }) {
  return (
    <ol className="border-t border-border">
      {systems.map((s, i) => (
        <li key={s.slug} className="reveal" style={{ ['--d' as string]: `${(i % 4) * 70}ms` }}>
          <Link href={`/systems/${s.slug}`} className="group grid grid-cols-[72px_1fr] items-center gap-5 border-b border-border py-5 md:grid-cols-[120px_minmax(0,3fr)_minmax(0,4fr)_minmax(0,2fr)_auto] md:gap-10 md:py-7">
            <span className="figure figure-hover aspect-[4/5] w-[72px] md:w-[120px]">
              <Image src={s.stills.front} alt="" width={240} height={300} sizes="120px" className="h-full w-full object-cover" />
            </span>
            <span>
              <span className="block t-h3 transition-colors duration-300 group-hover:text-bronce">{s.name}</span>
              <span className="mt-1 block text-[0.72rem] uppercase tracking-[0.2em] text-muted md:hidden">{getFamily(s.family)?.name}</span>
            </span>
            <span className="hidden font-heading text-[1.15rem] italic text-muted md:block">{s.line}</span>
            <span className="hidden text-[0.72rem] uppercase tracking-[0.2em] text-muted md:block">{getFamily(s.family)?.name}</span>
            <span aria-hidden="true" className="hidden h-px w-10 bg-current transition-all duration-500 group-hover:w-16 md:block" />
          </Link>
        </li>
      ))}
    </ol>
  );
}
