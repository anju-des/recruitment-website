# -*- coding: utf-8 -*-
"""Undo a bad slice, then make the edit it was supposed to make.

fix_duties.py cut from the as_duty comment to draft_rounds -- but
draft_rounds is defined first, so the slice ran backwards, came out
empty, and str.replace('', new, 1) put the block at the very start of
the file. Python then read JavaScript as its first line.

The stray block comes off, and as_duty is replaced where it actually
lives: from its own comment to the function after it.
"""
import io

p = 'jd_publish_step.py'
s = io.open(p, encoding='utf-8').read()

# the block that landed at the top, before the file's own first line
head = s.index('# -*- coding: utf-8 -*-')
stray = s[:head]
assert 'function as_duty' in stray, 'nothing stray at the top'
s = s[head:]
print('removed', len(stray), 'characters from the top')

NEW_DUTY = '''    // A bullet reads "Own the journey: from user flows to polished UI".
    // The verb phrase is the label; the gloss is what follows it.
    function as_duty(line) {
      var s = String(line || '').replace(/[.\\s\\u2013\\u2014-]+$/, '').trim();
      if (!s) return null;
      // the advert talking about itself, not the work
      if (/^(?:we|our|this role|the role|as a|join)\\b/i.test(s)) return null;
      var head = s;
      var tail = '';
      var cut = s.indexOf(':');
      if (cut > 0 && cut < 44) {
        head = s.slice(0, cut).trim();
        tail = s.slice(cut + 1).trim().split(/,|\\u2014| and /)[0].trim();
      }
      head = head.replace(/^[A-Z]/, function (c) { return c.toLowerCase(); });
      tail = tail.replace(/^[A-Z]/, function (c) { return c.toLowerCase(); });
      if (head.length < 8 || head.length > 90) return null;
      return { head: head, tail: tail.length > 70 ? '' : tail };
    }

'''

start = s.index('    // a duty, turned back into the sentence a person would say')
end = s.index('    // every question is assembled out of the document', start)
assert end > start, 'the slice still runs backwards'
s = s[:start] + NEW_DUTY + s[end:]

assert s.count('function as_duty') == 1, 'two as_duty definitions'
assert 'as_duty(line) {\n      var s = String(line || \'\')' in s
io.open(p, 'w', encoding='utf-8').write(s)
print('as_duty replaced in place')
