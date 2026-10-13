# -*- coding: utf-8 -*-
"""A light closing section under the black one.

It carries its own background, so it lifts the page out of the dark on its
own terms rather than waiting for the sky, and it comes up over the black
with a rounded top edge. The content fades and rises as the section arrives.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

old = """      </div>
    </div>
  </div>
</div>"""
new = """
        <!-- CLOSING -->
        <section class="rec-close">
          <div class="rec-close-in">
            <h2>Start hiring today. Anywhere.</h2>
            <p>A recruiter opens your role in the market you are hiring in, and Mira
            reads every application that lands. You pay only when someone joins.</p>
            <div class="rec-close-acts">
              <a class="rec-close-btn" href="#start">Post a role</a>
              <a class="rec-close-alt" href="#talk">Talk to a recruiter</a>
            </div>
          </div>
        </section>

      </div>
    </div>
  </div>
</div>"""
assert s.count(old) == 1, 'the wrapper close moved'
s = s.replace(old, new, 1)

old = '    /* ---- suggestions ------'
new = """    /* ---- closing ---------------------------------------------------------- */
    /* Its own light ground, rising over the black with a rounded top edge. */
    .rec-close { position:relative; margin-top:-40px; border-radius:36px 36px 0 0;
                 background:linear-gradient(180deg, #EFEAFF 0%, #FFFFFF 62%);
                 padding:132px 48px 140px; text-align:center; }
    .rec-close-in { max-width:720px; margin-inline:auto;
                    opacity:0; transform:translateY(34px);
                    transition:opacity .85s cubic-bezier(.22,.61,.36,1),
                               transform .85s cubic-bezier(.22,.61,.36,1); }
    .rec-close.is-on .rec-close-in { opacity:1; transform:none; }
    .rec-close h2 { font-size:clamp(30px, 2.2vw + 14px, 52px); font-weight:600;
                    line-height:1.12; letter-spacing:-0.03em; color:var(--grey-700);
                    text-wrap:balance; }
    .rec-close p { max-width:54ch; margin:22px auto 0; font-size:17px; line-height:1.65;
                   color:var(--text-secondary); text-wrap:pretty; }
    .rec-close-acts { display:flex; flex-wrap:wrap; justify-content:center;
                      align-items:center; gap:14px; margin-top:34px; }
    .rec-close-btn { display:inline-flex; align-items:center; height:46px; padding:0 26px;
                     border-radius:8px; background:#0f172a; color:#FFFFFF;
                     font-size:15px; font-weight:600; transition:background .14s; }
    .rec-close-btn:hover { background:#1e293b; }
    .rec-close-alt { display:inline-flex; align-items:center; height:46px; padding:0 20px;
                     border-radius:8px; font-size:15px; font-weight:500;
                     color:var(--text-primary); transition:background .14s; }
    .rec-close-alt:hover { background:rgba(32,22,66,.06); }
    @media (prefers-reduced-motion: reduce) {
      .rec-close-in { opacity:1; transform:none; }
    }

""" + old
assert old in s, 'suggestions marker moved'
s = s.replace(old, new, 1)

old = """      .rec-chat-sec { min-height:0; margin-top:0; padding-block:60px; }"""
new = """      .rec-chat-sec { min-height:0; margin-top:0; padding-block:60px; }
      .rec-close { padding:84px 24px 96px; }"""
assert old in s, 'responsive chat rule changed'
s = s.replace(old, new, 1)

old = "</script>\n</body>"
new = """
  // The closing section comes up as it arrives, and resets behind you.
  (function () {
    var close = document.querySelector('.rec-close');
    if (!close || !('IntersectionObserver' in window)) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.intersectionRatio >= 0.25) close.classList.add('is-on');
        else if (!e.isIntersecting) close.classList.remove('is-on');
      });
    }, { threshold: [0, 0.25] });
    io.observe(close);
  }());
</script>
</body>"""
assert old in s, 'script close not found'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('closing section added')
