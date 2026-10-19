const fs = require('fs');
const path = require('path');
const http = require('http');

async function checkUrl(url) {
  return new Promise((resolve) => {
    http.get(url, (res) => {
      let dataLen = 0;
      res.on('data', chunk => { dataLen += chunk.length; });
      res.on('end', () => {
        resolve({
          statusCode: res.statusCode,
          contentType: res.headers['content-type'],
          contentLength: dataLen || parseInt(res.headers['content-length'] || '0', 10)
        });
      });
    }).on('error', (err) => {
      resolve({ statusCode: 500, error: err.message });
    });
  });
}

async function runComprehensiveAudit() {
  console.log('===============================================================');
  console.log('   АСТРА: ПОЛНЫЙ УГЛУБЛЕННЫЙ АУДИТ 100% ВСЕХ АССЕТОВ ПРИЛОЖЕНИЯ');
  console.log('===============================================================');

  const baseDir = 'D:/projects/monly/АСТРА_АССЕТЫ';
  const appHtml = fs.readFileSync(path.join(baseDir, 'astra_main_app.html'), 'utf8');

  // Collect all runtime assets to test:
  const assetsToVerify = new Set();

  // 1. All static <img> src and style url() in HTML
  const staticSrcMatches = appHtml.match(/(?:src|href)=["']([^"']+\.(?:png|jpg|jpeg|svg|webp))["']/gi) || [];
  staticSrcMatches.forEach(m => {
    const p = m.replace(/(?:src|href)=["']/, '').replace(/["']$/, '').trim();
    if (!p.startsWith('http')) assetsToVerify.add(p);
  });

  // 2. 30 Moon spheres (moon_1.png .. moon_30.png)
  for (let d = 1; d <= 30; d++) {
    assetsToVerify.add(`moonly_3d_icons/moon_${d}.png`);
  }

  // 3. 78 Tarot Cards + Card Back
  assetsToVerify.add('moonly_3d_icons/ic_tarot_card_back_v3.png');
  assetsToVerify.add('moonly_3d_icons/ic_tarot_spread_slot_active.png');
  assetsToVerify.add('moonly_3d_icons/ic_taros_reset.png');
  const tarotCardsOnDisk = fs.readdirSync(path.join(baseDir, '01_ТАРО_КАРТЫ')).filter(f => /\.(png|jpg|webp)$/i.test(f));
  tarotCardsOnDisk.forEach(f => assetsToVerify.add(`01_ТАРО_КАРТЫ/${f}`));

  // 4. 24 Elder Futhark Runes
  const runesOnDisk = fs.readdirSync(path.join(baseDir, '02_СКАНДИНАВСКИЕ_РУНЫ')).filter(f => /\.(png|jpg|webp)$/i.test(f));
  runesOnDisk.forEach(f => assetsToVerify.add(`02_СКАНДИНАВСКИЕ_РУНЫ/${f}`));

  // 5. 57 Wisdom Goddesses
  const wisdomOnDisk = fs.readdirSync(path.join(baseDir, '03_ДЕВЫ_МУДРОСТИ')).filter(f => /\.(png|jpg|webp)$/i.test(f));
  wisdomOnDisk.forEach(f => assetsToVerify.add(`03_ДЕВЫ_МУДРОСТИ/${f}`));

  // 6. 40 Vedic Deities & Symbols
  const symbolsOnDisk = fs.readdirSync(path.join(baseDir, '04_СИМВОЛЫ_И_БОЖЕСТВА')).filter(f => /\.(png|jpg|webp)$/i.test(f));
  symbolsOnDisk.forEach(f => assetsToVerify.add(`04_СИМВОЛЫ_И_БОЖЕСТВА/${f}`));

  // 7. 82 Moon Calendar Backgrounds
  const bgsOnDisk = fs.readdirSync(path.join(baseDir, '09_ФОНЫ_ЛУННОГО_КАЛЕНДАРЯ')).filter(f => /\.(png|jpg|webp)$/i.test(f));
  bgsOnDisk.forEach(f => assetsToVerify.add(`09_ФОНЫ_ЛУННОГО_КАЛЕНДАРЯ/${f}`));

  // 8. 5 AI Astrologer Personas
  const personasOnDisk = fs.readdirSync(path.join(baseDir, '10_ПЕРСОНАЖИ_ИИ_АСТРОЛОГИ')).filter(f => /\.(png|jpg|webp)$/i.test(f));
  personasOnDisk.forEach(f => assetsToVerify.add(`10_ПЕРСОНАЖИ_ИИ_АСТРОЛОГИ/${f}`));

  // 9. Profile Avatars & Zodiac Totems
  const avatarsOnDisk = fs.readdirSync(path.join(baseDir, '11_ДЕФОЛТНЫЕ_И_AI_АВАТАРЫ')).filter(f => /\.(png|jpg|webp)$/i.test(f));
  avatarsOnDisk.forEach(f => assetsToVerify.add(`11_ДЕФОЛТНЫЕ_И_AI_АВАТАРЫ/${f}`));

  console.log(`Общий реестр верифицируемых ассетов: ${assetsToVerify.size} файлов.`);

  let diskOkCount = 0;
  let diskMissingCount = 0;
  let httpOkCount = 0;
  let httpFailedCount = 0;
  const missingFiles = [];
  const httpFailedFiles = [];

  const assetList = Array.from(assetsToVerify);
  for (let i = 0; i < assetList.length; i++) {
    const relPath = assetList[i];
    const fullDiskPath = path.join(baseDir, relPath);
    
    // Check disk
    if (fs.existsSync(fullDiskPath)) {
      const size = fs.statSync(fullDiskPath).size;
      if (size > 0) {
        diskOkCount++;
      } else {
        diskMissingCount++;
        missingFiles.push({ path: relPath, reason: 'Zero bytes on disk' });
      }
    } else {
      diskMissingCount++;
      missingFiles.push({ path: relPath, reason: 'File not found on disk' });
    }

    // Check HTTP delivery
    const encodedPath = relPath.split('/').map(encodeURIComponent).join('/');
    const url = `http://localhost:3000/%D0%90%D0%A1%D0%A2%D0%A0%D0%90_%D0%90%D0%A1%D0%A1%D0%95%D0%A2%D0%AB/${encodedPath}`;
    const httpRes = await checkUrl(url);

    if (httpRes.statusCode === 200 && httpRes.contentLength > 0) {
      httpOkCount++;
    } else {
      httpFailedCount++;
      httpFailedFiles.push({ path: relPath, status: httpRes.statusCode, bytes: httpRes.contentLength });
    }
  }

  console.log('\n================ РЕЗУЛЬТАТЫ ГЛУБОКОГО АУДИТА ================');
  console.log(`• Всего проверено уникальных файлов: ${assetList.length}`);
  console.log(`• На диске в наличии (>0 байт):       ${diskOkCount} / ${assetList.length} (${(diskOkCount/assetList.length*100).toFixed(1)}%)`);
  console.log(`• Успешно отдаются по HTTP 200:       ${httpOkCount} / ${assetList.length} (${(httpOkCount/assetList.length*100).toFixed(1)}%)`);
  console.log(`• Ошибок на диске:                    ${diskMissingCount}`);
  console.log(`• Ошибок HTTP:                        ${httpFailedCount}`);

  if (missingFiles.length > 0) {
    console.log('\n[ОШИБКИ ДИСКА]:');
    missingFiles.forEach(m => console.log(`  - ${m.path} (${m.reason})`));
  }
  if (httpFailedFiles.length > 0) {
    console.log('\n[ОШИБКИ СЕТИ HTTP]:');
    httpFailedFiles.forEach(h => console.log(`  - ${h.path} (HTTP ${h.status}, ${h.bytes}b)`));
  }

  if (diskMissingCount === 0 && httpFailedCount === 0) {
    console.log('\n[ИТОГ]: ИДЕАЛЬНО! ВСЕ 100% АССЕТОВ ВЕРИФИЦИРОВАНЫ И ОТДАЮТСЯ СЕРВЕРОМ БЕЗ ОШИБОК!');
  }

  // Breakdown by category
  console.log('\n--- ДЕТАЛИЗАЦИЯ ПО КАТЕГОРИЯМ ---');
  const catSummary = [
    { cat: '3D Сферы Луны (1-30)', count: 30 },
    { cat: 'Таро Карты (01_ТАРО_КАРТЫ)', count: tarotCardsOnDisk.length },
    { cat: 'Скандинавские Руны (02_СКАНДИНАВСКИЕ_РУНЫ)', count: runesOnDisk.length },
    { cat: 'Девы Мудрости (03_ДЕВЫ_МУДРОСТИ)', count: wisdomOnDisk.length },
    { cat: 'Божества & Символы (04_СИМВОЛЫ_И_БОЖЕСТВА)', count: symbolsOnDisk.length },
    { cat: 'Фоны Лунного Календаря (09_ФОНЫ_ЛУННОГО_КАЛЕНДАРЯ)', count: bgsOnDisk.length },
    { cat: 'ИИ Астрологи (10_ПЕРСОНАЖИ_ИИ_АСТРОЛОГИ)', count: personasOnDisk.length },
    { cat: 'Аватары и Тотемы (11_ДЕФОЛТНЫЕ_И_AI_АВАТАРЫ)', count: avatarsOnDisk.length }
  ];
  catSummary.forEach(c => console.log(`  ✓ ${c.cat}: ${c.count} шт.`));

  fs.writeFileSync('D:/projects/monly/deep_asset_audit_report.json', JSON.stringify({
    total: assetList.length,
    diskOk: diskOkCount,
    httpOk: httpOkCount,
    diskMissing: diskMissingCount,
    httpFailed: httpFailedCount,
    missingFiles,
    httpFailedFiles,
    categories: catSummary
  }, null, 2));
}

runComprehensiveAudit();
