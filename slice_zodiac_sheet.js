const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const srcPath = 'C:/Users/Александр/.gemini/antigravity/brain/8dc77ab2-b9dd-4a62-9311-ed7a2c195cb3/.user_uploaded/media_1792297050767_6933ef69.png';
const targetDir = 'D:/projects/monly/АСТРА_АССЕТЫ/11_ДЕФОЛТНЫЕ_И_AI_АВАТАРЫ';
const sortedDir = 'D:/projects/monly/фигасе/СОРТИРОВАННЫЕ_АССЕТЫ/11_ДЕФОЛТНЫЕ_И_AI_АВАТАРЫ';

if (!fs.existsSync(targetDir)) fs.mkdirSync(targetDir, { recursive: true });
if (!fs.existsSync(sortedDir)) fs.mkdirSync(sortedDir, { recursive: true });

// 12 Zodiac signs with exact detected centers in the 765x1024 sheet
const signs = [
  { num: '01', id: 'Aries', ru: 'Овен', cx: 134, cy: 136, r: 97 },
  { num: '02', id: 'Taurus', ru: 'Телец', cx: 369, cy: 132, r: 97 },
  { num: '03', id: 'Gemini', ru: 'Близнецы', cx: 607, cy: 137, r: 97 },
  { num: '04', id: 'Cancer', ru: 'Рак', cx: 136, cy: 385, r: 98 },
  { num: '05', id: 'Leo', ru: 'Лев', cx: 365, cy: 380, r: 97 },
  { num: '06', id: 'Virgo', ru: 'Дева', cx: 606, cy: 383, r: 97 },
  { num: '07', id: 'Libra', ru: 'Весы', cx: 134, cy: 630, r: 98 },
  { num: '08', id: 'Scorpio', ru: 'Скорпион', cx: 368, cy: 622, r: 98 },
  { num: '09', id: 'Sagittarius', ru: 'Стрелец', cx: 608, cy: 630, r: 97 },
  { num: '10', id: 'Capricorn', ru: 'Козерог', cx: 134, cy: 870, r: 98 },
  { num: '11', id: 'Aquarius', ru: 'Водолей', cx: 371, cy: 868, r: 98 },
  { num: '12', id: 'Pisces', ru: 'Рыбы', cx: 606, cy: 869, r: 98 }
];

async function sliceAll() {
  console.log('--- Slicing 12 Zodiac Avatars on Transparent Background ---');
  const img = sharp(srcPath);

  // Save the master sheet for reference
  fs.copyFileSync(srcPath, path.join(targetDir, 'zodiac_sheet_master_original.png'));
  fs.copyFileSync(srcPath, path.join(sortedDir, 'zodiac_sheet_master_original.png'));

  for (const s of signs) {
    const boxSize = s.r * 2 + 12; // box size with safety padding
    const halfBox = Math.floor(boxSize / 2);

    const left = Math.max(0, s.cx - halfBox);
    const top = Math.max(0, s.cy - halfBox);

    // High quality circular mask with smooth anti-aliased edge
    const maskSvg = Buffer.from(`
      <svg width="${boxSize}" height="${boxSize}">
        <defs>
          <filter id="feather">
            <feGaussianBlur stdDeviation="0.8" />
          </filter>
        </defs>
        <circle cx="${halfBox}" cy="${halfBox}" r="${s.r}" fill="white" filter="url(#feather)" />
      </svg>
    `);

    // Extract raw cell
    const cropped = await sharp(srcPath)
      .extract({ left, top, width: boxSize, height: boxSize })
      .toBuffer();

    // Apply circular alpha mask
    const circularAvatar = await sharp(cropped)
      .composite([{ input: maskSvg, blend: 'dest-in' }])
      .png()
      .toBuffer();

    const baseName = `zodiac_${s.num}_${s.id}`;

    // 1. Master Transparent PNG (1024x1024)
    const masterPng = path.join(targetDir, `${baseName}_master_1024.png`);
    await sharp(circularAvatar)
      .resize(1024, 1024, { fit: 'contain', background: { r: 0, g: 0, b: 0, alpha: 0 } })
      .png()
      .toFile(masterPng);

    // Copy to sorted
    fs.copyFileSync(masterPng, path.join(sortedDir, `${baseName}_master_1024.png`));

    // 2. Master WebP (1024x1024, with transparency!)
    const masterWebp = path.join(targetDir, `${baseName}_master_1024.webp`);
    await sharp(circularAvatar)
      .resize(1024, 1024, { fit: 'contain', background: { r: 0, g: 0, b: 0, alpha: 0 } })
      .webp({ quality: 90, alphaQuality: 100 })
      .toFile(masterWebp);

    // 3. Journal WebP (600x600, with transparency!)
    const journalWebp = path.join(targetDir, `${baseName}_journal_600.webp`);
    await sharp(circularAvatar)
      .resize(600, 600, { fit: 'contain', background: { r: 0, g: 0, b: 0, alpha: 0 } })
      .webp({ quality: 85, alphaQuality: 100 })
      .toFile(journalWebp);

    // 4. Small WebP (128x128, with transparency!)
    const smallWebp = path.join(targetDir, `${baseName}_small_128.webp`);
    await sharp(circularAvatar)
      .resize(128, 128, { fit: 'contain', background: { r: 0, g: 0, b: 0, alpha: 0 } })
      .webp({ quality: 85, alphaQuality: 100 })
      .toFile(smallWebp);

    console.log(`[${s.num}/12] ${s.ru} (${s.id}) -> Master PNG: ${(fs.statSync(masterPng).size / 1024).toFixed(1)} KB | Small WebP: ${(fs.statSync(smallWebp).size / 1024).toFixed(1)} KB`);
  }

  console.log('\n--- ALL 12 ZODIAC AVATARS CUT & EXPORTED WITH CLEAN TRANSPARENT BACKGROUNDS! ---');
}

sliceAll().catch(console.error);
