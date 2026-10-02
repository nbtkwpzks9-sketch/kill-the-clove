# -*- coding: utf-8 -*-
"""把三段视频转成 720p H.264+AAC（兼容 WebView），输出到 assets/"""
import os
import subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
AD = os.path.join(BASE, 'assets')
SRC = r'c:/Users/Gentech/CodeBuddy/奶龙moni'

JOBS = [
    ('3bd5f1bc6f9c17169fef55cb7db3be4a.mp4', 'intro.mp4'),   # 开场
    ('ffcd6abf589a934785c312e294fe3cc5_raw.mp4', 'fail.mp4'),  # 刺杀失败
    ('1a4b8f8e10a5913d80fb33f7e975b1f0_raw.mp4', 'win.mp4'),   # 刺杀成功
]

for src, dst in JOBS:
    sp = os.path.join(SRC, src)
    dp = os.path.join(AD, dst)
    cmd = [
        'ffmpeg', '-y', '-i', sp,
        '-vf', 'scale=1280:-2',
        '-c:v', 'libx264', '-profile:v', 'main', '-pix_fmt', 'yuv420p',
        '-crf', '26', '-preset', 'medium',
        '-c:a', 'aac', '-b:a', '96k', '-ar', '44100',
        '-movflags', '+faststart',
        dp,
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(dst, os.path.getsize(dp), 'bytes' if os.path.exists(dp) else 'FAILED')
