#!/usr/bin/env python3
"""Convert merged MFRL markdown notes to Zhihu-compatible format."""
import re
import os

BASE = '/home/youngsure/Code/TechArt/RL'
files = [
    f'{BASE}/note_of_mfrl.md',
    f'{BASE}/note_of_mfrl2.md',
    f'{BASE}/note_of_mfrl3.md',
    f'{BASE}/note_of_mfrl4.md',
]
GITHUB_RAW = 'https://raw.githubusercontent.com/YoungAndSure/TechArt/main/RL/images/'

# === Step 1: merge ===
parts = []
for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        parts.append(fh.read())
combined = '\n\n---\n\n'.join(parts)

# === Step 2.1: block math ```math ... ```  ->  $$ ... $$ ===
def replace_block_math(match):
    inner = match.group(1)
    lines = inner.strip().split('\n')
    formatted = ' '.join(line.strip() for line in lines)
    return '$$' + formatted + '$$'

combined = re.sub(r'``` ?math\s*\n(.*?)\n```', replace_block_math, combined, flags=re.DOTALL)

# === Step 2.2: inline math $`...`$  ->  $...$  (.+? does not match \n) ===
def replace_inline_math(match):
    return '$' + match.group(1) + '$'

combined = re.sub(r'\$`(.+?)`\$', replace_inline_math, combined)

# === Step 2.3: align -> aligned ===
combined = combined.replace('\\begin{align}', '\\begin{aligned}')
combined = combined.replace('\\end{align}', '\\end{aligned}')
combined = combined.replace('\\begin{align*}', '\\begin{aligned}')
combined = combined.replace('\\end{align*}', '\\end{aligned}')

# === Step 3: image paths -> GitHub raw URLs ===
combined = re.sub(
    r'!\[(.*?)\]\(\./images/(.*?)\)',
    r'![\1](' + GITHUB_RAW + r'\2)',
    combined,
)
combined = re.sub(
    r'!\[(.*?)\]\(images/(.*?)\)',
    r'![\1](' + GITHUB_RAW + r'\2)',
    combined,
)

# === Step 5: write ===
out_path = f'{BASE}/note_of_mfrl_zhihu.md'
with open(out_path, 'w', encoding='utf-8') as fh:
    fh.write(combined)
print(f'Wrote {out_path} ({len(combined)} bytes)')

# === Inline verification ===
print('--- inline checks ---')
print(f'  residual $`: {len(re.findall(r"\\$`", combined))}')
print(f'  residual ```math: {len(re.findall(r"``` ?math", combined))}')
print(f'  residual \\begin{{align}}: {len(re.findall(r"\\\\begin\\{align\\}", combined))}')
print(f'  residual local image refs: {len(re.findall(r"!\[.*?\]\((?:\./)?images/", combined))}')

# Print all image URLs to verify
urls = sorted(set(re.findall(r'https://raw\.githubusercontent\.com[^)]*', combined)))
print(f'  unique image URLs: {len(urls)}')
for u in urls:
    print(f'    {u}')