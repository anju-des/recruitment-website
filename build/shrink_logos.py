# -*- coding: utf-8 -*-
"""Shrink the tile logos to the size they are actually drawn at.

Each one is a bitmap wrapped in SVG — several are 3840x3840 — and they render
as 46px marks. That is 2.7MB arriving before eight thumbnails can appear,
which is why the boxes sit empty.

The wrapper is kept exactly as it is, including the ids and the viewBox, so
nothing referencing these files has to change. Only the embedded bitmap is
re-encoded smaller, and the pattern's scale is corrected to match: it is
1/width, so resizing the image without it would misplace the artwork.
"""
import base64
import io
import os
import re
import sys

from PIL import Image

LONG_SIDE = {'mira-logo.svg': 320}   # the wordmark needs the width
DEFAULT_LONG_SIDE = 160              # 46px marks, with room for 3x displays


def shrink(path):
    svg = io.open(path, encoding='utf-8').read()
    m = re.search(r'(xlink:href|href)="data:image/png;base64,([^"]+)"', svg)
    if not m:
        print('skip (no bitmap):', os.path.basename(path))
        return 0, 0

    before = os.path.getsize(path)
    img = Image.open(io.BytesIO(base64.b64decode(m.group(2))))
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    target = LONG_SIDE.get(os.path.basename(path), DEFAULT_LONG_SIDE)
    if max(img.size) <= target:
        print('skip (already small):', os.path.basename(path))
        return before, before

    ratio = target / float(max(img.size))
    size = (max(1, int(round(img.width * ratio))),
            max(1, int(round(img.height * ratio))))
    img = img.resize(size, Image.LANCZOS)

    buf = io.BytesIO()
    img.save(buf, format='PNG', optimize=True)
    data = base64.b64encode(buf.getvalue()).decode('ascii')

    svg = svg[:m.start(2)] + data + svg[m.end(2):]

    # the <image> declares the bitmap's pixel size...
    svg = re.sub(r'(<image[^>]*?)width="\d+" height="\d+"',
                 r'\g<1>width="%d" height="%d"' % size, svg, count=1)
    # ...and the pattern scales by 1/that, so both have to move together
    svg = re.sub(r'transform="scale\([^")]*\)"',
                 'transform="scale(%.10g %.10g)"' % (1.0 / size[0], 1.0 / size[1]),
                 svg, count=1)

    io.open(path, 'w', encoding='utf-8').write(svg)
    after = os.path.getsize(path)
    print('%-16s %7d -> %6d bytes  (bitmap %dx%d -> %dx%d)'
          % (os.path.basename(path), before, after,
             img.width / ratio, img.height / ratio, size[0], size[1]))
    return before, after


total_before = total_after = 0
for p in sys.argv[1:]:
    b, a = shrink(p)
    total_before += b
    total_after += a
if total_before:
    print('\ntotal %d -> %d bytes (%.1f%% smaller)'
          % (total_before, total_after,
             100.0 * (total_before - total_after) / total_before))
