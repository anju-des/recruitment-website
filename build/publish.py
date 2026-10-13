# -*- coding: utf-8 -*-
"""Copy a freshly built page into this repo — live, or into the preview.

    python build/publish.py ../EOR/docs              # -> /
    python build/publish.py ../EOR/docs --preview    # -> /preview/
    python build/publish.py --promote                # preview -> live

Pages serves one branch from one root, so the testing environment is a folder
rather than a second deployment: the preview is a self-contained copy under
`preview/`, served at <site>/preview/. Self-contained rather than sharing the
parent's assets — git stores identical blobs once, and a copy cannot break on
a path rewrite the way a shared one can.

The builder writes the page for the EOR docs portal, where the header logo
links back to that portal's index. Here there is no such page, so the link is
rewritten to `./`. Doing it by hand was forgotten once already, which is the
only reason this script exists.

Every asset the page names is copied too — including the ones a `src="..."`
scan misses, because the stylesheet arrives through a <link> and three of the
logos are named only inside CSS url() masks.
"""
import io
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PREVIEW = os.path.join(HERE, 'preview')

# A corner marker, so a preview tab is never mistaken for the live one. Fixed
# and tiny: it must not take part in the layout being judged.
BADGE = """<style>
  .rec-preview-flag { position:fixed; z-index:99; left:10px; bottom:10px;
    font:600 10px/1 ui-sans-serif,system-ui,sans-serif; letter-spacing:.08em;
    text-transform:uppercase; color:#fff; background:#F04438;
    border-radius:100px; padding:5px 9px; opacity:.85; pointer-events:none; }
</style>
<div class="rec-preview-flag">Preview</div>
"""


def referenced(html):
    """Every local file the page asks for, however it asks for it."""
    found = set()
    for pat in (r'src="([^"]+)"', r'href="([^"]+)"', r'url\(["\']?([^"\')]+)'):
        found.update(re.findall(pat, html))
    return sorted(
        f for f in found
        # %23 is an encoded '#': a fragment inside an inlined data URI,
        # not a file sitting next to the page
        if not f.startswith(('data:', 'http', '#', '%23', './', '/'))
    )


def write(html, src_dir, out_dir, badge):
    os.makedirs(out_dir, exist_ok=True)
    if badge:
        html = html.replace('</body>', BADGE + '</body>')
    io.open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8').write(html)

    missing = []
    for rel in referenced(html):
        src = os.path.join(src_dir, rel)
        if not os.path.isfile(src):
            missing.append(rel)
            continue
        dst = os.path.join(out_dir, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)
    if missing:
        print('MISSING from ' + src_dir + ':')
        for m in missing:
            print(' ', m)
        return 1
    print('wrote', os.path.relpath(out_dir, HERE) or '/', '+',
          len(referenced(html)), 'assets')
    return 0


def promote():
    """Move what is in preview to live, dropping the marker on the way."""
    page = os.path.join(PREVIEW, 'index.html')
    if not os.path.isfile(page):
        print('nothing in preview/ to promote')
        return 1
    html = io.open(page, encoding='utf-8').read()
    html = html.replace(BADGE, '')
    return write(html, PREVIEW, HERE, badge=False)


def main(argv):
    if '--promote' in argv:
        return promote()
    preview = '--preview' in argv
    src_dir = next((a for a in argv if not a.startswith('--')), '../EOR/docs')
    html = io.open(os.path.join(src_dir, 'recruitment-copy.html'),
                   encoding='utf-8').read()
    # the portal back-link has nowhere to go once the page is on its own
    html = html.replace('<a class="rec-logo" href="explore-services.html">',
                        '<a class="rec-logo" href="./">')
    return write(html, src_dir, PREVIEW if preview else HERE, badge=preview)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
