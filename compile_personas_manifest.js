const fs = require('fs');
const path = require('path');

const srcDir = 'D:/projects/monly/фигасе/СОРТИРОВАННЫЕ_АССЕТЫ/10_ПЕРСОНАЖИ_ИИ_АСТРОЛОГИ';
const targetDir = 'D:/projects/monly/АСТРА_АССЕТЫ/10_ПЕРСОНАЖИ_ИИ_АСТРОЛОГИ';
if (!fs.existsSync(targetDir)) fs.mkdirSync(targetDir, { recursive: true });

const PERSONA_STYLE_CORE = "cinematic luxury portrait of a warm serene spiritual mentor for Astra wellness app, gentle eyes, subtle genuine smile, soft natural studio portrait lighting with golden rim glow, warm earthy pastel background of sage and soft terracotta, elegant minimalist styling, modern quiet luxury aesthetic, 8k, square --v 6.1";

const personas = [
  {
    id: 1,
    name: "Luna",
    title_ru: "Мудрый Мистик",
    title_en: "Wise Mystic",
    focus: "Интуиция, глубокие ведические ритуалы, лунные циклы и медитация",
    srcFile: path.join(srcDir, "01_Luna_Wise_Mystic.png"),
    targetFile: path.join(targetDir, "01_Luna_Wise_Mystic.webp"),
    controlNet: { mode: "OpenPose/Face", strength: 0.35, denoise: 0.65 },
    prompt: `Portrait of Luna, a young wise mystic woman with ethereal soft platinum hair, serene and knowing gaze, ${PERSONA_STYLE_CORE}`
  },
  {
    id: 2,
    name: "Nova",
    title_ru: "Космический Коуч",
    title_en: "Cosmic Coach",
    focus: "Карьера, реализация потенциала, раскрытие талантов, смелые цели",
    srcFile: path.join(srcDir, "02_Nova_Cosmic_Coach.png"),
    targetFile: path.join(targetDir, "02_Nova_Cosmic_Coach.webp"),
    controlNet: { mode: "OpenPose/Face", strength: 0.35, denoise: 0.65 },
    prompt: `Portrait of Nova, an inspiring energetic female cosmic life coach with radiant smile and warm wavy brunette hair, ${PERSONA_STYLE_CORE}`
  },
  {
    id: 3,
    name: "Selena",
    title_ru: "Эмпатичный Оракул",
    title_en: "Empathic Oracle",
    focus: "Отношения, любовь, глубинная психология, исцеление сердечных ран",
    srcFile: path.join(srcDir, "03_Selena_Empathic_Oracle.png"),
    targetFile: path.join(targetDir, "03_Selena_Empathic_Oracle.webp"),
    controlNet: { mode: "OpenPose/Face", strength: 0.35, denoise: 0.65 },
    prompt: `Portrait of Selena, an empathetic gentle oracle woman with compassionate warm eyes and delicate features, ${PERSONA_STYLE_CORE}`
  },
  {
    id: 4,
    name: "Aurora",
    title_ru: "Холистический Целитель",
    title_en: "Holistic Healer",
    focus: "Баланс тела и духа, телесные практики, заземление, здоровый сон",
    srcFile: path.join(srcDir, "04_Aurora_Holistic_Healer.png"),
    targetFile: path.join(targetDir, "04_Aurora_Holistic_Healer.webp"),
    controlNet: { mode: "OpenPose/Face", strength: 0.35, denoise: 0.65 },
    prompt: `Portrait of Aurora, a holistic healer woman with warm glowing complexion, curly natural hair, calm grounding energy, ${PERSONA_STYLE_CORE}`
  },
  {
    id: 5,
    name: "Orion",
    title_ru: "Звездный Стратег",
    title_en: "Celestial Strategist",
    focus: "Бизнес, финансовые периоды, тайминг сделок, структурные решения",
    srcFile: path.join(srcDir, "05_Orion_Celestial_Strategist.png"),
    targetFile: path.join(targetDir, "05_Orion_Celestial_Strategist.webp"),
    controlNet: { mode: "OpenPose/Face", strength: 0.35, denoise: 0.65 },
    prompt: `Portrait of Orion, a calm charismatic male celestial strategist with intelligent observant gaze and tidy styling, ${PERSONA_STYLE_CORE}`
  }
];

fs.writeFileSync(path.join('D:/projects/monly/АСТРА_АССЕТЫ', 'personas_generation_manifest.json'), JSON.stringify(personas, null, 2), 'utf8');
fs.writeFileSync(path.join('D:/projects/monly/АСТРА_АССЕТЫ/astra_ru_data', 'personas_ru.json'), JSON.stringify(personas, null, 2), 'utf8');
console.log('Compiled Personas Manifest and Localized personas_ru.json for GigaChat context!');
