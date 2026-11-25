import Link from 'next/link';
import { notFound } from 'next/navigation';
import { pageMetadata } from '@/lib/seo';
import { FAMILIES, getFamily, systemsIn } from '@/data/collection';
import { SystemCard } from '@/components/SystemCard';
import { Breadcrumbs } from '@/components/Breadcrumbs';
import { KnowledgeGraph } from '@/components/KnowledgeGraph';

export function generateStaticParams() {
  return FAMILIES.map((f) => ({ family: f.slug }));
}
export const dynamicParams = false;

export async function generateMetadata({ params }: { params: Promise<{ family: string }> }) {
  const { family } = await params;
  const f = getFamily(family);
  if (!f) return {};
  return pageMetadata({ title: f.name, description: `${f.line} ${f.intro}`.slice(0, 158), path: `/collection/${f.slug}` });
}

export default async function FamilyPage({ params }: { params: Promise<{ family: string }> }) {
  const { family } = await params;
  const f = getFamily(family);
  if (!f) notFound();
  const items = systemsIn(f.slug);
  const others = FAMILIES.filter((o) => o.slug !== f.slug);
  return (
    <>
      <KnowledgeGraph path={`/collection/${f.slug}`} title={f.name} description={f.intro} crumbs={[{ name: 'Collection', path: '/collection' }, { name: f.name, path: `/collection/${f.slug}` }]} />
      <section className="wrap pt-16 pb-16 md:pt-24">
        <Breadcrumbs items={[{ name: 'Collection', href: '/collection' }, { name: f.name }]} />
        <h1 className="t-display mt-10 hero-rise">{f.name}</h1>
        <div className="mt-8 grid gap-6 md:grid-cols-12">
          <p className="t-lead italic md:col-span-5 hero-rise" style={{ ['--d' as string]: '80ms' }}>{f.line}</p>
          <p className="t-body md:col-span-5 md:col-start-8 hero-rise" style={{ ['--d' as string]: '160ms' }}>{f.intro}</p>
        </div>
      </section>
      <section className="wrap pb-28">
        <div className={`grid gap-x-10 gap-y-16 ${items.length > 1 ? 'md:grid-cols-2' : ''}`}>
          {items.map((s, i) => (
            <div key={s.slug} className={`reveal ${i % 2 === 1 ? 'md:mt-32' : ''}`}><SystemCard s={s} priority={i < 2} /></div>
          ))}
        </div>
      </section>
      <section className="border-t border-border">
        <div className="wrap flex flex-col gap-6 py-14 md:flex-row md:items-center md:justify-between">
          <p className="eyebrow">Other families</p>
          <ul className="flex flex-wrap gap-x-10 gap-y-3">
            {others.map((o) => (<li key={o.slug}><Link href={`/collection/${o.slug}`} className="t-h3 link-line">{o.name}</Link></li>))}
          </ul>
        </div>
      </section>
    </>
  );
}
