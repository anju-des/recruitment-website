# -*- coding: utf-8 -*-
"""Two values where two values help, one where they do not.

A flat "take the first two claims" made Stripe's location read "San
Francisco, South San Francisco, United States, Ireland" -- two
headquarters and two countries run together -- and its legal form
"corporation, limited liability company".

Founders are the case the allowance was for: "Patrick Collison, John
Collison" is the right answer and one of them is not. Industry too. The
rest take the first claim only.
"""
import io
import sys

OLD = """          ['P452', 'P159', 'P17', 'P31', 'P1454', 'P112', 'P169',
           'P749'].forEach(function (p) {
            (c[p] || []).slice(0, 2).forEach(function (claim) {
              var v = claim.mainsnak.datavalue &&
                      claim.mainsnak.datavalue.value;
              if (v && v.id) refs.push({ p: p, id: v.id });
            });
          });"""

NEW = """          // two only where two is the answer: people and industries
          [['P452', 2], ['P112', 2], ['P159', 1], ['P17', 1], ['P31', 1],
           ['P1454', 1], ['P169', 1], ['P749', 1]].forEach(function (r) {
            (c[r[0]] || []).slice(0, r[1]).forEach(function (claim) {
              var v = claim.mainsnak.datavalue &&
                      claim.mainsnak.datavalue.value;
              if (v && v.id) refs.push({ p: r[0], id: v.id });
            });
          });"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert s.count(OLD) == 1, (path, s.count(OLD))
    io.open(path, 'w', encoding='utf-8').write(s.replace(OLD, NEW, 1))
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
