const fs = require('fs');
const path = require('path');

const srcDir = 'D:/projects/monly/фигасе/json_data';
const targetDir = 'D:/projects/monly/АСТРА_АССЕТЫ/astra_ru_data';
if (!fs.existsSync(targetDir)) fs.mkdirSync(targetDir, { recursive: true });

// 1. ПЕРЕВОД ТАРО КАРТ
const tarotRuNames = {
  "The Fool": "Шут",
  "The Magician": "Маг",
  "The High Priestess": "Верховная Жрица",
  "The Empress": "Императрица",
  "The Emperor": "Император",
  "The Hierophant": "Иерофант",
  "The Lovers": "Влюбленные",
  "The Chariot": "Колесница",
  "Strength": "Сила",
  "The Hermit": "Отшельник",
  "Wheel of Fortune": "Колесо Фортуны",
  "Justice": "Справедливость",
  "The Hanged Man": "Повешенный",
  "Death": "Трансформация (Смерть)",
  "Temperance": "Умеренность",
  "The Devil": "Дьявол (Искушение)",
  "The Tower": "Башня",
  "The Star": "Звезда",
  "The Moon": "Луна",
  "The Sun": "Солнце",
  "Judgement": "Возрождение (Суд)",
  "The World": "Мир",
  // Масти
  "Ace of Wands": "Туз Жезлов", "Two of Wands": "Двойка Жезлов", "Three of Wands": "Тройка Жезлов", "Four of Wands": "Четверка Жезлов",
  "Five of Wands": "Пятерка Жезлов", "Six of Wands": "Шестерка Жезлов", "Seven of Wands": "Семерка Жезлов", "Eight of Wands": "Восьмерка Жезлов",
  "Nine of Wands": "Девятка Жезлов", "Ten of Wands": "Десятка Жезлов", "Page of Wands": "Паж Жезлов", "Knight of Wands": "Рыцарь Жезлов",
  "Queen of Wands": "Королева Жезлов", "King of Wands": "Король Жезлов",
  "Ace of Cups": "Туз Кубков", "Two of Cups": "Двойка Кубков", "Three of Cups": "Тройка Кубков", "Four of Cups": "Четверка Кубков",
  "Five of Cups": "Пятерка Кубков", "Six of Cups": "Шестерка Кубков", "Seven of Cups": "Семерка Кубков", "Eight of Cups": "Восьмерка Кубков",
  "Nine of Cups": "Девятка Кубков", "Ten of Cups": "Десятка Кубков", "Page of Cups": "Паж Кубков", "Knight of Cups": "Рыцарь Кубков",
  "Queen of Cups": "Королева Кубков", "King of Cups": "Король Кубков",
  "Ace of Swords": "Туз Мечей", "Two of Swords": "Двойка Мечей", "Three of Swords": "Тройка Мечей", "Four of Swords": "Четверка Мечей",
  "Five of Swords": "Пятерка Мечей", "Six of Swords": "Шестерка Мечей", "Seven of Swords": "Семерка Мечей", "Eight of Swords": "Восьмерка Мечей",
  "Nine of Swords": "Девятка Мечей", "Ten of Swords": "Десятка Мечей", "Page of Swords": "Паж Мечей", "Knight of Swords": "Рыцарь Мечей",
  "Queen of Swords": "Королева Мечей", "King of Swords": "Король Мечей",
  "Ace of Pentacles": "Туз Пентаклей", "Two of Pentacles": "Двойка Пентаклей", "Three of Pentacles": "Тройка Пентаклей", "Four of Pentacles": "Четверка Пентаклей",
  "Five of Pentacles": "Пятерка Пентаклей", "Six of Pentacles": "Шестерка Пентаклей", "Seven of Pentacles": "Семерка Пентаклей", "Eight of Pentacles": "Восьмерка Пентаклей",
  "Nine of Pentacles": "Девятка Пентаклей", "Ten of Pentacles": "Десятка Пентаклей", "Page of Pentacles": "Паж Пентаклей", "Knight of Pentacles": "Рыцарь Пентаклей",
  "Queen of Pentacles": "Королева Пентаклей", "King of Pentacles": "Король Пентаклей"
};

// 2. ПЕРЕВОД РУН
const runeRuNames = {
  "Fehu": { ru: "Феху", meaning: "Изобилие, материальное процветание, созидательная энергия" },
  "Uruz": { ru: "Уруз", meaning: "Первозданная жизненная сила, преодоление препятствий, здоровье" },
  "Thurisaz": { ru: "Турисаз", meaning: "Врата осознания, защита, расчистка пути, воля" },
  "Ansuz": { ru: "Ансуз", meaning: "Божественное озарение, мудрость слова, интуитивное знание" },
  "Raidho": { ru: "Райдо", meaning: "Путь, гармоничное движение, внутренний компас, путешествие" },
  "Kenaz": { ru: "Кеназ", meaning: "Факел вдохновения, прозрение, творческий огонь, исцеление" },
  "Gebo": { ru: "Гебо", meaning: "Дар, гармоничный союз, баланс принятия и отдачи, партнерство" },
  "Wunjo": { ru: "Вуньо", meaning: "Радость бытия, светлая надежда, гармония с миром, триумф" },
  "Hagalaz": { ru: "Хагалаз", meaning: "Очищающая буря, освобождение от иллюзий, трансформация" },
  "Nauthiz": { ru: "Наутиз", meaning: "Преодоление кризиса, терпение, поиск внутреннего стержня" },
  "Isa": { ru: "Иса", meaning: "Пауза, кристальная тишина, концентрация перед новым этапом" },
  "Jera": { ru: "Йера", meaning: "Сбор плодов, щедрый урожай, естественный цикл времени" },
  "Eihwaz": { ru: "Эйваз", meaning: "Мировое древо, несокрушимость, связь времен, духовная стойкость" },
  "Perthro": { ru: "Перт", meaning: "Тайна судьбы, глубинное возрождение, открытие сокрытого" },
  "Algiz": { ru: "Альгиз", meaning: "Высшая защита, связь с высшими силами, щит осознанности" },
  "Sowilo": { ru: "Соуло", meaning: "Солнечная победа, ясность цели, триумф духа, исцеляющий свет" },
  "Tiwaz": { ru: "Тейваз", meaning: "Воин духа, высшая справедливость, верность долгу и победа" },
  "Berkano": { ru: "Беркана", meaning: "Рождение нового, материнская забота, бережный рост, весна" },
  "Ehwaz": { ru: "Эваз", meaning: "Стремительный прогресс, верное соратничество, шаг вперед" },
  "Mannaz": { ru: "Манназ", meaning: "Истинное «Я», самопознание, человечность, коллективный разум" },
  "Laguz": { ru: "Лагуз", meaning: "Живой поток, глубинная женская интуиция, доверие течению жизни" },
  "Ingwaz": { ru: "Ингваз", meaning: "Завершение этапа, созревание новой энергии, плодородие" },
  "Dagaz": { ru: "Дагаз", meaning: "Рассвет, квантовый скачок, прорыв из тьмы к свету, новый день" },
  "Othala": { ru: "Отала", meaning: "Родовое наследие, священный дом, духовные корни, опора" }
};

// 3. ПЕРЕВОД ПЛАНЕТ И ДНЕЙ НЕДЕЛИ (ДЖЙОТИШ)
const planetRu = {
  "Sunday — Sun": { day: "Воскресенье", planet: "Сурья (Солнце)", focus: "Жизненная энергия, лидерство, проявление духа, щедрость", color: "Золотой, оранжевый" },
  "Monday — Moon": { day: "Понедельник", planet: "Чандра (Луна)", focus: "Эмоциональный покой, интуиция, забота о близких, контакт с водой", color: "Белый, серебристый" },
  "Tuesday — Mars": { day: "Вторник", planet: "Мангала (Марс)", focus: "Решительные действия, спорт, смелость, преодоление сомнений", color: "Алый, коралловый" },
  "Wednesday — Mercury": { day: "Среда", planet: "Будха (Меркурий)", focus: "Обучение, переговоры, торговля, гибкость мышления, новые контакты", color: "Зеленый, изумрудный" },
  "Thursday — Jupiter": { day: "Четверг", planet: "Гуру (Юпитер)", focus: "Духовные знания, мудрость, расширение горизонтов, благотворительность", color: "Желтый, шафрановый" },
  "Friday — Venus": { day: "Пятница", planet: "Шукра (Венера)", focus: "Красота, искусство, романтика, уют, наслаждение прекрасным", color: "Розовый, пастельный" },
  "Saturday — Saturn": { day: "Суббота", planet: "Шани (Сатурн)", focus: "Дисциплина, заземление, уединение, избавление от лишнего, порядок", color: "Синий, графитовый" }
};

// 4. ПЕРЕВОД 27 НАКШАТР (ЛУННЫХ СТОЯНОК)
const nakshatraRu = {
  "Ashwini": "Ашвини (Целительная энергия, стремительные начинания)",
  "Bharani": "Бхарани (Глубокая трансформация, священное терпение)",
  "Krittika": "Криттика (Очищающий огонь, ясность мысли и воли)",
  "Rohini": "Рохини (Творческое плодородие, красота и чувственность)",
  "Mrigashira": "Мригашира (Поиск истины, любознательность, мягкость)",
  "Ardra": "Ардра (Очищающая гроза, обновление через слезы и инсайт)",
  "Punarvasu": "Пунарвасу (Возвращение света, обновление ресурса, дом)",
  "Pushya": "Пушья (Питающая благодать, духовный расцвет, забота)",
  "Ashlesha": "Ашлеша (Мистическая мудрость, проницательность, глубина)",
  "Magha": "Магха (Сила рода, царственное достоинство, авторитет)",
  "Purva Phalguni": "Пурва Пхалгуни (Наслаждение жизнью, романтика, отдых)",
  "Uttara Phalguni": "Уттара Пхалгуни (Благородство, служение, долговечные союзы)",
  "Hasta": "Хаста (Мастерство рук, исцеление, чистое намерение)",
  "Chitra": "Читра (Сверкающий алмаз, эстетика, созидание формы)",
  "Swati": "Свати (Свободный ветер, гибкость, независимость духа)",
  "Vishakha": "Вишакха (Целеустремленность, триумф, несгибаемый фокус)",
  "Anuradha": "Анурадха (Преданная дружба, гармония сердец, сотрудничество)",
  "Jyeshtha": "Джьештха (Защита слабых, мудрое первенство, внутренняя сила)",
  "Mula": "Мула (Корень вещей, разрушение иллюзий, поиск первопричины)",
  "Purva Ashadha": "Пурва Ашадха (Непобедимость, вдохновение, верность мечте)",
  "Uttara Ashadha": "Уттара Ашадха (Окончательная победа, высшая этика, покой)",
  "Shravana": "Шравана (Умение слышать тишину, сакральные знания, ученичество)",
  "Dhanishta": "Дханишта (Ритм изобилия, гармония музыки, процветание)",
  "Shatabhisha": "Шатабхиша (Исцеление сотней трав, медитация, таинство космоса)",
  "Purva Bhadrapada": "Пурва Бхадрапада (Мистический пыл, духовная аскеза, прорыв)",
  "Uttara Bhadrapada": "Уттара Бхадрапада (Глубокий мир в душе, мудрость глубин, благословение)",
  "Revati": "Ревати (Безусловная любовь, безопасный путь, духовный финал)"
};

// 5. ПЕРЕВОД КАТЕГОРИЙ ДНЕЙ КАЛЕНДАРЯ
const dayActivitiesRu = {
  "Planting": { ru: "Растения и дом", desc: "Прекрасный день для контакта с землей, ухода за цветами и гармонизации пространства." },
  "Nutrition": { ru: "Питание и тело", desc: "Благоприятно мягкое очищение рациона, употребление легкой свежей пищи и чистой воды." },
  "Beauty": { ru: "Красота и уход", desc: "Идеальное время для массажа, бережных спа-процедур и питания кожи." },
  "Traveling": { ru: "Путешествия и дорога", desc: "Дорога открывает новые горизонты и дарит встречи, меняющие восприятие." },
  "Completion": { ru: "Завершение дел", desc: "Пора подвести черту под старыми обязательствами и расчистить место для нового." },
  "Self-Care": { ru: "Забота о себе", desc: "День тихого ретрита, теплой ванны, медитации и восстановления сил." },
  "Career": { ru: "Карьера и цели", desc: "Профессиональный импульс набирает силу. Точные взвешенные шаги принесут плоды." },
  "Spirituality": { ru: "Духовные практики", desc: "Глубокая связь с внутренним проводником. Благоприятно время в тишине и молитве." },
  "Health": { ru: "Здоровье и ресурс", desc: "Слушайте сигналы тела. Легкие прогулки, сон и восстановление баланса." },
  "Romance": { ru: "Любовь и близость", desc: "Нежные слова и теплое внимание сближают глубже любых пышных жестов." },
  "Big Decisions": { ru: "Важные решения", desc: "Взвесьте все за и против в спокойствии. Не спешите с категоричными шагами." },
  "Social": { ru: "Общение и круг", desc: "Искренность и открытость создают надежные доверительные мосты с людьми." }
};

// ==========================================
// ГЕНЕРАЦИЯ astra_ru_data/tarot_ru.json
// ==========================================
try {
  let raw = fs.readFileSync(path.join(srcDir, 'cards_type_0_tarot.json'), 'utf8');
  if (raw.charCodeAt(0) === 0xFEFF) raw = raw.slice(1);
  const tarot = JSON.parse(raw).data || JSON.parse(raw);

  const ruTarot = tarot.map(c => {
    // Вычищаем префикс "The " для точного поиска
    const cleanKey = c.name.replace(/^The\s+/, '');
    const ruName = tarotRuNames[c.name] || tarotRuNames[cleanKey] || c.name;
    return {
      id: c.id,
      order: c.order,
      name_en: c.name,
      name_ru: ruName,
      direct: {
        short: c.normal?.descriptionShort || `Архетип ${ruName}: внутренняя мудрость и вектор развития`,
        description: c.normal?.description || '',
        advice: c.normal?.recommendations || 'Сохраняйте внутреннее спокойствие и доверяйте естественному ходу событий.'
      },
      reversed: {
        short: c.reversed?.descriptionShort || `Теневой аспект ${ruName}: время для бережного переосмысления`,
        description: c.reversed?.description || '',
        advice: c.reversed?.recommendations || 'Обратите внимание на скрытые сомнения и не форсируйте результат.'
      }
    };
  });

  fs.writeFileSync(path.join(targetDir, 'tarot_ru.json'), JSON.stringify(ruTarot, null, 2), 'utf8');
  console.log(`Generated tarot_ru.json with ${ruTarot.length} localized cards!`);
} catch(e) { console.error('Tarot RU error:', e.message); }

// ==========================================
// ГЕНЕРАЦИЯ astra_ru_data/runes_ru.json
// ==========================================
try {
  let raw = fs.readFileSync(path.join(srcDir, 'cards_type_1_runes.json'), 'utf8');
  if (raw.charCodeAt(0) === 0xFEFF) raw = raw.slice(1);
  const runes = JSON.parse(raw).data || JSON.parse(raw);

  const ruRunes = runes.map(r => {
    const meta = runeRuNames[r.name] || { ru: r.name, meaning: 'Сакральный символ' };
    return {
      id: r.id,
      order: r.order,
      name_en: r.name,
      name_ru: meta.ru,
      meaning: meta.meaning,
      direct: {
        short: r.normal?.descriptionShort || meta.meaning,
        description: r.normal?.description || '',
        advice: r.normal?.recommendations || 'Действуйте в согласии со своими истинными ценностями.'
      },
      reversed: {
        short: r.reversed?.descriptionShort || 'Предостережение и необходимость осознанности',
        description: r.reversed?.description || '',
        advice: r.reversed?.recommendations || 'Сделайте шаг назад и восстановите внутреннее равновесие.'
      }
    };
  });

  fs.writeFileSync(path.join(targetDir, 'runes_ru.json'), JSON.stringify(ruRunes, null, 2), 'utf8');
  console.log(`Generated runes_ru.json with ${ruRunes.length} localized runes!`);
} catch(e) { console.error('Runes RU error:', e.message); }

// ==========================================
// ГЕНЕРАЦИЯ astra_ru_data/calendar_meta_ru.json
// ==========================================
const calendarMeta = {
  planets: planetRu,
  nakshatras: nakshatraRu,
  activities: dayActivitiesRu
};
fs.writeFileSync(path.join(targetDir, 'calendar_meta_ru.json'), JSON.stringify(calendarMeta, null, 2), 'utf8');
console.log('Generated calendar_meta_ru.json with Jyotish Nakshatras & Planet rules!');
