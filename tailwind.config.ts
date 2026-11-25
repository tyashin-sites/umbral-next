import type { Config } from 'tailwindcss';

// Every token resolves to a --brand-* variable (addendum §13) so the runtime
// /brand-kit.css can retune the palette without a rebuild. Values live in
// globals.css; docs/DESIGN-SPEC.md is the source of truth.
export default {
  content: ['./src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: 'var(--brand-primary)',
        'primary-contrast': 'var(--brand-primary-contrast)',
        accent: 'var(--brand-accent)',
        background: 'var(--brand-bg)',
        surface: 'var(--brand-surface)',
        foreground: 'var(--brand-text)',
        muted: 'var(--brand-text-muted)',
        border: 'var(--brand-border)',
        ink: 'var(--u-ink)',
        umbra: 'var(--u-umbra)',
        cal: 'var(--u-cal)',
        luz: 'var(--u-luz)',
        bronce: 'var(--u-bronce)',
        vidrio: 'var(--u-vidrio)',
      },
      borderRadius: {
        sm: 'var(--brand-radius-sm)',
        md: 'var(--brand-radius-md)',
        lg: 'var(--brand-radius-lg)',
        full: 'var(--brand-radius-full)',
      },
      fontFamily: {
        heading: ['var(--brand-heading-font)'],
        body: ['var(--brand-body-font)'],
        mono: ['var(--font-mono)'],
      },
    },
  },
} satisfies Config;
