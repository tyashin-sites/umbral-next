# Umbral — design spec (canonical; deviations are bugs)

**Thesis:** a quiet, exact house that measures itself in millimetres of frame — limestone light,
ink shadow, one bronze accent — where every product can be opened in 3D.

**Anti-goals (the "AI website" tells we refuse):** Inter/Space Grotesk display, purple/indigo/cyan,
gradient text, glassmorphism cards, centered hero + three icon cards, emoji or Lucide-in-tinted-square
icons, "Elevate/Seamless/Timeless" copy, fake testimonials, stat bands ("10k+ clients"), fade-up on
everything, bouncy easing, identical rounded-2xl cards. The logo test: put a competitor's name on the
hero — "the part of the house you pass through" + a shadow clock + 22 mm only works for Umbral.

## Colour
| Token | Hex | Use |
|---|---|---|
| Cal | #ECE7DE | dominant ground (~70%) |
| Luz | #F7F4EE | raised surfaces, hover |
| Tinta | #16140F | text, night sections (~20%) |
| Umbra | #2A251E | shadow, deep surfaces |
| Bronce | #8A6A47 | the only accent: rules, numbers, focus (≤3%) |
| Vidrio | #C7D0CE | glass in drawings only |
Forbidden: grey shadows, any blue/purple UI colour, gradients on text.

## Type
Newsreader 300/400 + italic (display, h1–h3, lead) · Hanken Grotesk 400/500 (body, UI, labels) ·
IBM Plex Mono 400 (every number). Display tracking −0.035em, line-height ≥0.98. Sentence case.
Eyebrows: 0.72rem, 0.22em tracking, uppercase, bronze hairline dash.

## Text budgets
Hero h1 ≤ 9 words. Section headline ≤ 12 words. Paragraph ≤ 3 sentences. One italic phrase per headline at most.

## Surfaces & lines
Radius 2 px. Hairlines (ink 14%) carry structure; boxes are rare. Night sections: ink + 7% warm grain.
Shadows tinted ink/umbra, two layers (rest/lift).

## Motion
One curve `cubic-bezier(.22,.61,.21,1)`. Reveal 1.1 s rise + blur settle, below the fold only, visible
without JS. Hero: CSS transform-only rise (never hidden — LCP law). Header condenses by colour/shadow,
never height (CLS law). Reduced motion kills all travel.

## Signature moments
1. Shadow clock (home hero) — mullion shadow placed by local time, advanced by scroll.
2. Sightline (home + Horizonte) — true-to-scale elevation, drag frame from 86 mm stiles to 22 mm.
3. Open it (every system) — Thridify 3D experience, poster-first, click to mount.

## Pages (one intent per URL)
/ (believe + browse) · /collection · /collection/[family] · /systems/[slug] (configure → quote) ·
/architects (documents) · /about (philosophy + demo disclosure) · /contact (quotation) · /privacy · /terms.

## Performance budget
LCP ≤ 2.5 s mobile, CLS 0, no third-party JS before interaction (3D mounts on click). If an idea breaks
the budget, the idea loses.
