const fs = require('fs');
const path = require('path');

const baseSorted = 'D:/projects/monly/фигасе/СОРТИРОВАННЫЕ_АССЕТЫ';
const targetRoot = 'D:/projects/monly/АСТРА_АССЕТЫ';
const jsonDir = 'D:/projects/monly/фигасе/json_data';

// ==========================================
// 1. МАНИФЕСТ ДЛЯ 02_СКАНДИНАВСКИЕ_РУНЫ (24 шт)
// ==========================================
try {
  let raw = fs.readFileSync(path.join(jsonDir, 'cards_type_1_runes.json'), 'utf8');
  if (raw.charCodeAt(0) === 0xFEFF) raw = raw.slice(1);
  const runes = JSON.parse(raw).data || JSON.parse(raw);
  
  const RUNE_STYLE_CORE = "smooth tactile river pebble stone talisman, rounded matte dark navy and charcoal ceramic pebble, engraved sacred ivory runic symbol with soft inner glow, studio lighting with gentle soft rim light, clean solid background, minimalist zen aesthetic, 8k, square --v 6.1";

  const runeManifest = runes.map((r, idx) => {
    const num = (r.order !== undefined ? r.order : idx).toString().padStart(2, '0');
    const safeName = r.name.replace(/[\/\\:\*\?"<>\|]/g, '_').replace(/\s+/g, '_');
    const srcFile = path.join(baseSorted, '02_СКАНДИНАВСКИЕ_РУНЫ', `${num}_${safeName}.png`);
    
    return {
      order: r.order !== undefined ? r.order : idx,
      id: r.id,
      name: r.name,
      originalFile: srcFile,
      targetFile: path.join(targetRoot, '02_СКАНДИНАВСКИЕ_РУНЫ', `${num}_${safeName}.webp`),
      controlNet: { mode: "Depth/Silhouette", strength: 0.35, denoise: 0.65 },
      prompt: `Elder Futhark Rune ${r.name}, symbolizing ${r.normal?.descriptionShort || 'ancient wisdom'}, ${RUNE_STYLE_CORE}`
    };
  });

  fs.writeFileSync(path.join(targetRoot, 'runes_generation_manifest.json'), JSON.stringify(runeManifest, null, 2), 'utf8');
  console.log(`Compiled Runes Manifest: ${runeManifest.length} items`);
} catch(e) { console.error('Runes manifest error:', e.message); }

// ==========================================
// 2. МАНИФЕСТ ДЛЯ 03_ДЕВЫ_МУДРОСТИ (57 шт)
// ==========================================
try {
  let raw = fs.readFileSync(path.join(jsonDir, 'cards_type_2_wisdom.json'), 'utf8');
  if (raw.charCodeAt(0) === 0xFEFF) raw = raw.slice(1);
  const wisdom = JSON.parse(raw).data || JSON.parse(raw);

  const GODDESS_STYLE_CORE = "ethereal celestial muse goddess representing cosmic harmony, serene porcelain features, flowing hair with delicate golden diadem, soft volumetric backlighting, muted soothing pastel palette of sage, terracotta, dusty rose and cream, peaceful meditative mood, high-end digital painting, 8k --ar 9:16 --v 6.1";

  const wisdomManifest = wisdom.map((w, idx) => {
    const num = (w.order !== undefined ? w.order : idx).toString().padStart(2, '0');
    const safeName = w.name.replace(/[\/\\:\*\?"<>\|]/g, '_').replace(/\s+/g, '_');
    const srcFile = path.join(baseSorted, '03_ДЕВЫ_МУДРОСТИ', `${num}_${safeName}.png`);

    return {
      order: w.order !== undefined ? w.order : idx,
      id: w.id,
      name: w.name,
      originalFile: srcFile,
      targetFile: path.join(targetRoot, '03_ДЕВЫ_МУДРОСТИ', `${num}_${safeName}.webp`),
      controlNet: { mode: "OpenPose/Face", strength: 0.35, denoise: 0.65 },
      prompt: `Celestial Goddess of ${w.name}, ${GODDESS_STYLE_CORE}`
    };
  });

  fs.writeFileSync(path.join(targetRoot, 'wisdom_generation_manifest.json'), JSON.stringify(wisdomManifest, null, 2), 'utf8');
  console.log(`Compiled Wisdom Manifest: ${wisdomManifest.length} items`);
} catch(e) { console.error('Wisdom manifest error:', e.message); }

// ==========================================
// 3. МАНИФЕСТ ДЛЯ 04_СИМВОЛЫ_И_БОЖЕСТВА (40 шт)
// ==========================================
try {
  let raw = fs.readFileSync(path.join(jsonDir, 'cards_type_3_symbols.json'), 'utf8');
  if (raw.charCodeAt(0) === 0xFEFF) raw = raw.slice(1);
  const symbols = JSON.parse(raw).data || JSON.parse(raw);

  const TEMPLE_STYLE_CORE = "stylized Vedic temple sculpture of sacred deity, serene calm facial expression with hands in peaceful namaste blessing, soft matte clay and terra-cotta texture, framed by an elegant arched temple alcove, warm glowing celestial planet sphere behind, ambient candlelight, sacred geometry, 8k --ar 9:16 --v 6.1";

  const symbolsManifest = symbols.map((s, idx) => {
    const num = (s.order !== undefined ? s.order : idx).toString().padStart(2, '0');
    const safeName = s.name.replace(/[\/\\:\*\?"<>\|]/g, '_').replace(/\s+/g, '_');
    const srcFile = path.join(baseSorted, '04_СИМВОЛЫ_И_БОЖЕСТВА', `${num}_${safeName}.png`);

    return {
      order: s.order !== undefined ? s.order : idx,
      id: s.id,
      name: s.name,
      originalFile: srcFile,
      targetFile: path.join(targetRoot, '04_СИМВОЛЫ_И_БОЖЕСТВА', `${num}_${safeName}.webp`),
      controlNet: { mode: "Depth/Pose", strength: 0.35, denoise: 0.65 },
      prompt: `Sacred Vedic Planetary Deity ${s.name}, ${TEMPLE_STYLE_CORE}`
    };
  });

  fs.writeFileSync(path.join(targetRoot, 'symbols_generation_manifest.json'), JSON.stringify(symbolsManifest, null, 2), 'utf8');
  console.log(`Compiled Symbols Manifest: ${symbolsManifest.length} items`);
} catch(e) { console.error('Symbols manifest error:', e.message); }

// ==========================================
// 4. МАНИФЕСТ ДЛЯ 09_ФОНЫ_ЛУННОГО_КАЛЕНДАРЯ (82 шт)
// ==========================================
try {
  const bgFiles = fs.readdirSync(path.join(baseSorted, '09_ФОНЫ_ЛУННОГО_КАЛЕНДАРЯ'));
  const LANDSCAPE_STYLE_CORE = "atmospheric minimalist landscape for cosmic wellness app, serene calm lake reflecting mountain silhouettes under soft twilight sky, warm gradient palette of dusty peach, sage green, and muted lavender, cinematic fine mist, gentle tranquil mood, 35mm film grain texture, high resolution, vertical 9:16 --v 6.1";

  const bgManifest = bgFiles.map((f, idx) => {
    const nameWithoutExt = path.basename(f, path.extname(f));
    return {
      index: idx + 1,
      originalFile: path.join(baseSorted, '09_ФОНЫ_ЛУННОГО_КАЛЕНДАРЯ', f),
      targetFile: path.join(targetRoot, '09_ФОНЫ_ЛУННОГО_КАЛЕНДАРЯ', `${nameWithoutExt}.webp`),
      controlNet: { mode: "Depth/ColorGrading", strength: 0.35, denoise: 0.65 },
      prompt: `Serene celestial twilight scenery for ${nameWithoutExt}, ${LANDSCAPE_STYLE_CORE}`
    };
  });

  fs.writeFileSync(path.join(targetRoot, 'backgrounds_generation_manifest.json'), JSON.stringify(bgManifest, null, 2), 'utf8');
  console.log(`Compiled Backgrounds Manifest: ${bgManifest.length} items`);
} catch(e) { console.error('Backgrounds manifest error:', e.message); }
