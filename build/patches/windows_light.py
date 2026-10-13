# -*- coding: utf-8 -*-
"""The windows go white.

Every surface and every piece of type inside them flips: white cards, dark
text, grey secondaries, with the violet accents kept. The logo stops being
inverted, since it is a dark mark and now sits on white.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

PAIRS = [
    # the card itself
    ("""               /* a solid surface, not glass: the sky under these windows ends
                  up light, and white glass on lavender is invisible */
               background:#141829;""",
     """               /* white cards on the lavender sky */
               background:#FFFFFF;"""),
    ("""               box-shadow:0 24px 80px rgba(167,139,250,.22), 0 0 46px rgba(139,92,246,.14),
                          0 30px 70px rgba(0,0,0,.40), inset 0 0 0 1px rgba(255,255,255,.08); }""",
     """               box-shadow:0 24px 70px rgba(91,61,168,.22), 0 2px 10px rgba(32,22,66,.10),
                          inset 0 0 0 1px rgba(32,22,66,.07); }"""),
    ("    .rec-win-bar { display:flex; align-items:center; justify-content:space-between;\n"
     "                   padding:14px 18px; background:rgba(255,255,255,0.025); }",
     "    .rec-win-bar { display:flex; align-items:center; justify-content:space-between;\n"
     "                   padding:14px 18px; background:#F7F8FA;\n"
     "                   box-shadow:inset 0 -1px 0 rgba(32,22,66,.07); }"),
    ("""    /* the logo is a dark mark, so it is inverted to sit on the dark bar */
    .rec-win-logo { height:18px; width:auto; display:block;
                    filter:invert(1) brightness(1.7); }""",
     """    /* a dark mark on a white bar: no inversion needed */
    .rec-win-logo { height:18px; width:auto; display:block; }"""),
    ("    .rec-win-dots { display:inline-flex; align-items:center; gap:14px; color:#6B7488; }",
     "    .rec-win-dots { display:inline-flex; align-items:center; gap:14px; color:#9AA2B2; }"),

    # the thread
    ("""    .rec-turn--you { align-self:flex-end; background:rgba(255,255,255,0.10); color:#F2F3F8;
                     border-bottom-right-radius:5px; }""",
     """    .rec-turn--you { align-self:flex-end; background:#EEF0F4; color:#222733;
                     border-bottom-right-radius:5px; }"""),
    ("""    .rec-turn--mira { align-self:flex-start; background:rgba(139,92,246,0.22); color:#EDEAFB;
                      border-bottom-left-radius:5px; }""",
     """    .rec-turn--mira { align-self:flex-start; background:#EFE9FF; color:#2E2358;
                      border-bottom-left-radius:5px; }"""),
    ("""    .rec-turn--typing { align-self:flex-start; display:flex; gap:5px; padding:14px 16px;
                        background:rgba(255,255,255,0.07); border-bottom-left-radius:5px; }""",
     """    .rec-turn--typing { align-self:flex-start; display:flex; gap:5px; padding:14px 16px;
                        background:#EEF0F4; border-bottom-left-radius:5px; }"""),
    ("    .rec-dot { width:6px; height:6px; border-radius:50%; background:#A8AFC2;",
     "    .rec-dot { width:6px; height:6px; border-radius:50%; background:#9AA2B2;"),
    ("""    .rec-turn--meta { display:flex; align-items:center; gap:9px; font-size:13.5px;
                      color:#8E97AE; }
    .rec-turn--meta svg { width:15px; height:15px; color:#A78BFA; }
    .rec-turn--say { font-size:14.5px; line-height:1.55; color:#E8EAF2; }""",
     """    .rec-turn--meta { display:flex; align-items:center; gap:9px; font-size:13.5px;
                      color:#6B7588; }
    .rec-turn--meta svg { width:15px; height:15px; color:#7C5CF6; }
    .rec-turn--say { font-size:14.5px; line-height:1.55; color:#222733; }"""),
    ("""    .rec-turn--card { border-radius:12px; overflow:hidden;
                      box-shadow:inset 0 0 0 1px rgba(255,255,255,.08); }""",
     """    .rec-turn--card { border-radius:12px; overflow:hidden;
                      box-shadow:inset 0 0 0 1px rgba(32,22,66,.10); }"""),
    ("""                     gap:16px; padding:14px 16px; background:rgba(255,255,255,.04); }
    .rec-card-head b { display:block; font-size:14.5px; font-weight:600; color:#F2F3F8; }
    .rec-card-head i { display:block; margin-top:2px; font-style:normal; font-size:12.5px;
                       color:#8E97AE; }
    .rec-card-count { flex:none; font-size:12.5px; color:#A78BFA; }""",
     """                     gap:16px; padding:14px 16px; background:#F7F8FA; }
    .rec-card-head b { display:block; font-size:14.5px; font-weight:600; color:#222733; }
    .rec-card-head i { display:block; margin-top:2px; font-style:normal; font-size:12.5px;
                       color:#6B7588; }
    .rec-card-count { flex:none; font-size:12.5px; color:#7C5CF6; }"""),
    ("""               gap:14px; padding:11px 16px;
               box-shadow:inset 0 1px 0 rgba(255,255,255,.06); }
    .rec-row-k { font-size:13px; color:#8E97AE; }
    .rec-row-v { font-size:13.5px; font-weight:600; color:#F2F3F8; }
    .rec-row-src { display:inline-flex; align-items:center; gap:7px; font-size:12.5px;
                   color:#9AA3B8; white-space:nowrap; }""",
     """               gap:14px; padding:11px 16px;
               box-shadow:inset 0 1px 0 rgba(32,22,66,.08); }
    .rec-row-k { font-size:13px; color:#6B7588; }
    .rec-row-v { font-size:13.5px; font-weight:600; color:#222733; }
    .rec-row-src { display:inline-flex; align-items:center; gap:7px; font-size:12.5px;
                   color:#6B7588; white-space:nowrap; }"""),
    ("""    .rec-turn--chips button { font-family:inherit; font-size:13px; font-weight:500;
                              color:#E8EAF2; background:rgba(255,255,255,.07);
                              border:none; border-radius:8px; padding:8px 13px;
                              cursor:pointer; transition:background .12s; }
    .rec-turn--chips button:hover { background:rgba(255,255,255,.13); }""",
     """    .rec-turn--chips button { font-family:inherit; font-size:13px; font-weight:500;
                              color:#363D4D; background:#F1F2F6;
                              border:none; border-radius:8px; padding:8px 13px;
                              cursor:pointer; transition:background .12s; }
    .rec-turn--chips button:hover { background:#E4E7EE; }"""),

    # the composer
    ("""    .rec-ask { margin:0 14px 14px; padding:12px 14px 10px; border-radius:12px;
               background:rgba(255,255,255,0.05); }
    .rec-ask-hint { font-size:14px; color:#7D869B; }""",
     """    .rec-ask { margin:0 14px 14px; padding:12px 14px 10px; border-radius:12px;
               background:#F4F5F8; }
    .rec-ask-hint { font-size:14px; color:#9AA2B2; }"""),
    ("""    .rec-ask-tools { display:inline-flex; align-items:center; gap:12px; color:#7D869B;""",
     """    .rec-ask-tools { display:inline-flex; align-items:center; gap:12px; color:#6B7588;"""),

    # the two side windows
    ("""    .rec-side-k { font-size:12px; font-weight:600; letter-spacing:.04em;
                  text-transform:uppercase; color:#A78BFA; }
    .rec-side-h { margin-top:8px; font-size:15px; font-weight:600; line-height:1.4;
                  color:#F2F3F8; }
    .rec-side-t { margin-top:4px; font-size:13.5px; color:#9AA3B8; }""",
     """    .rec-side-k { font-size:12px; font-weight:600; letter-spacing:.04em;
                  text-transform:uppercase; color:#7C5CF6; }
    .rec-side-h { margin-top:8px; font-size:15px; font-weight:600; line-height:1.4;
                  color:#222733; }
    .rec-side-t { margin-top:4px; font-size:13.5px; color:#6B7588; }"""),
    ("""                    padding-top:12px; font-size:13px; color:#8E97AE;
                    box-shadow:inset 0 1px 0 rgba(255,255,255,.07); }
    .rec-side-who b { font-weight:600; color:#E8EAF2; }""",
     """                    padding-top:12px; font-size:13px; color:#6B7588;
                    box-shadow:inset 0 1px 0 rgba(32,22,66,.08); }
    .rec-side-who b { font-weight:600; color:#222733; }"""),
    ("""    .rec-side-stat b { font-size:22px; font-weight:600; color:#F2F3F8; }
    .rec-side-stat span { font-size:13px; color:#8E97AE; }""",
     """    .rec-side-stat b { font-size:22px; font-weight:600; color:#222733; }
    .rec-side-stat span { font-size:13px; color:#6B7588; }"""),
    ("""                    font-weight:600; color:#E8EAF2; background:rgba(255,255,255,.09);
                    cursor:pointer; transition:background .12s; }
    .rec-side-btn:hover { background:rgba(255,255,255,.15); }""",
     """                    font-weight:600; color:#222733; background:#F1F2F6;
                    cursor:pointer; transition:background .12s; }
    .rec-side-btn:hover { background:#E4E7EE; }"""),
]

for old, new in PAIRS:
    assert old in s, 'rule not found: ' + old.strip().split('\n')[0][:60]
    s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('windows are white now')
