import { pageMetadata } from '@/lib/seo';
import { Breadcrumbs } from '@/components/Breadcrumbs';
import { siteConfig } from '@/config/site';

export const metadata = pageMetadata({ title: 'Terms', description: 'The terms for using the Umbral demonstration website.', path: '/terms' });

export default function Terms() {
  return (
    <section className="wrap pt-16 pb-[var(--section)] md:pt-24">
      <Breadcrumbs items={[{ name: 'Terms' }]} />
      <h1 className="t-h1 mt-10">Terms</h1>
      <div className="mt-12 max-w-[42rem] space-y-6 text-[1.02rem] leading-relaxed text-muted">
        <p>{siteConfig.demoNotice}</p>
        <h2 className="t-h3 pt-4 text-foreground">Nothing here is an offer</h2>
        <p>Product names, specifications, finishes and sizes on this site are illustrative. Nothing on the site is an offer to sell, and no enquiry creates a contract.</p>
        <h2 className="t-h3 pt-4 text-foreground">The 3D models</h2>
        <p>The models are shown for demonstration. You may view and share links to them; you may not copy or extract the model files.</p>
        <h2 className="t-h3 pt-4 text-foreground">Liability</h2>
        <p>The site is provided as it is. Do not rely on its figures for design, procurement or construction decisions.</p>
        <p className="pt-6 text-[0.85rem]">Last updated 25 November 2026.</p>
      </div>
    </section>
  );
}
