# -*- coding: utf-8 -*-
import os
import zipfile
import io
import hashlib
from collections import defaultdict
from PIL import Image

DEST_ROOT = r"D:\projects\monly\ОРИГИНАЛЬНЫЕ_АССЕТЫ_MOONLY"
os.makedirs(DEST_ROOT, exist_ok=True)

CATEGORIES = [
    "01_ФОНЫ_И_БАННЕРЫ_ВЫСОКОГО_РАЗРЕШЕНИЯ",
    "02_ИЛЛЮСТРАЦИИ_И_ОНБОРДИНГ",
    "03_ПЕЙВОЛЫ_И_ПОДПИСКА",
    "04_ТАРО_И_РУНЫ",
    "05_ЗОДИАК_И_НАТАЛЬНАЯ_КАРТА",
    "06_МЕДИТАЦИИ_И_ПРАКТИКИ",
    "07_3D_ИКОНКИ_И_ЭЛЕМЕНТЫ",
    "08_UI_И_ИНТЕРФЕЙС"
]

for c in CATEGORIES:
    os.makedirs(os.path.join(DEST_ROOT, c), exist_ok=True)

seen_hashes = {}
manifest = []

def classify(name, w, h, size):
    nl = name.lower()
    if any(k in nl for k in ['paywall', 'tariff', 'discount', 'purchase', 'annual', 'lifetime']):
        return "03_ПЕЙВОЛЫ_И_ПОДПИСКА"
    if any(k in nl for k in ['taro', 'card', 'arcana', 'rune', 'fehu', 'uruz', 'thurisaz', 'ansuz', 'glyph']):
        return "04_ТАРО_И_РУНЫ"
    if any(k in nl for k in ['zodiac', 'aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces', 'natal', 'planet', 'transit', 'retrograde', 'house']):
        return "05_ЗОДИАК_И_НАТАЛЬНАЯ_КАРТА"
    if any(k in nl for k in ['meditat', 'chakra', 'sound', 'healing', 'sleep', 'relax', 'gong', 'bowl']):
        return "06_МЕДИТАЦИИ_И_ПРАКТИКИ"
    if any(k in nl for k in ['onboard', 'welcome', 'intro', 'slide', 'tutorial', 'wisdom', 'karma', 'affirmation']):
        return "02_ИЛЛЮСТРАЦИИ_И_ОНБОРДИНГ"
    if any(k in nl for k in ['bg', 'back', 'sky', 'cloud', 'nature', 'landscape', 'sun', 'moon_phase', 'gradient', 'full_moon']) or (w and w >= 1000 and h and h >= 800) or size > 350*1024:
        return "01_ФОНЫ_И_БАННЕРЫ_ВЫСОКОГО_РАЗРЕШЕНИЯ"
    if any(k in nl for k in ['ic_', 'icon', 'btn', 'badge', 'logo', 'star', 'arrow', 'crown', 'crystal', 'sphere', 'check']):
        return "07_3D_ИКОНКИ_И_ЭЛЕМЕНТЫ"
    if w and w >= 400 and h and h >= 400:
        return "02_ИЛЛЮСТРАЦИИ_И_ОНБОРДИНГ"
    return "08_UI_И_ИНТЕРФЕЙС"

def save_image(data, raw_name, source_info):
    h = hashlib.sha256(data).hexdigest()
    if h in seen_hashes:
        return None

    # Get dimensions
    w, height = 0, 0
    fmt = "PNG"
    try:
        im = Image.open(io.BytesIO(data))
        w, height = im.width, im.height
        fmt = im.format or "PNG"
    except Exception:
        pass

    cat = classify(raw_name, w, height, len(data))
    
    # Clean filename
    clean_base = os.path.basename(raw_name).replace(" ", "_")
    ext = os.path.splitext(clean_base)[1].lower()
    if not ext:
        ext = ".png" if fmt == "PNG" else ".jpg"
        clean_base += ext

    target_path = os.path.join(DEST_ROOT, cat, clean_base)
    counter = 1
    stem, ext = os.path.splitext(clean_base)
    while os.path.exists(target_path):
        target_path = os.path.join(DEST_ROOT, cat, f"{stem}_{counter}{ext}")
        counter += 1

    with open(target_path, "wb") as f:
        f.write(data)

    rel_path = os.path.relpath(target_path, DEST_ROOT).replace("\\", "/")
    meta = {
        "filename": os.path.basename(target_path),
        "category": cat,
        "rel_path": rel_path,
        "width": w,
        "height": height,
        "size_bytes": len(data),
        "size_kb": round(len(data) / 1024, 1),
        "format": fmt,
        "source": source_info
    }
    seen_hashes[h] = meta
    manifest.append(meta)
    return meta

print("1. Extracting Moonly — Moon Calendar.zip...")
zip1 = r"C:\Users\Александр\Downloads\Moonly — Moon Calendar\Moonly — Moon Calendar.zip"
if os.path.exists(zip1):
    with zipfile.ZipFile(zip1) as z:
        for n in z.namelist():
            if n.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.svg')):
                save_image(z.read(n), n, "Moonly Web CDN Archive")

print(f"Extracted so far: {len(manifest)} unique assets")

print("2. Extracting Moonly XAPK (com.moonly.android.apk + config.xxhdpi.apk)...")
xapk = r"C:\Users\Александр\Downloads\Moonly_+Moon+Phases+&+Calendar_1.0.326_APKPure.xapk"
if os.path.exists(xapk):
    with zipfile.ZipFile(xapk) as xz:
        for inner_apk in ['config.xxhdpi.apk', 'com.moonly.android.apk']:
            if inner_apk in xz.namelist():
                apk_bytes = xz.read(inner_apk)
                with zipfile.ZipFile(io.BytesIO(apk_bytes)) as apk:
                    for n in apk.namelist():
                        if n.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                            save_image(apk.read(n), os.path.basename(n), f"Moonly APK ({inner_apk})")

print(f"Extracted so far: {len(manifest)} unique assets")

print("3. Scanning moonly_resources and moonly_extracted directories...")
for src_dir, label in [
    (r"C:\Users\Александр\Downloads\moonly_resources", "moonly_resources"),
    (r"C:\Users\Александр\Downloads\moonly_extracted", "moonly_extracted")
]:
    if os.path.exists(src_dir):
        for root, dirs, files in os.walk(src_dir):
            for fn in files:
                if fn.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    fp = os.path.join(root, fn)
                    try:
                        with open(fp, "rb") as f:
                            data = f.read()
                        save_image(data, fn, label)
                    except Exception:
                        pass

print(f"TOTAL UNIQUE ASSETS EXTRACTED: {len(manifest)}")

# Breakdown by category
cat_counts = defaultdict(int)
cat_sizes = defaultdict(int)
for m in manifest:
    cat_counts[m["category"]] += 1
    cat_sizes[m["category"]] += m["size_bytes"]

print("\n--- Breakdown by category ---")
for c in CATEGORIES:
    cnt = cat_counts[c]
    mb = cat_sizes[c] / (1024 * 1024)
    print(f"{c}: {cnt} files ({mb:.2f} MB)")

# Save Manifest JSON
import json
manifest_path = os.path.join(DEST_ROOT, "manifest_moonly_original_assets.json")
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)
print(f"\nManifest saved: {manifest_path}")
