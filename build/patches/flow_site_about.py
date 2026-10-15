# -*- coding: utf-8 -*-
"""A company without a Wikipedia article gets read from its own site.

Wikidata only ever holds one clause ("employer of record company in
India"), so companies without an article had nothing worth calling a
paragraph. Their own site has one: the meta description is the sentence
they wrote about themselves.

A browser cannot fetch an arbitrary site -- wisemonk.io sends no
access-control-allow-origin -- so this goes through r.jina.ai, whose
JSON response carries `description` and which does send the header when
an Origin is present. That is a third party in the path, and it sees the
domain a visitor typed. Worth knowing before this ships anywhere real.

Not taken: the readable page text. The first long paragraph on a
marketing home page is a testimonial or a call to action, and a customer
quote shown as "about the company" is worse than the one-liner it
replaced.

Six seconds and it gives up; the reader is slower than the other calls
and nobody should wait on it.
"""
import io
import sys

OLD_BUSY = """            busy = article ? 'reading about ' + who
                           : 'looking for a write-up';"""
NEW_BUSY = """            busy = article ? 'reading about ' + who
                           : 'reading ' + site;"""

OLD_READ = """        function read_about() {
          function then(text) {
            got.about = text || brief_line;
            if (!refs.length && !base.length) { rest(); return; }
            busy = 'reading the rest of the record';
            screen();
            window.setTimeout(read_more, 520);
          }
          if (!article) { then(''); return; }
          ask_json('https://en.wikipedia.org/api/rest_v1/page/summary/' +
                   encodeURIComponent(article))
            .then(function (d) { then((d && d.extract) || ''); },
                  function () { then(''); });
        }"""

NEW_READ = """        function read_about() {
          function then(text) {
            got.about = text || brief_line;
            busy = 'reading the rest of the record';
            screen();
            window.setTimeout(read_more, 520);
          }
          if (article) {
            ask_json('https://en.wikipedia.org/api/rest_v1/page/summary/' +
                     encodeURIComponent(article))
              .then(function (d) { then((d && d.extract) || ''); },
                    function () { then(''); });
            return;
          }
          // no article: read what the company says about itself
          var answered = false;
          function once(text) {
            if (answered) return;
            answered = true;
            then(text);
          }
          window.setTimeout(function () { once(''); }, 6000);
          window.fetch('https://r.jina.ai/https://' + site,
                       { headers: { 'Accept': 'application/json' } })
            .then(function (r) { return r.json(); })
            .then(function (d) {
              var dat = (d && d.data) || d || {};
              once(String(dat.description || '').trim());
            }, function () { once(''); });
        }"""


def patch(path):
    s = io.open(path, encoding='utf-8').read()
    for old, new in ((OLD_BUSY, NEW_BUSY), (OLD_READ, NEW_READ)):
        assert s.count(old) == 1, (path, old.strip()[:46], s.count(old))
        s = s.replace(old, new, 1)
    js = s[s.rindex('<script>'):]
    assert 'r.jina.ai' in js, path + ': the reader is not called'
    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


for p in sys.argv[1:]:
    patch(p)
