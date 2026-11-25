import { pageMetadata } from '@/lib/seo';
import { Breadcrumbs } from '@/components/Breadcrumbs';
import { QuoteForm } from '@/components/QuoteForm';
import { KnowledgeGraph } from '@/components/KnowledgeGraph';

const DESC = 'Ask Umbral for a quotation for your opening. Send the size and the system; we reply with questions, a drawing and a price.';
export const metadata = pageMetadata({ title: 'Enquire', description: DESC, path: '/contact' });

export default async function Contact({ searchParams }: { searchParams: Promise<{ system?: string }> }) {
  const { system } = await searchParams;
  return (
    <>
      <KnowledgeGraph path="/contact" title="Enquire" description={DESC} crumbs={[{ name: 'Enquire', path: '/contact' }]} />
      <section className="wrap pt-16 pb-[var(--section)] md:pt-24">
        <Breadcrumbs items={[{ name: 'Enquire' }]} />
        <div className="mt-10 grid gap-16 md:grid-cols-12">
          <div className="md:col-span-5">
            <h1 className="t-display hero-rise">Tell us about the opening.</h1>
            <p className="t-body mt-8 hero-rise" style={{ ['--d' as string]: '100ms' }}>Width, height, where it is, and what you liked in 3D. If you do not know the size yet, say so — most of our conversations start with a sketch.</p>
          </div>
          <div className="md:col-span-7"><QuoteForm system={system} /></div>
        </div>
      </section>
    </>
  );
}
