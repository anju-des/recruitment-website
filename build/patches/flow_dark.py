# -*- coding: utf-8 -*-
"""The flow goes dark.

One block appended after the flow's own rules, scoped to .rec-flow, so
nothing else on the page is touched: the hero, the bubble and the
sign-in screen stay as they are. Every override carries the .rec-flow
ancestor, which puts it a class above the rule it replaces, and the
handful that must beat .rec-flow.is-found repeat that too.

Three things that are not just colour swaps:

* the wordmark is a dark SVG and would have disappeared, so it is
  inverted to white;
* the primary button was near-black on white and would have vanished
  into the ground, so it flips to near-white on dark;
* the sand wash was light violet into blue over white. A dark page needs
  it as a glow rather than a tint, so it becomes violet bleeding into
  the background rather than onto it.
"""
import io
import sys

CSS = """
    /* ---- the flow, dark ------------------------------------------------- */
    .rec-flow { background:#0B0A12; color:#E6E3F2; }
    .rec-flow .rec-flow-head img { filter:brightness(0) invert(1); }
    .rec-flow .rec-flow-x { background:#1B1830; color:#CFC9E8; }
    .rec-flow .rec-flow-x:hover { background:#272244; color:#FFFFFF; }
    .rec-flow .rec-flow-bar { background:#1A1728; }

    /* a glow off the top rather than a tint laid over white */
    .rec-flow .rec-flow-sand::before {
      background:linear-gradient(118deg,
        rgba(124,92,246,.26), rgba(38,132,255,.14) 52%,
        rgba(11,10,18,0) 86%); }

    .rec-flow .rec-flow-q { color:#F5F3FD; }
    .rec-flow .rec-flow-hint { color:#A49CC6; }
    .rec-flow .rec-flow-in { background:#15131F; border-color:#2C2742;
                             color:#F2F0FA; }
    .rec-flow .rec-flow-in::placeholder { color:#6F688C; }

    /* near-black on dark is no button at all */
    .rec-flow .rec-flow-next { background:#F2F0FA; color:#14111F; }
    .rec-flow .rec-flow-next:hover { background:#FFFFFF; }
    .rec-flow .rec-flow-next[disabled] { background:#F2F0FA; opacity:.22; }
    .rec-flow .rec-flow-back { color:#A49CC6; }
    .rec-flow .rec-flow-back:hover { color:#FFFFFF; }
    .rec-flow .rec-flow-again { background:#15131F; border-color:#332E4C;
                                color:#D9D4EC; }
    .rec-flow .rec-flow-again:hover { background:#1E1A2E;
                                      border-color:#4C3F7A; color:#FFFFFF; }
    .rec-flow .rec-flow-skip { color:#8F88AE; }
    .rec-flow .rec-flow-skip:hover { color:#E6E3F2; }

    .rec-flow .rec-step { color:#7E7799; }
    .rec-flow .rec-step i { background:#1C1930; color:#8F88AE; }
    .rec-flow .rec-step.is-on { color:#F5F3FD; }
    .rec-flow .rec-step.is-done { color:#B4ADCE; }
    .rec-flow .rec-step.is-done i { background:#2A2342; color:#B9A8F5; }
    .rec-flow .rec-step + .rec-step::before { background:#2A2640; }

    .rec-flow .rec-done-card { background:#15131F; border-color:#2C2742;
                               box-shadow:0 1px 8px rgba(0,0,0,.3); }
    .rec-flow .rec-done-card b { color:#F2F0FA; }
    .rec-flow .rec-done-card:hover { border-color:#4C3F7A;
                                     box-shadow:0 2px 14px rgba(0,0,0,.4); }
    .rec-flow:not(.is-found) .rec-done-card { border-color:#5B49A0; }
    .rec-flow .rec-done-go { color:#7E7799; }

    .rec-flow .rec-found-card,
    .rec-flow.is-found .rec-found-card { background:#15131F;
                                         border-color:#262238;
                                         box-shadow:0 2px 18px
                                                    rgba(0,0,0,.34); }
    .rec-flow .rec-flow-found-say b { color:#F5F3FD; }
    .rec-flow .rec-flow-found-say i { color:#8880A8; }
    .rec-flow .rec-flow-found-badge { background:#241E3C; color:#B9A8F5; }
    .rec-flow .rec-found-about { color:#ADA6C8; }
    .rec-flow .rec-found-about.is-thin { color:#8880A8; }
    .rec-flow .rec-found-facts span { background:#1B1829; }
    .rec-flow .rec-found-facts i { color:#8880A8; }
    .rec-flow .rec-found-facts b { color:#F2F0FA; }
    .rec-flow .rec-found-links a { background:#15131F; border-color:#2E2944;
                                   color:#B9A8F5; }
    .rec-flow .rec-found-links a:hover { background:#1E1A2E;
                                         border-color:#4C3F7A; }

    .rec-flow .rec-work { color:#9C95BC; }
    .rec-flow .rec-work-head { color:#F2F0FA; }
    .rec-flow .rec-work-line.is-done { color:#7E7799; }
    .rec-flow .rec-work-line.is-now { color:#F2F0FA; }
    .rec-flow .rec-work-line.is-now b { background:#F2F0FA; }
    .rec-flow .rec-tell { color:#F2F0FA; }
    .rec-flow .rec-tell b { background:#F2F0FA; }

    .rec-flow .rec-board-role { background:#1B1829; }
    .rec-flow .rec-board-role b { color:#F2F0FA; }
    .rec-flow .rec-board-role i { color:#8880A8; }
    .rec-flow .rec-ready li { border-top-color:#262238; }
    .rec-flow .rec-ready i { color:#8880A8; }
    .rec-flow .rec-ready b { color:#F2F0FA; }
"""

ANCHOR = "    /* ---- Mira in the corner ---"


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'the flow, dark' not in s, path + ': already dark'
    assert s.count(ANCHOR) == 1, (path, 'anchor', s.count(ANCHOR))
    s = s.replace(ANCHOR, CSS.lstrip('\n') + '\n' + ANCHOR, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
