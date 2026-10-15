# -*- coding: utf-8 -*-
"""A miss is recoverable, and does not claim to be a find.

Typing strip.com for stripe.com ended on "Found your company", a FOUND
badge and no way back -- the one screen in the flow with nothing to do
on it, reached by the one mistake people actually make.

When the record comes back empty the screen says so, drops the badge,
and offers the field again. The domain is still in the brief, so the
button lands back on the question with what they typed ready to be
corrected rather than retyped.

The card itself stays: it shows what was searched for, which is the
thing they need to look at to spot the typo.
"""
import io
import sys

OLD = """        function screen() {
          card.innerHTML =
            '<h2 class="rec-flow-q is-alone">Found your company</h2>' +
            '<div class="rec-flow-found">' +
              '<span class="rec-flow-found-mark">' +
                (logo ? '<img src="' + esc(logo) + '" alt="">'
                      : esc(who.charAt(0))) +
              '</span>' +
              '<span class="rec-flow-found-say"><b>' + esc(who) + '</b>' +
                '<i>' + esc(site) + '</i></span>' +
              '<span class="rec-flow-found-badge">Found</span>' +
            '</div>' +"""

NEW = """        function screen() {
          // nothing came back: do not dress a miss up as a find
          var blank = finished && !got.about &&
                      !(got.facts && got.facts.length);
          card.innerHTML =
            '<h2 class="rec-flow-q is-alone">' +
              (blank ? 'Nothing on that domain' : 'Found your company') +
            '</h2>' +
            '<div class="rec-flow-found">' +
              '<span class="rec-flow-found-mark">' +
                (logo ? '<img src="' + esc(logo) + '" alt="">'
                      : esc(who.charAt(0))) +
              '</span>' +
              '<span class="rec-flow-found-say"><b>' + esc(who) + '</b>' +
                '<i>' + esc(site) + '</i></span>' +
              (blank ? ''
                     : '<span class="rec-flow-found-badge">Found</span>') +
            '</div>' +"""

OLD_TAIL = """            (finished && !got.about && !(got.facts && got.facts.length)
              ? '<p class="rec-found-about is-thin">No public record to ' +
                'read from. Mira will take the rest from you.</p>'
              : '');
        }"""

NEW_TAIL = """            (blank
              ? '<p class="rec-found-about is-thin">No public record for ' +
                  'that one. Check the spelling, or try another.</p>' +
                '<div class="rec-flow-act">' +
                  '<button type="button" class="rec-flow-back">Try another ' +
                    'website</button>' +
                '</div>'
              : '');

          var again = card.querySelector('.rec-flow-back');
          // the domain is still in the brief, so the field comes back filled
          if (again) again.addEventListener('click', function () { draw(); });
        }"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for old, new in ((OLD, NEW), (OLD_TAIL, NEW_TAIL)):
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    js = s[s.rindex('<script>'):]
    assert 'Nothing on that domain' in js, path + ': the miss has no heading'
    # the label is split across two literals, so match the first half
    assert 'Try another ' in js, path + ': the miss has no way out'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
