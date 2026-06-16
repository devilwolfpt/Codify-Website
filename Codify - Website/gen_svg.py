from PIL import ImageFont
font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 20)

with open(r'C:\Users\User\Ambiente de Trabalho\Stuff\Docs\Projetos\Codify - Website\wallpepar\b64_svg.txt', encoding='ascii') as f:
    b64_img = f.read()

with open(r'C:\Users\User\Ambiente de Trabalho\Stuff\Docs\Projetos\Codify - Website\b64_logo.txt', encoding='ascii') as f:
    b64_logo = f.read()

def advance(c):
    return font.getlength(c)

SVG_CENTER = 380

def layout_left(line, start_x):
    pos = start_x
    xs = []
    for c in line:
        xs.append(int(pos))
        pos += advance(c)
    end = int(pos)
    return xs, end

# Find start_x such that the longest line is centered as a block
lines = ['Codify', 'O melhor editor de codigo do mundo', 'Experimente já!']
widths = [sum(advance(c) for c in l) for l in lines]
max_width = max(widths)
start_x = int(SVG_CENTER - max_width / 2)

l1, l1_end = layout_left('Codify', start_x)
l2, l2_end = layout_left('O melhor editor de codigo do mundo', start_x)
l3, l3_end = layout_left('Experimente já!', start_x)

def add(kf, pct, x, y, opacity=None):
    t = f'        {pct:.1f}%{{transform:translate({x}px,{y}px)'
    if opacity is not None:
        t += f';opacity:{opacity}'
    t += '}'
    kf.append(t)

kf = []
Y1 = 140
Y2 = 180
add(kf, 0, l1[0], Y1, '0')
# Keep opacity 0 until just before first visible step
add(kf, 13.9, l1[0], Y1, '0')

# Phase 1: Write Codify (cursor LEADS by 1 — always at next char's position)
all_l1 = l1[1:] + [l1_end]
for i, x in enumerate(all_l1):
    pct = 14.0 + i * 0.7
    add(kf, pct, x, Y1, '1')
# Phase 2: Write line2 (cursor at second char onward)
pct_end_l1 = 14.0 + (len(all_l1)-1) * 0.7
add(kf, pct_end_l1 + 0.7, l1_end, Y1, '1')
# Jump to line2 second char (first char appears same pct)
all_l2 = l2[1:] + [l2_end]
for i, x in enumerate(all_l2):
    pct = pct_end_l1 + 1.4 + i * 0.7
    add(kf, pct, x, Y2, '1')

# Pause at line2 end
pct_end_l2 = pct_end_l1 + 1.4 + (len(all_l2)-1) * 0.7
add(kf, pct_end_l2 + 0.5, l2_end, Y2, '1')
# Keep opacity 1 until just before hiding
add(kf, pct_end_l2 + 1.4, l2_end, Y2, '1')
add(kf, pct_end_l2 + 1.5, l2_end, Y2, '0')

# Phase 3: Erase line2 (cursor leads by one — to right of char being erased)
add(kf, 48.5, l2_end, Y2, '0')
add(kf, 48.6, l2_end, Y2, '1')
erase_l2 = l2[:0:-1]  # [l2[-1], l2[-2], ..., l2[1]]
for i, x in enumerate(erase_l2):
    pct = 48.6 + (i+1) * 0.7
    add(kf, pct, x, Y2, '1')
pct_erase_end = 48.6 + len(erase_l2) * 0.7

# Phase 4: Erase line1 (jump + lead by one)
add(kf, pct_erase_end + 0.5, l2[1], Y2, '1')
erase_l1 = [l1_end] + l1[:0:-1]  # [l1_end, l1[-1], ..., l1[1]]
for i, x in enumerate(erase_l1):
    pct = pct_erase_end + 0.6 + i * 0.7
    add(kf, pct, x, Y1, '1')
pct_erase_l1 = pct_erase_end + 0.6 + (len(erase_l1)-1) * 0.7
# Keep opacity 1 then instant hide
add(kf, pct_erase_l1 + 1.4, l1[0], Y1, '1')
add(kf, pct_erase_l1 + 1.5, l1[0], Y1, '0')

# Phase 5: Write Experimente ja! (cursor leads by 1)
add(kf, 82.0, l3[0], Y2, '0')
all_l3 = l3[1:] + [l3_end]
for i, x in enumerate(all_l3):
    pct = 82.1 + i * 0.7
    add(kf, pct, x, Y2, '1')
# Keep opacity 1 then instant hide
pct_end_l3 = 82.1 + (len(all_l3)-1) * 0.7
add(kf, pct_end_l3 + 1.6, l3_end, Y2, '1')
add(kf, pct_end_l3 + 1.7, l3_end, Y2, '0')
add(kf, 100, l3_end, Y2, '0')

# Check for duplicates
pcts = [line.split('%')[0].strip() for line in kf if '%' in line]
dupes = {p for p in pcts if pcts.count(p) > 1}
if dupes:
    print(f'WARNING: {len(dupes)} duplicate percentages: {sorted(dupes, key=float)}')
else:
    print('OK: no duplicate percentages')

# Build full SVG
lines = []
SVG_H = 350
lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 {SVG_H}" width="100%" height="100%">')
lines.append('  <defs>')
lines.append('    <style>')
lines.append('      * { font-family: "Plus Jakarta Sans", "Segoe UI", sans-serif; }')
lines.append('      text { dominant-baseline: central; alignment-baseline: central; }')
lines.append('      @keyframes o1{0%{transform:rotate(0deg) translateX(28px) rotate(0deg)}100%{transform:rotate(360deg) translateX(28px) rotate(-360deg)}}')
lines.append('      @keyframes o2{0%{transform:rotate(90deg) translateX(28px) rotate(-90deg)}100%{transform:rotate(450deg) translateX(28px) rotate(-450deg)}}')
lines.append('      @keyframes o3{0%{transform:rotate(180deg) translateX(28px) rotate(-180deg)}100%{transform:rotate(540deg) translateX(28px) rotate(-540deg)}}')
lines.append('      @keyframes o4{0%{transform:rotate(270deg) translateX(28px) rotate(-270deg)}100%{transform:rotate(630deg) translateX(28px) rotate(-630deg)}}')
lines.append('      @keyframes fo{0%,25%{opacity:1}45%,100%{opacity:0}}')
lines.append('      @keyframes c1{0%,23%{opacity:1}25%,100%{opacity:0}}')
lines.append('      @keyframes c2{0%,23%{opacity:0}25%,48%{opacity:1}50%,100%{opacity:0}}')
lines.append('      @keyframes c3{0%,48%{opacity:0}50%,73%{opacity:1}75%,100%{opacity:0}}')
lines.append('      @keyframes c4{0%,73%{opacity:0}75%,100%{opacity:1}}')
lines.append('      @keyframes gp{0%,100%{stroke-opacity:0.1}50%{stroke-opacity:0.3}}')
lines.append('      @keyframes cr{')
lines.extend(kf)
lines.append('      }')
lines.append('      .a1{animation:o1 1.8s linear infinite;transform-origin:0 0}')
lines.append('      .a2{animation:o2 1.8s linear infinite;transform-origin:0 0}')
lines.append('      .a3{animation:o3 1.8s linear infinite;transform-origin:0 0}')
lines.append('      .a4{animation:o4 1.8s linear infinite;transform-origin:0 0}')
lines.append('      @keyframes foLoop{0%,22%{opacity:1}22%,100%{opacity:0}}')
lines.append('      .ob{animation:foLoop 14s infinite}')
lines.append('      .k1{animation:c1 0.5s steps(1) infinite}')
lines.append('      .k2{animation:c2 0.5s steps(1) infinite}')
lines.append('      .k3{animation:c3 0.5s steps(1) infinite}')
lines.append('      .k4{animation:c4 0.5s steps(1) infinite}')
lines.append('      .gl{animation:gp 3s ease-in-out infinite}')
lines.append('      .cr{opacity:0}')
lines.append('      .cr{animation:cr 14s linear infinite}')

def pct(t):
    return round(t / 14 * 100, 4)

def kf_body(appear, hide):
    pa = pct(appear)
    pb = pct(appear + 0.001)
    hb = pct(hide)
    hc = pct(hide + 0.001)
    return f'0%{{opacity:0}}{pa}%{{opacity:0}}{pb}%{{opacity:1}}{hb}%{{opacity:1}}{hc}%{{opacity:0}}100%{{opacity:0}}'

# logo: appear at 22% (3.08s), hide at 13.9s
lines.append(f'      @keyframes logoLoop{{0%{{opacity:0}}22%{{opacity:0}}{pct(3.081)}%{{opacity:1}}{pct(13.9)}%{{opacity:1}}{pct(13.901)}%{{opacity:0}}100%{{opacity:0}}}}')
lines.append(f'      .logo{{animation:logoLoop 14s infinite}}')

for i in range(len(l1)):
    appear = 2.0 + i * 0.1
    hide = 10.8 - i * 0.1
    lines.append(f'      @keyframes c1-{i}{{{kf_body(appear, hide)}}}')
    lines.append(f'      .c1-{i}{{animation:c1-{i} 14s infinite}}')
for i in range(len(l2)):
    appear = 2.7 + i * 0.1
    hide = 10.1 - i * 0.1
    lines.append(f'      @keyframes c2-{i}{{{kf_body(appear, hide)}}}')
    lines.append(f'      .c2-{i}{{animation:c2-{i} 14s infinite}}')
for i in range(len(l3)):
    appear = 11.5 + i * 0.1
    hide = 13.9
    lines.append(f'      @keyframes f2-{i}{{{kf_body(appear, hide)}}}')
    lines.append(f'      .f2-{i}{{animation:f2-{i} 14s infinite}}')

lines.append('      [class^="c"]{opacity:0}')
lines.append('      [class^="f"]{opacity:0}')
lines.append('    </style>')
lines.append('    <clipPath id="bgClip">')
lines.append(f'      <rect width="600" height="{SVG_H}" rx="20" />')
lines.append('    </clipPath>')
lines.append('  </defs>')
lines.append('')
lines.append(f'  <image href="data:image/jpeg;base64,{b64_img}" x="0" y="0" width="600" height="{SVG_H}" preserveAspectRatio="xMidYMid slice" clip-path="url(#bgClip)" />')
lines.append(f'  <rect width="600" height="{SVG_H}" rx="20" fill="rgba(0,0,0,0.55)" />')
lines.append('  <g class="ob" transform="translate(80,175)">')
lines.append('    <g class="a1"><text text-anchor="middle" font-size="20" fill="#7c3aed" font-weight="bold">&#9650;</text></g>')
lines.append('    <g class="a2"><text text-anchor="middle" font-size="20" fill="#3b82f6" font-weight="bold">&#9632;</text></g>')
lines.append('    <g class="a3"><text text-anchor="middle" font-size="20" fill="#ec4899" font-weight="bold">&#9679;</text></g>')
lines.append('    <g class="a4"><text text-anchor="middle" font-size="20" fill="#06b6d4" font-weight="bold">&#10006;</text></g>')
lines.append('  </g>')
lines.append(f'  <image class="logo" href="data:image/png;base64,{b64_logo}" x="0" y="95" width="160" height="160" />')

for i, (c, x) in enumerate(zip('Codify', l1)):
    lines.append(f'  <text class="c1-{i}" font-size="20" fill="white" x="{x}" y="140">{c}</text>')
for i, (c, x) in enumerate(zip('O melhor editor de codigo do mundo', l2)):
    lines.append(f'  <text class="c2-{i}" font-size="20" fill="white" x="{x}" y="180">{c}</text>')

lines.append('  <g class="cr">')
lines.append('    <text text-anchor="middle" font-size="20" fill="#a78bfa" font-weight="bold" class="k1">&#9650;</text>')
lines.append('    <text text-anchor="middle" font-size="20" fill="#a78bfa" font-weight="bold" class="k2">&#9632;</text>')
lines.append('    <text text-anchor="middle" font-size="20" fill="#a78bfa" font-weight="bold" class="k3">&#9679;</text>')
lines.append('    <text text-anchor="middle" font-size="20" fill="#a78bfa" font-weight="bold" class="k4">&#10006;</text>')
lines.append('  </g>')

third_text = 'Experimente já!'
for i, (c, x) in enumerate(zip(third_text, l3)):
    entity = '&#225;' if c == 'á' else c
    lines.append(f'  <text class="f2-{i}" font-size="20" fill="white" x="{x}" y="180">{entity}</text>')

lines.append(f'  <rect x="2" y="2" width="596" height="{SVG_H-4}" rx="20" fill="none" stroke="#7c3aed" stroke-width="1.5" class="gl" />')
lines.append('</svg>')

with open(r'C:\Users\User\Ambiente de Trabalho\Stuff\Docs\Projetos\Codify - Website\writing-animation.svg', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print(f'Written {len(lines)} lines')
