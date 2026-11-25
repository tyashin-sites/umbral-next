"""Umbral stills from a source .blend (read-only; never saved). Cycles, late-afternoon sun ~3800 K + cool sky fill.
nice -n 5 Blender -b --factory-startup <file.blend> -P render_stills.py -- <slug> [hero,front,detail] [samples]"""
import bpy, sys, os, json, math
from mathutils import Vector
argv = sys.argv[sys.argv.index('--') + 1:]
SLUG = argv[0]; SHOTS = (argv[1] if len(argv) > 1 else 'hero,front,detail').split(','); SPP = int(argv[2]) if len(argv) > 2 else 96
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, '..', '..', '..', 'public', 'images', SLUG)); os.makedirs(OUT, exist_ok=True)
DW = os.path.expanduser('~/Documents/Claude-Workspace/thridify-demos-2026-11/doorswindows')
CFG = json.load(open(os.path.join(HERE, 'stills_config.json')))[SLUG]
sc = bpy.context.scene

def path(o):
    p = []; x = o
    while x: p.append(x.name); x = x.parent
    return '/'.join(reversed(p))
hidden = CFG['hidden']
def is_hidden(o):
    p = path(o)
    return any(p == h or p.startswith(h + '/') for h in hidden)
for o in bpy.data.objects:
    if is_hidden(o): o.hide_render = True; o.hide_viewport = True

# animation: keep only the hero clip's NLA tracks
def set_pose(frame, clip):
    for o in bpy.data.objects:
        ad = o.animation_data
        if not ad: continue
        ad.action = None
        for t in ad.nla_tracks:
            t.mute = not any(clip and s.name.startswith(clip) for s in t.strips) if clip else True
    sc.frame_set(frame)

# finish overrides for the stills (Umbral default finish)
def tex_base(matname, img):
    m = bpy.data.materials.get(matname)
    if not m: return
    nt = m.node_tree; bsdf = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    t = nt.nodes.new('ShaderNodeTexImage'); t.image = bpy.data.images.load(os.path.join(DW, img))
    uv = nt.nodes.new('ShaderNodeUVMap'); uv.uv_map = CFG.get('uv0', 'UVMap')
    nt.links.new(uv.outputs[0], t.inputs[0]); nt.links.new(t.outputs[0], bsdf.inputs['Base Color'])
for matname, img in CFG.get('finish', {}).items(): tex_base(matname, img)

def visible_meshes(ctx=False):
    return [o for o in bpy.data.objects if o.type == 'MESH' and not o.hide_render and (ctx or not o.name.startswith('Fixed_Context'))]
def bbox(objs):
    lo = Vector((1e9,) * 3); hi = Vector((-1e9,) * 3)
    for o in objs:
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c); lo = Vector(map(min, lo, w)); hi = Vector(map(max, hi, w))
    return lo, hi
set_pose(0, None)
lo, hi = bbox(visible_meshes()); C = (lo + hi) / 2; W = hi.x - lo.x; H = hi.z - lo.z
floor_z = lo.z
# which side is the room: where the context floor reaches further (else config)
side = CFG.get('side')
if side is None:
    fl = [o for o in visible_meshes(True) if 'Floor' in o.name]
    if fl:
        flo, fhi = bbox(fl); side = 1 if (fhi.y - C.y) > (C.y - flo.y) else -1
    else: side = 1
print('BBOX', tuple(lo), tuple(hi), 'side', side)

# context: limestone floor plane + plaster wall around the opening (outside the model's own wall stubs), so the
# sun only reaches the room through the glass and the frame draws its shadow on the floor
lime = bpy.data.materials.new('Umbral_Limestone'); lime.use_nodes = True
b = lime.node_tree.nodes['Principled BSDF']; b.inputs['Base Color'].default_value = (0.74, 0.70, 0.63, 1); b.inputs['Roughness'].default_value = 0.8
plas = bpy.data.materials.new('Umbral_Plaster'); plas.use_nodes = True
b2 = plas.node_tree.nodes['Principled BSDF']; b2.inputs['Base Color'].default_value = (0.82, 0.79, 0.73, 1); b2.inputs['Roughness'].default_value = 0.9
bpy.ops.mesh.primitive_plane_add(size=1, location=(C.x, C.y, floor_z - 0.004)); f = bpy.context.object; f.scale = (30, 30, 1); f.data.materials.append(lime)
walls = [o for o in visible_meshes(True) if 'Wall' in o.name]
olo, ohi = bbox(visible_meshes() + walls)
t = 0.20 if not walls else max(0.05, (ohi.y - olo.y) * 0.5)
gap = 0.002; top = ohi.z + 3.0
for (x0, x1, z0, z1) in ((olo.x - 9.0, olo.x - gap, floor_z, top), (ohi.x + gap, ohi.x + 9.0, floor_z, top), (olo.x - gap, ohi.x + gap, ohi.z + gap, top)):
    if z1 - z0 < 0.01: continue
    bpy.ops.mesh.primitive_cube_add(size=1, location=((x0 + x1) / 2, (olo.y + ohi.y) / 2 if walls else C.y, (z0 + z1) / 2)); w = bpy.context.object
    w.scale = (x1 - x0, t, z1 - z0); w.data.materials.append(plas)

for o in bpy.data.objects:
    if o.type == 'MESH' and any(sl.material and ('Glass' in sl.material.name or 'glass' in sl.material.name) for sl in o.material_slots):
        o.visible_shadow = False
# world: soft cool sky fill
wd = bpy.data.worlds.new('UmbralSky'); sc.world = wd; wd.use_nodes = True; nt = wd.node_tree
bg = nt.nodes['Background']; bg.inputs[0].default_value = (0.62, 0.70, 0.80, 1); bg.inputs[1].default_value = CFG.get('sky', 0.6)
bg2 = nt.nodes.new('ShaderNodeBackground'); bg2.inputs[0].default_value = (0.86, 0.82, 0.76, 1); bg2.inputs[1].default_value = 1.0
lp = nt.nodes.new('ShaderNodeLightPath'); mx = nt.nodes.new('ShaderNodeMixShader'); mx2 = nt.nodes.new('ShaderNodeMixShader')
out = nt.nodes['World Output']
nt.links.new(lp.outputs['Is Glossy Ray'], mx.inputs[0]); nt.links.new(bg.outputs[0], mx.inputs[1]); nt.links.new(bg.outputs[0], mx.inputs[2])
nt.links.new(lp.outputs['Is Camera Ray'], mx2.inputs[0]); nt.links.new(mx.outputs[0], mx2.inputs[1]); nt.links.new(bg2.outputs[0], mx2.inputs[2])
nt.links.new(mx2.outputs[0], out.inputs[0])
# sun: low and warm, travelling from outside (-side) into the room (+side)
def blackbody(k):
    # rough 3800 K
    return (1.0, 0.72, 0.45)
d = Vector((CFG.get('sunx', 0.3), side * 0.80, -CFG.get('sunz', 0.55))).normalized()
bpy.ops.object.light_add(type='SUN'); sun = bpy.context.object; sun.data.energy = CFG.get('sunE', 4.5); sun.data.color = blackbody(3800); sun.data.angle = math.radians(0.8)
sun.rotation_euler = (-d).to_track_quat('Z', 'Y').to_euler()

sc.render.engine = 'CYCLES'
try:
    prefs = bpy.context.preferences.addons['cycles'].preferences; prefs.compute_device_type = 'METAL'; prefs.get_devices()
    for dv in prefs.devices: dv.use = True
    sc.cycles.device = 'GPU'
except Exception as e: print('GPU?', e)
sc.cycles.samples = SPP; sc.cycles.use_denoising = True; sc.cycles.max_bounces = 8; sc.cycles.transmission_bounces = 8
sc.view_settings.view_transform = 'AgX'
try: sc.view_settings.look = 'AgX - Medium High Contrast'
except Exception: pass
sc.render.image_settings.file_format = 'WEBP'; sc.render.image_settings.quality = 82; sc.render.image_settings.color_mode = 'RGB'
sc.render.film_transparent = False

cam_data = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cam_data); sc.collection.objects.link(cam); sc.camera = cam
def look(pos, tgt, lens):
    cam.location = pos; cam.rotation_euler = (Vector(tgt) - Vector(pos)).to_track_quat('-Z', 'Y').to_euler(); cam_data.lens = lens
def shot(name, w, h):
    sc.render.resolution_x, sc.render.resolution_y = w, h; sc.render.resolution_percentage = 100
    sc.render.filepath = os.path.join(OUT, name + '.webp'); bpy.ops.render.render(write_still=True)
    print('WROTE', sc.render.filepath, os.path.getsize(sc.render.filepath))

S = side
if 'hero' in SHOTS:
    set_pose(CFG.get('heroFrame', 0), CFG.get('clip'))
    hx = CFG.get('heroAz', 0.62)
    dist = max(W, H) * CFG.get('heroDist', 2.1)
    pos = Vector((C.x - math.sin(hx) * dist, C.y + S * math.cos(hx) * dist, floor_z + CFG.get('heroEye', 1.9)))
    tgt = Vector((C.x + W * 0.05, C.y + S * CFG.get('heroTgtY', 0.6), floor_z + H * 0.36))
    look(pos, tgt, CFG.get('heroLens', 35)); shot('hero', 2400, 1500)
if 'front' in SHOTS:
    set_pose(0, CFG.get('clip'))
    cam_data.sensor_fit = 'VERTICAL'; cam_data.sensor_height = 24
    fill = max(H * 1.18, W * 1.18 * 2000 / 1600)
    dist = (fill / 2) / math.tan(math.atan(12 / 70))
    look(Vector((C.x, C.y + S * dist, floor_z + H * 0.5)), Vector((C.x, C.y, floor_z + H * 0.5)), 70)
    shot('front', 1600, 2000); cam_data.sensor_fit = 'AUTO'; cam_data.sensor_width = 36
if 'detail' in SHOTS:
    set_pose(0, CFG.get('clip'))
    o = next(o for o in visible_meshes() if any(k in path(o) for k in CFG['detailMesh']))
    dl, dh = bbox([o]); dc = (dl + dh) / 2
    off = Vector(CFG.get('detailOff', (0.35, 0.55, 0.12))); off.y *= S
    look(dc + off, dc + Vector(CFG.get('detailTgt', (0, 0, 0))), CFG.get('detailLens', 50)); shot('detail', 1600, 1600)
print('DONE', SLUG)
