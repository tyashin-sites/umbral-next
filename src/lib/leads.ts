/** The one way the site writes a lead: POST /api/v1/contact/public/submit (X-API-Key → project) → Tyashin lead inbox. */
const PROJECT_ID = process.env.NEXT_PUBLIC_PROJECT_ID || '6ae9556c0d304c5ad2874e1d';
const API_URL = process.env.NEXT_PUBLIC_TYASHIN_API_URL || 'https://website-api.tyashin.com';
const API_KEY = process.env.NEXT_PUBLIC_TYASHIN_API_KEY || '';

export interface LeadPayload {
  name: string;
  email: string;
  phone?: string;
  subject?: string;
  message: string;
  source: string;
  customFields?: Record<string, string>;
}

// Time-trap: the API drops submissions made within ~2 s of the form rendering.
const RENDERED_AT = typeof window !== 'undefined' ? Date.now() : 0;

export async function submitLead(payload: LeadPayload): Promise<void> {
  const res = await fetch(`${API_URL}/api/v1/contact/public/submit`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...(API_KEY ? { 'X-API-Key': API_KEY } : {}) },
    body: JSON.stringify({ ...payload, renderedAt: RENDERED_AT || undefined, metadata: { projectId: PROJECT_ID }, pageUrl: typeof window !== 'undefined' ? window.location.href.slice(0, 500) : undefined }),
  });
  const json = (await res.json().catch(() => null)) as { success?: boolean; error?: { message?: string } } | null;
  if (!json?.success) throw new Error(json?.error?.message || 'We could not send that. Please try again.');
}
