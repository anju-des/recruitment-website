# -*- coding: utf-8 -*-
"""Official name is not a company signal; a country has one.

P1448 let Australia through -- states have official names, and so do
towns. The signals that stay are ones only an organisation carries: an
industry, a legal form, a founder, a chief executive, or an entry in a
company directory.

Wisemonk passes on industry and both directories, Stripe on industry.
Australia and Stribro have none of them.
"""
import io
import sys

OLD = "                    if (!(c.P452 || c.P1448 || c.P2088 || c.P4264)) return;"
NEW = ("                    if (!(c.P452 || c.P2088 || c.P4264 || c.P1454 ||\n"
       "                          c.P169 || c.P112)) return;")


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert s.count(OLD) == 1, (path, s.count(OLD))
    io.open(path, 'w', encoding='utf-8').write(s.replace(OLD, NEW, 1))
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
