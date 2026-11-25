"""Umbral backdrop (no marks): source sky/landscape generator with the logo removed."""
import bpy, os
import numpy as np
B = os.path.expanduser("/Users/aapastechpvtltd/Documents/Claude-Workspace/thridify-demos-2026-11/doorswindows/umbral-hep/backdrops")
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
    top = np.array([0.62, 0.72, 0.82]); mid = np.array([0.93, 0.90, 0.86]); low = np.array([0.96, 0.88, 0.78])
    t = np.clip(y / 0.62, 0, 1)[..., None]
    img = top * (1 - t) ** 1.4 + mid * (1 - (1 - t) ** 1.4)
    img = img * (1 - 0.25 * np.clip((y - 0.45) / 0.2, 0, 1)[..., None]) + low * 0.25 * np.clip((y - 0.45) / 0.2, 0, 1)[..., None]
    img += 0.012 * noise(H, W, 60, 3)[..., None]                       # soft cloud haze
    hz = 0.60
    for i, (amp, s, col, off) in enumerate([(0.022, 260, (0.74, 0.78, 0.80), -0.04), (0.014, 150, (0.62, 0.67, 0.67), -0.014)]):
        r = hz + off + amp * ridge(W, 10 + i, s * W / 2560)
        m = (y > r[None, :]).astype(np.float32)
        img = img * (1 - m[..., None] * 0.7) + np.array(col) * m[..., None] * 0.7
    lake = (y > hz).astype(np.float32)[..., None]
    water = np.array([0.66, 0.73, 0.77]) + 0.06 * (1 - (y - hz) / (1 - hz))[..., None]
    rip = np.real(np.fft.ifft(np.fft.fft(np.random.default_rng(5).standard_normal(H)) * np.exp(-2*np.pi**2*4*np.fft.fftfreq(H)**2)))[:, None]
    img = img * (1 - lake) + (water + 0.006 * (rip / rip.std()) [..., None] * np.ones((1, W, 1)) + 0.004 * noise(H, W, 30, 7)[..., None]) * lake
    vign = 1 - 0.10 * (((x - 0.5) / 0.7) ** 2 + ((y - 0.5) / 0.9) ** 2)[..., None]
    img = np.clip(img * vign, 0, 1)
    out = bpy.data.images.new(name, W, H); px = np.ones((H, W, 4), np.float32); px[..., :3] = img[::-1]
    out.colorspace_settings.name = 'Non-Color'; out.pixels.foreach_set(px.ravel())
    out.filepath_raw = os.path.join(B, name + ".jpg"); out.file_format = 'JPEG'; bpy.context.scene.render.image_settings.quality = 90; out.save()
make(2560, 1440, "patio-desktop", 300)
make(1080, 1920, "patio-mobile", 260)
