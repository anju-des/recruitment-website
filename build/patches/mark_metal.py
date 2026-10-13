# -*- coding: utf-8 -*-
"""The mark becomes metal: the artwork masks a polished gradient.

A filter cannot paint a sheen across a bitmap, so the image stops being an
<img> and becomes a mask over a gradient instead -- light, dark, light again,
which is what reads as polish. The extrusion has to move up to a wrapper:
filters apply before masking, so shadows set on the masked element itself
would be computed on the gradient's rectangle and then clipped away.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

old = """            <img class="rec-orb-mark" src="mira-mark.svg"
                 width="412" height="300" alt="Mira" loading="lazy">"""
new = """            <span class="rec-orb-mark" role="img" aria-label="Mira">
              <span class="rec-orb-face"></span>
            </span>"""
assert old in s, 'mark markup changed'
s = s.replace(old, new, 1)

shades = [(139, 110, 255), (128, 100, 242), (118, 90, 228), (108, 81, 213),
          (98, 72, 197), (88, 64, 180), (78, 56, 162), (68, 48, 143),
          (58, 40, 123), (48, 33, 102), (39, 26, 82), (30, 20, 62)]
body = '\n                           '.join(
    'drop-shadow(1.3px 1.7px 0 rgb(%d,%d,%d))' % c for c in shades)

start = s.index('    .rec-orb-mark { position:relative;')
end = s.index('    @media (prefers-reduced-motion: reduce) {', start)
old = s[start:end]
assert 'invert(1)' in old, 'mark rule changed'

new = """    .rec-orb-mark { position:relative; z-index:1; display:block;
                    width:min(30vmin, 210px); aspect-ratio:412 / 300;
                    transform-origin:50%% 55%%;
                    /* the body lives on the wrapper, so it is cast by the
                       masked shape rather than by the gradient's box */
                    filter:%s
                           drop-shadow(0 18px 26px rgba(10,4,32,.78))
                           drop-shadow(0 0 26px rgba(167,139,250,.34));
                    opacity:var(--mark, 0);
                    /* it turns square-on as it resolves, which is what sells
                       the body behind the face */
                    transform:perspective(900px)
                              rotateY(calc((1 - var(--mark, 0)) * -34deg))
                              rotateX(calc((1 - var(--mark, 0)) * 12deg))
                              scale(calc(0.9 + 0.1 * var(--mark, 0))); }
    /* polish is light, dark, light again across the form */
    .rec-orb-face { display:block; width:100%%; height:100%%;
                    -webkit-mask:url(mira-mark.svg) center / contain no-repeat;
                    mask:url(mira-mark.svg) center / contain no-repeat;
                    background:linear-gradient(152deg,
                      #FFFFFF 0%%, #F2EDFF 9%%, #B7A6EE 20%%, #6E5CB8 30%%,
                      #FDFBFF 42%%, #8C7ACF 54%%, #D9CEFF 64%%, #FFFFFF 73%%,
                      #7E6BC6 85%%, #EFE9FF 95%%, #FFFFFF 100%%);
                    background-size:230%% 230%%; background-position:12%% 18%%;
                    animation:rec-sheen 11s ease-in-out infinite; }
    @keyframes rec-sheen {
      0%%, 100%% { background-position:12%% 18%%; }
      50%%       { background-position:86%% 74%%; }
    }

""" % body
s = s[:start] + new + s[end:]

old = """      .rec-orb-core, .rec-orb-glow, .rec-orb-ring { transform:none; }
      .rec-orb-mark { opacity:1; transform:perspective(900px); }"""
new = """      .rec-orb-core, .rec-orb-glow, .rec-orb-ring { transform:none; }
      .rec-orb-mark { opacity:1; transform:perspective(900px); }
      .rec-orb-face { animation:none; }"""
assert old in s, 'reduced motion rule changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('the mark is metal')
