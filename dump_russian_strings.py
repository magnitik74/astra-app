import zipfile
import re

xapk = r"C:\Users\Александр\Downloads\Moonly_+Moon+Phases+&+Calendar_1.0.326_APKPure.xapk"
with zipfile.ZipFile(xapk) as xz:
    data = xz.read('com.moonly.android.apk')
    with zipfile.ZipFile(zipfile.io.BytesIO(data)) as apk:
        arsc = apk.read('resources.arsc')
        # find sequences of UTF-8 Russian characters
        # Cyrillic in UTF-8: 0xd0, 0xd1
        pattern = rb'(?:[\xd0\xd1][\x80-\xbf]|\s|[a-zA-Z0-9,\.\!\?\-\:\(\)\"\']){6,}'
        matches = re.findall(pattern, arsc)
        decoded = []
        for m in matches:
            try:
                s = m.decode('utf-8').strip()
                # Must contain at least some Cyrillic
                if any('\u0400' <= c <= '\u04FF' for c in s) and len(s) > 3:
                    decoded.append(s)
            except Exception:
                pass
        
        print(f"Total Russian strings extracted: {len(decoded)}")
        # Filter for settings, notifications, deities, calendar, etc.
        settings_kw = ['уведомлен', 'звук', 'вибрац', 'настройк', 'язык', 'подписк', 'аккаунт', 'очист', 'данные', 'о приложен', 'версия', 'поддержк', 'политик', 'услов']
        matched = [s for s in set(decoded) if any(k in s.lower() for k in settings_kw)]
        print(f"Settings-related strings ({len(matched)}):")
        for s in sorted(matched)[:50]:
            print("  *", s)
