const { spawn } = require('child_process');

const BROWSER_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const APP_URL = 'http://localhost:3000/%D0%90%D0%A1%D0%A2%D0%A0%D0%90_%D0%90%D0%A1%D0%A1%D0%95%D0%A2%D0%AB/astra_main_app.html';

const browser = spawn(BROWSER_PATH, [
  '--remote-debugging-port=9224',
  '--headless=new',
  '--window-size=430,932',
  '--disable-gpu',
  '--user-data-dir=C:\\temp\\edge_diag_' + Date.now(),
  APP_URL
]);

setTimeout(async () => {
  try {
    const targets = await (await fetch('http://127.0.0.1:9224/json')).json();
    const page = targets.find(t => t.type === 'page');
    const ws = new WebSocket(page.webSocketDebuggerUrl);
    ws.onopen = () => {
      let id = 1;
      const send = (method, params = {}) => new Promise(res => {
        const curId = id++;
        const handler = (evt) => {
          const msg = JSON.parse(evt.data);
          if (msg.id === curId) {
            ws.removeEventListener('message', handler);
            res(msg.result);
          }
        };
        ws.addEventListener('message', handler);
        ws.send(JSON.stringify({ id: curId, method, params }));
      });

      setTimeout(async () => {
        const evalRes = await send('Runtime.evaluate', {
          expression: `(() => {
            const items = Array.from(document.querySelectorAll('.day-scroll-item')).slice(0, 7);
            return items.map((it, idx) => ({
              idx,
              text: it.innerText,
              weekday: it.querySelector('.day-scroll-weekday')?.innerText,
              num: it.querySelector('.day-scroll-num')?.innerText,
              box: it.getBoundingClientRect(),
              weekdayBox: it.querySelector('.day-scroll-weekday')?.getBoundingClientRect(),
              style: window.getComputedStyle(it.querySelector('.day-scroll-weekday'))?.color
            }));
          })()`,
          returnByValue: true
        });
        console.log('Days DOM dump:\n', JSON.stringify(evalRes.result?.value, null, 2));
        browser.kill();
        process.exit(0);
      }, 1500);
    };
  } catch(e) {
    console.error('Error:', e.message);
    browser.kill();
    process.exit(1);
  }
}, 1500);
