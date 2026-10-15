# -*- coding: utf-8 -*-
"""Strip the bold off the value, not just off the label.

Claude writes "**Company:** Wisemonk" -- colon inside the asterisks -- so
the label pattern ate the opening pair and left the closing pair on the
front of the value: "** Wisemonk", and a website of "** https:" that built
a link to https://** https:.
"""
import io
import sys

OLD = """        if (m) got[m[1].toLowerCase()] = m[2].replace(/\\*+$/, '').trim();"""

NEW = """        if (m) {
          got[m[1].toLowerCase()] =
            m[2].replace(/^\\s*\\*+/, '').replace(/\\*+\\s*$/, '').trim();
        }"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert s.count(OLD) == 1, (path, s.count(OLD))
    io.open(path, 'w', encoding='utf-8').write(s.replace(OLD, NEW, 1))
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
