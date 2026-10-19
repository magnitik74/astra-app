import zipfile
import io
import re

xapk = r"C:\Users\Александр\Downloads\Moonly_+Moon+Phases+&+Calendar_1.0.326_APKPure.xapk"
with zipfile.ZipFile(xapk) as xz:
    data = xz.read('com.moonly.android.apk')
    with zipfile.ZipFile(io.BytesIO(data)) as apk:
        c = apk.read('classes6.dex')
        # find menu items, actions, navigation targets
        matches = re.findall(rb'open[A-Z][a-zA-Z0-9]+|navigate[A-Z][a-zA-Z0-9]+|on[A-Z][a-zA-Z0-9]+Click', c)
        print('Navigation/Click actions in classes6.dex:')
        for m in sorted(list(set([m.decode('utf-8', errors='ignore') for m in matches]))):
            if any(k in m.lower() for k in ['setting', 'menu', 'profile', 'notif', 'about', 'privacy', 'term', 'rate', 'share', 'sub', 'account', 'restore']):
                print(' ', m)
