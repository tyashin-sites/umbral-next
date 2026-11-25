import { getSiteRoutes } from '@/lib/site-routes';
import { siteUrl } from '@/lib/seo';

// Code-route sitemap (addendum §3g); the platform /sitemap.xml indexes it.
export const dynamic = 'force-static';
const ORIGIN = siteUrl('/').replace(/\/+$/, '');
const esc = (v: string) => v.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

export function GET(): Response {
  const urls = getSiteRoutes()
    .map((r) => [
      '  <url>',
      `    <loc>${esc(`${ORIGIN}${r.path === '/' ? '/' : r.path}`)}</loc>`,
      r.lastModified ? `    <lastmod>${r.lastModified}</lastmod>` : '',
      `    <changefreq>${r.changeFrequency}</changefreq>`,
      `    <priority>${r.priority.toFixed(1)}</priority>`,
      '  </url>',
    ].filter(Boolean).join('\n'))
    .join('\n');
  return new Response(`<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls}\n</urlset>\n`, {
    headers: { 'content-type': 'application/xml; charset=utf-8', 'cache-control': 'public, max-age=3600, s-maxage=86400' },
  });
}
