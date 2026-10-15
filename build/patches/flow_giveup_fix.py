# -*- coding: utf-8 -*-
"""When the lookup stops early, stop showing the steps it will never take.

give_up() went through step(), which advances the counter, so a failed
search left "matching the official website..." blinking away as the
current job and the header counting up to "step 4 of 4" for work that
had already been abandoned.

It now ends the list where it stopped, and the header says so instead of
counting.
"""
import io
import sys

OLD_PAINT = """              '<p class="rec-work-head"><span class="rec-work-dot"></span>' +
                'Mira is working on step ' + Math.min(now + 1, jobs.length) +
                ' of ' + jobs.length + '</p>' +"""

NEW_PAINT = """              '<p class="rec-work-head"><span class="rec-work-dot' +
                (stopped ? ' is-off' : '') + '"></span>' +
                (stopped ? 'Mira finished looking'
                         : 'Mira is working on step ' +
                           Math.min(now + 1, jobs.length) + ' of ' +
                           jobs.length) + '</p>' +"""

# anchored short, because the line that follows carries a literal arrow
OLD_LINE = """              (now < jobs.length"""
NEW_LINE = """              (!stopped && now < jobs.length"""

OLD_VARS = """        var ran = [];
        var now = 0;"""
NEW_VARS = """        var ran = [];
        var now = 0;
        var stopped = false;"""

OLD_GIVE = """        function give_up(why) {
          step(false, why, function () { show(); });
        }"""
NEW_GIVE = """        function give_up(why) {
          ran.push({ ok: false, say: why });
          stopped = true;
          paint();
          window.setTimeout(show, 760);
        }"""

OLD_CSS = """    .rec-work-dot { width:8px; height:8px; border-radius:50%; flex:none;
                    background:#12B76A;
                    animation:rec-work-pulse 1.5s ease-in-out infinite; }"""
NEW_CSS = """    .rec-work-dot { width:8px; height:8px; border-radius:50%; flex:none;
                    background:#12B76A;
                    animation:rec-work-pulse 1.5s ease-in-out infinite; }
    .rec-work-dot.is-off { background:#C4CAD6; animation:none; }"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for old, new in ((OLD_VARS, NEW_VARS), (OLD_PAINT, NEW_PAINT),
                     (OLD_LINE, NEW_LINE), (OLD_GIVE, NEW_GIVE),
                     (OLD_CSS, NEW_CSS)):
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
