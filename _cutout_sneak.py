# -*- coding: utf-8 -*-
"""潜行图单独抠像：cv2.grabCut（该图与 GIF 不同机位，无法用差分）"""
import os
import numpy as np
import cv2
from PIL import Image, ImageFilter
from scipy import ndimage

BASE = os.path.dirname(os.path.abspath(__file__))
AD = os.path.join(BASE, 'assets')
SRC = os.path.join(AD, 'spy_sneak.png')

img = cv2.imdecode(np.fromfile(SRC, dtype=np.uint8), cv2.IMREAD_COLOR)
h, w = img.shape[:2]
print('src', w, h)

mask = np.zeros((h, w), np.uint8)
bgd = np.zeros((1, 65), np.float64)
fgd = np.zeros((1, 65), np.float64)
rect = (int(w * 0.18), int(h * 0.10), int(w * 0.64), int(h * 0.78))
cv2.grabCut(img, mask, rect, bgd, fgd, 10, cv2.GC_INIT_WITH_RECT)

fg = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)
fg = ndimage.binary_closing(fg > 0, iterations=3)
fg = ndimage.binary_opening(fg, iterations=2)
lab, n = ndimage.label(fg)
print('raw fg ratio %.1f%%  components %d' % (fg.mean() * 100, n))
if n > 1:
    sz = ndimage.sum(fg, lab, range(1, n + 1))
    keep = np.where(sz > max(400, sz.max() * 0.05))[0] + 1
    fg = np.isin(lab, keep)
print('kept fg ratio %.1f%%' % (fg.mean() * 100))

alpha = Image.fromarray(np.where(fg, 255, 0).astype(np.uint8))
alpha = alpha.filter(ImageFilter.MedianFilter(3)).filter(ImageFilter.GaussianBlur(1.1))
rgb = Image.open(SRC).convert('RGBA')
rgb.putalpha(alpha)
out = rgb  # 保留原始 16:9 画幅（426x240），不裁剪
a = np.asarray(out.getchannel('A'))
ys = np.where((a > 32).any(axis=1))[0]
print('bottom ratio: %.3f' % (float(ys.max() + 1) / out.size[1]))
out.save(os.path.join(AD, 'spy_sneak_cut.png'))
print('sneak_cut ->', out.size)
