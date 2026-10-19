const { spawn } = require('child_process');

const BROWSER_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const APP_URL = 'http://localhost:3000/%D0%90%D0%A1%D0%A2%D0%A0%D0%90_%D0%90%D0%A1%D0%A1%D0%95%D0%A2%D0%AB/astra_main_app.html';

const browser = spawn(BROWSER_PATH, [
  '--remote-debugging-port=9225',
  '--headless=new',
  '--window-size=430,932',
  '--disable-gpu',
  '--user-data-dir=C:\\temp\\edge_click_test_' + Date.now(),
  APP_URL
]);

setTimeout(async () => {
  try {
    const targets = await (await fetch('http://127.0.0.1:9225/json')).json();
    const page = targets.find(t => t.type === 'page');
    const ws = new WebSocket(page.webSocketDebuggerUrl);
    ws.onopen = () => {
      let id = 1;
      const send = (method, params = {}) => new Promise((res, rej) => {
        const curId = id++;
        const handler = (evt) => {
          const msg = JSON.parse(evt.data);
          if (msg.id === curId) {
            ws.removeEventListener('message', handler);
            if (msg.error) rej(msg.error);
            else res(msg.result);
          }
        };
        ws.addEventListener('message', handler);
        ws.send(JSON.stringify({ id: curId, method, params }));
      });

      ws.addEventListener('message', (evt) => {
        const msg = JSON.parse(evt.data);
        if (msg.method === 'Runtime.consoleAPICalled') {
          console.log('[Console]', msg.params.type, msg.params.args.map(a => a.value || a.description).join(' '));
        }
        if (msg.method === 'Runtime.exceptionThrown') {
          console.log('[EXCEPTION]', msg.params.exceptionDetails?.exception?.description || msg.params.exceptionDetails?.text);
        }
      });

      setTimeout(async () => {
        await send('Runtime.enable');
        await send('Page.enable');

        console.log('--- Testing click on Day 1 ---');
        await send('Runtime.evaluate', {
          expression: `(() => {
            const items = document.querySelectorAll('.day-scroll-item');
            if (items[0]) items[0].click();
          })()`
        });

        console.log('--- Testing click on Day 2 ---');
        await send('Runtime.evaluate', {
          expression: `(() => {
            const items = document.querySelectorAll('.day-scroll-item');
            if (items[1]) items[1].click();
          })()`
        });

        console.log('--- Testing click on Day 6 ---');
        await send('Runtime.evaluate', {
          expression: `(() => {
            const items = document.querySelectorAll('.day-scroll-item');
            if (items[5]) items[5].click();
          })()`
        });

        console.log('--- Testing click on ОКТ (calendar-full-view-btn) ---');
        await send('Runtime.evaluate', {
          expression: `(() => {
            const btn = document.querySelector('.calendar-full-view-btn');
            if (btn) btn.click();
            const modal = document.getElementById('universal-modal');
            return { modalDisplay: modal?.style?.display, contentLen: modal?.innerHTML?.length };
          })()`,
          returnByValue: true
        }).then(r => console.log('OCT click result:', r.result?.value));

        browser.kill();
        process.exit(0);
      }, 2000);
    };
  } catch(e) {
    console.error('Error:', e);
    browser.kill();
    process.exit(1);
  }
}, 1500);
