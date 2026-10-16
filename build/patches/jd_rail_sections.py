# -*- coding: utf-8 -*-
"""The panel lists everything the last step made, under its own heading.

Rounds were there alone, which made the other three look like they had
not happened. Each now has a heading and its rows: the screening
questions, the interview rounds, the salary range with what it is a
range for, and the job description itself.

A step can hold several of these now, each keyed, so redrawing one does
not take the others with it.

The job description row opens the document rather than the screen --
it is the only row here that came from outside, and the sheet is where
it lives.
"""
import io
import sys

OLD_HEAD = "    // ---- what a step made, under that step ---------"
OLD_TAIL = "    // what a finished step leaves behind, under that step"

NEW_JS = r"""    // ---- what a step made, under that step --------------------------

    // Several of these can sit under one step, each with its own key, so
    // redrawing one leaves the rest alone. rows: [{ n, say, end, go }].
    function rail_set(i, key, label, count, rows) {
      var step = flow.querySelectorAll('.rec-step')[i];
      if (!step) return;
      var set = step.querySelector('.rec-rail-set[data-set="' + key + '"]');
      if (!rows || !rows.length) { if (set) set.remove(); return; }
      if (!set) {
        set = document.createElement('div');
        set.className = 'rec-rail-set';
        set.setAttribute('data-set', key);
        step.appendChild(set);
      }
      set.innerHTML =
        '<p class="rec-rail-head">' + esc(label) +
          (count ? '<b>' + esc(String(count)) + '</b>' : '') + '</p>' +
        '<ul class="rec-rail-rows">' +
          rows.map(function (r) {
            return '<li><button type="button" class="rec-rail-row">' +
              (r.n ? '<i>' + esc(r.n) + '</i>' : '') +
              '<span>' + esc(r.say) + '</span>' +
              (r.end ? '<em>' + esc(r.end) + '</em>' : '') +
              '</button></li>';
          }).join('') +
        '</ul>';
      var all = set.querySelectorAll('.rec-rail-row');
      for (var k = 0; k < all.length; k++) {
        (function (b, go) {
          b.addEventListener('click', go || function () {
            show_details(i, open_i !== i);
          });
        }(all[k], rows[k].go));
      }
    }

    // the panel reads off the same state the screens do
    function rail_draw() {
      if (!flow) return;

      if (kept[1]) {
        var said = (role.title || (brief.role || '').split(',')[0] || '')
          .trim();
        rail_set(1, 'board', 'Board', said ? '1 role' : '', [
          { say: board_addr((company && company.who) || ''), end: 'live' }
        ].concat(said ? [{ say: said }] : []));
      }

      if (!kept[2]) return;

      rail_set(2, 'qs', 'Screening questions',
        (role.questions || []).length,
        (role.questions || []).map(function (q, n) {
          return { n: String(n + 1), say: q };
        }));

      rail_set(2, 'rounds', 'Interview rounds', (role.rounds || []).length,
        (role.rounds || []).map(function (r, n) {
          return { n: String(n + 1), say: r.say,
                   end: r.mins ? r.mins + 'm' : '' };
        }));

      rail_set(2, 'pay', 'Salary range', '', role.pay
        ? [{ say: role.pay,
             end: role.pay_from === 'market' ? 'market' : 'yours' }]
        : []);

      rail_set(2, 'jd', 'Job description', '', jd
        ? [{ say: jd_name || 'The job description', end: 'open',
             go: show_jd }]
        : []);

      // a set that was empty once and filled later was appended last, so
      // the order says when each one arrived rather than what it is.
      // appendChild moves a node it already has: this puts them in order.
      var step = flow.querySelectorAll('.rec-step')[2];
      if (!step) return;
      ['qs', 'rounds', 'pay', 'jd'].forEach(function (key) {
        var set = step.querySelector('.rec-rail-set[data-set="' + key + '"]');
        if (set) step.appendChild(set);
      });
    }

"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert "rail_set(2, 'qs'" not in s, path + ': already sectioned'

    at = s.index(OLD_HEAD)
    end = s.index(OLD_TAIL, at)
    assert end > at, (path, 'the rail slice runs backwards')
    s = s[:at] + NEW_JS + s[end:]

    assert 'function found_who' not in s, path + ': a helper was left behind'
    assert s.count('function rail_set') == 1, (path, 'two rail_sets')
    assert s.count('function rail_draw') == 1, (path, 'two rail_draws')

    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
