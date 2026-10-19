import re

path = r'D:\projects\monly\АСТРА_АССЕТЫ\astra_main_app.html'
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

print(f'Length of astra_main_app.html: {len(text)} bytes')

# Find bottom nav bar
nav_match = re.search(r'<div class="bottom-nav"[^>]*>(.*?)</div>', text, re.DOTALL)
if nav_match:
    print('Bottom nav HTML:\n', nav_match.group(0))
else:
    # search any nav
    m = re.findall(r'<nav[^>]*>.*?</nav>', text, re.DOTALL)
    if m:
        print('Nav tag:\n', m[0])

# Find all views/screens
screens = re.findall(r'<div[^>]*class="[^"]*(?:screen|tab-content|view-section)[^"]*"[^>]*>', text)
print(f'Screens/Tabs ({len(screens)}):')
for s in screens[:15]:
    print('  ', s)

# Find switchTab calls and bottom bar
switch_calls = re.findall(r'switchTab\([^\)]+\)', text)
print('switchTab calls found:', sorted(list(set(switch_calls))))

# Find practice subtabs
practice_subtabs = re.findall(r'class="[^"]*practice-tab[^"]*"[^>]*>(.*?)</div>', text)
print('Practice subtabs:', practice_subtabs)

# Find healing subtabs
healing_subtabs = re.findall(r'class="[^"]*healing-tab[^"]*"[^>]*>(.*?)</div>', text)
print('Healing subtabs:', healing_subtabs)

# Check sound player
player = re.search(r'id="player-modal"[^>]*>.*?(?=</div>\s*<div id=")', text, re.DOTALL)
print('Player modal exists:', bool(player))

# Check paywall modal
paywall = re.search(r'id="paywall-modal"[^>]*>', text)
print('Paywall modal exists:', bool(paywall))

# Check chat mentors
mentors = re.findall(r'data-mentor="[^"]+"', text)
print('Chat mentors detected:', mentors)

