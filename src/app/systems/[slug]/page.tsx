import Link from 'next/link';
import Image from 'next/image';
import { notFound } from 'next/navigation';
import { pageMetadata } from '@/lib/seo';
import { SYSTEMS, getSystem, getFamily, shopperUrl, FINISH_SWATCHES, GLASS_NOTES } from '@/data/collection';
import { Breadcrumbs } from '@/components/Breadcrumbs';
import { Experience } from '@/components/Experience';
import { QuoteForm } from '@/components/QuoteForm';
import { SystemCard } from '@/components/SystemCard';
import { Sightline } from '@/components/signature/Sightline';
import { KnowledgeGraph } from '@/components/KnowledgeGraph';

export function generateStaticParams() {
  return SYSTEMS.map((s) => ({ slug: s.slug }));
}
export const dynamicParams = false;

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const s = getSystem(slug);
  if (!s) return {};
  return pageMetadata({ title: `${s.name} — ${getFamily(s.family)?.name}`, description: s.summary, path: `/systems/${s.slug}`, image: s.stills.hero });
}

export default async function SystemPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const s = getSystem(slug);
  if (!s) notFound();
  const family = getFamily(s.family)!;
  const url = s.previewId ? shopperUrl(s.previewId) : '';
  const related = [...SYSTEMS.filter((o) => o.family === s.family && o.slug !== s.slug), ...SYSTEMS.filter((o) => o.family !== s.family)].slice(0, 3);

  return (
    <>
      <KnowledgeGraph path={`/systems/${s.slug}`} title={s.name} description={s.summary} system={s} crumbs={[{ name: 'Collection', path: '/collection' }, { name: family.name, path: `/collection/${family.slug}` }, { name: s.name, path: `/systems/${s.slug}` }]} />

      {/* Hero: name left, still bleeding right */}
      <section className="pt-12 md:pt-16">
        <div className="wrap"><Breadcrumbs items={[{ name: 'Collection', href: '/collection' }, { name: family.name, href: `/collection/${family.slug}` }, { name: s.name }]} /></div>
        <div className="wrap mt-10 grid gap-10 md:grid-cols-12 md:items-end">
          <div className="md:col-span-5">
            <p className="eyebrow hero-fade">{family.name}</p>
            <h1 className="t-display mt-6 hero-rise">{s.name}</h1>
            <p className="t-lead mt-6 italic hero-rise" style={{ ['--d' as string]: '80ms' }}>{s.line}</p>
          </div>
          <div className="md:col-span-7">
            <div className="figure aspect-[16/11]">
              <Image src={s.stills.hero} alt={`${s.name}, partly open, in late-afternoon light`} fill priority sizes="(min-width: 768px) 58vw, 100vw" className="object-cover" />
            </div>
          </div>
        </div>
      </section>

      {/* Description + key numbers */}
      <section className="section">
        <div className="wrap grid gap-14 md:grid-cols-12">
          <div className="space-y-6 md:col-span-6">
            {s.paragraphs.map((p, i) => (<p key={i} className={i === 0 ? 't-lead reveal' : 't-body reveal'}>{p}</p>))}
            <p className="flex items-center gap-4 pt-4 text-[0.78rem] uppercase tracking-[0.18em] text-muted reveal"><span className="h-px w-8 bg-bronce" />{s.motion}</p>
          </div>
          <dl className="md:col-span-5 md:col-start-8 reveal">
            {(s.specs ?? []).slice(0, 4).map((sp) => (
              <div key={sp.label} className="spec-row"><dt>{sp.label}</dt><dd>{sp.value}</dd></div>
            ))}
          </dl>
        </div>
      </section>

      {/* Open it */}
      <section id="configure" className="pb-[var(--section)]">
        <div className="wrap">
          <div className="mb-8 flex flex-col justify-between gap-4 md:flex-row md:items-end">
            <div>
              <p className="eyebrow">Configure · open</p>
              <h2 className="t-h2 mt-5 max-w-[22ch]">Choose the finish, the glass and the size. Then open it.</h2>
            </div>
            {url ? <a href={url} target="_blank" rel="noopener" className="link-line text-[0.78rem] font-medium uppercase tracking-[0.16em]">Full screen, or in your room (AR)</a> : null}
          </div>
          <Experience name={s.name} poster={s.stills.hero} url={url} />
        </div>
      </section>

      {s.slug === 'horizonte' ? <Sightline target={s.sightlineMm || 19} opening={6000} label={s.name} /> : null}

      {/* Finishes, glass, sizes */}
      <section className="section">
        <div className="wrap grid gap-16 md:grid-cols-12">
          <div className="md:col-span-5">
            <p className="eyebrow reveal">Finishes</p>
            <ul className="mt-8 grid grid-cols-2 gap-x-6 gap-y-6">
              {(s.finishes ?? []).map((f) => (
                <li key={f} className="flex items-center gap-4 reveal">
                  <span className="h-10 w-10 shrink-0 rounded-full shadow-[inset_0_0_0_1px_rgb(22_20_15/0.15),var(--shadow-rest)]" style={{ background: FINISH_SWATCHES[f]?.hex ?? '#8a6a47' }} aria-hidden="true" />
                  <span><span className="block text-[0.95rem]">{f}</span><span className="block text-[0.78rem] text-muted">{FINISH_SWATCHES[f]?.en ?? ''}</span></span>
                </li>
              ))}
            </ul>
            {(s.glass ?? []).length ? (
              <>
                <p className="eyebrow mt-14 reveal">Glass</p>
                <ul className="mt-6">
                  {s.glass.map((g) => (<li key={g} className="spec-row reveal"><span>{g}</span><span className="text-[0.85rem] text-muted">{GLASS_NOTES[g] ?? ''}</span></li>))}
                </ul>
              </>
            ) : null}
          </div>
          <div className="md:col-span-6 md:col-start-7">
            <div className="figure aspect-square reveal">
              <Image src={s.stills.detail} alt={`${s.name}: detail of the profile and hardware`} fill sizes="(min-width: 768px) 45vw, 100vw" className="object-cover" />
            </div>
          </div>
        </div>
      </section>

      {/* Specification + what to notice */}
      <section className="on-night grain">
        <div className="wrap section grid gap-16 md:grid-cols-12">
          <div className="md:col-span-5">
            <p className="eyebrow">Specification</p>
            <dl className="mt-8 [&_.spec-row]:border-[rgb(236_231_222/0.12)] [&_dt]:text-[#a99f8f]">
              {(s.specs ?? []).map((sp) => (<div key={sp.label} className="spec-row"><dt>{sp.label}</dt><dd>{sp.value}</dd></div>))}
              {(s.sizes ?? []).length ? (<div className="spec-row"><dt>Configurations in 3D</dt><dd className="max-w-[18rem]">{s.sizes.join(' · ')}</dd></div>) : null}
            </dl>
            <p className="mt-6 text-[0.75rem] text-[#8f8676]">Illustrative specification for a demonstration house. Geometry from the parametric model.</p>
          </div>
          <div className="md:col-span-6 md:col-start-7">
            <p className="eyebrow">What to notice</p>
            <ol className="mt-8">
              {(s.notes ?? []).map((n, i) => (
                <li key={n.title} className="grid grid-cols-[2.5rem_1fr] gap-4 border-t border-[rgb(236_231_222/0.12)] py-6 reveal">
                  <span className="t-num text-[0.8rem] text-[#b6916a]">{String(i + 1).padStart(2, '0')}</span>
                  <span><span className="block font-heading text-xl">{n.title}</span><span className="mt-2 block text-[0.95rem] text-[#b7ad9d]">{n.text}</span></span>
                </li>
              ))}
            </ol>
          </div>
        </div>
      </section>

      {/* Front elevation + quotation */}
      <section className="section">
        <div className="wrap grid gap-16 md:grid-cols-12">
          <div className="md:col-span-4">
            <div className="figure aspect-[4/5] reveal">
              <Image src={s.stills.front} alt={`${s.name}, elevation`} fill sizes="(min-width: 768px) 30vw, 100vw" className="object-cover" />
            </div>
          </div>
          <div className="md:col-span-7 md:col-start-6">
            <p className="eyebrow">Quotation</p>
            <h2 className="t-h2 mt-5 max-w-[20ch]">Every {s.name} is made to its opening.</h2>
            <p className="t-body mt-5">Send us the size and what you chose in 3D. We reply with questions, a drawing and a price for that opening.</p>
            <div className="mt-12"><QuoteForm system={s.slug} /></div>
          </div>
        </div>
      </section>

      {/* Related */}
      <section className="border-t border-border">
        <div className="wrap section">
          <div className="flex items-end justify-between gap-6">
            <h2 className="t-h2">Also in the collection</h2>
            <Link href="/collection" className="link-line text-[0.8rem] font-medium uppercase tracking-[0.16em]">All nine</Link>
          </div>
          <div className="mt-14 grid gap-12 md:grid-cols-3">
            {related.map((r) => (<div key={r.slug} className="reveal"><SystemCard s={r} /></div>))}
          </div>
        </div>
      </section>
    </>
  );
}
