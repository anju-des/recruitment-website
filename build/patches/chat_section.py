# -*- coding: utf-8 -*-
"""A chat window where Mira answers on her own.

The conversation plays itself when the window comes into view: each turn
appears in order, with a typing indicator sitting in for the pause before
Mira replies. It resets when the window leaves, so it plays again on the way
back.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

# ---- markup ----------------------------------------------------------------
old = """          </p>
        </section>
"""
new = """          </p>
        </section>

        <!-- MIRA AT WORK -->
        <section class="rec-chat-sec">
          <div class="rec-win">
            <div class="rec-win-bar">
              <span class="rec-win-name">Mira</span>
              <span class="rec-win-dots" aria-hidden="true">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                     stroke-linecap="round"><path d="M5 12h14"/></svg>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                     stroke-linecap="round" stroke-linejoin="round"><path d="M14 4h6v6"/><path d="M10 20H4v-6"/><path d="M20 4l-7 7"/><path d="M4 20l7-7"/></svg>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                     stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>
              </span>
            </div>

            <div class="rec-thread">
              <div class="rec-turn rec-turn--you"><p>Senior backend engineer, Python + Django, Bengaluru</p></div>
              <div class="rec-turn rec-turn--typing"><span class="rec-dot"></span><span class="rec-dot"></span><span class="rec-dot"></span></div>
              <div class="rec-turn rec-turn--mira"><p>Posted. I&rsquo;ll read every application as it lands and rank it against your brief.</p></div>
              <div class="rec-turn rec-turn--you"><p>Anyone good yet?</p></div>
              <div class="rec-turn rec-turn--typing"><span class="rec-dot"></span><span class="rec-dot"></span><span class="rec-dot"></span></div>
              <div class="rec-turn rec-turn--mira"><p>38 so far, 6 worth your time. The closest has seven years on Django and has shipped payments twice.</p></div>
            </div>

            <div class="rec-ask">
              <p class="rec-ask-hint">Ask a follow-up&hellip;</p>
              <div class="rec-ask-row">
                <span class="rec-ask-tools" aria-hidden="true">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                       stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg>
                  <b>@</b>
                </span>
                <span class="rec-ask-send" aria-hidden="true">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"
                       stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5"/><path d="M5 12l7-7 7 7"/></svg>
                </span>
              </div>
            </div>
          </div>
        </section>
"""
assert s.count(old) == 1, 'statement section close moved'
s = s.replace(old, new, 1)

# ---- css -------------------------------------------------------------------
old = '    /* ---- suggestions ------'
new = """    /* ---- mira at work ---------------------------------------------------- */
    .rec-chat-sec { min-height:110vh; display:grid; place-items:center; }
    .rec-win { width:min(720px, 100%); border-radius:16px; overflow:hidden;
               background:rgba(255,255,255,0.035);
               box-shadow:0 30px 70px rgba(0,0,0,.45), inset 0 0 0 1px rgba(255,255,255,.07); }
    .rec-win-bar { display:flex; align-items:center; justify-content:space-between;
                   padding:14px 18px; background:rgba(255,255,255,0.025); }
    .rec-win-name { font-size:13.5px; font-weight:600; color:#E8EAF2; }
    .rec-win-dots { display:inline-flex; align-items:center; gap:14px; color:#6B7488; }
    .rec-win-dots svg { width:14px; height:14px; }

    .rec-thread { min-height:320px; padding:22px 18px; display:flex;
                  flex-direction:column; gap:12px; }
    .rec-turn { max-width:76%; padding:11px 14px; border-radius:14px; font-size:14.5px;
                line-height:1.5; opacity:0; transform:translateY(10px);
                transition:opacity .45s ease, transform .45s ease; }
    .rec-turn--you { align-self:flex-end; background:rgba(255,255,255,0.10); color:#F2F3F8;
                     border-bottom-right-radius:5px; }
    .rec-turn--mira { align-self:flex-start; background:rgba(139,92,246,0.22); color:#EDEAFB;
                      border-bottom-left-radius:5px; }
    .rec-turn--typing { align-self:flex-start; display:flex; gap:5px; padding:14px 16px;
                        background:rgba(255,255,255,0.07); border-bottom-left-radius:5px; }
    .rec-dot { width:6px; height:6px; border-radius:50%; background:#A8AFC2;
               animation:rec-blink 1.3s ease-in-out infinite; }
    .rec-dot:nth-child(2) { animation-delay:.18s; }
    .rec-dot:nth-child(3) { animation-delay:.36s; }
    @keyframes rec-blink { 0%, 100% { opacity:.3; } 50% { opacity:1; } }
    /* a turn is shown by script, in order; a typing turn is removed again
       once the reply it stands in for arrives */
    .rec-turn.is-on { opacity:1; transform:none; }
    .rec-turn.is-done { display:none; }

    .rec-ask { margin:0 14px 14px; padding:12px 14px 10px; border-radius:12px;
               background:rgba(255,255,255,0.05); }
    .rec-ask-hint { font-size:14px; color:#7D869B; }
    .rec-ask-row { display:flex; align-items:center; justify-content:space-between;
                   margin-top:10px; }
    .rec-ask-tools { display:inline-flex; align-items:center; gap:12px; color:#7D869B;
                     font-size:14px; font-weight:600; }
    .rec-ask-tools svg { width:15px; height:15px; }
    .rec-ask-send { width:30px; height:30px; border-radius:50%; display:grid;
                    place-items:center; background:#8B5CF6; color:#fff; }
    .rec-ask-send svg { width:15px; height:15px; }
    @media (prefers-reduced-motion: reduce) {
      .rec-turn { opacity:1; transform:none; }
      .rec-dot { animation:none; }
    }

""" + old
assert old in s, 'suggestions css marker moved'
s = s.replace(old, new, 1)

old = """      .rec-say { max-width:30ch; }"""
new = """      .rec-say { max-width:30ch; }
      .rec-win { width:100%; }
      .rec-turn { max-width:86%; font-size:13.5px; }"""
assert old in s, 'responsive statement rule changed'
s = s.replace(old, new, 1)

# ---- script ----------------------------------------------------------------
old = "</script>\n</body>"
new = """
  // Mira's thread plays itself: each turn in order, and a typing bubble is
  // taken away again as soon as the reply it stood in for appears.
  (function () {
    var win = document.querySelector('.rec-win');
    if (!win || !('IntersectionObserver' in window)) return;
    var turns = [].slice.call(win.querySelectorAll('.rec-turn'));
    var timers = [];

    function reset() {
      timers.forEach(clearTimeout);
      timers = [];
      turns.forEach(function (t) { t.classList.remove('is-on', 'is-done'); });
    }

    function play() {
      var at = 420;
      turns.forEach(function (turn, i) {
        timers.push(setTimeout(function () {
          turn.classList.add('is-on');
          var before = turns[i - 1];
          if (before && before.classList.contains('rec-turn--typing')) {
            before.classList.add('is-done');
          }
        }, at));
        at += turn.classList.contains('rec-turn--typing') ? 1100 : 900;
      });
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.intersectionRatio >= 0.6) { reset(); play(); }
        else if (!e.isIntersecting) reset();
      });
    }, { threshold: [0, 0.6] });
    io.observe(win);
  }());
</script>
</body>"""
assert old in s, 'script close not found'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('chat window added')
