# -*- coding: utf-8 -*-
"""The rail walks itself: a stage every three seconds, once you reach it.

It only runs while the section is actually on screen, so scrolling to it is
what starts it and scrolling away stops it rather than letting it cycle to
nobody. Clicking a stage takes it over and restarts the count from there,
and hovering holds it where it is -- a panel that moved on while you were
reading it would be worse than one that never moved.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

old = """    rail.addEventListener('click', function (e) {
      var tab = e.target.closest('[data-rec-stage]');
      if (!tab) return;
      var key = tab.getAttribute('data-rec-stage');
      mark(tab);
      tabs.forEach(function (t) {
        var on = t === tab;
        t.classList.toggle('is-on', on);
        t.setAttribute('aria-selected', on ? 'true' : 'false');
      });
      panes.forEach(function (pane) {
        pane.classList.toggle('is-on', pane.getAttribute('data-rec-pane') === key);
      });
    });
  }());"""

new = """    function show(tab) {
      var key = tab.getAttribute('data-rec-stage');
      mark(tab);
      tabs.forEach(function (t) {
        var on = t === tab;
        t.classList.toggle('is-on', on);
        t.setAttribute('aria-selected', on ? 'true' : 'false');
      });
      panes.forEach(function (pane) {
        pane.classList.toggle('is-on', pane.getAttribute('data-rec-pane') === key);
      });
    }

    var STEP = 3000;
    var at = 0, timer = null, seen = false, over = false;
    var still = window.matchMedia('(prefers-reduced-motion: reduce)');

    function stop() { clearInterval(timer); timer = null; }
    function start() {
      if (timer || !seen || over || still.matches) return;
      timer = setInterval(function () {
        at = (at + 1) % tabs.length;
        show(tabs[at]);
      }, STEP);
    }
    function restart() { stop(); start(); }

    rail.addEventListener('click', function (e) {
      var tab = e.target.closest('[data-rec-stage]');
      if (!tab) return;
      at = tabs.indexOf(tab);
      show(tab);
      restart();                       // your click resets the count
    });

    // reading it holds it; the pointer leaving lets it carry on
    var block = rail.parentNode;
    block.addEventListener('mouseenter', function () { over = true; stop(); });
    block.addEventListener('mouseleave', function () { over = false; start(); });
    block.addEventListener('focusin', function () { over = true; stop(); });
    block.addEventListener('focusout', function () { over = false; start(); });

    // it runs only while the section is on screen
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        seen = entries[0].isIntersecting;
        if (seen) { start(); } else { stop(); }
      }, { threshold: 0.4 }).observe(block);
    } else {
      seen = true;
      start();
    }
    if (still.addEventListener) {
      still.addEventListener('change', function () {
        if (still.matches) { stop(); } else { start(); }
      });
    }
  }());"""

assert old in s, 'rail click handler changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('the rail walks itself')
