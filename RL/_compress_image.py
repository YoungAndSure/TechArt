#!/usr/bin/env python3
"""Compress convex_example.png below 500KB for Zhihu."""
import os
from PIL import Image

src = '/home/youngsure/Code/TechArt/RL/images/convex_example.png'
print(f'Original size: {os.path.getsize(src)} bytes')

img = Image.open(src)
if img.mode == 'RGBA':
    bg = Image.new('RGB', img.size, (255, 255, 255))
    bg.paste(img, mask=img.split()[3])
    img = bg

# Plan A: try PNG optimize
img.save(src, 'PNG', optimize=True)
size = os.path.getsize(src)
print(f'After PNG optimize: {size} bytes')

# Plan B: if still > 500KB, switch to JPEG
if size > 500_000:
    jpg_path = src.replace('.png', '.jpg')
    for quality in [85, 75, 65, 55, 45]:
        img.save(jpg_path, 'JPEG', quality=quality, optimize=True)
        q_size = os.path.getsize(jpg_path)
        print(f'  JPEG q={quality}: {q_size} bytes')
        if q_size < 500_000:
            os.remove(src)
            print(f'Final: {jpg_path} ({q_size} bytes, q={quality})')
            break
    else:
        raise RuntimeError('Could not compress below 500KB')
else:
    print(f'Final: {src} ({size} bytes)')