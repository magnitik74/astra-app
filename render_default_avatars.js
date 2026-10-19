const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

const targetDir = 'D:/projects/monly/АСТРА_АССЕТЫ/11_ДЕФОЛТНЫЕ_И_AI_АВАТАРЫ';
if (!fs.existsSync(targetDir)) {
  fs.mkdirSync(targetDir, { recursive: true });
}

// 1. Female Default Avatar: "Муза Тишины"
const femaleSvg = `
<svg width="1024" height="1024" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Background Gradient -->
    <radialGradient id="bgGrad" cx="50%" cy="45%" r="65%">
      <stop offset="0%" stop-color="#222228" />
      <stop offset="70%" stop-color="#141417" />
      <stop offset="100%" stop-color="#0E0E11" />
    </radialGradient>
    
    <!-- Aura Glow -->
    <radialGradient id="auraGlow" cx="50%" cy="42%" r="40%">
      <stop offset="0%" stop-color="#F5A623" stop-opacity="0.25" />
      <stop offset="60%" stop-color="#9B51E0" stop-opacity="0.12" />
      <stop offset="100%" stop-color="#000000" stop-opacity="0" />
    </radialGradient>

    <!-- Clay Shading Gradient -->
    <linearGradient id="clayGrad" x1="20%" y1="0%" x2="80%" y2="100%">
      <stop offset="0%" stop-color="#EDE8E1" />
      <stop offset="40%" stop-color="#DDD6CC" />
      <stop offset="100%" stop-color="#B8AFA2" />
    </linearGradient>

    <linearGradient id="hairGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#3A373E" />
      <stop offset="100%" stop-color="#242327" />
    </linearGradient>

    <!-- Golden Rim Gradient -->
    <linearGradient id="goldRim" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFDF9F" />
      <stop offset="50%" stop-color="#D4AF37" stop-opacity="0.6" />
      <stop offset="100%" stop-color="#9B51E0" stop-opacity="0.2" />
    </linearGradient>

    <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="30" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <!-- Background Canvas -->
  <rect width="1024" height="1024" fill="url(#bgGrad)" />

  <!-- Ambient Aura Halo -->
  <circle cx="512" cy="450" r="340" fill="url(#auraGlow)" filter="url(#softGlow)" />

  <!-- Sacred Cosmic Rings -->
  <circle cx="512" cy="450" r="280" fill="none" stroke="url(#goldRim)" stroke-width="1.5" stroke-dasharray="6 8" opacity="0.45" />
  <circle cx="512" cy="450" r="240" fill="none" stroke="#F5A623" stroke-width="1" opacity="0.3" />
  <circle cx="512" cy="450" r="200" fill="none" stroke="#9B51E0" stroke-width="1" stroke-dasharray="3 5" opacity="0.25" />

  <!-- Subtle Constellation Stars -->
  <circle cx="400" cy="280" r="3" fill="#FFE8B5" opacity="0.7" />
  <circle cx="630" cy="310" r="2.5" fill="#FFE8B5" opacity="0.6" />
  <circle cx="340" cy="430" r="2" fill="#E8D7FF" opacity="0.5" />
  <circle cx="680" cy="460" r="2.5" fill="#FFE8B5" opacity="0.65" />
  <circle cx="512" cy="190" r="3.5" fill="#FFF2D6" opacity="0.8" />

  <!-- Little North Star Accent at Top -->
  <path d="M512 160 L514 175 L529 177 L514 179 L512 194 L510 179 L495 177 L510 175 Z" fill="#FFE3A8" opacity="0.85" />

  <!-- Female Silhouette / Clay Portrait -->
  <g id="femaleFigure" transform="translate(0, 40)">
    <!-- Shoulders & Linen Robe -->
    <path d="M 280 840 C 310 740, 390 670, 470 655 L 554 655 C 634 670, 714 740, 744 840 C 750 860, 710 880, 512 880 C 314 880, 274 860, 280 840 Z" fill="#2E2D33" stroke="url(#goldRim)" stroke-width="1.5" opacity="0.9" />

    <!-- Soft Linen Drape -->
    <path d="M 460 660 Q 512 730 564 660" fill="none" stroke="#D4AF37" stroke-width="1.5" opacity="0.4" />
    <path d="M 440 680 Q 512 760 584 680" fill="none" stroke="#F5A623" stroke-width="1" opacity="0.2" />

    <!-- Graceful Neck -->
    <path d="M 474 540 L 474 660 C 490 666, 534 666, 550 660 L 550 540 Z" fill="url(#clayGrad)" />
    <!-- Neck shadow -->
    <path d="M 474 540 C 495 565, 529 565, 550 540 L 550 560 C 529 580, 495 580, 474 560 Z" fill="#9C9487" opacity="0.5" />

    <!-- Head / Face Oval -->
    <ellipse cx="512" cy="460" rx="90" ry="118" fill="url(#clayGrad)" />

    <!-- Hair Silhouette (Matte Clay Slate) -->
    <path d="M 415 470 C 400 370, 450 320, 512 320 C 574 320, 624 370, 609 470 C 595 440, 570 380, 512 380 C 454 380, 429 440, 415 470 Z" fill="url(#hairGrad)" />
    <path d="M 420 440 C 410 350, 455 310, 512 310 C 569 310, 614 350, 604 440 C 625 380, 595 300, 512 300 C 429 300, 399 380, 420 440 Z" fill="#25242A" />

    <!-- Meditative Serene Features (Minimalist Line Art) -->
    <!-- Closed Eyes (Inner Peace) -->
    <path d="M 460 460 Q 478 468 494 460" fill="none" stroke="#686259" stroke-width="2.5" stroke-linecap="round" />
    <path d="M 530 460 Q 546 468 564 460" fill="none" stroke="#686259" stroke-width="2.5" stroke-linecap="round" />

    <!-- Delicate Eyebrows -->
    <path d="M 456 445 Q 476 438 496 444" fill="none" stroke="#7A7368" stroke-width="1.8" stroke-linecap="round" />
    <path d="M 528 444 Q 548 438 568 445" fill="none" stroke="#7A7368" stroke-width="1.8" stroke-linecap="round" />

    <!-- Subtle Nose -->
    <path d="M 512 452 L 510 490 Q 514 496 520 493" fill="none" stroke="#8D8477" stroke-width="1.8" stroke-linecap="round" />

    <!-- Serene Gentle Lips -->
    <path d="M 498 522 Q 512 529 526 522" fill="none" stroke="#B87D74" stroke-width="2.2" stroke-linecap="round" />
    <path d="M 504 525 Q 512 531 520 525" fill="none" stroke="#9E6760" stroke-width="1.5" stroke-linecap="round" />

    <!-- Third Eye Bindi / Golden Starlight Dot -->
    <circle cx="512" cy="425" r="3" fill="#F5A623" />
    <circle cx="512" cy="425" r="5" fill="#FFE3A8" opacity="0.4" />
  </g>

  <!-- Border Frame (Subtle Cosmic Glass Inset) -->
  <rect x="24" y="24" width="976" height="976" rx="40" fill="none" stroke="url(#goldRim)" stroke-width="1.5" opacity="0.3" />
</svg>
`;

// 2. Male Default Avatar: "Проводник Ясности"
const maleSvg = `
<svg width="1024" height="1024" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Background Gradient -->
    <radialGradient id="bgGradM" cx="50%" cy="45%" r="65%">
      <stop offset="0%" stop-color="#222329" />
      <stop offset="70%" stop-color="#141519" />
      <stop offset="100%" stop-color="#0E0E12" />
    </radialGradient>
    
    <!-- Aura Glow (Warm Terracotta & Solar Gold) -->
    <radialGradient id="auraGlowM" cx="50%" cy="42%" r="40%">
      <stop offset="0%" stop-color="#E07A5F" stop-opacity="0.22" />
      <stop offset="60%" stop-color="#F5A623" stop-opacity="0.12" />
      <stop offset="100%" stop-color="#000000" stop-opacity="0" />
    </radialGradient>

    <!-- Clay Shading Gradient -->
    <linearGradient id="clayGradM" x1="20%" y1="0%" x2="80%" y2="100%">
      <stop offset="0%" stop-color="#E8E2D8" />
      <stop offset="45%" stop-color="#D4CCC0" />
      <stop offset="100%" stop-color="#ADA496" />
    </linearGradient>

    <linearGradient id="hairGradM" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#323136" />
      <stop offset="100%" stop-color="#1F1E22" />
    </linearGradient>

    <!-- Golden Rim Gradient -->
    <linearGradient id="goldRimM" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFD699" />
      <stop offset="50%" stop-color="#E07A5F" stop-opacity="0.5" />
      <stop offset="100%" stop-color="#D4AF37" stop-opacity="0.2" />
    </linearGradient>

    <filter id="softGlowM" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="30" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <!-- Background Canvas -->
  <rect width="1024" height="1024" fill="url(#bgGradM)" />

  <!-- Ambient Aura Halo -->
  <circle cx="512" cy="450" r="340" fill="url(#auraGlowM)" filter="url(#softGlowM)" />

  <!-- Sacred Cosmic Geometry (Hexagonal & Circular Harmony) -->
  <circle cx="512" cy="450" r="285" fill="none" stroke="url(#goldRimM)" stroke-width="1.5" stroke-dasharray="6 8" opacity="0.45" />
  <circle cx="512" cy="450" r="245" fill="none" stroke="#E07A5F" stroke-width="1" opacity="0.3" />
  <circle cx="512" cy="450" r="205" fill="none" stroke="#F5A623" stroke-width="1" stroke-dasharray="3 5" opacity="0.25" />

  <!-- Geometric Rays / Diamond Accents -->
  <path d="M512 165 L512 735 M227 450 L797 450" stroke="url(#goldRimM)" stroke-width="0.8" stroke-dasharray="4 8" opacity="0.2" />

  <!-- Stars -->
  <circle cx="380" cy="290" r="2.8" fill="#FFE2B8" opacity="0.7" />
  <circle cx="650" cy="300" r="3" fill="#FFE2B8" opacity="0.75" />
  <circle cx="320" cy="460" r="2" fill="#FFC999" opacity="0.5" />
  <circle cx="700" cy="430" r="2.5" fill="#FFE2B8" opacity="0.6" />
  <circle cx="512" cy="190" r="3.5" fill="#FFF1D6" opacity="0.85" />

  <!-- North Star at Apex -->
  <path d="M512 160 L514 175 L529 177 L514 179 L512 194 L510 179 L495 177 L510 175 Z" fill="#FFD699" opacity="0.85" />

  <!-- Male Silhouette / Clay Portrait -->
  <g id="maleFigure" transform="translate(0, 40)">
    <!-- Shoulders & Minimalist Dark Cashmere Coat -->
    <path d="M 260 850 C 300 730, 380 660, 465 650 L 559 650 C 644 660, 724 730, 764 850 C 770 870, 720 890, 512 890 C 304 890, 254 870, 260 850 Z" fill="#28282E" stroke="url(#goldRimM)" stroke-width="1.5" opacity="0.95" />

    <!-- Collar / Mandarin Minimalist Line -->
    <path d="M 465 650 L 512 710 L 559 650" fill="none" stroke="#E07A5F" stroke-width="1.8" opacity="0.5" />
    <line x1="512" y1="710" x2="512" y2="820" stroke="#D4AF37" stroke-width="1.2" opacity="0.3" stroke-dasharray="3 4" />

    <!-- Sturdy Noble Neck -->
    <path d="M 466 535 L 466 655 C 485 662, 539 662, 558 655 L 558 535 Z" fill="url(#clayGradM)" />
    <!-- Neck shadow -->
    <path d="M 466 535 C 490 560, 534 560, 558 535 L 558 555 C 534 575, 490 575, 466 555 Z" fill="#948B7D" opacity="0.5" />

    <!-- Jaw & Face (Slightly more defined angular contour) -->
    <path d="M 420 420 C 420 340, 460 330, 512 330 C 564 330, 604 340, 604 420 C 604 490, 584 540, 534 565 C 520 572, 504 572, 490 565 C 440 540, 420 490, 420 420 Z" fill="url(#clayGradM)" />

    <!-- Hair Silhouette (Textured Minimalist Crop) -->
    <path d="M 416 410 C 405 340, 450 300, 512 295 C 574 300, 619 340, 608 410 C 596 360, 565 330, 512 330 C 459 330, 428 360, 416 410 Z" fill="url(#hairGradM)" />
    <path d="M 422 360 C 426 315, 465 285, 512 285 C 559 285, 598 315, 602 360 C 610 325, 580 275, 512 275 C 444 275, 414 325, 422 360 Z" fill="#1C1B1F" />

    <!-- Features: Calm Intelligent Gaze / Closed Eyes in Reflection -->
    <path d="M 456 456 Q 476 463 494 456" fill="none" stroke="#5E584F" stroke-width="2.6" stroke-linecap="round" />
    <path d="M 530 456 Q 548 463 568 456" fill="none" stroke="#5E584F" stroke-width="2.6" stroke-linecap="round" />

    <!-- Strong Calm Eyebrows -->
    <path d="M 450 440 Q 474 433 496 439" fill="none" stroke="#4F4A42" stroke-width="2.6" stroke-linecap="round" />
    <path d="M 528 439 Q 550 433 574 440" fill="none" stroke="#4F4A42" stroke-width="2.6" stroke-linecap="round" />

    <!-- Defined Nose Profile -->
    <path d="M 512 445 L 509 486 Q 513 493 521 489" fill="none" stroke="#7A7265" stroke-width="2" stroke-linecap="round" />

    <!-- Composed Thoughtful Mouth -->
    <path d="M 494 520 Q 512 524 530 520" fill="none" stroke="#8E6A64" stroke-width="2.4" stroke-linecap="round" />
    <path d="M 500 523 Q 512 527 524 523" fill="none" stroke="#75534E" stroke-width="1.6" stroke-linecap="round" />

    <!-- Golden Brow Accent -->
    <circle cx="512" cy="415" r="3" fill="#E07A5F" />
    <circle cx="512" cy="415" r="5" fill="#FFD699" opacity="0.35" />
  </g>

  <!-- Border Frame -->
  <rect x="24" y="24" width="976" height="976" rx="40" fill="none" stroke="url(#goldRimM)" stroke-width="1.5" opacity="0.3" />
</svg>
`;

async function renderAndExport(svgString, baseName, ruName) {
  console.log(`\nRendering ${ruName} (${baseName})...`);
  const svgBuffer = Buffer.from(svgString);

  // 1. Master PNG (1024x1024)
  const masterPngPath = path.join(targetDir, `${baseName}_master_1024.png`);
  await sharp(svgBuffer).png().toFile(masterPngPath);

  // 2. Master WebP (1024x1024)
  const masterWebpPath = path.join(targetDir, `${baseName}_master_1024.webp`);
  await sharp(svgBuffer).webp({ quality: 90 }).toFile(masterWebpPath);

  // 3. Journal WebP (600x600)
  const journalWebpPath = path.join(targetDir, `${baseName}_journal_600.webp`);
  await sharp(svgBuffer).resize(600, 600).webp({ quality: 85 }).toFile(journalWebpPath);

  // 4. Small WebP (128x128)
  const smallWebpPath = path.join(targetDir, `${baseName}_small_128.webp`);
  await sharp(svgBuffer).resize(128, 128).webp({ quality: 85 }).toFile(smallWebpPath);

  console.log(`  -> Master PNG  : ${(fs.statSync(masterPngPath).size / 1024).toFixed(1)} KB`);
  console.log(`  -> Master WebP : ${(fs.statSync(masterWebpPath).size / 1024).toFixed(1)} KB`);
  console.log(`  -> Journal 600 : ${(fs.statSync(journalWebpPath).size / 1024).toFixed(1)} KB`);
  console.log(`  -> Small 128   : ${(fs.statSync(smallWebpPath).size / 1024).toFixed(1)} KB`);
}

async function main() {
  await renderAndExport(femaleSvg, '01_Default_Female_Muse', 'Муза Тишины (Женский)');
  await renderAndExport(maleSvg, '02_Default_Male_Guide', 'Проводник Ясности (Мужской)');
  console.log('\n--- Both Default Master Avatars successfully created and resized! ---');
}

main().catch(console.error);
