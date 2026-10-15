# -*- coding: utf-8 -*-
"""The result column matches the question's width.

"Your custom job board is ready" and "Your account is ready to open"
were breaking over two lines in a 520px column while the question beside
them had 680. The two are the same screen a moment apart, so they take
the same measure.

The paragraph keeps its own max-width, so widening the column opens up
the headings and the tile rows without letting prose run long.
"""
import io
import sys

OLD = "    .rec-found-col { width:min(520px, 100%); margin-inline:auto;"
NEW = "    .rec-found-col { width:min(680px, 100%); margin-inline:auto;"


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert s.count(OLD) == 1, (path, s.count(OLD))
    io.open(path, 'w', encoding='utf-8').write(s.replace(OLD, NEW, 1))
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
