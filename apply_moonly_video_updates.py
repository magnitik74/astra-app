import re
import os

filepath = r"D:\projects\monly\АСТРА_АССЕТЫ\astra_main_app.html"

with open(filepath, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update CSS around line 956
new_css = """
    /* СТИКИ-ХЕДЕР КАЛЕНДАРЯ (Moonly Sticky Week Strip) */
    .calendar-sticky-header {
      position: sticky;
      top: 0;
      z-index: 95;
      background: rgba(18, 17, 24, 0.88);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      padding: 6px 0 10px;
      margin-bottom: 2px;
    }

    /* БЫСТРЫЕ КНОПКИ (Quick Action Pills: Натальная карта & Таро) */
    .calendar-quick-actions-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin-top: 10px;
      margin-bottom: 4px;
    }

    .calendar-quick-pill {
      background: #1C1C24;
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 20px;
      padding: 10px 14px;
      display: flex;
      align-items: center;
      gap: 12px;
      cursor: pointer;
      transition: transform 0.15s ease, background 0.15s ease;
      user-select: none;
    }

    .calendar-quick-pill:active {
      transform: scale(0.97);
      background: #252530;
    }

    .quick-pill-icon {
      width: 28px;
      height: 28px;
      object-fit: contain;
      flex-shrink: 0;
    }

    .quick-pill-text {
      display: flex;
      flex-direction: column;
    }

    .quick-pill-tag {
      font-size: 9px;
      font-weight: 700;
      color: #8E8E93;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .quick-pill-title {
      font-size: 13px;
      font-weight: 700;
      color: #FFF;
      margin-top: 1px;
    }

    /* МИКРО-БЕЙДЖ ДНЯ В КАРТОЧКЕ 1 (Садоводство / Красота) */
    .card-micro-badge-wrap {
      display: inline-flex;
      align-items: center;
      background: rgba(28, 28, 36, 0.85);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 20px;
      padding: 6px 12px;
      gap: 10px;
      cursor: pointer;
      transition: all 0.3s ease;
      backdrop-filter: blur(10px);
    }

    .card-micro-badge-wrap:active {
      transform: scale(0.96);
    }

    .badge-icon {
      width: 26px;
      height: 26px;
      object-fit: contain;
    }

    .badge-tag {
      font-size: 9px;
      font-weight: 700;
      color: #A0A5B5;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .badge-title {
      font-size: 13px;
      font-weight: 700;
      color: #FFF;
      display: flex;
      align-items: center;
      gap: 4px;
    }

    /* КАРТОЧКА 3: НЕДЕЛЬНЫЙ ПЛАН ПРАКТИК (Moonly DayProgram) */
    .calendar-practices-card {
      background: var(--moonly-card);
      border-radius: 32px;
      padding: 22px;
      margin-top: 14px;
      display: flex;
      flex-direction: column;
      box-shadow: 0 12px 36px rgba(0, 0, 0, 0.4);
    }

    .practice-item-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.06);
      border-radius: 20px;
      padding: 12px 14px;
      margin-top: 10px;
      cursor: pointer;
      transition: transform 0.15s ease, background 0.15s ease;
    }

    .practice-item-row:active {
      transform: scale(0.98);
      background: rgba(255, 255, 255, 0.08);
    }

    .practice-item-info {
      display: flex;
      flex-direction: column;
      flex: 1;
      padding-right: 12px;
    }

    .practice-item-tag {
      font-size: 10px;
      font-weight: 700;
      color: #A0A5B5;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .practice-item-title {
      font-size: 15px;
      font-weight: 700;
      color: #FFF;
      margin-top: 2px;
    }

    .practice-item-sub {
      font-size: 12px;
      color: #8E8E98;
      line-height: 1.35;
      margin-top: 2px;
    }

    .practice-item-thumb {
      position: relative;
      width: 60px;
      height: 60px;
      border-radius: 16px;
      overflow: hidden;
      flex-shrink: 0;
      background: #252230;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .practice-item-thumb img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    .practice-play-badge {
      position: absolute;
      width: 24px;
      height: 24px;
      border-radius: 50%;
      background: rgba(0, 0, 0, 0.55);
      backdrop-filter: blur(6px);
      display: flex;
      align-items: center;
      justify-content: center;
      color: #FFF;
      font-size: 10px;
    }

    /* КАРТОЧКИ 4+: ГЛОБАЛЬНАЯ АСТРОЛОГИЯ (Планетарные транзиты) */
    .calendar-planetary-card {
      background: var(--moonly-card);
      border-radius: 32px;
      padding: 22px;
      margin-top: 14px;
      cursor: pointer;
      position: relative;
      box-shadow: 0 12px 36px rgba(0, 0, 0, 0.4);
      transition: transform 0.15s ease;
    }

    .calendar-planetary-card:active {
      transform: scale(0.98);
    }

    .transit-orbit-visual {
      position: relative;
      width: 100%;
      height: 52px;
      margin-top: 16px;
      display: flex;
      align-items: center;
    }

    .transit-orbit-arc-line {
      position: absolute;
      top: 50%;
      left: 0;
      width: 100%;
      height: 38px;
      border-top: 2px solid rgba(247, 182, 77, 0.35);
      border-radius: 50% 50% 0 0;
      pointer-events: none;
    }

    .transit-planets-group {
      display: flex;
      align-items: center;
      gap: 6px;
      z-index: 2;
    }

    .transit-planet-sphere {
      width: 26px;
      height: 26px;
      border-radius: 50%;
      object-fit: contain;
      filter: drop-shadow(0 2px 6px rgba(0,0,0,0.6));
    }

    .transit-days-left-tag {
      margin-left: auto;
      font-size: 11px;
      font-weight: 800;
      color: #A0A5B5;
      letter-spacing: 0.8px;
      text-transform: uppercase;
      z-index: 2;
    }

    /* РАСКЛАД ТАРО: 3 СЛОТА */
    .tarot-three-slots-row {
      display: flex;
      justify-content: center;
      gap: 12px;
      margin-top: 16px;
      width: 100%;
    }

    .tarot-slot-box {
      width: 76px;
      height: 122px;
      border-radius: 14px;
      border: 1.5px dashed rgba(138, 99, 255, 0.35);
      background: rgba(25, 22, 38, 0.4);
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.25s ease;
      cursor: pointer;
      position: relative;
    }

    .tarot-slot-box.active {
      border: 2px dashed #F7B64D;
      background: rgba(247, 182, 77, 0.08);
      box-shadow: 0 0 16px rgba(247, 182, 77, 0.25);
    }

    .tarot-slot-box img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      border-radius: 12px;
    }

    .tarot-slot-arrow-indicator {
      display: flex;
      flex-direction: column;
      align-items: center;
      margin-top: 12px;
      gap: 4px;
      color: #F7B64D;
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 0.3px;
    }

    .tarot-toolbar-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      width: 100%;
      padding: 0 4px;
    }

    .tarot-round-tool-btn {
      width: 38px;
      height: 38px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.08);
      display: flex;
      align-items: center;
      justify-content: center;
      color: #FFF;
      font-size: 14px;
      cursor: pointer;
      transition: background 0.15s ease;
    }

    .tarot-round-tool-btn:active {
      background: rgba(255, 255, 255, 0.15);
    }

    .tarot-layout-selector-pill {
      display: flex;
      align-items: center;
      background: rgba(255, 255, 255, 0.08);
      border-radius: 18px;
      padding: 3px 6px;
      gap: 4px;
    }

    .tarot-layout-btn {
      padding: 4px 10px;
      border-radius: 14px;
      font-size: 12px;
      color: #A0A0B0;
      cursor: pointer;
      transition: all 0.15s ease;
    }

    .tarot-layout-btn.active {
      background: rgba(255, 255, 255, 0.18);
      color: #FFF;
      font-weight: 700;
    }
"""

if "/* СТИКИ-ХЕДЕР КАЛЕНДАРЯ" not in html:
    html = html.replace("/* Интерактивная колода Таро на радиусе", new_css + "\n    /* Интерактивная колода Таро на радиусе")

# 2. Update calendar header to be sticky in HTML
html = html.replace(
    '<div class="calendar-header-row">',
    '<div class="calendar-sticky-header"><div class="calendar-header-row">'
)
# And close it after calendar-full-view-btn
html = re.sub(
    r'(<span class="calendar-full-view-month" id="calendar-month-label">ОКТ</span>\s*</div>\s*</div>)',
    r'\1</div>',
    html
)

print("CSS and Header updated successfully!")
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(html)
