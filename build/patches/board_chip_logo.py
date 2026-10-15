# -*- coding: utf-8 -*-
"""The board chip carries the company mark, not a letter J.

With no logo passed, the chip fell back to the first letter of its own
label, so it read as a "J" tile beside the words "Job board". The board
belongs to the company, so it wears the company's mark -- which also
makes the two chips read as one set rather than two unrelated things.
"""
import io
import sys

OLD = "            put_mini(1, 'Job board', '', card.innerHTML);"
NEW = "            put_mini(1, 'Job board', found.logo, card.innerHTML);"


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert s.count(OLD) == 1, (path, s.count(OLD))
    io.open(path, 'w', encoding='utf-8').write(s.replace(OLD, NEW, 1))
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
