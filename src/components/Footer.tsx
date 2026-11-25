import Link from 'next/link';
import Image from 'next/image';
import { getBrandKit } from '@/lib/brand-kit';
import { siteConfig } from '@/config/site';
import { FAMILIES, SYSTEMS } from '@/data/collection';
import { Wordmark } from './Wordmark';

export async function Footer() {
  const kit = await getBrandKit();
  const logo = kit.logo?.dark;
  return (
    <footer className="on-night grain">
      <div className="wrap pt-24 pb-10">
        <div className="grid gap-16 md:grid-cols-12">
          <div className="md:col-span-5">
            {logo ? <Image src={logo} alt={siteConfig.name} width={160} height={36} className="h-8 w-auto" /> : <Wordmark className="text-cal" />}
            <p className="t-lead mt-8 max-w-[22ch] text-cal">{siteConfig.tagline}</p>
          </div>
          <nav aria-label="Collection" className="md:col-span-3">
            <p className="eyebrow">Collection</p>
            <ul className="mt-6 space-y-3 text-[0.95rem] text-[#cfc6b6]">
              {FAMILIES.map((f) => (
                <li key={f.slug}><Link className="link-line" href={`/collection/${f.slug}`}>{f.name}</Link></li>
              ))}
            </ul>
            <ul className="mt-6 grid grid-cols-2 gap-x-6 gap-y-2 text-[0.85rem] text-[#a99f8f]">
              {SYSTEMS.map((s) => (
                <li key={s.slug}><Link className="link-line" href={`/systems/${s.slug}`}>{s.name}</Link></li>
              ))}
            </ul>
          </nav>
          <nav aria-label="House" className="md:col-span-2">
            <p className="eyebrow">House</p>
            <ul className="mt-6 space-y-3 text-[0.95rem] text-[#cfc6b6]">
              <li><Link className="link-line" href="/about">Philosophy</Link></li>
              <li><Link className="link-line" href="/architects">For architects</Link></li>
              <li><Link className="link-line" href="/contact">Enquire</Link></li>
            </ul>
          </nav>
          <nav aria-label="Legal" className="md:col-span-2">
            <p className="eyebrow">Legal</p>
            <ul className="mt-6 space-y-3 text-[0.95rem] text-[#cfc6b6]">
              <li><Link className="link-line" href="/privacy">Privacy</Link></li>
              <li><Link className="link-line" href="/terms">Terms</Link></li>
            </ul>
          </nav>
        </div>
        <div className="rule-bronze mt-20" />
        <p className="mt-8 max-w-3xl text-[0.8rem] leading-relaxed text-[#a99f8f]">{siteConfig.demoNotice}</p>
        <div className="mt-10 flex flex-col justify-between gap-3 text-[0.75rem] text-[#8f8676] md:flex-row">
          <p>© {new Date().getFullYear()} Umbral. Made to size.</p>
          <p>3D experiences by <a href={siteConfig.builtBy.thridify} target="_blank" rel="noopener" className="link-line text-[#cfc6b6]">Thridify</a></p>
        </div>
        <div className="mt-8 border-t border-[rgb(236_231_222/0.08)] pt-6 text-center">
          <p className="text-xs text-[#8f8676]">Powered by <a href="https://tyashin.com" target="_blank" rel="noopener" className="hover:text-[#b6916a] hover:underline">Tyashin</a></p>
        </div>
      </div>
    </footer>
  );
}
