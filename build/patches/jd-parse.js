// Reading a job description with rules, not a model.
//
// Everything here is a guess with a reason behind it. A field it is not
// sure of comes back empty, because an empty field asks and a wrong one
// lies -- and every field it does fill is editable on screen before it
// is used for anything.

(function (root) {
  'use strict';

  // --- small helpers -------------------------------------------------

  function tidy(s) {
    return String(s || '')
      .replace(/ /g, ' ')
      .replace(/[‘’]/g, "'")
      .replace(/[“”]/g, '"')
      .replace(/[ \t]+/g, ' ')
      .trim();
  }

  // the bullet glyphs and the zero-width joiner Google Docs leaves behind
  function lines(text) {
    return String(text || '')
      .replace(/​|‍|﻿/g, '')
      .split(/\r?\n/)
      .map(function (l) { return tidy(l.replace(/^[●•▪\-*]\s*/, '')); })
      .filter(function (l) { return l.length > 0; });
  }

  function first(text, res, pick) {
    for (var i = 0; i < res.length; i++) {
      var m = text.match(res[i]);
      if (m) return tidy(m[pick || 1]);
    }
    return '';
  }

  // --- title ---------------------------------------------------------

  var TITLE_WORDS = /(engineer|developer|designer|manager|analyst|scientist|architect|consultant|specialist|lead|head|director|officer|executive|associate|intern|recruiter|marketer|writer|accountant|strategist|administrator|coordinator|representative|advocate|researcher)/i;

  function title(text, ls) {
    // a labelled title is the only kind we can be sure about
    var said = first(text, [
      /^\s*job\s*title\s*:\s*(.+)$/im,
      /^\s*(?:job\s*)?(?:role|position|designation)\s*:\s*(.+)$/im,
      /^\s*we(?:'re| are)\s+(?:currently\s+)?(?:looking\s+for|hiring|seeking)\s+(?:a|an)\s+([^.,\n]{3,60})/im
    ]);
    if (said) return clean_title(said);

    // otherwise the first line, but only if it reads like one
    for (var i = 0; i < Math.min(ls.length, 4); i++) {
      var l = ls[i];
      if (l.length <= 60 && TITLE_WORDS.test(l) && !/[.!?]$/.test(l)) {
        return clean_title(l);
      }
    }
    return '';
  }

  function clean_title(s) {
    return tidy(s)
      // "Content Writer to join our marketing team in Pune" is a sentence
      // with a title at the front of it
      .replace(/\s+(?:to|for|who|that|with|in|at|based|joining|reporting)\s+.*$/i, '')
      .replace(/^(?:a|an)\s+/i, '')
      .replace(/\s*\((?:remote|hybrid|on-?site|full[- ]time|part[- ]time)\)\s*$/i, '')
      .replace(/\s*[-–—|,]\s*(?:remote|hybrid|on-?site|full[- ]time|part[- ]time|bangalore|bengaluru|india).*$/i, '')
      .replace(/[\s:;,.]+$/, '');
  }

  // --- company -------------------------------------------------------

  var NAME = '([A-Z][A-Za-z0-9&.\'-]*(?:\\s+[A-Z][A-Za-z0-9&.\'-]*){0,2})';

  function company(text) {
    var said = first(text, [
      new RegExp('^\\s*company\\s*(?:name)?\\s*:\\s*(.+)$', 'im'),
      // "Wisemonk is an India-focused Employer of Record"
      new RegExp(NAME + '\\s+is\\s+(?:a|an|the)\\s', 'm'),
      // "At Wisemonk, we are driven by"
      new RegExp('\\bAt\\s+' + NAME + ',\\s+we\\b', 'm'),
      new RegExp('\\b(?:join|about)\\s+' + NAME + '\\b', 'm')
    ]);
    said = tidy(said).replace(/[,.]$/, '');
    // "We" and "Our" match the shape of a name without being one
    if (/^(we|our|the|this|it|they|about|join)$/i.test(said)) return '';
    return said;
  }

  // a domain in the text is a better answer than a name, when there is one
  function site(text) {
    var m = text.match(/\b(?:https?:\/\/)?(?:www\.)?([a-z0-9][a-z0-9-]*\.(?:com|io|co|ai|org|net|in|co\.in|co\.uk|dev|app))\b/i);
    if (!m) return '';
    var host = m[1].toLowerCase();
    // the ones that are never the employer
    if (/^(linkedin|indeed|glassdoor|naukri|greenhouse|lever|workable|gmail|google|example)\./.test(host)) {
      return '';
    }
    return host;
  }

  // --- where ---------------------------------------------------------

  function place(text, ls) {
    // "Bengaluru, Karnataka, India - Remote" near the top is a location
    // line, which is how a job board writes one
    for (var i = 0; ls && i < Math.min(ls.length, 6); i++) {
      var l = tidy(ls[i])
        .replace(/\s*[-\u2013\u2014|]\s*(?:remote|hybrid|on-?site).*$/i, '');
      if (l.length <= 60 && l.split(',').length >= 2 &&
          /^[A-Z][A-Za-z.'-]+(?:\s+[A-Z][A-Za-z.'-]+)?(?:\s*,\s*[A-Z][A-Za-z.'-]+(?:\s+[A-Z][A-Za-z.'-]+)?){1,3}$/.test(l)) {
        return tidy(l.split(',')[0]);
      }
    }

    var said = first(text, [
      /^\s*(?:location|based in|office)\s*:\s*(.+)$/im,
      /\b(?:based|located)\s+(?:at|in|out of)\s+(?:our\s+)?(?:office\s+in\s+|headquarters\s+in\s+)?(?:the\s+heart\s+of\s+)?([A-Z][^.,\n]{2,40})/m,
      /\bheadquarters\s+in\s+(?:the\s+heart\s+of\s+)?([A-Z][^.,\n]{2,40})/m,
      /\boffice\s+is\s+(?:conveniently\s+)?located\s+at\s+([^.\n]{4,80})/im,
      // "...to join our marketing team in Pune."
      /\b(?:join|team|role|position|office)\b[^.\n]{0,40}?\bin\s+([A-Z][a-z]{2,}(?:\s+[A-Z][a-z]+){0,2})\b/m
    ]);
    said = tidy(said).replace(/[,.]$/, '');
    if (!said) return '';
    // a street address answers "where exactly", not "where"
    if (/\d/.test(said) && said.split(/,/).length > 1) {
      var bits = said.split(/,/);
      said = tidy(bits[bits.length - 1]);
    }
    return said.replace(/^(?:the\s+heart\s+of\s+)/i, '');
  }

  function mode(text) {
    if (/\b(?:work[- ]from[- ]office|in[- ]office|on[- ]?site|onsite)\b/i.test(text)) {
      return 'On-site';
    }
    if (/\bhybrid\b/i.test(text)) return 'Hybrid';
    if (/\b(?:fully\s+)?remote\b|\bwork[- ]from[- ]home\b/i.test(text)) return 'Remote';
    return '';
  }

  function kind(text) {
    if (/\bfull[- ]time\b/i.test(text)) return 'Full-time';
    if (/\bpart[- ]time\b/i.test(text)) return 'Part-time';
    if (/\b(?:contract|contractor|freelance)\b/i.test(text)) return 'Contract';
    if (/\bintern(?:ship)?\b/i.test(text)) return 'Internship';
    return '';
  }

  // --- how long ------------------------------------------------------

  function years(text) {
    var m = text.match(/(\d{1,2})\s*(?:[-–—]|to)\s*(\d{1,2})\s*\+?\s*(?:years?|yrs?)\b/i);
    if (m) return m[1] + '–' + m[2] + ' years';
    m = text.match(/(\d{1,2})\s*\+\s*(?:years?|yrs?)\b/i);
    if (m) return m[1] + '+ years';
    m = text.match(/(?:minimum|at least|over)\s+(\d{1,2})\s*(?:years?|yrs?)\b/i);
    if (m) return m[1] + '+ years';
    return '';
  }

  // --- what with -----------------------------------------------------

  // Named things only. A rules parser cannot tell a skill from a noun,
  // but it can recognise a tool it has been told about, and everything
  // here is editable anyway.
  var TOOLS = [
    'Figma', 'Sketch', 'Adobe XD', 'Photoshop', 'Illustrator', 'Framer',
    'Webflow', 'Miro', 'Notion', 'Jira', 'Principle', 'After Effects',
    'React', 'Vue', 'Angular', 'Svelte', 'Next.js', 'Node.js', 'TypeScript',
    'JavaScript', 'Python', 'Java', 'Go', 'Golang', 'Rust', 'Ruby', 'PHP',
    'Swift', 'Kotlin', 'Django', 'Flask', 'FastAPI', 'Spring', 'Rails',
    'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'GraphQL', 'REST',
    'AWS', 'GCP', 'Azure', 'Docker', 'Kubernetes', 'Terraform',
    'SQL', 'Excel', 'Tableau', 'Power BI', 'Salesforce', 'HubSpot'
  ];

  var PHRASES = [
    'design systems', 'user research', 'prototyp(?:e|es|ing)', 'wireframing',
    'usability testing', 'user flows', 'interaction design',
    'visual design', 'product strategy', 'design thinking',
    'A/B testing', 'data analysis', 'machine learning',
    'microservices', 'CI/CD', 'test automation', 'accessibility'
  ];

  function skills(text) {
    var out = [];
    var seen = {};

    function add(s) {
      var k = s.toLowerCase();
      if (!seen[k]) { seen[k] = 1; out.push(s); }
    }

    TOOLS.forEach(function (t) {
      var re = new RegExp('(?:^|[^A-Za-z0-9.])' +
        t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '(?![A-Za-z0-9])', 'i');
      if (re.test(text)) add(t);
    });
    PHRASES.forEach(function (p) {
      if (new RegExp('\\b' + p.replace(/\//g, '\\/') + '\\b', 'i').test(text)) {
        // the pattern is not the name: "prototyp(?:e|es|ing)" is "Prototyping"
        add(p.replace(/\(\?:[^)]*\)/, 'ing')
             .replace(/^./, function (c) { return c.toUpperCase(); }));
      }
    });
    // "AI-first", "AI-powered" -- the JD's own words for it
    if (/\bAI[- ](?:first|powered|driven|native)\b/i.test(text)) add('AI-first design');
    return out.slice(0, 10);
  }

  // --- the sections, kept whole --------------------------------------

  function section(ls, heads) {
    var want = new RegExp('^(?:' + heads.join('|') + ')\\s*:?\\s*$', 'i');
    var stop = /^(?:[A-Z][A-Za-z \/&]{2,40})\s*:\s*$/;
    var out = [];
    var on = false;
    for (var i = 0; i < ls.length; i++) {
      var l = ls[i];
      if (want.test(l.replace(/:$/, '').trim()) || want.test(l)) { on = true; continue; }
      if (on) {
        if (stop.test(l) && !want.test(l)) break;
        out.push(l);
      }
    }
    return out;
  }

  function parse(text) {
    var t = String(text || '').replace(/ /g, ' ');
    var ls = lines(t);
    var flat = ls.join('\n');

    return {
      title: title(flat, ls),
      company: company(flat),
      site: site(flat),
      place: place(flat, ls),
      mode: mode(flat),
      kind: kind(flat),
      years: years(flat),
      skills: skills(flat),
      duties: section(ls, ['key responsibilities', 'responsibilities',
                           'what you(?:\'| wi)ll do', 'the role', 'role overview']),
      asks: section(ls, ['requirements', 'qualifications',
                         'what we(?:\'re| are) looking for', 'who you are',
                         'skills (?:&|and) experience']),
      text: t
    };
  }

  root.jdParse = parse;
}(typeof module !== 'undefined' && module.exports ? module.exports : window));
