"""Umbral stills (hero / front / detail) for Alba, Batiente, Tamiz from the source .blend files.
Blender 4.3: nice -n 5 Blender -b --factory-startup -P render_stills_abt.py -- <slug> [hero,front,detail] [preview]
Late-afternoon light: one low 3800 K sun from outside (+Y) raking through the glass onto the interior floor, cool sky fill."""
import bpy, sys, os, math
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:]
SLUG = argv[0]; SHOTS = argv[1].split(",") if len(argv) > 1 else ["hero", "front", "detail"]; PREVIEW = len(argv) > 2 and argv[2] == "preview"
DW = os.path.expanduser("~/Documents/Claude-Workspace/thridify-demos-2026-11/doorswindows")
TEX = f"{DW}/umbral-abt/{SLUG}/tex/"
OUT = os.path.expanduser(f"~/Documents/Claude-Workspace/tyashin-customer-sites/umbral-next/public/images/{SLUG}/")
if PREVIEW: OUT = f"{DW}/umbral-abt/{SLUG}/preview_"
os.makedirs(os.path.dirname(OUT), exist_ok=True)
P = {
 "alba": dict(blend="w2-10-leawod/LEAWOD-MXN120-R7.blend", size="_S1300x1600", sizes=["_S1100x1400", "_S1500x1800"],
   hide_names=["_Double_", "Glass_Frost", "Glass_Grey", "Glass_Triple", "GFrost", "GGrey", "GTriple"],
   base={"Interior_Wood": "interior_wood-roble-ahumado", "Exterior_Aluminium": "exterior_aluminium-acero-grafito", "Hardware_Handle": "hardware_handle-bronce-umbra"},
   swap={}, clip="Sash_Turn", hero_frame=30, hw="Hardware_Handle", unit="Frame_Alu_Single_S1300x1600", finish="Acero Grafito outside, Roble Ahumado inside, Bronce Umbra handle"),
 "batiente": dict(blend="05-hopes/HOPES-JT175-CASEMENT.blend", size="_S60x80", sizes=["_S48x72", "_S72x96"],
   hide_names=["Bead_Sloped", "Glass_Reeded", "Glass_SatinEtch", "Grille_None", "Grille_SDL_2x3", "Grille_TDL_2x4", "Grille_TDL_3x5"],
   base={"Frame_Steel": "frame_steel-bronce-umbra", "Hardware_Metal": "hardware_metal-laton-cepillado"},
   swap={"Frame_Steel": {"paint_normal": "frame_steel-normal-bronze_normal_2048", "paint_mr": "frame_steel-mr-bronze_mr_v2_2048"}}, clip="Sash_Open", hero_frame=62, hw="Hardware_Metal",
   unit="Frame_Outer_S60x80", finish="Bronce Umbra, Latón Cepillado handles"),
 "tamiz": dict(blend="14-crittall/CW-W20-SCREEN.blend", size="_S30", sizes=["_S24", "_S36"],
   hide_names=["Bars_Deco", "Bars_None", "Glass_Reeded", "Glass_Satin", "Glass_Solar", "Handle_Europrofile", "Handle_Soho"],
   base={"Frame_Powdercoat": "frame_powdercoat-acero-grafito", "Handle_Metal": "handle_metal-laton-cepillado"},
   swap={}, clip="Doors_Open", hero_frame=56, hw="Handle_Metal", unit="Frame_Steel_S30", finish="Acero Grafito, Latón Cepillado levers"),
}[SLUG]
bpy.ops.wm.open_mainfile(filepath=f"{DW}/{P['blend']}")
sc = bpy.context.scene
def chain(o):
    s = []
    while o: s.append(o.name); o = o.parent
    return "/".join(s)
for o in bpy.data.objects:
    c = chain(o)
    if any(t in c for t in P["sizes"]) or any(h in c for h in P["hide_names"]):
        o.hide_render = True; o.hide_viewport = True
# Umbral finishes on the materials
def img(path):
    return bpy.data.images.load(path, check_existing=True)
for mname, f in P["base"].items():
    m = bpy.data.materials[mname]; nt = m.node_tree; b = [n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'][0]
    s = b.inputs["Base Color"]
    if s.is_linked and s.links[0].from_node.type == 'TEX_IMAGE': s.links[0].from_node.image = img(f"{TEX}umbral-{SLUG}-{f}.jpg")
    else:
        t = nt.nodes.new("ShaderNodeTexImage"); t.image = img(f"{TEX}umbral-{SLUG}-{f}.jpg")
        # reuse the UV mapping of an existing image node (tiling), if any
        ex = [n for n in nt.nodes if n.type == 'TEX_IMAGE' and n is not t and n.inputs["Vector"].is_linked]
        if ex: nt.links.new(ex[0].inputs["Vector"].links[0].from_socket, t.inputs["Vector"])
        nt.links.new(t.outputs["Color"], s)
    for old, new in P["swap"].get(mname, {}).items():
        for n in nt.nodes:
            if n.type == 'TEX_IMAGE' and n.image and old in n.image.name:
                cs = n.image.colorspace_settings.name; n.image = img(f"{TEX}umbral-{SLUG}-{new}.jpg"); n.image.colorspace_settings.name = cs
# context: widen the wall and add an interior floor so the frame reads as architecture
def bounds(objs):
    pts = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
    return Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts))), Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
vis = [o for o in bpy.data.objects if o.type == 'MESH' and not o.hide_render]
walls = [o for o in vis if "Wall" in o.name]
plaster = bpy.data.materials.get("Fixed_Context_Plaster")
def box(name, x0, x1, y0, y1, z0, z1, mat):
    bpy.ops.mesh.primitive_cube_add(size=1, location=((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))
    o = bpy.context.active_object; o.name = name; o.scale = (x1 - x0, y1 - y0, z1 - z0); o.data.materials.append(mat); return o
wl, wh = bounds(walls)
H = max(3.2, wh.z + 0.4)
box("X_WallL", wl.x - 12, wl.x, wl.y, wh.y, 0, H, plaster); box("X_WallR", wh.x, wh.x + 12, wl.y, wh.y, 0, H, plaster)
box("X_WallT", wl.x, wh.x, wl.y, wh.y, wh.z, H, plaster)
if True:
    fz = -0.031 if SLUG == "tamiz" else 0.0
    fm = bpy.data.materials.new("X_Floor"); fm.use_nodes = True; bf = fm.node_tree.nodes["Principled BSDF"]
    bf.inputs["Base Color"].default_value = (0.70, 0.64, 0.55, 1); bf.inputs["Roughness"].default_value = 0.55
    if SLUG == "tamiz": fm = bpy.data.materials["Fixed_Context_Floor"]
    box("X_Floor", -14, 14, -14, wl.y + 0.001, fz - 0.02, fz, fm)
    box("X_FloorOut", -14, 14, wh.y - 0.001, 14, fz - 0.02, fz, fm)
# light
w = sc.world or bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True
bg = w.node_tree.nodes.get("Background"); bg.inputs["Color"].default_value = (0.58, 0.66, 0.80, 1); bg.inputs["Strength"].default_value = 0.30
for o in [o for o in bpy.data.objects if o.type == 'LIGHT']: bpy.data.objects.remove(o)
sun = bpy.data.objects.new("Sun", bpy.data.lights.new("Sun", 'SUN')); sc.collection.objects.link(sun)
sun.data.energy = 6.5; sun.data.color = (1.0, 0.70, 0.45); sun.data.angle = math.radians(0.8)
el, az = math.radians(33), math.radians(26)       # low sun, raking from outside (+Y) toward the room (-Y)
d = Vector((math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), -math.sin(el)))
sun.rotation_euler = (-d).to_track_quat('Z', 'Y').to_euler()
# render settings
sc.render.engine = 'CYCLES'; cy = sc.cycles
try:
    prefs = bpy.context.preferences.addons["cycles"].preferences; prefs.compute_device_type = 'METAL'; prefs.get_devices()
    for dv in prefs.devices: dv.use = True
    cy.device = 'GPU'
except Exception as e: print("GPU fallback", e)
cy.samples = 24 if PREVIEW else 112; cy.use_denoising = True; cy.max_bounces = 8; cy.transparent_max_bounces = 16
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'; sc.view_settings.exposure = 0.55
sc.render.image_settings.file_format = 'WEBP'; sc.render.image_settings.quality = 82; sc.render.image_settings.color_mode = 'RGB'
# pose
sc.frame_set(0); REST = {o.name: o.matrix_basis.copy() for o in bpy.data.objects}
def pose(frame):
    for o in bpy.data.objects:
        ad = o.animation_data
        if not ad: continue
        act = None
        for tr in ad.nla_tracks:
            for st in tr.strips:
                if st.action and st.action.name.startswith(P["clip"]): act = st.action
            tr.mute = True
        ad.action = act if frame else None
    sc.frame_set(frame or 0)
    if not frame:
        for o in bpy.data.objects:
            if o.animation_data: o.animation_data.action = None
            if o.name in REST: o.matrix_basis = REST[o.name]
unit = bpy.data.objects[P["unit"]]; ul, uh = bounds([unit]); C = (ul + uh) / 2; W, Hh = uh.x - ul.x, uh.z - ul.z
cam = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam")); sc.collection.objects.link(cam); sc.camera = cam
def look(pos, tgt, lens):
    cam.location = pos; cam.data.lens = lens; cam.rotation_euler = (Vector(tgt) - Vector(pos)).to_track_quat('-Z', 'Y').to_euler()
def shot(name, rx, ry, frame):
    sc.render.resolution_x, sc.render.resolution_y = (rx // 4, ry // 4) if PREVIEW else (rx, ry); sc.render.resolution_percentage = 100
    pose(frame); sc.render.filepath = OUT + name + ".webp"; bpy.ops.render.render(write_still=True); print("WROTE", sc.render.filepath)
k = max(W, Hh) * (0.78 if SLUG == "tamiz" else 1.0)
if "hero" in SHOTS:
    tgt = Vector((C.x + 0.22 * k, C.y - 0.55 * k, C.z - (0.26 if SLUG == "tamiz" else 0.38) * Hh))
    look(Vector((C.x - 0.62 * k, C.y - 2.30 * k, C.z + 0.02 * Hh)), tgt, 24); shot("hero", 2400, 1500, P["hero_frame"])
if "front" in SHOTS:
    tgt = Vector((C.x, C.y, C.z - 0.05 * Hh)); dist = max(1.18 * Hh / (2 * math.tan(math.atan(18 / 50))), 1.12 * W / (2 * math.tan(math.atan(14.4 / 50)))) + 0.2
    look(tgt + Vector((0, -dist, 0)), tgt, 50); shot("front", 1600, 2000, 0)
if "detail" in SHOTS:
    hw = [o for o in bpy.data.objects if o.type == 'MESH' and not o.hide_render and any(s.material and s.material.name == P["hw"] for s in o.material_slots)]
    hl, hh = bounds(hw[:1]); hc = (hl + hh) / 2
    look(hc + Vector((0.20, -0.34, 0.09)), hc + Vector((-0.02, 0, -0.03)), 55); shot("detail", 1600, 1600, 0)
print("FINISH", P["finish"])
