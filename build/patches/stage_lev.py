# -*- coding: utf-8 -*-
"""The stage section, rebuilt to the reference layout.

A two-tone line across the top, the four stages spread as a row of tabs, a
ruler under them with a mark that slides to whichever is open, and then one
wide panel: the claim on the left with its supporting line held at the
foot, and on the right a lit surface carrying the stage's own card with a
Mira read floating off its corner.
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
SPARK = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
         '<path d="M12 2.5l1.9 5.3 5.3 1.9-5.3 1.9L12 16.9l-1.9-5.3L4.8 9.7l5.3-1.9z"/>'
         '<path d="M19 14.5l.8 2.2 2.2.8-2.2.8-.8 2.2-.8-2.2-2.2-.8 2.2-.8z"/></svg>')
CLIP = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M5 4h9l5 5v11a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1z"/>'
        '<path d="M14 4v5h5"/></svg>')


def icon(key):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" '
            'aria-hidden="true">%s</svg>' % ICONS[key])


STAGES = [
    dict(key='screening',
         head='Read every application the morning it lands',
         foot='Mira ranks each CV against your scorecard and puts the six worth '
              'your time at the top. You set the bar; it only applies it.',
         art="""                <div class="rec-art-head">
                  <span><b>Senior Backend Engineer</b><i>Shortlist &middot; this morning</i></span>
                  <span class="rec-art-count">6 of 38</span>
                </div>
                <div class="rec-art-list">
                  <span class="rec-art-row"><b>Priya Nair</b><i>Senior Backend Engineer</i><em>92%</em></span>
                  <span class="rec-art-row"><b>Arjun Rao</b><i>Backend Engineer</i><em>86%</em></span>
                  <span class="rec-art-row"><b>Meera Joshi</b><i>Platform Engineer</i><em>81%</em></span>
                </div>""",
         tag='Shortlist &middot; today',
         lead='Six worth your time.',
         note='Two more than last week from the same intake, because the '
              'scorecard now weights payments experience.',
         file='Shortlist.pdf'),

    dict(key='interview',
         head='Book the panel around the time people actually have',
         foot='Mira reads everyone’s free time, proposes the slots that work '
              'and sends the invite. The conversation stays yours.',
         art="""                <div class="rec-art-head">
                  <span><b>Final round &middot; Priya Nair</b><i>45 minutes &middot; 3 interviewers</i></span>
                  <span class="rec-art-count">Pick a time</span>
                </div>
                <div class="rec-slots">
                  <span class="rec-slot"><b>Tue 11:00</b><i>All three free</i></span>
                  <span class="rec-slot is-pick"><b>Thu 10:00</b><i>All three free</i></span>
                  <span class="rec-slot"><b>Fri 16:30</b><i>Two of three</i></span>
                </div>""",
         tag='Scheduling &middot; final round',
         lead='Thursday saves four days.',
         note='The earliest hour all three interviewers share, and it keeps '
              'the offer inside your average.',
         file='Calendar invite'),

    dict(key='scorecard',
         head='Collect the feedback while the interview is still fresh',
         foot='Mira chases the scorecard the same afternoon and pulls the notes '
              'together. Whether it is a yes is not its call.',
         art="""                <div class="rec-art-head">
                  <span><b>Priya Nair</b><i>Panel of three &middot; filed today</i></span>
                  <span class="rec-art-count">3 of 3 in</span>
                </div>
                <div class="rec-art-scores">
                  <span class="rec-art-score"><i>System design</i><span class="rec-bar"><span style="width:90%"></span></span><em>4.5</em></span>
                  <span class="rec-art-score"><i>Code quality</i><span class="rec-bar"><span style="width:84%"></span></span><em>4.2</em></span>
                  <span class="rec-art-score"><i>Ownership</i><span class="rec-bar"><span style="width:70%"></span></span><em>3.5</em></span>
                </div>""",
         tag='Panel &middot; split',
         lead='Two yes, one lean no.',
         note='The disagreement is all on ownership. Worth one follow-up '
              'question before you decide.',
         file='Panel notes'),

    dict(key='offer',
         head='Send the offer the day the decision is made',
         foot='Mira drafts off the band you set, tracks it to signature and keeps '
              'the start date in front of everyone. The call is yours.',
         art="""                <div class="rec-art-head">
                  <span><b>Offer &middot; Priya Nair</b><i>Senior Backend Engineer</i></span>
                  <span class="rec-art-pill">Accepted</span>
                </div>
                <div class="rec-art-list">
                  <span class="rec-art-row"><b>Compensation</b><i>Within the band you set</i><em>&#8377;48L</em></span>
                  <span class="rec-art-row"><b>Starts</b><i>After a 30-day notice</i><em>13 Nov</em></span>
                  <span class="rec-art-row"><b>Time to hire</b><i>From first application</i><em>19 days</em></span>
                </div>""",
         tag='Offer &middot; signed',
         lead='Nineteen days to hire.',
         note='Five days inside your average for this role, and the band held '
              'without a counter.',
         file='Offer letter.pdf'),
]

tabs, panes = [], []
for i, st in enumerate(STAGES):
    on = ' is-on' if i == 0 else ''
    tabs.append(
        '              <button class="rec-stage-tab%s" type="button" role="tab"\n'
        '                      aria-selected="%s" data-rec-stage="%s">%s%s</button>'
        % (on, 'true' if i == 0 else 'false', st['key'], icon(st['key']),
           LABEL[st['key']]))
    panes.append("""            <div class="rec-stage-pane%s" data-rec-pane="%s" role="tabpanel">
              <div class="rec-stage-text">
                <h3 class="rec-stage-h">%s</h3>
                <p class="rec-stage-p">%s</p>
              </div>
              <div class="rec-stage-art">
                <div class="rec-art-card">
%s
                </div>
                <div class="rec-art-float">
                  <div class="rec-art-float-top">
                    <span class="rec-art-float-who">%sMira read</span>
                    <span class="rec-art-float-tag">%s</span>
                  </div>
                  <b>%s</b>
                  <p>%s</p>
                  <span class="rec-art-file">%s%s</span>
                </div>
              </div>
            </div>""" % (on, st['key'], st['head'], st['foot'], st['art'],
                         SPARK, st['tag'], st['lead'], st['note'], CLIP, st['file']))

block = """        <!-- and back down into violet, the same way -->
        <section class="rec-deep">
          <div class="rec-stage-pin">
            <h2 class="rec-stage-top">Mira works at every stage,
              <span>the way you already hire.</span></h2>

            <div class="rec-stage-rail" role="tablist" aria-label="Hiring stages">
%s
            </div>
            <div class="rec-stage-ruler" aria-hidden="true">
              <span class="rec-stage-mark"></span>
            </div>

%s
          </div>
        </section>""" % ('\n'.join(tabs), '\n'.join(panes))

start = s.index('        <!-- and back down into violet, the same way -->')
end = s.index('</section>', start) + len('</section>')
s = s[:start] + block + s[end:]

CSS = """    /* ---- stages ------------------------------------------------------------ */
    /* A line, a row of tabs, a ruler that marks which one is open, and one
       wide panel: the claim on the left, the stage's own card on the right. */
    .rec-stage-pin { position:sticky; top:0; min-height:100vh;
                     width:min(1280px, 92vw); margin-inline:auto;
                     display:flex; flex-direction:column; justify-content:center;
                     padding-block:90px;
                     opacity:var(--deep-in, 0);
                     transform:translateY(calc((1 - var(--deep-in, 0)) * 34px)); }
    .rec-stage-top { margin:0; text-align:center; color:#FFFFFF;
                     font-size:clamp(22px, 1.5vw + 11px, 34px); font-weight:600;
                     line-height:1.25; letter-spacing:-0.025em; text-wrap:balance; }
    .rec-stage-top span { color:#8D83B8; }

    .rec-stage-rail { display:flex; justify-content:space-between; gap:10px;
                      margin-top:38px; }
    .rec-stage-tab { display:inline-flex; align-items:center; gap:8px; cursor:pointer;
                     font-family:inherit; font-size:14.5px; font-weight:500;
                     border:none; background:none; padding:4px 2px; color:#8D83B8;
                     transition:color .2s; }
    .rec-stage-tab svg { width:16px; height:16px; flex:none; opacity:.75; }
    .rec-stage-tab:hover { color:#D8D1F2; }
    .rec-stage-tab.is-on { color:#FFFFFF; font-weight:600; }
    .rec-stage-tab.is-on svg { opacity:1; color:#C9B8FF; }

    /* the ruler: even ticks, and one bright mark that slides to the open tab */
    .rec-stage-ruler { position:relative; height:14px; margin-top:16px;
                       background-image:repeating-linear-gradient(90deg,
                         rgba(255,255,255,.17) 0 1px, transparent 1px 12px);
                       background-size:12px 8px; background-position:left center;
                       background-repeat:repeat-x; }
    .rec-stage-mark { position:absolute; top:0; bottom:0; width:2px;
                      left:var(--mark, 4%); background:#FFFFFF; border-radius:2px;
                      transition:left .45s cubic-bezier(.22,.61,.36,1); }

    .rec-stage-pane { display:none; }
    .rec-stage-pane.is-on { display:grid;
                            grid-template-columns:minmax(0, 0.92fr) minmax(0, 1.08fr);
                            margin-top:28px; border-radius:22px; overflow:hidden;
                            background:rgba(255,255,255,.035);
                            box-shadow:inset 0 0 0 1px rgba(255,255,255,.11); }
    /* claim at the top, the line that qualifies it held at the foot */
    .rec-stage-text { display:flex; flex-direction:column; justify-content:space-between;
                      gap:40px; padding:44px 42px; }
    .rec-stage-h { margin:0; max-width:15ch; color:#FFFFFF;
                   font-size:clamp(23px, 1.5vw + 11px, 33px); font-weight:600;
                   line-height:1.2; letter-spacing:-0.025em; text-wrap:balance; }
    .rec-stage-p { margin:0; max-width:40ch; color:#A79FC8;
                   font-size:15px; line-height:1.62; }

    /* the lit surface the card sits on */
    .rec-stage-art { position:relative; padding:34px 34px 44px;
                     background:
                       radial-gradient(120% 86% at 88% -8%, rgba(190,164,255,.52), transparent 58%),
                       radial-gradient(90% 70% at 12% 110%, rgba(124,92,246,.26), transparent 62%),
                       #150C2B; }
    .rec-art-card { border-radius:13px; overflow:hidden; background:#1C1136;
                    box-shadow:0 22px 50px rgba(8,2,24,.46),
                               inset 0 0 0 1px rgba(255,255,255,.10); }
    .rec-art-head { display:flex; align-items:flex-start; justify-content:space-between;
                    gap:14px; padding:14px 16px; background:rgba(255,255,255,.05); }
    .rec-art-head b { display:block; font-size:13.5px; font-weight:600; color:#F4F1FF; }
    .rec-art-head i { display:block; margin-top:2px; font-style:normal;
                      font-size:12px; color:#9A91BE; }
    .rec-art-count { flex:none; font-size:12px; color:#C0A9FF; white-space:nowrap; }
    .rec-art-pill { flex:none; font-size:12px; font-weight:600; color:#6FE0AC;
                    background:rgba(111,224,172,.14); border-radius:100px; padding:4px 10px; }
    .rec-art-row { display:grid; grid-template-columns:1fr auto; align-items:center;
                   column-gap:12px; padding:11px 16px;
                   box-shadow:inset 0 1px 0 rgba(255,255,255,.07); }
    .rec-art-row b { font-size:13.5px; font-weight:600; color:#F4F1FF; }
    .rec-art-row i { grid-column:1; font-style:normal; font-size:12px; color:#9A91BE; }
    .rec-art-row em { grid-column:2; grid-row:1 / span 2; font-style:normal;
                      font-size:13px; font-weight:600; color:#C0A9FF; }
    .rec-art-scores { padding:6px 16px 12px; }
    .rec-art-score { display:grid; grid-template-columns:100px 1fr 32px;
                     align-items:center; gap:11px; padding:9px 0; }
    .rec-art-score i { font-style:normal; font-size:12.5px; color:#9A91BE; }
    .rec-art-score em { font-style:normal; font-size:12.5px; font-weight:600;
                        color:#F4F1FF; text-align:right; }
    .rec-bar { height:6px; border-radius:100px; background:rgba(255,255,255,.10); }
    .rec-bar span { display:block; height:100%; border-radius:100px; background:#A78BFA; }
    /* the slot tiles are shared with the chat window, so the dark reading of
       them is scoped to this card only */
    .rec-art-card .rec-slots { padding:14px; gap:7px; }
    .rec-art-card .rec-slot { box-shadow:inset 0 0 0 1px rgba(255,255,255,.12); }
    .rec-art-card .rec-slot b { font-size:12.5px; color:#F4F1FF; }
    .rec-art-card .rec-slot i { font-size:11px; color:#9A91BE; }
    .rec-art-card .rec-slot.is-pick { background:rgba(167,139,250,.18);
                                      box-shadow:inset 0 0 0 1.5px #A78BFA; }
    .rec-art-card .rec-slot.is-pick b, .rec-art-card .rec-slot.is-pick i { color:#E7DEFF; }

    /* Mira's read of the card, sitting off its corner */
    .rec-art-float { position:absolute; right:16px; bottom:18px;
                     width:min(330px, 74%); border-radius:12px; padding:13px 15px 14px;
                     background:rgba(22,13,44,.88);
                     -webkit-backdrop-filter:blur(14px); backdrop-filter:blur(14px);
                     box-shadow:0 20px 44px rgba(8,2,24,.52),
                                inset 0 0 0 1px rgba(201,184,255,.22); }
    .rec-art-float-top { display:flex; align-items:center; justify-content:space-between;
                         gap:12px; margin-bottom:9px; }
    .rec-art-float-who { display:inline-flex; align-items:center; gap:6px;
                         font-size:12.5px; font-weight:600; color:#C9B8FF; }
    .rec-art-float-who svg { width:14px; height:14px; }
    .rec-art-float-tag { font-size:11.5px; color:#8D83B8; white-space:nowrap; }
    .rec-art-float b { display:block; font-size:13.5px; font-weight:600; color:#FFFFFF; }
    .rec-art-float p { margin:5px 0 0; font-size:12.5px; line-height:1.5; color:#A79FC8; }
    .rec-art-file { display:inline-flex; align-items:center; gap:7px; margin-top:11px;
                    font-size:11.5px; color:#D5CDF0; background:rgba(255,255,255,.07);
                    border-radius:7px; padding:5px 9px;
                    box-shadow:inset 0 0 0 1px rgba(255,255,255,.10); }
    .rec-art-file svg { width:13px; height:13px; color:#C0A9FF; }

    @media (prefers-reduced-motion: reduce) {
      .rec-stage-pin { opacity:1; transform:none; }
      .rec-stage-tab, .rec-stage-mark { transition:none; }
    }
    /* the tabs scroll across, the panel stacks, the read sits under the card */
    @media (max-width:1000px) {
      .rec-deep { min-height:0; padding-block:72px; }
      .rec-stage-pin { position:static; min-height:0; padding-block:0;
                       opacity:1; transform:none; }
      .rec-stage-rail { justify-content:flex-start; gap:22px; margin-top:28px;
                        overflow-x:auto; scrollbar-width:none; }
      .rec-stage-rail::-webkit-scrollbar { display:none; }
      .rec-stage-tab { flex:none; white-space:nowrap; }
      .rec-stage-ruler { display:none; }
      .rec-stage-pane.is-on { grid-template-columns:1fr; margin-top:22px; }
      .rec-stage-text { padding:28px 24px; gap:16px; }
      .rec-stage-h, .rec-stage-p { max-width:none; }
      .rec-stage-art { padding:22px 20px 24px; }
      .rec-art-float { position:static; width:auto; margin-top:16px; }
    }

"""

start = s.index('    /* ---- stages ------')
end = s.index('    /* ---- suggestions ------')
s = s[:start] + CSS + s[end:]

# ---- the mark follows the open tab -----------------------------------------
old = """      var key = tab.getAttribute('data-rec-stage');"""
new = """      var key = tab.getAttribute('data-rec-stage');
      mark(tab);"""
assert old in s, 'rail handler changed'
s = s.replace(old, new, 1)

old = """    var panes = [].slice.call(document.querySelectorAll('[data-rec-pane]'));"""
new = """    var panes = [].slice.call(document.querySelectorAll('[data-rec-pane]'));
    var ruler = document.querySelector('.rec-stage-ruler');
    // the mark is placed from the tab's own box, so it stays right at any width
    function mark(tab) {
      if (!ruler) return;
      var r = ruler.getBoundingClientRect(), t = tab.getBoundingClientRect();
      if (!r.width) return;
      var at = (t.left + t.width / 2 - r.left) / r.width * 100;
      ruler.style.setProperty('--mark', at.toFixed(2) + '%');
    }
    function remark() {
      var on = rail.querySelector('.rec-stage-tab.is-on');
      if (on) mark(on);
    }
    remark();
    window.addEventListener('resize', remark, { passive: true });
    if (document.fonts && document.fonts.ready) { document.fonts.ready.then(remark); }"""
assert old in s, 'rail panes line changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('stages, rebuilt to the reference')
