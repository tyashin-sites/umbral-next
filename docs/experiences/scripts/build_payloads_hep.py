"""Builds the Umbral PUT/variant payloads from the source product dumps (placeholders FIN:/ICON:/UPL: resolved in the tab)."""
import json, copy, sys
SRC = sys.argv[1]  # folder with h.json e.json p.json
spec = json.load(open('finish_spec.json'))
ROOT = {'h': ('SkyFrame1', 'Horizonte'), 'e': ('Fleetwood_3070T', 'Esquina'), 'p': ('Marvin_ULSD', 'Patio')}
def rp(k, s):
    a, b = ROOT[k]; return s.replace(a + '/', b + '/', 1) if s.startswith(a + '/') else (b if s == a else s)

DESC = {
 'h': "A frameless sliding glass wall. The frame sits in the floor, the ceiling and the walls, so the only vertical line is the interlock where two panes meet. Up to four panes, 8 metres wide.",
 'e': "A corner with no post. Both legs slide into pockets in the walls, and the corner of the room opens to the terrace. Thermally broken aluminium, 25 mm insulating glass, a floor that runs straight through.",
 'p': "A lift-and-slide door, timber inside and aluminium outside. A half turn of the handle lifts each panel 6 mm onto its rollers; it glides, stacks and settles back onto its seals.",
}
SIZES = {
 'h': {'Sideways · 2 elements · 4.4 m': '2 panels · 4.4 × 2.8 m', 'Sideways · 2 elements · 6.0 m': '2 panels · 6.0 × 2.8 m',
       'Central · 4 elements · 6.0 m': '4 panels, centre opening · 6.0 × 2.8 m', 'Central · 4 elements · 8.0 m': '4 panels, centre opening · 8.0 × 2.8 m'},
 'e': {"90° corner · 3 + 3 panels · 12' + 12' × 10'": 'Corner · 3 + 3 panels · 3.66 + 3.66 × 3.05 m',
       "90° corner · 2 + 2 panels · 8' + 8' × 9'": 'Corner · 2 + 2 panels · 2.44 + 2.44 × 2.74 m',
       "Straight pocket · 4 panels · 16' × 10'": 'Straight · 4 panels · 4.88 × 3.05 m'},
 'p': {'3 panels OXX · 12\'0" × 8\'0"': '3 panels · 3.66 × 2.44 m', '4 panels OXXX · 16\'0" × 8\'0"': '4 panels · 4.88 × 2.44 m',
       '3 panels OXX · 15\'0" × 10\'0"': '3 panels · 4.57 × 3.05 m'},
}
# modularizations: (label, [(meshId-suffix-after-root, label)], thumbnails kept from source by meshId)
MODS = {
 'h': [('Floor track', [('Track/Track_Plain', 'Flush: the floor runs over it'), ('Track/Track_Original', 'Visible track')]),
       ('Glass', [('Glass/Glass_ExtraClear', 'Claro'), ('Glass/Glass_Satin', 'Satinado'), ('Glass/Glass_Grey', 'Gris')])],
 'e': [('Glass', [('Glass_Clear', 'Claro'), ('Glass_Satin', 'Satinado'), ('Glass_Gray', 'Gris')]),
       ('Divided lites', [('SDL_None', 'Clear view'), ('SDL_SteelLook', 'Steel-line grid')])],
 'p': [('Glass', [('Glass_Clear', 'Claro'), ('Glass_GrayTint', 'Gris'), ('Glass_BronzeTint', 'Bronce'), ('Glass_Frost', 'Satinado'), ('Glass_NarrowReed', 'Acanalado')]),
       ('Divided lites', [('Grilles_None', 'Clear view'), ('Grilles_Rectangular', 'Grid · 22 mm bars'), ('Grilles_Prairie', 'Perimeter · 22 mm bars')]),
       ('Handle', [('Handle_Fixed', 'Fixed handle with key'), ('Handle_Flush', 'Flush lever')])],
}
# hotspot copy keyed by source title (+ layout tweaks)
HOT = {
 'h': {'Glides open on hidden rollers': ('slide', 'Slides on concealed rollers', 'Tap to open. The moving pane runs on the outer track and parks behind the fixed pane.'),
       'Slim interlock': ('interlock', 'One slim interlock', 'Where two panes meet, a 22 mm interlock is the only vertical line in the opening.'),
       'Frame hidden in the ceiling': ('head', 'Frame in the ceiling', 'The head profile sits in a 125 mm pocket above the ceiling line. The glass runs to the soffit.'),
       'Flush floor track': ('sill', 'Flush floor track', 'The rails sit 125 mm into the floor. Leave the track visible, or let the floor run over it and keep only two 20 mm slots.'),
       '12 mm single glazing': ('glass', '12 mm single glazing', 'One 12 mm pane, for rooms without thermal demands: pool houses, loggias, courtyards. Panes here reach 3.0 × 2.8 m.')},
 'e': {'Pocket the corner': ('pocket', 'Open the corner', 'Both legs slide into their wall pockets. No post, no jamb, only air where the corner was.'),
       'Pocket the panels': ('pocket', 'Open the wall', 'Four panels stack into one wall pocket and leave the full 4.88 m clear.'),
       'Flush pull, one-hand glide': ('pull', 'Flush pull', 'A recessed pull sits in the lead stile, so the panel passes fully into the pocket. Pull it and it collects the next panel at the interlock.'),
       'No-post 90° corner': ('corner', 'No post at 90°', 'Two panels meet at the corner with no post or jamb. When both legs pocket, the corner is gone.'),
       'Archetype lock stile': ('corner', 'Lock stile', 'The lead panel closes into the lock jamb on an 83 mm stile, with multi-point locking.'),
       '1" insulated glass': ('glass', '25 mm insulating glass', 'Two 6 mm panes and a dark spacer, glazed into thermally broken frames. Claro, Satinado or Gris under Glass.'),
       'Flush floor, stainless track': ('sill', 'The floor runs through', 'The sill pan sits in the slab, so the floor is level inside and out. Only the stainless track inserts show.'),
       'Thermally broken aluminum': ('frame', 'Thermally broken frame', 'Every profile carries a polyamide thermal break. Where two panels meet, the interlock reads 64 mm.')},
 'p': {'Turn the handle: the panel lifts': ('handle', 'Turn the handle', 'A 180° turn lifts the panel 6 mm onto its rollers. Turn it back and it settles onto the seals and locks.'),
       'Lift, roll and stack': ('liftslide', 'Lift, slide, stack', 'The moving panels lift, glide and stack over the fixed one. Each runs on its own track, 97.5 mm apart.'),
       'Wood inside': ('wood', 'Timber inside', 'The inside face is timber: Roble Ahumado or Nogal, or painted Piedra or Negro Carbón.'),
       'Aluminium clad outside': ('exterior', 'Aluminium outside', 'The outside face is 22 mm of extruded aluminium that takes the weather. Its finish is chosen separately from the timber.'),
       'Insulating glass': ('glass', '24 mm insulating glass', 'Two 5 mm panes around a 14 mm cavity. Claro, Gris, Bronce, Satinado or Acanalado under Glass.'),
       'Near-level threshold': ('sill', 'Near-level threshold', 'The sill sits in a slot in the floor, so only 5 mm of track shows above it.')},
}
SLUG = {'h': 'horizonte', 'e': 'esquina', 'p': 'patio'}
out = {}
for k in 'hep':
    x = json.load(open(f'{SRC}/{k}.json')); d = x['d']; slug = SLUG[k]; a, b = ROOT[k]
    srcmods = {m['meshId']: m for mod in d['modularizations'] for m in mod['meshes']}
    mods = []
    for i, (label, items) in enumerate(MODS[k]):
        ms = []
        for suf, name in items:
            sm = srcmods.get(a + '/' + suf); assert sm, (k, suf)
            e = {'meshId': b + '/' + suf, 'name': name}
            if sm.get('thumbnail'): e['thumbnail'] = sm['thumbnail']
            ms.append(e)
        mods.append({'label': label, 'type': 'single_select', 'isPublished': True, 'order': i, 'meshes': ms})
    hots = []
    for h in d['hotspots']:
        icon, title, text = HOT[k][h['title']]
        if k == 'p' and 'OXXX' in h['meshId'] and icon == 'liftslide':
            text = 'Three moving panels lift, glide and stack over the fixed one. Each runs on its own track, 97.5 mm apart.'
        nh = {kk: vv for kk, vv in h.items() if kk != 'surface'}
        nh.update(title=title, description=text, meshId=rp(k, h['meshId']), icon={'src': f'ICON:{slug}_{icon}.svg', 'color': '#16140FFF'})
        if k == 'h':
            nh['meshId'] = nh['meshId'].replace('Glass_Clear/Clear_', 'Glass_ExtraClear/ExtraClear_').replace('Track_Original/TrackO_', 'Track_Plain/TrackP_')
        hots.append(nh)
    nodes = []
    for n in spec[k]['nodes']:
        fins = n.get('finishes') or next(m for m in spec[k]['nodes'] if m['nodeId'] == n['same'])['finishes']
        nodes.append({'nodeId': n['nodeId'], 'name': n['label'], 'selectedMaterials': ['FINM:' + f['key'] for f in fins],
                      'selectedDesigns': ['FIND:' + f['key'] for f in fins], 'isLocked': False})
    vnodes = [{'nodeId': n['nodeId'], 'materialId': n['selectedMaterials'][0], 'designId': n['selectedDesigns'][0]} for n in nodes]
    defid = d['defaultVariant'] if isinstance(d['defaultVariant'], str) else d['defaultVariant']['variantId']
    variants = []
    for v in x['v']:
        hm = [rp(k, s) for s in v['hiddenMeshes']]
        if k == 'h':
            hm = [{'Horizonte/Track/Track_Plain': 'Horizonte/Track/Track_Original', 'Horizonte/Glass/Glass_ExtraClear': 'Horizonte/Glass/Glass_Clear'}.get(s, s) for s in hm]
        variants.append({'variantName': SIZES[k][v['variantName']], 'hiddenMeshes': hm, 'hiddenMaterials': v.get('hiddenMaterials') or [],
                         'cameraOrbit': v['cameraOrbit'], 'cameraTarget': v['cameraTarget'], 'nodes': vnodes,
                         'isPublished': True, 'isInStock': True, 'isDefault': v['variantId'] == defid})
    ms = {kk: vv for kk, vv in d['modelSettings'].items()}
    ms.update(background2DImageDesktop=f'UPL:{slug}-desktop.jpg', background2DImageMobile=f'UPL:{slug}-mobile.jpg', isSkybox3D=False,
              enableZoomAndSpinOnLoad=False, autoplay=False, exposure=ms.get('exposure', 1))
    cs = dict(d['customizerSettings']); cs['hidePriceConfigurator'] = True
    out[k] = {'put': {'description': DESC[k], 'nodes': nodes, 'modularizations': mods, 'hotspots': hots, 'modelSettings': ms,
                      'customizerSettings': cs, 'show3DCues': d['show3DCues']}, 'variants': variants}
    assert all('Fleetwood' not in s and 'Marvin' not in s and 'SkyFrame' not in s for v in variants for s in v['hiddenMeshes'])
txt = json.dumps(out, ensure_ascii=False)
import re
for bad in ['Sky-Frame', 'Fleetwood', 'Marvin', 'Kynar', 'Archetype', 'ULSD', '3070']:
    hits = [m.start() for m in re.finditer(bad, txt)]
    print(bad, len(hits), [txt[max(0, i-60):i+20] for i in hits[:3]])
json.dump(out, open('payloads.json', 'w'), ensure_ascii=False)
print({k: (len(v['put']['hotspots']), len(v['variants']), [m['label'] for m in v['put']['modularizations']]) for k, v in out.items()})
