# -*- coding: utf-8 -*-
"""The scorecard stage shows the ranking and the score, and nothing else.

The reference carries four bullets of reasoning per candidate; at this size
they would be grey mush, and the point of the panel is the order and the
number. Each row keeps its verdict line and its percentage, and the rows are
sorted by it.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

SPARK = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
         '<path d="M12 2.5l1.9 5.3 5.3 1.9-5.3 1.9L12 16.9l-1.9-5.3L4.8 9.7l5.3-1.9z"/>'
         '</svg>')

PEOPLE = [
    ('1', 'NV', 'Naina Verma', 'Product Designer &middot; 4 yrs &middot; Bengaluru',
     'Strong match, excellent fit', '92', 'top'),
    ('2', 'KS', 'Kabir Shah', 'Senior Product Designer &middot; 6 yrs &middot; Pune',
     'Strong match, minor gaps', '78', ''),
    ('3', 'IS', 'Ira Sundaram', 'Product Designer &middot; 3 yrs &middot; Remote',
     'Promising, short on depth', '64', 'low'),
]

rows = []
for no, initials, name, meta, verdict, score, tone in PEOPLE:
    cls = ' rec-rank-row--' + tone if tone else ''
    rows.append("""                  <div class="rec-rank-row%s">
                    <span class="rec-rank-no">%s</span>
                    <span class="rec-rank-pic" aria-hidden="true">%s</span>
                    <span class="rec-rank-main">
                      <b>%s</b>
                      <i>%s</i>
                    </span>
                    <span class="rec-rank-verdict">
                      <em>%s</em>
                      <b>%s<sup>%%</sup></b>
                    </span>
                  </div>""" % (cls, no, initials, name, meta, verdict, score))

MOCK = """                <div class="rec-rank">
                  <div class="rec-rank-top">
                    <span class="rec-rank-mira">%s Mira &middot; ranked by fit</span>
                    <span class="rec-rank-count">3 of 38</span>
                  </div>
%s
                </div>""" % (SPARK, '\n'.join(rows))

old = """                <!-- product image goes here, e.g.
                     <img src="stage-scorecard.png" alt="" loading="lazy"> -->"""
assert old in s, 'scorecard art slot changed'
s = s.replace(old, MOCK, 1)

CSS = """    /* the ranking: who is in front, and by how much */
    .rec-rank { position:relative; z-index:1; width:100%; height:100%;
                display:flex; flex-direction:column; gap:9px; }
    .rec-rank-top { flex:none; display:flex; align-items:center;
                    justify-content:space-between; gap:12px; padding:0 2px 1px; }
    .rec-rank-mira { display:inline-flex; align-items:center; gap:6px;
                     font-size:11.5px; font-weight:600; color:#5B3DD4; }
    .rec-rank-mira svg { width:13px; height:13px; }
    .rec-rank-count { font-size:11px; color:#6E6690; }

    .rec-rank-row { flex:1 1 0; display:grid;
                    grid-template-columns:auto auto minmax(0, 1fr) 178px;
                    align-items:stretch; gap:0; border-radius:12px; overflow:hidden;
                    background:#FFFFFF;
                    box-shadow:0 14px 32px rgba(48,28,104,.14),
                               inset 0 0 0 1px rgba(25,18,49,.08); }
    .rec-rank-no { align-self:center; padding-left:16px; font-size:12px;
                   font-weight:600; color:#A49DBC;
                   font-variant-numeric:tabular-nums; }
    .rec-rank-pic { align-self:center; width:30px; height:30px; margin-left:11px;
                    border-radius:9px; display:grid; place-items:center;
                    font-size:11.5px; font-weight:600; color:#4C1D95;
                    background:linear-gradient(140deg,#EDE7FF,#D7C9FF); }
    .rec-rank-main { align-self:center; min-width:0; padding:12px 14px; }
    .rec-rank-main b { display:block; font-size:13px; font-weight:600;
                       color:#191231; }
    .rec-rank-main i { display:block; margin-top:3px; font-style:normal;
                       font-size:11px; color:#8A83A6; }
    /* the verdict and the number, on their own ground */
    .rec-rank-verdict { display:flex; flex-direction:column; justify-content:center;
                        gap:5px; padding:12px 14px; background:#F4F0FF;
                        box-shadow:inset 1px 0 0 rgba(124,92,246,.18); }
    .rec-rank-verdict em { font-style:normal; font-size:10px; font-weight:600;
                           line-height:1.35; letter-spacing:.03em;
                           text-transform:uppercase; color:#5B3DD4; }
    .rec-rank-verdict b { font-size:21px; font-weight:600; line-height:1;
                          color:#4C1D95; letter-spacing:-0.02em;
                          font-variant-numeric:tabular-nums; }
    .rec-rank-verdict sup { font-size:11px; font-weight:600; top:-0.55em; }
    /* the leader reads a shade warmer, the tail a shade quieter */
    .rec-rank-row--top .rec-rank-verdict { background:#EDE6FF; }
    .rec-rank-row--low .rec-rank-verdict { background:#F7F5FC; }
    .rec-rank-row--low .rec-rank-verdict em,
    .rec-rank-row--low .rec-rank-verdict b { color:#6E6690; }

"""
anchor = "    @media (prefers-reduced-motion: reduce) {\n      .rec-stage-pin { opacity:1; transform:none; }"
assert anchor in s, 'stage reduced-motion block changed'
s = s.replace(anchor, CSS + anchor, 1)

old = """      .rec-call-pair { display:none; }"""
new = """      .rec-call-pair { display:none; }
      .rec-rank-row { grid-template-columns:auto auto minmax(0, 1fr); }
      .rec-rank-verdict { grid-column:1 / -1; flex-direction:row;
                          align-items:center; justify-content:space-between;
                          box-shadow:inset 0 1px 0 rgba(124,92,246,.18); }"""
assert old in s, 'responsive call rule changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('ranking and score')
