import Link from 'next/link';
import { pageMetadata } from '@/lib/seo';
import { FAMILIES, systemsIn } from '@/data/collection';
import { SystemCard } from '@/components/SystemCard';
import { Breadcrumbs } from '@/components/Breadcrumbs';
import { KnowledgeGraph } from '@/components/KnowledgeGraph';

const DESC = 'Nine Umbral systems in four families: glass walls, entrances, windows and interiors. Each one configurable and openable in 3D.';
export const metadata = pageMetadata({ title: 'The collection', description: DESC, path: '/collection' });

export default function CollectionPage() {
  return (
    <>
      <KnowledgeGraph path="/collection" title="The collection" description={DESC} crumbs={[{ name: 'Collection', path: '/collection' }]} />
      <section className="wrap pt-16 pb-12 md:pt-24">
        <Breadcrumbs items={[{ name: 'Collection' }]} />
        <h1 className="t-display mt-10 max-w-[12ch] hero-rise">The collection</h1>
        <p className="t-lead mt-8 max-w-[34ch] text-muted hero-rise" style={{ ['--d' as string]: '100ms' }}>Nine systems, four families. Every one is made to size, and every one can be opened on this site.</p>
      </section>
      {FAMILIES.map((f, fi) => {
        const items = systemsIn(f.slug);
        return (
          <section key={f.slug} className="border-t border-border">
            <div className="wrap py-20 md:py-28">
              <div className="grid gap-8 md:grid-cols-12">
                <div className="md:col-span-4">
                  <span className="t-num text-[0.8rem] text-bronce">0{fi + 1}</span>
                  <h2 className="t-h1 mt-4 reveal">{f.name}</h2>
                  <p className="mt-4 font-heading text-xl italic text-muted reveal">{f.line}</p>
                  <p className="t-body mt-6 reveal">{f.intro}</p>
                  <Link href={`/collection/${f.slug}`} className="link-line mt-8 inline-block text-[0.8rem] font-medium uppercase tracking-[0.16em]">{f.name}, in full</Link>
                </div>
                <div className={`grid gap-x-8 gap-y-14 md:col-span-8 ${items.length > 1 ? 'sm:grid-cols-2' : ''}`}>
                  {items.map((s, i) => (
                    <div key={s.slug} className={`reveal ${i % 2 === 1 ? 'sm:mt-24' : ''}`}><SystemCard s={s} tall={items.length > 1} priority={fi === 0 && i < 2} /></div>
                  ))}
                </div>
              </div>
            </div>
          </section>
        );
      })}
    </>
  );
}
