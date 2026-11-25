import Link from 'next/link';
import Image from 'next/image';
import { pageMetadata } from '@/lib/seo';
import { siteConfig } from '@/config/site';
import { SYSTEMS, FAMILIES, getSystem, systemsIn } from '@/data/collection';
import { ShadowClock } from '@/components/signature/ShadowClock';
import { Sightline } from '@/components/signature/Sightline';
import { Experience } from '@/components/Experience';
import { SystemIndex } from '@/components/SystemIndex';
import { KnowledgeGraph } from '@/components/KnowledgeGraph';

export const metadata = pageMetadata({
  title: 'Glass walls, pivot doors and windows with almost no frame',
  description: siteConfig.description,
  path: '/',
});

const BELIEFS = [
  { n: '01', title: 'The frame is a shadow.', text: 'Every millimetre of frame is a millimetre of shadow on the floor at four in the afternoon. We count them.' },
  { n: '02', title: 'The opening is the product.', text: 'A door is judged in the two seconds it moves: its weight, its travel, the sound it does not make.' },
  { n: '03', title: 'Weather is a guest.', text: 'Glass should let the season in and keep the weather out. Numbers prove that. Adjectives do not.' },
  { n: '04', title: 'Show everything.', text: 'Every system here can be configured, turned and opened before anyone talks to us. A model you can open is proof.' },
];

export default function Home() {
  const lead = getSystem('horizonte')!;
  const feature = getSystem('eje')!;
  return (
    <>
      <KnowledgeGraph path="/" />

      {/* ── Hero: the shadow clock ─────────────────────────────── */}
      <section data-sun-root className="relative -mt-[72px] flex min-h-[100svh] items-end overflow-hidden pb-[clamp(3rem,8vh,6rem)] pt-[140px]">
        <ShadowClock />
        <div className="wrap relative">
          <p className="eyebrow hero-fade" style={{ ['--d' as string]: '200ms' }}>Glass walls · Entrances · Windows</p>
          <h1 className="t-display mt-8 max-w-[11ch] hero-rise">The part of the house you <span className="t-italic">pass through.</span></h1>
          <div className="mt-10 grid gap-8 md:grid-cols-12 md:items-end">
            <p className="t-lead max-w-[30ch] text-[#3d372e] md:col-span-6 hero-rise" style={{ ['--d' as string]: '120ms' }}>
              Openings with the least frame we can build. Every one can be configured and opened here, in 3D, before we speak.
            </p>
            <div className="flex flex-wrap items-center gap-6 md:col-span-6 md:justify-end hero-fade" style={{ ['--d' as string]: '500ms' }}>
              <Link href="/collection" className="btn btn-primary">See the collection <span className="arrow" aria-hidden="true" /></Link>
              <Link href={`/systems/${lead.slug}`} className="link-line text-[0.8rem] font-medium uppercase tracking-[0.16em]">Open {lead.name} in 3D</Link>
            </div>
          </div>
        </div>
      </section>

      {/* ── Manifesto: asymmetric, image-led ───────────────────── */}
      <section className="section">
        <div className="wrap grid gap-14 md:grid-cols-12 md:items-center">
          <div className="md:col-span-5 md:pr-6">
            <p className="eyebrow reveal">Umbral</p>
            <p className="t-h2 mt-8 reveal">Umbral means <span className="t-italic">threshold.</span> It is one letter from <span className="t-italic">umbra</span> — the darkest part of a shadow.</p>
            <p className="t-body mt-8 reveal">We make the thresholds of serious houses: walls of glass that step aside, doors that turn on their own axis, windows that open two ways and close completely. We measure our work in millimetres of frame you no longer see.</p>
            <Link href="/about" className="link-line mt-10 inline-block text-[0.8rem] font-medium uppercase tracking-[0.16em] reveal">Our philosophy</Link>
          </div>
          <div className="md:col-span-7">
            <Link href={`/systems/${lead.slug}`} className="figure figure-hover block aspect-[16/11] reveal">
              <Image src={lead.stills.hero} alt={`${lead.name} sliding glass wall, partly open, late-afternoon light`} fill sizes="(min-width: 768px) 58vw, 100vw" className="object-cover" />
            </Link>
            <p className="mt-4 flex justify-between text-[0.75rem] uppercase tracking-[0.18em] text-muted"><span>{lead.name}</span><span className="t-num normal-case tracking-normal">22 mm interlock</span></p>
          </div>
        </div>
      </section>

      {/* ── Families: four lines, then the full index ─────────── */}
      <section className="section pt-0">
        <div className="wrap">
          <div className="flex flex-col justify-between gap-6 md:flex-row md:items-end">
            <h2 className="t-h1 max-w-[14ch] reveal">Nine systems. Four kinds of threshold.</h2>
            <Link href="/collection" className="link-line text-[0.8rem] font-medium uppercase tracking-[0.16em] reveal">The whole collection</Link>
          </div>
          <div className="mt-16 grid gap-px bg-border md:grid-cols-4">
            {FAMILIES.map((f, i) => (
              <Link key={f.slug} href={`/collection/${f.slug}`} className="group bg-cal p-7 pb-9 transition-colors duration-500 hover:bg-luz reveal" style={{ ['--d' as string]: `${i * 80}ms` }}>
                <span className="t-num text-[0.75rem] text-bronce">0{i + 1}</span>
                <span className="mt-10 block t-h3">{f.name}</span>
                <span className="mt-3 block font-heading italic text-muted">{f.line}</span>
                <span className="mt-8 block text-[0.72rem] uppercase tracking-[0.2em] text-muted">{systemsIn(f.slug).map((s) => s.name).join(' · ')}</span>
              </Link>
            ))}
          </div>
          <div className="mt-20"><SystemIndex systems={SYSTEMS} /></div>
        </div>
      </section>

      {/* ── Signature 2 ─────────────────────────────────────────── */}
      <Sightline target={22} opening={6000} label="Horizonte 22" />

      {/* ── Signature 3: open it ───────────────────────────────── */}
      <section className="section">
        <div className="wrap grid gap-12 lg:grid-cols-12 lg:items-center">
          <div className="lg:col-span-4">
            <p className="eyebrow reveal">Open it</p>
            <h2 className="t-h2 mt-6 reveal">A drawing is a promise. A model you can open is proof.</h2>
            <p className="t-body mt-6 reveal">{feature.name} is a steel door that turns on a pivot set in from its edge. Choose the finish, the glass and the size, then open it. Every system on this site works the same way.</p>
            <Link href={`/systems/${feature.slug}`} className="link-line mt-8 inline-block text-[0.8rem] font-medium uppercase tracking-[0.16em] reveal">{feature.name}, in full</Link>
          </div>
          <div className="lg:col-span-8 reveal">
            <Experience name={feature.name} pid={feature.pid} poster={feature.stills.hero} />
          </div>
        </div>
      </section>

      {/* ── Beliefs: numbered, on hairlines (never a card grid) ── */}
      <section className="section pt-0">
        <div className="wrap grid gap-12 md:grid-cols-12">
          <div className="md:col-span-4">
            <p className="eyebrow reveal">What we believe</p>
          </div>
          <ol className="md:col-span-8">
            {BELIEFS.map((b, i) => (
              <li key={b.n} className="grid grid-cols-[3rem_1fr] gap-6 border-t border-border py-9 md:grid-cols-[4rem_minmax(0,5fr)_minmax(0,6fr)] reveal" style={{ ['--d' as string]: `${i * 60}ms` }}>
                <span className="t-num text-[0.8rem] text-bronce">{b.n}</span>
                <h3 className="t-h3">{b.title}</h3>
                <p className="col-start-2 text-muted md:col-start-3">{b.text}</p>
              </li>
            ))}
          </ol>
        </div>
      </section>

      {/* ── Architects + enquiry ───────────────────────────────── */}
      <section className="on-night grain">
        <div className="wrap section grid gap-12 md:grid-cols-12 md:items-end">
          <div className="md:col-span-7">
            <p className="eyebrow reveal">For architects</p>
            <h2 className="t-h1 mt-6 max-w-[16ch] reveal">Sections, specifications, and an opening configured to your drawing.</h2>
          </div>
          <div className="flex flex-wrap gap-5 md:col-span-5 md:justify-end reveal">
            <Link href="/architects" className="btn btn-ghost">Architects <span className="arrow" aria-hidden="true" /></Link>
            <Link href="/contact" className="btn btn-primary">Enquire <span className="arrow" aria-hidden="true" /></Link>
          </div>
        </div>
      </section>
    </>
  );
}
