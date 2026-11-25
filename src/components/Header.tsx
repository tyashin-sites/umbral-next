import Link from 'next/link';
import Image from 'next/image';
import { getBrandKit } from '@/lib/brand-kit';
import { siteConfig } from '@/config/site';
import { Wordmark } from './Wordmark';
import { MobileNav } from './MobileNav';
import { HeaderFX } from './HeaderFX';

export async function Header() {
  const kit = await getBrandKit();
  const logo = kit.logo?.light;
  return (
    <header className="site-header">
      <a href="#main" className="skip">Skip to content</a>
      <div className="wrap flex items-center justify-between">
        <Link href="/" className="flex items-center" aria-label={`${siteConfig.name} — home`}>
          {logo ? <Image src={logo} alt={siteConfig.name} width={140} height={32} className="h-7 w-auto" priority /> : <Wordmark />}
        </Link>
        <nav aria-label="Primary" className="hidden items-center gap-10 text-[0.78rem] font-medium uppercase tracking-[0.18em] md:flex">
          {siteConfig.nav.map((n) => (
            <Link key={n.href} href={n.href} className="link-line py-1">{n.label}</Link>
          ))}
        </nav>
        <MobileNav items={siteConfig.nav} />
      </div>
      <HeaderFX />
    </header>
  );
}
