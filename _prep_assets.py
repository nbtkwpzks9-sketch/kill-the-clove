# -*- coding: utf-8 -*-
"""把已抠好的角色素材搬进 assassinate-king/assets
- king_sleep.png : 睡觉态，朝右（背对从左边靠近的刺客）
- king_alert.png : 警觉态，朝左（回头看向刺客，原图即朝左）
- spy_sneak.png  : 潜行/静止
- spy_walk.gif   : 走路（按住时）
"""
import os
import shutil
from PIL import Image

SRC = r'c:/Users/Gentech/CodeBuddy/奶龙moni/kill-the-king/_assets'
DST = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')

sleep = Image.open(os.path.join(SRC, 'ktkKingSleep.png'))
# ktkKingSleep.png 之前被镜像过（朝左），这里再翻一次回到朝右
sleep.transpose(Image.FLIP_LEFT_RIGHT).save(os.path.join(DST, 'king_sleep.png'))
shutil.copyfile(os.path.join(SRC, 'ktkKingAlert.png'), os.path.join(DST, 'king_alert.png'))
shutil.copyfile(os.path.join(SRC, 'ktkSneak.png'), os.path.join(DST, 'spy_sneak.png'))
shutil.copyfile(os.path.join(SRC, 'ktkWalk.gif'), os.path.join(DST, 'spy_walk.gif'))

for f in ['king_sleep.png', 'king_alert.png', 'spy_sneak.png', 'spy_walk.gif']:
    p = os.path.join(DST, f)
    im = Image.open(p)
    print(f, im.size, im.mode, os.path.getsize(p))
