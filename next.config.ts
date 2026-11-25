import { initOpenNextCloudflareForDev } from '@opennextjs/cloudflare';
initOpenNextCloudflareForDev();

const PROJECT_ID = process.env.PROJECT_ID || '6ae9556c0d304c5ad2874e1d';
const PROJECT_SLUG = process.env.PROJECT_SLUG || 'doors-website';

const nextConfig = {
  env: {
    NEXT_PUBLIC_TYASHIN_API_KEY: process.env.TYASHIN_API_KEY || '',
    NEXT_PUBLIC_PROJECT_ID: PROJECT_ID,
    NEXT_PUBLIC_TYASHIN_API_URL: process.env.TYASHIN_API_URL || 'https://website-api.tyashin.com',
    NEXT_PUBLIC_SITE_DOMAIN: process.env.SITE_DOMAIN || '',
  },
  images: {
    formats: ['image/avif', 'image/webp'] as ('image/avif' | 'image/webp')[],
    // Allowlist only (never '**': open image proxy).
    remotePatterns: [
      { protocol: 'https' as const, hostname: 'website-api.tyashin.com' },
      { protocol: 'https' as const, hostname: '*.tyashin.com' },
      { protocol: 'https' as const, hostname: '*.thridify.com' },
    ],
  },
  async redirects() {
    return [
      { source: '/products', destination: '/collection', permanent: true },
      { source: '/shop', destination: '/collection', permanent: true },
    ];
  },
  async rewrites() {
    // Platform-owned paths are dispatched by Tyashin on the real host; on direct
    // workers.dev access proxy them to the slug host. No-op in production.
    const ORIGIN = process.env.TYASHIN_STOREFRONT_ORIGIN || `https://${PROJECT_SLUG}.sites.tyashin.com`;
    return [
      { source: '/brand-kit.css', destination: `${ORIGIN}/brand-kit.css` },
      { source: '/tyashin-runtime.js', destination: `${ORIGIN}/tyashin-runtime.js` },
      { source: '/sitemap.xml', destination: `${ORIGIN}/sitemap.xml` },
      { source: '/robots.txt', destination: `${ORIGIN}/robots.txt` },
    ];
  },
};

export default nextConfig;
