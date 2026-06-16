import xml.etree.ElementTree as ET
import re

tree = ET.parse(r'C:\Users\User\Ambiente de Trabalho\Stuff\Docs\Projetos\Codify - Website\writing-animation.svg')
root = tree.getroot()
ns = {'svg': 'http://www.w3.org/2000/svg'}
style = root.find('.//svg:style', ns)
css = style.text

count = css.count('@keyframes cr')
print(f'@keyframes cr count: {count}')

print(f'.cr{{animation:cr 14s: {"cr{animation:cr 14s" in css}')
print(f'.cr{{opacity:0}}: {"cr{opacity:0}" in css}')

texts = root.findall('.//svg:text', ns)
c1 = [t for t in texts if t.get('class','').startswith('c1')]
c2 = [t for t in texts if t.get('class','').startswith('c2')]
f2 = [t for t in texts if t.get('class','').startswith('f2')]
print(f'c1: {len(c1)}, c2: {len(c2)}, f2: {len(f2)}')

# Extract keyframe with brace matching
idx = css.index('@keyframes cr{')
depth = 1
pos = idx + len('@keyframes cr{')
while depth > 0 and pos < len(css):
    if css[pos] == '{': depth += 1
    elif css[pos] == '}': depth -= 1
    pos += 1
kf_text = css[idx:pos]
print(f'Keyframe lines: {kf_text.count(chr(10))+1}')
# Show first 10 and last 5 lines
lines = kf_text.split('\n')
print('--- First 10 ---')
for l in lines[:10]:
    print(l)
print('--- Last 5 ---')
for l in lines[-5:]:
    print(l)

# Check for duplicate percentages
pcts = re.findall(r'(\d+\.?\d*)%{', kf_text)
dupes = [p for p in pcts if pcts.count(p) > 1]
if dupes:
    print(f'Duplicate percentages: {set(dupes)}')
else:
    print('No duplicate percentages')
