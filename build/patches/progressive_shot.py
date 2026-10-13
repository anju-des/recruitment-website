# -*- coding: utf-8 -*-
"""Make the portal screenshot reveal itself as the page scrolls.

It starts as a sliver at the foot of the full-screen hero and grows to its full
height as you scroll, ending as a section of its own.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# ------------------------------------------------------------------ markup
start = s.index('              <div class="rec-hero-shot">')
end = s.index('</div>', s.index('<img', start)) + len('</div>')
block = s[start:end]
assert 'recruit-portal.png' in block, 'hero shot markup changed'
s = s[:start].rstrip('\n') + '\n' + s[end:].lstrip('\n')

# close the hero, then the shot as its own section
hero_close = """          </div>
        </section>
"""
assert hero_close in s, 'hero close moved'
new = hero_close + """
        <!-- PORTAL -->
        <section class="rec-shot-sec">
          <div class="rec-shot">
            <img src="recruit-portal.png" width="1911" height="902" fetchpriority="high"
                 alt="The Wisemonk recruitment portal: post a role, pending actions and recent pipeline activity">
          </div>
        </section>
"""
s = s.replace(hero_close, new, 1)

# ------------------------------------------------------------------ styles
old_css_start = s.index('    /* pinned to the hero\'s floor')
old_css_end = s.index('    /* ---- hero composer')
old_css = s[old_css_start:old_css_end]
assert 'rec-hero-shot' in old_css, 'shot css changed'

new_css = """    /* The portal sits in its own section, clipped to a sliver at first and
       grown by the scroll script below. Height is inline-styled from JS, so
       the value here is only the starting state (and the whole state when
       scripting is off -- see the no-js note in the script). */
    .rec-shot-sec { margin-top:-54px; }
    .rec-shot { max-width:1200px; margin-inline:auto; height:var(--rec-peek);
                border-radius:16px 16px 0 0; overflow:hidden; line-height:0;
                border:8px solid var(--primary-100); border-bottom:none;
                will-change:height; }
    .rec-shot img { width:100%; height:auto; display:block; }

"""
s = s[:old_css_start] + new_css + s[old_css_end:]

# the hero now stops above the sliver, and the flow section no longer has to
# cancel the gap -- the portal section does
s = s.replace('min-height:calc(100vh - var(--rec-chrome));',
              'min-height:calc(100vh - var(--rec-chrome) - var(--rec-peek));', 1)
s = s.replace("""                     padding:40px; margin-top:-54px; }""",
              """                     padding:40px; }""", 1)

# the blanket padding would put a floor under the sliver
s = s.replace("    .rec-wrap > section.rec-hero { padding-bottom:0; }\n",
              "    .rec-wrap > section.rec-hero { padding-bottom:0; }\n"
              "    .rec-wrap > section.rec-shot-sec { padding:0 48px; }\n", 1)

# ------------------------------------------------------------------ script
SCRIPT = """
<script>
  // Grow the portal screenshot from a sliver to its full height as the page
  // scrolls. Without scripting the sliver is all you get, which is why the
  // section below it never depends on this running.
  (function () {
    var shot = document.querySelector('.rec-shot');
    if (!shot) return;
    var img = shot.querySelector('img');
    var peek = parseInt(getComputedStyle(document.documentElement)
                        .getPropertyValue('--rec-peek'), 10) || 150;
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function full() {
      // content box, so the border is already excluded
      return Math.round(shot.clientWidth * img.naturalHeight / img.naturalWidth);
    }
    function apply() {
      if (!img.naturalWidth) return;
      var target = full();
      if (reduce) { shot.style.height = target + 'px'; return; }
      var top = shot.getBoundingClientRect().top;
      // 0 while the sliver sits at the foot of the hero, 1 after the shot has
      // travelled 60% of a viewport upwards
      var p = (window.innerHeight - top - peek) / (window.innerHeight * 0.6);
      p = Math.max(0, Math.min(1, p));
      shot.style.height = Math.round(peek + (target - peek) * p) + 'px';
    }

    var queued = false;
    function onScroll() {
      if (queued) return;
      queued = true;
      requestAnimationFrame(function () { queued = false; apply(); });
    }
    if (img.complete) apply(); else img.addEventListener('load', apply);
    addEventListener('scroll', onScroll, { passive: true });
    addEventListener('resize', onScroll);
  }());
</script>
"""
assert '</body>' in s, 'body close missing'
s = s.replace('\n</body>', SCRIPT + '</body>', 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('progressive reveal wired')
