# -*- coding: utf-8 -*-
"""Step two spins from the moment step one ends, and stops when it is built.

Two gaps, both at the seams:

Step one tucked away and then waited 700ms before step two began, so the
rail showed a plain "2" for most of a second -- the step was neither
done nor doing anything, which is the one thing it was never going to
be. It goes busy as step one ends.

And it kept spinning while the finished board sat on screen for two
seconds, because the tick was inside the tuck timer. Step one ticks when
its facts land; step two now ticks when its board lands.
"""
import io
import sys

EDITS = [
    ("""            put_mini(0, who, logo, card.innerHTML);
            card.innerHTML = '';
            window.setTimeout(board, 700);""",
     """            put_mini(0, who, logo, card.innerHTML);
            card.innerHTML = '';
            step_busy(1);          # no dead "2" in the gap
            window.setTimeout(board, 700);"""),

    ("""          window.setTimeout(function () {
            if (!flow || flow.hidden) return;
            at_step(1, true);
            flow.classList.add('is-found');""",
     """          at_step(1, true);      # built: stop spinning now, not at the tuck
          window.setTimeout(function () {
            if (!flow || flow.hidden) return;
            flow.classList.add('is-found');"""),
]


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for old, new in EDITS:
        old = old.replace('          # ', '          // ').replace('      # ', '      // ')
        new = new.replace('          # ', '          // ').replace('      # ', '      // ')
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
