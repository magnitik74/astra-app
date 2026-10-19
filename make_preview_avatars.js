const fs = require('fs');
const sharp = require('sharp');

async function makeSideBySide() {
  const fPath = 'D:/projects/monly/АСТРА_АССЕТЫ/11_ДЕФОЛТНЫЕ_И_AI_АВАТАРЫ/01_Default_Female_Muse_master_1024.png';
  const mPath = 'D:/projects/monly/АСТРА_АССЕТЫ/11_ДЕФОЛТНЫЕ_И_AI_АВАТАРЫ/02_Default_Male_Guide_master_1024.png';
  const outPath = 'D:/projects/monly/АСТРА_АССЕТЫ/11_ДЕФОЛТНЫЕ_И_AI_АВАТАРЫ/astra_default_avatars_side_by_side.png';

  const fBuf = await sharp(fPath).resize(540, 540).toBuffer();
  const mBuf = await sharp(mPath).resize(540, 540).toBuffer();

  const canvas = sharp({
    create: {
      width: 1200,
      height: 640,
      channels: 4,
      background: { r: 14, g: 14, b: 18, alpha: 1 }
    }
  });

  await canvas
    .composite([
      { input: fBuf, top: 50, left: 40 },
      { input: mBuf, top: 50, left: 620 }
    ])
    .png()
    .toFile(outPath);

  console.log('Side-by-side preview created:', outPath);
}

makeSideBySide().catch(console.error);
