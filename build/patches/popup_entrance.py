# -*- coding: utf-8 -*-
"""Swap the scroll-linked reveal for a one-shot pop-in.

Scroll-linked meant the image scrubbed with the scrollbar. This plays once, at
its own pace, the first time the portal comes into view.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

start = s.index('    /* no width cap: the portal fills the section */')
end = s.index('    /* ---- hero composer')
old = s[start:end]
assert 'rec-reveal' in old, 'portal css changed'

new = """    /* no width cap: the portal fills the section */
    .rec-shot-sec { background:var(--bg-subtle); }
    .rec-shot { border-radius:16px; overflow:hidden; line-height:0;
                border:8px solid var(--primary-100); }
    .rec-shot img { width:100%; height:auto; display:block; }

    /* Pops in once, the first time it comes into view -- a fixed 700ms, not
       scrubbed by the scrollbar. The starting state is applied by script
       (.rec-anim) so that without JS the image is simply visible rather than
       stuck at opacity 0. */
    .rec-shot.rec-anim { opacity:0; transform:translateY(30px) scale(.97);
                         transform-origin:50% 0; }
    .rec-shot.rec-in { animation:rec-pop .7s cubic-bezier(.22,.61,.36,1) both; }
    @keyframes rec-pop {
      from { opacity:0; transform:translateY(30px) scale(.97); }
      to   { opacity:1; transform:none; }
    }
    @media (prefers-reduced-motion: reduce) {
      .rec-shot.rec-anim { opacity:1; transform:none; }
      .rec-shot.rec-in { animation:none; }
    }

"""
s = s[:start] + new + s[end:]

# the starting-crop token is no longer used
s = s.replace('"--rec-chrome:140px; --rec-start:400px;", 1)', '"--rec-chrome:140px;", 1)', 1)
assert '--rec-start' not in s, 'a reference to the crop token is left'

SCRIPT = """
<script>
  // Pop the portal in the first time it scrolls into view. The hidden start
  // state is added here, not in the stylesheet, so the image stays visible if
  // this never runs.
  (function () {
    var shot = document.querySelector('.rec-shot');
    if (!shot || !('IntersectionObserver' in window)) return;
    shot.classList.add('rec-anim');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        shot.classList.add('rec-in');
        io.disconnect();
      });
    }, { threshold: 0.15 });
    io.observe(shot);
  }());
</script>
"""
assert '</body>' in s, 'body close missing'
s = s.replace('\n</body>', SCRIPT + '</body>', 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('portal now pops in once on first view')
