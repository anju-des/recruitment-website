# -*- coding: utf-8 -*-
"""Where the figure came from, as chips you can open.

The provenance was a two-line grey paragraph -- the right information
in the wrong shape, read once and then in the way. It is chips now:
what the range is for, and the three places it was read from, each one
a link to that place.

The claim is the same and the check is better: a sentence naming
Glassdoor is a citation, a chip that opens Glassdoor is a source.
"""
import io
import sys

# --- what draft_pay records ------------------------------------------

EDITS = [
    # the state it keeps
    ("""    var role = { title: '', place: '', mode: '', years: '',
                 skills: '', pay: '', pay_from: '', pay_why: '',
                 questions: [], rounds: [] };""",
     """    var role = { title: '', place: '', mode: '', years: '',
                 skills: '', pay: '', pay_from: '', pay_for: '',
                 pay_refs: [], questions: [], rounds: [] };"""),

    # a figure typed over the estimate drops the chips with the claim
    ("""          if (k === 'pay' && role.pay_from === 'market') {
            // theirs now, not a market range
            role.pay_from = 'said';
            role.pay_why = '';
          }""",
     """          if (k === 'pay' && role.pay_from === 'market') {
            // theirs now, not a market range
            role.pay_from = 'said';
            role.pay_for = '';
            role.pay_refs = [];
          }"""),
]

REFS_JS = r"""
    // the pages those ranges were read from, by family
    function PAY_REFS(kind) {
      var levels = kind === 'engineering'
        ? 'https://www.levels.fyi/t/software-engineer/locations/india'
        : 'https://www.levels.fyi/t/product-designer/locations/india';
      var glass = kind === 'engineering'
        ? 'https://www.glassdoor.co.in/Salaries/india-software-engineer-salary-SRCH_IL.0,5_IN115_KO6,23.htm'
        : 'https://www.glassdoor.co.in/Salaries/india-product-designer-salary-SRCH_IL.0,5_IN115_KO6,22.htm';
      return [
        { say: 'Glassdoor', href: glass },
        { say: 'Payscale',
          href: 'https://www.payscale.com/research/IN/Country=India/Salary' },
        { say: 'Levels.fyi', href: levels }
      ];
    }
"""

CSS = """    /* a row straight under a part heading needs no rule above it:
       the heading is already the separation */
    .rec-part-head + .rec-role-row { border-top:0; padding-top:2px; }
    .rec-pay-from { display:flex; flex-wrap:wrap; align-items:center;
                    gap:6px; margin:10px 0 0; }
    .rec-pay-for { padding:4px 10px; border-radius:100px; background:#F4F2FB;
                   font-size:11.5px; color:#6B6487; }
    .rec-pay-ref { padding:4px 10px; border-radius:100px;
                   border:1px solid #E7E2F6; background:#FFFFFF;
                   font-size:11.5px; color:#6B4BE8; text-decoration:none;
                   transition:background .14s, border-color .14s; }
    .rec-pay-ref:hover { background:#F7F5FE; border-color:#BCAEF0; }
    .rec-pay-ref::after { content:"\\2197"; margin-left:4px; opacity:.6; }
"""

CSS_ANCHOR = """    .rec-part-say { margin:10px 0 0; font-size:12.5px; color:#9A93B8; }"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-pay-ref' not in s, path + ': already chipped'

    # what draft_pay records, spliced between escape-free anchors: the
    # line being replaced carries an em-dash the file stores as the
    # character, so it cannot be matched from a patch that writes —
    head = "        role.pay_from = 'market';\n"
    tail = "        return band.say;"
    at = s.index(head) + len(head)
    end = s.index(tail, at)
    assert 'pay_why' in s[at:end], (path, 'not the market branch')
    s = s[:at] + """        role.pay_for = band.kind + ' · ' +
          role.years.replace(/\\s*years?$/, '') + ' yrs · India';
        role.pay_refs = PAY_REFS(family(role.title));
""" + s[end:]

    # and the sentence under the figure, which also carries an em-dash
    head = "            (role.pay_why\n"
    tail = "          '</div>' : '') +"
    at = s.index(head)
    end = s.index(tail, at)
    s = s[:at] + """            (role.pay_from === 'market'
              ? '<p class="rec-pay-from">' +
                  '<span class="rec-pay-for">' + esc(role.pay_for) +
                  '</span>' +
                  role.pay_refs.map(function (r) {
                    return '<a class="rec-pay-ref" href="' + esc(r.href) +
                      '" target="_blank" rel="noreferrer noopener">' +
                      esc(r.say) + '</a>';
                  }).join('') +
                '</p>'
              : (role.pay ? '' :
                '<p class="rec-part-say">No published range for this one ' +
                '— add what you are paying.</p>')) +
""" + s[end:]

    old = """      role.pay_from = '';
      role.pay_why = '';
      return '';"""
    new = """      role.pay_from = '';
      role.pay_for = '';
      role.pay_refs = [];
      return '';"""
    assert s.count(old) == 1, (path, 'the empty branch', s.count(old))
    s = s.replace(old, new, 1)

    for old, new in EDITS:
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)

    mark = "    var BAND_SRC = "
    at = s.index(mark)
    end = s.index('\n', at) + 1
    s = s[:at] + s[end:] + ''
    assert 'BAND_SRC' not in s, path + ': the old source line survives'

    mark = "    // the bands are rupees a year"
    assert s.count(mark) == 1, (path, 'refs anchor', s.count(mark))
    s = s.replace(mark, REFS_JS + '\n' + mark, 1)

    assert s.count(CSS_ANCHOR) == 1, (path, 'css', s.count(CSS_ANCHOR))
    s = s.replace(CSS_ANCHOR, CSS_ANCHOR + '\n' + CSS, 1)

    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
