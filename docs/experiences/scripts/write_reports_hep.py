"""Writes docs/experiences/{horizonte,esquina,patio}.json from the payloads and ids."""
import json, os, sys
D = os.path.expanduser('~/Documents/Claude-Workspace/thridify-demos-2026-11/doorswindows/umbral-hep/')
pay = json.load(open(D + 'payloads.json')); spec = json.load(open(D + 'finish_spec.json')); ids = json.load(open(D + 'product_ids.json'))
prev = json.load(open(D + 'preview_ids.json'))
OUT = os.path.expanduser('~/Documents/Claude-Workspace/tyashin-customer-sites/umbral-next/docs/experiences/')
META = {
 'h': dict(slug='horizonte', name='Umbral Horizonte 19', pid='UMBRAL-HORIZONTE', sourceFolder='09-skyframe',
   motion='The moving pane glides sideways on the outer track and parks behind the fixed pane (centre-opening sizes: both middle panes part outwards); 8 s clip Panels_Slide, from the first hotspot.',
   sizes=[('2 panels · 4.4 × 2.8 m', 4400, 2800), ('2 panels · 6.0 × 2.8 m', 6000, 2800), ('4 panels, centre opening · 6.0 × 2.8 m', 6000, 2800), ('4 panels, centre opening · 8.0 × 2.8 m', 8000, 2800)],
   geometry={'sightline_mm': 22, 'frame_depth_mm': 136, 'max_panel_w_mm': 3000, 'max_panel_h_mm': 2800, 'glazing': '12 mm single (monolithic)'},
   finish='Bronce Umbra', default_size='2 panels · 6.0 × 2.8 m',
   options=['Size (4 variants)', 'Floor track: Flush (floor runs over it) / Visible track', 'Glass: Claro / Satinado / Gris', 'Frame finish (5)', 'Pull handle finish (5)'],
   gaps=['The name says 19 but the model\'s interlock stile is 22 mm wide (the source generator\'s estimate); the sightline figure here is the model\'s real 22 mm.',
         'Glass: no reeded or bronze-tint pane exists in this model, so the set is Claro (low-iron), Satinado and Gris (grey tint, outside the BRAND glass list); the source\'s plain clear-float pane is kept hidden.',
         'Material names carry the product (\'Umbral – Bronce Umbra · Horizonte\') because material names must be unique per account and each product\'s maps differ.',
         'Hotspots are placed for the 6.0 m sizes; on 4.4 m and 8.0 m they sit on the same glass/stile positions.',
         'Internal GLB node names were renamed (root Horizonte); no logo meshes existed in the source model.']),
 'e': dict(slug='esquina', name='Umbral Esquina', pid='UMBRAL-ESQUINA', sourceFolder='w2-12-fleetwood',
   motion='Both legs of the corner telescope into their wall pockets (lead panel collects each next panel at the interlock), leg B 8 frames behind; 9 s clip Panels_Pocket_<size>, plus a short lead-panel slide on the flush-pull hotspot.',
   sizes=[('Corner · 3 + 3 panels · 3.66 + 3.66 × 3.05 m', 7315, 3048), ('Corner · 2 + 2 panels · 2.44 + 2.44 × 2.74 m', 4877, 2743), ('Straight · 4 panels · 4.88 × 3.05 m', 4877, 3048)],
   geometry={'sightline_mm': 64, 'frame_depth_mm': 49, 'max_panel_w_mm': 1250, 'max_panel_h_mm': 2995, 'glazing': '25 mm insulating (6 + 13 + 6 mm), dark spacer'},
   finish='Acero Grafito', default_size='Corner · 3 + 3 panels · 3.66 + 3.66 × 3.05 m',
   options=['Size / layout (3 variants: two corners, one straight pocket)', 'Glass: Claro / Satinado / Gris', 'Divided lites: Clear view / Steel-line grid', 'Frame finish (6)', 'Flush pull finish (4)'],
   gaps=['frame_depth_mm is per track (49 mm); a 3-panel leg runs three tracks.', 'Glass set is Claro, Satinado and Gris (grey tint, outside the BRAND glass list); no reeded or bronze pane in this model.',
         'Width is per leg for the corner sizes (width_mm = both legs added).', 'Material names carry the product (account-unique names).',
         'Hotspots on moving panels stay at their rest positions while the clip plays (platform behaviour).']),
 'p': dict(slug='patio', name='Umbral Patio', pid='UMBRAL-PATIO', sourceFolder='08-marvin',
   motion='The handle turns 180°, the moving panels lift 6 mm onto their rollers, glide and stack over the fixed panel, then return and settle; 10 s clip Panels_LiftSlide_<size>, and a handle-only lift clip.',
   sizes=[('3 panels · 3.66 × 2.44 m', 3658, 2438), ('4 panels · 4.88 × 2.44 m', 4877, 2438), ('3 panels · 4.57 × 3.05 m', 4572, 3048)],
   geometry={'sightline_mm': 149, 'frame_depth_mm': 271, 'max_panel_w_mm': 1533, 'max_panel_h_mm': 2994, 'glazing': '24 mm insulating (5 + 14 + 5 mm)'},
   finish='Bronce Umbra', default_size='3 panels · 3.66 × 2.44 m',
   options=['Size (3 variants)', 'Glass: Claro / Gris / Bronce / Satinado / Acanalado', 'Divided lites: Clear view / Grid / Perimeter', 'Handle: Fixed handle with key / Flush lever', 'Inside: timber (4)', 'Outside: metal (5)', 'Handle finish (4)', 'Threshold track (4)'],
   gaps=['sightline_mm = two 102 mm meeting stiles less their 55 mm overlap; frame_depth_mm is the 3-panel jamb (4-panel: 368 mm).',
         'Interior timber is a retint of the source oak/mahogany textures, not a new grain scan.', 'Material names carry the product (account-unique names).']),
}
for k, m in META.items():
    p = pay[k]; nodes = [n for n in spec[k]['nodes']]
    fins = []
    for n in nodes:
        for f in (n.get('finishes') or []):
            if f['finish'] not in fins: fins.append(f['finish'])
    glass = next(x for x in p['put']['modularizations'] if x['label'] == 'Glass')
    hs, seen = [], set()
    for h in p['put']['hotspots']:
        if h['title'] in seen: continue
        seen.add(h['title']); hs.append({'title': h['title'], 'text': h['description']})
    pid = prev.get(k)
    rep = {'slug': m['slug'], 'name': m['name'], 'pid': m['pid'], 'productId': ids[k], 'previewId': pid,
           'live': f'https://admin.thridify.com/p/{pid}' if pid else None, 'admin': f'https://admin.thridify.com/products/{ids[k]}',
           'sourceFolder': m['sourceFolder'], 'motion': m['motion'],
           'sizes': [{'label': l, 'width_mm': w, 'height_mm': h} for l, w, h in m['sizes']], 'defaultSize': m['default_size'],
           'finishes': fins, 'finishNodes': {n['label']: [f['finish'] for f in (n.get('finishes') or next(x for x in nodes if x['nodeId'] == n.get('same'))['finishes'])] for n in nodes},
           'glass': [x['name'] for x in glass['meshes']], 'options': m['options'], 'hotspots': hs, 'geometry': m['geometry'],
           'stills': {'hero': f"/images/{m['slug']}/hero.webp", 'front': f"/images/{m['slug']}/front.webp", 'detail': f"/images/{m['slug']}/detail.webp", 'finish': m['finish']},
           'description': p['put']['description'], 'gaps': m['gaps'] + ([] if pid else ['Not published yet: optimiser still running at hand-off.'])}
    json.dump(rep, open(OUT + m['slug'] + '.json', 'w'), indent=2, ensure_ascii=False)
    print('wrote', m['slug'], pid)
