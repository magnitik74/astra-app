const fs = require('fs');
const path = require('path');

console.log('--- Astra Cosmic Guide: Localizing Calendar 2026 ---');

// Load Raw Calendar
let raw = fs.readFileSync('D:/projects/monly/фигасе/json_data/calendar_2026_full.json', 'utf8');
if (raw.charCodeAt(0) === 0xFEFF) raw = raw.slice(1);
const rawData = JSON.parse(raw);
const days = rawData.data;

// Translation Dictionaries
const zodiacRu = {
  'Aries': { name: 'Овен', element: 'Огонь', ruler: 'Марс' },
  'Taurus': { name: 'Телец', element: 'Земля', ruler: 'Венера' },
  'Gemini': { name: 'Близнецы', element: 'Воздух', ruler: 'Меркурий' },
  'Cancer': { name: 'Рак', element: 'Вода', ruler: 'Луна' },
  'Leo': { name: 'Лев', element: 'Огонь', ruler: 'Солнце' },
  'Virgo': { name: 'Дева', element: 'Земля', ruler: 'Меркурий' },
  'Libra': { name: 'Весы', element: 'Воздух', ruler: 'Венера' },
  'Scorpio': { name: 'Скорпион', element: 'Вода', ruler: 'Марс / Кету' },
  'Sagittarius': { name: 'Стрелец', element: 'Огонь', ruler: 'Юпитер' },
  'Capricorn': { name: 'Козерог', element: 'Земля', ruler: 'Сатурн' },
  'Aquarius': { name: 'Водолей', element: 'Воздух', ruler: 'Сатурн / Раху' },
  'Pisces': { name: 'Рыбы', element: 'Вода', ruler: 'Юпитер' }
};

const planetRu = {
  'Sun': { ru: 'Сурья (Солнце)', qualities: 'Жизненная сила, лидерство, уверенность' },
  'Moon': { ru: 'Чандра (Луна)', qualities: 'Интуиция, покой ума, эмоциональная гармония' },
  'Mars': { ru: 'Мангала (Марс)', qualities: 'Энергия действия, смелость, преодоление преград' },
  'Mercury': { ru: 'Будха (Меркурий)', qualities: 'Ясность мысли, общение, обучение, торговля' },
  'Jupiter': { ru: 'Гуру (Юпитер)', qualities: 'Мудрость, духовные знания, расширение, удача' },
  'Venus': { ru: 'Шукра (Венера)', qualities: 'Красота, любовь, творчество, эстетическое наслаждение' },
  'Saturn': { ru: 'Шани (Сатурн)', qualities: 'Дисциплина, терпение, заземление, внутренняя опора' }
};

const moonPhaseRu = {
  'Waxing Moon': 'Растущая Луна (Шукла Пакша)',
  'Full Moon': 'Полнолуние (Пурнима)',
  'Waning Moon': 'Убывающая Луна (Кришна Пакша)',
  'New Moon': 'Новолуние (Амавасья)'
};

const tithiRu = {
  1: { name: '1-й Лунный день (Пратипад)', meaning: 'Семя месяца — чистое намерение, тишина и зарождение замысла' },
  2: { name: '2-й Лунный день (Двитья)', meaning: 'Мягкий свет — закладка фундамента, питание и спокойные планы' },
  3: { name: '3-й Лунный день (Тритья)', meaning: 'Сила всходов — решительность, энергия действия и проявление воли' },
  4: { name: '4-й Лунный день (Чатуртхи)', meaning: 'Преодоление преград — осознанность, бдительность и стойкость духа' },
  5: { name: '5-й Лунный день (Панчами)', meaning: 'Свет познания — обучение, творчество, целительство и благословение' },
  6: { name: '6-й Лунный день (Шашти)', meaning: 'Внутренний воин — дисциплина, победа над сомнениями и забота о теле' },
  7: { name: '7-й Лунный день (Саптами)', meaning: 'Путь странника — гармония движения, новые горизонты и вдохновение' },
  8: { name: '8-й Лунный день (Аштами)', meaning: 'Трансформация — очищение от старых привязанностей, баланс сил' },
  9: { name: '9-й Лунный день (Навами)', meaning: 'Магия воли — концентрация, устранение иллюзий и уверенность' },
  10: { name: '10-й Лунный день (Дашами)', meaning: 'Врата победы — успешные начинания, общественное признание и дела' },
  11: { name: '11-й Лунный день (Экадаши)', meaning: 'Священный пост — очищение ума и тела, глубокая медитация и ясность' },
  12: { name: '12-й Лунный день (Двадаши)', meaning: 'Милосердие — щедрость, дарение тепла, благодарность и прощение' },
  13: { name: '13-й Лунный день (Трайодаши)', meaning: 'Омоложение — исцеление, радость общения, обновление связей' },
  14: { name: '14-й Лунный день (Чатурдаши)', meaning: 'Порог кульминации — глубинная очистка перед полной Луной' },
  15: { name: '15-й Лунный день (Пурнима — Полнолуние)', meaning: 'Зенит сияния — пик интуиции, наполненность чувств и духовная сила' },
  16: { name: '16-й Лунный день (Пратипад убывающей)', meaning: 'Щедрость плодов — передача знаний, щедрость и покой' },
  17: { name: '17-й Лунный день (Двитья убывающей)', meaning: 'Радость бытия — праздник души, творчество и единение сердец' },
  18: { name: '18-й Лунный день (Тритья убывающей)', meaning: 'Зеркало правды — самоанализ, избавление от чужих масок' },
  19: { name: '19-й Лунный день (Чатуртхи убывающей)', meaning: 'Лабиринт мысли — верность себе, осторожность и осознанный покой' },
  20: { name: '20-й Лунный день (Панчами убывающей)', meaning: 'Парение орла — преодоление сомнений, масштабный взгляд на жизнь' },
  21: { name: '21-й Лунный день (Шашти убывающей)', meaning: 'Командный дух — дружба, верность союзам и вдохновляющая беседа' },
  22: { name: '22-й Лунный день (Саптами убывающей)', meaning: 'Печать мудрости — глубокие инсайты, чтение священных текстов' },
  23: { name: '23-й Лунный день (Аштами убывающей)', meaning: 'Внутренняя броня — защита личных границ, твердость и очищение' },
  24: { name: '24-й Лунный день (Навами убывающей)', meaning: 'Пробуждение созидания — телесная сила, исцеление и покой' },
  25: { name: '25-й Лунный день (Дашами убывающей)', meaning: 'Тихие воды — слушание внутреннего голоса, уединение и мудрость' },
  26: { name: '26-й Лунный день (Экадаши убывающей)', meaning: 'Очищение кармы — легкая пища, молитва и освобождение от долгов' },
  27: { name: '27-й Лунный день (Двадаши убывающей)', meaning: 'Океаническая интуиция — морские сны, мягкость и прозрения' },
  28: { name: '28-й Лунный день (Трайодаши убывающей)', meaning: 'Постижение гармонии — умиротворение, светлая радость и благодарность' },
  29: { name: '29-й Лунный день (Чатурдаши убывающей)', meaning: 'Очищающий вихрь — завершение старого цикла, прощение обид' },
  30: { name: '30-й Лунный день (Амавасья — Новолуние)', meaning: 'Космическое безмолвие — перезагрузка духа, благословение предков' }
};

const nakshatraRu = {
  'Ashwini': { ru: 'Ашвини', symbol: 'Голова коня', essence: 'Стремительное исцеление, импульс к началу' },
  'Bharani': { ru: 'Бхарани', symbol: 'Йони / Лоно', essence: 'Священное терпение, вынашивание плодов' },
  'Krittika': { ru: 'Криттика', symbol: 'Пламя / Клинок', essence: 'Очищающий огонь, кристальная ясность мысли' },
  'Rohini': { ru: 'Рохини', symbol: 'Колесница', essence: 'Изобилие, женская притягательность, земная любовь' },
  'Mrigashira': { ru: 'Мригашира', symbol: 'Голова оленя', essence: 'Любознательный поиск истины, нежность чувств' },
  'Ardra': { ru: 'Ардра', symbol: 'Слеза / Алмаз', essence: 'Очищающая гроза, сброс напряжения, прозрение' },
  'Punarvasu': { ru: 'Пунарвасу', symbol: 'Колчан со стрелами', essence: 'Возвращение света, исцеляющий дом, надежда' },
  'Pushya': { ru: 'Пушья', symbol: 'Цветок лотоса', essence: 'Самая благословенная накшатра, духовная опора' },
  'Ashlesha': { ru: 'Ашлеша', symbol: 'Свернувшаяся змея', essence: 'Глубинная интуиция, психологическая мудрость' },
  'Magha': { ru: 'Магха', symbol: 'Трон предков', essence: 'Царственное достоинство, связь с родом' },
  'Purva Phalguni': { ru: 'Пурва Пхалгуни', symbol: 'Гамак', essence: 'Наслаждение жизнью, романтика, отдых и шарм' },
  'Uttara Phalguni': { ru: 'Уттара Пхалгуни', symbol: 'Ложе союза', essence: 'Верность договоренностям, честность и долг' },
  'Hasta': { ru: 'Хаста', symbol: 'Ладонь', essence: 'Мастерство рук, чуткость, созидание и целительство' },
  'Chitra': { ru: 'Читра', symbol: 'Сверкающий жемчуг', essence: 'Архитектура красоты, дизайн, творческое сияние' },
  'Swati': { ru: 'Свати', symbol: 'Молодой побег', essence: 'Свободный ветер, независимость, гибкость ума' },
  'Vishakha': { ru: 'Вишакха', symbol: 'Триумфальная арка', essence: 'Железная воля, достижение великой цели' },
  'Anuradha': { ru: 'Анурадха', symbol: 'Цветущий лотос', essence: 'Преданная дружба, гармония сердец и путешествия' },
  'Jyeshtha': { ru: 'Джьештха', symbol: 'Круглый амулет', essence: 'Внутренний авторитет, защита близких, зрелость' },
  'Mula': { ru: 'Мула', symbol: 'Связка корней', essence: 'Постижение первопричины, разрушение иллюзий' },
  'Purva Ashadha': { ru: 'Пурва Ашадха', symbol: 'Веер', essence: 'Непобедимая вера в мечту, эмоциональный взлет' },
  'Uttara Ashadha': { ru: 'Уттара Ашадха', symbol: 'Бивни слона', essence: 'Благородный триумф, высшая этика и стойкость' },
  'Shravana': { ru: 'Шравана', symbol: 'Три уха / Следы', essence: 'Умение слышать шепот Вселенной, знание истины' },
  'Dhanishta': { ru: 'Дханишта', symbol: 'Барабан Шивы', essence: 'Ритм изобилия, музыка души, материальный успех' },
  'Shatabhisha': { ru: 'Шатабхиша', symbol: 'Сто звезд', essence: 'Тайна космического исцеления, тишина и покой' },
  'Purva Bhadrapada': { ru: 'Пурва Бхадрапада', symbol: 'Меч очищения', essence: 'Мистическая глубина, духовный прорыв' },
  'Uttara Bhadrapada': { ru: 'Уттара Бхадрапада', symbol: 'Змея глубин', essence: 'Абсолютный мир в сердце, мудрость сострадания' },
  'Revati': { ru: 'Ревати', symbol: 'Рыба в океане', essence: 'Безусловная любовь, мягкий финал и покровительство' }
};

const activityNamesRu = {
  'nutrition': 'Питание и диета',
  'planting': 'Дом и растения',
  'selfCare': 'Забота о себе',
  'travelling': 'Поездки и дорога',
  'career': 'Карьера и бизнес',
  'spirituality': 'Духовные практики',
  'health': 'Здоровье и спорт',
  'beauty': 'Красота и спа',
  'completion': 'Завершение дел',
  'romance': 'Романтика и чувства',
  'bigDecision': 'Важные решения',
  'socialActivity': 'Общение и связи'
};

const statusMap = {
  2: 'Благоприятно',
  0: 'Нейтрально',
  1: 'Неблагоприятно'
};

const astraCalendar = [];

for (const day of days) {
  const moonEvent = (day.events || []).find(e => e.moonContent && e.moonContent.moonDay);
  const holidayEvent = (day.events || []).find(e => e.holidayContent);
  const dailyEvent = (day.events || []).find(e => e.dailyContent);

  const tithiNum = day.moonDay || (moonEvent ? moonEvent.moonContent.moonDay.number : 1);
  const tithiInfo = tithiRu[tithiNum] || { name: `${tithiNum}-й лунный день`, meaning: 'День космического ритма' };

  let nakshatraInfo = null;
  if (moonEvent && moonEvent.moonContent.nakshatra) {
    const rawName = moonEvent.moonContent.nakshatra.name;
    nakshatraInfo = nakshatraRu[rawName] || { ru: rawName, symbol: '', essence: '' };
    nakshatraInfo.raw = rawName;
    nakshatraInfo.number = moonEvent.moonContent.nakshatra.number;
  }

  let signInfo = null;
  if (moonEvent && moonEvent.moonContent.sign) {
    const rawSign = moonEvent.moonContent.sign.name;
    signInfo = zodiacRu[rawSign] || { name: rawSign, element: '', ruler: '' };
    signInfo.raw = rawSign;
    signInfo.number = moonEvent.moonContent.sign.number;
  }

  let planetInfo = null;
  if (moonEvent && moonEvent.moonContent.planet) {
    const rawPlanet = moonEvent.moonContent.planet.name;
    planetInfo = planetRu[rawPlanet] || { ru: rawPlanet, qualities: '' };
    planetInfo.raw = rawPlanet;
  }

  // Phase
  const rawPhase = moonEvent && moonEvent.header ? moonEvent.header.subTitle : 'Waxing Moon';
  const phaseRu = moonPhaseRu[rawPhase] || rawPhase;

  // Spheres of Life
  const spheres = {};
  if (day.dayProperties) {
    for (const [key, val] of Object.entries(day.dayProperties)) {
      if (activityNamesRu[key]) {
        spheres[key] = {
          name: activityNamesRu[key],
          score: val,
          status: statusMap[val] || 'Нейтрально'
        };
      }
    }
  }

  // Daily Advice / Insight
  let dailyInsight = null;
  if (dailyEvent && dailyEvent.dailyContent) {
    dailyInsight = {
      title: dailyEvent.dailyContent.title,
      good: dailyEvent.dailyContent.goodDescription,
      warning: dailyEvent.dailyContent.badDescription
    };
  }

  // Holiday
  let holiday = null;
  if (holidayEvent && holidayEvent.holidayContent) {
    holiday = {
      title: holidayEvent.holidayContent.title,
      isEkadashi: !!holidayEvent.holidayContent.ekadashi,
      description: holidayEvent.holidayContent.description
    };
  }

  astraCalendar.push({
    date: day.date,
    tithi: {
      number: tithiNum,
      name: tithiInfo.name,
      meaning: tithiInfo.meaning,
      phase: phaseRu
    },
    nakshatra: nakshatraInfo,
    zodiacSign: signInfo,
    planetaryRuler: planetInfo,
    isEkadashi: day.dayProperties ? !!day.dayProperties.ekadashi : false,
    spheres: spheres,
    dailyInsight: dailyInsight,
    holiday: holiday
  });
}

const outPath = 'D:/projects/monly/АСТРА_АССЕТЫ/astra_ru_data/astra_calendar_2026_ru.json';
fs.writeFileSync(outPath, JSON.stringify(astraCalendar, null, 2), 'utf8');

const fileSizeMb = (fs.statSync(outPath).size / (1024 * 1024)).toFixed(2);
console.log(`\nSUCCESS! Created Russian Calendar 2026: ${outPath}`);
console.log(`Processed ${astraCalendar.length} days. File size: ${fileSizeMb} MB (compact & clean native JSON)`);
