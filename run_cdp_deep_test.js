const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const BROWSER_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const APP_URL = 'http://localhost:3000/%D0%90%D0%A1%D0%A2%D0%A0%D0%90_%D0%90%D0%A1%D0%A1%D0%95%D0%A2%D0%AB/astra_main_app.html';
const SCREENSHOT_DIR = 'D:/projects/monly/test_screenshots';
const DEBUG_PORT = 9223;

const auditReport = {
  timestamp: new Date().toISOString(),
  environment: {
    browser: 'Microsoft Edge Chromium Headless (CDP)',
    viewport: { width: 430, height: 932, deviceScaleFactor: 2 },
    targetUrl: APP_URL
  },
  tests: [],
  consoleLogs: [],
  exceptions: [],
  networkErrors: [],
  screenshots: []
};

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function waitForBrowser(port, maxAttempts = 30) {
  for (let i = 0; i < maxAttempts; i++) {
    try {
      const res = await fetch(`http://127.0.0.1:${port}/json/version`);
      if (res.ok) {
        return true;
      }
    } catch (e) {
      // not ready yet
    }
    await sleep(300);
  }
  return false;
}

class CdpClient {
  constructor(wsUrl) {
    this.wsUrl = wsUrl;
    this.ws = null;
    this.msgId = 1;
    this.pending = new Map();
    this.handlers = new Map();
  }

  async connect() {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(this.wsUrl);
      this.ws.onopen = () => resolve();
      this.ws.onerror = (err) => reject(err);
      this.ws.onmessage = (event) => {
        const msg = JSON.parse(event.data);
        if (msg.id && this.pending.has(msg.id)) {
          const { resolve, reject } = this.pending.get(msg.id);
          this.pending.delete(msg.id);
          if (msg.error) {
            reject(new Error(msg.error.message || JSON.stringify(msg.error)));
          } else {
            resolve(msg.result);
          }
        } else if (msg.method) {
          const cbs = this.handlers.get(msg.method) || [];
          cbs.forEach(cb => cb(msg.params));
        }
      };
    });
  }

  send(method, params = {}) {
    const id = this.msgId++;
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }

  on(method, cb) {
    if (!this.handlers.has(method)) {
      this.handlers.set(method, []);
    }
    this.handlers.get(method).push(cb);
  }

  async evaluate(fnOrExpr) {
    const expression = typeof fnOrExpr === 'function' ? `(${fnOrExpr.toString()})()` : fnOrExpr;
    const res = await this.send('Runtime.evaluate', {
      expression,
      returnByValue: true,
      awaitPromise: true
    });
    if (res.exceptionDetails) {
      const err = res.exceptionDetails.exception?.description || res.exceptionDetails.text;
      auditReport.exceptions.push(err);
      throw new Error(err);
    }
    return res.result?.value;
  }

  async takeScreenshot(filename) {
    const res = await this.send('Page.captureScreenshot', { format: 'png' });
    const buffer = Buffer.from(res.data, 'base64');
    const fullPath = path.join(SCREENSHOT_DIR, filename);
    fs.writeFileSync(fullPath, buffer);
    auditReport.screenshots.push({ filename, path: fullPath, size: buffer.length });
    console.log(`  [Скриншот] Сохранен: ${filename} (${(buffer.length / 1024).toFixed(1)} КБ)`);
    return fullPath;
  }

  close() {
    if (this.ws) {
      try { this.ws.close(); } catch(e){}
    }
  }
}

async function main() {
  console.log('================================================================');
  console.log('   АСТРА: ЗАПУСК ГЛУБОКОГО ИНТЕРАКТИВНОГО CDP-ТЕСТИРОВАНИЯ      ');
  console.log('================================================================');

  const userDataDir = 'C:\\temp\\browser_cdp_profile_' + Date.now();
  const browserProcess = spawn(BROWSER_PATH, [
    `--remote-debugging-port=${DEBUG_PORT}`,
    '--headless=new',
    '--window-size=430,932',
    '--disable-gpu',
    '--no-first-run',
    '--no-default-browser-check',
    `--user-data-dir=${userDataDir}`,
    'about:blank'
  ], { detached: false });

  browserProcess.on('error', (err) => {
    console.error('Ошибка запуска браузера:', err);
  });

  console.log('• Ожидание инициализации Chromium Debugger на порту ' + DEBUG_PORT + '...');
  const ready = await waitForBrowser(DEBUG_PORT);
  if (!ready) {
    console.error('Не удалось подключиться к порту ' + DEBUG_PORT);
    browserProcess.kill();
    process.exit(1);
  }
  console.log('• Chromium запущен и готов к CDP взаимодействию.');

  let client;
  try {
    const targetsRes = await fetch(`http://127.0.0.1:${DEBUG_PORT}/json`);
    const targets = await targetsRes.json();
    const pageTarget = targets.find(t => t.type === 'page') || targets[0];
    console.log('• Подключение к странице:', pageTarget.webSocketDebuggerUrl);

    client = new CdpClient(pageTarget.webSocketDebuggerUrl);
    await client.connect();

    // Enable domains
    await client.send('Page.enable');
    await client.send('Runtime.enable');
    await client.send('Network.enable');
    await client.send('DOM.enable');

    // Auto-handle JavaScript alerts
    client.on('Page.javascriptDialogOpening', async (params) => {
      console.log(`  [Auto-dismissing alert]: "${params.message}"`);
      await client.send('Page.handleJavaScriptDialog', { accept: true });
    });

    // Override window.alert before any scripts run
    await client.send('Page.addScriptToEvaluateOnNewDocument', {
      source: `
        window.alert = function(msg) {
          console.log('[window.alert intercepted]: ' + msg);
        };
      `
    });

    // Emulate iPhone 14 Pro Max screen
    await client.send('Emulation.setDeviceMetricsOverride', {
      width: 430,
      height: 932,
      deviceScaleFactor: 2,
      mobile: true
    });

    // Event listeners
    client.on('Runtime.consoleAPICalled', (params) => {
      const text = params.args.map(a => a.value || a.description || '').join(' ');
      auditReport.consoleLogs.push({ type: params.type, text });
      if (params.type === 'error') {
        console.log(`  [Console Error]: ${text}`);
      }
    });

    client.on('Runtime.exceptionThrown', (params) => {
      const desc = params.exceptionDetails?.exception?.description || params.exceptionDetails?.text;
      auditReport.exceptions.push(desc);
      console.log(`  [Uncaught JS Exception]: ${desc}`);
    });

    client.on('Network.responseReceived', (params) => {
      if (params.response.status >= 400 && !params.response.url.endsWith('favicon.ico')) {
        auditReport.networkErrors.push({
          url: params.response.url,
          status: params.response.status,
          statusText: params.response.statusText
        });
        console.log(`  [Network 4xx/5xx]: ${params.response.status} - ${params.response.url}`);
      }
    });

    // Navigate to app
    console.log(`• Загрузка приложения: ${APP_URL}`);
    await client.send('Page.navigate', { url: APP_URL });
    await sleep(2500); // Wait for initial render and scripts

    function recordTest(name, passed, details = '') {
      auditReport.tests.push({ name, passed, details });
      console.log(`[${passed ? 'PASS' : 'FAIL'}] ${name} ${details ? '(' + details + ')' : ''}`);
    }

    // -------------------------------------------------------------
    // TEST SUITE 1: CALENDAR SCREEN & INTERACTIONS
    // -------------------------------------------------------------
    console.log('\n--- ТЕСТ 1: ЭКРАН 1 «КАЛЕНДАРЬ» ---');
    const calScreenVisible = await client.evaluate(() => {
      const el = document.getElementById('screen-calendar');
      return el && window.getComputedStyle(el).display !== 'none';
    });
    recordTest('Календарь отображается по умолчанию', calScreenVisible);
    await client.takeScreenshot('01_screen_calendar_default.png');

    // Select Day 15 (Full Moon phase)
    await client.evaluate(() => { selectCalendarDay(15); });
    await sleep(400);
    const day15Status = await client.evaluate(() => {
      const moon = document.getElementById('calendar-moon-corner').src;
      const bg = document.getElementById('calendar-bg-img').src;
      return { moon, bg };
    });
    recordTest('Выбор 15-го лунного дня обновляет фазу луны и фон', day15Status.moon.includes('moon_15.png'), `Moon: ${day15Status.moon.split('/').pop()}, Bg: ${day15Status.bg.split('/').pop()}`);
    await client.takeScreenshot('02_calendar_day_15_selected.png');

    // Open Day Details Recommendation Modal
    await client.evaluate(() => { openDayDetailModal(); });
    await sleep(500);
    const dayModalOpen = await client.evaluate(() => {
      const m = document.getElementById('universal-modal');
      return m && m.style.display === 'flex' && m.innerText.includes('15-й Лунный день');
    });
    recordTest('Модальное окно рекомендаций дня открывается корректно', dayModalOpen);
    await client.takeScreenshot('03_modal_day_recommendations.png');

    // Close Modal
    await client.evaluate(() => { closeUniversalModal(); });
    await sleep(300);

    // Open Monthly 31-day Grid Modal
    await client.evaluate(() => { openMonthCalendarModal(); });
    await sleep(500);
    const monthModalOpen = await client.evaluate(() => {
      const m = document.getElementById('universal-modal');
      const hasTitle = m && m.innerText.includes('Октябрь 2026');
      const moonsCount = m ? m.querySelectorAll('img[src*="moon_"]').length : 0;
      return m && m.style.display === 'flex' && hasTitle && moonsCount >= 28;
    });
    recordTest('Модальный 31-дневный лунный календарь-сетка генерируется', monthModalOpen);
    await client.takeScreenshot('04_modal_monthly_calendar_grid.png');
    await client.evaluate(() => { closeUniversalModal(); });
    await sleep(300);

    // Open Dream Journal Modal
    await client.evaluate(() => { openDreamerModal(); });
    await sleep(500);
    const dreamModalOpen = await client.evaluate(() => {
      const m = document.getElementById('universal-modal');
      return m && m.style.display === 'flex' && document.getElementById('dream-text-input') !== null;
    });
    recordTest('Интерактивный Дневник Снов открывается с полем ввода', dreamModalOpen);
    await client.takeScreenshot('05_modal_dream_journal.png');

    // Test saving a dream entry
    await client.evaluate(() => {
      document.getElementById('dream-text-input').value = 'Я видел полет над золотым океаном в полнолуние.';
      saveDreamEntry();
    });
    await sleep(400);
    const savedDreamInStorage = await client.evaluate(() => {
      return localStorage.getItem('astra_dream_day_15');
    });
    recordTest('Сон успешно сохраняется в localStorage', !!savedDreamInStorage && savedDreamInStorage.includes('золотым океаном'));
    await client.evaluate(() => { closeUniversalModal(); });
    await sleep(300);

    // -------------------------------------------------------------
    // TEST SUITE 2: PRACTICES SCREEN (TAROT, RUNES, WISDOM)
    // -------------------------------------------------------------
    console.log('\n--- ТЕСТ 2: ЭКРАН 2 «ПРАКТИКИ» ---');
    await client.evaluate(() => { switchTab('screen-practices'); });
    await sleep(500);
    const practicesVisible = await client.evaluate(() => {
      const el = document.getElementById('screen-practices');
      return el && window.getComputedStyle(el).display !== 'none';
    });
    recordTest('Вкладка «Практики» активируется', practicesVisible);
    await client.takeScreenshot('06_screen_practices_main.png');

    // Draw Tarot Card in Spread
    await client.evaluate(() => { drawCardByDeckIndex(3); });
    await sleep(1000); // Wait for 3D flip animation
    const cardDrawn = await client.evaluate(() => {
      const res = document.getElementById('spread-result');
      const name = document.getElementById('res-card-name')?.innerText || '';
      return res && res.style.display !== 'none' && name.length > 0;
    });
    recordTest('Вытягивание карты Таро: 3D переворот и интерпретация', cardDrawn);
    await client.takeScreenshot('07_tarot_spread_card_drawn.png');

    // Open full card reading modal
    await client.evaluate(() => { openActiveCardModal(); });
    await sleep(500);
    const cardModalOpen = await client.evaluate(() => {
      const m = document.getElementById('universal-modal');
      return m && m.style.display === 'flex' && m.innerText.toLowerCase().includes('архетип');
    });
    recordTest('Модальное окно углубленного чтения карты Таро открывается', cardModalOpen);
    await client.takeScreenshot('08_modal_tarot_deep_reading.png');
    await client.evaluate(() => { closeUniversalModal(); });
    await sleep(300);

    // Reset Tarot Spread
    await client.evaluate(() => { resetTarotSpread(); });
    await sleep(400);
    const spreadReset = await client.evaluate(() => {
      const res = document.getElementById('spread-result');
      return res && res.style.display === 'none';
    });
    recordTest('Сброс расклада возвращает стол в исходное состояние', spreadReset);
    await client.takeScreenshot('09_tarot_spread_reset.png');

    // Toggle Tarot View to All 78 Cards
    await client.evaluate(() => { toggleTarotView('all'); });
    await sleep(500);
    const all78CardsRendered = await client.evaluate(() => {
      const cards = document.querySelectorAll('#tarot-grid-body .tarot-grid-item');
      return cards.length === 78;
    });
    recordTest('Каталог «Все 78 карт» отображает ровно 78 карт', all78CardsRendered);
    await client.takeScreenshot('10_tarot_catalog_all_78_cards.png');

    // Filter by Cups (Кубки = 14 карт)
    await client.evaluate(() => { filterTarotGrid('cups', null); });
    await sleep(300);
    const cupsCount = await client.evaluate(() => {
      return document.querySelectorAll('#tarot-grid-body .tarot-grid-item').length;
    });
    recordTest('Фильтр по масти «Кубки» отфильтровал 14 карт', cupsCount === 14, `Найдено: ${cupsCount}`);

    // Search for "Маг"
    await client.evaluate(() => {
      const input = document.getElementById('tarot-search-box');
      input.value = 'Маг';
      handleTarotSearch({ target: input });
    });
    await sleep(300);
    const magFound = await client.evaluate(() => {
      const items = document.querySelectorAll('#tarot-grid-body .tarot-grid-item');
      return items.length >= 1 && items[0].innerText.includes('Маг');
    });
    recordTest('Поиск по картам «Маг» находит карту', magFound);
    await client.takeScreenshot('11_tarot_filter_and_search.png');

    // Switch to Runes practice
    await client.evaluate(() => {
      const pills = document.querySelectorAll('.practice-main-tab-pill');
      switchPracticeSection('runes', pills[1]);
    });
    await sleep(500);
    const runesCount = await client.evaluate(() => {
      return document.querySelectorAll('#runes-grid-body .rune-item-card').length;
    });
    recordTest('Скандинавские руны: отображаются ровно 24 камня Старшего Футарка', runesCount === 24, `Найдено: ${runesCount}`);
    await client.takeScreenshot('12_practices_runes_grid.png');

    // Click Rune Fehu (index 0)
    await client.evaluate(() => { showRuneModal(0); });
    await sleep(500);
    const runeModalOpen = await client.evaluate(() => {
      const m = document.getElementById('universal-modal');
      return m && m.style.display === 'flex' && m.innerText.includes('Феху');
    });
    recordTest('Модальное окно толкования руны Феху открывается', runeModalOpen);
    await client.takeScreenshot('13_modal_rune_fehu.png');
    await client.evaluate(() => { closeUniversalModal(); });
    await sleep(300);

    // Switch to Wisdom Goddesses & Vedic Deities
    await client.evaluate(() => {
      const pills = document.querySelectorAll('.practice-main-tab-pill');
      switchPracticeSection('wisdom', pills[2]);
    });
    await sleep(500);
    const wisdomCount = await client.evaluate(() => {
      return document.querySelectorAll('#wisdom-grid-body .wisdom-item-card').length;
    });
    recordTest('Девы Мудрости & Божества: отображаются все 97 карт', wisdomCount === 97, `Найдено: ${wisdomCount}`);
    await client.takeScreenshot('14_practices_wisdom_grid.png');

    // Switch to Affirmations
    await client.evaluate(() => {
      const pills = document.querySelectorAll('.practice-main-tab-pill');
      switchPracticeSection('affirmations', pills[3]);
    });
    await sleep(500);
    const initialAffirmation = await client.evaluate(() => {
      return document.getElementById('active-affirmation-text').innerText;
    });
    await client.evaluate(() => { nextAffirmation(); });
    await sleep(300);
    const nextAff = await client.evaluate(() => {
      return document.getElementById('active-affirmation-text').innerText;
    });
    recordTest('Аффирмации: циклический генератор меняет цитату', initialAffirmation !== nextAff);
    await client.takeScreenshot('15_practices_affirmations.png');

    // -------------------------------------------------------------
    // TEST SUITE 3: HEALING SCREEN & AUDIO GENERATOR
    // -------------------------------------------------------------
    console.log('\n--- ТЕСТ 3: ЭКРАН 3 «ИСЦЕЛЕНИЕ» ---');
    await client.evaluate(() => { switchTab('screen-healing'); });
    await sleep(500);
    const healingVisible = await client.evaluate(() => {
      const el = document.getElementById('screen-healing');
      return el && window.getComputedStyle(el).display !== 'none';
    });
    recordTest('Вкладка «Исцеление» активна', healingVisible);

    // Change frequency to 528 Hz
    await client.evaluate(() => {
      const chips = document.querySelectorAll('.freq-selector-chip');
      setHealingFrequency(528, chips[1]);
    });
    await sleep(300);
    const freqActive = await client.evaluate(() => currentFrequency === 528);
    recordTest('Переключение целебной частоты на 528 Гц', freqActive);
    await client.takeScreenshot('16_screen_healing_mandala.png');

    // -------------------------------------------------------------
    // TEST SUITE 4: CHAT SCREEN & ASTROLOGICAL AI
    // -------------------------------------------------------------
    console.log('\n--- ТЕСТ 4: ЭКРАН 4 «ЧАТ С АСТРОЛОГОМ» ---');
    await client.evaluate(() => { switchTab('screen-chat'); });
    await sleep(500);
    const chatVisible = await client.evaluate(() => {
      const el = document.getElementById('screen-chat');
      return el && window.getComputedStyle(el).display !== 'none';
    });
    recordTest('Вкладка «Чат» активна с профилем Луны', chatVisible);
    await client.takeScreenshot('17_screen_chat_initial.png');

    // Click quick suggestion chip
    await client.evaluate(() => { sendQuickMessage('Что меня ждет в полнолуние?'); });
    await sleep(1800); // Wait for typing indicator and AI answer
    const messagesCount = await client.evaluate(() => {
      return document.querySelectorAll('#chat-messages > div').length;
    });
    recordTest('Интерактивный диалог: ответ ИИ-астролога сгенерирован', messagesCount >= 2, `Сообщений в чате: ${messagesCount}`);
    await client.takeScreenshot('18_screen_chat_ai_reply.png');

    // -------------------------------------------------------------
    // TEST SUITE 5: PROFILE ("ТЫ") SCREEN & VEDIC MODALS
    // -------------------------------------------------------------
    console.log('\n--- ТЕСТ 5: ЭКРАН 5 «ТЫ» (ПРОФИЛЬ И НАТАЛЬНЫЕ МАТРИЦЫ) ---');
    await client.evaluate(() => { switchTab('screen-you'); });
    await sleep(500);
    const youVisible = await client.evaluate(() => {
      const el = document.getElementById('screen-you');
      return el && window.getComputedStyle(el).display !== 'none';
    });
    recordTest('Вкладка «Ты» активна', youVisible);
    await client.takeScreenshot('19_screen_profile_main.png');

    // Open Avatar Selector Modal
    await client.evaluate(() => { openAvatarSelectorModal(); });
    await sleep(500);
    const avatarGridCount = await client.evaluate(() => {
      const m = document.getElementById('universal-modal');
      return m && m.style.display === 'flex' && m.querySelectorAll('.avatar-picker-cell').length >= 14;
    });
    recordTest('Модальный выбор аватара содержит 12 Зодиакальных Тотемов + Музу/Проводника', avatarGridCount);
    await client.takeScreenshot('20_modal_avatar_selector.png');

    // Select Scorpio Totem
    await client.evaluate(() => { setProfileAvatar('zodiac_08_Scorpio_journal_600.webp'); });
    await sleep(400);
    const profileAvatarUpdated = await client.evaluate(() => {
      return document.getElementById('profile-main-avatar').src.includes('zodiac_08_Scorpio');
    });
    recordTest('Выбор тотема Скорпиона обновил главное фото профиля в 216dp рамке', profileAvatarUpdated);
    await client.takeScreenshot('21_profile_avatar_scorpio_updated.png');

    // Open Birth Chart Modal
    await client.evaluate(() => { openBirthChartModal(); });
    await sleep(500);
    const birthChartOpen = await client.evaluate(() => {
      const m = document.getElementById('universal-modal');
      return m && m.style.display === 'flex' && m.innerText.includes('Асцендент') && m.innerText.includes('Скорпион');
    });
    recordTest('Модальная Натальная Карта (Джйотиш матрица) открывается', birthChartOpen);
    await client.takeScreenshot('22_modal_birth_chart.png');
    await client.evaluate(() => { closeUniversalModal(); });
    await sleep(300);

    // Open Compatibility Calculator Modal
    await client.evaluate(() => { openCompatibilityCalculatorModal(); });
    await sleep(500);
    const compModalOpen = await client.evaluate(() => {
      const m = document.getElementById('universal-modal');
      return m && m.style.display === 'flex' && m.innerText.includes('Синастри') && m.innerText.includes('85%');
    });
    recordTest('Модальный расчет Синастрии (Совместимость 85% по 6 сферам) отображается', compModalOpen);
    await client.takeScreenshot('23_modal_compatibility_synastry.png');
    await client.evaluate(() => { closeUniversalModal(); });
    await sleep(300);

    // Open 2026 Year Forecast Modal
    await client.evaluate(() => { openYearForecastModal(); });
    await sleep(500);
    const forecastOpen = await client.evaluate(() => {
      const m = document.getElementById('universal-modal');
      return m && m.style.display === 'flex' && m.innerText.includes('2026');
    });
    recordTest('Модальный Большой Прогноз на 2026 год открывается', forecastOpen);
    await client.takeScreenshot('24_modal_year_2026_forecast.png');
    await client.evaluate(() => { closeUniversalModal(); });
    await sleep(300);

    // -------------------------------------------------------------
    // TEST SUITE 6: LAYOUT FIDELITY & NO HORIZONTAL OVERFLOW
    // -------------------------------------------------------------
    console.log('\n--- ТЕСТ 6: ВЕРСТКА, АДАПТИВНОСТЬ И ОТСУТСТВИЕ ГОРИЗОНТАЛЬНОГО ПЕРЕПОЛНЕНИЯ ---');
    const layoutMetrics = await client.evaluate(() => {
      return {
        clientWidth: document.documentElement.clientWidth,
        scrollWidth: document.documentElement.scrollWidth,
        bodyClientWidth: document.body.clientWidth,
        bodyScrollWidth: document.body.scrollWidth,
        hasHorizontalOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth
      };
    });
    const noOverflow = !layoutMetrics.hasHorizontalOverflow;
    recordTest('Отсутствие горизонтального скролла (overflow-x leak) на мобильном экране', noOverflow, `scrollWidth: ${layoutMetrics.scrollWidth}px, clientWidth: ${layoutMetrics.clientWidth}px`);

    // -------------------------------------------------------------
    // FINAL HEALTH CHECK
    // -------------------------------------------------------------
    console.log('\n--- ИТОГОВЫЙ АНАЛИЗ ОШИБОК РАНТАЙМА ---');
    const totalExceptions = auditReport.exceptions.length;
    const totalConsoleErrors = auditReport.consoleLogs.filter(l => l.type === 'error').length;
    const totalNetwork4xx = auditReport.networkErrors.length;

    recordTest('0 неперехваченных исключений JavaScript (Uncaught Exceptions)', totalExceptions === 0, `Ошибок: ${totalExceptions}`);
    recordTest('0 фатальных ошибок в console.error', totalConsoleErrors === 0, `Ошибок: ${totalConsoleErrors}`);
    recordTest('0 сетевых ошибок HTTP 4xx/5xx', totalNetwork4xx === 0, `Ошибок: ${totalNetwork4xx}`);

    const allPassed = auditReport.tests.every(t => t.passed);
    console.log('\n================================================================');
    console.log(`ИТОГ CDP ТЕСТИРОВАНИЯ: ${allPassed ? 'ВСЕ ТЕСТЫ УСПЕШНО ПРОЙДЕНЫ (100% PASS)' : 'ОБНАРУЖЕНЫ СБОИ'}`);
    console.log(`Всего тестов: ${auditReport.tests.length}`);
    console.log(`Успешно:     ${auditReport.tests.filter(t => t.passed).length}`);
    console.log(`Провалено:   ${auditReport.tests.filter(t => !t.passed).length}`);
    console.log(`Скриншотов:  ${auditReport.screenshots.length}`);
    console.log('================================================================');

    fs.writeFileSync('D:/projects/monly/cdp_deep_audit_report.json', JSON.stringify(auditReport, null, 2));
    console.log('Подробный отчет записан в: D:/projects/monly/cdp_deep_audit_report.json');

  } catch (err) {
    console.error('Ошибка в ходе выполнения CDP тестов:', err);
  } finally {
    if (client) client.close();
    browserProcess.kill();
    console.log('Браузер процесс завершен.');
  }
}

main();
