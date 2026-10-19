# -*- coding: utf-8 -*-
import os
import shutil

TARGET_FILE = r"D:\projects\monly\АСТРА_АССЕТЫ\astra_main_app.html"
BACKUP_FILE = r"D:\projects\monly\АСТРА_АССЕТЫ\astra_main_app.html.bak_tarot_paywall"

print(f"Backing up {TARGET_FILE} -> {BACKUP_FILE}...")
shutil.copyfile(TARGET_FILE, BACKUP_FILE)

with open(TARGET_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Tarot Arc CSS and add Paywall & Triad CSS
css_tarot_old = """    .spread-deck-arc-container {
      position: relative;
      width: 100%;
      height: 146px;
      margin-top: 14px;
      overflow: hidden;
      touch-action: pan-y;
      user-select: none;
      cursor: grab;
      border-radius: 20px;
      background: radial-gradient(ellipse at 50% 100%, rgba(30, 25, 45, 0.4) 0%, transparent 70%);
    }

    .spread-deck-arc-container:active {
      cursor: grabbing;
    }

    .spread-deck-arc-viewport {
      position: relative;
      width: 100%;
      height: 100%;
      pointer-events: auto;
      transition: opacity 0.3s ease;
    }

    .spread-deck-arc-viewport.dimmed {
      opacity: 0.22;
      pointer-events: none;
    }

    .spread-arc-card {
      position: absolute;
      width: 62px;
      height: 98px;
      border-radius: 10px;
      box-shadow: 0 6px 18px rgba(0, 0, 0, 0.7);
      cursor: pointer;
      transform-origin: 50% 120%;
      transition: box-shadow 0.2s ease, filter 0.2s ease;
      will-change: transform, left, top;
      border: 1px solid rgba(255, 255, 255, 0.12);
      background: #181822;
      overflow: hidden;
    }

    .spread-arc-card img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      pointer-events: none;
      display: block;
    }

    .spread-arc-card:hover {
      filter: brightness(1.22);
      box-shadow: 0 10px 24px rgba(247, 182, 77, 0.45);
      z-index: 80 !important;
    }"""

css_tarot_new = """    .spread-deck-arc-container {
      position: relative;
      width: 100%;
      height: 185px;
      margin-top: 10px;
      overflow: hidden;
      touch-action: pan-y;
      user-select: none;
      cursor: grab;
      border-radius: 20px;
      background: radial-gradient(ellipse at 50% 100%, rgba(138, 99, 255, 0.15) 0%, transparent 75%);
    }

    .spread-deck-arc-container:active {
      cursor: grabbing;
    }

    .spread-deck-arc-viewport {
      position: relative;
      width: 100%;
      height: 100%;
      pointer-events: auto;
      transition: opacity 0.3s ease;
    }

    .spread-deck-arc-viewport.dimmed {
      opacity: 0.22;
      pointer-events: none;
    }

    .spread-arc-card {
      position: absolute;
      width: 62px;
      height: 98px;
      border-radius: 10px;
      box-shadow: 0 8px 22px rgba(0, 0, 0, 0.8);
      cursor: pointer;
      transform-origin: 50% 50%;
      transition: box-shadow 0.2s ease, filter 0.2s ease, border-color 0.2s ease;
      will-change: transform, left, top;
      border: 1px solid rgba(255, 255, 255, 0.2);
      background: #14141e;
      overflow: hidden;
    }

    .spread-arc-card img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      pointer-events: none;
      display: block;
    }

    .spread-arc-card:hover {
      filter: brightness(1.25);
      border-color: #F7B64D;
      box-shadow: 0 10px 24px rgba(247, 182, 77, 0.5);
      z-index: 120 !important;
    }

    /* Модальное окно Триады Таро (3-карточный расклад) */
    .triad-modal-container {
      display: flex;
      flex-direction: column;
      width: 100%;
      padding: 0 4px 10px;
    }

    .triad-modal-header {
      text-align: center;
      margin-bottom: 16px;
    }

    .triad-badge {
      display: inline-block;
      font-size: 11px;
      font-weight: 800;
      color: var(--moonly-gold);
      letter-spacing: 0.6px;
      text-transform: uppercase;
      margin-bottom: 4px;
    }

    .triad-title {
      font-size: 20px;
      font-weight: 800;
      color: #FFFFFF;
      margin: 0 0 4px;
    }

    .triad-subtitle {
      font-size: 12px;
      color: var(--moonly-text-sub);
    }

    .triad-cards-row {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 10px;
      margin-bottom: 18px;
    }

    .triad-mini-card {
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
    }

    .triad-mini-pos {
      font-size: 9.5px;
      font-weight: 800;
      color: #F7B64D;
      letter-spacing: 0.4px;
      margin-bottom: 6px;
      text-transform: uppercase;
    }

    .triad-card-frame {
      width: 100%;
      aspect-ratio: 1 / 1.55;
      border-radius: 12px;
      overflow: hidden;
      border: 1.5px solid rgba(255, 255, 255, 0.15);
      box-shadow: 0 6px 18px rgba(0,0,0,0.6);
      background: #14141d;
    }

    .triad-card-frame img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }

    .triad-card-caption {
      font-size: 10.5px;
      font-weight: 700;
      color: #FFFFFF;
      margin-top: 6px;
      line-height: 1.25;
    }

    .triad-details-section {
      display: flex;
      flex-direction: column;
      gap: 12px;
      margin-bottom: 18px;
    }

    .triad-detail-card {
      background: var(--moonly-card);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 18px;
      padding: 14px 16px;
      text-align: left;
    }

    .triad-pos-tag {
      display: inline-block;
      font-size: 10.5px;
      font-weight: 800;
      padding: 3px 10px;
      border-radius: 8px;
      margin-bottom: 8px;
      text-transform: uppercase;
      letter-spacing: 0.4px;
    }

    .triad-detail-title {
      font-size: 14.5px;
      font-weight: 800;
      color: #FFFFFF;
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }

    .triad-arch-tag {
      font-size: 11px;
      font-weight: 600;
      color: var(--moonly-gold);
    }

    .triad-detail-text {
      font-size: 13px;
      line-height: 1.5;
      color: #D4D4DF;
      margin: 0;
    }

    .triad-synergy-box {
      background: linear-gradient(135deg, rgba(138, 99, 255, 0.14) 0%, rgba(30, 25, 45, 0.7) 100%);
      border: 1.5px solid rgba(138, 99, 255, 0.35);
      border-radius: 18px;
      padding: 16px;
      margin-bottom: 18px;
      text-align: left;
    }

    .triad-synergy-title {
      font-size: 13.5px;
      font-weight: 800;
      color: #C4B5FD;
      margin-bottom: 6px;
      letter-spacing: 0.3px;
    }

    .triad-synergy-text {
      font-size: 13px;
      line-height: 1.55;
      color: #E4E4EE;
      margin: 0;
    }

    /* Кнопка "Обсудить с наставником" */
    .mentor-insight-cta-btn {
      width: 100%;
      border-radius: 24px;
      background: linear-gradient(135deg, #8A63FF 0%, #633BF3 100%);
      border: none;
      color: #FFFFFF;
      padding: 13px 16px;
      display: flex;
      align-items: center;
      gap: 12px;
      cursor: pointer;
      box-shadow: 0 8px 24px rgba(138, 99, 255, 0.4);
      margin-bottom: 10px;
      transition: transform 0.18s ease, box-shadow 0.18s ease;
      text-align: left;
    }

    .mentor-insight-cta-btn:hover {
      transform: scale(1.02);
      box-shadow: 0 10px 30px rgba(138, 99, 255, 0.55);
    }

    .mentor-cta-icon {
      font-size: 22px;
      width: 38px;
      height: 38px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.18);
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }

    .mentor-cta-text-wrap {
      display: flex;
      flex-direction: column;
    }

    .mentor-cta-title {
      font-size: 13.5px;
      font-weight: 800;
      color: #FFFFFF;
      letter-spacing: 0.2px;
    }

    .mentor-cta-subtitle {
      font-size: 10.5px;
      color: rgba(255, 255, 255, 0.8);
      margin-top: 2px;
    }

    .triad-close-btn {
      width: 100%;
      height: 44px;
      border-radius: 22px;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: #FFFFFF;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
    }

    /* АУТЕНТИЧНЫЙ ПЕЙВОЛ MOONLY (MeaningsV2RepeatPaywallBottomFragment) */
    .universal-modal-sheet.paywall-mode {
      padding: 0 0 32px 0 !important;
      max-height: 94% !important;
      background: #121218 !important;
      border-radius: 28px 28px 0 0 !important;
      overflow-y: auto;
      overflow-x: hidden;
    }

    .moonly-paywall-wrap {
      display: flex;
      flex-direction: column;
      width: 100%;
    }

    .moonly-paywall-hero {
      position: relative;
      width: 100%;
      height: 250px;
      overflow: hidden;
      border-radius: 28px 28px 0 0;
    }

    .moonly-paywall-bg-img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: center top;
      display: block;
    }

    .moonly-paywall-hero-grad {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: linear-gradient(180deg, rgba(18, 18, 24, 0.05) 0%, rgba(18, 18, 24, 0.4) 45%, #121218 100%);
      pointer-events: none;
    }

    .moonly-paywall-close-btn {
      position: absolute;
      top: 14px;
      right: 14px;
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: rgba(0, 0, 0, 0.45);
      border: 1px solid rgba(255, 255, 255, 0.2);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      z-index: 10;
      backdrop-filter: blur(10px);
      padding: 0;
    }

    .moonly-paywall-close-btn img {
      width: 14px;
      height: 14px;
      opacity: 0.9;
    }

    .moonly-paywall-hero-content {
      position: absolute;
      bottom: 12px;
      left: 0;
      width: 100%;
      padding: 0 20px;
      text-align: center;
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    .moonly-paywall-hero-pill {
      display: inline-flex;
      align-items: center;
      padding: 4px 12px;
      border-radius: 12px;
      background: rgba(247, 182, 77, 0.2);
      border: 1px solid rgba(247, 182, 77, 0.4);
      color: #F7B64D;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.6px;
      text-transform: uppercase;
      margin-bottom: 8px;
    }

    .moonly-paywall-hero-title {
      font-size: 23px;
      font-weight: 800;
      color: #FFFFFF;
      line-height: 1.2;
      letter-spacing: 0.2px;
      margin: 0 0 6px;
      text-shadow: 0 2px 10px rgba(0,0,0,0.6);
    }

    .moonly-paywall-hero-sub {
      font-size: 12.5px;
      color: #C5C5D2;
      line-height: 1.4;
      margin: 0;
      max-width: 330px;
      text-shadow: 0 1px 4px rgba(0,0,0,0.8);
    }

    .moonly-paywall-body {
      padding: 16px 18px 24px;
      display: flex;
      flex-direction: column;
      align-items: center;
      background: #121218;
    }

    .moonly-paywall-features-container {
      width: 100%;
      display: flex;
      justify-content: center;
      margin-bottom: 16px;
    }

    .moonly-paywall-features-img {
      width: 100%;
      max-width: 340px;
      height: auto;
      display: block;
      filter: drop-shadow(0 4px 12px rgba(0,0,0,0.4));
    }

    .moonly-paywall-review-card {
      width: 100%;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 18px;
      padding: 14px 16px;
      text-align: center;
      margin-bottom: 18px;
      transition: opacity 0.3s ease;
    }

    .moonly-paywall-stars {
      color: #F7B64D;
      font-size: 16px;
      letter-spacing: 3px;
      margin-bottom: 6px;
    }

    .moonly-paywall-quote {
      font-size: 13px;
      font-weight: 600;
      line-height: 1.45;
      color: #E6E6EE;
      margin-bottom: 8px;
      font-style: italic;
      min-height: 38px;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .moonly-paywall-author-row {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
    }

    .moonly-paywall-avatar {
      width: 20px;
      height: 20px;
      border-radius: 50%;
      object-fit: cover;
    }

    .moonly-paywall-name {
      font-size: 11.5px;
      color: #8E8E9E;
      font-weight: 600;
    }

    .moonly-paywall-plans-row {
      width: 100%;
      display: grid;
      grid-template-columns: 1fr 1.15fr 1fr;
      gap: 8px;
      margin-bottom: 20px;
      align-items: stretch;
    }

    .moonly-plan-card {
      position: relative;
      background: rgba(255, 255, 255, 0.04);
      border: 1.5px solid rgba(255, 255, 255, 0.09);
      border-radius: 20px;
      padding: 14px 8px 12px;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      cursor: pointer;
      transition: all 0.22s ease;
    }

    .moonly-plan-card.selected {
      background: linear-gradient(180deg, rgba(247, 182, 77, 0.16) 0%, rgba(24, 24, 34, 0.9) 100%);
      border-color: #F7B64D;
      box-shadow: 0 0 20px rgba(247, 182, 77, 0.22);
      transform: translateY(-2px);
    }

    .moonly-plan-badge {
      position: absolute;
      top: -10px;
      background: linear-gradient(135deg, #FF6B6B 0%, #E83A3A 100%);
      color: #FFF;
      font-size: 10px;
      font-weight: 800;
      padding: 2px 8px;
      border-radius: 10px;
      box-shadow: 0 2px 8px rgba(232, 58, 58, 0.5);
      letter-spacing: 0.4px;
    }

    .moonly-plan-icon-wrap {
      width: 44px;
      height: 44px;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .moonly-plan-icon-wrap img {
      width: 100%;
      height: 100%;
      object-fit: contain;
    }

    .moonly-plan-title {
      font-size: 12.5px;
      font-weight: 700;
      color: #FFFFFF;
      margin-bottom: 3px;
    }

    .moonly-plan-price {
      font-size: 16px;
      font-weight: 800;
      color: #F7B64D;
      margin-bottom: 2px;
    }

    .moonly-plan-card.selected .moonly-plan-price {
      color: #FFCF70;
    }

    .moonly-plan-sub {
      font-size: 10px;
      color: #8C8C9A;
      line-height: 1.25;
    }

    .moonly-paywall-submit-btn {
      width: 100%;
      height: 52px;
      border-radius: 26px;
      background: linear-gradient(135deg, #F7B64D 0%, #E59824 100%);
      border: none;
      color: #121218;
      font-size: 15px;
      font-weight: 800;
      letter-spacing: 0.3px;
      cursor: pointer;
      box-shadow: 0 6px 24px rgba(247, 182, 77, 0.4);
      display: flex;
      align-items: center;
      justify-content: center;
      transition: transform 0.18s ease, box-shadow 0.18s ease;
    }

    .moonly-paywall-submit-btn:hover {
      transform: scale(1.02);
      box-shadow: 0 8px 30px rgba(247, 182, 77, 0.55);
    }

    .moonly-paywall-guarantee {
      font-size: 11px;
      color: #727282;
      margin-top: 12px;
      text-align: center;
      line-height: 1.4;
    }"""

if css_tarot_old in content:
    content = content.replace(css_tarot_old, css_tarot_new)
    print("✓ Updated CSS: Tarot arc, Triad Modal, and Moonly Paywall")
else:
    print("WARN: Could not find exact css_tarot_old block")

# 2. Update Paywall JS logic
js_paywall_old = """    /* Модальное окно Astra Plus / Paywall Sheet */
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
    }"""

js_paywall_new = """    /* Аутентичный пейвол Moonly (MeaningsV2RepeatPaywallBottomFragment) */
    let paywallReviewTimer = null;
    const MOONLY_REVIEWS = [
      { text: "«Moonly помогло мне найти баланс и гармонию в повседневной жизни.»", name: "Анна М. • 5 звезд в App Store", avatar: "moonly_3d_icons/ic_you_report_ascendant.png" },
      { text: "«Невероятная точность натальной карты и ежедневных рекомендаций!»", name: "Елена К. • 5 звезд в Google Play", avatar: "moonly_3d_icons/ic_you_report_personality.png" },
      { text: "«Медитации и лунный календарь стали моим утренним ритуалом.»", name: "Дарья С. • 5 звезд в App Store", avatar: "moonly_3d_icons/ic_you_report_birth_chart.png" },
      { text: "«Лучшее ведическое приложение, эстетика и глубина на высшем уровне.»", name: "Мария В. • 5 звезд в Google Play", avatar: "moonly_3d_icons/ic_you_report_destiny.png" }
    ];
    let currentReviewIdx = 0;

    function openAstraPlusModal(dayObj) {
      const content = `
        <div class="moonly-paywall-wrap">
          <div class="moonly-paywall-hero">
            <img src="moonly_paywall/new_paywall_bg_female_2.png" class="moonly-paywall-bg-img" alt="Moonly Muse">
            <div class="moonly-paywall-hero-grad"></div>
            <button class="moonly-paywall-close-btn" onclick="closeUniversalModal()">
              <img src="moonly_paywall/ic_close_paywall.png" alt="Close">
            </button>
            <div class="moonly-paywall-hero-content">
              <div class="moonly-paywall-hero-pill">✨ ПОЛНЫЙ ДОСТУП СО СКИДКОЙ 60%</div>
              <h2 class="moonly-paywall-hero-title">Откройте мудрость звезд</h2>
              <p class="moonly-paywall-hero-sub">Календарь на 2026–2027, все сферы жизни, расклады Таро и персональный астро-наставник</p>
            </div>
          </div>

          <div class="moonly-paywall-body">
            <!-- 6 Фич из Moonly ic_paywall_meanings_features.png -->
            <div class="moonly-paywall-features-container">
              <img src="moonly_paywall/ic_paywall_meanings_features.png" alt="Moonly Meanings Features" class="moonly-paywall-features-img">
            </div>

            <!-- Автоматически сменяющиеся отзывы пользователей (5 сек) -->
            <div class="moonly-paywall-review-card" id="paywall-review-card">
              <div class="moonly-paywall-stars">★★★★★</div>
              <div class="moonly-paywall-quote" id="paywall-review-quote">«Moonly помогло мне найти баланс и гармонию в повседневной жизни.»</div>
              <div class="moonly-paywall-author-row">
                <img src="moonly_3d_icons/ic_you_report_ascendant.png" id="paywall-review-avatar" class="moonly-paywall-avatar" alt="Avatar">
                <span class="moonly-paywall-name" id="paywall-review-name">Анна М. • 5 звезд в App Store</span>
              </div>
            </div>

            <!-- 3 Тарифа с круглыми иконками из Moonly -->
            <div class="moonly-paywall-plans-row">
              <!-- Месяц -->
              <div class="moonly-plan-card" onclick="selectMoonlyPlan(this, 'month')">
                <div class="moonly-plan-icon-wrap">
                  <img src="moonly_paywall/ic_paywall_round_month.png" alt="Month">
                </div>
                <div class="moonly-plan-title">1 Месяц</div>
                <div class="moonly-plan-price">499 ₽</div>
                <div class="moonly-plan-sub">в месяц</div>
              </div>

              <!-- Год (Рекомендованный) -->
              <div class="moonly-plan-card selected" onclick="selectMoonlyPlan(this, 'year')">
                <div class="moonly-plan-badge">-60%</div>
                <div class="moonly-plan-icon-wrap">
                  <img src="moonly_paywall/ic_paywall_round_year.png" alt="Year">
                </div>
                <div class="moonly-plan-title">1 Год</div>
                <div class="moonly-plan-price">199 ₽</div>
                <div class="moonly-plan-sub">/ мес (2 390 ₽/год)</div>
              </div>

              <!-- Навсегда -->
              <div class="moonly-plan-card" onclick="selectMoonlyPlan(this, 'lifetime')">
                <div class="moonly-plan-icon-wrap">
                  <img src="moonly_paywall/ic_paywall_round_lifetime.png" alt="Lifetime">
                </div>
                <div class="moonly-plan-title">Навсегда</div>
                <div class="moonly-plan-price">5 990 ₽</div>
                <div class="moonly-plan-sub">разовый доступ</div>
              </div>
            </div>

            <!-- Кнопка CTA -->
            <button class="moonly-paywall-submit-btn" onclick="confirmSubscription()">
              <span>Попробовать 7 дней бесплатно</span>
            </button>
            <div class="moonly-paywall-guarantee">
              Без списаний сейчас • Отмена в любой момент • Полная безопасность
            </div>
          </div>
        </div>
      `;
      showUniversalModal(content, true);

      // Запуск циклической ротации отзывов каждые 4.5 секунды
      if (paywallReviewTimer) clearInterval(paywallReviewTimer);
      currentReviewIdx = 0;
      paywallReviewTimer = setInterval(() => {
        const card = document.getElementById('paywall-review-card');
        if (!card) return;
        currentReviewIdx = (currentReviewIdx + 1) % MOONLY_REVIEWS.length;
        const rev = MOONLY_REVIEWS[currentReviewIdx];
        card.style.opacity = '0.2';
        setTimeout(() => {
          const q = document.getElementById('paywall-review-quote');
          const n = document.getElementById('paywall-review-name');
          const a = document.getElementById('paywall-review-avatar');
          if (q) q.innerText = rev.text;
          if (n) n.innerText = rev.name;
          if (a) a.src = rev.avatar;
          card.style.opacity = '1';
        }, 250);
      }, 4500);
    }

    function selectMoonlyPlan(card, type) {
      document.querySelectorAll('.moonly-plan-card').forEach(c => c.classList.remove('selected'));
      card.classList.add('selected');
    }

    function confirmSubscription() {
      alert("✨ Поздравляем! Полный доступ Astra Plus активирован на 7 дней бесплатно.");
      closeUniversalModal();
    }"""

if js_paywall_old in content:
    content = content.replace(js_paywall_old, js_paywall_new)
    print("✓ Updated Paywall JS: Moonly authentic layout and review carousel")
else:
    print("WARN: Could not find exact js_paywall_old block")

# 3. Update Tarot Arc Deck logic
js_tarot_arc_old = """    function renderTarotArcCards() {
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
    }"""

js_tarot_arc_new = """    function renderTarotArcCards() {
      const container = document.getElementById('tarot-arc-container');
      const containerW = container ? container.clientWidth : 340;
      const centerX = containerW / 2;
      const R = 440;
      const stepAngle = 3.8;
      const N = tarotDeckCards.length;
      const apexY = 14;

      tarotDeckCards.forEach((c, i) => {
        const angleDeg = tarotDeckRotation + (i - (N - 1) / 2) * stepAngle;
        const angleRad = (angleDeg * Math.PI) / 180;

        const isVisible = (Math.abs(angleDeg) <= 60);
        if (!isVisible) {
          c.el.style.display = 'none';
          return;
        }

        const x = centerX + R * Math.sin(angleRad) - 31;
        const y = apexY + R * (1 - Math.cos(angleRad));

        c.el.style.display = 'block';
        c.el.style.left = `${x.toFixed(1)}px`;
        c.el.style.top = `${y.toFixed(1)}px`;
        c.el.style.transform = `rotate(${angleDeg.toFixed(2)}deg)`;
        c.el.style.zIndex = Math.round(100 - Math.abs(angleDeg));

        const distFromCenter = Math.abs(angleDeg);
        if (distFromCenter > 38) {
          c.el.style.opacity = Math.max(0.15, 1 - (distFromCenter - 38) / 20).toFixed(2);
        } else {
          c.el.style.opacity = '1';
        }
      });
    }"""

if js_tarot_arc_old in content:
    content = content.replace(js_tarot_arc_old, js_tarot_arc_new)
    print("✓ Updated renderTarotArcCards math: zero clipping, continuous convex fan dome")
else:
    print("WARN: Could not find exact js_tarot_arc_old block")

# 4. Update initTarotArcDeck to use 22 Major Arcana and smooth drag
js_init_deck_old = """    function initTarotArcDeck() {
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
          if (Math.abs(tarotVelocity) > 0.3) return;
          drawCardFromArc(i, cardData, cardEl);
        });

        viewport.appendChild(cardEl);
        tarotDeckCards.push({ el: cardEl, data: cardData, index: i });
      }

      renderTarotArcCards();
      setupArcDragEvents();
    }"""

js_init_deck_new = """    function initTarotArcDeck() {
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
          if (Math.abs(tarotVelocity) > 0.4) return;
          drawCardFromArc(i, cardData, cardEl);
        });

        viewport.appendChild(cardEl);
        tarotDeckCards.push({ el: cardEl, data: cardData, index: i });
      });

      renderTarotArcCards();
      setupArcDragEvents();
    }"""

if js_init_deck_old in content:
    content = content.replace(js_init_deck_old, js_init_deck_new)
    print("✓ Updated initTarotArcDeck: 22 Major Arcana cards")
else:
    print("WARN: Could not find exact js_init_deck_old block")

# 5. Update drawCardFromArc, selectTarotSlot, and resetTarotSpread
js_draw_old = """    function drawCardFromArc(index, cardData, cardEl) {
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
    }"""

js_draw_new = """    function drawCardFromArc(index, cardData, cardEl) {
      currentDrawnCard = cardData;
      drawnSlots[activeSlotIndex] = cardData;

      const slotBox = document.getElementById(`tarot-slot-${activeSlotIndex}`);
      const slotImg = document.getElementById(`slot-img-${activeSlotIndex}`);
      if (slotImg) {
        slotImg.src = `01_ТАРО_КАРТЫ/${cardData.file}`;
        slotImg.style.opacity = '1';
        slotBox.style.border = '2px solid #F7B64D';
        slotBox.style.boxShadow = '0 0 16px rgba(247, 182, 77, 0.4)';
        slotBox.style.transform = 'scale(1.08)';
        setTimeout(() => slotBox.style.transform = 'scale(1)', 250);
      }

      const filledCount = drawnSlots.filter(Boolean).length;
      const res = document.getElementById('spread-result');
      const prompt = document.getElementById('tarot-prompt-indicator');

      if (filledCount === 3) {
        if (prompt) prompt.style.display = 'none';
        document.getElementById('res-card-name').innerText = "🔮 Расклад Триады завершен";
        document.getElementById('res-card-archetype').innerText = `${drawnSlots[0].name} • ${drawnSlots[1].name} • ${drawnSlots[2].name}`;
        document.getElementById('res-card-reading').innerText = "Все 3 ключевые энергии дня раскрыты! Ознакомьтесь с глубоким синтезом триады или обсудите инсайт с личным наставником.";
        if (res) res.style.display = 'flex';
      } else {
        if (prompt) {
          prompt.innerHTML = `<span style="font-size: 11px;">▲</span><span>Вытянуто ${filledCount} из 3 • Тяните следующую карту</span>`;
        }
        document.getElementById('res-card-name').innerText = cardData.name;
        document.getElementById('res-card-archetype').innerText = cardData.arch;
        document.getElementById('res-card-reading').innerText = cardData.direct;
        if (res) res.style.display = 'flex';

        // Переключаем на следующий свободный слот
        if (activeSlotIndex < 2) {
          setTimeout(() => selectTarotSlot(activeSlotIndex + 1), 600);
        }
      }
    }"""

if js_draw_old in content:
    content = content.replace(js_draw_old, js_draw_new)
    print("✓ Updated drawCardFromArc: 3-card completion state and prompt handling")
else:
    print("WARN: Could not find exact js_draw_old block")

# 6. Update openActiveCardModal and showCardModal to include Triad reading + Mentor Insight Button
js_modal_old = """    function showCardModal(card) {
      const content = `
        <img src="01_ТАРО_КАРТЫ/${card.file}" style="width: 140px; height: 220px; border-radius: 16px; object-fit: cover; align-self: center; box-shadow: 0 8px 24px rgba(0,0,0,0.6);" onerror="this.src='moonly_3d_icons/ic_tarot_card_back_v3.png'">
        <h3 style="font-size: 20px; font-weight: 800; color: #FFF; margin-top: 14px; text-align: center;">${card.name}</h3>
        <div style="font-size: 11px; font-weight: 700; color: var(--moonly-gold); text-transform: uppercase; text-align: center; margin-top: 4px;">Архетип: ${card.arch}</div>
        
        <div style="margin-top: 18px;">
          <h4 style="font-size: 13px; color: var(--moonly-gold); text-transform: uppercase;">Прямое значение</h4>
          <p style="font-size: 14px; line-height: 1.45; color: #E5E5EB; margin-top: 6px;">${card.direct}</p>
        </div>

        <div style="margin-top: 14px;">
          <h4 style="font-size: 13px; color: #8A63FF; text-transform: uppercase;">Совет Аркана</h4>
          <p style="font-size: 14px; line-height: 1.45; color: #E5E5EB; margin-top: 6px;">${card.advice}</p>
        </div>

        <button onclick="closeUniversalModal()" style="margin-top: 22px; height: 48px; border-radius: 24px; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); color: #FFF; font-weight: 700; cursor: pointer;">Закрыть</button>
      `;
      showUniversalModal(content);
    }

    function openActiveCardModal() {
      showCardModal(currentDrawnCard);
    }"""

js_modal_new = """    function showCardModal(card) {
      if (!card) return;
      const content = `
        <div style="display: flex; flex-direction: column; width: 100%; text-align: left;">
          <img src="01_ТАРО_КАРТЫ/${card.file}" style="width: 140px; height: 220px; border-radius: 16px; object-fit: cover; align-self: center; box-shadow: 0 8px 24px rgba(0,0,0,0.6);" onerror="this.src='moonly_3d_icons/ic_tarot_card_back_v3.png'">
          <h3 style="font-size: 20px; font-weight: 800; color: #FFF; margin-top: 14px; text-align: center;">${card.name}</h3>
          <div style="font-size: 11px; font-weight: 700; color: var(--moonly-gold); text-transform: uppercase; text-align: center; margin-top: 4px;">Архетип: ${card.arch}</div>
          
          <div style="margin-top: 18px; background: var(--moonly-card); border-radius: 16px; padding: 14px;">
            <h4 style="font-size: 12px; color: var(--moonly-gold); text-transform: uppercase; margin-bottom: 4px;">Прямое значение</h4>
            <p style="font-size: 13.5px; line-height: 1.45; color: #E5E5EB; margin: 0;">${card.direct}</p>
          </div>

          <div style="margin-top: 10px; background: var(--moonly-card); border-radius: 16px; padding: 14px;">
            <h4 style="font-size: 12px; color: #A78BFA; text-transform: uppercase; margin-bottom: 4px;">Совет Аркана</h4>
            <p style="font-size: 13.5px; line-height: 1.45; color: #E5E5EB; margin: 0;">${card.advice}</p>
          </div>

          <!-- Кнопка "Обсудить с наставником • Получить инсайт" -->
          <button class="mentor-insight-cta-btn" onclick="openMentorInsightFromSingleCard('${card.name.replace(/'/g, "\\'")}', '${card.arch.replace(/'/g, "\\'")}')" style="margin-top: 16px;">
            <span class="mentor-cta-icon">💬</span>
            <div class="mentor-cta-text-wrap">
              <span class="mentor-cta-title">Обсудить с наставником • Получить инсайт</span>
              <span class="mentor-cta-subtitle">Задать вопрос ИИ-астрологу о значении этого аркана</span>
            </div>
          </button>

          <button onclick="closeUniversalModal()" style="margin-top: 8px; height: 46px; border-radius: 23px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); color: #FFF; font-weight: 700; cursor: pointer;">Закрыть</button>
        </div>
      `;
      showUniversalModal(content);
    }

    function openActiveCardModal() {
      const drawn = drawnSlots.filter(Boolean);
      if (drawn.length === 3) {
        openTriadSpreadModal(drawnSlots);
      } else if (currentDrawnCard) {
        showCardModal(currentDrawnCard);
      } else if (drawn.length > 0) {
        showCardModal(drawn[drawn.length - 1]);
      }
    }

    function openTriadSpreadModal(slots) {
      const c0 = slots[0];
      const c1 = slots[1];
      const c2 = slots[2];

      const synergyText = `В раскладе сегодняшнего дня аркан «${c0.name}» создает устойчивую исходную точку, проходя через трансформационный вызов «${c1.name}», и открывает ясный путь в энергиях «${c2.name}». Синтез энергий советует не форсировать события, действовать осознанно и довериться своему внутреннему компасу.`;

      const content = `
        <div class="triad-modal-container">
          <div class="triad-modal-header">
            <div class="triad-badge">🔮 РАСКЛАД «ТРИПТИХ СУДЬБЫ»</div>
            <h2 class="triad-title">Полное толкование Триады</h2>
            <div class="triad-subtitle">Синтез космических энергий дня по 3 ключевым позициям</div>
          </div>

          <!-- 3 Карты в ряд -->
          <div class="triad-cards-row">
            <div class="triad-mini-card">
              <div class="triad-mini-pos">1. СИТУАЦИЯ</div>
              <div class="triad-card-frame">
                <img src="01_ТАРО_КАРТЫ/${c0.file}" alt="${c0.name}">
              </div>
              <div class="triad-card-caption">${c0.name}</div>
            </div>

            <div class="triad-mini-card">
              <div class="triad-mini-pos">2. УРОК</div>
              <div class="triad-card-frame">
                <img src="01_ТАРО_КАРТЫ/${c1.file}" alt="${c1.name}">
              </div>
              <div class="triad-card-caption">${c1.name}</div>
            </div>

            <div class="triad-mini-card">
              <div class="triad-mini-pos">3. СОВЕТ</div>
              <div class="triad-card-frame">
                <img src="01_ТАРО_КАРТЫ/${c2.file}" alt="${c2.name}">
              </div>
              <div class="triad-card-caption">${c2.name}</div>
            </div>
          </div>

          <!-- Детальные блоки толкования каждой позиции -->
          <div class="triad-details-section">
            <div class="triad-detail-card">
              <div class="triad-pos-tag" style="background: rgba(247, 182, 77, 0.15); color: #F7B64D; border: 1px solid rgba(247, 182, 77, 0.3);">
                Позиция 1 • Текущая ситуация и фундамент
              </div>
              <div class="triad-detail-title">${c0.name} <span class="triad-arch-tag">${c0.arch}</span></div>
              <p class="triad-detail-text">${c0.direct}</p>
            </div>

            <div class="triad-detail-card">
              <div class="triad-pos-tag" style="background: rgba(235, 87, 87, 0.15); color: #FF7B7B; border: 1px solid rgba(235, 87, 87, 0.3);">
                Позиция 2 • Препятствие, вызов и кармический урок
              </div>
              <div class="triad-detail-title">${c1.name} <span class="triad-arch-tag">${c1.arch}</span></div>
              <p class="triad-detail-text">${c1.direct} Обратите внимание на скрытые иллюзии и не спешите с выводами.</p>
            </div>

            <div class="triad-detail-card">
              <div class="triad-pos-tag" style="background: rgba(138, 99, 255, 0.15); color: #A78BFA; border: 1px solid rgba(138, 99, 255, 0.3);">
                Позиция 3 • Совет Аркана и высший исход
              </div>
              <div class="triad-detail-title">${c2.name} <span class="triad-arch-tag">${c2.arch}</span></div>
              <p class="triad-detail-text">${c2.advice}</p>
            </div>
          </div>

          <!-- Синтез триады -->
          <div class="triad-synergy-box">
            <div class="triad-synergy-title">✨ Космический Синтез Триады</div>
            <p class="triad-synergy-text">${synergyText}</p>
          </div>

          <!-- ГЛАВНАЯ КНОПКА: ОБСУДИТЬ С НАСТАВНИКОМ • ПОЛУЧИТЬ ИНСАЙТ -->
          <button class="mentor-insight-cta-btn" onclick="openMentorInsightFromTriad()">
            <span class="mentor-cta-icon">💬</span>
            <div class="mentor-cta-text-wrap">
              <span class="mentor-cta-title">Обсудить с наставником • Получить инсайт</span>
              <span class="mentor-cta-subtitle">Персональный ИИ-разбор синергии расклада в чате</span>
            </div>
          </button>

          <button class="triad-close-btn" onclick="closeUniversalModal()">Закрыть расклад</button>
        </div>
      `;
      showUniversalModal(content);
    }

    function openMentorInsightFromTriad() {
      closeUniversalModal();
      switchTab('screen-chat');

      const c0 = drawnSlots[0] ? drawnSlots[0].name : "19. Солнце";
      const c1 = drawnSlots[1] ? drawnSlots[1].name : "02. Верховная Жрица";
      const c2 = drawnSlots[2] ? drawnSlots[2].name : "18. Луна";

      const question = `Я сделал расклад Таро «Триптих дня»:
1. Ситуация: ${c0}
2. Урок: ${c1}
3. Совет: ${c2}

Помоги мне глубже расшифровать синергию этих трех энергий и дай персональный совет на сегодня.`;

      const input = document.getElementById('chat-input-field');
      if (input) {
        input.value = question;
        setTimeout(() => {
          sendChatMessage();
        }, 200);
      }
    }

    function openMentorInsightFromSingleCard(cardName, cardArch) {
      closeUniversalModal();
      switchTab('screen-chat');

      const question = `Я изучаю аркан «${cardName}» (${cardArch}). Как лучше всего интегрировать эту энергию сегодня и на что обратить внимание?`;

      const input = document.getElementById('chat-input-field');
      if (input) {
        input.value = question;
        setTimeout(() => {
          sendChatMessage();
        }, 200);
      }
    }"""

if js_modal_old in content:
    content = content.replace(js_modal_old, js_modal_new)
    print("✓ Updated openActiveCardModal: full Triad Spread Modal + 'Обсудить с наставником'")
else:
    print("WARN: Could not find exact js_modal_old block")

# 7. Update showUniversalModal and closeUniversalModal
js_univ_modal_old = """    function showUniversalModal(html) {
      document.getElementById('universal-modal-content').innerHTML = html;
      document.getElementById('universal-modal').style.display = 'flex';
    }

    function closeUniversalModal() {
      document.getElementById('universal-modal').style.display = 'none';
    }"""

js_univ_modal_new = """    function showUniversalModal(html, isPaywall = false) {
      const modal = document.getElementById('universal-modal');
      const handle = document.querySelector('.modal-close-handle');
      if (isPaywall) {
        modal.classList.add('paywall-mode');
        if (handle) handle.style.display = 'none';
      } else {
        modal.classList.remove('paywall-mode');
        if (handle) handle.style.display = 'block';
      }
      document.getElementById('universal-modal-content').innerHTML = html;
      modal.style.display = 'flex';
    }

    function closeUniversalModal() {
      const modal = document.getElementById('universal-modal');
      if (modal) {
        modal.style.display = 'none';
        modal.classList.remove('paywall-mode');
      }
      if (paywallReviewTimer) {
        clearInterval(paywallReviewTimer);
        paywallReviewTimer = null;
      }
    }"""

if js_univ_modal_old in content:
    content = content.replace(js_univ_modal_old, js_univ_modal_new)
    print("✓ Updated showUniversalModal & closeUniversalModal: paywall-mode and timer cleanup")
else:
    print("WARN: Could not find exact js_univ_modal_old block")

# 8. Enhance getAstrologicalAIResponse to answer Tarot questions deeply
js_astro_ai_old = """    function getAstrologicalAIResponse(q) {
      const query = q.toLowerCase();
      if (query.includes('тельце') || query.includes('луна')) {
        return 'Луна в знаке Тельца усиливает земную устойчивость и интуицию тела. Это благоприятное время для заботы о комфорте, завершения начатых задач и заземления эмоций.';
      } else if (query.includes('финанс') || query.includes('деньг') || query.includes('работ')) {
        return 'В финансовой сфере сейчас работает закон терпения и основательности. Избегайте импульсивных трат: надежные семена, посаженные сейчас, дадут богатый урожай.';
      } else if (query.includes('вечер') || query.includes('сил') || query.includes('ритуал')) {
        return 'Для вечернего ритуала зажгите свечу, включите частоту 432 Гц и примите теплую ванну с морской солью. Позвольте дню раствориться в мягком лунном покое.';
      } else if (query.includes('любов') || query.includes('отношен') || query.includes('сердц')) {
        return 'В отношениях царит искренность и чуткость. Позвольте себе открыться близкому человеку без защитных масок — Вселенная поддерживает созидательную любовь.';
      } else {
        return 'Вселенная слышит твой запрос. Энергетический фон благоприятствует глубокому созерцанию, очищению ума от суеты и доверию высшему замыслу.';
      }
    }"""

js_astro_ai_new = """    function getAstrologicalAIResponse(q) {
      const query = q.toLowerCase();
      if (query.includes('триптих') || (query.includes('ситуация') && query.includes('совет')) || (query.includes('расклад') && query.includes('таро'))) {
        return 'Твой триптих раскрывает редкую гармонию: энергия первого аркана закладывает фундамент осознанности, второй предупреждает о сомнениях ума, а третий дает высший вектор — действовать мягко и доверять интуиции. Сегодня космические врата открыты для созидания.';
      } else if (query.includes('аркан') || query.includes('таро')) {
        return 'Этот аркан сейчас активно вибрирует в твоем поле. Он советует удерживать равновесие между разумом и сердцем. Прислушивайся к тонким знакам — сегодня случайности не случайны.';
      } else if (query.includes('тельце') || query.includes('луна')) {
        return 'Луна в знаке Тельца усиливает земную устойчивость и интуицию тела. Это благоприятное время для заботы о комфорте, завершения начатых задач и заземления эмоций.';
      } else if (query.includes('финанс') || query.includes('деньг') || query.includes('работ')) {
        return 'В финансовой сфере сейчас работает закон терпения и основательности. Избегайте импульсивных трат: надежные семена, посаженные сейчас, дадут богатый урожай.';
      } else if (query.includes('вечер') || query.includes('сил') || query.includes('ритуал')) {
        return 'Для вечернего ритуала зажгите свечу, включите частоту 432 Гц и примите теплую ванну с морской солью. Позвольте дню раствориться в мягком лунном покое.';
      } else if (query.includes('любов') || query.includes('отношен') || query.includes('сердц')) {
        return 'В отношениях царит искренность и чуткость. Позвольте себе открыться близкому человеку без защитных масок — Вселенная поддерживает созидательную любовь.';
      } else {
        return 'Вселенная слышит твой запрос. Энергетический фон благоприятствует глубокому созерцанию, очищению ума от суеты и доверию высшему замыслу.';
      }
    }"""

if js_astro_ai_old in content:
    content = content.replace(js_astro_ai_old, js_astro_ai_new)
    print("✓ Updated getAstrologicalAIResponse: deep responses for Tarot readings")
else:
    print("WARN: Could not find exact js_astro_ai_old block")

with open(TARGET_FILE, "w", encoding="utf-8") as f:
    f.write(content)

print("SUCCESS: Target file written successfully.")
