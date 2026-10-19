const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

async function makeComposite() {
  const dir = 'D:/projects/monly/АСТРА_АССЕТЫ/11_ДЕФОЛТНЫЕ_И_AI_АВАТАРЫ';
  const signs = [
    '01_Aries', '02_Taurus', '03_Gemini',
    '04_Cancer', '05_Leo', '06_Virgo',
    '07_Libra', '08_Scorpio', '09_Sagittarius',
    '10_Capricorn', '11_Aquarius', '12_Pisces'
  ];

  const cellW = 260;
  const cellH = 260;
  const pad = 20;

  const totalW = cellW * 4 + pad * 5; // 4 cols
  const totalH = cellH * 3 + pad * 4; // 3 rows

  const compositeItems = [];

  for (let i = 0; i < signs.length; i++) {
    const col = i % 4;
    const row = Math.floor(i / 4);
    const left = pad + col * (cellW + pad);
    const top = pad + row * (cellH + pad);

    const fName = `zodiac_${signs[i]}_master_1024.png`;
    const fPath = path.join(dir, fName);

    const buf = await sharp(fPath).resize(cellW, cellH).toBuffer();
    compositeItems.push({ input: buf, top, left });
  }

  // Dark graphite canvas
  const canvas = sharp({
    create: {
      width: totalW,
      height: totalH,
      channels: 4,
      background: { r: 18, g: 18, b: 22, alpha: 1 }
    }
  });

  const outPath = path.join(dir, 'astra_12_zodiac_composite.png');
  await canvas.composite(compositeItems).png().toFile(outPath);

  // Copy to artifacts
  const artPath = 'C:/Users/Александр/.gemini/antigravity/brain/8dc77ab2-b9dd-4a62-9311-ed7a2c195cb3/astra_12_zodiac_composite.png';
  fs.copyFileSync(outPath, artPath);

  console.log('Saved 12 Zodiac composite to:', artPath);
}

makeComposite().catch(console.error);
