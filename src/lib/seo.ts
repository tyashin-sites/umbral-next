import type { Metadata } from 'next';
import { siteConfig } from '@/config/site';

const PROJECT_SLUG = process.env.PROJECT_SLUG || 'doors-website';
const CUSTOM_DOMAIN = process.env.NEXT_PUBLIC_SITE_DOMAIN || process.env.SITE_DOMAIN || '';

/** ONE canonical host (addendum §3c): the slug host until a real domain exists. */
export const SITE = {
  name: siteConfig.name,
  domain: CUSTOM_DOMAIN || `${PROJECT_SLUG}.sites.tyashin.com`,
  isCustomDomain: Boolean(CUSTOM_DOMAIN),
  defaultOgImage: '/og-default.jpg',
  locale: 'en_GB',
  twitter: '',
};

export function siteUrl(path = '/'): string {
  const host = SITE.isCustomDomain ? `www.${SITE.domain}` : SITE.domain;
  const p = path === '/' ? '' : `/${path.replace(/^\/+/, '')}`;
  return `https://${host}${p}`;
}

export const NOINDEX = (process.env.ROBOTS_NOINDEX ?? 'true') !== 'false';

export function pageMetadata(opts: {
  title?: string;
  description: string;
  path: string;
  image?: string;
  type?: 'website' | 'article';
}): Metadata {
  const url = siteUrl(opts.path);
  const image = opts.image || SITE.defaultOgImage;
  const title = opts.title || SITE.name;
  return {
    title: opts.title,
    description: opts.description,
    alternates: { canonical: url },
    openGraph: { type: opts.type || 'website', url, siteName: SITE.name, title, description: opts.description, locale: SITE.locale, images: [{ url: image }] },
    twitter: { card: 'summary_large_image', title, description: opts.description, images: [image] },
  };
}
