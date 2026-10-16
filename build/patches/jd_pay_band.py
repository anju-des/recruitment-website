# -*- coding: utf-8 -*-
"""Pay gets a number, and the number gets a source.

A figure invented on the spot and labelled "current market rate" is a
claim made to every visitor that this page knows the market. It does
not, and an employer who believes it pays for the mistake.

So the number is real: published ranges, looked up, written down with
the date they were read and the sites they came from, and shown with
what they are a range *for* -- this family, this experience, this
country. The screen says so, and says to replace them with the
company's own placement data.

Where there is no band -- a family nobody has figures for here, a
country other than India, an experience the document never stated --
it asks instead of reaching. And a job description that states pay
beats all of it: that one is not an estimate at all.

The figures: design 0-3 7-13, 4-6 14-25, 7+ 22-40 LPA; engineering
0-3 8-18, 4-6 18-32, 7+ 32-55 LPA. Read 16 October 2026 from Glassdoor
India, Payscale, Levels.fyi and published 2026 salary guides, which
disagree with each other by a lot -- these are the middles of what they
say, for product companies rather than services firms.
"""
import io
import sys

BANDS_JS = r"""
    // Published ranges, read 16 October 2026 (Glassdoor India, Payscale,
    // Levels.fyi and 2026 salary guides). They disagree with each other by
    // a wide margin; these are the middle of what they say, for product
    // companies rather than services firms. The screen says as much, and
    // says to replace them.
    var BANDS = {
      design: [
        { upto: 3, say: '₹7–13 LPA' },
        { upto: 6, say: '₹14–25 LPA' },
        { upto: 99, say: '₹22–40 LPA' }
      ],
      engineering: [
        { upto: 3, say: '₹8–18 LPA' },
        { upto: 6, say: '₹18–32 LPA' },
        { upto: 99, say: '₹32–55 LPA' }
      ]
    };

    var BAND_SRC = 'Glassdoor, Payscale and Levels.fyi, read October 2026';

    // the bands are rupees a year: anywhere else and they say nothing
    var IN_INDIA = /\b(india|bengaluru|bangalore|mumbai|delhi|gurugram|gurgaon|noida|hyderabad|pune|chennai|kolkata|ahmedabad|jaipur|kochi|indore|chandigarh|trivandrum|thiruvananthapuram|coimbatore)\b/i;

    function years_as_number(said) {
      var m = String(said || '').match(/(\d{1,2})\s*(?:[-–—]|to)\s*(\d{1,2})/);
      if (m) return Number(m[2]);
      m = String(said || '').match(/(\d{1,2})/);
      return m ? Number(m[1]) : 0;
    }

    // a range for this family, this experience, this country -- or nothing
    function market_band() {
      var where = (role.place || '') + ' ' + ((company && company.based) || '');
      if (!IN_INDIA.test(where)) return null;
      var rows = BANDS[family(role.title)];
      if (!rows) return null;
      var n = years_as_number(role.years);
      if (!n) return null;
      for (var i = 0; i < rows.length; i++) {
        if (n <= rows[i].upto) {
          return { say: rows[i].say, n: n,
                   kind: family(role.title) === 'design' ? 'product design'
                                                         : 'engineering' };
        }
      }
      return null;
    }
"""

# draft_pay keeps reading the document first, then falls back to the band
OLD_PAY_HEAD = "    // what the job description says about pay, which is often nothing"
# draft_pay is the last of the drafting helpers; the wiring follows it
OLD_PAY_TAIL = "    // re-injected HTML brings no listeners"

NEW_PAY = r"""    // what the job description says about pay, which is often nothing
    function draft_pay() {
      var text = (jd && jd.text) || '';
      var m = text.match(
        /(?:₹|INR|Rs\.?|\$|USD)\s?[\d,.]+\s?(?:[-–to]+\s?(?:₹|INR|Rs\.?|\$|USD)?\s?[\d,.]+)?\s*(?:LPA|lakh|lakhs|per annum|a year|\/year|k)?/i);
      if (m && /\d/.test(m[0])) {
        role.pay_from = 'said';
        return m[0].trim();
      }
      var band = market_band();
      if (band) {
        role.pay_from = 'market';
        role.pay_why = 'Typical for ' + band.kind + ' at ' +
          role.years.replace(/\s*years?$/, '') + ' years in India — ' +
          BAND_SRC + '. Replace it with your own placement data.';
        return band.say;
      }
      role.pay_from = '';
      role.pay_why = '';
      return '';
    }

"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    assert 'market_band' not in s, path + ': already has a band'

    # the state the pay row keeps about itself
    old = ("    var role = { title: '', place: '', mode: '', years: '',\n"
           "                 skills: '', pay: '', questions: [], rounds: [] };")
    new = ("    var role = { title: '', place: '', mode: '', years: '',\n"
           "                 skills: '', pay: '', pay_from: '', pay_why: '',\n"
           "                 questions: [], rounds: [] };")
    assert s.count(old) == 1, (path, 'role state', s.count(old))
    s = s.replace(old, new, 1)

    # the bands, next to the other things the step drafts from
    mark = "    // what the job description says about pay, which is often nothing"
    assert s.count(mark) == 1, (path, 'bands anchor', s.count(mark))
    s = s.replace(mark, BANDS_JS + '\n' + mark, 1)

    at = s.index(OLD_PAY_HEAD, s.index('var BANDS'))
    end = s.index(OLD_PAY_TAIL, at)
    assert end > at, (path, 'the pay slice runs backwards')
    s = s[:at] + NEW_PAY + s[end:]

    # and what the screen says about it
    old = """            '<h3 class="rec-part-head">Pay' +
              '<span>' + (role.pay
                ? 'as the job description states it'
                : 'the job description does not say') + '</span></h3>' +
            '<div class="rec-role-row"><i>Salary</i>' +
              '<input class="rec-role-in" data-k="pay" value="' +
                esc(role.pay || '') + '" placeholder="' +
                'Add what you are paying"></div>' +
            (role.pay ? '' :
              '<p class="rec-part-say">Mira can estimate this once your own ' +
              'placement data is behind it. It will not guess one.</p>') +"""
    new = """            '<h3 class="rec-part-head">Pay' +
              '<span>' + (role.pay_from === 'said'
                ? 'as the job description states it'
                : role.pay_from === 'market'
                  ? 'the job description does not say, so: the market'
                  : 'the job description does not say') + '</span></h3>' +
            '<div class="rec-role-row"><i>Salary</i>' +
              '<input class="rec-role-in" data-k="pay" value="' +
                esc(role.pay || '') + '" placeholder="' +
                'Add what you are paying"></div>' +
            (role.pay_why
              ? '<p class="rec-part-say">' + esc(role.pay_why) + '</p>'
              : (role.pay ? '' :
                '<p class="rec-part-say">No published range for this one ' +
                'here. Add what you are paying — Mira will not guess ' +
                'a number.</p>')) +"""
    assert s.count(old) == 1, (path, 'the pay row', s.count(old))
    s = s.replace(old, new, 1)

    # a figure typed over the estimate is no longer the estimate
    old = """          var k = box.getAttribute('data-k');
          role[k] = box.value;"""
    new = """          var k = box.getAttribute('data-k');
          role[k] = box.value;
          if (k === 'pay' && role.pay_from === 'market') {
            // theirs now, not a market range
            role.pay_from = 'said';
            role.pay_why = '';
          }"""
    assert s.count(old) == 1, (path, 'pay edit', s.count(old))
    s = s.replace(old, new, 1)

    # the line it says while drafting
    old = "          { say: 'reading the job description for pay',"
    new = "          { say: 'working out what this should pay',"
    assert s.count(old) == 1, (path, 'the line', s.count(old))
    s = s.replace(old, new, 1)

    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
