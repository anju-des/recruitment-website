# -*- coding: utf-8 -*-
"""The screen holds and the scroll changes the stage.

The section is long enough to give each of the four a stretch of its own;
the frame is pinned across all of it, so scrolling moves the stage rather
than the page. The clock is gone -- two things driving the same rail would
have fought each other, and the scroll is the one the reader controls.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# ---- a stretch of scroll per stage, under one long pin ---------------------
old = """    /* one screen of ramp, then a screen of the colour it arrived at */
    .rec-deep { position:relative; min-height:200vh; }"""
new = """    /* one screen of ramp, then a stretch of held scroll for each stage */
    .rec-deep { position:relative; min-height:340vh; }"""
assert old in s, 'deep section rule changed'
s = s.replace(old, new, 1)

# ---- the scroll handler says which stage ------------------------------------
old = """        // the rail comes up over the back half of that ramp
        root.style.setProperty('--deep-in',
          Math.min(1, Math.max(0, (down - 0.45) / 0.4)).toFixed(3));
      }"""
new = """        // the rail comes up over the back half of that ramp
        root.style.setProperty('--deep-in',
          Math.min(1, Math.max(0, (down - 0.45) / 0.4)).toFixed(3));
        // past the ramp the frame is pinned, and the scroll walks the stages:
        // an equal stretch each, measured on the section rather than the pin
        if (window.__recStage) {
          var span = Math.max(1, deep.offsetHeight - window.innerHeight);
          var q = Math.min(0.9999, Math.max(0, (window.scrollY - dt) / span));
          window.__recStage(Math.floor(q * window.__recStages));
        }
      }"""
assert old in s, 'deep-in band changed'
s = s.replace(old, new, 1)

# ---- the rail takes its cue from the scroll, not a clock --------------------
start = s.index("""    var STEP = 3000;""")
end = s.index("  }());" + "\n\n\n" + "  // Mira's thread plays itself:")
block = s[start:end]
assert 'setInterval' in block, 'autoplay block changed'
s = s[:start] + """    var at = 0;
    window.__recStages = tabs.length;
    // the page's scroll handler calls this; a click just sets it directly
    window.__recStage = function (i) {
      if (i === at || !tabs[i]) return;
      at = i;
      show(tabs[i]);
    };

    rail.addEventListener('click', function (e) {
      var tab = e.target.closest('[data-rec-stage]');
      if (!tab) return;
      at = tabs.indexOf(tab);
      show(tab);
    });
""" + s[end:]

io.open(p, 'w', encoding='utf-8').write(s)
print('the scroll walks the stages')
