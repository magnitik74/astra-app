const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const BROWSER_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const APP_URL = 'http://localhost:3000/%D0%90%D0%A1%D0%A2%D0%A0%D0%90_%D0%90%D0%A1%D0%A1%D0%95%D0%A2%D0%AB/astra_main_app.html';
const DEBUG_PORT = 9226;

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
  const userDataDir = path.join(__dirname, '.temp_edge_video_' + Date.now());
  const proc = spawn(BROWSER_PATH, [
    `--remote-debugging-port=${DEBUG_PORT}`,
    '--headless=new',
    '--disable-gpu',
    `--user-data-dir=${userDataDir}`,
    '--window-size=430,932',
    APP_URL
  ]);

  console.log('Launching Edge on port', DEBUG_PORT);
  const ready = await waitForBrowser(DEBUG_PORT);
  if (!ready) {
    console.error('Failed to launch browser');
    proc.kill();
    return;
  }

  const listRes = await fetch(`http://127.0.0.1:${DEBUG_PORT}/json/list`);
  const pages = await listRes.json();
  const pageTarget = pages.find(p => p.type === 'page');
  console.log('Connected to target:', pageTarget.title);

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

  // 1. Screenshot of Day 18 with Cat Art and authentic Moonly feed
  let shot = await client.send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('D:/projects/monly/test_screenshots/01_main_feed_day18_cat.png', Buffer.from(shot.data, 'base64'));
  console.log('1. Captured 01_main_feed_day18_cat.png');

  // 2. Open Card 1 (Day 18 Horoscope Modal with Spheres)
  await client.send('Runtime.evaluate', { expression: `document.querySelector('.calendar-card-for-you').click()` });
  await sleep(800);
  shot = await client.send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('D:/projects/monly/test_screenshots/02_horoscope_modal_spheres.png', Buffer.from(shot.data, 'base64'));
  console.log('2. Captured 02_horoscope_modal_spheres.png');

  // Close modal
  await client.send('Runtime.evaluate', { expression: `closeUniversalModal()` });
  await sleep(400);

  // 3. Click Day 19 to trigger Astra Plus Paywall Modal
  await client.send('Runtime.evaluate', {
    expression: `
      const d19 = document.querySelector('.day-scroll-item[data-date-key="2026-10-19"]');
      if (d19) d19.click();
    `
  });
  await sleep(800);
  shot = await client.send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('D:/projects/monly/test_screenshots/03_astra_plus_paywall_modal.png', Buffer.from(shot.data, 'base64'));
  console.log('3. Captured 03_astra_plus_paywall_modal.png');

  // Close paywall
  await client.send('Runtime.evaluate', { expression: `closeUniversalModal()` });
  await sleep(400);

  // 4. Scroll calendar track into November and update month tag
  await client.send('Runtime.evaluate', {
    expression: `
      const track = document.getElementById('calendar-days-track');
      track.scrollLeft = 1400;
      updateActiveMonthLabel(track);
    `
  });
  await sleep(600);
  shot = await client.send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('D:/projects/monly/test_screenshots/04_calendar_scroll_november.png', Buffer.from(shot.data, 'base64'));
  console.log('4. Captured 04_calendar_scroll_november.png');

  // 5. Switch to Practices tab (Tarot Three Slots + Radial Arc Fan)
  await client.send('Runtime.evaluate', { expression: `switchTab('screen-practices')` });
  await sleep(800);
  shot = await client.send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('D:/projects/monly/test_screenshots/05_tarot_three_slots_arc_fan.png', Buffer.from(shot.data, 'base64'));
  console.log('5. Captured 05_tarot_three_slots_arc_fan.png');

  // 6. Draw card into Slot 0 from Arc
  await client.send('Runtime.evaluate', {
    expression: `
      const firstCard = document.querySelector('.spread-arc-card');
      if (firstCard) firstCard.click();
    `
  });
  await sleep(800);
  shot = await client.send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('D:/projects/monly/test_screenshots/06_tarot_card_drawn.png', Buffer.from(shot.data, 'base64'));
  console.log('6. Captured 06_tarot_card_drawn.png');

  client.close();
  proc.kill();
  try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch (e) {}
  console.log('Visual test suite completed successfully!');
}

run().catch(console.error);
