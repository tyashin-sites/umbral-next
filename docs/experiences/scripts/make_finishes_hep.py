# Blender headless: retint source base-colour textures to the Umbral finish vocabulary.
# nice -n 5 /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup -P make_finishes_hep.py
import bpy, numpy as np, os, json
D = os.path.expanduser('~/Documents/Claude-Workspace/thridify-demos-2026-11/doorswindows/')
OUT = D + 'umbral-hep/finishes/'; os.makedirs(OUT, exist_ok=True)
HEX = {'Bronce Umbra':'#4A3A2A','Latón Cepillado':'#B08D57','Acero Grafito':'#3A3B3C','Negro Carbón':'#1A1A1A',
       'Anodizado Natural':'#A9ABAD','Piedra':'#E7E2D8','Roble Ahumado':'#5B4332','Nogal':'#4A3426'}
SF = D+'09-skyframe/textures/finishes/'; FW = D+'w2-12-fleetwood/textures/2k/'; MV = D+'08-marvin/textures/2k/'
JOBS = [  # (out key, source base, finish)
 ('h_frame_bronce', SF+'profile_bronze.jpg','Bronce Umbra'), ('h_frame_grafito', SF+'profile_black.jpg','Acero Grafito'),
 ('h_frame_negro', SF+'profile_black.jpg','Negro Carbón'), ('h_frame_natural', SF+'profile_natural.jpg','Anodizado Natural'),
 ('h_frame_piedra', SF+'profile_traffic.jpg','Piedra'),
 ('e_frame_natural', FW+'fin_anod_clear.jpg','Anodizado Natural'), ('e_frame_bronce', FW+'fin_anod_mbronze.jpg','Bronce Umbra'),
 ('e_frame_grafito', FW+'fin_anod_black.jpg','Acero Grafito'), ('e_frame_negro', FW+'fin_k_black50.jpg','Negro Carbón'),
 ('e_frame_piedra', FW+'fin_k_bone.jpg','Piedra'), ('e_frame_laton', FW+'fin_s_champagne.jpg','Latón Cepillado'),
 ('e_hw_natural', FW+'fin_hw_ss.jpg','Anodizado Natural'), ('e_hw_negro', FW+'fin_hw_black.jpg','Negro Carbón'),
 ('e_hw_laton', FW+'fin_hw_ss.jpg','Latón Cepillado'), ('e_hw_bronce', FW+'fin_hw_ss.jpg','Bronce Umbra'),
 ('p_wood_roble', MV+'fin_oak_hazelnut.jpg','Roble Ahumado'), ('p_wood_nogal', MV+'fin_mahog_clear.jpg','Nogal'),
 ('p_wood_piedra', MV+'fin_paint_white.jpg','Piedra'), ('p_wood_negro', MV+'fin_paint_black.jpg','Negro Carbón'),
 ('p_clad_bronce', MV+'fin_clad_bronze.jpg','Bronce Umbra'), ('p_clad_grafito', MV+'fin_clad_gunmetal.jpg','Acero Grafito'),
 ('p_clad_negro', MV+'fin_clad_ebony.jpg','Negro Carbón'), ('p_clad_piedra', MV+'fin_clad_stone_white.jpg','Piedra'),
 ('p_clad_natural', MV+'fin_clad_bright_silver.jpg','Anodizado Natural'),
 ('p_hw_bronce', MV+'fin_hw_bronze.jpg','Bronce Umbra'), ('p_hw_laton', MV+'fin_hw_brass.jpg','Latón Cepillado'),
 ('p_hw_grafito', MV+'fin_hw_nickel.jpg','Acero Grafito'), ('p_hw_negro', MV+'fin_hw_bronze.jpg','Negro Carbón'),
 ('p_sill_bronce', MV+'fin_sill_bronze.jpg','Bronce Umbra'), ('p_sill_natural', MV+'fin_sill_mill.jpg','Anodizado Natural'),
 ('p_sill_grafito', MV+'fin_sill_mill.jpg','Acero Grafito'), ('p_sill_negro', MV+'fin_sill_mill.jpg','Negro Carbón'),
]
def save(arr, w, h, path, q=88):
    im = bpy.data.images.new('o', w, h, alpha=False); im.colorspace_settings.name = 'Non-Color'
    im.pixels.foreach_set(arr.astype(np.float32).ravel())
    s = bpy.context.scene; s.render.image_settings.file_format = 'JPEG'; s.render.image_settings.quality = q
    s.render.image_settings.color_mode = 'RGB'; s.view_settings.view_transform = 'Standard'
    im.save_render(path, scene=s); bpy.data.images.remove(im)
report = {}
for key, src, fin in JOBS:
    im = bpy.data.images.load(src); im.colorspace_settings.name = 'Non-Color'
    w, h = im.size; px = np.empty(w*h*4, np.float32); im.pixels.foreach_get(px); px = px.reshape(h, w, 4)
    rgb = px[..., :3]; mean = rgb.reshape(-1, 3).mean(0)
    tgt = np.array([int(HEX[fin][i:i+2], 16)/255 for i in (1, 3, 5)])
    # keep the source's relative variation (grain, die lines), recentred on the target colour
    lum = rgb.mean(-1, keepdims=True); lm = max(lum.mean(), 1e-3)
    var = np.clip(lum/lm, 0.55, 1.6) ** (0.8 if tgt.mean() < 0.3 else 1.0)
    out = np.clip(tgt[None, None, :] * var, 0, 1)
    full = np.dstack([out, np.ones((h, w, 1))])
    save(full, w, h, OUT + key + '.jpg')
    # thumbnail 256: centre crop resampled by striding
    st = max(1, w // 256); th = full[::st, ::st][:256, :256]
    save(th, th.shape[1], th.shape[0], OUT + 'thumb_' + key + '.jpg', 90)
    report[key] = {'src': os.path.basename(src), 'finish': fin, 'size': [w, h], 'mean_out': [round(float(x), 3) for x in out.reshape(-1, 3).mean(0)]}
    bpy.data.images.remove(im)
json.dump(report, open(OUT + 'finishes.json', 'w'), indent=1, ensure_ascii=False)
print('DONE', len(report))
