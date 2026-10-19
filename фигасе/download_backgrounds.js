const https = require('https');
const fs = require('fs');
const path = require('path');

let raw = fs.readFileSync('D:/projects/monly/фигасе/json_data/calendar_2026_full.json', 'utf8');
if (raw.charCodeAt(0) === 0xFEFF) raw = raw.slice(1);
const cal = JSON.parse(raw);

const targetDir = 'D:/projects/monly/фигасе/СОРТИРОВАННЫЕ_АССЕТЫ/09_ФОНЫ_ЛУННОГО_КАЛЕНДАРЯ';
if (!fs.existsSync(targetDir)) fs.mkdirSync(targetDir, { recursive: true });

const bgMap = new Map();
cal.data.forEach(day => {
  if (day.events) {
    day.events.forEach(ev => {
      const url = ev.backgroundUrl || (ev.moonDaily && ev.moonDaily.imageUrl);
      if (url && url.startsWith('http')) {
        const title = (ev.center && ev.center.title) || (ev.header && ev.header.title) || ('MoonDay_' + day.moonDay);
        const cleanTitle = title.replace(/[\/\\:\*\?"<>\|]/g, '_').replace(/\s+/g, '_').trim();
        if (!bgMap.has(url)) {
          bgMap.set(url, cleanTitle);
        }
      }
    });
  }
});

console.log('Unique calendar backgrounds to download:', bgMap.size);

const entries = Array.from(bgMap.entries());
let downloaded = 0;

function downloadNext(index) {
  if (index >= entries.length) {
    console.log('All backgrounds downloaded successfully! Total:', downloaded);
    return;
  }
  const [url, name] = entries[index];
  const ext = path.extname(url.split('?')[0]) || '.jpg';
  const fileName = (index + 1).toString().padStart(2, '0') + '_' + name + ext;
  const filePath = path.join(targetDir, fileName);

  if (fs.existsSync(filePath)) {
    downloaded++;
    downloadNext(index + 1);
    return;
  }

  const file = fs.createWriteStream(filePath);
  https.get(url, res => {
    res.pipe(file);
    file.on('finish', () => {
      file.close();
      downloaded++;
      if (downloaded % 10 === 0 || downloaded === entries.length) {
        console.log('Progress: ' + downloaded + ' / ' + entries.length);
      }
      downloadNext(index + 1);
    });
  }).on('error', err => {
    console.error('Error downloading ' + url, err.message);
    downloadNext(index + 1);
  });
}

downloadNext(0);
