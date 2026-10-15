# -*- coding: utf-8 -*-
"""One less "for" in the opening sentence.

"writes the role for your company instead of for a job title" trips on the
second preposition, and it is the first line anyone reads here.
"""
import io
import sys

OLD = ("'that across and Mira writes the role for your company instead ' +\n"
       "            'of for a job title.</p>' +")
NEW = ("'that across and the role goes out for your company, not for a ' +\n"
       "            'job title.</p>' +")


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert s.count(OLD) == 1, (path, s.count(OLD))
    io.open(path, 'w', encoding='utf-8').write(s.replace(OLD, NEW, 1))
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
