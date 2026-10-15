# -*- coding: utf-8 -*-
"""Just ask the question.

The prompt is two sentences now. No labels, no "reply with exactly these
lines", no telling Claude what not to do -- a form sent to someone who
already knows the answer.

Which means the reply comes back as prose, so the page stops depending on
labels. It still reads them when they are there (Claude formats unasked
often enough), and otherwise finds the one thing in free text worth
finding: the domain. The domain carries the logo, the link, and a
serviceable company name -- wisemonk.io is Wisemonk -- so a plain
paragraph still builds the card.

If there is no domain in the reply the card still appears with the text,
just without a mark or a link. Something beats nothing on a card whose
whole job is to say who this is.
"""
import io
import sys

OLD_PROMPT = """    // four lines: who they are and which company. The rest is looked up.
    var PROMPT = [
      'I am briefing a role to Wisemonk\\'s AI recruiter, Mira. Tell it who I ' +
        'am and which company I work for.',
      '',
      'Reply with exactly these four lines and nothing else:',
      '',
      'Company:',
      'Website:',
      'Name:',
      'Role:',
      '',
      'Website is the company domain on its own, like example.com. Name and ' +
        'Role are mine.',
      '',
      'Use what you already know, and leave a value empty if you do not know ' +
        'it. Do not describe the company \\u2014 the name and the domain are ' +
        'all that is wanted.',
      '',
      'No preamble, no extra lines, no questions.'
    ].join('\\n');"""

NEW_PROMPT = """    // the whole prompt. Anything more is a form sent to someone who already
    // knows the answer.
    var PROMPT = [
      'Tell me about yourself and your company.',
      '',
      'I am briefing a role to Wisemonk\\'s AI recruiter, Mira, and it should ' +
        'know who it is hiring for.'
    ].join('\\n');"""

OLD_READ = """    function host(w) {"""

NEW_READ = """    // in free text the domain is the one thing worth finding: it carries the
    // logo, the link, and a serviceable name for the company
    var A_DOMAIN = /\\b((?:[a-z0-9][a-z0-9-]*\\.)+[a-z]{2,12})\\b/i;

    function named(domain) {
      var core = domain.split('.')[0].replace(/[-_]+/g, ' ');
      return core.charAt(0).toUpperCase() + core.slice(1);
    }

    // labels when Claude writes them, prose when it does not
    function shape(text) {
      var co = read(text);
      if (co.company || co.website) return co;

      var raw = String(text || '').trim();
      if (!raw) return {};
      var found = raw.match(A_DOMAIN);
      var site = found ? host(found[1]) : '';
      return { company: site ? named(site) : '', website: site, about: raw };
    }

    function host(w) {"""

OLD_WIRE = """        var co = read(box.value);
        if (co.company) { keep(co); show(co); }"""

NEW_WIRE = """        var co = shape(box.value);
        if (co.company || co.about) { keep(co); show(co); }"""

OLD_MARK = """        '<span class="rec-co-mark">' + esc((co.company || '?').charAt(0)) +
        '</span>' +"""

NEW_MARK = """        '<span class="rec-co-mark">' + esc((co.company || '').charAt(0)) +
        '</span>' +"""

OLD_CSS = """    .rec-co-about { margin:5px 0 0; font-size:13.5px; line-height:1.55;
                    color:var(--text-secondary); }"""

NEW_CSS = """    .rec-co-about { margin:5px 0 0; font-size:13.5px; line-height:1.55;
                    color:var(--text-secondary);
                    /* prose can run long; the whole of it is still stored */
                    display:-webkit-box; -webkit-line-clamp:5;
                    -webkit-box-orient:vertical; overflow:hidden; }"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for old, new in ((OLD_PROMPT, NEW_PROMPT), (OLD_READ, NEW_READ),
                     (OLD_WIRE, NEW_WIRE), (OLD_MARK, NEW_MARK),
                     (OLD_CSS, NEW_CSS)):
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    cut = s[s.index('var PROMPT'):s.index(".join('\\n');")]
    for gone in ("'Company:'", 'exactly these', 'No preamble'):
        assert gone not in cut, path + ': the form survives: ' + gone
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
