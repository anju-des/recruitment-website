# -*- coding: utf-8 -*-
"""Drop the portal chrome: sidebar, header bar and the Back link.

The page becomes a standalone landing page rather than a screen inside the
portal shell.
"""
import io
import re

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

anchor = "shell = shell.replace('<h1>Background Verification</h1>', '<h1>Recruitment Support</h1>')"
assert anchor in s, 'shell anchor moved'

patch = anchor + '''

# This page stands on its own, so the portal chrome comes out: the sidebar,
# the header bar, and (further down, in CONTENT) the Back link.
m = re.search(r'  <aside class="sidebar">.*?</aside>\\n', shell, re.S)
assert m, 'sidebar block not found in the shell'
shell = shell[:m.start()] + shell[m.end():]

m = re.search(r'    <header class="header">.*?</header>\\n', shell, re.S)
assert m, 'header block not found in the shell'
shell = shell[:m.start()] + shell[m.end():]'''
s = s.replace(anchor, patch, 1)

# the back link lives in this file's own CONTENT
back = ('      <a href="explore-services.html" class="rec-back">'
        '<svg viewBox="0 0 24 24"><use href="#ic-arrow-left"/></svg> Back</a>\n')
assert back in s, 'back link markup changed'
s = s.replace(back, '', 1)

# nothing sits above the hero any more
s = s.replace('"--rec-chrome:140px;", 1)', '"--rec-chrome:0px;", 1)', 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('sidebar, header and back link removed')
