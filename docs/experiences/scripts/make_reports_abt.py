import json, os, sys
ids = json.load(open(os.path.expanduser("~/Documents/Claude-Workspace/thridify-demos-2026-11/doorswindows/umbral-abt/product_ids.json")))
prev = json.loads(sys.argv[1])
R = {
 "alba": dict(name="Umbral Alba", pid="UMBRAL-ALBA", sourceFolder="w2-10-leawod",
  motion="Tilt-and-turn: the handle turns up and the leaf tips in 7° from the top (Sash_Tilt), or turns level and the leaf swings in 85° on concealed hinges (Sash_Turn); two-leaf versions move both leaves, mirrored.",
  sizes=[{"label": f"{c} · {w} × {h} mm", "width_mm": w, "height_mm": h} for w, h in ((1100, 1400), (1300, 1600), (1500, 1800)) for c in ("One leaf", "Two leaves")],
  finishes=["Roble Ahumado", "Nogal", "Piedra", "Negro Carbón", "Acero Grafito", "Bronce Umbra", "Anodizado Natural", "Latón Cepillado"],
  glass=["Claro", "Bronce", "Satinado"],
  options=["Size and leaves (6 variants: one or two leaves × 3 sizes)", "Interior · wood: Roble Ahumado, Nogal, Piedra, Negro Carbón", "Exterior · aluminium: Acero Grafito, Bronce Umbra, Negro Carbón, Piedra, Anodizado Natural", "Handle: Bronce Umbra, Latón Cepillado, Anodizado Natural, Acero Grafito, Negro Carbón", "Glass: Claro double 5/27/5 argon, Claro triple, Bronce tinted, Satinado acid-etched"],
  hotspots=[("Tilt for air", "Turn the handle up and the leaf tips in 7° from the top. Air moves, rain stays out."), ("Turn to open", "Handle level, the leaf swings in 85° on its hidden hinges. The whole opening is clear."), ("Welded corners", "Frame and leaf are each one welded ring, 7 mm radius at the corners. No mitre line to open up."), ("Hinges inside the frame", "The pivots sit in the rebate. Closed, nothing shows."), ("Solid wood inside", "28.7 mm of timber on the frame, 16 mm on the leaf, facing the room. Smoked oak, walnut or painted."), ("Insulating glass", "5 mm, 27 mm argon, 5 mm, held in a 45 mm rabbet. Triple glazing on request."), ("Aluminium outside", "A thermally broken aluminium shell takes the weather. The whole section is 121 mm deep.")],
  geometry={"sightline_mm": 81, "frame_depth_mm": 121, "max_panel_w_mm": 1474, "max_panel_h_mm": 1774, "glazing": "37 mm double 5/27 argon/5 (triple 4/12/4/12/4 option)", "corner_radius_mm": 7, "note": "sightline = interior frame 13 + leaf 62 (+ gaps) read from the source section; leaf = 1500 × 1800 frame less 13 mm wood frame and 2 mm gap each side"},
  stills_finish="Acero Grafito outside, Roble Ahumado inside, Bronce Umbra handle",
  gaps=["Sizes are estimated (made to measure; no published sizes in the source).", "Hotspot pins show on the default variant only (platform behaviour inherited from the source build); the animations still play in every variant via the default view.", "Handle finishes share one metallic roughness map, so Negro Carbón and Piedra handles read slightly metallic.", "No inward fly screen modelled (it would block the tilt/turn).", "Hero still shows the leaf only slightly open: the 85° turn hides the frame shadow on the floor."]),
 "batiente": dict(name="Umbral Batiente", pid="UMBRAL-BATIENTE", sourceFolder="05-hopes",
  motion="Out-swing casement pair: both cam levers lift 90°, the left leaf swings out to 80°, then the right (which carries the astragal); they close in reverse order (Sash_Open).",
  sizes=[{"label": f"Pair and transom · {w} × {h} mm", "width_mm": w, "height_mm": h} for w, h in ((1219, 1829), (1524, 2032), (1829, 2438))],
  finishes=["Bronce Umbra", "Acero Grafito", "Negro Carbón", "Piedra", "Latón Cepillado"],
  glass=["Claro", "Satinado", "Acanalado"],
  options=["Size (3 variants, pair and transom)", "Steel: Bronce Umbra, Acero Grafito, Negro Carbón, Piedra, Latón Cepillado", "Handle: Bronce Umbra, Latón Cepillado, Acero Grafito, Negro Carbón", "Glazing bars: through bars 35 mm 2 × 3 / 2 × 4 / 3 × 5, applied bars 22 mm 2 × 3, no bars", "Glass: Claro low-E, Satinado acid-etched, Acanalado reeded", "Glazing bead: square or sloped"],
  hotspots=[("Open the casements", "Lift the cam handles and both leaves swing out to 80°. The right leaf carries the astragal, so it closes last and seals first."), ("Hot-rolled steel, welded", "Solid steel, welded at every corner. 36.5 mm where it is fixed, 66.7 mm where it opens."), ("Insulating glass", "Two 6 mm lites with a 12.5 mm cavity. The spacer is finished in the frame colour."), ("Glazing beads", "Square or sloped. The choice sets the shadow line the bead draws on the glass.")],
  geometry={"sightline_mm": 36.5, "operable_sightline_mm": 66.7, "frame_depth_mm": 44.5, "max_panel_w_mm": 890, "max_panel_h_mm": 1790, "glazing": "24.5 mm double 6/12.5/6", "glazing_bar_mm": 34.9, "note": "max leaf from the 1829 × 2438 size: (1829 − 2 × 25 frame) / 2 wide, casement zone to the transom bar centre high (estimate from generator parameters)"},
  stills_finish="Bronce Umbra steel, Latón Cepillado handles",
  gaps=["Sizes are estimated (built to order).", "Hotspot pins show on the default size only; the shopper's dimension readout uses the whole GLB box (all three sizes).", "No sidelites; one panel configuration (pair + transom).", "Through bars are modelled as caps on both faces over continuous glass (not individually glazed panes).", "Latón Cepillado on the steel uses the bronze grain maps (suggested option)."]),
 "tamiz": dict(name="Umbral Tamiz", pid="UMBRAL-TAMIZ", sourceFolder="14-crittall",
  motion="Side-hung door pair inside a gridded screen: lever down, the first leaf swings to 92°, the second follows to 90°, then they close (Doors_Open); the lever hotspot opens only the first leaf to ~72° (Leaf_Active_Open).",
  sizes=[{"label": f"Pair and sidelights · {w} × {h} mm", "width_mm": w, "height_mm": h} for w, h in ((2420, 2520), (3020, 2690), (3620, 2880))],
  finishes=["Acero Grafito", "Negro Carbón", "Bronce Umbra", "Piedra", "Anodizado Natural", "Latón Cepillado"],
  glass=["Claro", "Bronce", "Satinado", "Acanalado"],
  options=["Size (3 variants: door pair 1.4 / 1.7 / 2.0 m with sidelights and transom)", "Steel: Acero Grafito, Negro Carbón, Bronce Umbra, Piedra, Anodizado Natural", "Handle: Latón Cepillado, Bronce Umbra, Anodizado Natural, Negro Carbón", "Glazing bars: grid, horizontal bands, no bars", "Glass: Claro, Bronce tinted, Satinado acid-etched, Acanalado reeded", "Lever: round rose, long plate, square rose"],
  hotspots=[("Open both doors", "The first leaf swings to 92°, the second follows to 90°. Then they close in the same order, reversed."), ("Lever", "On a round rose, a long plate or a square rose. Press it and the first leaf opens on its own."), ("Powder-coated steel", "Hot-rolled, galvanised, powder-coated to 30 % gloss. It reads matt in daylight."), ("Glass", "16.4 mm insulating glass behind 25 mm bars. Claro, Satinado, Acanalado or Bronce."), ("Low threshold", "15 mm high. The floor runs through from one room to the next.")],
  geometry={"sightline_mm": 32, "leaf_sightline_mm": 55, "frame_depth_mm": 34, "max_panel_w_mm": 1000, "max_panel_h_mm": 2400, "glazing": "16.4 mm double", "glazing_bar_mm": 25, "threshold_mm": 15, "note": "max leaf from the 3.6 m size (door pair 2000 × 2400); horizontal coupling 85 mm"},
  stills_finish="Acero Grafito steel, Latón Cepillado levers",
  gaps=["Sizes are estimated.", "The source context is an exterior terrace; the model still carries a stone terrace strip on one side, which reads as the next room's floor.", "Only three lever shapes; no single-door or arched layouts.", "Bronce glass is the source solar-control pane re-tinted in the GLB, with a drawn swatch thumbnail."]),
}
for slug, r in R.items():
    pv = prev[slug]
    out = {"slug": slug, "name": r["name"], "pid": r["pid"], "productId": ids[slug], "previewId": pv,
           "live": f"https://admin.thridify.com/p/{pv}", "admin": f"https://admin.thridify.com/products/{ids[slug]}",
           "sourceFolder": r["sourceFolder"], "motion": r["motion"], "sizes": r["sizes"], "finishes": r["finishes"], "glass": r["glass"], "options": r["options"],
           "hotspots": [{"title": t, "text": x} for t, x in r["hotspots"]], "geometry": r["geometry"],
           "stills": {"hero": f"/images/{slug}/hero.webp", "front": f"/images/{slug}/front.webp", "detail": f"/images/{slug}/detail.webp", "finish": r["stills_finish"]},
           "gaps": r["gaps"]}
    json.dump(out, open(f"{slug}.json", "w"), indent=2, ensure_ascii=False)
print("ok")
