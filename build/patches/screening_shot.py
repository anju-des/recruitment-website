# -*- coding: utf-8 -*-
"""The screening stage shows the applicants list it is talking about.

Built as markup rather than a screenshot so it stays sharp and themeable,
tightened to three rows at the size the panel actually gives it. Every name,
company and place is invented -- nothing from the real pipeline.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

VET = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
       'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
       '<path d="M12 3l7 3v5.5c0 4-3 7.5-7 8.5-4-1-7-4.5-7-8.5V6z"/>'
       '<path d="M9.2 12.2l2 2 3.6-4"/></svg>')
SPARK = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
         '<path d="M12 2.5l1.9 5.3 5.3 1.9-5.3 1.9L12 16.9l-1.9-5.3L4.8 9.7l5.3-1.9z"/>'
         '</svg>')
DOTS = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
        '<circle cx="12" cy="5" r="1.6"/><circle cx="12" cy="12" r="1.6"/>'
        '<circle cx="12" cy="19" r="1.6"/></svg>')


def row(initial, company, when, name, title, yrs, place, tags, done=False, vetted=False):
    chips = ''.join('<em>%s</em>' % t for t in tags)
    act = ('<span class="rec-app-act rec-app-act--done">Shortlisted</span>'
           if done else '<span class="rec-app-act">Shortlist</span>')
    vet = ('<span class="rec-app-vet">%s Wisemonk vetted</span>' % VET) if vetted else ''
    return """                  <div class="rec-app-row">
                    <span class="rec-app-pic" aria-hidden="true">%s</span>
                    <span class="rec-app-main">
                      <i class="rec-app-meta">%s &middot; %s</i>
                      <b>%s &mdash; %s, %s</b>%s
                      <i class="rec-app-place">%s</i>
                      <span class="rec-app-tags">%s</span>
                    </span>
                    %s
                  </div>""" % (initial, company, when, name, title, yrs, vet, place,
                               chips, act)


MOCK = """                <div class="rec-app">
                  <div class="rec-app-top">
                    <span>
                      <b>Product designer</b>
                      <i>Full-time &middot; posted 12 October</i>
                    </span>
                    <span class="rec-app-dots" aria-hidden="true">%s</span>
                  </div>
                  <div class="rec-app-tabs">
                    <span class="rec-app-tab is-on">Applicants</span>
                    <span class="rec-app-tab">Pipeline</span>
                    <span class="rec-app-tab">Hired</span>
                    <span class="rec-app-mira">%s Mira AI</span>
                  </div>
%s
%s
%s
                </div>""" % (
    DOTS, SPARK,
    row('N', 'Northwind Labs (current)', '4 days ago',
        'Naina Verma', 'Product Designer', '4 yrs', 'Bengaluru',
        ['Design systems', 'Figma', 'Prototyping'], done=True, vetted=True),
    row('K', 'Marigold Health (previous)', '9 days ago',
        'Kabir Shah', 'Senior Product Designer', '6 yrs', 'Pune',
        ['B2B SaaS', 'Design tokens', 'User research']),
    row('I', 'Palladio Studio (current)', 'a month ago',
        'Ira Sundaram', 'Product Designer', '3 yrs', 'Remote &middot; India',
        ['Figma', 'Interaction', 'Motion']),
)

old = """                <!-- product image goes here, e.g.
                     <img src="stage-screening.png" alt="" loading="lazy"> -->"""
assert old in s, 'screening art slot changed'
s = s.replace(old, MOCK, 1)

CSS = """    /* the applicants list, drawn rather than screenshotted so it stays sharp */
    .rec-app { position:relative; z-index:1; width:100%; border-radius:14px;
               overflow:hidden; background:#FFFFFF;
               box-shadow:0 22px 50px rgba(48,28,104,.20),
                          inset 0 0 0 1px rgba(25,18,49,.08); }
    .rec-app-top { display:flex; align-items:flex-start; justify-content:space-between;
                   gap:12px; padding:14px 16px 10px; }
    .rec-app-top b { display:block; font-size:15px; font-weight:600; color:#191231;
                     letter-spacing:-0.015em; }
    .rec-app-top i { display:block; margin-top:3px; font-style:normal; font-size:11.5px;
                     color:#8A83A6; }
    .rec-app-dots { flex:none; color:#A49DBC; }
    .rec-app-dots svg { width:15px; height:15px; display:block; }
    .rec-app-tabs { display:flex; align-items:center; gap:18px; padding:0 16px;
                    box-shadow:inset 0 -1px 0 rgba(25,18,49,.09); }
    .rec-app-tab { padding:7px 0 9px; font-size:12px; color:#8A83A6; }
    .rec-app-tab.is-on { color:#191231; font-weight:600;
                         box-shadow:inset 0 -2px 0 #191231; }
    .rec-app-mira { margin-left:auto; display:inline-flex; align-items:center; gap:5px;
                    font-size:11.5px; font-weight:600; color:#5B3DD4;
                    background:#EFE9FF; border-radius:100px; padding:4px 10px; }
    .rec-app-mira svg { width:12px; height:12px; }

    .rec-app-row { display:grid; grid-template-columns:auto minmax(0, 1fr) auto;
                   gap:12px; align-items:start; padding:12px 16px;
                   box-shadow:inset 0 -1px 0 rgba(25,18,49,.07); }
    .rec-app-row:last-child { box-shadow:none; }
    .rec-app-pic { flex:none; width:30px; height:30px; border-radius:9px;
                   display:grid; place-items:center; font-size:12px; font-weight:600;
                   color:#4C1D95; background:linear-gradient(140deg,#EDE7FF,#D7C9FF); }
    .rec-app-meta { display:block; font-style:normal; font-size:11px; color:#8A83A6; }
    /* the designation only -- never the skills-and-years tail */
    .rec-app-main b { display:inline; font-size:13px; font-weight:600; color:#191231; }
    .rec-app-place { display:block; margin-top:3px; font-style:normal; font-size:11px;
                     color:#8A83A6; }
    .rec-app-vet { display:inline-flex; align-items:center; gap:4px; margin-left:7px;
                   font-size:10.5px; font-weight:600; color:#5B3DD4;
                   background:#EFE9FF; border-radius:100px; padding:2px 7px; }
    .rec-app-vet svg { width:11px; height:11px; }
    .rec-app-tags { display:flex; flex-wrap:wrap; gap:5px; margin-top:8px; }
    .rec-app-tags em { font-style:normal; font-size:10.5px; color:#4E4870;
                       border-radius:100px; padding:3px 9px;
                       box-shadow:inset 0 0 0 1px rgba(25,18,49,.13); }
    .rec-app-act { flex:none; font-size:11.5px; font-weight:600; color:#FFFFFF;
                   background:#7C5CF6; border-radius:8px; padding:7px 13px;
                   white-space:nowrap; }
    .rec-app-act--done { color:#027A48; background:#E6F9F0;
                         box-shadow:inset 0 0 0 1px rgba(2,122,72,.16); }

"""
anchor = "    @media (prefers-reduced-motion: reduce) {\n      .rec-stage-pin { opacity:1; transform:none; }"
assert anchor in s, 'stage reduced-motion block changed'
s = s.replace(anchor, CSS + anchor, 1)

old = """      .rec-stage-art { padding:22px 20px 24px; min-height:220px; }"""
new = """      .rec-stage-art { padding:22px 20px 24px; min-height:0; }
      .rec-app-tags { display:none; }"""
assert old in s, 'responsive art rule changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('screening shows the list')
