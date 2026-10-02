# -*- coding: utf-8 -*-
"""诊断潜行图与 GIF 背景的差异分布，尝试直方图匹配后再差分"""
import os
import numpy as np
from PIL import Image
from scipy import ndimage

AD = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
im = Image.open(os.path.join(AD, 'spy_walk.gif'))
fr = []
i = 0
while True:
    try:
        im.seek(i); fr.append(np.asarray(im.convert('RGB'), dtype=np.float32)); i += 1
    except EOFError:
        break
bg = np.median(np.stack(fr), axis=0)
sp = np.asarray(Image.open(os.path.join(AD, 'spy_sneak.png')).convert('RGB'), dtype=np.float32)

d = np.abs(sp - bg).max(axis=2)
print('diff stats: mean %.1f  >34:%d  >60:%d  >90:%d' % (
    d.mean(), (d > 34).sum(), (d > 60).sum(), (d > 90).sum()))

h, w = d.shape
for r in range(3):
    row = []
    for c in range(3):
        blk = d[r * h // 3:(r + 1) * h // 3, c * w // 3:(c + 1) * w // 3]
        row.append(int((blk > 34).mean() * 100))
    print('grid%>34:', row)

# 直方图匹配：把 sneak 的通道分布拉到 bg 的分布上
out = np.empty_like(sp)
for ch in range(3):
    s = sp[:, :, ch]; t = bg[:, :, ch]
    sv, si = np.unique(np.round(s).astype(np.uint8), return_inverse=True)
    tv = np.array([np.percentile(t, np.percentile(s, p)) for p in np.linspace(0, 100, 256)])
    out[:, :, ch] = tv[si.reshape(s.shape)]
d2 = np.abs(out - bg).max(axis=2)
print('after match: mean %.1f  >34:%d  >60:%d' % (d2.mean(), (d2 > 34).sum(), (d2 > 60).sum()))
m = d2 > 40
m = ndimage.binary_closing(m, iterations=2)
lab, n = ndimage.label(m)
if n:
    sz = ndimage.sum(m, lab, range(1, n + 1))
    print('components>500px:', int((sz > 500).sum()), 'largest:', int(sz.max()))
