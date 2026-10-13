# -*- coding: utf-8 -*-
"""Mira at every stage: a rail of four, each with its own answer.

Screening, interview, scorecard, offer -- pick one on the left and the
right changes. Each stage says what Mira does and, under it, what stays
with the recruiter, because the whole positioning is human-led.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

ICONS = {
    'screening': '<path d="M3 5h18l-7 8.2V20l-4 1.6v-8.4z"/>',
    'interview': '<rect x="3" y="5" width="18" height="16" rx="2.5"/>'
                 '<path d="M8 3v4M16 3v4M3 11h18"/>',
    'scorecard': '<rect x="5" y="4" width="14" height="17" rx="2.5"/>'
                 '<path d="M9.5 4h5v3h-5z"/><path d="M9 13.5l2 2 4-4.5"/>',
    'offer': '<circle cx="12" cy="12" r="9"/><path d="M8.3 12.4l2.6 2.6 4.8-5.4"/>',
}
LABEL = {'screening': 'Screening', 'interview': 'Interview',
         'scorecard': 'Scorecard', 'offer': 'Offer'}


def icon(key, cls=''):
    return ('<svg%s viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" '
            'aria-hidden="true">%s</svg>'
            % ((' class="%s"' % cls) if cls else '', ICONS[key]))


STAGES = [
    ('screening',
     'Every application read the morning it lands',
     'Mira reads each CV against the scorecard you wrote, ranks it, and puts '
     'the six worth your time at the top of the list.',
     'You set the bar',
     'The scorecard is yours. Mira only applies it, and shows its working on '
     'every candidate.',
     """              <div class="rec-art-head">
                <span><b>Senior Backend Engineer</b><i>Shortlist &middot; this morning</i></span>
                <span class="rec-art-count">6 of 38</span>
              </div>
              <div class="rec-art-list">
                <span class="rec-art-row"><b>Priya Nair</b><i>Senior Backend Engineer</i><em>92%</em></span>
                <span class="rec-art-row"><b>Arjun Rao</b><i>Backend Engineer</i><em>86%</em></span>
                <span class="rec-art-row"><b>Meera Joshi</b><i>Platform Engineer</i><em>81%</em></span>
              </div>"""),

    ('interview',
     'Panels booked around the time people actually have',
     'Mira reads the free time of everyone on the panel, proposes the slots '
     'that work, and sends the invite with the Meet link attached.',
     'You keep the room',
     'Mira never sits in your place. It finds the hour and writes the invite; '
     'the conversation is yours.',
     """              <div class="rec-art-head">
                <span><b>Final round &middot; Priya Nair</b><i>45 minutes &middot; 3 interviewers</i></span>
                <span class="rec-art-count">Pick a time</span>
              </div>
              <div class="rec-slots">
                <span class="rec-slot"><b>Tue 11:00</b><i>All three free</i></span>
                <span class="rec-slot is-pick"><b>Thu 10:00</b><i>All three free</i></span>
                <span class="rec-slot"><b>Fri 16:30</b><i>Two of three</i></span>
              </div>"""),

    ('scorecard',
     'Feedback collected while the interview is still fresh',
     'Mira chases the scorecard the same afternoon, pulls the notes together, '
     'and tells you where the panel disagrees.',
     'You call it',
     'Mira summarises what the panel said. Whether that is a yes is not its '
     'decision to make.',
     """              <div class="rec-art-head">
                <span><b>Priya Nair</b><i>Panel of three &middot; filed today</i></span>
                <span class="rec-art-count">3 of 3 in</span>
              </div>
              <div class="rec-art-scores">
                <span class="rec-art-score"><i>System design</i><span class="rec-bar"><span style="width:90%"></span></span><em>4.5</em></span>
                <span class="rec-art-score"><i>Code quality</i><span class="rec-bar"><span style="width:84%"></span></span><em>4.2</em></span>
                <span class="rec-art-score"><i>Ownership</i><span class="rec-bar"><span style="width:70%"></span></span><em>3.5</em></span>
              </div>
              <div class="rec-art-note">The panel split on ownership &mdash; two yes, one lean no.</div>"""),

    ('offer',
     'Offers that go out the day the decision is made',
     'Mira drafts the offer off the band you set, tracks it to signature, and '
     'keeps the start date in front of everyone who needs it.',
     'You make the offer',
     'The number, the title and the call are yours. Mira does the paperwork '
     'and the chasing.',
     """              <div class="rec-art-head">
                <span><b>Offer &middot; Priya Nair</b><i>Senior Backend Engineer</i></span>
                <span class="rec-art-pill">Accepted</span>
              </div>
              <div class="rec-art-list">
                <span class="rec-art-row"><b>Compensation</b><i>Within the band you set</i><em>&#8377;48L</em></span>
                <span class="rec-art-row"><b>Starts</b><i>After a 30-day notice</i><em>13 Nov</em></span>
                <span class="rec-art-row"><b>Time to hire</b><i>From first application</i><em>19 days</em></span>
              </div>"""),
]

rail = []
panes = []
for i, (key, head, sub, note_t, note_b, art) in enumerate(STAGES):
    on = ' is-on' if i == 0 else ''
    rail.append(
        '            <button class="rec-stage-tab%s" type="button" role="tab"\n'
        '                    aria-selected="%s" data-rec-stage="%s">\n'
        '              %s\n'
        '              %s\n'
        '            </button>' % (on, 'true' if i == 0 else 'false', key,
                                   icon(key), LABEL[key]))
    panes.append(
        """          <div class="rec-stage-pane%s" data-rec-pane="%s" role="tabpanel">
            <div class="rec-stage-text">
              <span class="rec-stage-chip">%s%s</span>
              <h3 class="rec-stage-h">%s</h3>
              <p class="rec-stage-p">%s</p>
              <div class="rec-stage-note">
                <b>%s</b>
                <p>%s</p>
              </div>
            </div>
            <div class="rec-stage-art">
              <div class="rec-art-card">
%s
              </div>
            </div>
          </div>""" % (on, key, icon(key), LABEL[key], head, sub, note_t, note_b, art))

block = """        <!-- and back down into violet, the same way -->
        <section class="rec-deep">
          <div class="rec-stage-pin">
            <div class="rec-stage-rail" role="tablist" aria-label="Hiring stages">
%s
            </div>
%s
          </div>
        </section>""" % ('\n'.join(rail), '\n'.join(panes))

old = """        <!-- and back down into violet, the same way -->
        <section class="rec-deep"></section>"""
assert old in s, 'deep section markup changed'
s = s.replace(old, block, 1)

CSS = """
    /* ---- stages ------------------------------------------------------------ */
    /* It holds the middle of the screen for the length of the section, and
       arrives with the violet rather than after it. */
    .rec-stage-pin { position:sticky; top:0; min-height:100vh;
                     width:min(1240px, 92vw); margin-inline:auto;
                     display:grid; grid-template-columns:208px minmax(0, 1fr);
                     gap:34px; align-content:center; align-items:center;
                     opacity:var(--deep-in, 0);
                     transform:translateY(calc((1 - var(--deep-in, 0)) * 34px)); }
    .rec-stage-rail { display:flex; flex-direction:column; border-radius:16px;
                      overflow:hidden; background:rgba(255,255,255,.045);
                      box-shadow:inset 0 0 0 1px rgba(255,255,255,.12); }
    .rec-stage-tab { display:flex; align-items:center; gap:11px; cursor:pointer;
                     font-family:inherit; font-size:14px; font-weight:500;
                     text-align:left; border:none; background:none;
                     padding:17px 18px; color:#BDB4DE;
                     box-shadow:inset 0 -1px 0 rgba(255,255,255,.09);
                     transition:background .2s, color .2s, box-shadow .2s; }
    .rec-stage-tab:last-child { box-shadow:none; }
    .rec-stage-tab svg { width:17px; height:17px; flex:none; color:#9D8DD6; }
    .rec-stage-tab:hover { color:#EDE9FF; background:rgba(255,255,255,.05); }
    /* the one you are reading carries the accent, like a selected file */
    .rec-stage-tab.is-on { color:#FFFFFF; background:rgba(255,255,255,.11);
                           box-shadow:inset 3px 0 0 #A78BFA,
                                      inset 0 -1px 0 rgba(255,255,255,.09); }
    .rec-stage-tab.is-on:last-child { box-shadow:inset 3px 0 0 #A78BFA; }
    .rec-stage-tab.is-on svg { color:#C9B8FF; }

    .rec-stage-pane { display:none; }
    .rec-stage-pane.is-on { display:grid;
                            grid-template-columns:minmax(0, 1fr) minmax(0, 1.06fr);
                            gap:40px; align-items:center; }
    .rec-stage-chip { display:inline-flex; align-items:center; gap:7px;
                      font-size:12.5px; font-weight:500; color:#DCD3FF;
                      background:rgba(167,139,250,.20); border-radius:100px;
                      padding:6px 13px;
                      box-shadow:inset 0 0 0 1px rgba(201,184,255,.22); }
    .rec-stage-chip svg { width:14px; height:14px; }
    .rec-stage-h { margin:18px 0 0; max-width:19ch; color:#FFFFFF;
                   font-size:clamp(23px, 1.5vw + 12px, 34px); font-weight:600;
                   line-height:1.18; letter-spacing:-0.025em; text-wrap:balance; }
    .rec-stage-p { margin:13px 0 0; max-width:46ch; color:#B6ADD6;
                   font-size:15.5px; line-height:1.6; }
    /* what the recruiter keeps -- the point of the whole page */
    .rec-stage-note { margin-top:22px; border-radius:12px; padding:14px 16px;
                      background:rgba(255,255,255,.05);
                      box-shadow:inset 0 0 0 1px rgba(201,184,255,.20); }
    .rec-stage-note b { display:block; font-size:13.5px; font-weight:600;
                        color:#EDE9FF; }
    .rec-stage-note p { margin:5px 0 0; font-size:13.5px; line-height:1.55;
                        color:#ABA2CB; }

    /* the picture of the stage: a lit tile with one card on it */
    .rec-stage-art { border-radius:20px; padding:30px;
                     background:linear-gradient(135deg, #7C5CF6 0%, #A98BFF 42%,
                                                #E6B8E8 78%, #FBD2C4 100%); }
    .rec-art-card { border-radius:13px; overflow:hidden; background:#FFFFFF;
                    box-shadow:0 18px 40px rgba(22,10,56,.26); }
    .rec-art-head { display:flex; align-items:flex-start; justify-content:space-between;
                    gap:14px; padding:14px 16px; background:#F7F8FA; }
    .rec-art-head b { display:block; font-size:14px; font-weight:600; color:#222733; }
    .rec-art-head i { display:block; margin-top:2px; font-style:normal;
                      font-size:12px; color:#6B7588; }
    .rec-art-count { flex:none; font-size:12px; color:#7C5CF6; white-space:nowrap; }
    .rec-art-pill { flex:none; font-size:12px; font-weight:600; color:#027A48;
                    background:#E6F9F0; border-radius:100px; padding:4px 10px; }
    .rec-art-row { display:grid; grid-template-columns:1fr auto; align-items:center;
                   column-gap:12px; padding:11px 16px;
                   box-shadow:inset 0 1px 0 rgba(32,22,66,.08); }
    .rec-art-row b { font-size:13.5px; font-weight:600; color:#222733; }
    .rec-art-row i { grid-column:1; font-style:normal; font-size:12px; color:#6B7588; }
    .rec-art-row em { grid-column:2; grid-row:1 / span 2; font-style:normal;
                      font-size:13px; font-weight:600; color:#5B3DD4; }
    .rec-art-scores { padding:6px 16px 12px; }
    .rec-art-score { display:grid; grid-template-columns:104px 1fr 34px;
                     align-items:center; gap:11px; padding:9px 0; }
    .rec-art-score i { font-style:normal; font-size:12.5px; color:#6B7588; }
    .rec-art-score em { font-style:normal; font-size:12.5px; font-weight:600;
                        color:#222733; text-align:right; }
    .rec-bar { height:6px; border-radius:100px; background:#EEF0F4; }
    .rec-bar span { display:block; height:100%; border-radius:100px; background:#8B5CF6; }
    .rec-art-note { padding:11px 16px; font-size:12.5px; color:#6B7588;
                    box-shadow:inset 0 1px 0 rgba(32,22,66,.08); }
    @media (prefers-reduced-motion: reduce) {
      .rec-stage-pin { opacity:1; transform:none; }
      .rec-stage-tab { transition:none; }
    }
"""

old = "    /* ---- suggestions ------"
assert old in s, 'suggestions block missing'
s = s.replace(old, CSS + "\n    /* ---- suggestions ------", 1)

# ---- narrow screens: the rail goes across the top, the art under the words --
old = """      .rec-close { min-height:40vh; }
      .rec-deep { min-height:60vh; }"""
new = """      .rec-close { min-height:40vh; }
      .rec-deep { min-height:0; padding-block:72px; }
      .rec-stage-pin { position:static; min-height:0; grid-template-columns:1fr;
                       gap:24px; opacity:1; transform:none; }
      .rec-stage-rail { flex-direction:row; overflow-x:auto; }
      .rec-stage-tab { flex:1 0 auto; justify-content:center; padding:13px 14px;
                       box-shadow:inset -1px 0 0 rgba(255,255,255,.09); }
      .rec-stage-tab.is-on, .rec-stage-tab.is-on:last-child {
        box-shadow:inset 0 -3px 0 #A78BFA; }
      .rec-stage-pane.is-on { grid-template-columns:1fr; gap:26px; }
      .rec-stage-art { padding:20px; border-radius:16px; }"""
assert old in s, 'responsive closing rule changed'
s = s.replace(old, new, 1)

# ---- the rail arrives with the violet --------------------------------------
old = """        down = Math.min(1, Math.max(0, down));
      }"""
new = """        down = Math.min(1, Math.max(0, down));
        // the rail comes up over the back half of that ramp
        root.style.setProperty('--deep-in',
          Math.min(1, Math.max(0, (down - 0.45) / 0.4)).toFixed(3));
      }"""
assert old in s, 'deep progress changed'
s = s.replace(old, new, 1)

# ---- and the rail itself ----------------------------------------------------
old = "  // Mira's thread plays itself:"
new = """  // One stage at a time: the rail picks which pane is shown.
  (function () {
    var rail = document.querySelector('.rec-stage-rail');
    if (!rail) return;
    var tabs = [].slice.call(rail.querySelectorAll('[data-rec-stage]'));
    var panes = [].slice.call(document.querySelectorAll('[data-rec-pane]'));
    rail.addEventListener('click', function (e) {
      var tab = e.target.closest('[data-rec-stage]');
      if (!tab) return;
      var key = tab.getAttribute('data-rec-stage');
      tabs.forEach(function (t) {
        var on = t === tab;
        t.classList.toggle('is-on', on);
        t.setAttribute('aria-selected', on ? 'true' : 'false');
      });
      panes.forEach(function (pane) {
        pane.classList.toggle('is-on', pane.getAttribute('data-rec-pane') === key);
      });
    });
  }());


  // Mira's thread plays itself:"""
assert old in s, 'thread comment changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('four stages on a rail')
