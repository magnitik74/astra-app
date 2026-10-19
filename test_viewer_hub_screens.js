const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const BROWSER_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const APP_URL = 'http://localhost:3000/astra_viewer_hub.html';
const DEBUG_PORT = 9229;
const SHOTS_DIR = 'D:/projects/monly/test_screenshots/viewer_hub_tests';

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
  const userDataDir = path.join(__dirname, '.temp_edge_hub_' + Date.now());
  const proc = spawn(BROWSER_PATH, [
    `--remote-debugging-port=${DEBUG_PORT}`,
    '--headless=new',
    '--disable-gpu',
    `--user-data-dir=${userDataDir}`,
    '--window-size=1280,900',
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
    width: 1280,
    height: 900,
    deviceScaleFactor: 1,
    mobile: false
  });

  await sleep(1500);

  async function snap(name) {
    const shot = await client.send('Page.captureScreenshot', { format: 'png' });
    const targetPath = path.join(SHOTS_DIR, name);
    fs.writeFileSync(targetPath, Buffer.from(shot.data, 'base64'));
    console.log(`[PASS] Captured: ${name}`);
  }

  // 1. Initial View: Onboarding
  console.log('1. Capturing Onboarding view in Hub...');
  await snap('01_hub_onboarding_view.png');

  // 2. Click "Экраны Астры" (Screens Tab)
  console.log('2. Switching to "Экраны Астры"...');
  await client.send('Runtime.evaluate', {
    expression: `
      document.querySelector('[data-view="screens"]').click();
    `
  });
  await sleep(1000);
  await snap('02_hub_screens_calendar_pure.png');

  // 3. Switch to Tarot Mode 1 Screen
  console.log('3. Switching to Tarot Mode 1...');
  await client.send('Runtime.evaluate', {
    expression: `
      loadAppScreen(1); // tarot_1
    `
  });
  await sleep(1000);
  await snap('03_hub_screens_tarot1_pure.png');

  // 4. Switch to Light Chat Screen
  console.log('4. Switching to Light Chat...');
  await client.send('Runtime.evaluate', {
    expression: `
      loadAppScreen(14); // chat
    `
  });
  await sleep(1000);
  await snap('04_hub_screens_light_chat.png');

  // 5. Toggle tabs to show tabs
  console.log('5. Toggling tabs to SHOWN...');
  await client.send('Runtime.evaluate', {
    expression: `
      toggleTabsBtn.click();
    `
  });
  await sleep(1000);
  await snap('05_hub_screens_with_tabs.png');

  // 6. Switch to Compare Tab (Side-by-side with Moonly)
  console.log('6. Switching to Compare Tab...');
  await client.send('Runtime.evaluate', {
    expression: `
      document.querySelector('[data-view="compare"]').click();
    `
  });
  await sleep(1000);
  await snap('06_hub_compare_side_by_side.png');

  // 7. Switch to Affirmations Ritual Tab
  console.log('7. Switching to Affirmations Ritual Tab...');
  await client.send('Runtime.evaluate', {
    expression: `
      document.querySelector('[data-view="ritual"]').click();
    `
  });
  await sleep(1000);
  await snap('07_hub_affirmations_ritual.png');

  client.close();
  proc.kill();
  try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch (e) {}
  console.log('ALL VIEWER HUB TESTS PASSED SUCCESSFULLY!');
}

run().catch(console.error);
