"""Umbral finish textures for Alba / Batiente / Tamiz, remapped from the source builds' own procedural maps.
Each base colour keeps the source's micro-variation but is shifted to the Umbral swatch mean (BRAND.md).
Run: Blender -b --factory-startup -P finishes_abt.py"""
import bpy, numpy as np, json, os, shutil
DW = os.path.expanduser("~/Documents/Claude-Workspace/thridify-demos-2026-11/doorswindows")
WK = DW + "/umbral-abt"
HEX = {"Bronce Umbra": "#4A3A2A", "Latón Cepillado": "#B08D57", "Acero Grafito": "#3A3B3C", "Negro Carbón": "#1A1A1A",
       "Anodizado Natural": "#A9ABAD", "Piedra": "#E7E2D8", "Roble Ahumado": "#5B4332", "Nogal": "#4A3426"}
SLUG = {"Bronce Umbra": "bronce-umbra", "Latón Cepillado": "laton-cepillado", "Acero Grafito": "acero-grafito", "Negro Carbón": "negro-carbon",
        "Anodizado Natural": "anodizado-natural", "Piedra": "piedra", "Roble Ahumado": "roble-ahumado", "Nogal": "nogal"}
# node -> label, [(finish, source base, [normal, mr], metalize_mr_roughness or None, size)]
A, H, C = DW + "/w2-10-leawod/textures/finishes/", DW + "/05-hopes/textures/finishes/", DW + "/14-crittall/textures/finishes/"
SPEC = {
 "alba": [
  ("Interior_Wood", "Interior · wood", [
    ("Roble Ahumado", A + "wood_American_Oak.jpg", [A + "wood_normal_2048.jpg", A + "wood_mr_2048.jpg"], None, 2048),
    ("Nogal", A + "wood_Burmese_Teak.jpg", [A + "wood_normal_2048.jpg", A + "wood_mr_2048.jpg"], None, 2048),
    ("Piedra", A + "powder_9016.jpg", [A + "wood_normal_2048.jpg", A + "wood_mr_2048.jpg"], None, 1024),
    ("Negro Carbón", A + "powder_9005.jpg", [A + "wood_normal_2048.jpg", A + "wood_mr_2048.jpg"], None, 1024)]),
  ("Exterior_Aluminium", "Exterior · aluminium", [
    ("Acero Grafito", A + "powder_7016.jpg", [A + "powder_normal_2048.jpg", A + "powder_mr_2048.jpg"], None, 1024),
    ("Bronce Umbra", A + "powder_8019.jpg", [A + "powder_normal_2048.jpg", A + "powder_mr_2048.jpg"], 0.42, 1024),
    ("Negro Carbón", A + "powder_9005.jpg", [A + "powder_normal_2048.jpg", A + "powder_mr_2048.jpg"], None, 1024),
    ("Piedra", A + "powder_9016.jpg", [A + "powder_normal_2048.jpg", A + "powder_mr_2048.jpg"], None, 1024),
    ("Anodizado Natural", A + "powder_7035.jpg", [A + "powder_normal_2048.jpg", A + "powder_mr_2048.jpg"], 0.36, 1024)]),
  ("Hardware_Handle", "Handle", [
    ("Bronce Umbra", A + "hw_F4.jpg", [A + "hardware_normal_1024.jpg", A + "hardware_mr_1024.jpg"], None, 1024),
    ("Latón Cepillado", A + "hw_F4.jpg", [A + "hardware_normal_1024.jpg", A + "hardware_mr_1024.jpg"], None, 1024),
    ("Anodizado Natural", A + "hw_F1.jpg", [A + "hardware_normal_1024.jpg", A + "hardware_mr_1024.jpg"], None, 1024),
    ("Acero Grafito", A + "hw_F69.jpg", [A + "hardware_normal_1024.jpg", A + "hardware_mr_1024.jpg"], None, 1024),
    ("Negro Carbón", A + "hw_F9714M.jpg", [A + "hardware_normal_1024.jpg", A + "hardware_mr_1024.jpg"], None, 1024)])],
 "batiente": [
  ("Frame_Steel", "Steel", [
    ("Bronce Umbra", H + "bronze_Empire_Bronze_v2.jpg", [H + "bronze_normal_2048.jpg", H + "bronze_mr_v2_2048.jpg"], None, 2048),
    ("Acero Grafito", H + "paint_Wrought_Iron.jpg", [H + "paint_normal_2048.jpg", H + "paint_mr_2048.jpg"], None, 1024),
    ("Negro Carbón", H + "paint_Black.jpg", [H + "paint_normal_2048.jpg", H + "paint_mr_2048.jpg"], None, 1024),
    ("Piedra", H + "paint_Polar_White.jpg", [H + "paint_normal_2048.jpg", H + "paint_mr_2048.jpg"], None, 1024),
    ("Latón Cepillado", H + "bronze_Empire_Bronze_v2.jpg", [H + "bronze_normal_2048.jpg", H + "bronze_mr_v2_2048.jpg"], None, 2048)]),
  ("Hardware_Metal", "Handle", [
    ("Bronce Umbra", H + "hw_OilRubbed_Bronze.jpg", [H + "hardware_normal_1024.jpg", H + "hardware_mr_1024.jpg"], None, 1024),
    ("Latón Cepillado", H + "hw_Satin_Brass.jpg", [H + "hardware_normal_1024.jpg", H + "hardware_mr_1024.jpg"], None, 1024),
    ("Acero Grafito", H + "hw_Satin_Nickel.jpg", [H + "hardware_normal_1024.jpg", H + "hardware_mr_1024.jpg"], None, 1024),
    ("Negro Carbón", H + "hw_OilRubbed_Bronze.jpg", [H + "hardware_normal_1024.jpg", H + "hardware_mr_1024.jpg"], None, 1024)])],
 "tamiz": [
  ("Frame_Powdercoat", "Steel", [
    ("Acero Grafito", C + "frame_Graphite_Grey_RAL_7024.jpg", [C + "pc_normal_2048.jpg", C + "pc_mr_2048.jpg"], None, 1024),
    ("Negro Carbón", C + "frame_Crittall_Black_RAL_9005.jpg", [C + "pc_normal_2048.jpg", C + "pc_mr_2048.jpg"], None, 1024),
    ("Bronce Umbra", C + "frame_Light_Bronze_RAL_8070.jpg", [C + "pc_normal_2048.jpg", C + "pc_mr_2048.jpg"], 0.42, 1024),
    ("Piedra", C + "frame_Crittall_White_RAL_9911.jpg", [C + "pc_normal_2048.jpg", C + "pc_mr_2048.jpg"], None, 1024),
    ("Anodizado Natural", C + "frame_Light_Grey_RAL_7035.jpg", [C + "pc_normal_2048.jpg", C + "pc_mr_2048.jpg"], 0.36, 1024)]),
  ("Handle_Metal", "Handle", [
    ("Latón Cepillado", C + "metal_Polished_Brass.jpg", [C + "me_normal_2048.jpg", C + "me_mr_Satin_Chrome.jpg"], None, 1024),
    ("Bronce Umbra", C + "metal_Polished_Brass.jpg", [C + "me_normal_2048.jpg", C + "me_mr_Satin_Chrome.jpg"], None, 1024),
    ("Anodizado Natural", C + "metal_Satin_Chrome.jpg", [C + "me_normal_2048.jpg", C + "me_mr_Satin_Chrome.jpg"], None, 1024),
    ("Negro Carbón", C + "metal_Black.jpg", [C + "me_normal_2048.jpg", C + "me_mr_Black.jpg"], None, 1024)])],
}
def load(p):
    im = bpy.data.images.load(p); w, h = im.size
    a = np.array(im.pixels[:], dtype=np.float32).reshape(h, w, 4); return im, a
def save(a, path, fmt="JPEG", q=90):
    h, w = a.shape[:2]; im = bpy.data.images.new("o", w, h, alpha=False)
    im.pixels.foreach_set(a.ravel()); im.filepath_raw = path; im.file_format = fmt
    sc = bpy.context.scene; sc.render.image_settings.quality = q
    im.save_render(path) if False else im.save(); bpy.data.images.remove(im)
def resize(a, n):
    h, w = a.shape[:2]
    if w == n: return a
    if w > n and w % n == 0:
        f = w // n; return a.reshape(n, f, n, f, 4).mean(axis=(1, 3))
    ys = (np.arange(n) * h / n).astype(int); xs = (np.arange(n) * w / n).astype(int); return a[ys][:, xs]
def srgb2lin(c): return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
def lin2srgb(c): c = np.clip(c, 0, 1); return np.where(c <= 0.0031308, c * 12.92, 1.055 * c ** (1 / 2.4) - 0.055)
man = {}
for slug, nodes in SPEC.items():
    out = f"{WK}/{slug}/tex"; os.makedirs(out, exist_ok=True); man[slug] = []
    for nodeId, label, fins in nodes:
        for fin, src, maps, metal, size in fins:
            im, a = load(src); bpy.data.images.remove(im)
            a = resize(a, size)  # pixels from Blender are linear for sRGB JPGs? images load as sRGB bytes -> float = sRGB values
            tgt = np.array([int(HEX[fin][i:i + 2], 16) / 255 for i in (1, 3, 5)])
            lin = srgb2lin(a[..., :3]); m = lin.reshape(-1, 3).mean(0); t = srgb2lin(tgt)
            o = a.copy(); o[..., :3] = lin2srgb(lin * (t / np.maximum(m, 1e-4)))
            base = f"{out}/umbral-{slug}-{nodeId.lower()}-{SLUG[fin]}.jpg"; save(o, base)
            th = f"{out}/umbral-{slug}-{nodeId.lower()}-{SLUG[fin]}_thumb.jpg"; save(resize(o, 128), th)
            mfiles = []
            for i, mp in enumerate(maps):
                kind = "normal" if i == 0 else "mr"
                if kind == "mr" and metal is not None:
                    im, b = load(mp); bpy.data.images.remove(im); b = b.copy()
                    b[..., 2] = 1.0; b[..., 1] = np.clip(b[..., 1] * 0 + metal + (b[..., 1] - b[..., 1].mean()) * 0.6, 0.05, 1)
                    dst = f"{out}/umbral-{slug}-{nodeId.lower()}-mr-metal-{SLUG[fin]}.jpg"; save(b, dst)
                else:
                    dst = f"{out}/umbral-{slug}-{nodeId.lower()}-{kind}-{os.path.basename(mp).replace('Empire_Bronze','b').replace('Crittall_','')}"
                    dst = dst.replace("me_mr_", "mr_").replace("Satin_Chrome", "satin").replace("Black", "black")
                    if not os.path.exists(dst): shutil.copy(mp, dst)
                mfiles.append(os.path.basename(dst))
            man[slug].append({"node": nodeId, "label": label, "finish": fin, "base": os.path.basename(base), "thumb": os.path.basename(th), "maps": mfiles})
json.dump(man, open(WK + "/finishes_manifest.json", "w"), indent=1, ensure_ascii=False)
print("DONE", {k: len(v) for k, v in man.items()})
