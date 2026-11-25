import type { Metadata, Viewport } from 'next';
import { bodyFont, headingFont, monoFont } from '@/lib/fonts';
import { Header } from '@/components/Header';
import { Footer } from '@/components/Footer';
import { RevealObserver } from '@/components/Reveal';
import { SITE, siteUrl, NOINDEX } from '@/lib/seo';
import { siteConfig } from '@/config/site';
import './globals.css';

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl('/')),
  title: { default: `${SITE.name} — ${siteConfig.tagline}`, template: `%s · ${SITE.name}` },
  description: siteConfig.description,
  openGraph: { type: 'website', siteName: SITE.name, locale: SITE.locale, url: siteUrl('/'), title: SITE.name, images: [{ url: SITE.defaultOgImage }] },
  twitter: { card: 'summary_large_image' },
  robots: NOINDEX ? { index: false, follow: true } : undefined,
};

export const viewport: Viewport = { themeColor: '#ECE7DE' };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${bodyFont.variable} ${headingFont.variable} ${monoFont.variable}`} style={{ backgroundColor: '#ECE7DE' }}>
      <body className="font-body bg-background text-foreground antialiased" style={{ backgroundColor: '#ECE7DE' }}>
        <Header />
        <main id="main" className="min-h-screen overflow-x-clip">{children}</main>
        <Footer />
        <RevealObserver />
      </body>
    </html>
  );
}
