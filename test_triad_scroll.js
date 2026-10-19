const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const BROWSER_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const APP_URL = 'http://localhost:3000/%D0%90%D0%A1%D0%A2%D0%A0%D0%90_%D0%90%D0%A1%D0%A1%D0%95%D0%A2%D0%AB/astra_main_app.html';
const DEBUG_PORT = 9228;

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
  const userDataDir = path.join(__dirname, '.temp_edge_tarot_scroll_' + Date.now());
  const proc = spawn(BROWSER_PATH, [
    `--remote-debugging-port=${DEBUG_PORT}`,
    '--headless=new',
    '--disable-gpu',
    `--user-data-dir=${userDataDir}`,
    '--window-size=430,932',
    APP_URL
  ]);

  const ready = await waitForBrowser(DEBUG_PORT);
  if (!ready) {
    console.error('Failed to launch browser');
    proc.kill();
    return;
  }

  const listRes = await fetch(`http://127.0.0.1:${DEBUG_PORT}/json/list`);
  const pages = await listRes.json();
  const pageTarget = pages.find(p => p.type === 'page');

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

  // Switch to Practices -> Tarot
  await client.send('Runtime.evaluate', { expression: `switchTab('screen-practices')` });
  await sleep(600);

  // Draw 3 cards
  await client.send('Runtime.evaluate', {
    expression: `
      selectTarotSlot(0);
      drawCardFromArc(19, TAROT_CARDS.find(c => c.name.includes("Солнце")), null);
      selectTarotSlot(1);
      drawCardFromArc(2, TAROT_CARDS.find(c => c.name.includes("Жрица")), null);
      selectTarotSlot(2);
      drawCardFromArc(18, TAROT_CARDS.find(c => c.name.includes("Луна")), null);
      openActiveCardModal();
    `
  });
  await sleep(800);

  // Scroll modal sheet down to show the Mentor CTA button
  await client.send('Runtime.evaluate', {
    expression: `
      const modal = document.getElementById('universal-modal');
      if (modal) modal.scrollTop = 480;
    `
  });
  await sleep(600);

  const shot = await client.send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('D:/projects/monly/test_screenshots/09b_tarot_triad_modal_bottom_mentor_btn.png', Buffer.from(shot.data, 'base64'));
  console.log('Captured 09b_tarot_triad_modal_bottom_mentor_btn.png');

  client.close();
  proc.kill();
  try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch (e) {}
}

run().catch(console.error);
