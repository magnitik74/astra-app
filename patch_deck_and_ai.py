# -*- coding: utf-8 -*-
TARGET_FILE = r"D:\projects\monly\АСТРА_АССЕТЫ\astra_main_app.html"

with open(TARGET_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# Update initTarotArcDeck
old_init = """    function initTarotArcDeck() {
      const viewport = document.getElementById('tarot-arc-viewport');
      if (!viewport) return;
      viewport.innerHTML = '';
      tarotDeckCards = [];

      const NUM_CARDS = 24;
      for (let i = 0; i < NUM_CARDS; i++) {
        const cardData = TAROT_CARDS[i % TAROT_CARDS.length];
        const cardEl = document.createElement('div');
        cardEl.className = 'spread-arc-card';
        cardEl.dataset.index = i;
        cardEl.innerHTML = `<img src="moonly_3d_icons/ic_tarot_card_back_v3.png" alt="Back">`;

        cardEl.addEventListener('click', (e) => {
          if (Math.abs(tarotVelocity) > 0.4 || tarotIsDragging) return;
          e.stopPropagation();
          drawCardFromArc(i, cardData, cardEl);
        });

        viewport.appendChild(cardEl);
        tarotDeckCards.push({ el: cardEl, data: cardData, index: i });
      }

      renderTarotArcCards();
      setupArcDragEvents();
    }"""

new_init = """    function initTarotArcDeck() {
      const viewport = document.getElementById('tarot-arc-viewport');
      if (!viewport) return;
      viewport.innerHTML = '';
      tarotDeckCards = [];

      const majors = TAROT_CARDS.filter(c => c.suit === 'major');
      const deckList = majors.length >= 22 ? majors : TAROT_CARDS.slice(0, 22);

      deckList.forEach((cardData, i) => {
        const cardEl = document.createElement('div');
        cardEl.className = 'spread-arc-card';
        cardEl.dataset.index = i;
        cardEl.innerHTML = `<img src="moonly_3d_icons/ic_tarot_card_back_v3.png" alt="Back">`;

        cardEl.addEventListener('click', (e) => {
          if (Math.abs(tarotVelocity) > 0.4 || tarotIsDragging) return;
          e.stopPropagation();
          drawCardFromArc(i, cardData, cardEl);
        });

        viewport.appendChild(cardEl);
        tarotDeckCards.push({ el: cardEl, data: cardData, index: i });
      });

      renderTarotArcCards();
      setupArcDragEvents();
    }"""

if old_init in content:
    content = content.replace(old_init, new_init)
    print("✓ Updated initTarotArcDeck to 22 Major Arcana cards.")
else:
    print("WARN: old_init not found")

# Update getAstrologicalAIResponse
old_ai = """    function getAstrologicalAIResponse(q) {
      const query = q.toLowerCase();
      if (query.includes('тельце') || query.includes('луна')) {
        return 'Луна в знаке Тельца усиливает земную устойчивость и интуицию тела. Это благоприятное время для заботы о комфорте, завершения начатых задач и заземления эмоций.';
      } else if (query.includes('финанс') || query.includes('деньг') || query.includes('работ')) {
        return 'В финансовой сфере сейчас работает закон терпения и основательности. Избегайте импульсивных трат: надежные семена, посаженные сейчас, дадут богатый урожай.';
      } else if (query.includes('вечер') || query.includes('сил') || query.includes('ритуал')) {
        return 'Для вечернего ритуала зажгите свечу, включите частоту 432 Гц и примите теплую ванну с морской солью. Позвольте дню раствориться в мягком лунном покое.';
      } else {
        return 'Звёзды слышат чистоту вашего намерения. Сейчас формируется энергетический фундамент для следующего лунного цикла — сохраняйте душевный покой и верьте в свой путь.';
      }
    }"""

new_ai = """    function getAstrologicalAIResponse(q) {
      const query = q.toLowerCase();
      if (query.includes('триптих') || (query.includes('ситуация') && query.includes('совет')) || (query.includes('расклад') && query.includes('таро'))) {
        return 'Твой триптих раскрывает редкую гармонию: энергия первого аркана закладывает фундамент осознанности, второй предупреждает о скрытых вызовах ума, а третий дает высший вектор — действовать мягко и доверять интуиции. Сегодня космические врата открыты для созидания.';
      } else if (query.includes('аркан') || query.includes('таро')) {
        return 'Этот аркан сейчас активно вибрирует в твоем поле. Он советует удерживать равновесие между разумом и сердцем. Прислушивайся к тонким знакам — сегодня случайности не случайны.';
      } else if (query.includes('тельце') || query.includes('луна')) {
        return 'Луна в знаке Тельца усиливает земную устойчивость и интуицию тела. Это благоприятное время для заботы о комфорте, завершения начатых задач и заземления эмоций.';
      } else if (query.includes('финанс') || query.includes('деньг') || query.includes('работ')) {
        return 'В финансовой сфере сейчас работает закон терпения и основательности. Избегайте импульсивных трат: надежные семена, посаженные сейчас, дадут богатый урожай.';
      } else if (query.includes('вечер') || query.includes('сил') || query.includes('ритуал')) {
        return 'Для вечернего ритуала зажгите свечу, включите частоту 432 Гц и примите теплую ванну с морской солью. Позвольте дню раствориться в мягком лунном покое.';
      } else {
        return 'Звёзды слышат чистоту вашего намерения. Сейчас формируется энергетический фундамент для следующего лунного цикла — сохраняйте душевный покой и верьте в свой путь.';
      }
    }"""

if old_ai in content:
    content = content.replace(old_ai, new_ai)
    print("✓ Updated getAstrologicalAIResponse for rich Tarot and Triad insights.")
else:
    print("WARN: old_ai not found")

with open(TARGET_FILE, "w", encoding="utf-8") as f:
    f.write(content)

print("Finished updates.")
