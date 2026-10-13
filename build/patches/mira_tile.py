# -*- coding: utf-8 -*-
"""The third tile is Mira sitting in the call, not you.

It carries the wordmark instead of a muted-mic glyph and is labelled Mira,
which is also what the rail beside it says. The photo rules had to learn to
ignore this one image, or the logo would have been stretched to cover the
tile like a camera feed.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# ---- the tile ---------------------------------------------------------------
start = s.index('<div class="rec-call-vid rec-call-vid--you">')
end = s.index('</div>', s.index('rec-call-tag">You</span>', start)) + len('</div>')
old = s[start:end]
assert 'rec-call-av--sm' in old, 'mira tile markup changed'
new = """<div class="rec-call-vid rec-call-vid--mira">
                        <img class="rec-call-bot" src="mira-logo.svg"
                             width="1152" height="365" alt="Mira" loading="lazy">
                        <span class="rec-call-tag">Mira</span>
                      </div>"""
s = s[:start] + new + s[end:]

# ---- the photo rules stop applying to the wordmark -------------------------
old = """    .rec-call-vid img { position:absolute; inset:0; width:100%; height:100%;
                        object-fit:cover; border-radius:inherit; }
    .rec-call-vid img ~ .rec-call-av { display:none; }"""
new = """    .rec-call-vid > img:not(.rec-call-bot) { position:absolute; inset:0;
                        width:100%; height:100%;
                        object-fit:cover; border-radius:inherit; }
    .rec-call-vid > img:not(.rec-call-bot) ~ .rec-call-av { display:none; }
    /* the wordmark sits in the tile the way a logo does, not as a feed */
    .rec-call-bot { position:relative; z-index:1; width:62px; height:auto;
                    filter:invert(1) brightness(1.9); opacity:.95; }"""
assert old in s, 'photo rules changed'
s = s.replace(old, new, 1)

old = """    .rec-call-vid:has(img)::after { content:""; position:absolute; inset:auto 0 0 0;"""
new = """    .rec-call-vid:has(> img:not(.rec-call-bot))::after { content:"";
                                    position:absolute; inset:auto 0 0 0;"""
assert old in s, 'vignette rule changed'
s = s.replace(old, new, 1)

old = """    .rec-call-vid--you { background:linear-gradient(145deg, #4B2F8F 0%, #7C5CF6 60%,
                                                    #C0A9FF 100%); }"""
new = """    .rec-call-vid--mira { background:linear-gradient(145deg, #4B2F8F 0%, #7C5CF6 60%,
                                                      #C0A9FF 100%); }"""
assert old in s, 'mira tile rule changed'
s = s.replace(old, new, 1)

assert 'rec-call-vid--you' not in s, 'a --you reference is left'
io.open(p, 'w', encoding='utf-8').write(s)
print('Mira is in the call')
