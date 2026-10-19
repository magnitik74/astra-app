const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');
const sharp = require('sharp');

/**
 * Astra Batch Generation Runner with OpenRouter
 */

const MANIFESTS = {
  'avatars': 'D:/projects/monly/АСТРА_АССЕТЫ/avatars_generation_manifest.json',
  'personas': 'D:/projects/monly/АСТРА_АССЕТЫ/personas_generation_manifest.json',
  'tarot': 'D:/projects/monly/АСТРА_АССЕТЫ/tarot_generation_manifest.json',
  'runes': 'D:/projects/monly/АСТРА_АССЕТЫ/runes_generation_manifest.json',
  'wisdom': 'D:/projects/monly/АСТРА_АССЕТЫ/wisdom_generation_manifest.json',
  'symbols': 'D:/projects/monly/АСТРА_АССЕТЫ/symbols_generation_manifest.json',
  'backgrounds': 'D:/projects/monly/АСТРА_АССЕТЫ/backgrounds_generation_manifest.json'
};

const MANIFEST_DIRS = {
  'avatars': 'D:/projects/monly/АСТРА_АССЕТЫ/11_ДЕФОЛТНЫЕ_И_AI_АВАТАРЫ',
  'personas': 'D:/projects/monly/АСТРА_АССЕТЫ/10_ПЕРСОНАЖИ_ИИ_АСТРОЛОГИ',
  'tarot': 'D:/projects/monly/АСТРА_АССЕТЫ/01_ТАРО_КАРТЫ',
  'runes': 'D:/projects/monly/АСТРА_АССЕТЫ/02_СКАНДИНАВСКИЕ_РУНЫ',
  'wisdom': 'D:/projects/monly/АСТРА_АССЕТЫ/03_ДЕВЫ_МУДРОСТИ',
  'symbols': 'D:/projects/monly/АСТРА_АССЕТЫ/04_СИМВОЛЫ_И_БОЖЕСТВА',
  'backgrounds': 'D:/projects/monly/АСТРА_АССЕТЫ/09_ФОНЫ_ЛУННОГО_КАЛЕНДАРЯ'
};

const PROGRESS_FILE = 'D:/projects/monly/АСТРА_АССЕТЫ/generation_progress.json';

function getProgress() {
  if (fs.existsSync(PROGRESS_FILE)) {
    try {
      return JSON.parse(fs.readFileSync(PROGRESS_FILE, 'utf8'));
    } catch (e) {
      return {};
    }
  }
  return {};
}

function saveProgress(data) {
  fs.writeFileSync(PROGRESS_FILE, JSON.stringify(data, null, 2), 'utf8');
}

function downloadImage(url, dest) {
  return new Promise((resolve, reject) => {
    if (url.startsWith('data:image')) {
      const base64Data = url.replace(/^data:image\/\w+;base64,/, '');
      fs.writeFileSync(dest, Buffer.from(base64Data, 'base64'));
      return resolve();
    }

    const client = url.startsWith('https') ? https : http;
    client.get(url, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return downloadImage(res.headers.location, dest).then(resolve).catch(reject);
      }
      if (res.statusCode !== 200) {
        return reject(new Error(`Status ${res.statusCode} for ${url}`));
      }
      const stream = fs.createWriteStream(dest);
      res.pipe(stream);
      stream.on('finish', () => {
        stream.close();
        resolve();
      });
    }).on('error', reject);
  });
}

async function processResizes(inputPath, outputDir, baseName) {
  if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

  const masterPath = path.join(outputDir, `${baseName}_master_1024.webp`);
  const journalPath = path.join(outputDir, `${baseName}_journal_600.webp`);
  const smallPath = path.join(outputDir, `${baseName}_small_128.webp`);

  await sharp(inputPath).resize(1024, 1024, { fit: 'cover' }).webp({ quality: 90 }).toFile(masterPath);
  await sharp(inputPath).resize(600, 600, { fit: 'cover' }).webp({ quality: 85 }).toFile(journalPath);
  await sharp(inputPath).resize(128, 128, { fit: 'cover' }).webp({ quality: 85 }).toFile(smallPath);

  return { master: masterPath, journal: journalPath, small: smallPath };
}

function callOpenRouter(prompt, apiKey, model = 'black-forest-labs/flux-1-dev') {
  return new Promise((resolve, reject) => {
    const payload = JSON.stringify({
      model: model,
      messages: [{ role: 'user', content: prompt }]
    });

    const options = {
      hostname: 'openrouter.ai',
      port: 443,
      path: '/api/v1/chat/completions',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
        'HTTP-Referer': 'https://astra.app',
        'X-Title': 'Astra Cosmic Guide',
        'Content-Length': Buffer.byteLength(payload)
      }
    };

    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', (d) => body += d);
      res.on('end', () => {
        try {
          const json = JSON.parse(body);
          if (res.statusCode !== 200) {
            return reject(new Error(json.error ? json.error.message : `HTTP ${res.statusCode}: ${body}`));
          }
          const content = json.choices && json.choices[0] && json.choices[0].message ? json.choices[0].message.content : '';
          
          const mdMatch = content.match(/!\[.*?\]\((https?:\/\/[^\s\)]+|data:image\/[^\s\)]+)\)/);
          if (mdMatch) return resolve(mdMatch[1]);

          const urlMatch = content.match(/https?:\/\/[^\s"'<>]+\.(?:png|jpg|jpeg|webp)/i);
          if (urlMatch) return resolve(urlMatch[0]);

          if (json.choices[0].message.images && json.choices[0].message.images.length > 0) {
            return resolve(json.choices[0].message.images[0]);
          }

          if (content.startsWith('data:image')) return resolve(content);

          reject(new Error(`Could not parse image URL: ${content.slice(0, 150)}...`));
        } catch (e) {
          reject(new Error(`Invalid JSON: ${e.message}`));
        }
      });
    });

    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

// Main execution function
async function run() {
  const args = process.argv.slice(2);
  const apiKey = process.env.OPENROUTER_API_KEY || process.env.AI_API_KEY;
  const isDryRun = args.includes('--dry-run') || !args.includes('--live') || !apiKey;
  const manifestName = args.find(a => !a.startsWith('--')) || 'tarot';
  const model = args.find(a => a.startsWith('--model=')) ? args.find(a => a.startsWith('--model=')).split('=')[1] : 'black-forest-labs/flux-1-dev';

  console.log('=====================================================');
  console.log('✨ АСТРА: BATCH GENERATION RUNNER (OpenRouter) ✨');
  console.log(`Manifest: ${manifestName}`);
  console.log(`Model   : ${model}`);
  console.log(`Mode    : ${isDryRun ? 'DRY-RUN (Симуляция без списания баланса)' : 'LIVE (Боевой запуск через OpenRouter API)'}`);
  console.log('=====================================================\n');

  if (!MANIFESTS[manifestName]) {
    console.error(`Unknown manifest: ${manifestName}. Available: ${Object.keys(MANIFESTS).join(', ')}`);
    return;
  }

  const manifestPath = MANIFESTS[manifestName];
  const items = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
  const progress = getProgress();
  const baseDir = MANIFEST_DIRS[manifestName];

  // Normalize item fields
  const normalizedItems = items.map(item => {
    const id = item.id || item.name || item.targetFile || item.targetFileName;
    const prompt = item.prompt || item.generationPrompt || '';
    let targetFile = item.targetFile;
    if (!targetFile && item.targetFileName) {
      targetFile = path.join(baseDir, item.targetFileName);
    }
    return {
      id,
      name: item.name || id,
      prompt,
      targetFile: targetFile || path.join(baseDir, `${id}.webp`)
    };
  });

  console.log(`Total items in manifest: ${normalizedItems.length}`);
  let completed = 0;
  let pending = 0;

  for (const item of normalizedItems) {
    if (progress[item.id] && progress[item.id].status === 'success') {
      completed++;
    } else {
      pending++;
    }
  }

  console.log(`Status: ${completed} completed, ${pending} pending to generate.\n`);

  if (isDryRun) {
    console.log('--- PREVIEWING NEXT 5 ITEMS IN QUEUE ---');
    let shown = 0;
    for (const item of normalizedItems) {
      if (!progress[item.id] || progress[item.id].status !== 'success') {
        console.log(`[Item] ${item.name}`);
        console.log(`       Target: ${item.targetFile}`);
        console.log(`       Prompt: ${item.prompt.slice(0, 110)}...`);
        shown++;
        if (shown >= 5) break;
      }
    }
    console.log('\n💡 Для боевого запуска:');
    console.log('  1. Пополните OpenRouter криптой');
    console.log('  2. Установите ключ в терминале:');
    console.log('     $env:OPENROUTER_API_KEY="sk-or-v1-ваш_ключ"');
    console.log(`  3. Запустите: node run_generation.js ${manifestName} --live\n`);
    return;
  }

  console.log(`🚀 Starting live generation for ${pending} items via OpenRouter (${model})...\n`);

  for (let i = 0; i < normalizedItems.length; i++) {
    const item = normalizedItems[i];

    if (progress[item.id] && progress[item.id].status === 'success') {
      continue;
    }

    console.log(`[${i + 1}/${normalizedItems.length}] Generating: ${item.name}...`);
    try {
      const imageUrl = await callOpenRouter(item.prompt, apiKey, model);
      console.log(`  -> Generated! Downloading...`);

      const outDir = path.dirname(item.targetFile);
      const baseName = path.basename(item.targetFile, path.extname(item.targetFile));
      const rawDest = path.join(outDir, `${baseName}_raw.png`);

      await downloadImage(imageUrl, rawDest);

      // Multi-res resize to WebP
      const resizes = await processResizes(rawDest, outDir, baseName);
      console.log(`  -> Resized to 1024, 600, 128 WebP!`);

      progress[item.id] = {
        status: 'success',
        timestamp: new Date().toISOString(),
        files: resizes
      };
      saveProgress(progress);

      // 2 sec delay between requests
      await new Promise(r => setTimeout(r, 2000));
    } catch (e) {
      console.error(`  ❌ Failed ${item.name}: ${e.message}`);
      progress[item.id] = { status: 'error', error: e.message, timestamp: new Date().toISOString() };
      saveProgress(progress);
    }
  }

  console.log('\n--- BATCH GENERATION FINISHED! ---');
}

run().catch(console.error);
