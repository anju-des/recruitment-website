# -*- coding: utf-8 -*-
"""Send does nothing with nothing in the field.

Pressing it empty opened the flow on the company question, which is the
right screen for someone who has no job description and the wrong one
for someone who has simply not typed anything yet -- the page is a
field and a send button, and the first thing many people do is press
the button.

The question stays exactly where it was for the no-JD path: describe
the role, press send, and it asks for the company. It just will not
open on an empty field. The cursor goes back to where the words are
meant to go, which says more than a message would.
"""
import io
import sys

OLD = """    form.addEventListener('submit', function (e) {
      e.preventDefault();
      open();
    });"""

NEW = """    form.addEventListener('submit', function (e) {
      e.preventDefault();
      // nothing to go on: the field is the answer, not a screen
      if (!field.value.trim()) { field.focus(); return; }
      open();
    });"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert s.count(OLD) == 1, (path, 'submit', s.count(OLD))
    s = s.replace(OLD, NEW, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
