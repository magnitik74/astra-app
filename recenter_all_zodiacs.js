const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const srcPath = 'C:/Users/Александр/.gemini/antigravity/brain/8dc77ab2-b9dd-4a62-9311-ed7a2c195cb3/.user_uploaded/media_1792297050767_6933ef69.png';
const targetDir = 'D:/projects/monly/АСТРА_АССЕТЫ/11_ДЕФОЛТНЫЕ_И_AI_АВАТАРЫ';
const sortedDir = 'D:/projects/monly/фигасе/СОРТИРОВАННЫЕ_АССЕТЫ/11_ДЕФОЛТНЫЕ_И_AI_АВАТАРЫ';

// Exact mathematical grid centers (found via edge luminosity profile)
const cols = [140, 378, 616];
const rows = [144, 388, 630, 874];

const zodiacMeta = [
  { num: '01', id: 'Aries', ru: 'Овен', col: 0, row: 0 },
  { num: '02', id: 'Taurus', ru: 'Телец', col: 1, row: 0 },
  { num: '03', id: 'Gemini', ru: 'Близнецы', col: 2, row: 0 },

  { num: '04', id: 'Cancer', ru: 'Рак', col: 0, row: 1 },
  { num: '05', id: 'Leo', ru: 'Лев', col: 1, row: 1 },
  { num: '06', id: 'Virgo', ru: 'Дева', col: 2, row: 1 },

  { num: '07', id: 'Libra', ru: 'Весы', col: 0, row: 2 },
  { num: '08', id: 'Scorpio', ru: 'Скорпион', col: 1, row: 2 },
  { num: '09', id: 'Sagittarius', ru: 'Стрелец', col: 2, row: 2 },

  { num: '10', id: 'Capricorn', ru: 'Козерог', col: 0, row: 3 },
  { num: '11', id: 'Aquarius', ru: 'Водолей', col: 1, row: 3 },
  { num: '12', id: 'Pisces', ru: 'Рыбы', col: 2, row: 3 }
];

async function recenterAll() {
  console.log('=== Recentering and Reslicing All 12 Zodiac Avatars ===');
  const size = 236;
  const half = 118;
  const r = 95; // Exact radius of circular medallion

  const maskSvg = Buffer.from(`
    <svg width="${size}" height="${size}">
      <defs>
        <filter id="smooth">
          <feGaussianBlur stdDeviation="0.6" />
        </filter>
      </defs>
      <circle cx="${half}" cy="${half}" r="${r}" fill="white" filter="url(#smooth)" />
    </svg>
  `);

  for (const z of zodiacMeta) {
    const cx = cols[z.col];
    const cy = rows[z.row];
    const left = Math.max(0, cx - half);
    const top = Math.max(0, cy - half);

    // Extract exact box
    const cropped = await sharp(srcPath)
      .extract({ left, top, width: size, height: size })
      .toBuffer();

    // Mask with exact centered circle
    const masked = await sharp(cropped)
      .composite([{ input: maskSvg, blend: 'dest-in' }])
      .png()
      .toBuffer();

    const baseName = `zodiac_${z.num}_${z.id}`;

    // 1. Master PNG (1024x1024, perfectly centered, true alpha)
    const masterPng = path.join(targetDir, `${baseName}_master_1024.png`);
    await sharp(masked)
      .resize(1024, 1024, { fit: 'contain', background: { r: 0, g: 0, b: 0, alpha: 0 } })
      .png()
      .toFile(masterPng);
    fs.copyFileSync(masterPng, path.join(sortedDir, `${baseName}_master_1024.png`));

    // 2. Master WebP (1024x1024)
    const masterWebp = path.join(targetDir, `${baseName}_master_1024.webp`);
    await sharp(masked)
      .resize(1024, 1024, { fit: 'contain', background: { r: 0, g: 0, b: 0, alpha: 0 } })
      .webp({ quality: 90, alphaQuality: 100 })
      .toFile(masterWebp);

    // 3. Journal WebP (600x600)
    const journalWebp = path.join(targetDir, `${baseName}_journal_600.webp`);
    await sharp(masked)
      .resize(600, 600, { fit: 'contain', background: { r: 0, g: 0, b: 0, alpha: 0 } })
      .webp({ quality: 85, alphaQuality: 100 })
      .toFile(journalWebp);

    // 4. Small WebP (128x128)
    const smallWebp = path.join(targetDir, `${baseName}_small_128.webp`);
    await sharp(masked)
      .resize(128, 128, { fit: 'contain', background: { r: 0, g: 0, b: 0, alpha: 0 } })
      .webp({ quality: 85, alphaQuality: 100 })
      .toFile(smallWebp);

    console.log(`[${z.num}/12] ${z.ru} (${z.id}) at (${cx}, ${cy}) -> 100% Centered!`);
  }

  // Re-build 12 zodiac composite for artifacts
  const cellW = 260;
  const cellH = 260;
  const pad = 20;
  const totalW = cellW * 4 + pad * 5;
  const totalH = cellH * 3 + pad * 4;

  const compositeItems = [];
  for (let i = 0; i < zodiacMeta.length; i++) {
    const col = i % 4;
    const row = Math.floor(i / 4);
    const left = pad + col * (cellW + pad);
    const top = pad + row * (cellH + pad);
    const fName = `zodiac_${zodiacMeta[i].num}_${zodiacMeta[i].id}_master_1024.png`;
    const buf = await sharp(path.join(targetDir, fName)).resize(cellW, cellH).toBuffer();
    compositeItems.push({ input: buf, top, left });
  }

  const compositeCanvas = sharp({
    create: {
      width: totalW,
      height: totalH,
      channels: 4,
      background: { r: 18, g: 18, b: 22, alpha: 1 }
    }
  });

  const compPath = path.join(targetDir, 'astra_12_zodiac_composite.png');
  await compositeCanvas.composite(compositeItems).png().toFile(compPath);

  // Copy to artifacts
  const artPath = 'C:/Users/Александр/.gemini/antigravity/brain/8dc77ab2-b9dd-4a62-9311-ed7a2c195cb3/astra_12_zodiac_composite.png';
  fs.copyFileSync(compPath, artPath);

  console.log('Updated composite preview in artifacts!');
}

recenterAll().catch(console.error);
