# -*- coding: utf-8 -*-
"""Two things the narrow layout showed up.

  * Gmail and Outlook drew the same envelope, which reads as a mistake when
    they sit side by side -- Outlook becomes an inbox tray.
  * In the stacked fallback the tile row landed above the heading; the copy
    should lead, so it takes order:-1.
"""
import io

p = 'build_recruitment_page.py'
s = io.open(p, encoding='utf-8').read()

old = """            <div class="rec-tile rec-tile--d1" style="left:7%; top:48%">
              <svg viewBox="0 0 24 24"><use href="#ic-sms"/></svg>
              <span>Outlook</span>"""
new = """            <div class="rec-tile rec-tile--d1" style="left:7%; top:48%">
              <svg viewBox="0 0 24 24"><use href="#ic-direct-inbox"/></svg>
              <span>Outlook</span>"""
assert old in s, 'Outlook tile changed'
s = s.replace(old, new, 1)

# the icon list the builder inlines from the sprite
old = "NEEDED = ['ic-calendar', 'ic-cpu',"
assert old in s, 'tile icon list moved'
s = s.replace(old, "NEEDED = ['ic-calendar', 'ic-cpu', 'ic-direct-inbox',", 1)

old = '      .rec-integrations-copy { padding:0; }\n'
new = '      .rec-integrations-copy { padding:0; order:-1; }\n'
assert old in s, 'responsive copy rule changed'
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('Outlook icon swapped; copy leads in the stacked layout')
