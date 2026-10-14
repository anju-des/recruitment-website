# -*- coding: utf-8 -*-
"""Keep listening after Chrome hangs up.

`continuous = true` does not mean what it sounds like: Chrome still ends the
session on a pause of a few seconds and fires `end`, which was switching the
button off underneath the person still talking.

So the button now holds the intent and the recogniser is restarted whenever
it ends while that intent stands. Two guards on that: a refusal (no
permission, no microphone) clears the intent rather than looping on a dialog
the person has already dismissed, and a session that ends within a blink of
starting, four times over, gives up rather than spinning.
"""
import io
import sys

OLD = """    var on = false;
    var base = '';"""
NEW = """    var on = false;        // what the button shows
    var wanted = false;    // what the person asked for, across restarts
    var base = '';
    var began = 0;
    var retries = 0;"""

OLD_START = """    function start() {
      base = field.value.replace(/\\s+$/, '');
      try {
        rec.start();
      } catch (e) {
        return;                      // already running; the end event tidies up
      }
      mark(true);
      field.focus();
      // focusing opens the example briefs, and they would sit over the words
      // as they arrive
      if (list) list.hidden = true;
    }

    function stop() {
      mark(false);
      try { rec.stop(); } catch (e) {}
    }"""
NEW_START = """    function begin() {
      try {
        rec.start();
        began = Date.now();
      } catch (e) {}                 // already running; the end event tidies up
    }

    function start() {
      base = field.value.replace(/\\s+$/, '');
      wanted = true;
      retries = 0;
      begin();
      mark(true);
      field.focus();
      // focusing opens the example briefs, and they would sit over the words
      // as they arrive
      if (list) list.hidden = true;
    }

    function stop() {
      wanted = false;                // before the stop, or `end` restarts it
      mark(false);
      try { rec.stop(); } catch (e) {}
    }"""

OLD_END = """    rec.addEventListener('end', function () { mark(false); });
    rec.addEventListener('error', function () { mark(false); });"""
NEW_END = """    // `continuous` does not survive a pause: Chrome ends the session after a
    // few quiet seconds, which was switching the button off under someone
    // still talking. Pick it straight back up while the button is down.
    rec.addEventListener('end', function () {
      if (!wanted) { mark(false); return; }
      // unless it is ending the instant it starts, which is a loop
      retries = Date.now() - began < 400 ? retries + 1 : 0;
      if (retries > 3) { wanted = false; mark(false); return; }
      begin();
    });

    rec.addEventListener('error', function (e) {
      var why = e && e.error;
      // no permission, or no microphone: asking again just reopens a dialog
      // the person has already answered
      if (why === 'not-allowed' || why === 'service-not-allowed' ||
          why === 'audio-capture') {
        wanted = false;
        mark(false);
      }
      // 'no-speech' and 'aborted' fall through to `end`, which restarts it
    });"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'var wanted' not in s, path + ': already restarts'
    for old, new in ((OLD, NEW), (OLD_START, NEW_START), (OLD_END, NEW_END)):
        assert s.count(old) == 1, (path, old.strip()[:44], s.count(old))
        s = s.replace(old, new, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
