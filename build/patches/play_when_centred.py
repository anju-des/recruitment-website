# -*- coding: utf-8 -*-
"""The thread waits until the window is actually centred.

It was firing on a visibility threshold, which the window crossed while it
was still climbing into the frame -- so the conversation had played out
before it arrived. It now starts at the moment the section pins, which is
exactly when the window reaches the middle, and the scroll is held from
there until the answer is complete.
"""
import io
import re

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# ---- the thread exposes a start and a reset instead of watching itself -----
old = """    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.intersectionRatio >= 0.6) { reset(); play(); }
        else if (!e.isIntersecting) reset();
      });
    }, { threshold: [0, 0.6] });
    io.observe(win);"""
new = """    // The scroll handler calls these: it knows when the section pins, which
    // is the moment the window reaches the middle of the screen.
    var started = false;
    window.__miraStart = function () {
      if (started) return;
      started = true;
      reset();
      play();
    };
    window.__miraReset = function () {
      if (!started) return;
      started = false;
      reset();
    };"""
assert old in s, 'chat observer changed'
s = s.replace(old, new, 1)

# ---- a brisker thread, since the page is waiting on it ---------------------
old = "        at += turn.classList.contains('rec-turn--typing') ? 850 : 620;"
new = "        at += turn.classList.contains('rec-turn--typing') ? 560 : 340;"
assert old in s, 'thread timing changed'
s = s.replace(old, new, 1)

# ---- the scroll handler starts it at the pin -------------------------------
old = """          var chatTop = window.scrollY + cb.top;"""
new = """          var chatTop = window.scrollY + cb.top;
          // centred the moment the section pins
          if (window.scrollY >= chatTop - 2) {
            if (window.__miraStart) window.__miraStart();
          } else if (window.scrollY < chatTop - window.innerHeight * 0.5) {
            if (window.__miraReset) window.__miraReset();
          }"""
assert old in s, 'chat top block changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('the thread starts when the window centres')
