const fs = require('fs');
const path = require('path');

const base = 'D:/projects/monly/АСТРА_АССЕТЫ';
const wisdomFiles = fs.readdirSync(path.join(base, '03_ДЕВЫ_МУДРОСТИ')).filter(f => /\.(png|jpg|webp)$/i.test(f));
const symbolFiles = fs.readdirSync(path.join(base, '04_СИМВОЛЫ_И_БОЖЕСТВА')).filter(f => /\.(png|jpg|webp)$/i.test(f));

console.log(`Wisdom files count: ${wisdomFiles.length}`);
console.log(`Symbol files count: ${symbolFiles.length}`);

// Name formatting helpers
function formatWisdomName(filename) {
  const baseName = filename.replace(/^\d+_/, '').replace(/\.(png|jpg|webp)$/i, '').replace(/_/g, ' ');
  return `Дева ${baseName}`;
}

function formatSymbolName(filename) {
  const baseName = filename.replace(/^\d+_/, '').replace(/\.(png|jpg|webp)$/i, '').replace(/_/g, ' ');
  return `${baseName} • Ведический Символ`;
}

const wisdomData = [];

wisdomFiles.forEach(f => {
  wisdomData.push({
    name: formatWisdomName(f),
    file: `03_ДЕВЫ_МУДРОСТИ/${f}`,
    desc: 'Священный женский архетип космической мудрости, интуиции и духовной силы.'
  });
});

symbolFiles.forEach(f => {
  wisdomData.push({
    name: formatSymbolName(f),
    file: `04_СИМВОЛЫ_И_БОЖЕСТВА/${f}`,
    desc: 'Ведическое божество и сакральный астрологический символ гармонии планет.'
  });
});

console.log(`Total full WISDOM_DATA items: ${wisdomData.length}`);

// Load HTML
let html = fs.readFileSync(path.join(base, 'astra_main_app.html'), 'utf8');

// Replace WISDOM_DATA
const replacementWisdom = `const WISDOM_DATA = ${JSON.stringify(wisdomData, null, 6)};`;
html = html.replace(/const WISDOM_DATA = \[[\s\S]*?\];/, replacementWisdom);

// Fix saveDreamEntry
html = html.replace(
  `function saveDreamEntry() {
      const txt = document.getElementById('dream-text-input').value.trim();
      if (txt) {
        alert("Сон успешно сохранен в вашем космическом дневнике!");
        closeUniversalModal();
      }
    }`,
  `function saveDreamEntry() {
      const txt = document.getElementById('dream-text-input').value.trim();
      if (txt) {
        localStorage.setItem(\`astra_dream_day_\${currentSelectedDay}\`, txt);
        alert("Сон успешно сохранен в вашем космическом дневнике!");
        closeUniversalModal();
      }
    }`
);

// Fix filterTarotGrid
html = html.replace(
  `function filterTarotGrid(suit, pill) {
      document.querySelectorAll('.tarot-filter-pill').forEach(p => p.classList.remove('active'));
      pill.classList.add('active');`,
  `function filterTarotGrid(suit, pill) {
      document.querySelectorAll('.tarot-filter-pill').forEach(p => p.classList.remove('active'));
      if (pill) pill.classList.add('active');`
);

// Fix handleTarotSearch
html = html.replace(
  `function handleTarotSearch(val) {
      const query = val.toLowerCase().trim();`,
  `function handleTarotSearch(val) {
      const query = typeof val === 'string' ? val.toLowerCase().trim() : (val?.target?.value || '').toLowerCase().trim();`
);

// Fix showRuneModal
html = html.replace(
  `function showRuneModal(r) {
      const content = \`
        <div style="display: flex; flex-direction: column; align-items: center; text-align: center;">
          <img src="02_СКАНДИНАВСКИЕ_РУНЫ/\${r.file}"`,
  `function showRuneModal(r) {
      const rune = typeof r === 'number' ? RUNES_DATA[r] : r;
      const content = \`
        <div style="display: flex; flex-direction: column; align-items: center; text-align: center;">
          <img src="02_СКАНДИНАВСКИЕ_РУНЫ/\${rune.file}"`
);
html = html.replace(
  `<h2 style="font-size: 22px; font-weight: 800; color: #FFF; margin-top: 14px;">\${r.name}</h2>`,
  `<h2 style="font-size: 22px; font-weight: 800; color: #FFF; margin-top: 14px;">\${rune.name}</h2>`
);
html = html.replace(
  `<p style="font-size: 15px; line-height: 1.5; color: #E5E5EB; margin-top: 6px;">\${r.desc}</p>`,
  `<p style="font-size: 15px; line-height: 1.5; color: #E5E5EB; margin-top: 6px;">\${rune.desc}</p>`
);

// Fix showCardModal to include 'Архетип'
html = html.replace(
  `<div style="font-size: 11px; font-weight: 700; color: var(--moonly-gold); text-transform: uppercase; text-align: center; margin-top: 4px;">\${card.arch}</div>`,
  `<div style="font-size: 11px; font-weight: 700; color: var(--moonly-gold); text-transform: uppercase; text-align: center; margin-top: 4px;">Архетип: \${card.arch}</div>`
);

// Fix setHealingFrequency
html = html.replace(
  `function setHealingFrequency(freq, chip) {
      document.querySelectorAll('.freq-selector-chip').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      currentFrequency = freq;`,
  `function setHealingFrequency(freq, chip) {
      document.querySelectorAll('.freq-selector-chip').forEach(c => c.classList.remove('active'));
      if (chip) chip.classList.add('active');
      currentFrequency = freq;`
);

fs.writeFileSync(path.join(base, 'astra_main_app.html'), html, 'utf8');
console.log('astra_main_app.html успешно обновлен с 97 картами мудрости и защитными проверками!');
