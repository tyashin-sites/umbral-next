"""Alba / Batiente / Tamiz: brand-clean copies of the source GLBs (names only, geometry untouched),
Umbral backdrops and recoloured hotspot icons. System python3, stdlib only."""
import json, struct, re, os, shutil, subprocess, sys
DW = os.path.expanduser("~/Documents/Claude-Workspace/thridify-demos-2026-11/doorswindows")
WK = os.path.expanduser("~/Documents/Claude-Workspace/thridify-demos-2026-11/doorswindows/umbral-abt")
BRONZE_GLASS = [0.32, 0.22, 0.14]
P = {
 "alba": dict(src="w2-10-leawod", glb="LEAWOD-MXN120-R7.glb", out="UMBRAL-ALBA.glb",
   ren=[("LEAWOD-MXN120-R7", "UMBRAL-ALBA"), ("LeawodR7", "UmbralAlba")], tint={"Glass_Grey": 0.42},
   icons="icons", bd="branding"),
 "batiente": dict(src="05-hopes", glb="HOPES-JT175-CASEMENT.glb", out="UMBRAL-BATIENTE.glb",
   ren=[("HOPES-JT175-CASEMENT", "UMBRAL-BATIENTE"), ("HopesJamestown175", "UmbralBatiente")], tint={},
   icons="icons", bd="branding"),
 "tamiz": dict(src="14-crittall", glb="CW-W20-SCREEN.glb", out="UMBRAL-TAMIZ.glb",
   ren=[("CW-W20-SCREEN", "UMBRAL-TAMIZ"), ("CW_AO", "UMBRAL-TAMIZ_AO"), ("CrittallW20", "UmbralTamiz"), ("Berkeley", "Rosa"), ("Europrofile", "Placa"), ("Soho", "Recta")],
   tint={"Fixed_Glass_Solar": 0.42}, icons="branding/icons", bd="branding"),
}
BRAND = re.compile(r"leawod|mxn|hoppe|maco|hope|jamestown|jt175|ppg|empire|crittall|w20|duralife|berkeley|europrofile|soho|cw[-_]", re.I)
def ren(s, rules):
    for a, b in rules: s = s.replace(a, b)
    return s
def clean_glb(k, c):
    b = open(f"{DW}/{c['src']}/{c['glb']}", "rb").read()
    jl = struct.unpack("<I", b[12:16])[0]; j = json.loads(b[20:20 + jl]); rest = b[20 + jl:]
    for key in ("nodes", "meshes", "materials", "images", "textures", "animations", "scenes", "accessors", "bufferViews"):
        for x in j.get(key, []):
            for f in ("name", "uri"):
                if isinstance(x.get(f), str): x[f] = ren(x[f], c["ren"])
    for m in j["materials"]:
        if m["name"] in c["tint"]:
            m["pbrMetallicRoughness"]["baseColorFactor"] = BRONZE_GLASS + [c["tint"][m["name"]]]
    j["asset"]["generator"] = "Umbral"
    left = [(key, x.get("name")) for key in ("nodes", "meshes", "materials", "images", "animations") for x in j.get(key, []) if x.get("name") and BRAND.search(x["name"])]
    js = json.dumps(j, separators=(",", ":")).encode()
    while len(js) % 4: js += b" "
    out = struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(js) + len(rest)) + struct.pack("<II", len(js), 0x4E4F534A) + js + rest
    open(f"{WK}/{k}/{c['out']}", "wb").write(out)
    paths = sorted({x["name"] for x in j["nodes"]})
    return left
def strip_brand_svg(svg):
    svg = re.sub(r"<text[^>]*>[^<]*</text>", "", svg)
    svg = re.sub(r"<image[^>]*/>", "", svg)
    i = svg.find('opacity="0.30">')  # Hope's logo group: cut it with its nested <g>s
    if i > 0:
        s = svg.rfind("<g", 0, i); d = 0; p = s
        for m in re.finditer(r"<g\b|</g>", svg[s:]):
            d += 1 if m.group() != "</g>" else -1
            if d == 0: p = s + m.end(); break
        svg = svg[:s] + svg[p:]
    svg = re.sub(r"#(fd5e00|c61a1a|e8692d)", "#8A6A47", svg, flags=re.I)  # source accent rules -> Umbral bronze
    return svg
def backdrops(k, c):
    for n, w in (("backdrop_desktop", 2560), ("backdrop_mobile", 1920)):
        svg = strip_brand_svg(open(f"{DW}/{c['src']}/{c['bd']}/{n}.svg").read())
        W = 2560 if "desktop" in n else 1080; H = 1440 if "desktop" in n else 1920
        x, y, fs = (110, 150, 44) if W > H else (W / 2 - 110, 150, 40)
        mark = f'<text x="{x:.0f}" y="{y}" font-family="Newsreader, Georgia, Times New Roman, serif" font-size="{fs}" letter-spacing="{fs*0.42:.0f}" fill="#16140F" opacity="0.22">UMBRAL</text>'
        svg = svg.replace("</svg>", mark + "</svg>")
        assert not BRAND.search(re.sub(r'id="[^"]*"', "", svg)), (k, n)
        o = f"{WK}/{k}/{n}.svg"; open(o, "w").write(svg)
        subprocess.run(["qlmanage", "-t", "-s", str(w), "-o", f"{WK}/{k}", o], capture_output=True)
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "86", o + ".png", "--out", f"{WK}/{k}/umbral-{k}-{n}.jpg"], capture_output=True)
        os.remove(o + ".png")
def icons(k, c):
    d = f"{DW}/{c['src']}/{c['icons']}"; os.makedirs(f"{WK}/{k}/icons", exist_ok=True)
    dark = {"#0b4272", "#1d1d1b", "#1d1d1d"}; acc = {"#fd5e00", "#e8692d", "#ff6b6b", "#9fd3ff"}
    for f in os.listdir(d):
        if not f.endswith(".svg"): continue
        s = open(f"{d}/{f}").read()
        s = re.sub(r"#[0-9a-fA-F]{6}", lambda m: "#16140F" if m.group().lower() in dark else ("#8A6A47" if m.group().lower() in acc else m.group()), s)
        assert not BRAND.search(s), f
        open(f"{WK}/{k}/icons/umbral-{k}-{f}", "w").write(s)
ONLY_BD = "--backdrops" in sys.argv
for k in [a for a in sys.argv[1:] if not a.startswith("--")] or P:
    os.makedirs(f"{WK}/{k}", exist_ok=True)
    if not ONLY_BD: print(k, "brand names left in GLB:", clean_glb(k, P[k])); icons(k, P[k])
    backdrops(k, P[k])
    for n, (w, h) in (("backdrop_desktop", (2560, 1440)), ("backdrop_mobile", (1080, 1920))):
        subprocess.run(["sips", "-z", str(h), str(w), f"{WK}/{k}/umbral-{k}-{n}.jpg"], capture_output=True)
