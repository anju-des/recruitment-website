# -*- coding: utf-8 -*-
"""The lines start grey and turn white one at a time.

The fade-from-nothing was easy to miss: by the time the text was centred the
whole thing had already played, and three lines appearing took barely a
second. Now all three are there in grey from the start -- the thing that
moves is the colour, line by line, with a long enough gap between them to
read as a sequence.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

old = """    .rec-line { display:block; }
    .rec-line--lead { font-weight:600; color:#FFFFFF; }
    /* each line waits its turn; the start state is added by script so the
       text is simply present if that never runs */
    .rec-say.rec-anim .rec-line { opacity:0; transform:translateY(16px); }
    .rec-say.rec-in .rec-line { animation:rec-line-in .75s cubic-bezier(.22,.61,.36,1) both; }
    .rec-say.rec-in .rec-line:nth-child(2) { animation-delay:.22s; }
    .rec-say.rec-in .rec-line:nth-child(3) { animation-delay:.44s; }
    /* each line lifts into white as it arrives; the animation fills forwards,
       so the colour it ends on is the colour it keeps */
    @keyframes rec-line-in {
      from { opacity:0; transform:translateY(16px); color:#8E97AE; }
      to   { opacity:1; transform:none; color:#FFFFFF; }
    }
    @media (prefers-reduced-motion: reduce) {
      .rec-say.rec-anim .rec-line { opacity:1; transform:none; }
      .rec-say.rec-in .rec-line { animation:none; }
    }"""
new = """    .rec-line { display:block; color:#8E97AE; }
    .rec-line--lead { font-weight:600; }
    /* the text is always there in grey; what moves is the colour, one line at
       a time, and it fills forwards so each line keeps the white it reaches */
    .rec-say.rec-in .rec-line { animation:rec-line-white .7s ease-out both; }
    .rec-say.rec-in .rec-line:nth-child(2) { animation-delay:.5s; }
    .rec-say.rec-in .rec-line:nth-child(3) { animation-delay:1s; }
    @keyframes rec-line-white {
      from { color:#8E97AE; }
      to   { color:#FFFFFF; }
    }
    @media (prefers-reduced-motion: reduce) {
      .rec-say.rec-in .rec-line { animation:none; color:#FFFFFF; }
    }"""
assert old in s, 'line css changed'
s = s.replace(old, new, 1)

# the observer no longer needs to hide anything first, and it should wait
# until the block is properly in view rather than firing at the edge
old = """    var say = document.querySelector('.rec-say');
    if (!say || !('IntersectionObserver' in window)) return;
    say.classList.add('rec-anim');"""
new = """    var say = document.querySelector('.rec-say');
    if (!say || !('IntersectionObserver' in window)) return;"""
assert old in s, 'statement script changed'
s = s.replace(old, new, 1)

old = "    }, { threshold: 0.6 });"
new = "    }, { threshold: 0.95 });"
assert old in s, 'threshold changed'
s = s.replace(old, new, 1)

old = "  // The statement arrives a line at a time, once, when it is well in view."
new = "  // The lines turn white one at a time, once, when the block is in view."
assert old in s, 'statement comment changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('grey to white, line by line')
