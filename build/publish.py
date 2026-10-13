# -*- coding: utf-8 -*-
"""Copy a freshly built page into this repo, with the one edit it needs.

    python build/publish.py ../EOR/docs

The builder writes the page for the EOR docs portal, where the header logo
links back to that portal's index. Here there is no such page, so the link is
rewritten to `./`. Doing it by hand was forgotten once already, which is the
only reason this script exists.

Every asset the page names is copied too -- including the ones a `src="..."`
scan misses, because the stylesheet arrives through a <link> and three of the
logos are named only inside CSS url() masks.
"""
import io
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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


def main(src_dir):
    page = os.path.join(src_dir, 'recruitment-copy.html')
    html = io.open(page, encoding='utf-8').read()

    # the portal back-link has nowhere to go once the page is on its own
    html = html.replace('<a class="rec-logo" href="explore-services.html">',
                        '<a class="rec-logo" href="./">')

    io.open(os.path.join(HERE, 'index.html'), 'w', encoding='utf-8').write(html)

    missing = []
    for rel in referenced(html):
        src = os.path.join(src_dir, rel)
        if not os.path.isfile(src):
            missing.append(rel)
            continue
        dst = os.path.join(HERE, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)
        print('copied', rel)

    if missing:
        print('\nMISSING from', src_dir + ':')
        for m in missing:
            print(' ', m)
        return 1
    print('\nindex.html and every asset it names are in place')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else '../EOR/docs'))
