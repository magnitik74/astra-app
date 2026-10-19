import re

filepath = r"D:\projects\monly\АСТРА_АССЕТЫ\astra_main_app.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's inspect where calendar-sticky-header ends
# We want to insert the Quick Actions row right after calendar-sticky-header
quick_actions_html = """
        <!-- Две быстрые кнопки: Натальная карта & Таро (Moonly 1:1) -->
        <div class="calendar-quick-actions-row">
          <div class="calendar-quick-pill" onclick="openBirthChartModal()">
            <img class="quick-pill-icon" src="moonly_3d_icons/ic_new_spirituality.png" alt="Natal">
            <div class="quick-pill-text">
              <span class="quick-pill-tag">ПОЗНАЙТЕ СЕБЯ</span>
              <span class="quick-pill-title">Натальная карта</span>
            </div>
          </div>
          <div class="calendar-quick-pill" onclick="switchTab('screen-practices')">
            <img class="quick-pill-icon" src="moonly_3d_icons/ic_tarot_card_back_v3.png" alt="Tarot">
            <div class="quick-pill-text">
              <span class="quick-pill-tag">РАСКЛАД</span>
              <span class="quick-pill-title">Таро</span>
            </div>
          </div>
        </div>
"""

if 'calendar-quick-actions-row' not in content:
    content = content.replace(
        '<span class="calendar-full-view-month" id="calendar-month-label">ОКТ</span>\n          </div>\n        </div></div>',
        '<span class="calendar-full-view-month" id="calendar-month-label">ОКТ</span>\n          </div>\n        </div></div>\n' + quick_actions_html
    )

# Let's update Card 1 to include the rotating micro-badge at bottom
# Find Card 1: calendar-card-for-you
old_card1_marker = """            <div class="calendar-event-bottom-row">
              <div class="calendar-event-status-block">
                <span class="calendar-event-status-tag">СФЕРА ДНЯ</span>
                <div class="calendar-event-status-val">
                  <span id="calendar-focus-sphere">Любовь и гармония</span>
                  <span style="color: #34C759; font-size: 13px; margin-left: 2px;">▲</span>
                </div>
              </div>
            </div>"""

new_card1_bottom = """            <div class="calendar-event-bottom-row" style="align-items: flex-end; justify-content: space-between;">
              <div class="card-micro-badge-wrap" id="card-rotating-badge-btn" onclick="event.stopPropagation(); toggleDayBadgeDetail();">
                <img class="badge-icon" id="card-badge-icon" src="moonly_3d_icons/ic_new_planting.png" alt="Planting">
                <div>
                  <div class="badge-tag" id="card-badge-tag">ПОРА САЖАТЬ!</div>
                  <div class="badge-title" id="card-badge-title">Садоводство <span id="card-badge-suffix" style="color: #34C759; font-size: 11px;">▲</span></div>
                </div>
              </div>
            </div>"""

if old_card1_marker in content:
    content = content.replace(old_card1_marker, new_card1_bottom)

# Let's replace Card 3 (transit card) and lifestyle grid with authentic Moonly Feed:
# 1. Card 3: Ваш недельный план практик (Сурья Намаскар, Карма, Вход в медитации)
# 2. Card 4: ГЛОБАЛЬНАЯ АСТРОЛОГИЯ (Этап для пересмотра)
# 3. Card 5: ГЛОБАЛЬНАЯ АСТРОЛОГИЯ (Проверка эго)
feed_replacement = """        <!-- Карточка 3: ПО ВАШЕЙ НАТАЛЬНОЙ КАРТЕ • Ваш недельный план практик (Moonly 1:1) -->
        <div class="calendar-practices-card">
          <div class="calendar-event-header" style="height: auto; margin-bottom: 8px;">
            <div class="calendar-event-header-left">
              <img class="calendar-event-header-icon" src="moonly_3d_icons/moonly_plus_icon_1.png" alt="Plan">
              <div>
                <div class="calendar-event-top-tag">ПО ВАШЕЙ НАТАЛЬНОЙ КАРТЕ</div>
                <div class="calendar-event-day-title">Ваш недельный план практик</div>
              </div>
            </div>
            <img class="calendar-event-arrow" src="moonly_3d_icons/ic_calendar_v2_arrow.png" alt="Arrow">
          </div>

          <h3 style="font-size: 18px; font-weight: 700; color: #FFF; margin-top: 14px;">Начните с себя</h3>
          <p style="font-size: 13px; line-height: 1.45; color: #A0A5B5; margin-top: 4px;">
            Значимые перемены в жизни начинаются с намерения. Прислушайтесь к себе — что вы хотите изменить?
          </p>

          <!-- 1. Сурья Намаскар -->
          <div class="practice-item-row" onclick="openSuryaPlayerModal()">
            <div class="practice-item-info">
              <span class="practice-item-tag">🎧 ПРАКТИКИ • УТРО</span>
              <span class="practice-item-title">Сурья Намаскар</span>
              <span class="practice-item-sub">Разбудите тело и наполнитесь солнечной энергией</span>
            </div>
            <div class="practice-item-thumb">
              <img src="09_ФОНЫ_ЛУННОГО_КАЛЕНДАРЯ/12_EVENT.jpg" alt="Surya">
              <div class="practice-play-badge">▶</div>
            </div>
          </div>

          <!-- 2. Карма (Чёткое намерение) -->
          <div class="practice-item-row" onclick="openKarmaModal()">
            <div class="practice-item-info">
              <span class="practice-item-tag">🪷 КАРМА • ВЕСЬ ДЕНЬ</span>
              <span class="practice-item-title">Чёткое намерение</span>
              <span class="practice-item-sub">Посейте зерно желанных перемен</span>
            </div>
            <div class="practice-item-thumb">
              <img src="moonly_3d_icons/ic_comp_karmic.png" style="width: 44px; height: 44px; object-fit: contain;" alt="Karma">
            </div>
          </div>

          <!-- 3. Вход в медитации -->
          <div class="practice-item-row" onclick="openMeditationPlayerModal()">
            <div class="practice-item-info">
              <span class="practice-item-tag">🎧 МЕДИТАЦИЯ • ВЕЧЕР</span>
              <span class="practice-item-title">Вход в медитации</span>
              <span class="practice-item-sub">Почувствуйте своё тело и верните внутреннее равновесие</span>
            </div>
            <div class="practice-item-thumb">
              <img src="09_ФОНЫ_ЛУННОГО_КАЛЕНДАРЯ/15_EVENT.jpg" alt="Meditation">
              <div class="practice-play-badge">▶</div>
            </div>
          </div>
        </div>

        <!-- Секция: ГЛОБАЛЬНАЯ АСТРОЛОГИЯ (Карточка 4: Этап для пересмотра) -->
        <div class="calendar-planetary-card" onclick="openTransitDetailModal()">
          <div class="calendar-event-header" style="height: auto;">
            <div class="calendar-event-header-left">
              <img class="calendar-event-header-icon" src="moonly_3d_icons/ic_new_spirituality.png" alt="Astrology">
              <div>
                <div class="calendar-event-top-tag">ГЛОБАЛЬНАЯ АСТРОЛОГИЯ</div>
                <div class="calendar-event-day-title">Влияние планет на вас</div>
              </div>
            </div>
            <img class="calendar-event-arrow" src="moonly_3d_icons/ic_calendar_v2_arrow.png" alt="Arrow">
          </div>

          <div style="font-size: 11px; font-weight: 700; color: #8E8E98; margin-top: 16px; text-transform: uppercase;">17 ОКТ.–5 НОЯБ.</div>
          <div style="font-size: 20px; font-weight: 800; color: #FFF; margin-top: 2px;">Этап для пересмотра</div>

          <div style="display: flex; gap: 24px; margin-top: 14px;">
            <div>
              <div style="font-size: 10px; font-weight: 700; color: #8E8E98; text-transform: uppercase;">СОЕДИНЕНИЕ</div>
              <div style="font-size: 14px; font-weight: 700; color: #FFF; margin-top: 2px;">Солнце, Меркурий, Венера</div>
            </div>
            <div>
              <div style="font-size: 10px; font-weight: 700; color: #8E8E98; text-transform: uppercase;">ЗНАК ЗОДИАКА</div>
              <div style="font-size: 14px; font-weight: 700; color: #FFF; margin-top: 2px;">Весы ♎</div>
            </div>
          </div>

          <!-- Дуга орбиты с планетами -->
          <div class="transit-orbit-visual">
            <div class="transit-orbit-arc-line"></div>
            <div class="transit-planets-group">
              <img class="transit-planet-sphere" src="moonly_3d_icons/transit_planet_sun.png" alt="Sun">
              <img class="transit-planet-sphere" src="moonly_3d_icons/transit_planet_mercury.png" alt="Mercury">
              <img class="transit-planet-sphere" src="moonly_3d_icons/transit_planet_venus.png" alt="Venus">
            </div>
            <span class="transit-days-left-tag">ОСТАЛОСЬ 19 ДН.</span>
          </div>
        </div>

        <!-- Карточка 5: Проверка эго -->
        <div class="calendar-planetary-card" onclick="openTransitDetailModal()">
          <div style="font-size: 11px; font-weight: 700; color: #8E8E98; text-transform: uppercase;">17 ОКТ.–16 НОЯБ.</div>
          <div style="font-size: 20px; font-weight: 800; color: #FFF; margin-top: 2px;">Проверка эго</div>

          <div style="display: flex; gap: 24px; margin-top: 14px;">
            <div>
              <div style="font-size: 10px; font-weight: 700; color: #8E8E98; text-transform: uppercase;">ПАДЕНИЕ</div>
              <div style="font-size: 14px; font-weight: 700; color: #FFF; margin-top: 2px;">Солнце</div>
            </div>
            <div>
              <div style="font-size: 10px; font-weight: 700; color: #8E8E98; text-transform: uppercase;">ЗНАК ЗОДИАКА</div>
              <div style="font-size: 14px; font-weight: 700; color: #FFF; margin-top: 2px;">Весы ♎</div>
            </div>
          </div>

          <div class="transit-orbit-visual">
            <div class="transit-orbit-arc-line"></div>
            <div class="transit-planets-group">
              <img class="transit-planet-sphere" src="moonly_3d_icons/transit_planet_sun.png" alt="Sun">
            </div>
            <span class="transit-days-left-tag">ОСТАЛОСЬ 29 ДН.</span>
          </div>
        </div>

        <!-- Баннер Дневника Снов (Dreamer) -->
        <div class="dreamer-quick-banner" onclick="openDreamerModal()">
          <img class="dreamer-quick-icon" src="moonly_3d_icons/ic_calendar_dreamer.png" alt="Dreamer">
          <div class="dreamer-quick-text">
            <span class="dreamer-quick-sub">ДНЕВНИК СНОВ</span>
            <span class="dreamer-quick-title">Записать и толковать сон с AI</span>
          </div>
          <img class="calendar-event-arrow" src="moonly_3d_icons/ic_calendar_v2_arrow.png" alt="Arrow">
        </div>"""

# Replace from `<!-- Карточка 3: Транзит Луны` down to `</div>\n      </div>\n\n      <!-- ==========================================\n           ЭКРАН 2: ПРАКТИКИ`
pattern = r'<!-- Карточка 3: Транзит Луны[\s\S]*?<!-- Баннер Дневника Снов \(Dreamer\)[\s\S]*?</div>\s*</div>'
content = re.sub(pattern, feed_replacement + "\n      </div>", content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Calendar feed replaced with authentic Moonly cards!")
