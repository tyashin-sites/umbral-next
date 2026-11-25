/**
 * The Umbral collection — the ONE data source for every system page, family
 * page, the sitemap and the knowledge graph. Illustrative specifications:
 * Umbral is a demonstration house (see /about); geometry figures come from
 * the parametric 3D models in docs/experiences/*.json.
 */

export type FamilySlug = 'glass-walls' | 'entrances' | 'windows' | 'interiors';

export interface Family {
  slug: FamilySlug;
  name: string;
  line: string;
  intro: string;
}

export interface Spec {
  label: string;
  value: string;
}

export interface System {
  slug: string;
  name: string;
  pid: string;
  family: FamilySlug;
  /** One line: what it does, not what it is. */
  line: string;
  /** Short description for cards and meta (≤ 160 chars). */
  summary: string;
  paragraphs: string[];
  motion: string;
  sightlineMm: number;
  specs: Spec[];
  finishes: string[];
  glass: string[];
  sizes: string[];
  notes: { title: string; text: string }[];
  /** Thridify shopper preview id (admin.thridify.com/p/<id>). */
  previewId: string;
  stills: { hero: string; front: string; detail: string };
}

export const FAMILIES: Family[] = [
  {
    slug: 'glass-walls',
    name: 'Glass walls',
    line: 'Walls that step aside.',
    intro:
      'Sliding, pocketing, folding and lifting systems for openings wider than a room. The frame you see is the frame we could not remove.',
  },
  {
    slug: 'entrances',
    name: 'Entrances',
    line: 'The first thing the house says.',
    intro:
      'Pivot and hinged doors in steel, brass and bronze. Heavy enough to feel, balanced enough to open with two fingers.',
  },
  {
    slug: 'windows',
    name: 'Windows',
    line: 'Light in, weather out.',
    intro:
      'Tilt-and-turn and steel casement windows for houses that open in more than one way, and close completely.',
  },
  {
    slug: 'interiors',
    name: 'Interiors',
    line: 'Rooms that keep their light.',
    intro:
      'Steel-and-glass screens that divide a plan without darkening it. Sound stays in the room; daylight does not.',
  },
];

export const FINISH_SWATCHES: Record<string, { hex: string; en: string }> = {
  'Bronce Umbra': { hex: '#4A3A2A', en: 'Dark patinated bronze' },
  'Latón Cepillado': { hex: '#B08D57', en: 'Brushed brass' },
  'Acero Grafito': { hex: '#3A3B3C', en: 'Graphite steel, satin' },
  'Negro Carbón': { hex: '#1A1A1A', en: 'Carbon black, matte' },
  'Anodizado Natural': { hex: '#A9ABAD', en: 'Clear anodised aluminium' },
  Piedra: { hex: '#E7E2D8', en: 'Stone white, satin' },
  'Roble Ahumado': { hex: '#5B4332', en: 'Smoked oak' },
  Nogal: { hex: '#4A3426', en: 'Walnut' },
};

export const GLASS_NOTES: Record<string, string> = {
  Claro: 'Low-iron, clear to the edge',
  Satinado: 'Acid-etched, light without view',
  Acanalado: 'Reeded, 10 mm flutes',
  Bronce: 'Bronze tint, softens the sun',
};

// Filled from docs/experiences/<slug>.json once each experience is published.
export const SYSTEMS: System[] = [
  {
    slug: 'horizonte',
    name: 'Horizonte 19',
    pid: 'UMBRAL-HORIZONTE',
    family: 'glass-walls',
    line: 'Nineteen millimetres between you and the horizon.',
    summary: 'A frameless sliding glass wall. The interlock between panes is 19 mm; the frame disappears into floor, ceiling and wall.',
    paragraphs: [
      'Horizonte is a sliding wall of glass with almost nothing around it. The head and sill are recessed into the structure, so the only line left in the view is the 19 mm interlock where two panes meet.',
      'Panes run on stainless rollers inside the floor. A pane of several square metres moves with one hand and stops without a sound.',
    ],
    motion: 'Panes slide past each other on concealed floor tracks.',
    sightlineMm: 19,
    specs: [],
    finishes: [],
    glass: [],
    sizes: [],
    notes: [],
    previewId: '',
    stills: { hero: '/images/horizonte/hero.webp', front: '/images/horizonte/front.webp', detail: '/images/horizonte/detail.webp' },
  },
  {
    slug: 'esquina',
    name: 'Esquina',
    pid: 'UMBRAL-ESQUINA',
    family: 'glass-walls',
    line: 'The corner, without the corner.',
    summary: 'A post-free corner. Both legs of glass slide and pocket into the walls, and the corner of the house opens to the air.',
    paragraphs: [
      'Esquina takes the post out of the corner. Two runs of sliding glass meet at ninety degrees with no structure between them, then disappear into pockets in the walls.',
      'Closed, it is a glass corner. Open, the room has two missing walls and the floor runs straight out to the terrace.',
    ],
    motion: 'Both legs slide away from the corner and pocket into the walls.',
    sightlineMm: 0,
    specs: [],
    finishes: [],
    glass: [],
    sizes: [],
    notes: [],
    previewId: '',
    stills: { hero: '/images/esquina/hero.webp', front: '/images/esquina/front.webp', detail: '/images/esquina/detail.webp' },
  },
  {
    slug: 'pliegue',
    name: 'Pliegue',
    pid: 'UMBRAL-PLIEGUE',
    family: 'glass-walls',
    line: 'A wall that folds like a page.',
    summary: 'A folding glass wall. Panels hinge and stack to one side, opening the full width of the room.',
    paragraphs: [
      'Pliegue folds. Each panel hinges against the next and the whole wall stacks to the side in a few steps, leaving the opening nearly as wide as the room.',
      'The stack is shallow and the track is flush with the floor, so open or closed the threshold is one surface.',
    ],
    motion: 'Panels fold in pairs and stack to one side.',
    sightlineMm: 0,
    specs: [],
    finishes: [],
    glass: [],
    sizes: [],
    notes: [],
    previewId: '',
    stills: { hero: '/images/pliegue/hero.webp', front: '/images/pliegue/front.webp', detail: '/images/pliegue/detail.webp' },
  },
  {
    slug: 'patio',
    name: 'Patio',
    pid: 'UMBRAL-PATIO',
    family: 'glass-walls',
    line: 'Lift, then glide.',
    summary: 'A lift-and-slide door. A quarter turn of the handle lifts the panel off its seals; it glides, then settles back to seal.',
    paragraphs: [
      'Patio is the heaviest thing in the house that moves easily. Turning the handle lifts the panel a few millimetres off its seals; it travels on rollers, and when you turn the handle back it sinks and seals against the weather.',
      'Large panes, a sill flush with the floor and a seal that does not wear from sliding.',
    ],
    motion: 'Handle turns, the panel lifts, slides, then lowers to seal.',
    sightlineMm: 0,
    specs: [],
    finishes: [],
    glass: [],
    sizes: [],
    notes: [],
    previewId: '',
    stills: { hero: '/images/patio/hero.webp', front: '/images/patio/front.webp', detail: '/images/patio/detail.webp' },
  },
  {
    slug: 'eje',
    name: 'Eje',
    pid: 'UMBRAL-EJE',
    family: 'entrances',
    line: 'A door that turns on its own axis.',
    summary: 'An off-centre pivot entrance door in steel and brass. Taller than a room, opened with two fingers.',
    paragraphs: [
      'Eje has no hinges. The leaf turns on a pivot set in from its edge, so a door far taller than a person balances on its own axis and swings open with very little effort.',
      'The leaf is steel; the pull runs the height of the door in brass or bronze, the one part of the house everyone touches.',
    ],
    motion: 'The leaf rotates on an off-centre pivot.',
    sightlineMm: 0,
    specs: [],
    finishes: [],
    glass: [],
    sizes: [],
    notes: [],
    previewId: '',
    stills: { hero: '/images/eje/hero.webp', front: '/images/eje/front.webp', detail: '/images/eje/detail.webp' },
  },
  {
    slug: 'reja',
    name: 'Reja',
    pid: 'UMBRAL-REJA',
    family: 'entrances',
    line: 'Steel drawn as thin as a pencil line.',
    summary: 'Slim-profile steel French doors with sidelites and transom. A grid of light, held by very little steel.',
    paragraphs: [
      'Reja is a pair of steel doors drawn with a fine pen. Hot-rolled profiles carry the glass in slender bars, and the grid of light they make is the architecture of the room.',
      'Sidelites and a transom extend the same grid around the doors, so one opening reads as a single wall of panes.',
    ],
    motion: 'A pair of leaves swings open from the centre.',
    sightlineMm: 0,
    specs: [],
    finishes: [],
    glass: [],
    sizes: [],
    notes: [],
    previewId: '',
    stills: { hero: '/images/reja/hero.webp', front: '/images/reja/front.webp', detail: '/images/reja/detail.webp' },
  },
  {
    slug: 'alba',
    name: 'Alba',
    pid: 'UMBRAL-ALBA',
    family: 'windows',
    line: 'Opens two ways. Closes one.',
    summary: 'A tilt-and-turn window. Tilt it for air at night; turn it fully open in the morning; close it on three seals.',
    paragraphs: [
      'Alba opens in two ways from one handle. A quarter turn tilts the sash in at the top for air you can sleep with; a half turn swings it fully open.',
      'Closed, the sash pulls tight onto its seals from every side. The room goes quiet.',
    ],
    motion: 'The sash tilts in at the top, or turns fully open on its side.',
    sightlineMm: 0,
    specs: [],
    finishes: [],
    glass: [],
    sizes: [],
    notes: [],
    previewId: '',
    stills: { hero: '/images/alba/hero.webp', front: '/images/alba/front.webp', detail: '/images/alba/detail.webp' },
  },
  {
    slug: 'batiente',
    name: 'Batiente',
    pid: 'UMBRAL-BATIENTE',
    family: 'windows',
    line: 'The leaf that swings.',
    summary: 'A steel casement window. A cam handle draws the sash onto its seal; released, it swings out on concealed hinges.',
    paragraphs: [
      'Batiente is the oldest kind of window, made exactly. A cam handle lifts and pulls the steel sash against its seal; released, the sash swings outward on hinges you barely see.',
      'Slim steel, deep shadows in the reveal, and glass set in putty-line beads.',
    ],
    motion: 'The cam releases and the sash swings out.',
    sightlineMm: 0,
    specs: [],
    finishes: [],
    glass: [],
    sizes: [],
    notes: [],
    previewId: '',
    stills: { hero: '/images/batiente/hero.webp', front: '/images/batiente/front.webp', detail: '/images/batiente/detail.webp' },
  },
  {
    slug: 'tamiz',
    name: 'Tamiz',
    pid: 'UMBRAL-TAMIZ',
    family: 'interiors',
    line: 'A wall that keeps the light.',
    summary: 'An interior steel-and-glass screen with doors. Divides the plan, passes the daylight through.',
    paragraphs: [
      'Tamiz divides a room without closing it. A steel grid holds clear, etched or reeded glass, so the study keeps its quiet and the hall keeps its light.',
      'Doors are framed into the same grid and swing on the same lines; closed, you cannot tell where the wall ends and the door begins.',
    ],
    motion: 'The paired doors in the screen swing open.',
    sightlineMm: 0,
    specs: [],
    finishes: [],
    glass: [],
    sizes: [],
    notes: [],
    previewId: '',
    stills: { hero: '/images/tamiz/hero.webp', front: '/images/tamiz/front.webp', detail: '/images/tamiz/detail.webp' },
  },
];

export function getSystem(slug: string): System | undefined {
  return SYSTEMS.find((s) => s.slug === slug);
}

export function getFamily(slug: string): Family | undefined {
  return FAMILIES.find((f) => f.slug === slug);
}

export function systemsIn(family: FamilySlug): System[] {
  return SYSTEMS.filter((s) => s.family === family);
}

export function shopperUrl(previewId: string): string {
  return `https://admin.thridify.com/p/${encodeURIComponent(previewId)}`;
}
