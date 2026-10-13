# -*- coding: utf-8 -*-
"""Slow the exit right down, and take the header with it.

Three changes: the sequence runs over far more scroll, the content fades on a
straight line to zero instead of racing ahead, and the header fades with
everything else. The field's own quick hide-on-scroll comes out -- it was
fighting the slow fade by vanishing in a fraction of the distance.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# ---- the header fades with the rest ----------------------------------------
old = """    /* content sits above the sky; the header above that */
    .rec-head { position:relative; z-index:2; }"""
new = """    /* content sits above the sky; the header above that, and it leaves on
       the same fade so nothing is left floating over the dark */
    .rec-head { position:relative; z-index:2; opacity:var(--rec-fade, 1); }"""
assert old in s, 'layering comment changed'
s = s.replace(old, new, 1)

# ---- a much longer run, and a straight fade --------------------------------
old = """      var span = Math.max(1, hero.offsetHeight * 0.7);"""
new = """      var span = Math.max(1, hero.offsetHeight * 1.7);"""
assert old in s, 'span changed'
s = s.replace(old, new, 1)

old = """      root.style.setProperty('--rec-lift', (p * 150).toFixed(2));
      root.style.setProperty('--rec-fade', (1 - Math.min(1, p * 1.25)).toFixed(3));"""
new = """      root.style.setProperty('--rec-lift', (p * 190).toFixed(2));
      root.style.setProperty('--rec-fade', (1 - p).toFixed(3));"""
assert old in s, 'lift/fade assignment changed'
s = s.replace(old, new, 1)

# ---- the field no longer darts away on its own -----------------------------
start = s.index("  // The field follows the scroll direction")
end = s.index("  // Scroll progress drives the hero's exit")
block = s[start:end]
assert 'is-out' in block, 'field scroll block changed'
s = s[:start] + s[end:]

old = """    .rec-compose-wrap.is-out { opacity:0; transform:translateY(-22px) scale(.94);
                               pointer-events:none; }
"""
assert old in s, 'is-out rule changed'
s = s.replace(old, '', 1)

old = """      .rec-compose-wrap.is-out { opacity:1; transform:none; pointer-events:auto; }
"""
assert old in s, 'reduced-motion is-out rule changed'
s = s.replace(old, '', 1)

# the only mention left should be the note on fill-mode, which still applies
old = '''       leave .is-out unable to move anything. */'''
assert old in s
s = s.replace(old, '''       leave a class-based override unable to move anything. */''', 1)
assert 'is-out' not in s, 'an is-out reference is left'
io.open(p, 'w', encoding='utf-8').write(s)
print('slower exit; header included; field no longer darts')
