const fs = require('fs');
const path = require('path');

const srcJson = 'D:/projects/monly/фигасе/json_data/cards_type_0_tarot.json';
const srcImagesDir = 'D:/projects/monly/фигасе/СОРТИРОВАННЫЕ_АССЕТЫ/01_ТАРО_КАРТЫ';
const targetDir = 'D:/projects/monly/АСТРА_АССЕТЫ/01_ТАРО_КАРТЫ';
const outputManifest = 'D:/projects/monly/АСТРА_АССЕТЫ/tarot_generation_manifest.json';

let raw = fs.readFileSync(srcJson, 'utf8');
if (raw.charCodeAt(0) === 0xFEFF) raw = raw.slice(1);
const cards = JSON.parse(raw).data || JSON.parse(raw);

// Базовый суффикс нашего фирменного стиля АСТРА (тактильный 3D Clay, утренний теплый свет, персик и шалфей, мягкие матовые текстуры)
const ASTRA_STYLE_CORE = "whimsical soft 3D clay animation style, cute rounded clay characters and objects, tactile matte velvet clay and felt texture, warm diffused morning sunlight with subtle golden rim lighting, cozy peaceful atmosphere, studio clay miniature sculpture, pastel palette of warm peach, beige, terracotta and sage green, clean solid background, masterpiece, 8k --ar 9:16 --v 6.1";

const promptMap = {
  "The Fool": "A whimsical young traveler in a pointed soft jester hat holding a wooden staff with a small bundle over shoulder, walking cheerfully on the edge of a cliff, accompanied by a happy small white clay dog looking up, a playful cute crocodile below in water, golden warm sun rising above",
  "The Magician": "A serene young mystic standing behind a stone altar with four sacred elemental tools (cup, wand, sword, pentacle coin), one hand raised toward the glowing sky holding a small wand, the other pointing down to earth, glowing infinity symbol floating above head, blooming roses and lilies around",
  "The High Priestess": "A tranquil sacred priestess sitting between two soft rounded temple pillars (one dark plum, one pale cream), wearing flowing pastel robes and a glowing crescent moon crown, holding a mystical scroll in lap, large soft crescent moon glowing behind, quiet celestial sanctuary",
  "The Empress": "A gentle loving empress resting comfortably on soft velvet cushions in a lush blooming garden, wearing a loose cozy gown, surrounded by soft golden wheat sheaves and wild flowers, warm radiant maternal glow, peace, nature and abundance",
  "The Emperor": "A calm wise leader seated on a solid stone throne decorated with soft carved ram heads, holding a golden scepter and orb, sturdy posture, draped in warm terracotta cloak, gentle confident expression, stylized geometric mountains in background",
  "The Hierophant": "A venerable spiritual mentor seated in a cozy sanctuary, right hand raised in peaceful blessing, two respectful acolytes listening attentively, warm candlelight and soft sacred geometry arches in background",
  "The Lovers": "Two loving figures standing hand in hand under a large benevolent radiant sun, surrounded by lush peaceful garden trees, soft floral blooms, harmonious union and mutual trust",
  "The Chariot": "A brave young hero standing in an ornate stone chariot drawn by two cute rounded resting sphinxes, canopy of stars above, determined but serene expression, moving forward steadily",
  "Strength": "A gentle serene woman lovingly embracing and calming a cute rounded soft golden lion, infinity symbol hovering softly above, flowers winding around them, triumph of gentleness and love over force",
  "The Hermit": "A contemplative wise elder standing alone on a quiet snowy mountain peak, holding a glowing lantern with a six-pointed star inside in one hand and a wooden walking stick in the other, starry night sky, inner guiding light",
  "Wheel of Fortune": "A whimsical rotating celestial stone wheel floating among soft pastel clouds, surrounded by four cute symbolic winged creatures reading scrolls in four corners, cyclical nature of life",
  "Justice": "A balanced serene figure seated on a stone bench holding upright double-edged sword in right hand and golden scales in left, steady calm gaze, draped in balanced drapery",
  "The Hanged Man": "A peaceful figure suspended upside down by one foot from a living T-shaped wooden tree branch, serene relaxed expression with glowing halo of insight around head, calm surrender and higher perspective",
  "Death": "A transformative mystical figure in gentle soft armor holding a white five-petaled rose banner, sunrise breaking over a distant river between two towers, shedding the old to welcome new rebirth, peaceful transformation",
  "Temperance": "A graceful winged angel standing with one foot in a calm sparkling stream and one on stone bank, gently pouring liquid light back and forth between two clay cups, path winding toward golden sun in distant mountains",
  "The Devil": "A whimsical stylized winged creature perched on a stone pedestal with two figures loosely holding draped ribbons, gentle allegorical depiction of habits and attachments, soft shadows, warm playful tone",
  "The Tower": "A stylized stone tower on a rocky summit touched by a gentle lightning flash, crowns of flowers falling softly, stars emerging in the dusk sky, releasing old structures for freedom",
  "The Star": "A naked graceful maiden kneeling beside a calm starry pool, pouring clear water from two jugs (one onto earth, one into pond), large radiant eight-pointed star shining brightly in twilight sky surrounded by seven smaller stars",
  "The Moon": "A glowing golden crescent moon in deep night sky, two cute soft rounded wolves howling by a winding blue river leading from deep hills, friendly crayfish peeking out of water, magical dreamscape",
  "The Sun": "A joyful radiant child riding a friendly white horse under a huge smiling warm golden sun, large sunflowers blooming along a stone wall, pure happiness, vitality and celebration",
  "Judgement": "A benevolent winged angel sounding a gentle golden horn from soft clouds, figures below joyfully raising their hands in awakening and renewal, fresh start and higher calling",
  "The World": "A dancing radiant figure surrounded by an oval wreath of laurel leaves, flanked by four cute rounded guardian totems in four corners, ultimate wholeness, completion and cosmic harmony"
};

const manifest = [];
cards.forEach((c, idx) => {
  const num = (c.order !== undefined ? c.order : idx).toString().padStart(2, '0');
  const safeName = c.name.replace(/[\/\\:\*\?"<>\|]/g, '_').replace(/\s+/g, '_');
  const originalFileName = `${num}_${safeName}.png`;
  const originalFilePath = path.join(srcImagesDir, originalFileName);

  const customPromptSubject = promptMap[c.name] || `A whimsical clay illustration depicting the archetype of ${c.name}, ${c.normal?.descriptionShort || 'symbol of cosmic journey'}`;
  const fullPrompt = `${customPromptSubject}, ${ASTRA_STYLE_CORE}`;

  manifest.push({
    order: c.order !== undefined ? c.order : idx,
    id: c.id,
    name: c.name,
    originalFileName: originalFileName,
    originalFileExists: fs.existsSync(originalFilePath),
    targetFileName: `${num}_${safeName}.webp`,
    controlNetConfig: {
      mode: "Image-to-Image / Depth / Pose",
      sourceImage: originalFilePath,
      strength: 0.35,
      denoise: 0.65
    },
    generationPrompt: fullPrompt
  });
});

fs.writeFileSync(outputManifest, JSON.stringify(manifest, null, 2), 'utf8');
console.log(`Successfully compiled Tarot Generation Manifest with ${manifest.length} cards!`);
console.log(`Manifest saved at: ${outputManifest}`);
