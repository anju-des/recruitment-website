# -*- coding: utf-8 -*-
"""The offer stage: the candidate's profile, hired, with the offer to send.

Same person as the three stages before it, so the panels read as one hire
rather than four stock screens. The send action floats off the card's corner
the way the reference's primary action does.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()


def ic(body, fill=False):
    if fill:
        return ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">%s'
                '</svg>' % body)
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
            'aria-hidden="true">%s</svg>' % body)


CHECK = ic('<path d="M20 6.5L9.5 17 4 11.5"/>')
TICK = ic('<path d="M20 6.5L9.5 17 4 11.5"/>')
SPARK = ic('<path d="M12 2.5l1.9 5.3 5.3 1.9-5.3 1.9L12 16.9l-1.9-5.3L4.8 9.7l5.3-1.9z"/>',
           fill=True)
SEND = ic('<path d="M4 12h15"/><path d="M13 6l6 6-6 6"/>')

FACTS = [('Compensation', '&#8377;48L'), ('Starts', '13 Nov'),
         ('Notice served', '30 days')]
facts = '\n'.join("""                    <span class="rec-offer-fact">
                      <i>%s</i>
                      <b>%s</b>
                    </span>""" % f for f in FACTS)

TAGS = ['Within your band', 'Panel aligned', 'References cleared']
tags = ''.join('<em>%s%s</em>' % (TICK, t) for t in TAGS)

MOCK = """                <div class="rec-offer">
                  <div class="rec-offer-head">
                    <img class="rec-offer-pic" src="face-candidate.png" alt=""
                         width="693" height="388" loading="lazy" decoding="async">
                    <span class="rec-offer-id">
                      <b>Naina Verma</b>
                      <i>Product Designer &middot; 4 yrs &middot; Bengaluru</i>
                      <u>Shortlisted from the careers site &middot; 19 days ago</u>
                    </span>
                    <span class="rec-offer-badge">%s Hired</span>
                  </div>

                  <div class="rec-offer-facts">
%s
                  </div>

                  <div class="rec-offer-tags">%s</div>

                  <div class="rec-offer-float">
                    <span class="rec-offer-float-i" aria-hidden="true">%s</span>
                    <span class="rec-offer-float-id">
                      <b>Send the offer</b>
                      <i>Drafted from the band you set</i>
                    </span>
                    <span class="rec-offer-go">Send %s</span>
                  </div>
                </div>""" % (CHECK, facts, tags, SPARK, SEND)

old = """                <!-- product image goes here, e.g.
                     <img src="stage-offer.png" alt="" loading="lazy"> -->"""
assert old in s, 'offer art slot changed'
s = s.replace(old, MOCK, 1)

CSS = """    /* the hire: a profile, the terms, and the one action left to take */
    .rec-offer { position:relative; z-index:1; width:100%; height:100%;
                 display:flex; flex-direction:column; gap:14px;
                 padding:18px 20px 92px; border-radius:14px; background:#FFFFFF;
                 box-shadow:0 22px 50px rgba(48,28,104,.20),
                            inset 0 0 0 1px rgba(25,18,49,.08); }
    .rec-offer-head { flex:none; display:flex; align-items:flex-start; gap:14px; }
    .rec-offer-pic { flex:none; width:64px; height:64px; border-radius:12px;
                     object-fit:cover; object-position:50% 22%;
                     box-shadow:inset 0 0 0 1px rgba(25,18,49,.10); }
    .rec-offer-id { flex:1; min-width:0; }
    .rec-offer-id b { display:block; font-size:16px; font-weight:600;
                      color:#191231; letter-spacing:-0.015em; }
    .rec-offer-id i { display:block; margin-top:3px; font-style:normal;
                      font-size:12px; color:#6E6690; }
    .rec-offer-id u { display:block; margin-top:5px; text-decoration:none;
                      font-size:11px; color:#A49DBC; }
    .rec-offer-badge { flex:none; display:inline-flex; align-items:center; gap:5px;
                       font-size:11.5px; font-weight:600; color:#027A48;
                       background:#E6F9F0; border-radius:100px; padding:5px 11px;
                       box-shadow:inset 0 0 0 1px rgba(2,122,72,.18); }
    .rec-offer-badge svg { width:12px; height:12px; }

    .rec-offer-facts { flex:none; display:grid; grid-template-columns:repeat(3, 1fr);
                       gap:1px; border-radius:11px; overflow:hidden;
                       background:rgba(25,18,49,.09);
                       box-shadow:inset 0 0 0 1px rgba(25,18,49,.09); }
    .rec-offer-fact { padding:10px 13px; background:#FBFAFF; }
    .rec-offer-fact i { display:block; font-style:normal; font-size:10.5px;
                        color:#8A83A6; }
    .rec-offer-fact b { display:block; margin-top:3px; font-size:14px;
                        font-weight:600; color:#191231;
                        font-variant-numeric:tabular-nums; }

    .rec-offer-tags { flex:none; display:flex; flex-wrap:wrap; gap:6px; }
    .rec-offer-tags em { display:inline-flex; align-items:center; gap:5px;
                         font-style:normal; font-size:11px; color:#4C1D95;
                         background:#F1EBFF; border-radius:100px; padding:5px 11px; }
    .rec-offer-tags svg { width:11px; height:11px; color:#7C5CF6; }

    /* the action floats off the card, which is where the eye ends up */
    .rec-offer-float { position:absolute; z-index:2; right:14px; bottom:14px;
                       left:auto; display:flex; align-items:center; gap:11px;
                       border-radius:12px; padding:10px 11px 10px 13px;
                       background:#FFFFFF;
                       box-shadow:0 18px 38px rgba(48,28,104,.26),
                                  inset 0 0 0 1px rgba(124,92,246,.26); }
    .rec-offer-float-i { flex:none; width:26px; height:26px; border-radius:8px;
                         display:grid; place-items:center; color:#FFFFFF;
                         background:linear-gradient(140deg,#7C5CF6,#A98BFF); }
    .rec-offer-float-i svg { width:14px; height:14px; }
    .rec-offer-float-id b { display:block; font-size:12.5px; font-weight:600;
                            color:#191231; }
    .rec-offer-float-id i { display:block; margin-top:2px; font-style:normal;
                            font-size:10.5px; color:#8A83A6; }
    .rec-offer-go { flex:none; display:inline-flex; align-items:center; gap:5px;
                    font-size:11.5px; font-weight:600; color:#FFFFFF;
                    background:#7C5CF6; border-radius:9px; padding:7px 12px; }
    .rec-offer-go svg { width:13px; height:13px; }

"""
anchor = "    @media (prefers-reduced-motion: reduce) {\n      .rec-stage-pin { opacity:1; transform:none; }"
assert anchor in s, 'stage reduced-motion block changed'
s = s.replace(anchor, CSS + anchor, 1)

old = """      .rec-rank-row { grid-template-columns:auto auto minmax(0, 1fr); }"""
new = """      .rec-offer { padding-bottom:18px; }
      .rec-offer-float { position:static; margin-top:12px; }
      .rec-rank-row { grid-template-columns:auto auto minmax(0, 1fr); }"""
assert old in s, 'responsive rank rule changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('offer profile built')
