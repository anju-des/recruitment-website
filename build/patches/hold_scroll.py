# -*- coding: utf-8 -*-
"""Hold the page still until Mira has finished answering.

The thread plays out before the scroll is handed back, so nobody slides past
the answer half-written. Three ways out, because taking someone's scroll away
is a thing to do carefully: it releases when the last turn lands, on Escape,
and on a hard timeout in case a frame never arrives.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# a brisker thread, since the page is waiting on it
old = "        at += turn.classList.contains('rec-turn--typing') ? 1100 : 900;"
new = "        at += turn.classList.contains('rec-turn--typing') ? 850 : 620;"
assert old in s, 'thread timing changed'
s = s.replace(old, new, 1)

old = """    var turns = [].slice.call(win.querySelectorAll('.rec-turn'));
    var timers = [];"""
new = """    var turns = [].slice.call(win.querySelectorAll('.rec-turn'));
    var timers = [];
    var held = false, everHeld = false;

    // Holding the scroll means blocking the events that cause it, rather than
    // touching overflow -- the page keeps its position and nothing shifts.
    function stop(e) { e.preventDefault(); }
    var KEYS = [' ', 'PageDown', 'PageUp', 'ArrowDown', 'ArrowUp', 'Home', 'End'];
    function onKey(e) {
      if (e.key === 'Escape') { release(); return; }
      if (KEYS.indexOf(e.key) > -1) e.preventDefault();
    }
    function hold() {
      if (held || everHeld) return;
      held = everHeld = true;
      window.addEventListener('wheel', stop, { passive: false });
      window.addEventListener('touchmove', stop, { passive: false });
      window.addEventListener('keydown', onKey, { passive: false });
    }
    function release() {
      if (!held) return;
      held = false;
      window.removeEventListener('wheel', stop, { passive: false });
      window.removeEventListener('touchmove', stop, { passive: false });
      window.removeEventListener('keydown', onKey, { passive: false });
    }"""
assert old in s, 'thread script head changed'
s = s.replace(old, new, 1)

old = """    function play() {
      var at = 420;"""
new = """    function play() {
      var at = 420;
      hold();"""
assert old in s, 'play opening changed'
s = s.replace(old, new, 1)

old = """      });
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.intersectionRatio >= 0.6) { reset(); play(); }"""
new = """      });
      // the scroll comes back as the last turn lands, and no later than this
      // whatever happens to the frames in between
      timers.push(setTimeout(release, at + 200));
      timers.push(setTimeout(release, 9000));
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.intersectionRatio >= 0.6) { reset(); play(); }"""
assert old in s, 'play close changed'
s = s.replace(old, new, 1)

# a reset must never leave the page stuck
old = """    function reset() {
      timers.forEach(clearTimeout);
      timers = [];"""
new = """    function reset() {
      timers.forEach(clearTimeout);
      timers = [];
      release();"""
assert old in s, 'reset changed'
s = s.replace(old, new, 1)

old = """      .rec-win { width:100%; }
      .rec-win--2, .rec-win--3 { opacity:1; transform:none; }"""
assert old in s, 'responsive window rules changed'
io.open(p, 'w', encoding='utf-8').write(s)
print('scroll waits for the answer')
