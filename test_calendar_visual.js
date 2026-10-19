const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const http = require('http');

const BROWSER_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const APP_URL = 'http://localhost:3000/%D0%90%D0%A1%D0%A2%D0%A0%D0%90_%D0%90%D0%A1%D0%A1%D0%95%D0%A2%D0%AB/astra_main_app.html';
const DEBUG_PORT = 9225;

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
    const id = this.id++;
    return new Promise((resolve, reject) => {
      this.callbacks.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }

  async eval(expr) {
    const res = await this.send('Runtime.evaluate', {
      expression: expr,
      returnByValue: true,
      awaitPromise: true
    });
    if (res.exceptionDetails) {
      throw new Error(res.exceptionDetails.text || 'Eval error');
    }
    return res.result ? res.result.value : undefined;
  }

  async screenshot(outputPath) {
    const res = await this.send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(outputPath, Buffer.from(res.data, 'base64'));
  }

  close() {
    try { this.ws.close(); } catch (e) {}
  }
}

(async () => {
  console.log('--- Launching Edge CDP for Calendar Verification ---');
  const browserProc = spawn(BROWSER_PATH, [
    `--remote-debugging-port=${DEBUG_PORT}`,
    '--headless=new',
    '--disable-gpu',
    '--no-first-run',
    '--no-default-browser-check',
    '--user-data-dir=' + path.join(__dirname, 'edge_cal_profile')
  ]);

  const ready = await waitForBrowser(DEBUG_PORT);
  if (!ready) {
    console.error('Browser failed to start debug port');
    process.exit(1);
  }

  const listRes = await fetch(`http://127.0.0.1:${DEBUG_PORT}/json/list`);
  const pages = await listRes.json();
  const pageTarget = pages.find(p => p.type === 'page') || pages[0];

  const cdp = new CdpClient(pageTarget.webSocketDebuggerUrl);
  await cdp.connect();

  await cdp.send('Page.enable');
  await cdp.send('DOM.enable');
  await cdp.send('Runtime.enable');

  // Set mobile iPhone 14 Pro viewport: 430 x 932
  await cdp.send('Emulation.setDeviceMetricsOverride', {
    width: 430,
    height: 932,
    deviceScaleFactor: 2,
    mobile: true
  });

  console.log('Navigating to app URL:', APP_URL);
  await cdp.send('Page.navigate', { url: APP_URL });
  await sleep(2000);

  // 1. Inspect day items
  const dayItemsInfo = await cdp.eval(`(() => {
    const items = document.querySelectorAll('.day-scroll-item');
    return Array.from(items).slice(0, 10).map((it, idx) => ({
      dayNum: it.querySelector('.day-scroll-num').innerText,
      weekday: it.querySelector('.day-scroll-weekday').innerText,
      moonSrc: it.querySelector('.day-scroll-moon').src,
      selected: it.classList.contains('selected'),
      isToday: it.classList.contains('is-today')
    }));
  })()`);

  console.log('Day items 1-10 audit:', JSON.stringify(dayItemsInfo, null, 2));

  // 2. Test drag to scroll simulation
  console.log('Testing Drag-To-Scroll...');
  const beforeScroll = await cdp.eval(`document.getElementById('calendar-days-track').scrollLeft`);
  console.log('Initial scrollLeft:', beforeScroll);

  // Simulate mouse drag
  await cdp.eval(`(() => {
    const track = document.getElementById('calendar-days-track');
    const rect = track.getBoundingClientRect();
    const startX = rect.left + 200;
    const startY = rect.top + 30;

    track.dispatchEvent(new MouseEvent('mousedown', { clientX: startX, clientY: startY, bubbles: true }));
    track.dispatchEvent(new MouseEvent('mousemove', { clientX: startX - 100, clientY: startY, bubbles: true }));
    window.dispatchEvent(new MouseEvent('mouseup', { clientX: startX - 100, clientY: startY, bubbles: true }));
  })()`);

  await sleep(300);
  const afterScroll = await cdp.eval(`document.getElementById('calendar-days-track').scrollLeft`);
  console.log('After Drag scrollLeft:', afterScroll);

  // 3. Test clicking day 2 and day 6
  console.log('Testing Click on Day 2...');
  await cdp.eval(`(() => {
    const day2 = document.querySelector('.day-scroll-item[data-day="2"]');
    if (day2) day2.click();
  })()`);
  await sleep(300);

  const day2Selected = await cdp.eval(`document.querySelector('.day-scroll-item[data-day="2"]').classList.contains('selected')`);
  console.log('Day 2 selected:', day2Selected);

  // 4. Capture screenshot of Day 2
  const outShotDay2 = path.join(__dirname, 'test_screenshots', 'cal_drag_day2_fixed.png');
  await cdp.screenshot(outShotDay2);
  console.log('Captured screenshot Day 2:', outShotDay2);

  // 5. Click Day 13 (today/full view)
  console.log('Testing Click on Day 13...');
  await cdp.eval(`(() => {
    const day13 = document.querySelector('.day-scroll-item[data-day="13"]');
    if (day13) day13.click();
  })()`);
  await sleep(300);

  const outShotDay13 = path.join(__dirname, 'test_screenshots', 'cal_moonly_authentic_header.png');
  await cdp.screenshot(outShotDay13);
  console.log('Captured screenshot Day 13:', outShotDay13);

  // 6. Test Day 6 at scroll 0 (exact match to user feedback screenshot)
  console.log('Testing Click on Day 6 with scrollLeft = 0...');
  await cdp.eval(`(() => {
    const track = document.getElementById('calendar-days-track');
    const day6 = document.querySelector('.day-scroll-item[data-day="6"]');
    if (day6) day6.click();
    track.scrollLeft = 0;
  })()`);
  await sleep(400);

  const outShotDay6 = path.join(__dirname, 'test_screenshots', 'cal_user_comparison_day6.png');
  await cdp.screenshot(outShotDay6);
  console.log('Captured screenshot Day 6 comparison:', outShotDay6);

  cdp.close();
  browserProc.kill();
  console.log('Test complete!');
})();
