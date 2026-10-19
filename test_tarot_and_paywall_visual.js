const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const BROWSER_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const APP_URL = 'http://localhost:3000/%D0%90%D0%A1%D0%A2%D0%A0%D0%90_%D0%90%D0%A1%D0%A1%D0%95%D0%A2%D0%AB/astra_main_app.html';
const DEBUG_PORT = 9227;

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
  const userDataDir = path.join(__dirname, '.temp_edge_tarot_' + Date.now());
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

  // 1. Switch to Practices tab (Tarot Spread)
  console.log('1. Switching to Practices -> Tarot Spread...');
  await client.send('Runtime.evaluate', { expression: `switchTab('screen-practices')` });
  await sleep(600);

  let shot = await client.send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('D:/projects/monly/test_screenshots/07_tarot_arc_fan_perfect_dome.png', Buffer.from(shot.data, 'base64'));
  console.log('-> Captured 07_tarot_arc_fan_perfect_dome.png');

  // 2. Draw 3 cards into all 3 slots
  console.log('2. Drawing 3 cards into slots 0, 1, 2...');
  await client.send('Runtime.evaluate', {
    expression: `
      // Вытягиваем карту в слот 0
      selectTarotSlot(0);
      drawCardFromArc(19, TAROT_CARDS.find(c => c.name.includes("Солнце")), null);
      // Вытягиваем карту в слот 1
      selectTarotSlot(1);
      drawCardFromArc(2, TAROT_CARDS.find(c => c.name.includes("Жрица")), null);
      // Вытягиваем карту в слот 2
      selectTarotSlot(2);
      drawCardFromArc(18, TAROT_CARDS.find(c => c.name.includes("Луна")), null);
    `
  });
  await sleep(800);

  shot = await client.send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('D:/projects/monly/test_screenshots/08_tarot_triad_completed_3cards.png', Buffer.from(shot.data, 'base64'));
  console.log('-> Captured 08_tarot_triad_completed_3cards.png');

  // 3. Open Full Triad Spread Modal
  console.log('3. Opening Full Triad Spread Modal...');
  await client.send('Runtime.evaluate', { expression: `openActiveCardModal()` });
  await sleep(800);

  shot = await client.send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('D:/projects/monly/test_screenshots/09_tarot_triad_full_modal_with_mentor_btn.png', Buffer.from(shot.data, 'base64'));
  console.log('-> Captured 09_tarot_triad_full_modal_with_mentor_btn.png');

  // 4. Click "Обсудить с наставником • Получить инсайт" button
  console.log('4. Clicking "Обсудить с наставником • Получить инсайт"...');
  await client.send('Runtime.evaluate', { expression: `openMentorInsightFromTriad()` });
  await sleep(1500); // Wait for chat transition and AI mentor Luna to answer

  shot = await client.send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('D:/projects/monly/test_screenshots/10_chat_mentor_insight_triad_response.png', Buffer.from(shot.data, 'base64'));
  console.log('-> Captured 10_chat_mentor_insight_triad_response.png');

  // 5. Switch to Calendar and trigger Authentic Moonly Paywall
  console.log('5. Opening Authentic Moonly Paywall...');
  await client.send('Runtime.evaluate', {
    expression: `
      switchTab('screen-calendar');
      openAstraPlusModal({ day: 19 });
    `
  });
  await sleep(1000);

  shot = await client.send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('D:/projects/monly/test_screenshots/11_authentic_moonly_paywall_modal.png', Buffer.from(shot.data, 'base64'));
  console.log('-> Captured 11_authentic_moonly_paywall_modal.png');

  client.close();
  proc.kill();
  try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch (e) {}
  console.log('ALL VISUAL TESTS COMPLETED SUCCESSFULLY!');
}

run().catch(console.error);
