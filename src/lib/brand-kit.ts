/** Runtime brand kit (addendum §12): logos/colours set in Tyashin admin, ISR 5 min. */
export interface BrandKitData {
  version: number;
  siteName: string;
  logo?: { light?: string; dark?: string; monogram?: string; favicon?: string; aspectRatio?: string };
}

const API = process.env.TYASHIN_API_URL || 'https://website-api.tyashin.com';
const PROJECT_ID = process.env.PROJECT_ID || '6ae9556c0d304c5ad2874e1d';

export async function getBrandKit(): Promise<BrandKitData> {
  try {
    const res = await fetch(`${API}/api/v1/public/brand-kit.json?projectId=${PROJECT_ID}`, { next: { revalidate: 300 } });
    if (res.ok) return (await res.json()) as BrandKitData;
  } catch {
    /* fall back to the text wordmark */
  }
  return { version: 0, siteName: '' };
}
