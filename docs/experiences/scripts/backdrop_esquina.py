"""Umbral backdrop (no marks): source sky/landscape generator with the logo removed."""
import bpy, os
import numpy as np
B = os.path.expanduser("/Users/aapastechpvtltd/Documents/Claude-Workspace/thridify-demos-2026-11/doorswindows/umbral-hep/backdrops")
def save_rgba(arr, path, fmt='PNG'):
    h, w = arr.shape[:2]
    im = bpy.data.images.new(os.path.basename(path), w, h, alpha=True); im.colorspace_settings.name = 'Non-Color'
    im.pixels.foreach_set(arr[::-1].ravel()); im.filepath_raw = path; im.file_format = fmt
    bpy.context.scene.render.image_settings.quality = 90; im.save(); bpy.data.images.remove(im)

def noise(h, w, s, seed):
    rng = np.random.default_rng(seed); n = rng.standard_normal((h, w))
    fy = np.fft.fftfreq(h)[:, None]; fx = np.fft.fftfreq(w)[None, :]
    o = np.fft.ifft2(np.fft.fft2(n) * np.exp(-2 * np.pi**2 * s**2 * (fx**2 + fy**2))).real
    return (o - o.mean()) / (o.std() + 1e-9)

def ridge(w, seed, s):
    rng = np.random.default_rng(seed); n = rng.standard_normal(w)
    f = np.fft.fftfreq(w); o = np.fft.ifft(np.fft.fft(n) * np.exp(-2 * np.pi**2 * s**2 * f**2)).real
    return (o - o.mean()) / (o.std() + 1e-9)

def make(W, H, name, logo_w):
    y = np.linspace(0, 1, H)[:, None] * np.ones((1, W)); x = np.ones((H, 1)) * np.linspace(0, 1, W)[None, :]
    top = np.array([0.55, 0.68, 0.80]); mid = np.array([0.95, 0.86, 0.76]); hor = np.array([0.99, 0.80, 0.62])
    t = np.clip(y / 0.58, 0, 1)[..., None]
    img = top * (1 - t) ** 1.3 + mid * (1 - (1 - t) ** 1.3)
    img = img * (1 - 0.5 * np.clip((y - 0.42) / 0.16, 0, 1)[..., None]) + hor * 0.5 * np.clip((y - 0.42) / 0.16, 0, 1)[..., None]
    sun = np.exp(-(((x - 0.68) * W / H) ** 2 + (y - 0.56) ** 2) / 0.02)[..., None]       # soft low sun glow
    img = img + sun * np.array([0.10, 0.06, 0.02])
    img += 0.010 * noise(H, W, 70, 3)[..., None]
    hz = 0.585
    for i, (amp, s, col, off, a) in enumerate([(0.030, 300, (0.78, 0.70, 0.68), -0.050, 0.55),
                                                (0.020, 180, (0.66, 0.60, 0.58), -0.022, 0.65),
                                                (0.012, 110, (0.52, 0.50, 0.46), -0.006, 0.75)]):
        r = hz + off + amp * ridge(W, 20 + i, s * W / 2560)
        m = (y > r[None, :]).astype(np.float32)[..., None]
        img = img * (1 - m * a) + np.array(col) * m * a
    sea = (y > hz).astype(np.float32)[..., None]
    water = np.array([0.62, 0.70, 0.76]) + 0.08 * np.clip(1 - (y - hz) / 0.12, 0, 1)[..., None] * np.array([1.0, 0.6, 0.2])
    glint = np.exp(-((x - 0.68) * W / H / 0.06) ** 2)[..., None] * np.clip(1 - (y - hz) / 0.25, 0, 1)[..., None] * 0.10
    img = img * (1 - sea) + (water + glint + 0.006 * noise(H, W, 6, 7)[..., None]) * sea
    vign = 1 - 0.10 * (((x - 0.5) / 0.7) ** 2 + ((y - 0.5) / 0.9) ** 2)[..., None]
    img = np.clip(img * vign, 0, 1)
    out = np.ones((H, W, 4), np.float32); out[..., :3] = img
    save_rgba(out, os.path.join(B, name + ".jpg"), 'JPEG')
make(2560, 1440, "esquina-desktop", 330)
make(1080, 1920, "esquina-mobile", 300)
print("branding done")
