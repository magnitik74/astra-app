const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { execSync } = require('child_process');
const ffmpeg = require('ffmpeg-static');
const sharp = require('sharp');

console.log('=== Astra Cosmic Guide: Affirmations & Video Loops Pipeline ===');

const srcVideoDir = 'D:/projects/monly/фигасе/СОРТИРОВАННЫЕ_АССЕТЫ/08_АФФИРМАЦИИ_ВИДЕО';
const outVideoDir = 'D:/projects/monly/АСТРА_АССЕТЫ/08_АФФИРМАЦИИ_ВИДЕО';
const outDataDir = 'D:/projects/monly/АСТРА_АССЕТЫ/astra_ru_data';

if (!fs.existsSync(outVideoDir)) fs.mkdirSync(outVideoDir, { recursive: true });
if (!fs.existsSync(outDataDir)) fs.mkdirSync(outDataDir, { recursive: true });

// 1. Read Affirmations JSON
let rawAffs = fs.readFileSync('D:/projects/monly/фигасе/json_data/affirmations_all.json', 'utf8');
if (rawAffs.charCodeAt(0) === 0xFEFF) rawAffs = rawAffs.slice(1);
const affsData = JSON.parse(rawAffs);
const rawList = affsData.data.affirmations; // 363 items

console.log(`Loaded ${rawList.length} affirmations from affirmations_all.json.`);

// 2. Map files in source directory by hash
const videoFiles = fs.readdirSync(srcVideoDir).filter(f => f.endsWith('.mp4'));
const hashToSrc = new Map();
const fileToHash = new Map();

for (const f of videoFiles) {
  const p = path.join(srcVideoDir, f);
  const buf = fs.readFileSync(p);
  const h = crypto.createHash('md5').update(buf).digest('hex');
  if (!hashToSrc.has(h)) hashToSrc.set(h, p);
  fileToHash.set(f, h);
}

console.log(`Found ${videoFiles.length} raw files, ${hashToSrc.size} unique video streams.`);

// 3. Select top 40 unique loops by usage frequency
const hashUsage = new Map();
for (const a of rawList) {
  // Filename in sorted folder corresponds to affirmationId, e.g. "001_Affirmation_208.mp4"
  const matchingFile = videoFiles.find(f => f.includes(`Affirmation_${a.affirmationId}.mp4`));
  if (matchingFile) {
    const h = fileToHash.get(matchingFile);
    hashUsage.set(h, (hashUsage.get(h) || 0) + 1);
  }
}

// Sort hashes by frequency
const sortedHashes = Array.from(hashToSrc.keys()).sort((a, b) => (hashUsage.get(b) || 0) - (hashUsage.get(a) || 0));
const top40Hashes = sortedHashes.slice(0, 40);

console.log(`Selected Top ${top40Hashes.length} high-aesthetic unique loops for processing.`);

async function run() {
  const loopCatalog = [];
  const hashToLoopId = new Map();

  for (let i = 0; i < top40Hashes.length; i++) {
  const h = top40Hashes[i];
  const srcFile = hashToSrc.get(h);
  const loopNum = String(i + 1).padStart(2, '0');
  const loopId = `astra_loop_${loopNum}`;

  const targetMp4 = path.join(outVideoDir, `${loopId}.mp4`);
  const targetPoster = path.join(outVideoDir, `${loopId}_poster.webp`);
  const tempPosterPng = path.join(outVideoDir, `temp_${loopNum}.png`);

  hashToLoopId.set(h, loopId);

  // Check if already processed
  if (!fs.existsSync(targetMp4) || !fs.existsSync(targetPoster)) {
    console.log(`[${i + 1}/40] Encoding ${loopId}.mp4 from ${path.basename(srcFile)}...`);
    
    // FFmpeg video encode: mute, faststart, subtle color grade
    const cmdVideo = `"${ffmpeg}" -y -i "${srcFile}" -an -vf "eq=contrast=1.04:brightness=-0.02:saturation=0.92" -c:v libx264 -crf 24 -preset fast -movflags +faststart "${targetMp4}"`;
    execSync(cmdVideo, { stdio: 'ignore' });

    // Poster frame
    const cmdPoster = `"${ffmpeg}" -y -ss 00:00:01 -i "${srcFile}" -vframes 1 "${tempPosterPng}"`;
    execSync(cmdPoster, { stdio: 'ignore' });

    // WebP poster via sharp directly with await
    await sharp(tempPosterPng)
      .webp({ quality: 85 })
      .toFile(targetPoster);
    if (fs.existsSync(tempPosterPng)) fs.unlinkSync(tempPosterPng);
  } else {
    console.log(`[${i + 1}/40] ${loopId} already processed, skipping encode.`);
  }

  const mp4SizeKb = (fs.statSync(targetMp4).size / 1024).toFixed(0);
  const posterSizeKb = (fs.statSync(targetPoster).size / 1024).toFixed(0);

  loopCatalog.push({
    loopId,
    filename: `${loopId}.mp4`,
    posterFilename: `${loopId}_poster.webp`,
    mp4Path: `assets/08_АФФИРМАЦИИ_ВИДЕО/${loopId}.mp4`,
    posterPath: `assets/08_АФФИРМАЦИИ_ВИДЕО/${loopId}_poster.webp`,
    fileSizeKb: parseInt(mp4SizeKb, 10),
    posterSizeKb: parseInt(posterSizeKb, 10)
  });
}

// 5. Save Video Loops Catalog
const catalogPath = path.join(outVideoDir, 'video_loops_catalog.json');
fs.writeFileSync(catalogPath, JSON.stringify(loopCatalog, null, 2), 'utf8');
console.log(`\nSaved Video Loops Catalog: ${catalogPath}`);

// 6. Map all 363 Affirmations to the 40 clean loops
const astraAffirmations = rawList.map((a, idx) => {
  const matchingFile = videoFiles.find(f => f.includes(`Affirmation_${a.affirmationId}.mp4`));
  const h = matchingFile ? fileToHash.get(matchingFile) : null;
  
  // Assign loop (either matched or round-robin across top 40)
  let loopId = h && hashToLoopId.has(h) ? hashToLoopId.get(h) : loopCatalog[idx % loopCatalog.length].loopId;
  const loopInfo = loopCatalog.find(l => l.loopId === loopId) || loopCatalog[0];

  return {
    id: idx + 1,
    affirmationId: a.affirmationId,
    textEn: a.text.replace(/\u00a0/g, ' '),
    video: {
      loopId: loopInfo.loopId,
      mp4: loopInfo.mp4Path,
      poster: loopInfo.posterPath
    }
  };
});

  const affsPath = path.join(outDataDir, 'astra_affirmations_base.json');
  fs.writeFileSync(affsPath, JSON.stringify(astraAffirmations, null, 2), 'utf8');
  console.log(`Saved Affirmations Base: ${affsPath} (${astraAffirmations.length} items mapped)`);

  console.log('\n--- Video Loops and Affirmations Pipeline Completed! ---');
}

run().catch(console.error);
