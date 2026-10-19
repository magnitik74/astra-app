const fs = require('fs');
const path = require('path');

const baseDump = 'D:/projects/monly/фигасе/full_dump';
const jsonDir = path.join(baseDump, 'json_data');
const mediaDir = path.join(baseDump, 'media');
const targetRoot = 'D:/projects/monly/фигасе/СОРТИРОВАННЫЕ_АССЕТЫ';

function cleanName(str) {
  if (!str) return 'Unnamed';
  return str.replace(/[\/\\:\*\?"<>\|]/g, '_').replace(/\s+/g, '_').trim();
}

function ensureDir(p) {
  if (!fs.existsSync(p)) fs.mkdirSync(p, { recursive: true });
}

function findSourceFile(url) {
  if (!url) return null;
  const fileName = path.basename(url.split('?')[0]);
  const subdirs = ['images', 'audio', 'videos'];
  for (const s of subdirs) {
    const full = path.join(mediaDir, s, fileName);
    if (fs.existsSync(full)) return full;
  }
  return null;
}

function copyMapped(url, targetFolder, targetFileName) {
  const src = findSourceFile(url);
  if (!src) return false;
  ensureDir(targetFolder);
  const ext = path.extname(src);
  const dest = path.join(targetFolder, cleanName(targetFileName) + ext);
  if (!fs.existsSync(dest)) {
    fs.copyFileSync(src, dest);
  }
  return true;
}

let stats = {};

// 1. ТАРО КАРТЫ
try {
  let raw = fs.readFileSync(path.join(jsonDir, 'cards_type_0_tarot.json'), 'utf8');
  if (raw.charCodeAt(0) === 0xFEFF) raw = raw.slice(1);
  const cards = JSON.parse(raw).data || JSON.parse(raw);
  let count = 0;
  cards.forEach((c, idx) => {
    const num = (c.order !== undefined ? c.order : idx).toString().padStart(2, '0');
    const name = num + '_' + cleanName(c.name);
    if (copyMapped(c.imageUrl, path.join(targetRoot, '01_ТАРО_КАРТЫ'), name)) count++;
  });
  stats['01_ТАРО_КАРТЫ'] = count;
} catch(e) { console.error('Tarot error:', e.message); }

// 2. РУНЫ
try {
  let raw = fs.readFileSync(path.join(jsonDir, 'cards_type_1_runes.json'), 'utf8');
  if (raw.charCodeAt(0) === 0xFEFF) raw = raw.slice(1);
  const cards = JSON.parse(raw).data || JSON.parse(raw);
  let count = 0;
  cards.forEach((c, idx) => {
    const num = (c.order !== undefined ? c.order : idx).toString().padStart(2, '0');
    const name = num + '_' + cleanName(c.name);
    if (copyMapped(c.imageUrl, path.join(targetRoot, '02_СКАНДИНАВСКИЕ_РУНЫ'), name)) count++;
  });
  stats['02_СКАНДИНАВСКИЕ_РУНЫ'] = count;
} catch(e) { console.error('Runes error:', e.message); }

// 3. МУДРОСТЬ (ДЕВЫ-МУЗЫ)
try {
  let raw = fs.readFileSync(path.join(jsonDir, 'cards_type_2_wisdom.json'), 'utf8');
  if (raw.charCodeAt(0) === 0xFEFF) raw = raw.slice(1);
  const cards = JSON.parse(raw).data || JSON.parse(raw);
  let count = 0;
  cards.forEach((c, idx) => {
    const num = (c.order !== undefined ? c.order : idx).toString().padStart(2, '0');
    const name = num + '_' + cleanName(c.name);
    if (copyMapped(c.imageUrl, path.join(targetRoot, '03_ДЕВЫ_МУДРОСТИ'), name)) count++;
  });
  stats['03_ДЕВЫ_МУДРОСТИ'] = count;
} catch(e) { console.error('Wisdom error:', e.message); }

// 4. СИМВОЛЫ И ВЕДИЧЕСКИЕ БОГИ
try {
  let raw = fs.readFileSync(path.join(jsonDir, 'cards_type_3_symbols.json'), 'utf8');
  if (raw.charCodeAt(0) === 0xFEFF) raw = raw.slice(1);
  const cards = JSON.parse(raw).data || JSON.parse(raw);
  let count = 0;
  cards.forEach((c, idx) => {
    const num = (c.order !== undefined ? c.order : idx).toString().padStart(2, '0');
    const name = num + '_' + cleanName(c.name);
    if (copyMapped(c.imageUrl, path.join(targetRoot, '04_СИМВОЛЫ_И_БОЖЕСТВА'), name)) count++;
  });
  stats['04_СИМВОЛЫ_И_БОЖЕСТВА'] = count;
} catch(e) { console.error('Symbols error:', e.message); }

// 5. МЕДИТАЦИИ (АУДИО, ВИДЕО И ОБЛОЖКИ)
try {
  let raw = fs.readFileSync(path.join(jsonDir, 'meditations_page_1.json'), 'utf8');
  if (raw.charCodeAt(0) === 0xFEFF) raw = raw.slice(1);
  const list = JSON.parse(raw).data || JSON.parse(raw);
  let count = 0;
  list.forEach((m, idx) => {
    const num = (idx + 1).toString().padStart(3, '0');
    const baseName = num + '_' + cleanName(m.name);
    if (copyMapped(m.cardIconUrl, path.join(targetRoot, '05_МЕДИТАЦИИ/Обложки'), baseName + '_cover')) count++;
    if (copyMapped(m.soundUrl, path.join(targetRoot, '05_МЕДИТАЦИИ/Аудио'), baseName + '_audio')) count++;
    if (copyMapped(m.videoUrl, path.join(targetRoot, '05_МЕДИТАЦИИ/Видео_Фоны'), baseName + '_loop')) count++;
  });
  stats['05_МЕДИТАЦИИ'] = count;
} catch(e) { console.error('Meditations error:', e.message); }

// 6. ЗВУКИ И ЧАСТОТЫ СОЛЬФЕДЖИО
try {
  let raw = fs.readFileSync(path.join(jsonDir, 'sounds_page_1.json'), 'utf8');
  if (raw.charCodeAt(0) === 0xFEFF) raw = raw.slice(1);
  const list = JSON.parse(raw).data || JSON.parse(raw);
  let count = 0;
  list.forEach((s, idx) => {
    const num = (idx + 1).toString().padStart(3, '0');
    const baseName = num + '_' + cleanName(s.name);
    if (copyMapped(s.cardIconUrl, path.join(targetRoot, '06_ЗВУКИ_И_ЧАСТОТЫ/Обложки'), baseName + '_cover')) count++;
    if (copyMapped(s.soundUrl, path.join(targetRoot, '06_ЗВУКИ_И_ЧАСТОТЫ/Аудио_Частоты'), baseName + '_audio')) count++;
    if (copyMapped(s.videoUrl, path.join(targetRoot, '06_ЗВУКИ_И_ЧАСТОТЫ/Видео_Фоны'), baseName + '_loop')) count++;
  });
  stats['06_ЗВУКИ_И_ЧАСТОТЫ'] = count;
} catch(e) { console.error('Sounds error:', e.message); }

// 7. СКАЗКИ НА НОЧЬ (STORIES)
try {
  let raw = fs.readFileSync(path.join(jsonDir, 'stories_page_1.json'), 'utf8');
  if (raw.charCodeAt(0) === 0xFEFF) raw = raw.slice(1);
  const list = JSON.parse(raw).data || JSON.parse(raw);
  let count = 0;
  list.forEach((st, idx) => {
    const num = (idx + 1).toString().padStart(3, '0');
    const baseName = num + '_' + cleanName(st.name);
    if (copyMapped(st.iconUrl, path.join(targetRoot, '07_СКАЗКИ_НА_НОЧЬ/Обложки'), baseName + '_cover')) count++;
  });
  stats['07_СКАЗКИ_НА_НОЧЬ'] = count;
} catch(e) { console.error('Stories error:', e.message); }

// 8. АФФИРМАЦИИ (ВИДЕО ЦИКЛЫ)
try {
  let raw = fs.readFileSync(path.join(jsonDir, 'affirmations_all.json'), 'utf8');
  if (raw.charCodeAt(0) === 0xFEFF) raw = raw.slice(1);
  const affs = JSON.parse(raw).data.affirmations || [];
  let count = 0;
  affs.slice(0, 100).forEach((af, idx) => {
    const num = (idx + 1).toString().padStart(3, '0');
    const baseName = num + '_Affirmation_' + (af.affirmationId || idx);
    if (copyMapped(af.videoUrl, path.join(targetRoot, '08_АФФИРМАЦИИ_ВИДЕО'), baseName)) count++;
  });
  stats['08_АФФИРМАЦИИ_ВИДЕО'] = count;
} catch(e) { console.error('Affirmations error:', e.message); }

console.log('СОРТИРОВКА ЗАВЕРШЕНА УСПЕШНО!');
console.log(JSON.stringify(stats, null, 2));
