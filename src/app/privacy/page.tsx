import { pageMetadata } from '@/lib/seo';
import { Breadcrumbs } from '@/components/Breadcrumbs';

export const metadata = pageMetadata({ title: 'Privacy', description: 'How Umbral handles the details you send through this website.', path: '/privacy' });

export default function Privacy() {
  return (
    <section className="wrap pt-16 pb-[var(--section)] md:pt-24">
      <Breadcrumbs items={[{ name: 'Privacy' }]} />
      <h1 className="t-h1 mt-10">Privacy</h1>
      <div className="mt-12 max-w-[42rem] space-y-6 text-[1.02rem] leading-relaxed text-muted">
        <p>Umbral is a demonstration website. This notice says what happens to what you send us here.</p>
        <h2 className="t-h3 pt-4 text-foreground">What we collect</h2>
        <p>Only what you type into an enquiry form: your name, email, and optionally your phone number, project location, opening sizes and message. We also record which page you sent it from.</p>
        <h2 className="t-h3 pt-4 text-foreground">Why</h2>
        <p>To answer your enquiry. We do not sell your details, add you to a mailing list, or use them for advertising.</p>
        <h2 className="t-h3 pt-4 text-foreground">Where it is kept</h2>
        <p>Enquiries are stored in the website platform that runs this site (Tyashin). The 3D viewer is provided by Thridify and loads only when you open a model.</p>
        <h2 className="t-h3 pt-4 text-foreground">Your choices</h2>
        <p>Ask us through the enquiry form to see, correct or delete what you sent, and we will do it.</p>
        <p className="pt-6 text-[0.85rem]">Last updated 25 November 2026.</p>
      </div>
    </section>
  );
}
