import { FAMILIES, SYSTEMS } from '@/data/collection';

export interface SiteRoute { path: string; priority: number; changeFrequency: 'weekly' | 'monthly' | 'yearly'; lastModified?: string }

const LAUNCH = '2026-11-25';

/** Every indexable code route. Dynamic routes' generateStaticParams read the same arrays. */
export function getSiteRoutes(): SiteRoute[] {
  return [
    { path: '/', priority: 1, changeFrequency: 'monthly', lastModified: LAUNCH },
    { path: '/collection', priority: 0.9, changeFrequency: 'monthly', lastModified: LAUNCH },
    ...FAMILIES.map((f) => ({ path: `/collection/${f.slug}`, priority: 0.8, changeFrequency: 'monthly' as const, lastModified: LAUNCH })),
    ...SYSTEMS.map((s) => ({ path: `/systems/${s.slug}`, priority: 0.8, changeFrequency: 'monthly' as const, lastModified: LAUNCH })),
    { path: '/architects', priority: 0.6, changeFrequency: 'monthly', lastModified: LAUNCH },
    { path: '/about', priority: 0.6, changeFrequency: 'yearly', lastModified: LAUNCH },
    { path: '/contact', priority: 0.6, changeFrequency: 'yearly', lastModified: LAUNCH },
    { path: '/privacy', priority: 0.2, changeFrequency: 'yearly', lastModified: LAUNCH },
    { path: '/terms', priority: 0.2, changeFrequency: 'yearly', lastModified: LAUNCH },
  ];
}
