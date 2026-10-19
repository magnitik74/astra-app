# -*- coding: utf-8 -*-
import subprocess
import time
import json
import urllib.request
import os

DEBUG_PORT = 9240
USER_DATA = os.path.join(r"D:\projects\monly", f".temp_edge_gal_{int(time.time())}")
EDGE_EXE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
URL = "http://localhost:3000/moonly_original_assets_gallery.html"

proc = subprocess.Popen([
    EDGE_EXE,
    f"--remote-debugging-port={DEBUG_PORT}",
    "--headless=new",
    "--disable-gpu",
    f"--user-data-dir={USER_DATA}",
    "--window-size=1280,950",
    URL
])

time.sleep(2)

# Get WebSocket URL
req = urllib.request.urlopen(f"http://127.0.0.1:{DEBUG_PORT}/json/list")
pages = json.loads(req.read().decode())
ws_url = pages[0]["webSocketDebuggerUrl"]

import asyncio
import websockets

async def capture():
    async with websockets.connect(ws_url, max_size=50*1024*1024) as ws:
        msg_id = 1
        async def send(method, params={}):
            nonlocal msg_id
            cid = msg_id
            msg_id += 1
            await ws.send(json.dumps({"id": cid, "method": method, "params": params}))
            while True:
                resp = json.loads(await ws.recv())
                if resp.get("id") == cid:
                    return resp.get("result", {})

        await send("Page.enable")
        await asyncio.sleep(1.5)

        # 1. Capture Paywalls view
        await send("Runtime.evaluate", {
            "expression": """
                const pills = document.querySelectorAll('.cat-pill');
                for (const p of pills) {
                    if (p.innerText.includes('Пейволы')) { p.click(); break; }
                }
            """
        })
        await asyncio.sleep(1.0)
        shot = await send("Page.captureScreenshot", {"format": "png"})
        import base64
        with open(r"D:\projects\monly\test_screenshots\14_gallery_paywalls.png", "wb") as f:
            f.write(base64.b64decode(shot["data"]))
        print("Captured 14_gallery_paywalls.png")

        # 2. Capture 3D Icons view
        await send("Runtime.evaluate", {
            "expression": """
                const pills = document.querySelectorAll('.cat-pill');
                for (const p of pills) {
                    if (p.innerText.includes('3D-Иконки')) { p.click(); break; }
                }
            """
        })
        await asyncio.sleep(1.0)
        shot = await send("Page.captureScreenshot", {"format": "png"})
        with open(r"D:\projects\monly\test_screenshots\15_gallery_3d_icons.png", "wb") as f:
            f.write(base64.b64decode(shot["data"]))
        print("Captured 15_gallery_3d_icons.png")

        # 3. Capture Tarot and Runes view
        await send("Runtime.evaluate", {
            "expression": """
                const pills = document.querySelectorAll('.cat-pill');
                for (const p of pills) {
                    if (p.innerText.includes('Таро')) { p.click(); break; }
                }
            """
        })
        await asyncio.sleep(1.0)
        shot = await send("Page.captureScreenshot", {"format": "png"})
        with open(r"D:\projects\monly\test_screenshots\16_gallery_tarot_runes.png", "wb") as f:
            f.write(base64.b64decode(shot["data"]))
        print("Captured 16_gallery_tarot_runes.png")

        # 4. Open Modal Zoom on a Paywall card
        await send("Runtime.evaluate", {
            "expression": """
                const pills = document.querySelectorAll('.cat-pill');
                for (const p of pills) {
                    if (p.innerText.includes('Пейволы')) { p.click(); break; }
                }
            """
        })
        await asyncio.sleep(0.5)
        await send("Runtime.evaluate", {
            "expression": """
                const cards = document.querySelectorAll('.asset-card');
                for (const c of cards) {
                    if (c.innerText.includes('female')) { c.click(); break; }
                }
            """
        })
        await asyncio.sleep(0.8)
        shot = await send("Page.captureScreenshot", {"format": "png"})
        with open(r"D:\projects\monly\test_screenshots\17_gallery_zoom_modal.png", "wb") as f:
            f.write(base64.b64decode(shot["data"]))
        print("Captured 17_gallery_zoom_modal.png")

asyncio.run(capture())
proc.kill()
try:
    import shutil
    shutil.rmtree(USER_DATA, ignore_errors=True)
except Exception:
    pass
print("ALL GALLERY SCREENSHOTS CAPTURED!")
