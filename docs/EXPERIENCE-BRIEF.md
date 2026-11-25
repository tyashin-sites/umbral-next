# Umbral experiences — agent brief (25 Nov 2026)

You turn existing, published Thridify door/window configurators on the account
**doorswindows@thridify.com** into NEW products for the invented house **Umbral**. Read
`docs/BRAND.md` in this repo first (names, finish vocabulary, voice, banned words).
The source products are real-brand replicas; the Umbral copies must carry **no real brand
name, logo, mark, product code or brand-specific finish name anywhere** (product, variants,
option sets, finishes, hotspots, descriptions, file names the shopper can see).

Repo: `~/Documents/Claude-Workspace/tyashin-customer-sites/umbral-next` (call it REPO).
Source folders: `~/Documents/Claude-Workspace/thridify-demos-2026-11/doorswindows/<folder>/`
(each has HANDOFF.md, the .blend, the generator, the GLB, textures, mesh_paths.json, video/spec.json).

## Read first
1. `~/Documents/Claude-Workspace/thridify-demos-2026-11/PLAYBOOK.md` and
   `~/Documents/Claude-Workspace/thridify-demos-2026-11/doorswindows/DW-BRIEF.md` (platform
   findings: glass as show/hide meshes, never finishes; material names unique, ≤50 chars;
   `selectedMaterials` + `selectedDesigns` both required; defaultVariant is a string id).
2. Your source folder's HANDOFF.md.
3. The copy recipe (no duplicate endpoint exists):
   upload GLB (`GET /v1/file/start-file-upload/<name>?uniqueFolder=1`, PUT bytes to `url`) →
   `POST /v1/product` with the source's GET body minus `id, createdOn, updatedOn,
   resolvedEnvironment, previewId, lastPublishedAt, model, defaultVariant, modelSettings,
   customizerSettings, hotspots` plus new `pid`, `name`, `modelFolder`, `modelFilePath` →
   poll `GET /v1/product/:id/optimize-model/status` until `succeeded` →
   `PUT /v1/product/:id` with `modelSettings`, `customizerSettings` (merge
   `hidePriceConfigurator: true`), `hotspots` (no `surface` field), `modularizations` →
   POST each variant (`/v1/product/:id/variant`) → set `defaultVariant` → publish (same way
   the source build published; see PLAYBOOK) → wait, then QA `/p/<previewId>?v=1`.

## Access
- Chrome **"Browser 3"** (deviceId `f96d8cc3-7448-4fe6-bea7-0c182e03dedc`) is signed in to
  admin.thridify.com as doorswindows@. Create ONE tab of your own (`tabs_create_mcp`), go to
  `https://admin.thridify.com/products/list`, paste
  `~/Documents/Claude-Workspace/thridify-demos-2026-11/doorswindows/dw-tab-helper.js` into
  `javascript_tool`, then use `T.api` / `T.input` / `T.uploadInput` (+ the `file_upload` tool).
- NEVER sign in/out, never call ghost/admin/user endpoints, never print or return the token.
  Only close the tab YOU created. Other agents share this browser.
- Never modify or delete the SOURCE products or anything you did not create.
  `GET /v1/material` before creating finishes so retries don't duplicate.

## What each Umbral product must have
- `pid`: `UMBRAL-<NAME>` (e.g. `UMBRAL-HORIZONTE`), `name`: `Umbral <Name>` (e.g. `Umbral Horizonte 19`).
- **Brand marks gone.** If the source model has logo/brand-mark meshes (check
  `video/spec.json` → `thridify.hideMeshes`, mesh names, HANDOFF), remove them from the
  geometry: open the .blend headless, delete those objects, re-export the GLB with the same
  export settings the generator uses (never scale anything). Re-run `_audit/audit_glb.py` on it.
- **Finishes** re-created as new materials named `Umbral – <Finish>` from BRAND.md's
  vocabulary (reuse the source textures/maps; map each source finish to the closest Umbral
  finish; drop source finishes that have no close match; keep 4–7 per node). Interior/exterior
  nodes stay split where the source has them.
- **Option sets / variants / glass / sizes**: keep every configurable dimension the source
  has (sizes, panel counts, glass types, grids, handles), relabelled in Umbral language
  (Spanish glass names from BRAND.md: Claro, Satinado, Acanalado, Bronce; sizes in metric
  first, e.g. "4 panels · 6.0 m"). No source brand wording in any label.
- **Hotspots**: same positions and animations; titles and descriptions rewritten in the
  Umbral voice (exact, quiet, numbers over adjectives, ≤ 2 sentences, sentence case, none of
  the banned words). Custom SVG icons may be reused if they carry no brand mark.
- Backdrop: reuse the source backdrop if it has no brand marks.
- `customizerSettings.hidePriceConfigurator = true` (merged, keep other settings).
- Description (product) in the Umbral voice, 2–3 sentences.

## Stills for the website (Blender, free, local)
From the cleaned .blend, render with Cycles (Metal GPU if available, ≤128 samples + denoise):
- `hero.webp` 2400×1500, 3/4 view, late-afternoon light: one low warm sun (~3800 K) raking
  across the floor so the frame casts long mullion shadows; soft cool sky fill. Limestone/
  plaster context from the model. The opening shown OPEN partway if it reads better.
- `front.webp` 1600×2000 portrait, straight-on elevation, closed.
- `detail.webp` 1600×1600, close crop of the profile/handle/hinge where the craft is.
- Default finish: the most "Umbral" one (Bronce Umbra or Acero Grafito) unless the system
  is clearly anodised/black; record which.
Save to `REPO/public/images/<slug>/` (slug = lowercase name without number: horizonte, eje …).
WebP quality ~82, each ≤ 400 KB. This Mac has no cwebp or Pillow: have Blender write WebP
directly (`scene.render.image_settings.file_format = 'WEBP'`, `quality = 82`). Run Blender as
`nice -n 5 /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup -P script.py`.
Keep render scripts in `REPO/docs/experiences/scripts/` (not in public/).

## Report
Write `REPO/docs/experiences/<slug>.json`:
```json
{ "slug":"horizonte", "name":"Umbral Horizonte 19", "pid":"UMBRAL-HORIZONTE",
  "productId":"…", "previewId":"…", "live":"https://admin.thridify.com/p/<previewId>",
  "admin":"https://admin.thridify.com/products/<productId>",
  "sourceFolder":"09-skyframe",
  "motion":"what opens and how (one line)",
  "sizes":[{"label":"…","width_mm":0,"height_mm":0}],
  "finishes":["Bronce Umbra", "…"], "glass":["Claro","…"], "options":["…"],
  "hotspots":[{"title":"…","text":"…"}],
  "geometry":{"sightline_mm":0,"frame_depth_mm":0,"max_panel_w_mm":0,"max_panel_h_mm":0,"glazing":"e.g. 34 mm triple"},
  "stills":{"hero":"/images/horizonte/hero.webp","front":"…","detail":"…","finish":"Bronce Umbra"},
  "gaps":["anything not done"] }
```
`geometry` comes from the generator's real parameters (what the model actually is). Then
reply in ≤ 150 words: links, what's configurable, anything unfinished.

Target: about 60–75 minutes for your three products. Work them in parallel where you can
(start the optimiser for product 2 while you configure product 1).
