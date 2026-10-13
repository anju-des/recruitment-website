# -*- coding: utf-8 -*-
"""The interview stage shows the call, with Mira taking the notes.

Laid out like the reference -- one large tile, two small ones, a side rail --
but the rail carries a running transcript instead of a radar chart and a
score, because what Mira does here is listen and write it down. Drawn in
markup, violet, with invented people.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

MIC = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
       'stroke-linecap="round" aria-hidden="true">'
       '<rect x="9" y="3" width="6" height="11" rx="3"/>'
       '<path d="M5 11a7 7 0 0 0 14 0M12 18v3"/></svg>')

LINES = [
    ('12:04', 'Naina', 'I’d start by mapping where people drop off, then fix '
                       'the worst step first.'),
    ('12:06', 'Arun', 'How did you measure that at Northwind?'),
    ('12:07', 'Naina', 'A weekly funnel review. Onboarding went from nine screens '
                       'to four.'),
]

lines = '\n'.join(
    """                      <span class="rec-call-line">
                        <i>%s</i>
                        <b>%s</b>
                        <em>%s</em>
                      </span>""" % l for l in LINES)

MOCK = """                <div class="rec-call">
                  <div class="rec-call-vids">
                    <div class="rec-call-vid rec-call-vid--main">
                      <span class="rec-call-av">NV</span>
                      <span class="rec-call-tag">Naina Verma</span>
                      <span class="rec-call-cap">&ldquo;&hellip;then fix the worst step first.&rdquo;</span>
                    </div>
                    <div class="rec-call-pair">
                      <div class="rec-call-vid">
                        <span class="rec-call-av rec-call-av--sm">AP</span>
                        <span class="rec-call-tag">Arun Pillai</span>
                      </div>
                      <div class="rec-call-vid rec-call-vid--you">
                        <span class="rec-call-av rec-call-av--sm">%s</span>
                        <span class="rec-call-tag">You</span>
                      </div>
                    </div>
                  </div>

                  <div class="rec-call-side">
                    <div class="rec-call-who">
                      <span class="rec-call-who-pic" aria-hidden="true">M</span>
                      <span class="rec-call-who-id">
                        <b>Mira notetaker</b>
                        <i>Final round &middot; 45 min</i>
                      </span>
                      <span class="rec-call-live">Live</span>
                    </div>
                    <div class="rec-call-lines">
%s
                    </div>
                    <div class="rec-call-note">
                      <b>Mira</b>
                      <em>Asked for a number and got one. Strong on prioritising.</em>
                    </div>
                  </div>
                </div>""" % (MIC, lines)

old = """                <!-- product image goes here, e.g.
                     <img src="stage-interview.png" alt="" loading="lazy"> -->"""
assert old in s, 'interview art slot changed'
s = s.replace(old, MOCK, 1)

CSS = """    /* the call, with the notetaker rail beside it */
    .rec-call { position:relative; z-index:1; width:100%; display:grid;
                grid-template-columns:minmax(0, 1fr) 224px; gap:9px; padding:9px;
                border-radius:15px; background:#FFFFFF;
                box-shadow:0 22px 50px rgba(48,28,104,.20),
                           inset 0 0 0 1px rgba(25,18,49,.08); }
    .rec-call-vids { display:grid; grid-template-rows:minmax(0, 1fr) auto; gap:9px; }
    .rec-call-pair { display:grid; grid-template-columns:1fr 1fr; gap:9px; }
    /* no photographs: each tile is a lit surface with the person's initials,
       the way a call looks before anyone turns a camera on */
    .rec-call-vid { position:relative; aspect-ratio:16 / 10; border-radius:10px;
                    overflow:hidden; display:grid; place-items:center;
                    background:linear-gradient(145deg, #40288C 0%, #6B46E0 52%,
                                               #9D7BF5 100%); }
    .rec-call-vid--main { aspect-ratio:16 / 9;
                          background:linear-gradient(145deg, #2E1B6B 0%, #5B3DD4 48%,
                                                     #A98BFF 100%); }
    .rec-call-vid--you { background:linear-gradient(145deg, #4B2F8F 0%, #7C5CF6 60%,
                                                    #C0A9FF 100%); }
    .rec-call-av { width:46px; height:46px; border-radius:50%; display:grid;
                   place-items:center; font-size:14px; font-weight:600; color:#FFFFFF;
                   background:rgba(255,255,255,.18);
                   box-shadow:inset 0 0 0 1px rgba(255,255,255,.34); }
    .rec-call-av--sm { width:30px; height:30px; font-size:11px; }
    .rec-call-av--sm svg { width:13px; height:13px; }
    .rec-call-tag { position:absolute; left:8px; bottom:8px; font-size:10.5px;
                    font-weight:500; color:#FFFFFF; background:rgba(16,8,38,.46);
                    -webkit-backdrop-filter:blur(6px); backdrop-filter:blur(6px);
                    border-radius:6px; padding:3px 8px; }
    .rec-call-cap { position:absolute; left:50%; translate:-50% 0; bottom:9px;
                    max-width:74%; text-align:center; font-size:11px; color:#FFFFFF;
                    background:rgba(16,8,38,.56);
                    -webkit-backdrop-filter:blur(6px); backdrop-filter:blur(6px);
                    border-radius:7px; padding:5px 10px; }

    .rec-call-side { display:flex; flex-direction:column; gap:9px; min-width:0; }
    .rec-call-who { display:flex; align-items:center; gap:9px; border-radius:10px;
                    padding:9px 10px; background:#F4F1FF;
                    box-shadow:inset 0 0 0 1px rgba(124,92,246,.16); }
    .rec-call-who-pic { flex:none; width:26px; height:26px; border-radius:50%;
                        display:grid; place-items:center; font-size:11px;
                        font-weight:600; color:#FFFFFF;
                        background:linear-gradient(140deg,#7C5CF6,#A98BFF); }
    .rec-call-who-id { flex:1; min-width:0; }
    .rec-call-who-id b { display:block; font-size:11.5px; font-weight:600;
                         color:#191231; }
    .rec-call-who-id i { display:block; font-style:normal; font-size:10px;
                         color:#8A83A6; }
    .rec-call-live { flex:none; display:inline-flex; align-items:center; gap:5px;
                     font-size:10px; font-weight:600; color:#5B3DD4; }
    .rec-call-live::before { content:""; width:6px; height:6px; border-radius:50%;
                             background:#7C5CF6; }

    .rec-call-lines { flex:1 1 auto; min-height:0; display:flex;
                      flex-direction:column; gap:10px; border-radius:10px;
                      padding:11px 11px 12px; background:#F7F5FF;
                      box-shadow:inset 0 0 0 1px rgba(25,18,49,.07); }
    .rec-call-line { display:block; }
    .rec-call-line i { font-style:normal; font-size:9.5px; color:#A49DBC;
                       font-variant-numeric:tabular-nums; }
    .rec-call-line b { margin-left:6px; font-size:10.5px; font-weight:600;
                       color:#5B3DD4; }
    .rec-call-line em { display:block; margin-top:2px; font-style:normal;
                        font-size:11px; line-height:1.45; color:#4E4870; }
    /* what Mira adds on top of the record, rather than the record itself */
    .rec-call-note { border-radius:10px; padding:9px 11px;
                     background:linear-gradient(135deg, #EFE9FF, #F7EFFB);
                     box-shadow:inset 0 0 0 1px rgba(124,92,246,.22); }
    .rec-call-note b { display:block; font-size:10px; font-weight:600;
                       color:#5B3DD4; letter-spacing:.02em; }
    .rec-call-note em { display:block; margin-top:3px; font-style:normal;
                        font-size:11px; line-height:1.45; color:#3B3263; }

"""
anchor = "    @media (prefers-reduced-motion: reduce) {\n      .rec-stage-pin { opacity:1; transform:none; }"
assert anchor in s, 'stage reduced-motion block changed'
s = s.replace(anchor, CSS + anchor, 1)

old = """      .rec-app-tags { display:none; }"""
new = """      .rec-app-tags { display:none; }
      .rec-call { grid-template-columns:1fr; }
      .rec-call-pair { display:none; }"""
assert old in s, 'responsive art rule changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('the call, with Mira listening')
