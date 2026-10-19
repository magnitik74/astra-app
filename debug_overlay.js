const sharp = require('sharp');
const fs = require('fs');

async function debugOverlay() {
  const srcPath = 'C:/Users/Александр/.gemini/antigravity/brain/8dc77ab2-b9dd-4a62-9311-ed7a2c195cb3/.user_uploaded/media_1792297050767_6933ef69.png';
  const meta = await sharp(srcPath).metadata();
  console.log('Original size:', meta.width, 'x', meta.height);

  // Let's create an SVG overlay with circles at our previous coordinates
  const previousSigns = [
    { num: '01', id: 'Aries', cx: 134, cy: 136, r: 97 },
    { num: '02', id: 'Taurus', cx: 369, cy: 132, r: 97 },
    { num: '03', id: 'Gemini', cx: 607, cy: 137, r: 97 },
    { num: '04', id: 'Cancer', cx: 136, cy: 385, r: 98 },
    { num: '05', id: 'Leo', cx: 365, cy: 380, r: 97 },
    { num: '06', id: 'Virgo', cx: 606, cy: 383, r: 97 },
    { num: '07', id: 'Libra', cx: 134, cy: 630, r: 98 },
    { num: '08', id: 'Scorpio', cx: 368, cy: 622, r: 98 },
    { num: '09', id: 'Sagittarius', cx: 608, cy: 630, r: 97 },
    { num: '10', id: 'Capricorn', cx: 134, cy: 870, r: 98 },
    { num: '11', id: 'Aquarius', cx: 371, cy: 868, r: 98 },
    { num: '12', id: 'Pisces', cx: 606, cy: 869, r: 98 }
  ];

  const svgCircles = previousSigns.map(s => `
    <circle cx="${s.cx}" cy="${s.cy}" r="${s.r}" fill="none" stroke="red" stroke-width="2" />
    <circle cx="${s.cx}" cy="${s.cy}" r="3" fill="cyan" />
  `).join('\n');

  const overlaySvg = Buffer.from(`
    <svg width="${meta.width}" height="${meta.height}">
      ${svgCircles}
    </svg>
  `);

  await sharp(srcPath)
    .composite([{ input: overlaySvg }])
    .png()
    .toFile('D:/projects/monly/debug_circles_overlay.png');

  console.log('Saved debug_circles_overlay.png');
}

debugOverlay().catch(console.error);
