import { Newsreader, Hanken_Grotesk, IBM_Plex_Mono } from 'next/font/google';

// Display: an editorial serif, light at size. Body/UI: an architectural grotesk.
// Mono: every number on the site (mm, m², dB, W/m²K) — specification as material.
export const headingFont = Newsreader({
  subsets: ['latin'],
  weight: ['300', '400'],
  style: ['normal', 'italic'],
  variable: '--font-heading',
  display: 'swap',
});

export const bodyFont = Hanken_Grotesk({
  subsets: ['latin'],
  weight: ['400', '500'],
  variable: '--font-body',
  display: 'swap',
});

export const monoFont = IBM_Plex_Mono({
  subsets: ['latin'],
  weight: ['400'],
  variable: '--font-mono',
  display: 'swap',
});
