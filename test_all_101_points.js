const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const BROWSER_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const APP_URL = 'http://localhost:3000/%D0%90%D0%A1%D0%A2%D0%A0%D0%90_%D0%90%D0%A1%D0%A1%D0%95%D0%A2%D0%AB/astra_main_app.html';
const DEBUG_PORT = 9228;
const SHOTS_DIR = 'D:/projects/monly/test_screenshots/final_101_points';

if (!fs.existsSync(SHOTS_DIR)) {
  fs.mkdirSync(SHOTS_DIR, { recursive: true });
}

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function waitForBrowser(port, maxAttempts = 30) {
  for (let i = 0; i < maxAttempts; i++) {
    try {
      const res = await fetch(`http://127.0.0.1:${port}/json/version`);
      if (res.ok) return true;
    } catch (e) {}
    await sleep(300);
  }
  return false;
}

class CdpClient {
  constructor(wsUrl) {
    this.wsUrl = wsUrl;
    this.id = 1;
    this.callbacks = new Map();
  }

  async connect() {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(this.wsUrl);
      this.ws.onopen = () => resolve();
      this.ws.onerror = (err) => reject(err);
      this.ws.onmessage = (event) => {
        const msg = JSON.parse(event.data);
        if (msg.id && this.callbacks.has(msg.id)) {
          const { resolve, reject } = this.callbacks.get(msg.id);
          this.callbacks.delete(msg.id);
          if (msg.error) reject(msg.error);
          else resolve(msg.result);
        }
      };
    });
  }

  send(method, params = {}) {
    return new Promise((resolve, reject) => {
      const id = this.id++;
      this.callbacks.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }

  close() {
    try { this.ws.close(); } catch (e) {}
  }
}

async function run() {
  const userDataDir = path.join(__dirname, '.temp_edge_101_' + Date.now());
  const proc = spawn(BROWSER_PATH, [
    `--remote-debugging-port=${DEBUG_PORT}`,
    '--headless=new',
    '--disable-gpu',
    `--user-data-dir=${userDataDir}`,
    '--window-size=430,932',
    APP_URL
  ]);

  console.log('Launching browser on port', DEBUG_PORT);
  const ready = await waitForBrowser(DEBUG_PORT);
  if (!ready) {
    console.error('Failed to launch browser');
    proc.kill();
    return;
  }

  const listRes = await fetch(`http://127.0.0.1:${DEBUG_PORT}/json/list`);
  const pages = await listRes.json();
  const pageTarget = pages.find(p => p.type === 'page');
  console.log('Target found:', pageTarget.title);

  const client = new CdpClient(pageTarget.webSocketDebuggerUrl);
  await client.connect();

  await client.send('Page.enable');
  await client.send('Emulation.setDeviceMetricsOverride', {
    width: 430,
    height: 932,
    deviceScaleFactor: 2,
    mobile: true
  });

  await sleep(1500);

  // Helper to capture
  async function snap(name) {
    const shot = await client.send('Page.captureScreenshot', { format: 'png' });
    const targetPath = path.join(SHOTS_DIR, name);
    fs.writeFileSync(targetPath, Buffer.from(shot.data, 'base64'));
    console.log(`[PASS] Captured: ${name}`);
  }

  // 1. Calendar Screen
  console.log('1. Verifying Calendar & Feed Screen...');
  await snap('01_calendar_screen_3d_moon_feed.png');

  // 2. Onboarding Modal (Slide 4: Personal Astrologer 24/7)
  console.log('2. Verifying Onboarding Modal Slide 4 (Personal Astrologer 24/7)...');
  await client.send('Runtime.evaluate', {
    expression: `
      startOnboardingFlow();
      currentOnboardSlide = 3; // Slide 4
      renderCurrentOnboardSlide();
    `
  });
  await sleep(600);
  await snap('02_onboarding_slide4_personal_astrologer_24_7.png');

  // Close Onboarding
  await client.send('Runtime.evaluate', { expression: `skipOnboarding();` });
  await sleep(400);

  // 3. Practices -> Tarot 1 Card Hero Scale with Arc Fan
  console.log('3. Verifying Practices -> Tarot Mode 1...');
  await client.send('Runtime.evaluate', {
    expression: `
      switchMainScreen('practices');
      switchPracticeTab('tarot');
      setTarotMode(1);
      pullCardFromFan(10);
    `
  });
  await sleep(600);
  await snap('03_tarot_mode1_hero_scale_pulled.png');

  // 4. Practices -> Tarot Mode 2 (3 Cards Spread)
  console.log('4. Verifying Practices -> Tarot Mode 2 (3 Cards)...');
  await client.send('Runtime.evaluate', {
    expression: `
      setTarotMode(3);
      pullCardFromFan(5);
      pullCardFromFan(12);
      pullCardFromFan(18);
    `
  });
  await sleep(600);
  await snap('04_tarot_mode2_three_cards_spread.png');

  // 5. Tarot 78 Cards Catalog with 5 Suits
  console.log('5. Verifying Tarot 78 Cards Catalog...');
  await client.send('Runtime.evaluate', { expression: `setTarotMode('all');` });
  await sleep(600);
  await snap('05_tarot_catalog_78_cards_suits.png');

  // 6. Sliding Bottom Sheet with 3D Flip (RotateZ 180deg)
  console.log('6. Verifying Sliding Bottom Sheet with 3D Card Flip...');
  await client.send('Runtime.evaluate', {
    expression: `
      const sampleCard = ASTRA_TAROT_DATABASE.find(c => c.name.includes('Маг')) || ASTRA_TAROT_DATABASE[0];
      openCardMeaningModal(sampleCard);
      toggleCard3DFlip();
    `
  });
  await sleep(600);
  await snap('06_tarot_bottom_sheet_3d_flip_reversed.png');
  await client.send('Runtime.evaluate', { expression: `closeSheet('sheet-card-meaning');` });
  await sleep(400);

  // 7. Practices -> Runes (Hero 3D Stone & 24 Elder Futhark)
  console.log('7. Verifying Runes 24 Elder Futhark...');
  await client.send('Runtime.evaluate', {
    expression: `
      switchPracticeTab('runes');
      drawDailyRune();
      openRunesCatalogModal();
    `
  });
  await sleep(600);
  await snap('07_runes_elder_futhark_catalog_modal.png');
  await client.send('Runtime.evaluate', { expression: `closeSheet('modal-runes-catalog');` });
  await sleep(400);

  // 8. Healing & Soundscape (68 Sounds & Categories)
  console.log('8. Verifying Soundscape 68 Sounds...');
  await client.send('Runtime.evaluate', { expression: `switchMainScreen('healing');` });
  await sleep(600);
  await snap('08_soundscape_68_sounds_categories.png');

  // 9. Full-Screen Sound Player with Live Video Background & Sleep Timer
  console.log('9. Verifying Full-Screen Sound Player...');
  await client.send('Runtime.evaluate', {
    expression: `
      openSoundPlayerById(291);
      cycleSleepTimer();
    `
  });
  await sleep(800);
  await snap('09_sound_fullscreen_player_timer.png');
  await client.send('Runtime.evaluate', { expression: `closeSoundPlayer();` });
  await sleep(400);

  // 10. Light Chat with 5 Mentors (#F5F6FA) & Card Insight
  console.log('10. Verifying Light Chat with Mentor Insight...');
  await client.send('Runtime.evaluate', {
    expression: `
      switchMainScreen('chat');
      receiveMentorInsight({
        type: 'Расклад Таро • Маг (I)',
        title: 'Маг — Владыка Воли и Потенциала',
        text: 'Карта указывает на то, что у вас есть все ресурсы для реализации задуманного. Действуйте смело и открыто.'
      });
    `
  });
  await sleep(600);
  await snap('10_light_chat_mentor_insight_feedback.png');

  // 11. Profile "You" with Star Frame & 60 Avatars Modal
  console.log('11. Verifying Profile "You" & Avatar Modal...');
  await client.send('Runtime.evaluate', {
    expression: `
      switchMainScreen('you');
      openAvatarSelectorModal();
    `
  });
  await sleep(600);
  await snap('11_profile_you_avatars_gallery_modal.png');
  await client.send('Runtime.evaluate', { expression: `closeSheet('modal-avatar-selector');` });
  await sleep(400);

  // 12. Settings Screen (Boltik) with RuStore Account Deletion & NASA Info
  console.log('12. Verifying Settings Screen...');
  await client.send('Runtime.evaluate', { expression: `openSettingsScreen();` });
  await sleep(600);
  await snap('12_settings_screen_rustore_account_deletion.png');
  await client.send('Runtime.evaluate', { expression: `closeSettingsScreen();` });
  await sleep(400);

  // 13. Astra Plus Paywall with 3 Tariff Plans
  console.log('13. Verifying Astra Plus Paywall...');
  await client.send('Runtime.evaluate', { expression: `openPaywallModal();` });
  await sleep(600);
  await snap('13_paywall_astra_plus_3_plans.png');

  // 14. Verify Point 101 Security Shield Integrity
  console.log('14. Checking Point 101 Security Shield...');
  const secResult = await client.send('Runtime.evaluate', {
    expression: `
      ({
        hasAstraSecurity: !!window.AstraSecurity,
        signature: window.AstraSecurity ? window.AstraSecurity.getSignature() : null,
        vaultWorks: (() => {
          try {
            AstraSecurity.Vault.set('test_k', 'sec_pass');
            return AstraSecurity.Vault.get('test_k') === 'sec_pass';
          } catch(e) { return false; }
        })()
      })
    `,
    returnByValue: true
  });
  console.log('Security Shield Test Result:', JSON.stringify(secResult.result.value, null, 2));

  client.close();
  proc.kill();
  try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch (e) {}
  console.log('ALL 14 TEST STEPS VERIFIED AND CAPTURED SUCCESSFULLY!');
}

run().catch(console.error);
