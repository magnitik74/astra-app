const fs = require('fs');
const path = require('path');

const srcManifest = 'D:/projects/monly/АСТРА_АССЕТЫ/astra_ru_data/astra_mentors_system.json';
const targetManifest = 'D:/projects/monly/АСТРА_АССЕТЫ/personas_generation_manifest.json';
const srcImagesDir = 'D:/projects/monly/фигасе/СОРТИРОВАННЫЕ_АССЕТЫ/10_ПЕРСОНАЖИ_ИИ_АСТРОЛОГИ';
const targetImagesDir = 'D:/projects/monly/АСТРА_АССЕТЫ/10_ПЕРСОНАЖИ_ИИ_АСТРОЛОГИ';

const data = JSON.parse(fs.readFileSync(srcManifest, 'utf8'));

const originalFileMapping = {
  1: '01_Luna_Wise_Mystic.png',
  2: '02_Nova_Cosmic_Coach.png',
  3: '03_Selena_Empathic_Oracle.png',
  4: '04_Aurora_Holistic_Healer.png',
  5: '05_Orion_Celestial_Strategist.png'
};

const fullManifest = data.personas.map(p => {
  const origFile = originalFileMapping[p.id];
  const origPath = path.join(srcImagesDir, origFile);
  const targetFile = path.join(targetImagesDir, `0${p.id}_${p.name_ru}_${p.code}.webp`);

  return {
    id: p.id,
    code: p.code,
    name_ru: p.name_ru,
    title_ru: p.title_ru,
    archetype: p.archetype,
    element: p.element,
    key_planets: p.key_planets,
    voice_tone: p.voice_tone,
    specialization: p.specialization,
    system_prompt_gigachat: p.system_prompt_gigachat,
    originalSourceImage: origPath,
    originalExists: fs.existsSync(origPath),
    targetFile: targetFile,
    controlNetConfig: {
      mode: "OpenPose / Face Reference",
      sourceImage: origPath,
      strength: 0.35,
      denoise: 0.65
    },
    generationPrompt: p.visual_dna.generation_prompt
  };
});

fs.writeFileSync(targetManifest, JSON.stringify(fullManifest, null, 2), 'utf8');
console.log(`Successfully compiled updated personas generation manifest with ${fullManifest.length} mentors!`);
