const fs = require('fs');
const path = require('path');
const dir = path.join(__dirname, 'фигасе', 'real_onboarding_official', 'screen_mockups', 'html_screens');
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html')).sort();
for (let i = 0; i < files.length; i++) {
  const f = files[i];
  const c = fs.readFileSync(path.join(dir, f), 'utf8');
  const b = (c.match(/class="badge">([^<]*)/) || [])[1] || '';
  const t = (c.match(/class="title">([\s\S]*?)<\/div>/) || [])[1] || '';
  const s = (c.match(/class="subtitle">([\s\S]*?)<\/div>/) || [])[1] || '';
  const hasV = c.includes('<video');
  const hasO = c.includes('opt-card');
  const hasInput = c.includes('<input');
  console.log(`${i}: ${f}\n   BADGE: ${b}\n   TITLE: ${t.replace(/\s+/g, ' ').trim()}\n   SUB: ${s.replace(/\s+/g, ' ').trim()}\n   TYPE: ${hasV ? 'VIDEO' : (hasO ? 'QUIZ' : (hasInput ? 'INPUT' : 'OTHER'))}\n`);
}
