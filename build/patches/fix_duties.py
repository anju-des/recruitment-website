# -*- coding: utf-8 -*-
"""Responsibilities are bullets, not the paragraph above them.

`duties` took whichever heading came first, and "Role Overview" comes
before "Key Responsibilities" -- so the duty it offered was the opening
sentence of the advert: "We're looking for a Product Designer who owns
the product experience end-to-end". Pasted into a question that was
expecting a verb phrase, it read "This role asks you to we're looking
for a Product Designer".

It asks for the responsibilities and only falls back to the overview
when a job description has none.

And a bullet is written "Own the journey: from user flows to polished
UI" -- the verb phrase is the label, the part after the colon is the
gloss. The question wants the label.
"""
import io

# --- the parser asks for the right section ---------------------------

p = 'jd-parse.js'
s = io.open(p, encoding='utf-8').read()

old = """      duties: section(ls, ['key responsibilities', 'responsibilities',
                           'what you(?:\\'| wi)ll do', 'the role', 'role overview']),"""
new = """      // the bullets if there are any, the overview only if there are not
      duties: section(ls, ['key responsibilities', 'responsibilities',
                           'what you(?:\\'| wi)ll do']).length
        ? section(ls, ['key responsibilities', 'responsibilities',
                       'what you(?:\\'| wi)ll do'])
        : section(ls, ['the role', 'role overview']),"""
assert s.count(old) == 1, ('duties', s.count(old))
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new, 1))
print('parser: responsibilities first')

# --- the question uses the verb phrase, not the gloss ----------------

p = 'jd_publish_step.py'
s = io.open(p, encoding='utf-8').read()

old = s[s.index("    // a duty, turned back into the sentence a person would say"):
        s.index("    function draft_rounds() {")]

new = '''    // A bullet reads "Own the journey: from user flows to polished UI".
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
s = s.replace(old, new, 1)

old = """      var duties = (jd && jd.duties) || [];
      for (var i = 0; i < duties.length && out.length < 2; i++) {
        var d = as_duty(duties[i]);
        if (d.length > 24 && d.length < 140) {
          out.push('This role asks you to ' + d +
                   '. When have you done that, and how did it go?');
        }
      }"""
new = """      var duties = (jd && jd.duties) || [];
      for (var i = 0; i < duties.length && out.length < 2; i++) {
        var d = as_duty(duties[i]);
        if (!d) continue;
        out.push('This role asks you to ' + d.head +
                 (d.tail ? ' \\u2014 ' + d.tail : '') +
                 '. When have you done that, and how did it go?');
      }"""
assert s.count(old) == 1, ('question two', s.count(old))
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('question: the verb phrase')
