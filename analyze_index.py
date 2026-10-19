import re

with open(r'D:\projects\monly\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

print('Length of index.html:', len(text))

# Search for navigation items
nav = re.findall(r'<nav[^>]*>.*?</nav>', text, re.DOTALL)
if nav:
    print('Nav HTML:\n', nav[0])
else:
    m = re.findall(r'<div[^>]*class=["\'][^"\']*nav[^"\']*["\'][^>]*>.*?</div>', text, re.DOTALL)
    if m:
        print('Nav div:\n', m[0][:600])

# Search for main tab containers
tabs = re.findall(r'id=["\'](?:tab-|screen-|section-)[^"\']+["\']', text)
print('Tabs/screens found:', sorted(list(set(tabs))))
