"""Umbral stills (hero / front / detail) for Horizonte, Esquina and Patio, rendered from the source .blend files.
nice -n 5 /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup -P render_stills_hep.py -- <slug> [hero,front,detail] [--test]
Nothing in the model is scaled or moved: only visibility (same hidden-mesh list as the default configurator variant),
the default Umbral finish colours, lights, world and cameras are set here."""
import bpy, sys, os, json, math
from mathutils import Vector
argv = sys.argv[sys.argv.index('--') + 1:]
SLUG = argv[0]; SHOTS = (argv[1] if len(argv) > 1 and not argv[1].startswith('--') else 'hero,front,detail').split(','); TEST = '--test' in argv
D = os.path.expanduser('~/Documents/Claude-Workspace/thridify-demos-2026-11/doorswindows/')
REPO = os.path.expanduser('~/Documents/Claude-Workspace/tyashin-customer-sites/umbral-next/')
OUT = REPO + f'public/images/{SLUG}/'; os.makedirs(OUT, exist_ok=True)
FIN = D + 'umbral-hep/finishes/'
HEX = {'Bronce Umbra': '#4A3A2A', 'Latón Cepillado': '#B08D57', 'Acero Grafito': '#3A3B3C', 'Negro Carbón': '#1A1A1A',
       'Anodizado Natural': '#A9ABAD', 'Piedra': '#E7E2D8', 'Roble Ahumado': '#5B4332', 'Nogal': '#4A3426'}
CFG = {
 'horizonte': dict(blend='09-skyframe/SF1.blend', root=('SkyFrame1', 'Horizonte'), unit='W60', clip='Panels_Slide', open_frame=90,
                   finish={'Frame_Anodised': ('Bronce Umbra', None), 'Handle_Metal': ('Bronce Umbra', None)}, label='Bronce Umbra', ext=[('Fixed_Context_Floor', -30, 30, -30, -0.07, -0.004, 0.6), ('Fixed_Context_Terrace', -30, 30, 0.07, 30, -0.004, 0.6)]),
 'esquina':   dict(blend='w2-12-fleetwood/FLEETWOOD-3070T.blend', root=('Fleetwood_3070T', 'Esquina'), unit='C33_120', clip='Panels_Pocket_C33_120', open_frame=70,
                   finish={'Frame_Aluminum': ('Acero Grafito', 'e_frame_grafito'), 'Hardware_Steel': ('Anodizado Natural', 'e_hw_natural')}, label='Acero Grafito', ext=[('Fixed_Context_Floor', -30, 30, -30, 30, -0.006, 1.5)]),
 'patio':     dict(blend='08-marvin/MARVIN-ULSD.blend', root=('Marvin_ULSD', 'Patio'), unit='OXX_12080', clip='Panels_LiftSlide_OXX_12080', open_frame=88,
                   finish={'Interior_Wood': ('Roble Ahumado', 'p_wood_roble'), 'Exterior_Clad': ('Bronce Umbra', 'p_clad_bronce'),
                           'Hardware_Metal': ('Bronce Umbra', 'p_hw_bronce'), 'Sill_Anodized': ('Bronce Umbra', 'p_sill_bronce')}, label='Bronce Umbra exterior, Roble Ahumado interior', ext=[('#D8D2C6', -30, 30, -30, 30, -0.006, 0.6)], wall_ext=True),
}[SLUG]
bpy.ops.wm.open_mainfile(filepath=D + CFG['blend'])
sc = bpy.context.scene
def srgb2lin(c): return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def hexlin(h): return tuple(srgb2lin(int(h[i:i + 2], 16) / 255) for i in (1, 3, 5)) + (1,)
# ---------- visibility: the default variant's hidden meshes
pay = json.load(open(D + 'umbral-hep/payloads.json'))[{'horizonte': 'h', 'esquina': 'e', 'patio': 'p'}[SLUG]]
var = next(v for v in pay['variants'] if v['isDefault'])
old, new = CFG['root']
hidden = [h.replace(new, old, 1) for h in var['hiddenMeshes']]
def path(o):
    p = []
    while o: p.append(o.name); o = o.parent
    return '/'.join(reversed(p))
for o in bpy.data.objects:
    pth = path(o)
    hide = any(pth == h or pth.startswith(h + '/') for h in hidden)
    o.hide_render = hide; o.hide_viewport = hide
# the Horizonte default glass is ExtraClear (Claro): Glass_Clear is outside the option set and always hidden
# ---------- animation: only the chosen clip plays
for o in bpy.data.objects:
    ad = o.animation_data
    if not ad: continue
    ad.action = None
    for t in ad.nla_tracks: t.mute = not t.name.startswith(CFG['clip'])
# ---------- finishes (helpers defined earlier)
def _unused(c): return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def hexlin(h): return tuple(srgb2lin(int(h[i:i + 2], 16) / 255) for i in (1, 3, 5)) + (1,)
for mname, (fin, tex) in CFG['finish'].items():
    m = bpy.data.materials.get(mname)
    if not m: print('MISSING MAT', mname); continue
    p = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'); inp = p.inputs['Base Color']
    if inp.is_linked and inp.links[0].from_node.type == 'TEX_IMAGE' and tex:
        node = inp.links[0].from_node; img = bpy.data.images.load(FIN + tex + '.jpg'); img.colorspace_settings.name = 'sRGB'; node.image = img
    else:
        for l in list(inp.links): m.node_tree.links.remove(l)
        inp.default_value = hexlin(HEX[fin])
# ---------- stills-only context: extend the model's own floors so the frame never shows a void (the model is untouched)
import bmesh
def ext_plane(mat_name, x0, x1, y0, y1, z, tile):
    if mat_name.startswith('#'):
        m = bpy.data.materials.new('UmbralStillFlat'); m.use_nodes = True
        bp = m.node_tree.nodes['Principled BSDF']; bp.inputs['Base Color'].default_value = hexlin(mat_name); bp.inputs['Roughness'].default_value = 0.62
        m0 = m
    m0 = bpy.data.materials.get(mat_name) if not mat_name.startswith('#') else m0
    if not m0: print('no ctx mat', mat_name); return
    m = m0.copy(); white = bpy.data.images.new('white1', 4, 4); white.pixels.foreach_set([1.0] * 64)
    for n in m.node_tree.nodes:
        if n.type == 'TEX_IMAGE' and n.image and 'AO' in n.image.name: n.image = white
    me = bpy.data.meshes.new('UmbralStillFloor'); bm = bmesh.new()
    vs = [bm.verts.new((x, y, z)) for x, y in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))]; f = bm.faces.new(vs)
    uvn = None
    for n in m.node_tree.nodes:
        if n.type == 'UVMAP' and n.uv_map: uvn = n.uv_map
    uv = bm.loops.layers.uv.new(uvn or 'UVMap')
    for l in f.loops: l[uv].uv = (l.vert.co.x / tile, l.vert.co.y / tile)
    bm.to_mesh(me); me.materials.append(m); o = bpy.data.objects.new('UmbralStillFloor', me); sc.collection.objects.link(o)
for spec in CFG.get('ext', []): ext_plane(*spec)
if CFG.get('wall_ext'):
    ws = [o for o in bpy.data.objects if o.type == 'MESH' and not o.hide_render and any(mm and mm.name == 'Fixed_Context_Wall' for mm in o.data.materials)]
    lo = Vector((1e9,) * 3); hi = Vector((-1e9,) * 3)
    for o in ws:
        for c in o.bound_box:
            wv = o.matrix_world @ Vector(c); lo = Vector(map(min, lo, wv)); hi = Vector(map(max, hi, wv))
    print('WALL', tuple(round(x, 3) for x in lo), tuple(round(x, 3) for x in hi))
    pm = bpy.data.materials.new('UmbralStillPlaster'); pm.use_nodes = True
    pb = pm.node_tree.nodes['Principled BSDF']; pb.inputs['Base Color'].default_value = hexlin('#E4DFD6'); pb.inputs['Roughness'].default_value = 0.8
    for x0, x1 in ((-14.0, lo.x + 0.002), (hi.x - 0.002, 14.0)):
        bpy.ops.mesh.primitive_cube_add(size=1, location=((x0 + x1) / 2, (lo.y + hi.y) / 2, hi.z / 2))
        b = bpy.context.active_object; b.scale = (x1 - x0, hi.y - lo.y, hi.z); b.data.materials.append(pm)
# ---------- glass passes light (shadow rays see a tinted transparent surface)
for m in bpy.data.materials:
    if not m.use_nodes: continue
    p = next((n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if not p: continue
    tw = p.inputs.get('Transmission Weight') or p.inputs.get('Transmission')
    if not (tw and tw.default_value > 0.5): continue
    nt = m.node_tree; out = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL')
    src = out.inputs['Surface'].links[0].from_socket
    lp = nt.nodes.new('ShaderNodeLightPath'); tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mx = nt.nodes.new('ShaderNodeMixShader')
    tr.inputs['Color'].default_value = (0.93, 0.95, 0.94, 1)
    nt.links.new(lp.outputs['Is Shadow Ray'], mx.inputs['Fac']); nt.links.new(src, mx.inputs[1]); nt.links.new(tr.outputs['BSDF'], mx.inputs[2])
    nt.links.new(mx.outputs['Shader'], out.inputs['Surface'])
# ---------- bounds of the visible product (no context)
def vis_bounds(filter_fn):
    lo = Vector((1e9,) * 3); hi = Vector((-1e9,) * 3)
    dg = bpy.context.evaluated_depsgraph_get()
    for o in bpy.data.objects:
        if o.type != 'MESH' or o.hide_render or not filter_fn(o): continue
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c); lo = Vector(map(min, lo, w)); hi = Vector(map(max, hi, w))
    return lo, hi
sc.frame_set(0)
lo, hi = vis_bounds(lambda o: 'Context' not in o.name and 'Wall' not in o.name)
ctr = (lo + hi) / 2; size = hi - lo
print('BOUNDS', tuple(round(x, 2) for x in lo), tuple(round(x, 2) for x in hi))
# ---------- world + light: low warm sun from the exterior, cool sky fill
w = bpy.data.worlds.new('UmbralSky'); sc.world = w; w.use_nodes = True
bg = w.node_tree.nodes['Background']; bg.inputs['Color'].default_value = (0.42, 0.52, 0.68, 1); bg.inputs['Strength'].default_value = 0.55
def k2rgb(k):  # rough blackbody → linear RGB for 3800 K
    return (1.0, 0.70, 0.45)
sun = bpy.data.lights.new('Sun', 'SUN'); sun.energy = 4.2; sun.color = k2rgb(3800); sun.angle = math.radians(0.6)
so = bpy.data.objects.new('Sun', sun); sc.collection.objects.link(so); so.visible_glossy = False; so.visible_transmission = False
# exterior side: +Y for Horizonte and Patio (interior is -Y); the generators put the interior on -Y for all three
EXT = Vector((0, 1, 0))
def aim(obj, target):
    d = (target - obj.location); obj.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
# ---------- render settings
sc.render.engine = 'CYCLES'
try:
    prefs = bpy.context.preferences.addons['cycles'].preferences; prefs.compute_device_type = 'METAL'; prefs.get_devices()
    for dv in prefs.devices: dv.use = True
    sc.cycles.device = 'GPU'
except Exception as e: print('GPU fallback', e)
sc.cycles.samples = 16 if TEST else 128; sc.cycles.use_denoising = True
sc.cycles.max_bounces = 8; sc.cycles.transparent_max_bounces = 16; sc.cycles.transmission_bounces = 8
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Base Contrast' if 'AgX - Base Contrast' in [l for l in []] else 'None'
sc.view_settings.exposure = 0.0
sc.render.image_settings.file_format = 'WEBP'; sc.render.image_settings.quality = 82; sc.render.image_settings.color_mode = 'RGB'
cam_d = bpy.data.cameras.new('Cam'); cam = bpy.data.objects.new('Cam', cam_d); sc.collection.objects.link(cam); sc.camera = cam
SH = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stills_cameras.json')))[SLUG]
for shot in SHOTS:
    s = SH[shot]
    sc.frame_set(CFG['open_frame'] if s.get('open') else 0)
    W, H = s['res']; sc.render.resolution_x, sc.render.resolution_y = (W // 4, H // 4) if TEST else (W, H); sc.render.resolution_percentage = 100
    if s.get('focus'):
        objs = [o for o in bpy.data.objects if o.type == 'MESH' and not o.hide_render and any(m and m.name == s['focus'] for m in o.data.materials)]
        objs.sort(key=lambda o: (o.matrix_world @ Vector(o.bound_box[0])).x)
        o = objs[s.get('focus_i', 0)]; c = sum((o.matrix_world @ Vector(b) for b in o.bound_box), Vector()) / 8
        print('FOCUS', o.name, tuple(round(x, 3) for x in c), [x.name for x in objs][:6])
        tgt = c + Vector(s.get('toff', (0, 0, 0))); cam.location = tgt + Vector(s['off']); aim(cam, tgt)
    else:
        cam.location = Vector(s['loc']); aim(cam, Vector(s['target'])); cam_d.lens = s['lens']; cam_d.sensor_width = 36
    az, el = math.radians(s.get("sun_az", 35)), math.radians(s.get('sun_el', 11))
    so.rotation_euler = (0, 0, 0); d = Vector((math.cos(el) * math.sin(az), math.cos(el) * math.cos(az), math.sin(el)))  # direction TO the sun
    so.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler()
    sun.energy = s.get('sun_e', 4.2); bg.inputs['Strength'].default_value = s.get('sky', 0.55)
    sc.view_settings.exposure = s.get('exp', 0.0)
    fn = OUT + shot + ('_test' if TEST else '') + '.webp'
    sc.render.filepath = fn; bpy.ops.render.render(write_still=True); print('WROTE', fn, os.path.getsize(fn))
