# -*- coding: utf-8 -*-
"""刺客素材抠像：
GIF 逐帧解出 -> 时间中位数建背景模型 -> 差分抠前景 -> 输出透明精灵表 spy_walk_sheet.png
潜行图 spy_sneak.png 用同一套方法单独抠成透明 PNG
"""
import os
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

BASE = os.path.dirname(os.path.abspath(__file__))
AD = os.path.join(BASE, 'assets')


def load_gif_frames(path):
    im = Image.open(path)
    frames = []
    try:
        i = 0
        while True:
            im.seek(i)
            frames.append(im.convert('RGB').copy())
            i += 1
    except EOFError:
        pass
    return frames, im.info.get('duration', 100)


def build_bg(frames):
    a = np.stack([np.asarray(f, dtype=np.float32) for f in frames])
    return np.median(a, axis=0)


def fg_mask(frame, bg, thr=34):
    d = np.abs(np.asarray(frame, dtype=np.float32) - bg).max(axis=2)
    m = d > thr
    m = ndimage.binary_closing(m, iterations=2)
    m = ndimage.binary_opening(m, iterations=2)
    lab, n = ndimage.label(m)
    if n > 1:
        sizes = ndimage.sum(m, lab, range(1, n + 1))
        keep = np.where(sizes > max(200, sizes.max() * 0.06))[0] + 1
        m = np.isin(lab, keep)
    return m


def refine(rgb, pr, diff):
    """用 grabCut 以差分结果为初始提示细化前景；再与差分区求交，剔除背景残渣"""
    import cv2
    bgr = cv2.cvtColor(np.asarray(rgb), cv2.COLOR_RGB2BGR)
    m = np.where(pr, cv2.GC_PR_FGD, cv2.GC_PR_BGD).astype(np.uint8)
    m[:2, :] = cv2.GC_BGD; m[-2:, :] = cv2.GC_BGD
    m[:, :2] = cv2.GC_BGD; m[:, -2:] = cv2.GC_BGD
    bgd = np.zeros((1, 65), np.float64); fgd = np.zeros((1, 65), np.float64)
    cv2.grabCut(bgr, m, None, bgd, fgd, 8, cv2.GC_INIT_WITH_MASK)
    out = (m == cv2.GC_FGD) | (m == cv2.GC_PR_FGD)
    # 只保留与差分区重叠（膨胀 3px 容差）的部分，清掉成块背景残留
    near_diff = ndimage.binary_dilation(diff, iterations=3)
    out &= near_diff
    out = ndimage.binary_opening(ndimage.binary_closing(out, iterations=3), iterations=2)
    lab, n = ndimage.label(out)
    if n > 1:
        sz = ndimage.sum(out, lab, range(1, n + 1))
        keep = np.where(sz > max(120, sz.max() * 0.05))[0] + 1
        out = np.isin(lab, keep)
    return out


def apply_mask(rgb, m, blur=1.1):
    alpha = np.where(m, 255, 0).astype(np.uint8)
    a = Image.fromarray(alpha).filter(ImageFilter.MedianFilter(3))
    a = a.filter(ImageFilter.GaussianBlur(blur))
    av = np.asarray(a).astype(np.int16)
    av[av < 70] = 0            # 清掉半透明残渣
    a = Image.fromarray(av.astype(np.uint8))
    out = rgb.convert('RGBA')
    out.putalpha(a)
    return out


def main():
    frames, dur = load_gif_frames(os.path.join(AD, 'spy_walk.gif'))
    print('gif frames:', len(frames), 'duration:', dur)
    bg = build_bg(frames)

    cuts = []
    for i, f in enumerate(frames):
        diff = np.abs(np.asarray(f, dtype=np.float32) - bg).max(axis=2) > 30
        pr = fg_mask(f, bg)
        m = refine(f, pr, diff)
        cuts.append(apply_mask(f, m))
        print('  frame', i, 'fg px: diff', int(pr.sum()), '-> grabcut', int(m.sum()))

    # 保留原始 16:9 画幅（不裁剪），只让背景变透明
    bot = []
    for i, c in enumerate(cuts):
        a = np.asarray(c.getchannel('A'))
        ys = np.where((a > 32).any(axis=1))[0]
        bot.append(float(ys.max() + 1) / c.size[1])
    print('bottom ratios:', [round(b, 3) for b in bot])

    # 横向拼成精灵表，帧尺寸 = 原始 426x240（16:9）
    sizes = [c for c in cuts]
    H = cuts[0].size[1]
    tw = sum(c.size[0] for c in sizes)
    sheet = Image.new('RGBA', (tw, H), (0, 0, 0, 0))
    x = 0
    for c in sizes:
        sheet.paste(c, (x, 0), c)
        x += c.size[0]
    sheet.save(os.path.join(AD, 'spy_walk_sheet.png'))
    print('sheet ->', sheet.size, 'frames:', len(sizes), 'frame widths:', [c.size[0] for c in sizes])

    # 潜行图与 GIF 不同机位，不能用差分；由 _cutout_sneak.py 用 grabCut 单独抠
    print('sneak handled by _cutout_sneak.py')


if __name__ == '__main__':
    main()
