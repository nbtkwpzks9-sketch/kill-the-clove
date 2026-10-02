# -*- coding: utf-8 -*-
"""场景图居中裁成 16:9（只裁不缩放，不压缩变形）"""
import os
import shutil
from PIL import Image

AD = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
R = 16 / 9

for name in ['scene1.jpg', 'scene2.jpg']:
    p = os.path.join(AD, name)
    bak = os.path.join(AD, name.replace('.jpg', '_orig.jpg'))
    if not os.path.exists(bak):
        shutil.copyfile(p, bak)
    im = Image.open(p)
    w, h = im.size
    if w / h > R:                      # 太宽 -> 裁左右
        nw = int(round(h * R))
        x0 = (w - nw) // 2
        out = im.crop((x0, 0, x0 + nw, h))
    else:                              # 太高 -> 裁上下
        nh = int(round(w / R))
        y0 = (h - nh) // 2
        out = im.crop((0, y0, w, y0 + nh))
    out.save(p, quality=92)
    print(name, im.size, '->', out.size, 'ratio %.3f' % (out.size[0] / out.size[1]))
