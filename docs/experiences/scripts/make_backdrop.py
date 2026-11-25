"""Umbral backdrop (shared by Eje, Reja, Pliegue): late-afternoon limestone sky over a hazy ridge and a pale terrace,
faint UMBRAL wordmark low-left. Writes SVG then rasterises with qlmanage + sips (no stock, no AI)."""
import os, subprocess, math, random
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets')
def ridge(W, y0, amp, seed, n=9):
    random.seed(seed); pts = []
    for i in range(n + 1):
        x = W * i / n; pts.append((x, y0 - amp * (0.4 + 0.6 * random.random())))
    d = f"M0 {pts[0][1]:.1f} "
    for (x0, y_0), (x1, y1) in zip(pts, pts[1:]):
        cx = (x0 + x1) / 2; d += f"C {cx:.1f} {y_0:.1f}, {cx:.1f} {y1:.1f}, {x1:.1f} {y1:.1f} "
    return d
def svg(W, H, hz, wx, wy, ws):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{max(W,H)}" height="{max(W,H)}" viewBox="0 0 {W} {H}" preserveAspectRatio="none">
<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C9CFCC"/><stop offset="0.55" stop-color="#E6E1D6"/><stop offset="1" stop-color="#F1E6D6"/></linearGradient>
<linearGradient id="fl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E4DDD0"/><stop offset="1" stop-color="#CFC6B6"/></linearGradient>
<radialGradient id="sun" cx="0.78" cy="{hz/H:.3f}" r="0.55"><stop offset="0" stop-color="#F7E3C4" stop-opacity="0.75"/><stop offset="1" stop-color="#F7E3C4" stop-opacity="0"/></radialGradient>
<filter id="b"><feGaussianBlur stdDeviation="{W/400:.1f}"/></filter>
</defs>
<rect width="{W}" height="{H}" fill="url(#sky)"/>
<rect width="{W}" height="{hz}" fill="url(#sun)"/>
<g filter="url(#b)">
<path d="{ridge(W, hz, H*0.07, 3)} L {W} {hz+4} L 0 {hz+4} Z" fill="#B9BDB5" opacity="0.55"/>
<path d="{ridge(W, hz, H*0.035, 8, 13)} L {W} {hz+4} L 0 {hz+4} Z" fill="#A4A99E" opacity="0.5"/>
</g>
<rect y="{hz}" width="{W}" height="{H-hz}" fill="url(#fl)"/>
<rect y="{hz}" width="{W}" height="{H*0.004:.1f}" fill="#8A6A47" opacity="0.10"/>
<text x="{wx}" y="{wy}" font-family="Newsreader, Georgia, 'Times New Roman', serif" font-weight="300" font-size="{ws}" letter-spacing="{ws*0.32:.1f}" fill="#16140F" opacity="0.13">UMBRAL</text>
</svg>'''
for name, args in (('umbral_backdrop_desktop', (2560, 1440, 1000, 150, 1330, 46)), ('umbral_backdrop_mobile', (1080, 1920, 1330, 80, 1820, 40))):
    p = os.path.join(OUT, name + '.svg'); open(p, 'w').write(svg(*args))
    subprocess.run(['qlmanage', '-t', '-s', str(max(args[0], args[1])), '-o', OUT, p], capture_output=True)
    png = p + '.png'
    subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '88', png, '--out', os.path.join(OUT, name + '.jpg')], capture_output=True)
    subprocess.run(['sips', '-z', str(args[1]), str(args[0]), os.path.join(OUT, name + '.jpg')], capture_output=True)  # qlmanage squares it
    os.remove(png); print(name, 'ok')
