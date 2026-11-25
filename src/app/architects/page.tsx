import { pageMetadata } from '@/lib/seo';
import { SYSTEMS } from '@/data/collection';
import { Breadcrumbs } from '@/components/Breadcrumbs';
import { QuoteForm } from '@/components/QuoteForm';
import { KnowledgeGraph } from '@/components/KnowledgeGraph';
import Link from 'next/link';

const DESC = 'Section drawings, specification text and 3D models of every Umbral system, prepared for your project. For architects and interior designers.';
export const metadata = pageMetadata({ title: 'For architects', description: DESC, path: '/architects' });

const OFFER = [
  ['Sections', 'Head, sill and jamb sections for each system and configuration, at 1:1 and 1:5.'],
  ['Specification text', 'Clause-ready descriptions with the performance figures for your opening sizes.'],
  ['3D, configured', 'The model you configure on this site, exported for your own renderings and reviews.'],
  ['A drawing back', 'Send us your elevation. We return it with the opening drawn in our system, and the questions it raises.'],
];

export default function Architects() {
  return (
    <>
      <KnowledgeGraph path="/architects" title="For architects" description={DESC} crumbs={[{ name: 'For architects', path: '/architects' }]} />
      <section className="wrap pt-16 md:pt-24">
        <Breadcrumbs items={[{ name: 'For architects' }]} />
        <h1 className="t-display mt-10 max-w-[12ch] hero-rise">Drawn to your drawing.</h1>
        <p className="t-lead mt-8 max-w-[38ch] text-muted hero-rise" style={{ ['--d' as string]: '100ms' }}>Everything you need to put an Umbral opening into a set of drawings, and nothing you do not.</p>
      </section>
      <section className="section">
        <div className="wrap grid gap-px bg-border md:grid-cols-4">
          {OFFER.map(([t, d], i) => (
            <div key={t} className="bg-cal p-8 reveal" style={{ ['--d' as string]: `${i * 70}ms` }}>
              <span className="t-num text-[0.75rem] text-bronce">0{i + 1}</span>
              <h2 className="t-h3 mt-10">{t}</h2>
              <p className="mt-4 text-muted">{d}</p>
            </div>
          ))}
        </div>
      </section>
      <section className="pb-[var(--section)]">
        <div className="wrap grid gap-14 md:grid-cols-12">
          <div className="md:col-span-4">
            <p className="eyebrow">Systems</p>
            <ul className="mt-6">
              {SYSTEMS.map((s) => (
                <li key={s.slug} className="spec-row"><Link href={`/systems/${s.slug}`} className="link-line">{s.name}</Link><span className="text-[0.8rem] text-muted">{s.motion.split(',')[0].replace(/\.$/, '')}</span></li>
              ))}
            </ul>
          </div>
          <div className="md:col-span-7 md:col-start-6">
            <p className="eyebrow">Request documents</p>
            <h2 className="t-h2 mt-5">Tell us the project and the openings.</h2>
            <div className="mt-12"><QuoteForm kind="architect" /></div>
          </div>
        </div>
      </section>
    </>
  );
}
