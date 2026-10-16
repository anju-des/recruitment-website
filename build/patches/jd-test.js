// What the parser makes of a few job descriptions, the real one first.
var fs = require('fs');
var parse = require('./jd-parse.js').jdParse;

var cases = {
  'the real one (Wisemonk, PDF)': fs.readFileSync('jd.txt', 'utf8'),

  'a LinkedIn-style post, no labels':
    'Senior Backend Engineer (Remote)\n' +
    'Razorpay\n' +
    'Bengaluru, Karnataka, India - Remote\n\n' +
    'About the job\n' +
    'Razorpay is a full-stack financial solutions company. We are looking ' +
    'for engineers who have 5+ years of experience building distributed ' +
    'systems in Go or Java, with PostgreSQL and Kubernetes in production. ' +
    'You will own services end to end.\n\n' +
    'Requirements\n' +
    '- 5+ years backend experience\n' +
    '- Strong with Go, PostgreSQL, Docker, Kubernetes\n' +
    '- Experience with microservices and CI/CD\n',

  'a terse one-paragraph brief':
    'We are hiring a Content Writer to join our marketing team in Pune. ' +
    'Full-time, hybrid. At least 2 years writing for B2B SaaS. ' +
    'Apply at careers@brightscale.in',

  'a messy one that should mostly come back empty':
    'Exciting opportunity!!! Join the rocketship. ' +
    'DM me if interested. Competitive pay, great culture.'
};

function show(name, got) {
  console.log('\n===== ' + name + ' =====');
  ['title', 'company', 'site', 'place', 'mode', 'kind', 'years'].forEach(function (k) {
    console.log('  ' + k.padEnd(8) + (got[k] || '— (asks)'));
  });
  console.log('  skills  ' + (got.skills.join(' · ') || '—'));
  console.log('  duties  ' + got.duties.length + ' lines, asks ' + got.asks.length + ' lines');
}

Object.keys(cases).forEach(function (n) { show(n, parse(cases[n])); });
