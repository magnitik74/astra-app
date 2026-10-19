import json
import os

with open(r"D:\projects\monly\moonly_sounds_api_response.json", "r", encoding="utf-8") as f:
    raw = json.load(f)

items = raw.get("data", [])
compiled_sounds = []

for it in items:
    cats = [c["name"] for c in it.get("categories", [])]
    compiled_sounds.append({
        "id": it.get("id"),
        "name": it.get("name"),
        "categories": cats,
        "description": it.get("description", ""),
        "soundUrl": it.get("soundUrl", ""),
        "videoUrl": it.get("videoUrl", ""),
        "cardIconUrl": it.get("cardIconUrl", ""),
        "duration": it.get("soundDuration", 3600),
        "free": it.get("free", True),
        "isWelcome": it.get("isWelcome", False)
    })

print(f"Compiled {len(compiled_sounds)} sounds.")

js_content = f"// ASTRA 68 HEALING SOUNDS & VIDEO LOOPS (ORIGINAL API CATALOG)\n"
js_content += f"const ASTRA_SOUNDS_DATABASE = {json.dumps(compiled_sounds, ensure_ascii=False, indent=2)};\n"

out_file = r"D:\projects\monly\АСТРА_АССЕТЫ\astra_sounds_data.js"
with open(out_file, "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"Saved to {out_file}")
