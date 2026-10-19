import re

filepath = r"D:\projects\monly\АСТРА_АССЕТЫ\astra_main_app.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the Tarot Spread Section HTML to match Moonly 1:1
old_tarot_spread = """          <!-- ВИД А: РАСКЛАД ДНЯ (fragment_practice_spread_one_card.xml) -->
          <div id="tarot-view-spread" class="spread-one-card-container">
            <div class="spread-title">Карта дня • Джйотиш</div>
            <div class="spread-subtitle">Сформулируйте в мыслях сокровенный вопрос и коснитесь колоды внизу</div>

            <!-- Слот для карты -->
            <div class="spread-slot-wrapper">
              <div class="spread-slot-frame" id="spread-slot-frame"></div>
              <div class="spread-slot-card" id="slot-card-flipper" onclick="flipActiveCard()">
                <div class="card-face back">
                  <img src="moonly_3d_icons/ic_tarot_card_back_v3.png" alt="Back">
                </div>
                <div class="card-face front">
                  <img id="slot-card-front-img" src="01_ТАРО_КАРТЫ/03_The_Popess_(The_High_Priestess).png" alt="Tarot Front">
                </div>
              </div>
            </div>

            <!-- Подсказка -->
            <div class="spread-prompt-wrap" id="spread-prompt">
              <img class="spread-prompt-arrow" src="moonly_3d_icons/ic_taros_arrow.png" alt="Arrow">
              <span class="spread-prompt-text">Вытяните карту из колоды</span>
            </div>

            <!-- Результат вытягивания карты -->
            <div class="spread-result-details" id="spread-result">
              <span class="spread-card-name" id="res-card-name">03. Верховная Жрица</span>
              <span class="spread-card-archetype" id="res-card-archetype">Интуиция • Тайные знания • Подсознание</span>
              <div class="spread-card-reading" id="res-card-reading">
                Сегодня твой внутренний компас точнее любых логических расчетов. Прислушайся к тихому голосу души и вещим снам — ответы уже созрели внутри тебя.
              </div>
              <div class="spread-actions-row">
                <div class="spread-reset-btn" onclick="resetTarotSpread()" title="Перемешать колоду">
                  <img src="moonly_3d_icons/ic_taros_reset.png" alt="Reset">
                </div>
                <button class="spread-full-reading-btn" onclick="openActiveCardModal()">Читать полное толкование</button>
              </div>
            </div>

            <!-- Интерактивный веер карт колоды по радиусу (Moonly 1:1 Drag, Spin & Draw) -->
            <div class="spread-deck-arc-container" id="tarot-arc-container">
              <div class="spread-deck-arc-viewport" id="tarot-arc-viewport">
                <!-- 24 аркана генерируются динамически по математической круговой дуге -->
              </div>
            </div>
          </div>"""

new_tarot_spread = """          <!-- ВИД А: РАСКЛАД ДНЯ (Moonly 1:1 Three-card Spread & Radial Fan Arc) -->
          <div id="tarot-view-spread" class="spread-one-card-container">
            <!-- Верхняя панель инструментов расклада -->
            <div class="tarot-toolbar-row">
              <div class="tarot-round-tool-btn" onclick="alert('История прошлых раскладов Таро сохранена в профиле')">🕒</div>
              <div class="tarot-layout-selector-pill">
                <div class="tarot-layout-btn" onclick="setTarotLayout(1, this)">▯</div>
                <div class="tarot-layout-btn active" onclick="setTarotLayout(3, this)">🗂</div>
                <div class="tarot-layout-btn" onclick="setTarotLayout('fan', this)">🎴</div>
                <div class="tarot-layout-btn" onclick="toggleTarotView('all')">☰</div>
              </div>
              <div class="tarot-round-tool-btn" onclick="alert('Расклад Таро на 3 карты:\\n1. Прошлое / Текущая ситуация\\n2. Препятствие / Урок\\n3. Исход и совет Аркана')">ℹ</div>
            </div>

            <div style="font-size: 16px; font-weight: 700; color: #FFF; text-align: center; margin-top: 14px;" id="tarot-step-title">Текущая ситуация</div>

            <!-- 3 слота расклада -->
            <div class="tarot-three-slots-row">
              <div class="tarot-slot-box active" id="tarot-slot-0" onclick="selectTarotSlot(0)">
                <img id="slot-img-0" src="moonly_3d_icons/ic_tarot_spread_slot_active.png" style="opacity: 0.15;" alt="Slot 1">
              </div>
              <div class="tarot-slot-box" id="tarot-slot-1" onclick="selectTarotSlot(1)">
                <img id="slot-img-1" src="moonly_3d_icons/ic_tarot_card_back_v3.png" style="opacity: 0.1;" alt="Slot 2">
              </div>
              <div class="tarot-slot-box" id="tarot-slot-2" onclick="selectTarotSlot(2)">
                <img id="slot-img-2" src="moonly_3d_icons/ic_tarot_card_back_v3.png" style="opacity: 0.1;" alt="Slot 3">
              </div>
            </div>

            <!-- Индикатор вытягивания -->
            <div class="tarot-slot-arrow-indicator" id="tarot-prompt-indicator">
              <span style="font-size: 11px;">▲</span>
              <span>Вытянуть карты</span>
            </div>

            <!-- Детали вытянутой карты -->
            <div class="spread-result-details" id="spread-result" style="display: none; margin-top: 10px;">
              <span class="spread-card-name" id="res-card-name">03. Верховная Жрица</span>
              <span class="spread-card-archetype" id="res-card-archetype">Интуиция • Тайные знания • Подсознание</span>
              <div class="spread-card-reading" id="res-card-reading">
                Сегодня твой внутренний компас точнее любых логических расчетов. Прислушайся к тихому голосу души.
              </div>
              <div class="spread-actions-row">
                <div class="spread-reset-btn" onclick="resetTarotSpread()" title="Перемешать колоду">
                  <img src="moonly_3d_icons/ic_taros_reset.png" alt="Reset">
                </div>
                <button class="spread-full-reading-btn" onclick="openActiveCardModal()">Читать полное толкование</button>
              </div>
            </div>

            <!-- Интерактивный радиальный веер карт колоды (круговая дуга с инерцией) -->
            <div class="spread-deck-arc-container" id="tarot-arc-container">
              <div class="spread-deck-arc-viewport" id="tarot-arc-viewport">
                <!-- 24 аркана генерируются динамически по математической дуге -->
              </div>
            </div>
          </div>"""

if old_tarot_spread in content:
    content = content.replace(old_tarot_spread, new_tarot_spread)

# 2. Update JavaScript:
# We need:
# - Continuous timeline from Oct 1 2026 to Mar 31 2027
# - Rotating badge interval
# - Surya player, Karma modal, Meditation player
# - Interactive Tarot Arc Deck with inertia & drawing into slots
# - Paywall modal for days >= Oct 19

new_js_code = """
    /* ========================================================
       11. ДИНАМИЧЕСКИЙ КАЛЕНДАРЬ (МУЛЬТИМЕСЯЧНАЯ ЛЕНТА & PAYWALL)
       ======================================================== */
    let currentSelectedDay = 18; // 18 октября 2026 (День из видеозаписи пользователя)
    let currentSelectedDateKey = "2026-10-18";
    let activeSlotIndex = 0;
    let drawnSlots = [null, null, null];

    // Месяцы и дни (182 непрерывных дня: Октябрь 2026 - Март 2027)
    const MONTH_DATA = [
      { year: 2026, month: 10, name: "ОКТ", days: 31, startWeekday: 3 }, // 1 окт 2026 - Четверг (3)
      { year: 2026, month: 11, name: "НОЯ", days: 30, startWeekday: 6 },
      { year: 2026, month: 12, name: "ДЕК", days: 31, startWeekday: 1 },
      { year: 2027, month: 1,  name: "ЯНВ", days: 31, startWeekday: 4 },
      { year: 2027, month: 2,  name: "ФЕВ", days: 28, startWeekday: 0 },
      { year: 2027, month: 3,  name: "МАР", days: 31, startWeekday: 0 }
    ];

    const ALL_DAYS_TIMELINE = [];
    MONTH_DATA.forEach(m => {
      for (let d = 1; d <= m.days; d++) {
        const dateKey = `${m.year}-${String(m.month).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
        const weekdayIndex = (m.startWeekday + d - 1) % 7;
        const weekdays = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС'];
        const isPro = (m.year > 2026 || m.month > 10 || (m.month === 10 && d >= 19));
        
        // Лунный день (цикл 1-30)
        let moonDay = ((d + 10) % 30) + 1;
        if (m.month === 10 && d === 18) moonDay = 8; // 8-й лунный день на видео
        
        ALL_DAYS_TIMELINE.push({
          dateKey,
          day: d,
          month: m.month,
          monthName: m.name,
          year: m.year,
          weekday: weekdays[weekdayIndex],
          moonDay: moonDay,
          isPro: isPro,
          isToday: (m.month === 10 && d === 18)
        });
      }
    });

    function initCalendarDays() {
      const track = document.getElementById('calendar-days-track');
      if (!track) return;
      track.innerHTML = '';

      ALL_DAYS_TIMELINE.forEach((item, index) => {
        const el = document.createElement('div');
        const isSelected = (item.dateKey === currentSelectedDateKey);

        el.className = `day-scroll-item ${isSelected ? 'selected' : ''} ${item.isToday ? 'is-today' : ''} ${item.isPro ? 'is-pro' : ''}`;
        el.dataset.dateKey = item.dateKey;
        el.dataset.monthName = item.monthName;

        el.innerHTML = `
          <span class="day-scroll-weekday" style="${item.isToday ? 'color:#F7B64D;font-weight:700;' : ''}">${item.weekday}</span>
          <img class="day-scroll-moon" src="moonly_3d_icons/moon_${item.moonDay}.png" alt="Moon ${item.moonDay}">
          <span class="day-scroll-num">${item.day}</span>
        `;

        el.addEventListener('click', () => {
          if (track._hasDragged) return;
          if (item.isPro) {
            openAstraPlusModal(item);
          } else {
            selectCalendarDay(item, el);
          }
        });

        track.appendChild(el);
      });

      enableDragToScroll(track);

      // Скролл-слушатель для динамической смены кнопки месяца (ОКТ / НОЯ / ДЕК / ЯНВ)
      track.addEventListener('scroll', () => {
        updateActiveMonthLabel(track);
      }, { passive: true });

      // Центрируем день 18 при загрузке
      setTimeout(() => {
        const sel = track.querySelector(`.day-scroll-item[data-date-key="${currentSelectedDateKey}"]`);
        if (sel) {
          const scrollPos = sel.offsetLeft - (track.clientWidth / 2) + (sel.clientWidth / 2);
          track.scrollTo({ left: Math.max(0, scrollPos), behavior: 'smooth' });
        }
      }, 100);
    }

    function updateActiveMonthLabel(track) {
      const center = track.scrollLeft + (track.clientWidth / 2);
      const items = track.querySelectorAll('.day-scroll-item');
      let currentItem = null;
      let minDistance = 99999;

      items.forEach(it => {
        const itCenter = it.offsetLeft + (it.clientWidth / 2);
        const dist = Math.abs(itCenter - center);
        if (dist < minDistance) {
          minDistance = dist;
          currentItem = it;
        }
      });

      if (currentItem && currentItem.dataset.monthName) {
        const lbl = document.getElementById('calendar-month-label');
        if (lbl && lbl.innerText !== currentItem.dataset.monthName) {
          lbl.innerText = currentItem.dataset.monthName;
        }
      }
    }

    function selectCalendarDay(item, element) {
      currentSelectedDateKey = item.dateKey;
      currentSelectedDay = item.day;

      document.querySelectorAll('.day-scroll-item').forEach(el => {
        if (el.dataset.dateKey === item.dateKey) {
          el.classList.add('selected');
        } else {
          el.classList.remove('selected');
        }
      });

      // Обновляем Карточку 1 (Гороскоп дня и фокус)
      const bgImg = document.getElementById('calendar-bg-img');
      const focusEl = document.getElementById('calendar-day-focus');
      
      if (item.dateKey === "2026-10-18") {
        if (bgImg) bgImg.src = "09_ФОНЫ_ЛУННОГО_КАЛЕНДАРЯ/cat_bathrobe_coffee_day18.jpg";
        if (focusEl) focusEl.innerText = "Устанавливайте границы с людьми, которые забирают больше энергии, чем дают";
      } else {
        const bgNum = ((item.day * 3) % 35) + 1;
        if (bgImg) bgImg.src = `09_ФОНЫ_ЛУННОГО_КАЛЕНДАРЯ/${bgNum}_EVENT.jpg`;
        if (focusEl) focusEl.innerText = `Энергия лунного дня ${item.moonDay} направляет намерения — замыслы кристаллизуются, обретая устойчивую форму.`;
      }

      // Обновляем Карточку 2 (Лунный день)
      const moonCorner = document.getElementById('calendar-moon-corner');
      if (moonCorner) moonCorner.src = `moonly_3d_icons/moon_${item.moonDay}.png`;

      let phaseName = "Растущая Луна";
      if (item.moonDay === 1 || item.moonDay === 30) phaseName = "Новолуние";
      else if (item.moonDay < 15) phaseName = "Растущая Луна";
      else if (item.moonDay === 15) phaseName = "Полнолуние";
      else phaseName = "Убывающая Луна";

      const lunarTitle = document.getElementById('calendar-lunar-phase-title');
      if (lunarTitle) {
        lunarTitle.innerText = `${item.moonDay}-й лунный день • ${phaseName}`;
      }
    }

    /* Ротация микро-бейджа Карточки 1 (Садоводство <-> Красота) */
    let currentBadgeMode = 0;
    function initRotatingBadge() {
      setInterval(() => {
        currentBadgeMode = (currentBadgeMode === 0) ? 1 : 0;
        const icon = document.getElementById('card-badge-icon');
        const tag = document.getElementById('card-badge-tag');
        const title = document.getElementById('card-badge-title');
        if (!icon || !tag || !title) return;

        if (currentBadgeMode === 0) {
          icon.src = "moonly_3d_icons/ic_new_planting.png";
          tag.innerText = "ПОРА САЖАТЬ!";
          title.innerHTML = `Садоводство <span style="color:#34C759;font-size:11px;">▲</span>`;
        } else {
          icon.src = "moonly_3d_icons/ic_new_beauty.png";
          tag.innerText = "БЛИСТАЙТЕ";
          title.innerHTML = `Красота <span style="font-size:11px;">🔒</span>`;
        }
      }, 4000);
    }

    function toggleDayBadgeDetail() {
      if (currentBadgeMode === 0) {
        alert("Садоводство: Сегодня идеальное время для посева семян и пересадки комнатных растений.");
      } else {
        openAstraPlusModal({ day: currentSelectedDay });
      }
    }

    /* Модальное окно Astra Plus / Paywall Sheet */
    function openAstraPlusModal(dayObj) {
      const content = `
        <div class="paywall-modal-container">
          <div class="paywall-crown-badge">
            <span class="paywall-crown-icon">👑</span>
          </div>
          <div class="paywall-title">Откройте все дни с Astra Plus</div>
          <div class="paywall-subtitle">
            Прогноз на ${dayObj.day ? dayObj.day + ' число' : 'будущие дни'}, накшатры, персональные транзиты и полный доступ ко всем раскладам Таро
          </div>

          <div class="paywall-features-list">
            <div class="paywall-feature-item">
              <div class="paywall-feature-icon">✨</div>
              <div class="paywall-feature-text">Доступ ко всем месяцам года: Ноябрь, Декабрь 2026, 2027</div>
            </div>
            <div class="paywall-feature-item">
              <div class="paywall-feature-icon">🤍</div>
              <div class="paywall-feature-text">3 сферы гороскопа: Романтика, Важные решения, Социум</div>
            </div>
            <div class="paywall-feature-item">
              <div class="paywall-feature-icon">🪐</div>
              <div class="paywall-feature-text">Формулы Джйотиш и точность расчета координат уровня NASA</div>
            </div>
          </div>

          <div class="paywall-plans-row">
            <div class="paywall-plan-card" onclick="selectPaywallPlan(this, 'month')">
              <div class="paywall-plan-name">1 Месяц</div>
              <div class="paywall-plan-price">499 ₽</div>
              <div class="paywall-plan-period">в месяц</div>
            </div>
            <div class="paywall-plan-card selected" onclick="selectPaywallPlan(this, 'year')">
              <div class="paywall-badge-best">ВЫГОДА 60%</div>
              <div class="paywall-plan-name">1 Год</div>
              <div class="paywall-plan-price">199 ₽</div>
              <div class="paywall-plan-period">в месяц (2 390 ₽/год)</div>
            </div>
          </div>

          <button class="paywall-submit-btn" onclick="confirmSubscription()">Попробовать 7 дней бесплатно</button>
        </div>
      `;
      showUniversalModal(content);
    }

    function selectPaywallPlan(card, type) {
      document.querySelectorAll('.paywall-plan-card').forEach(c => c.classList.remove('selected'));
      card.classList.add('selected');
    }

    function confirmSubscription() {
      alert("✨ Поздравляем! Подписка Astra Plus активирована на 7 дней бесплатно.");
      closeUniversalModal();
    }

    /* Модальное окно Гороскопа дня со Сферами (Видео 00:19 - 00:26) */
    function openDayDetailModal() {
      const content = `
        <div style="text-align: center; padding-bottom: 20px;">
          <h2 style="font-size: 20px; font-weight: 800; color: #FFF;">Ежедневный гороскоп</h2>
          <div style="font-size: 11px; font-weight: 700; color: #8E8E98; text-transform: uppercase; margin-top: 4px;">ПО ВАШЕЙ НАТАЛЬНОЙ КАРТЕ • ОКТ. 18</div>

          <div style="background: rgba(255,255,255,0.04); border-radius: 20px; padding: 16px; margin-top: 18px; text-align: left;">
            <div style="font-size: 10px; font-weight: 700; color: #A0A5B5; text-transform: uppercase;">ФОКУС ДНЯ</div>
            <div style="font-size: 17px; font-weight: 700; color: #FFF; line-height: 1.4; margin-top: 6px;">
              Устанавливайте границы с людьми, которые забирают больше энергии, чем дают.
            </div>
            <div style="font-size: 13px; line-height: 1.5; color: #C5C5D2; margin-top: 10px;">
              Ваш день наполнен позитивной энергией и возможностями для созидательного общения, однако некоторые контакты потребуют осознанной дистанции.
            </div>
          </div>

          <!-- Сферы жизни с глиняными 3D-иконками -->
          <div style="margin-top: 16px; display: flex; flex-direction: column; gap: 10px; text-align: left;">
            <div style="display: flex; align-items: center; justify-content: space-between; background: rgba(255,255,255,0.05); padding: 14px 16px; border-radius: 18px;">
              <span style="font-size: 15px; font-weight: 700; color: #FFF;">Романтика 🔒</span>
              <img src="moonly_3d_icons/ic_new_romance.png" style="width: 28px; height: 28px; object-fit: contain;">
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between; background: rgba(255,255,255,0.05); padding: 14px 16px; border-radius: 18px;">
              <span style="font-size: 15px; font-weight: 700; color: #FFF;">Важные решения 🔒</span>
              <img src="moonly_3d_icons/ic_new_decisions.png" style="width: 28px; height: 28px; object-fit: contain;">
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between; background: rgba(255,255,255,0.05); padding: 14px 16px; border-radius: 18px;">
              <span style="font-size: 15px; font-weight: 700; color: #FFF;">Социум 🔒</span>
              <img src="moonly_3d_icons/ic_new_social.png" style="width: 28px; height: 28px; object-fit: contain;">
            </div>
          </div>

          <!-- Блоки доверия: Джйотиш и NASA -->
          <div style="background: rgba(255,255,255,0.03); border-radius: 20px; padding: 16px; margin-top: 16px; text-align: left;">
            <div style="display: flex; gap: 12px; align-items: flex-start;">
              <div style="font-size: 20px;">🕉</div>
              <div>
                <div style="font-size: 13px; font-weight: 700; color: #FFF;">Формулы Джйотиш</div>
                <div style="font-size: 11px; color: #9E9EA8; margin-top: 2px;">Этот прогноз составлен по аутентичным ведическим формулам: реальные градусы, реальные Накшатры.</div>
              </div>
            </div>
            <div style="display: flex; gap: 12px; align-items: flex-start; margin-top: 14px;">
              <div style="font-size: 20px;">🪐</div>
              <div>
                <div style="font-size: 13px; font-weight: 700; color: #FFF;">Точность уровня NASA</div>
                <div style="font-size: 11px; color: #9E9EA8; margin-top: 2px;">Наши расчёты астрономических положений планет соответствуют эфемеридам JPL NASA.</div>
              </div>
            </div>
          </div>

          <button onclick="openAstraPlusModal({day: 18})" style="width: 100%; height: 48px; border-radius: 24px; background: #FFF; color: #000; font-weight: 700; font-size: 14px; margin-top: 20px; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px;">
            <span>🔒</span> Открыть Сферы
          </button>
        </div>
      `;
      showUniversalModal(content);
    }

    /* Модальное окно Кармы (Видео 00:54 - 01:06) */
    function openKarmaModal() {
      const content = `
        <div style="text-align: left; padding: 10px 4px 24px;">
          <div style="font-size: 11px; font-weight: 700; color: #8E8E98; text-transform: uppercase;">КАРМА</div>
          <h2 style="font-size: 24px; font-weight: 800; color: #FFF; margin-top: 4px;">Карма</h2>
          
          <div style="font-size: 16px; line-height: 1.45; font-weight: 600; color: #E5E5EB; margin-top: 16px;">
            Перемены начинаются, когда вы ставите себя на первое место. Пора прислушаться к своим желаниям.
          </div>

          <div style="margin-top: 24px; display: flex; flex-direction: column; gap: 18px;">
            <div style="display: flex; gap: 12px;">
              <span style="font-size: 16px; font-weight: 800; color: #F7B64D;">1.</span>
              <div style="font-size: 14px; line-height: 1.45; color: #DDD;">Продолжите фразу «Я готов...» — придумайте как можно больше вариантов.</div>
            </div>
            <div style="display: flex; gap: 12px;">
              <span style="font-size: 16px; font-weight: 800; color: #F7B64D;">2.</span>
              <div style="font-size: 14px; line-height: 1.45; color: #DDD;">Запишите одно чувство, которое вам хочется испытывать чаще в этом месяце.</div>
            </div>
            <div style="display: flex; gap: 12px;">
              <span style="font-size: 16px; font-weight: 800; color: #F7B64D;">3.</span>
              <div style="font-size: 14px; line-height: 1.45; color: #DDD;">Сегодня перед каждым выбором спрашивайте себя: это приближает меня к тому, кем я хочу быть?</div>
            </div>
          </div>

          <button onclick="closeUniversalModal()" style="width: 100%; height: 48px; border-radius: 24px; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); color: #FFF; font-weight: 700; margin-top: 28px; cursor: pointer;">Завершить практику</button>
        </div>
      `;
      showUniversalModal(content);
    }

    /* Модальное окно Медитации с 3D-торосом (Видео 01:07 - 01:17) */
    function openMeditationPlayerModal() {
      const content = `
        <div style="text-align: center; padding: 10px 4px 20px;">
          <div style="font-size: 16px; font-weight: 800; color: #FFF;">Вход в медитации</div>
          <div style="font-size: 11px; font-weight: 700; color: #8E8E98; text-transform: uppercase; margin-top: 2px;">РАССЛАБЛЕНИЕ • 15 МИН</div>

          <!-- 3D Глиняный пульсирующий цветок -->
          <div style="margin: 28px auto 20px; width: 170px; height: 170px; border-radius: 50%; background: radial-gradient(circle, rgba(235,170,185,0.25) 0%, rgba(138,99,255,0.15) 50%, transparent 70%); display: flex; align-items: center; justify-content: center; animation: breathPulse 6s infinite ease-in-out;">
            <img src="09_ФОНЫ_ЛУННОГО_КАЛЕНДАРЯ/15_EVENT.jpg" style="width: 120px; height: 120px; border-radius: 50%; object-fit: cover; box-shadow: 0 10px 30px rgba(0,0,0,0.6);">
          </div>

          <!-- Кнопки управления аудио -->
          <div style="display: flex; align-items: center; justify-content: center; gap: 26px; margin-top: 16px;">
            <div style="width: 42px; height: 42px; border-radius: 50%; background: rgba(255,255,255,0.08); display: flex; align-items: center; justify-content: center; color: #FFF; cursor: pointer; font-size: 13px;">↺ 10</div>
            <div id="meditation-play-toggle" onclick="toggleTone()" style="width: 62px; height: 62px; border-radius: 50%; background: #FFF; color: #000; display: flex; align-items: center; justify-content: center; font-size: 22px; cursor: pointer; box-shadow: 0 6px 20px rgba(255,255,255,0.3);">▶</div>
            <div style="width: 42px; height: 42px; border-radius: 50%; background: rgba(255,255,255,0.08); display: flex; align-items: center; justify-content: center; color: #FFF; cursor: pointer; font-size: 13px;">10 ↻</div>
          </div>

          <!-- Таймлайн прогресса -->
          <div style="margin-top: 24px; padding: 0 10px;">
            <div style="width: 100%; height: 4px; background: rgba(255,255,255,0.15); border-radius: 2px; position: relative;">
              <div style="width: 25%; height: 100%; background: #F7B64D; border-radius: 2px;"></div>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 11px; color: #8E8E98; margin-top: 6px;">
              <span>03:45</span>
              <span>15:00</span>
            </div>
          </div>

          <p style="font-size: 12px; color: #A0A5B5; line-height: 1.4; margin-top: 18px; text-align: left;">
            Введение в практику медитаций: мы учимся входить в глубокий контакт с телом, концентрироваться на дыхании и растворять ментальный шум.
          </p>
        </div>
      `;
      showUniversalModal(content);
    }

    function openSuryaPlayerModal() {
      openMeditationPlayerModal();
    }

    /* ========================================================
       12. ИНТЕРАКТИВНЫЙ ВЕЕР ТАРО НА ДУГЕ ОКРУЖНОСТИ (1:1 MOONLY)
       ======================================================== */
    let tarotDeckCards = [];
    let tarotDeckRotation = 0;
    let tarotIsDragging = false;
    let tarotStartX = 0;
    let tarotStartRotation = 0;
    let tarotVelocity = 0;
    let tarotAnimFrame = null;
    let tarotLastX = 0;
    let tarotLastTime = 0;

    function initTarotArcDeck() {
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
    }

    function renderTarotArcCards() {
      const R = 340;
      const stepAngle = 4.6;
      const N = tarotDeckCards.length;
      const containerW = 340;
      const centerX = containerW / 2;
      const centerY = 280;

      tarotDeckCards.forEach((c, i) => {
        const angleDeg = tarotDeckRotation + (i - (N - 1) / 2) * stepAngle;
        const angleRad = (angleDeg * Math.PI) / 180;

        const x = centerX + R * Math.sin(angleRad) - 31;
        const y = centerY - R * Math.cos(angleRad) - 49;

        const isVisible = (angleDeg > -75 && angleDeg < 75);
        if (!isVisible) {
          c.el.style.display = 'none';
          return;
        }

        c.el.style.display = 'block';
        c.el.style.left = `${x}px`;
        c.el.style.top = `${y}px`;
        c.el.style.transform = `rotate(${angleDeg}deg)`;
        c.el.style.zIndex = Math.round(50 - Math.abs(angleDeg));

        const distFromCenter = Math.abs(angleDeg);
        if (distFromCenter > 42) {
          c.el.style.opacity = Math.max(0.15, 1 - (distFromCenter - 42) / 30);
        } else {
          c.el.style.opacity = '1';
        }
      });
    }

    function setupArcDragEvents() {
      const container = document.getElementById('tarot-arc-container');
      if (!container) return;

      const onStart = (clientX) => {
        tarotIsDragging = true;
        tarotStartX = clientX;
        tarotStartRotation = tarotDeckRotation;
        tarotVelocity = 0;
        tarotLastX = clientX;
        tarotLastTime = performance.now();
        if (tarotAnimFrame) cancelAnimationFrame(tarotAnimFrame);
      };

      const onMove = (clientX) => {
        if (!tarotIsDragging) return;
        const dx = clientX - tarotStartX;
        tarotDeckRotation = tarotStartRotation + (dx * 0.22);

        const now = performance.now();
        const dt = now - tarotLastTime;
        if (dt > 10) {
          tarotVelocity = ((clientX - tarotLastX) / dt) * 3.8;
          tarotLastX = clientX;
          tarotLastTime = now;
        }

        clampArcRotation();
        renderTarotArcCards();
      };

      const onEnd = () => {
        if (!tarotIsDragging) return;
        tarotIsDragging = false;
        startArcInertia();
      };

      container.addEventListener('mousedown', (e) => onStart(e.clientX));
      window.addEventListener('mousemove', (e) => onMove(e.clientX));
      window.addEventListener('mouseup', onEnd);

      container.addEventListener('touchstart', (e) => {
        if (e.touches.length === 1) onStart(e.touches[0].clientX);
      }, { passive: true });

      window.addEventListener('touchmove', (e) => {
        if (tarotIsDragging && e.touches.length === 1) {
          onMove(e.touches[0].clientX);
        }
      }, { passive: true });

      window.addEventListener('touchend', onEnd);

      container.addEventListener('wheel', (e) => {
        if (Math.abs(e.deltaX) > 0 || Math.abs(e.deltaY) > 0) {
          const delta = Math.abs(e.deltaX) > Math.abs(e.deltaY) ? e.deltaX : e.deltaY;
          tarotDeckRotation -= delta * 0.12;
          clampArcRotation();
          renderTarotArcCards();
        }
      }, { passive: true });
    }

    function clampArcRotation() {
      const maxRot = 55;
      if (tarotDeckRotation > maxRot) tarotDeckRotation = maxRot;
      if (tarotDeckRotation < -maxRot) tarotDeckRotation = -maxRot;
    }

    function startArcInertia() {
      if (Math.abs(tarotVelocity) < 0.05) return;
      tarotDeckRotation += tarotVelocity;
      tarotVelocity *= 0.92;
      clampArcRotation();
      renderTarotArcCards();

      if (Math.abs(tarotVelocity) >= 0.05) {
        tarotAnimFrame = requestAnimationFrame(startArcInertia);
      }
    }

    function selectTarotSlot(idx) {
      activeSlotIndex = idx;
      document.querySelectorAll('.tarot-slot-box').forEach((s, i) => {
        if (i === idx) s.classList.add('active');
        else s.classList.remove('active');
      });
      const titles = ["Текущая ситуация", "Препятствие и Урок", "Совет Аркана"];
      const lbl = document.getElementById('tarot-step-title');
      if (lbl) lbl.innerText = titles[idx] || "Карта расклада";
    }

    function drawCardFromArc(index, cardData, cardEl) {
      currentDrawnCard = cardData;
      drawnSlots[activeSlotIndex] = cardData;

      const slotBox = document.getElementById(`tarot-slot-${activeSlotIndex}`);
      const slotImg = document.getElementById(`slot-img-${activeSlotIndex}`);
      if (slotImg) {
        slotImg.src = `01_ТАРО_КАРТЫ/${cardData.file}`;
        slotImg.style.opacity = '1';
        slotBox.style.border = '2px solid #F7B64D';
        slotBox.style.transform = 'scale(1.08)';
        setTimeout(() => slotBox.style.transform = 'scale(1)', 250);
      }

      // Показываем результат
      const res = document.getElementById('spread-result');
      const prompt = document.getElementById('tarot-prompt-indicator');
      if (prompt) prompt.style.display = 'none';

      document.getElementById('res-card-name').innerText = cardData.name;
      document.getElementById('res-card-archetype').innerText = cardData.arch;
      document.getElementById('res-card-reading').innerText = cardData.direct;
      if (res) res.style.display = 'flex';

      // Переключаем на следующий свободный слот
      if (activeSlotIndex < 2) {
        setTimeout(() => selectTarotSlot(activeSlotIndex + 1), 600);
      }
    }

    function resetTarotSpread() {
      drawnSlots = [null, null, null];
      for (let i = 0; i < 3; i++) {
        const slotImg = document.getElementById(`slot-img-${i}`);
        const slotBox = document.getElementById(`tarot-slot-${i}`);
        if (slotImg) {
          slotImg.src = (i === 0) ? "moonly_3d_icons/ic_tarot_spread_slot_active.png" : "moonly_3d_icons/ic_tarot_card_back_v3.png";
          slotImg.style.opacity = '0.15';
        }
        if (slotBox) slotBox.style.border = (i === 0) ? '2px dashed #F7B64D' : '1.5px dashed rgba(138, 99, 255, 0.35)';
      }
      selectTarotSlot(0);

      const res = document.getElementById('spread-result');
      const prompt = document.getElementById('tarot-prompt-indicator');
      if (res) res.style.display = 'none';
      if (prompt) prompt.style.display = 'flex';

      renderTarotArcCards();
    }
"""

# Replace the existing initCalendarDays and tarot functions
# Find from `function initCalendarDays()` down to `function openDayDetailModal()`
js_pattern = r'function initCalendarDays\(\)[\s\S]*?function openDayDetailModal\(\)[\s\S]*?showUniversalModal\(content\);\s*\}'
content = re.sub(js_pattern, new_js_code, content)

# Make sure initTarotArcDeck and initRotatingBadge are called in DOMContentLoaded
old_dom_loaded = """    window.addEventListener('DOMContentLoaded', () => {
      initCalendarDays();
      renderTarotGrid(TAROT_CARDS);
      renderRunesGrid();
      renderWisdomGrid();
    });"""

new_dom_loaded = """    window.addEventListener('DOMContentLoaded', () => {
      initCalendarDays();
      initRotatingBadge();
      initTarotArcDeck();
      renderTarotGrid(TAROT_CARDS);
      renderRunesGrid();
      renderWisdomGrid();
    });"""

content = content.replace(old_dom_loaded, new_dom_loaded)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Full application logic updated with video mechanics successfully!")
