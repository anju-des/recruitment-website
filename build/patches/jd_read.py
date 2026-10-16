# -*- coding: utf-8 -*-
"""A job description is a second way into the flow.

The composer stays the headline: describing the role in a sentence is
the lower-effort start. Underneath it, for people who already have the
document open, a quieter door -- drop a file, choose one, or paste.

Everything here happens in the browser. A PDF is read by pdf.js, which
is fetched once and only when a PDF is actually dropped; text files need
nothing at all. Nothing is uploaded, which is the only reason the line
under the drop zone can say so.

The reader rebuilds lines from the text items' y positions rather than
joining them end to end, because the parser that reads the result works
on lines: "Job Title:" has to still be at the start of one.

This file adds the reading and the parsing. What the flow does with the
result comes next.
"""
import io
import sys

MARKUP = """              <div class="rec-drop">
                <input type="file" class="rec-drop-in" hidden
                       accept=".pdf,.txt,.md,.text,application/pdf,text/plain">
                <button type="button" class="rec-drop-go">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
                       stroke-width="1.8" stroke-linecap="round"
                       stroke-linejoin="round" aria-hidden="true">
                    <path d="M14 3v4a1 1 0 0 0 1 1h4"/>
                    <path d="M19 8v10a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h7z"/>
                    <path d="M9 13h6M9 17h4"/>
                  </svg>
                  <span>Have a job description? <b>Drop it here</b></span>
                </button>
                <p class="rec-drop-say">PDF or text. Read in your browser &mdash;
                  the file never leaves it.</p>
              </div>
"""

CSS = """    /* the second door: quieter than the composer on purpose */
    .rec-drop { margin:14px auto 0; width:100%; max-width:820px;
                text-align:center; }
    .rec-drop-go { display:inline-flex; align-items:center; gap:9px;
                   padding:10px 18px; border-radius:100px; cursor:pointer;
                   border:1px dashed #CFD6E4; background:rgba(255,255,255,.6);
                   font:inherit; font-size:14px; color:#5C6779;
                   transition:border-color .15s, color .15s, background .15s; }
    .rec-drop-go svg { width:17px; height:17px; flex:none; }
    .rec-drop-go b { font-weight:600; color:#4B3BC8; }
    .rec-drop-go:hover { border-color:#A9B4C9; background:#FFFFFF;
                         color:#3A4556; }
    .rec-drop-go:focus-visible { outline:2px solid #7C5CF6;
                                 outline-offset:3px; }
    .rec-drop-say { margin:9px 0 0; font-size:12px; color:#94a3b8; }
    .rec-drop.is-over .rec-drop-go { border-style:solid; border-color:#7C5CF6;
                                     background:#FFFFFF; color:#1A1430; }
    .rec-drop.is-bad .rec-drop-go { border-color:#E3A0A0; color:#B4443C; }
    .rec-drop-err { margin:9px 0 0; font-size:12.5px; color:#B4443C; }
    .rec-drop-err[hidden] { display:none; }
    /* a long paste is probably a JD, but that is the visitor's call */
    .rec-drop-ask { display:inline-flex; align-items:center; gap:8px;
                    margin:10px 0 0; padding:8px 14px; border-radius:100px;
                    border:1px solid #D8CFF8; background:#F6F3FF;
                    font:inherit; font-size:13px; color:#4B3BC8;
                    cursor:pointer; }
    .rec-drop-ask[hidden] { display:none; }
    .rec-drop-ask:hover { background:#EFEAFF; }
    @media (max-width:640px) {
      .rec-drop-go { font-size:13px; padding:9px 14px; }
    }
"""

CSS_ANCHOR = "    .rec-compose-wrap { width:100%; max-width:820px; margin:48px auto 0; }"

MARKUP_ANCHOR = """              </form>
"""

# the reader and the parser, as one block of the page's own script
JS = r"""
  // ---- reading a job description, in the browser ----------------------

  var PDFJS_SRC = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/' +
                  'pdf.min.js';
  var PDFJS_WORKER = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/' +
                     '3.11.174/pdf.worker.min.js';
  var pdfjs_wait = null;

  // fetched once, and only when a PDF is actually dropped
  function pdfjs() {
    if (pdfjs_wait) return pdfjs_wait;
    pdfjs_wait = new Promise(function (ok, no) {
      var s = document.createElement('script');
      s.src = PDFJS_SRC;
      s.onload = function () {
        var lib = window.pdfjsLib;
        if (!lib) { no(new Error('pdf reader did not load')); return; }
        lib.GlobalWorkerOptions.workerSrc = PDFJS_WORKER;
        ok(lib);
      };
      s.onerror = function () { no(new Error('pdf reader did not load')); };
      document.head.appendChild(s);
    });
    return pdfjs_wait;
  }

  // text items carry their position, so the lines can be put back the way
  // they were written. The parser downstream reads lines, not a paragraph.
  function pdf_lines(items) {
    var rows = [];
    var at = null;
    var y = null;
    for (var i = 0; i < items.length; i++) {
      var it = items[i];
      var ty = it.transform ? Math.round(it.transform[5]) : 0;
      if (y === null || Math.abs(ty - y) > 3) {
        if (at !== null) rows.push(at);
        at = '';
        y = ty;
      }
      at += it.str;
      if (it.hasEOL) { rows.push(at); at = ''; y = null; }
    }
    if (at !== null && at !== '') rows.push(at);
    return rows.join('\n');
  }

  var JD_MAX = 8 * 1024 * 1024;
  var JD_PAGES = 12;

  // resolves to text, or rejects with something worth showing a person
  function read_jd(file) {
    if (!file) return Promise.reject(new Error('no file'));
    if (file.size > JD_MAX) {
      return Promise.reject(new Error('That file is over 8MB — try the ' +
        'text, or a smaller export.'));
    }
    var name = (file.name || '').toLowerCase();
    if (/\.(txt|md|text)$/.test(name) || file.type === 'text/plain') {
      return file.text();
    }
    if (/\.docx?$/.test(name)) {
      return Promise.reject(new Error('I can’t read Word files yet — ' +
        'paste the text, or export it as a PDF.'));
    }
    if (!/\.pdf$/.test(name) && file.type !== 'application/pdf') {
      return Promise.reject(new Error('That looks like a ' +
        (name.split('.').pop() || 'file') + '. I can read a PDF or text.'));
    }
    return file.arrayBuffer().then(function (buf) {
      return pdfjs().then(function (lib) {
        return lib.getDocument({ data: buf }).promise;
      }).then(function (doc) {
        var n = Math.min(doc.numPages, JD_PAGES);
        var want = [];
        for (var i = 1; i <= n; i++) want.push(i);
        return Promise.all(want.map(function (i) {
          return doc.getPage(i).then(function (p) {
            return p.getTextContent();
          }).then(function (c) { return pdf_lines(c.items); });
        })).then(function (pages) {
          var text = pages.join('\n');
          // a scan has no text layer, and no amount of trying changes that
          if (text.replace(/\s/g, '').length < 60) {
            throw new Error('That PDF has no text in it — a scan, most ' +
              'likely. Paste the text instead?');
          }
          return text;
        });
      });
    });
  }
"""

PARSE_JS_MARK = "  // ---- reading a job description, in the browser ---------"


def patch(path, parser_js):
    s = io.open(path, encoding='utf-8').read()
    assert 'rec-drop-go' not in s, path + ': already has the door'

    assert s.count(MARKUP_ANCHOR) >= 1, (path, 'form end')
    # the composer's own closing tag, the first one in the hero
    at = s.index('<form class="rec-compose"')
    end = s.index(MARKUP_ANCHOR, at) + len(MARKUP_ANCHOR)
    s = s[:end] + MARKUP + s[end:]

    assert s.count(CSS_ANCHOR) == 1, (path, 'css', s.count(CSS_ANCHOR))
    s = s.replace(CSS_ANCHOR, CSS_ANCHOR + '\n' + CSS, 1)

    mark = "  // the hero's composer, wired at load;"
    assert s.count(mark) == 1, (path, 'js anchor', s.count(mark))
    s = s.replace(mark, JS + '\n' + parser_js + '\n' + mark, 1)

    io.open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)


def as_page_js(src):
    """The parser, inlined whole.

    Its own closure stays on: the page's script is long and the parser's
    names -- lines, first, site, mode, parse -- are exactly the kind that
    collide. It hands out one name, window.jdParse, as it already does.
    """
    out = ['  // ---- what a job description says, read with rules ---------'
           '-------']
    for line in src.rstrip().split('\n'):
        out.append(('  ' + line).rstrip() if line.strip() else '')
    return '\n'.join(out) + '\n'


if __name__ == '__main__':
    parser = io.open('jd-parse.js', encoding='utf-8').read()
    js = as_page_js(parser)
    for p in sys.argv[1:]:
        patch(p, js)
