# -*- coding: utf-8 -*-
"""Two more windows arrive, one at a time, and each takes the centre.

They sit in the same flex row as the first, so all three are the same size
and the spacing is fixed. The row slides left by exactly one window-plus-gap
per arrival -- (50% - half a window) is that distance for a row of three --
so whichever window arrived last is the one in the middle of the screen.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

BAR = """            <div class="rec-win-bar">
              <img class="rec-win-logo" src="mira-logo.svg" width="1152" height="365" alt="Mira">
              <span class="rec-win-dots" aria-hidden="true">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                     stroke-linecap="round"><path d="M5 12h14"/></svg>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                     stroke-linecap="round" stroke-linejoin="round"><path d="M14 4h6v6"/><path d="M10 20H4v-6"/><path d="M20 4l-7 7"/><path d="M4 20l7-7"/></svg>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                     stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>
              </span>
            </div>"""

ASK = """            <div class="rec-ask">
              <p class="rec-ask-hint">Ask a follow-up&hellip;</p>
              <div class="rec-ask-row">
                <span class="rec-ask-tools" aria-hidden="true">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                       stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg>
                  <b>@</b>
                </span>
                <span class="rec-ask-right">
                <span class="rec-ask-send" aria-hidden="true">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"
                       stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5"/><path d="M5 12l7-7 7 7"/></svg>
                </span>
                </span>
              </div>
            </div>"""

SEARCH = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"\n'
          '                     stroke-linecap="round" aria-hidden="true">'
          '<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>')


def window(ask, meta, lead, title, sub, count, rows, tail, chips):
    out = ['          <div class="rec-win rec-win--static">', BAR, '',
           '            <div class="rec-thread">',
           '              <div class="rec-turn rec-turn--you"><p>%s</p></div>' % ask,
           '              <div class="rec-turn rec-turn--meta">',
           '                ' + SEARCH,
           '                %s' % meta,
           '              </div>',
           '              <div class="rec-turn rec-turn--say"><p>%s</p></div>' % lead,
           '              <div class="rec-turn rec-turn--card">',
           '                <div class="rec-card-head">',
           '                  <span>',
           '                    <b>%s</b>' % title,
           '                    <i>%s</i>' % sub,
           '                  </span>',
           '                  <span class="rec-card-count">%s</span>' % count,
           '                </div>']
    for k, v, src, logo in rows:
        out += ['                  <div class="rec-row">',
                '                    <span class="rec-row-k">%s</span>' % k,
                '                    <span class="rec-row-v">%s</span>' % v,
                '                    <span class="rec-row-src"><img src="%s" alt="" loading="lazy">%s</span>'
                % (logo, src),
                '                  </div>']
    out += ['              </div>',
            '              <div class="rec-turn rec-turn--say"><p>%s</p></div>' % tail,
            '              <div class="rec-turn rec-turn--chips">']
    for c in chips:
        out.append('                <button type="button">%s</button>' % c)
    out += ['              </div>',
            '            </div>',
            '',
            ASK,
            '          </div>']
    return '\n'.join(out) + '\n'


schedule = window(
    'Who is interviewing this week?',
    'Checked 3 calendars and the open scorecards',
    'Six are on the calendar, two still need a panel.',
    'This week', 'Interviews &middot; 4 roles', '6 booked',
    [('Tuesday', '11:00 &middot; Priya Nair, round 2', 'Calendar', 'logo-4.svg'),
     ('Wednesday', '15:30 &middot; Arjun Rao, system design', 'Calendar', 'logo-4.svg'),
     ('Thursday', '10:00 &middot; Meera Joshi, final', 'Calendar', 'logo-4.svg'),
     ('Waiting', '2 panels have not replied', 'Slack', 'logo-3.svg')],
    'I can nudge the two panels that have gone quiet since Friday.',
    ['Nudge the panels', 'Move Thursday', 'Share the agenda'])

report = window(
    'How did hiring go last month?',
    'Read 7 roles and every scorecard filed',
    'September closed four roles, one ahead of the plan.',
    'September', 'Across 7 open roles', '4 hires',
    [('Offers', '4 accepted of 5 sent', 'Scorecard', 'logo-7.svg'),
     ('Time to hire', '19 days, down from 24', 'Weekly report', 'logo-3.svg'),
     ('Where they came from', 'Careers site 2 &middot; referral 2', 'Careers site', 'logo-8.svg'),
     ('Carried over', '3 roles still open', 'Calendar', 'logo-4.svg')],
    'Two of the three carried-over roles already have a shortlist waiting.',
    ['Open the roles', 'See the shortlists', 'Send me the report'])

old = """          </div>
          </div>
          </div>
        </section>"""
assert s.count(old) == 1, 'chat section close changed'
s = s.replace(old, "          </div>\n" + schedule + report
              + "          </div>\n          </div>\n        </section>", 1)

# ---- the row: same size, fixed gap, one window of travel per arrival --------
old = """    .rec-wins { position:absolute; top:50%; left:50%; translate:-50% -50%;
                display:flex;
                transform:translateY(calc(var(--win-down, 0) * 8vh))
                          scale(calc(1 - 0.06 * var(--win-down, 0))); }
    .rec-win { flex:none; width:540px; max-height:calc(100vh - 96px);"""
new = """    .rec-wins { position:absolute; top:50%; left:50%; translate:-50% -50%;
                display:flex; gap:36px;
                /* (50% - half a window) is exactly one window plus one gap for
                   a row of three, so each step centres the newest arrival */
                transform:scale(calc(1 - 0.06 * var(--win-down, 0)))
                          translateX(calc((1 - var(--wins, 0)) * (50% - 270px)))
                          translateY(calc(var(--win-down, 0) * 8vh)); }
    /* the two that follow are written out in full; they only have to appear */
    .rec-win--static { opacity:var(--wv, 0);
                       transform:translateX(calc((1 - var(--wv, 0)) * 48px)); }
    .rec-wins > .rec-win--static:nth-child(2) { --wv:var(--w2, 0); }
    .rec-wins > .rec-win--static:nth-child(3) { --wv:var(--w3, 0); }
    .rec-win--static .rec-turn { opacity:1; transform:none; }
    .rec-win { flex:none; width:540px; height:min(660px, calc(100vh - 190px));
               max-height:calc(100vh - 96px);"""
assert old in s, 'row/window rule changed'
s = s.replace(old, new, 1)

old = "      .rec-win { width:100%; max-height:none; }"
new = """      .rec-win { width:100%; height:auto; max-height:none; }
      .rec-win--static { opacity:1; transform:none; }"""
assert old in s, 'responsive window rule changed'
s = s.replace(old, new, 1)

# ---- room for the two extra beats ------------------------------------------
old = "    .rec-chat-sec { position:relative; min-height:260vh; margin-top:-55vh; }"
new = "    .rec-chat-sec { position:relative; min-height:400vh; margin-top:-55vh; }"
assert old in s, 'chat section rule changed'
s = s.replace(old, new, 1)

old = """        back = parseFloat(band(2.5, 1.5));      // the sky lightens
        root.style.setProperty('--win-down', band(2.4, 1.85));   // window drops
        root.style.setProperty('--close-in', band(1.9, 1.35));   // then the words
        // once it has arrived in the light, it drops the dark treatment
        if (win) { win.classList.toggle('is-light', parseFloat(band(2.4, 1.85)) > 0.92); }"""
new = """        back = parseFloat(band(3.5, 2.5));      // the sky lightens
        root.style.setProperty('--win-down', band(3.4, 2.85));   // window drops
        root.style.setProperty('--close-in', band(2.9, 2.35));   // then the words
        // once it has arrived in the light, it drops the dark treatment
        if (win) { win.classList.toggle('is-light', parseFloat(band(3.4, 2.85)) > 0.92); }
        // and then the other two, one at a time, each taking the centre
        var w2 = parseFloat(band(2.2, 1.7));
        var w3 = parseFloat(band(1.75, 1.25));
        root.style.setProperty('--w2', w2.toFixed(3));
        root.style.setProperty('--w3', w3.toFixed(3));
        root.style.setProperty('--wins', (w2 + w3).toFixed(3));"""
assert old in s, 'closing bands changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('two more windows')
