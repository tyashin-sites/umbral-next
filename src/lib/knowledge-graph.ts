import { siteConfig } from '@/config/site';
import { siteUrl } from '@/lib/seo';
import type { System } from '@/data/collection';

type Node = Record<string, unknown>;

/**
 * ONE interlinked @graph per page (addendum §3b). Umbral quotes per opening, so a
 * system page is an ItemPage, never a Product node without offers (§3b priceless rule).
 */
export function buildGraph(opts: {
  path: string;
  title?: string;
  description?: string;
  crumbs?: { name: string; path: string }[];
  system?: System;
}): Node {
  const origin = siteUrl('/').replace(/\/+$/, '');
  const pageUrl = siteUrl(opts.path);
  const org: Node = {
    '@type': 'Organization',
    '@id': `${origin}/#organization`,
    name: siteConfig.name,
    url: `${origin}/`,
    logo: `${origin}/icon.png`,
    description: siteConfig.description,
    slogan: siteConfig.tagline,
    knowsAbout: [
      'minimal frame sliding glass walls', 'pocketing corner doors', 'folding glass walls', 'lift-and-slide doors',
      'pivot entrance doors', 'steel French doors', 'tilt-and-turn windows', 'steel casement windows',
      'interior steel and glass screens', 'architectural glazing', '3D door and window configurators',
    ],
    ...(siteConfig.social.length ? { sameAs: siteConfig.social.map((s) => s.href) } : {}),
  };
  const website: Node = { '@type': 'WebSite', '@id': `${origin}/#website`, url: `${origin}/`, name: siteConfig.name, publisher: { '@id': `${origin}/#organization` }, inLanguage: 'en' };
  const graph: Node[] = [org, website];

  if (opts.path !== '/') {
    const page: Node = {
      '@type': opts.system ? 'ItemPage' : 'WebPage',
      '@id': `${pageUrl}#webpage`,
      url: pageUrl,
      name: opts.title,
      description: opts.description,
      isPartOf: { '@id': `${origin}/#website` },
      about: { '@id': `${origin}/#organization` },
      breadcrumb: { '@id': `${pageUrl}#breadcrumb` },
    };
    if (opts.system) page.primaryImageOfPage = { '@type': 'ImageObject', url: `${origin}${opts.system.stills.hero}` };
    graph.push(page);
    const crumbs = [{ name: 'Umbral', path: '/' }, ...(opts.crumbs ?? [])];
    graph.push({
      '@type': 'BreadcrumbList',
      '@id': `${pageUrl}#breadcrumb`,
      itemListElement: crumbs.map((c, i) => ({ '@type': 'ListItem', position: i + 1, name: c.name, item: siteUrl(c.path) })),
    });
  }
  return { '@context': 'https://schema.org', '@graph': graph };
}
