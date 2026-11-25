"""Rename brand-bearing node/mesh/image/material names inside a GLB JSON chunk (geometry untouched, nothing scaled).
python3 glb_rename.py in.glb out.glb '{"Old":"New",...}'"""
import json, struct, sys
src, dst, mp = sys.argv[1], sys.argv[2], json.loads(sys.argv[3])
b = open(src, 'rb').read(); jl = struct.unpack('<I', b[12:16])[0]; j = json.loads(b[20:20 + jl]); rest = b[20 + jl:]
def fix(s):
    for k, v in mp.items(): s = s.replace(k, v)
    return s
n = 0
for key in ('nodes', 'meshes', 'images', 'materials', 'textures', 'animations', 'scenes'):
    for o in j.get(key, []):
        if 'name' in o:
            new = fix(o['name']); n += new != o['name']; o['name'] = new
js = json.dumps(j, separators=(',', ':')).encode()
while len(js) % 4: js += b' '
out = b[:12] + struct.pack('<I', len(js)) + b'JSON' + js + rest
out = out[:8] + struct.pack('<I', len(out)) + out[12:]
open(dst, 'wb').write(out); print('renamed', n, '->', dst, len(out))
