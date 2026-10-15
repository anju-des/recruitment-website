# -*- coding: utf-8 -*-
"""The chips carry a second line, and the room to show it.

"Wise" and "Job board" are labels, not answers -- they say which step
left the card, not what the step found. A line under each says that:
the domain that was looked up, and the address the board was given.

The mark grows with the card so the two lines sit against something,
rather than a 22px square floating beside a block of text.

The board address was written in one place and would have been written
again by the restore, so it moves into a function both can call. One
formula, one address.
"""
import io
import sys

EDITS = [
    # one formula for the address
    ("""    // the account screen's one action, defined where a reopen can find it""",
     """    // the board's address, from the one place that decides it
    function board_addr(who) {
      return String(who || '').toLowerCase().replace(/[^a-z0-9]/g, '') +
             '.mira.jobs';
    }

    // the account screen's one action, defined where a reopen can find it"""),

    ("""        var addr = found.who.toLowerCase().replace(/[^a-z0-9]/g, '') +
                   '.mira.jobs';""",
     """        var addr = board_addr(found.who);"""),

    # the chip itself
    ("""    function put_mini(i, label, logo, html) {""",
     """    function put_mini(i, label, sub, logo, html) {"""),

    ("""          '</span><b>' + esc(label) + '</b>' +""",
     """          '</span>' +
          '<span class="rec-done-text"><b>' + esc(label) + '</b>' +
            (sub ? '<i>' + esc(sub) + '</i>' : '') + '</span>' +"""),

    # and the four places that build one
    ("""            put_mini(1, 'Job board', found.logo, card.innerHTML);""",
     """            put_mini(1, 'Job board', addr, found.logo, card.innerHTML);"""),

    ("""            put_mini(0, who, logo, card.innerHTML);""",
     """            put_mini(0, who, brief.website, logo, card.innerHTML);"""),

    ("""      put_mini(0, was.who, was.logo, screens[0]);
      var last = 0;
      if (screens[1]) { put_mini(1, 'Job board', was.logo, screens[1]);
                        last = 1; }""",
     """      put_mini(0, was.who, was.website || '', was.logo, screens[0]);
      var last = 0;
      if (screens[1]) { put_mini(1, 'Job board', board_addr(was.who),
                                 was.logo, screens[1]);
                        last = 1; }"""),
]

CSS_EDITS = [
    ("""    .rec-done-card { display:flex; align-items:center; gap:9px; font:inherit;
                     margin:2px 0 0 30px; padding:9px 12px; max-width:100%;""",
     """    .rec-done-card { display:flex; align-items:center; gap:11px;
                     font:inherit;
                     margin:3px 0 0 30px; padding:11px 13px; max-width:100%;"""),

    ("""    .rec-done-mark { flex:none; width:22px; height:22px; border-radius:7px;
                     overflow:hidden; display:grid; place-items:center;
                     background:linear-gradient(135deg,#8B5CF6,#2684FF);
                     color:#FFFFFF; font-size:11px; font-weight:700; }""",
     """    .rec-done-mark { flex:none; width:30px; height:30px; border-radius:9px;
                     overflow:hidden; display:grid; place-items:center;
                     background:linear-gradient(135deg,#8B5CF6,#2684FF);
                     color:#FFFFFF; font-size:13px; font-weight:700; }"""),

    ("""    .rec-done-card b { min-width:0; font-size:13px; font-weight:600;
                       color:#1A1430; white-space:nowrap; overflow:hidden;
                       text-overflow:ellipsis; }""",
     """    .rec-done-text { display:flex; flex-direction:column; gap:1px;
                      min-width:0; }
    .rec-done-card b { min-width:0; font-size:13.5px; font-weight:600;
                       color:#1A1430; white-space:nowrap; overflow:hidden;
                       text-overflow:ellipsis; }
    .rec-done-card i { min-width:0; font-style:normal; font-size:11.5px;
                       color:#8A82A8; white-space:nowrap; overflow:hidden;
                       text-overflow:ellipsis; }"""),
]

def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-done-text' not in s, path + ': already two lines'
    for old, new in EDITS + CSS_EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    js = s[s.rindex('<script>'):]
    assert js.count('put_mini(') == 5, (path, 'call sites',
                                        js.count('put_mini('))
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
