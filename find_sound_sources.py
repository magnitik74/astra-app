import zipfile
import re
import os

zip1 = r"C:\Users\Александр\Downloads\Moonly — Moon Calendar\Moonly — Moon Calendar.zip"
xapk = r"C:\Users\Александр\Downloads\Moonly_+Moon+Phases+&+Calendar_1.0.326_APKPure.xapk"

print("--- Searching web zip ---")
if os.path.exists(zip1):
    with zipfile.ZipFile(zip1) as z:
        for n in z.namelist():
            if n.endswith(('.js', '.html', '.json')):
                try:
                    c = z.read(n).decode('utf-8', errors='ignore')
                    m = re.findall(r'https?://[^\s"\'<>]+\.(?:mp3|m4a|wav|ogg)', c)
                    if m:
                        print(f"Found in {n}: {len(m)} audio URLs:")
                        for u in set(m):
                            print("  ", u)
                    # Check for API sound endpoints
                    api_m = re.findall(r'https?://[^\s"\'<>]+/(?:sounds|sound|audio|meditations|tracks)[^\s"\'<>]*', c)
                    if api_m:
                        print(f"API endpoints in {n}:")
                        for u in set(api_m)[:5]:
                            print("  ", u)
                except Exception as e:
                    pass

print("\n--- Searching APK ---")
if os.path.exists(xapk):
    with zipfile.ZipFile(xapk) as xz:
        for inner in ['com.moonly.android.apk', 'config.xxhdpi.apk']:
            if inner in xz.namelist():
                data = xz.read(inner)
                with zipfile.ZipFile(zipfile.io.BytesIO(data)) as apk:
                    for n in apk.namelist():
                        if n.endswith(('.js', '.json', '.xml')):
                            try:
                                c = apk.read(n).decode('utf-8', errors='ignore')
                                m = re.findall(r'https?://[^\s"\'<>]+\.(?:mp3|m4a|wav|ogg)', c)
                                if m:
                                    print(f"Found in APK {n}: {len(m)} audio URLs")
                                    for u in set(m)[:5]:
                                        print("  ", u)
                                # check sound CDN or API
                                endpoints = re.findall(r'https?://[^\s"\'<>]*(?:moonly|sound|audio|cdn)[^\s"\'<>]*(?:mp3|m4a|audio)', c, re.IGNORECASE)
                                if endpoints:
                                    print(f"Endpoints in {n}:")
                                    for u in set(endpoints)[:5]:
                                        print("  ", u)
                            except Exception:
                                pass
