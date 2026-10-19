const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');
const { execSync } = require('child_process');

const FFMPEG_PATH = path.resolve(__dirname, 'node_modules/ffmpeg-static/ffmpeg.exe');
const OUTPUT_DIR = path.resolve(__dirname, 'АСТРА_АССЕТЫ/08_АФФИРМАЦИИ_ВИДЕО');
const TEMP_DIR = path.resolve(__dirname, 'temp_raw_loops');

if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR, { recursive: true });
if (!fs.existsSync(TEMP_DIR)) fs.mkdirSync(TEMP_DIR, { recursive: true });

// 40 Curated Video Prompts across 5 Sacred Elements (8 each)
const LOOP_SPECS = [
  // WATER (01 - 08) - Peace, trust, emotional flow
  { id: 1, element: 'water', query: 'calm lake water ripples sunset' },
  { id: 2, element: 'water', query: 'ocean waves slow motion twilight' },
  { id: 3, element: 'water', query: 'water droplets on glass dark' },
  { id: 4, element: 'water', query: 'underwater blue light rays sea' },
  { id: 5, element: 'water', query: 'mountain stream water dark stones' },
  { id: 6, element: 'water', query: 'calm ocean surface dusk night' },
  { id: 7, element: 'water', query: 'rain on water surface dark' },
  { id: 8, element: 'water', query: 'water reflection golden hour dusk' },

  // FIRE & LIGHT (09 - 16) - Inner strength, transformation, radiance
  { id: 9, element: 'fire', query: 'candle flame macro dark background' },
  { id: 10, element: 'fire', query: 'fireplace glowing embers warm fire' },
  { id: 11, element: 'fire', query: 'bonfire sparks dark night' },
  { id: 12, element: 'fire', query: 'candle burning soft warm light' },
  { id: 13, element: 'fire', query: 'oil lamp flame warm glow' },
  { id: 14, element: 'fire', query: 'sunrise light rays through forest' },
  { id: 15, element: 'fire', query: 'burning incense glowing ember' },
  { id: 16, element: 'fire', query: 'candlelight soft sacred meditation' },

  // CELESTIAL & SPACE (17 - 24) - Intuition, cosmic path, higher self
  { id: 17, element: 'celestial', query: 'milky way stars night sky timelapse' },
  { id: 18, element: 'celestial', query: 'full moon night sky clouds dark' },
  { id: 19, element: 'celestial', query: 'starry night sky mountain' },
  { id: 20, element: 'celestial', query: 'aurora borealis night sky deep' },
  { id: 21, element: 'celestial', query: 'galaxy nebula stars dark space' },
  { id: 22, element: 'celestial', query: 'moon through dark clouds night' },
  { id: 23, element: 'celestial', query: 'stars rotation night sky timelapse' },
  { id: 24, element: 'celestial', query: 'constellations night sky stars' },

  // AIR & MIST (25 - 32) - Mental clarity, freedom, breath
  { id: 25, element: 'air', query: 'fog rolling through pine forest' },
  { id: 26, element: 'air', query: 'mist mountain valley sunrise' },
  { id: 27, element: 'air', query: 'sunset golden clouds moving slowly' },
  { id: 28, element: 'air', query: 'smoke dark background smooth flow' },
  { id: 29, element: 'air', query: 'soft clouds dusk pastel golden hour' },
  { id: 30, element: 'air', query: 'morning mist over calm lake' },
  { id: 31, element: 'air', query: 'foggy dense forest trees serene' },
  { id: 32, element: 'air', query: 'clouds timelapse sunset gradient' },

  // EARTH & NATURE (33 - 40) - Abundance, vitality, grounding
  { id: 33, element: 'earth', query: 'flower blooming timelapse dark' },
  { id: 34, element: 'earth', query: 'dew drops on green leaf macro' },
  { id: 35, element: 'earth', query: 'golden grass swaying sunset light' },
  { id: 36, element: 'earth', query: 'wheat field golden hour gentle wind' },
  { id: 37, element: 'earth', query: 'lotus flower dark water slow motion' },
  { id: 38, element: 'earth', query: 'sunlight through forest canopy' },
  { id: 39, element: 'earth', query: 'wet sand texture waves receding' },
  { id: 40, element: 'earth', query: 'mossy stones forest stream meditation' }
];

const usedVideoIds = new Set();

function downloadFile(url, destPath) {
  return new Promise((resolve, reject) => {
    try {
      execSync(`curl.exe -s -L "${url}" -o "${destPath}" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"`, { stdio: 'ignore' });
      if (fs.existsSync(destPath) && fs.statSync(destPath).size > 1000) {
        resolve(destPath);
      } else {
        reject(new Error('Downloaded file is empty or missing'));
      }
    } catch (err) {
      reject(err);
    }
  });
}

function searchPixabay(apiKey, query) {
  return new Promise((resolve, reject) => {
    const encQuery = encodeURIComponent(query);
    const url = `https://pixabay.com/api/videos/?key=${apiKey}&q=${encQuery}&video_type=film&per_page=15&safesearch=true`;
    const options = {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      }
    };
    https.get(url, options, res => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          if (json.hits && json.hits.length > 0) {
            // Pick first hit not yet used
            const availableHit = json.hits.find(h => !usedVideoIds.has(h.id)) || json.hits[0];
            usedVideoIds.add(availableHit.id);

            const v = availableHit.videos;
            // Prefer medium or large for best quality / speed balance
            const chosen = (v.medium && v.medium.url) ? v.medium.url :
                           (v.large && v.large.url) ? v.large.url :
                           (v.small && v.small.url) ? v.small.url : null;
            resolve(chosen);
          } else {
            resolve(null);
          }
        } catch(e) {
          reject(e);
        }
      });
    }).on('error', reject);
  });
}

function processWithFFmpeg(rawVideoPath, outMp4Path, outPosterPath) {
  // Astra Pipeline:
  // 1. Scale and crop to 720x1280 (exact 9:16 vertical)
  // 2. Astra Color grade: shadow lift to #141418, amber warmth #F5A623, desaturate neon
  // 3. Ping-pong loop (forward + reverse concat) for 100% mathematically seamless loop
  // 4. Strip audio (-an), H.264 CRF 24, pix_fmt yuv420p (iOS/Android compatible), +faststart

  const vf = [
    'scale=720:1280:force_original_aspect_ratio=increase',
    'crop=720:1280',
    'eq=contrast=1.06:brightness=-0.04:saturation=0.82',
    'colorbalance=rs=0.04:gs=-0.02:bs=-0.04:rm=0.06:gm=0.02:bm=-0.05'
  ].join(',');

  // Ping-pong filter complex: take 2.5s -> reverse -> concat to 5.0s seamless loop
  const filterComplex = `[0:v]trim=0:2.5,setpts=PTS-STARTPTS,${vf}[fwd];[fwd]split[f1][f2];[f2]reverse[rev];[f1][rev]concat=n=2:v=1[outv]`;

  const cmdMp4 = `"${FFMPEG_PATH}" -y -i "${rawVideoPath}" -filter_complex "${filterComplex}" -map "[outv]" -an -c:v libx264 -pix_fmt yuv420p -preset slow -crf 24 -movflags +faststart "${outMp4Path}"`;
  execSync(cmdMp4, { stdio: 'ignore' });

  // Extract poster frame (q=80 webp)
  const cmdPoster = `"${FFMPEG_PATH}" -y -ss 00:00:01 -i "${outMp4Path}" -vframes 1 -c:v libwebp -quality 80 "${outPosterPath}"`;
  execSync(cmdPoster, { stdio: 'ignore' });
}

async function main() {
  const args = process.argv.slice(2);
  let pixabayKey = process.env.PIXABAY_API_KEY || '18951010-f6cd83f2bbd188e2e1827d8bd';

  for (const arg of args) {
    if (arg.startsWith('--key=') || arg.startsWith('--pixabay=')) {
      pixabayKey = arg.split('=')[1];
    }
  }

  console.log(`================================================================`);
  console.log(`Запуск пайплайна 40 видеолупов «АСТРА» через Pixabay API`);
  console.log(`================================================================`);
  console.log(`Всего слотов: ${LOOP_SPECS.length} (5 стихий по 8 видео).`);

  let completed = 0;

  for (const spec of LOOP_SPECS) {
    const loopNum = String(spec.id).padStart(2, '0');
    const outMp4 = path.join(OUTPUT_DIR, `astra_loop_${loopNum}.mp4`);
    const outPoster = path.join(OUTPUT_DIR, `astra_loop_${loopNum}_poster.webp`);

    if (fs.existsSync(outMp4) && fs.existsSync(outPoster) && fs.statSync(outMp4).size > 10000) {
      console.log(`[${loopNum}/40] Уже готов: astra_loop_${loopNum}.mp4 (пропуск)`);
      completed++;
      continue;
    }

    console.log(`[${loopNum}/40] Поиск: "${spec.query}" (${spec.element})...`);
    try {
      let downloadUrl = await searchPixabay(pixabayKey, spec.query);

      if (!downloadUrl) {
        console.warn(`  ВНИМАНИЕ: Видео по запросу "${spec.query}" не найдено! Пробуем запасной запрос "${spec.element}"...`);
        downloadUrl = await searchPixabay(pixabayKey, spec.element);
      }

      if (!downloadUrl) {
        console.error(`  Пропуск слота ${loopNum}: видео не найдено.`);
        continue;
      }

      const tempRaw = path.join(TEMP_DIR, `temp_raw_${loopNum}.mp4`);
      console.log(`  Скачивание сырого видео...`);
      await downloadFile(downloadUrl, tempRaw);

      console.log(`  FFmpeg: Астра-колоргрейдинг (#141418 + #F5A623) + 9:16 пинг-понг луп + постер...`);
      processWithFFmpeg(tempRaw, outMp4, outPoster);

      // Clean temp
      if (fs.existsSync(tempRaw)) fs.unlinkSync(tempRaw);

      const stats = fs.statSync(outMp4);
      console.log(`  ГОТОВО: astra_loop_${loopNum}.mp4 (${Math.round(stats.size / 1024)} KB) + poster.webp`);
      completed++;
    } catch (err) {
      console.error(`  ОШИБКА слота ${loopNum}:`, err.message);
    }
  }

  console.log(`\n================================================================`);
  console.log(`Пайплайн завершен: ${completed}/${LOOP_SPECS.length} видео готовы в продакшн!`);
  console.log(`Папка: ${OUTPUT_DIR}`);
  console.log(`Галерея для проверки: D:/projects/monly/АСТРА_АССЕТЫ/astra_video_loops_gallery.html`);
  console.log(`================================================================`);
}

main().catch(console.error);
