# -*- coding: utf-8 -*-
"""Only take the logo if it is a logo.

For a domain it does not know, Google's favicon service answers 404 with a
decodable 16x16 globe -- and Chrome fires `load`, not `error`, when the
body decodes. So the error handler never ran and unknown companies got a
grey globe that reads as a broken image.

A real answer at sz=128 comes back 128 wide; the globe is 16. Anything
under 64 is the placeholder, and the lettered tile stays.
"""
import io
import sys

OLD = """        img.addEventListener('load', function () {
          mark.textContent = '';
          mark.appendChild(img);
        });"""

NEW = """        img.addEventListener('load', function () {
          // a 404 from this service still decodes: it answers with a 16px
          // globe, where a real logo at sz=128 comes back 128 wide
          if (img.naturalWidth < 64) return;
          mark.textContent = '';
          mark.appendChild(img);
        });"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert s.count(OLD) == 1, (path, s.count(OLD))
    io.open(path, 'w', encoding='utf-8').write(s.replace(OLD, NEW, 1))
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
