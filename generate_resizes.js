const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

/**
 * Universal Multi-Resolution Resizer for Astra Cosmic Guide
 * Creates:
 * 1. Master WebP (1024x1024, Q90)
 * 2. Journal WebP (600x600, Q85) - for feeds, cards, profile screens
 * 3. Small WebP (128x128, Q85) - for chat lists, header avatars, badges
 */

async function processImage(inputPath, outputDir, baseName) {
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  const image = sharp(inputPath);
  const metadata = await image.metadata();

  console.log(`\nProcessing: ${path.basename(inputPath)} (${metadata.width}x${metadata.height})`);

  // 1. Master 1024
  const masterPath = path.join(outputDir, `${baseName}_master_1024.webp`);
  await sharp(inputPath)
    .resize(1024, 1024, { fit: 'cover', position: 'center' })
    .webp({ quality: 90 })
    .toFile(masterPath);
  const masterSize = fs.statSync(masterPath).size;
  console.log(`  -> Master  (1024x1024): ${(masterSize / 1024).toFixed(1)} KB [${path.basename(masterPath)}]`);

  // 2. Journal 600
  const journalPath = path.join(outputDir, `${baseName}_journal_600.webp`);
  await sharp(inputPath)
    .resize(600, 600, { fit: 'cover', position: 'center' })
    .webp({ quality: 85 })
    .toFile(journalPath);
  const journalSize = fs.statSync(journalPath).size;
  console.log(`  -> Journal (600x600)  : ${(journalSize / 1024).toFixed(1)} KB [${path.basename(journalPath)}]`);

  // 3. Small 128
  const smallPath = path.join(outputDir, `${baseName}_small_128.webp`);
  await sharp(inputPath)
    .resize(128, 128, { fit: 'cover', position: 'center' })
    .webp({ quality: 85 })
    .toFile(smallPath);
  const smallSize = fs.statSync(smallPath).size;
  console.log(`  -> Small   (128x128)  : ${(smallSize / 1024).toFixed(1)} KB [${path.basename(smallPath)}]`);
}

async function runDemo() {
  const sourceDir = 'D:/projects/monly/фигасе/СОРТИРОВАННЫЕ_АССЕТЫ/00_ИКОНКИ_И_ЛОГОТИП_АСТРА';
  const targetDir = 'D:/projects/monly/АСТРА_АССЕТЫ/00_ИКОНКИ_И_ЛОГОТИП_АСТРА';

  const icon1 = path.join(sourceDir, 'Astra_Icon_Option_1_StarFlower_1024x1024.png');
  const icon2 = path.join(sourceDir, 'Astra_Icon_Option_2_MandalaLotus_1024x1024.png');

  if (fs.existsSync(icon1)) {
    await processImage(icon1, targetDir, 'Astra_AppIcon_StarFlower');
  }
  if (fs.existsSync(icon2)) {
    await processImage(icon2, targetDir, 'Astra_AppIcon_MandalaLotus');
  }
  console.log('\n--- Multi-resolution pipeline demo finished successfully! ---');
}

runDemo().catch(console.error);
