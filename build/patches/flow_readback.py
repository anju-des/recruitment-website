# -*- coding: utf-8 -*-
"""The review reads the brief back instead of tabling it.

The sentence someone typed is the brief, so it leads, set large. The three
things Mira asked for follow as cards rather than rows: a table of four
label-and-value pairs is a form being checked, and this screen is meant to
be a thing being recognised.
"""
import io
import sys

OLD_JS = """    function review() {
      var rows = [
        ['Role', brief.role],
        ['Location', brief.location],
        ['Budget', brief.salary],
        ['Skills', brief.skills.join(', ')]
      ].map(function (r) {
        return '<div class="rec-flow-row"><dt>' + esc(r[0]) + '</dt><dd>' +
          (r[1] ? esc(r[1]) : '<em>Not given</em>') + '</dd></div>';
      }).join('');
      return '<h2 class="rec-flow-q">Ready to publish.</h2>' +
        '<p class="rec-flow-hint">This is what Mira has. Publish it and every ' +
        'application is read and ranked against it from the moment it lands.</p>' +
        '<dl class="rec-flow-sum">' + rows + '</dl>' +"""

NEW_JS = """    function review() {
      var facts = [
        ['Where', brief.location],
        ['Budget', brief.salary],
        ['Skills', brief.skills.join(', ')]
      ].map(function (f) {
        return '<span class="rec-flow-fact"><i>' + esc(f[0]) + '</i>' +
          (f[1] ? '<b>' + esc(f[1]) + '</b>'
                : '<b class="is-blank">Not given</b>') + '</span>';
      }).join('');
      return '<h2 class="rec-flow-q">Ready to publish.</h2>' +
        '<p class="rec-flow-hint">This is what Mira has. Publish it and every ' +
        'application is read and ranked against it from the moment it lands.</p>' +
        '<p class="rec-flow-brief' + (brief.role ? '' : ' is-blank') + '">' +
          (brief.role ? esc(brief.role) : 'No description given') + '</p>' +
        '<div class="rec-flow-facts">' + facts + '</div>' +"""

OLD_CSS = """    /* what it has understood */
    .rec-flow-sum { text-align:left; margin:0 0 clamp(24px, 3vw, 34px);
                    border:1px solid #E7E2F6; border-radius:16px;
                    overflow:hidden; }
    .rec-flow-row { display:flex; gap:18px; padding:15px 20px;
                    border-top:1px solid #F0ECFA; }
    .rec-flow-row:first-child { border-top:0; }
    .rec-flow-row dt { flex:none; width:104px; margin:0; color:#8A82A8;
                       font-size:12.5px; letter-spacing:.02em;
                       text-transform:uppercase; padding-top:2px; }
    .rec-flow-row dd { margin:0; color:#1A1430; font-size:15px;
                       line-height:1.5; }
    .rec-flow-row dd em { font-style:normal; color:#A49CC0; }"""

NEW_CSS = """    /* what it has understood, read back rather than tabled */
    .rec-flow-brief { max-width:34ch; margin:0 auto clamp(20px, 2.4vw, 30px);
                      color:#1A1430; font-size:clamp(17px, 0.6vw + 13px, 22px);
                      line-height:1.45; letter-spacing:-0.012em;
                      text-wrap:balance; }
    .rec-flow-brief.is-blank { color:#A49CC0; }
    .rec-flow-facts { display:flex; flex-wrap:wrap; justify-content:center;
                      gap:10px; margin-bottom:clamp(24px, 3vw, 34px); }
    .rec-flow-fact { display:flex; flex-direction:column; gap:3px;
                     min-width:120px; padding:12px 18px; border-radius:12px;
                     background:#F6F4FD; text-align:center; }
    .rec-flow-fact i { font-style:normal; color:#8A82A8; font-size:11px;
                       letter-spacing:.09em; text-transform:uppercase; }
    .rec-flow-fact b { font-weight:600; color:#1A1430; font-size:14.5px;
                       line-height:1.4; }
    .rec-flow-fact b.is-blank { font-weight:500; color:#A49CC0; }"""

OLD_MQ = """    @media (max-width:600px) {
      .rec-flow-row { flex-direction:column; gap:4px; }
      .rec-flow-row dt { width:auto; }
      .rec-flow-act { flex-wrap:wrap; }
    }"""
NEW_MQ = """    @media (max-width:600px) {
      .rec-flow-fact { min-width:0; flex:1 1 140px; }
      .rec-flow-act { flex-wrap:wrap; }
    }"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for old, new in ((OLD_JS, NEW_JS), (OLD_CSS, NEW_CSS), (OLD_MQ, NEW_MQ)):
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    assert 'rec-flow-sum' not in s, path + ': a table reference is left'
    assert 'rec-flow-row' not in s, path + ': a row reference is left'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
