import re

with open(r'D:\projects\monly\АСТРА_АССЕТЫ\astra_main_app.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

modals = re.findall(r'id="[^"]*modal[^"]*"', text, re.IGNORECASE)
print('Modals found in HTML:', set(modals))

p = re.search(r'<div id="screen-practices"[^>]*>(.*?)<div id="screen-healing"', text, re.DOTALL)
if p:
    print('\n--- Practices Screen Header & Content ---')
    print(p.group(1)[:1500])

h = re.search(r'<div id="screen-healing"[^>]*>(.*?)<div id="screen-chat"', text, re.DOTALL)
if h:
    print('\n--- Healing Screen Header & Content ---')
    print(h.group(1)[:1500])

c = re.search(r'<div id="screen-chat"[^>]*>(.*?)<div id="screen-you"', text, re.DOTALL)
if c:
    print('\n--- Chat Screen Header & Content ---')
    print(c.group(1)[:1500])

idx = text.find('id="screen-you"')
if idx != -1:
    print('\n--- You Screen (First 2500 chars) ---')
    print(text[idx:idx+2500])


