import Link from 'next/link';
import Image from 'next/image';
import { pageMetadata } from '@/lib/seo';
import { siteConfig } from '@/config/site';
import { getSystem } from '@/data/collection';
import { Breadcrumbs } from '@/components/Breadcrumbs';
import { KnowledgeGraph } from '@/components/KnowledgeGraph';

const DESC = 'Why Umbral makes the thinnest frames it can, why every system opens in 3D on this site, and what the house believes.';
export const metadata = pageMetadata({ title: 'Philosophy', description: DESC, path: '/about' });

const BELIEFS = [
  ['The frame is a shadow.', 'Every millimetre of frame is a millimetre of shadow on the floor at four in the afternoon. We count them, and we spend most of our engineering removing them: into the floor, the ceiling, the wall.'],
  ['The opening is the product.', 'A door is judged in the two seconds it moves. We tune the weight, the travel and the stop until a three-metre leaf feels like a page turning. The sound it does not make is part of the specification.'],
  ['Weather is a guest.', 'Glass should let the season in and keep the weather out. We describe that with numbers — thermal transmittance, sound reduction, watertightness — because adjectives cannot be tested.'],
  ['Show everything.', 'A drawing is a promise; a model you can open is proof. Every Umbral system can be configured, turned and opened on this site before anyone talks to us. When you call, you already know what you want.'],
];

export default function About() {
  const eje = getSystem('eje')!;
  return (
    <>
      <KnowledgeGraph path="/about" title="Philosophy" description={DESC} crumbs={[{ name: 'Philosophy', path: '/about' }]} />
      <section className="wrap pt-16 md:pt-24">
        <Breadcrumbs items={[{ name: 'Philosophy' }]} />
        <h1 className="t-display mt-10 max-w-[13ch] hero-rise">A threshold is the only part of a house you <span className="t-italic">pass through.</span></h1>
        <p className="t-lead mt-10 max-w-[36ch] text-muted hero-rise" style={{ ['--d' as string]: '100ms' }}>We make it the part you remember.</p>
      </section>
      <section className="section">
        <div className="wrap grid gap-14 md:grid-cols-12 md:items-start">
          <div className="figure aspect-[4/5] md:col-span-5 reveal">
            <Image src={eje.stills.front} alt={`${eje.name} pivot door`} fill sizes="(min-width: 768px) 40vw, 100vw" className="object-cover" />
          </div>
          <div className="md:col-span-6 md:col-start-7">
            <p className="eyebrow reveal">Mission</p>
            <p className="t-h2 mt-6 reveal">{siteConfig.mission}</p>
            <ol className="mt-16">
              {BELIEFS.map(([t, d], i) => (
                <li key={t} className="grid grid-cols-[3rem_1fr] gap-5 border-t border-border py-8 reveal">
                  <span className="t-num text-[0.8rem] text-bronce">0{i + 1}</span>
                  <span><span className="block t-h3">{t}</span><span className="mt-3 block text-muted">{d}</span></span>
                </li>
              ))}
            </ol>
          </div>
        </div>
      </section>
      <section className="on-night grain">
        <div className="wrap section grid gap-10 md:grid-cols-12">
          <div className="md:col-span-5">
            <p className="eyebrow">About this house</p>
            <h2 className="t-h2 mt-6">Umbral is a demonstration.</h2>
          </div>
          <div className="space-y-5 md:col-span-6 md:col-start-7">
            <p className="t-body">{siteConfig.demoNotice}</p>
            <p className="t-body">The site runs on <a className="link-line text-cal" href="https://tyashin.com" target="_blank" rel="noopener">Tyashin</a>. Every product is a parametric 3D model built and hosted on <a className="link-line text-cal" href="https://thridify.com" target="_blank" rel="noopener">Thridify</a>: sizes are rebuilt from parameters rather than scaled, finishes carry real texture maps, and the opening motion is the one the hardware makes. A real manufacturer gets the same, made from its own drawings.</p>
            <div className="pt-4"><Link href="/contact" className="btn btn-primary">Enquire <span className="arrow" aria-hidden="true" /></Link></div>
          </div>
        </div>
      </section>
    </>
  );
}
