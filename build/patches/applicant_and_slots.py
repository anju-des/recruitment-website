# -*- coding: utf-8 -*-
"""The second window answers with a person, the third with a time.

Three windows that all answered with the same table read as one screenshot
copied twice. Each now shows the thing its question is actually about: a
pipeline, an applicant, a slot to book.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

BAR = """            <div class="rec-win-bar">
              <img class="rec-win-logo" src="mira-logo.svg" width="1152" height="365" alt="Mira">
              <span class="rec-win-dots" aria-hidden="true">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                     stroke-linecap="round"><path d="M5 12h14"/></svg>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                     stroke-linecap="round" stroke-linejoin="round"><path d="M14 4h6v6"/><path d="M10 20H4v-6"/><path d="M20 4l-7 7"/><path d="M4 20l7-7"/></svg>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                     stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>
              </span>
            </div>"""

ASK = """            <div class="rec-ask">
              <p class="rec-ask-hint">Ask a follow-up&hellip;</p>
              <div class="rec-ask-row">
                <span class="rec-ask-tools" aria-hidden="true">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                       stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg>
                  <b>@</b>
                </span>
                <span class="rec-ask-right">
                <span class="rec-ask-send" aria-hidden="true">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"
                       stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5"/><path d="M5 12l7-7 7 7"/></svg>
                </span>
                </span>
              </div>
            </div>"""

SEARCH = ("""<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"
                     stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>""")


def shell(body):
    return ("""          <div class="rec-win rec-win--static">
%s

            <div class="rec-thread">
%s
            </div>

%s
          </div>
""" % (BAR, body, ASK))


applicant = shell("""              <div class="rec-turn rec-turn--you"><p>Who is the strongest applicant so far?</p></div>
              <div class="rec-turn rec-turn--meta">
                %s
                Matched 38 r&eacute;sum&eacute;s against the scorecard
              </div>
              <div class="rec-turn rec-turn--say"><p>Priya Nair, on every line of the scorecard but one.</p></div>
              <div class="rec-turn rec-turn--card">
                <div class="rec-who">
                  <span class="rec-who-pic" aria-hidden="true">PN</span>
                  <span class="rec-who-id">
                    <b>Priya Nair</b>
                    <i>Senior Backend Engineer</i>
                  </span>
                  <span class="rec-who-fit">92%% match</span>
                </div>
                  <div class="rec-row">
                    <span class="rec-row-k">Experience</span>
                    <span class="rec-row-v">7 yrs &middot; shipped payments at scale</span>
                    <span class="rec-row-src"><img src="logo-7.svg" alt="" loading="lazy">R&eacute;sum&eacute;</span>
                  </div>
                  <div class="rec-row">
                    <span class="rec-row-k">Based in</span>
                    <span class="rec-row-v">Bengaluru &middot; open to hybrid</span>
                    <span class="rec-row-src"><img src="logo-8.svg" alt="" loading="lazy">Careers site</span>
                  </div>
                  <div class="rec-row">
                    <span class="rec-row-k">Available</span>
                    <span class="rec-row-v">30-day notice period</span>
                    <span class="rec-row-src"><img src="logo-3.svg" alt="" loading="lazy">Screening call</span>
                  </div>
                <div class="rec-skills">
                  <span>Django</span><span>PostgreSQL</span><span>Kafka</span>
                  <span>Payments</span><span>AWS</span>
                </div>
              </div>
              <div class="rec-turn rec-turn--say"><p>The one gap is Go, which the role lists as nice to have.</p></div>
              <div class="rec-turn rec-turn--chips">
                <button type="button">Open the scorecard</button>
                <button type="button">Set up a call</button>
                <button type="button">Share with the panel</button>
              </div>""" % SEARCH)


schedule = shell("""              <div class="rec-turn rec-turn--you"><p>Book the final round with Priya</p></div>
              <div class="rec-turn rec-turn--meta">
                %s
                Read the free time of all three interviewers
              </div>
              <div class="rec-turn rec-turn--say"><p>Three slots work for the whole panel this week.</p></div>
              <div class="rec-turn rec-turn--card">
                <div class="rec-card-head">
                  <span>
                    <b>Final round &middot; Priya Nair</b>
                    <i>45 minutes &middot; 3 interviewers</i>
                  </span>
                  <span class="rec-card-count">Pick a time</span>
                </div>
                <div class="rec-slots">
                  <span class="rec-slot">
                    <b>Tue 11:00</b>
                    <i>All three free</i>
                  </span>
                  <span class="rec-slot is-pick">
                    <b>Thu 10:00</b>
                    <i>All three free</i>
                  </span>
                  <span class="rec-slot">
                    <b>Fri 16:30</b>
                    <i>Two of three</i>
                  </span>
                </div>
                  <div class="rec-row">
                    <span class="rec-row-k">Panel</span>
                    <span class="rec-row-v">Dev lead, architect, hiring manager</span>
                    <span class="rec-row-src"><img src="logo-3.svg" alt="" loading="lazy">Slack</span>
                  </div>
                <div class="rec-meet">
                  <img src="logo-4.svg" alt="" loading="lazy">
                  A Google Meet link goes out with the invite
                </div>
              </div>
              <div class="rec-turn rec-turn--say"><p>Thursday keeps the offer inside the 21-day average.</p></div>
              <div class="rec-turn rec-turn--chips">
                <button type="button">Send the invite</button>
                <button type="button">See other times</button>
                <button type="button">Add an interviewer</button>
              </div>""" % SEARCH)

start = s.index('          <div class="rec-win rec-win--static">')
end = s.index('          </div>\n          </div>\n        </section>')
assert start < end, 'static windows not found'
assert 'Who is interviewing this week?' in s[start:end], 'static window content changed'
s = s[:start] + applicant + schedule + s[end:]

# ---- what the two new answers are made of ----------------------------------
old = "    .rec-turn--chips { display:flex; flex-wrap:wrap; gap:8px; }"
new = """    /* an applicant, rather than another table of counts */
    .rec-who { display:flex; align-items:center; gap:14px; padding:14px 16px;
               background:#F7F8FA; }
    .rec-who-pic { flex:none; width:44px; height:44px; border-radius:50%;
                   display:grid; place-items:center; font-size:14.5px; font-weight:600;
                   color:#4C1D95; background:linear-gradient(140deg,#EDE7FF,#CFC2FF); }
    .rec-who-id { flex:1; min-width:0; }
    .rec-who-id b { display:block; font-size:14.5px; font-weight:600; color:#222733; }
    .rec-who-id i { display:block; margin-top:2px; font-style:normal; font-size:12.5px;
                    color:#6B7588; }
    .rec-who-fit { flex:none; font-size:12px; font-weight:600; color:#5B3DD4;
                   background:#EFE9FF; border-radius:100px; padding:5px 11px; }
    .rec-skills { display:flex; flex-wrap:wrap; gap:6px; padding:12px 16px 14px;
                  box-shadow:inset 0 1px 0 rgba(32,22,66,.08); }
    .rec-skills span { font-size:12px; color:#4E5768; background:#F1F2F6;
                       border-radius:6px; padding:5px 9px; }

    /* a time to book, rather than a list of times already booked */
    .rec-slots { display:grid; grid-template-columns:repeat(3, 1fr); gap:8px;
                 padding:14px 16px; }
    .rec-slot { border-radius:10px; padding:10px 8px; text-align:center;
                box-shadow:inset 0 0 0 1px rgba(32,22,66,.12); }
    .rec-slot b { display:block; font-size:13px; font-weight:600; color:#222733; }
    .rec-slot i { display:block; margin-top:3px; font-style:normal; font-size:11.5px;
                  color:#6B7588; }
    /* the one Mira is proposing */
    .rec-slot.is-pick { background:#F3EEFF; box-shadow:inset 0 0 0 1.5px #8B5CF6; }
    .rec-slot.is-pick b, .rec-slot.is-pick i { color:#4C1D95; }
    .rec-meet { display:flex; align-items:center; gap:9px; padding:11px 16px;
                font-size:12.5px; color:#6B7588;
                box-shadow:inset 0 1px 0 rgba(32,22,66,.08); }
    .rec-meet img { width:15px; height:15px; object-fit:contain; }

    .rec-turn--chips { display:flex; flex-wrap:wrap; gap:8px; }"""
assert old in s, 'chips rule changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('an applicant and a slot picker')
