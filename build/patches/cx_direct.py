# -*- coding: utf-8 -*-
"""The row under the composer opens their Claude. No panel in between.

claude.ai/new?q=... puts the question in the box of a fresh chat, and the
route survives the sign-in redirect for anyone signed out. They send it,
Claude writes the profile, they paste it back with the role.

The prompt asks for the company and the person and says so three times,
because a model handed a short list will add a fifth item nobody wanted --
and whatever comes back gets read as fact by whoever picks up the role,
which is why it also says not to guess.

The row reports back in place rather than opening anything: a new tab is
already a context switch, and a modal on top of it would be a second one.
The arrow points out of the page because that is where the click goes.
"""
import io
import sys

SPARK = ('<svg class="rec-cx-mark" viewBox="0 0 24 24" fill="currentColor" '
         'aria-hidden="true"><path d="M12 3c.6 4.2 1.8 5.4 6 6-4.2.6-5.4 1.8-6 '
         '6-.6-4.2-1.8-5.4-6-6 4.2-.6 5.4-1.8 6-6z"/></svg>')

ROW = """              <div class="rec-cx-row">
                <button type="button" class="rec-cx">
                  @SPARK@
                  <span class="rec-cx-say"><b>Connect your Claude</b>
                    <i>so the brief knows who it is hiring for</i></span>
                  <svg class="rec-cx-go" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2.1" stroke-linecap="round"
                    stroke-linejoin="round" aria-hidden="true"><path d="M7 17L17 7"/>
                    <path d="M9 7h8v8"/></svg>
                </button>
              </div>
""".replace('@SPARK@', SPARK)

ANCHOR = """              </form>
              </div>
              <ul class="rec-suggest" aria-label="Example roles" hidden>
"""

CSS = """
    /* ---- connect your Claude -------------------------------------------- */
    .rec-cx-row { width:100%; text-align:center; margin-top:16px; }
    .rec-cx { display:inline-flex; align-items:center; gap:10px;
              max-width:100%; padding:9px 14px 9px 13px; cursor:pointer;
              border:1px solid rgba(124,92,246,.22); border-radius:100px;
              background:rgba(124,92,246,.05); font:inherit; text-align:left;
              transition:background .15s, border-color .15s, transform .15s; }
    .rec-cx:hover { background:rgba(124,92,246,.1);
                    border-color:rgba(124,92,246,.4);
                    transform:translateY(-1px); }
    .rec-cx:focus-visible { outline:2px solid #7C5CF6; outline-offset:3px; }
    .rec-cx-mark { width:17px; height:17px; flex:none; color:#7C5CF6; }
    .rec-cx-say { min-width:0; }
    .rec-cx b { font-size:14px; font-weight:600; color:var(--text-primary); }
    .rec-cx i { font-style:normal; font-size:14px; color:var(--text-muted); }
    .rec-cx i::before { content:"\\00b7"; margin:0 8px; color:#C6BFE0; }
    .rec-cx-go { width:14px; height:14px; flex:none; color:var(--text-muted); }
    @media (prefers-reduced-motion: reduce) {
      .rec-cx { transition:none; }
      .rec-cx:hover { transform:none; }
    }
"""

CSS_ANCHOR = "    /* ---- Mira in the corner ---"

JS = r"""
  // Connect your Claude: straight out to claude.ai with the question already
  // in the box. Nothing server-side, so nothing to wait for.
  (function () {
    var row = document.querySelector('.rec-cx');
    if (!row) return;

    // "only what you already know" and "do not guess" are load-bearing: this
    // text comes back as a company profile and will be read as fact.
    var PROMPT = [
      'I am briefing a role to Wisemonk\'s AI recruiter, Mira, and it works ' +
        'better when it knows who it is hiring for.',
      '',
      'Write me a profile I can paste in — plain prose, no headings or ' +
        'bullet points. Cover these two things only, and only what you ' +
        'already know:',
      '',
      '- the company: what we do, what we sell and who we sell it to, roughly ' +
        'how big we are, and where the team works from',
      '- me: my name, my role, and what I am responsible for here',
      '',
      'Nothing else — no hiring advice, no role description, no ' +
        'suggestions.',
      '',
      'Do not guess. If you do not know something, leave it out and ask me ' +
        'instead.'
    ].join('\n');

    var say = row.querySelector('.rec-cx-say');
    var resting = say.innerHTML;
    var back = 0;

    row.addEventListener('click', function () {
      window.open('https://claude.ai/new?q=' + encodeURIComponent(PROMPT),
                  '_blank', 'noopener');
      // said in place: the new tab is already a context switch
      say.innerHTML = '<b>Opened in Claude</b><i>paste what it writes into ' +
                      'the box above</i>';
      window.clearTimeout(back);
      back = window.setTimeout(function () { say.innerHTML = resting; }, 12000);
    });
  }());
"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-cx' not in s, path + ': already has the row'

    assert s.count(ANCHOR) == 1, (path, 'composer anchor', s.count(ANCHOR))
    s = s.replace(ANCHOR, ANCHOR.replace(
        '              <ul class="rec-suggest"',
        ROW + '              <ul class="rec-suggest"'), 1)

    assert s.count(CSS_ANCHOR) == 1, (path, 'css anchor', s.count(CSS_ANCHOR))
    s = s.replace(CSS_ANCHOR, CSS.lstrip('\n') + '\n' + CSS_ANCHOR, 1)

    i = s.rindex('</script>')
    s = s[:i] + JS + s[i:]

    assert 'rec-cxp' not in s, path + ': a panel crept back in'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
