# -*- coding: utf-8 -*-
"""Fill the offer card's empty half with the case for the hire.

A short summary and the run of dates it took, which is the one place on the
page where all four stages appear at once -- applied, shortlisted, final
round, offer -- so the panel closes the story the other three told.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

STEPS = [('Applied', '24 Sep'), ('Shortlisted', '25 Sep'),
         ('Final round', '10 Oct'), ('Offer out', '13 Oct')]
steps = '\n'.join("""                    <span class="rec-offer-step">
                      <b>%s</b>
                      <i>%s</i>
                    </span>""" % st for st in STEPS)

BLOCK = """
                  <div class="rec-offer-sum">
                    <b>Why Naina</b>
                    <p>First on the ranking, and the only candidate the panel
                      agreed on without a second conversation. The band held,
                      so the offer went out the same afternoon.</p>
                  </div>

                  <div class="rec-offer-track">
%s
                  </div>
""" % steps

old = """                  <div class="rec-offer-tags">"""
start = s.index(old)
end = s.index('</div>\n', start) + len('</div>\n')
s = s[:end] + BLOCK + s[end:]

CSS = """    /* the case for the hire, and the run of dates behind it */
    .rec-offer-sum { flex:none; border-radius:11px; padding:11px 13px;
                     background:#FBFAFF;
                     box-shadow:inset 0 0 0 1px rgba(25,18,49,.08); }
    .rec-offer-sum b { display:block; font-size:11.5px; font-weight:600;
                       color:#5B3DD4; }
    .rec-offer-sum p { margin:4px 0 0; font-size:11.5px; line-height:1.5;
                       color:#4E4870; }

    .rec-offer-track { flex:none; display:grid; grid-template-columns:repeat(4, 1fr);
                       padding-top:2px; }
    .rec-offer-step { position:relative; padding-top:15px; }
    /* the rail runs from each dot to the next, and stops at the last */
    .rec-offer-step::before { content:""; position:absolute; top:4px; left:4px;
                              right:0; height:2px; background:#E6DEFF; }
    .rec-offer-step:last-child::before { display:none; }
    .rec-offer-step::after { content:""; position:absolute; top:0; left:0;
                             width:10px; height:10px; border-radius:50%;
                             background:#7C5CF6;
                             box-shadow:0 0 0 3px rgba(124,92,246,.16); }
    .rec-offer-step b { display:block; font-size:11px; font-weight:600;
                        color:#191231; }
    .rec-offer-step i { display:block; margin-top:1px; font-style:normal;
                        font-size:10.5px; color:#8A83A6; }

"""
anchor = "    /* the action floats off the card, which is where the eye ends up */"
assert anchor in s, 'offer float comment changed'
s = s.replace(anchor, CSS + anchor, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('summary and timeline added')
