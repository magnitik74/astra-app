const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const BROWSER_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const APP_URL = 'http://localhost:3000/moonly_original_assets_gallery.html';
const DEBUG_PORT = 9230;

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

async function run() {
  const userDataDir = path.join(__dirname, '.temp_edge_gal_' + Date.now());
  const proc = spawn(BROWSER_PATH, [
    `--remote-debugging-port=${DEBUG_PORT}`,
    '--headless=new',
    '--disable-gpu',
    `--user-data-dir=${userDataDir}`,
    '--window-size=1280,900',
    APP_URL
  ]);

  for (let i = 0; i < 30; i++) {
    try {
      const res = await fetch(`http://127.0.0.1:${DEBUG_PORT}/json/version`);
      if (res.ok) break;
    } catch (e) {}
    await sleep(300);
  }

  const listRes = await fetch(`http://127.0.0.1:${DEBUG_PORT}/json/list`);
  const pages = await listRes.json();
  const pageTarget = pages.find(p => p.type === 'page');

  const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);
  await new Promise(r => ws.onopen = r);

  let id = 1;
  const send = (method, params = {}) => new Promise((resolve) => {
    const curId = id++;
    const handler = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.id === curId) {
        ws.removeEventListener('message', handler);
        resolve(msg.result);
      }
    };
    ws.addEventListener('message', handler);
    ws.send(JSON.stringify({ id: curId, method, params }));
  });

  await sleep(2500);

  const shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('D:/projects/monly/test_screenshots/12_moonly_original_assets_gallery.png', Buffer.from(shot.data, 'base64'));
  console.log('Saved 12_moonly_original_assets_gallery.png');

  ws.close();
  proc.kill();
  try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch (e) {}
}

run().catch(console.error);
