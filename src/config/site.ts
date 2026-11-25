/**
 * Every brand string on the site lives here (addendum: one siteConfig).
 * Umbral is a demonstration house: there is deliberately NO phone, address,
 * or registration number. Enquiries go through the forms (Tyashin lead inbox).
 */
export const siteConfig = {
  name: 'Umbral',
  wordmark: 'UMBRAL',
  tagline: 'Thresholds, in light and shadow.',
  description:
    'Umbral makes glass walls, pivot doors, steel doors and windows with the thinnest frames we can build — each one configurable and openable in 3D before you call us.',
  mission:
    'To make the line between inside and outside as thin, as quiet and as exact as it can be — and then to make it open beautifully.',
  demoNotice:
    'Umbral is a demonstration house created by Tyashin and Thridify to show what a door and window maker’s website can be. Its products, names and specifications are illustrative.',
  nav: [
    { label: 'Collection', href: '/collection' },
    { label: 'Architects', href: '/architects' },
    { label: 'House', href: '/about' },
    { label: 'Enquire', href: '/contact' },
  ],
  social: [] as { label: string; href: string }[],
  builtBy: { tyashin: 'https://tyashin.com', thridify: 'https://thridify.com' },
} as const;
