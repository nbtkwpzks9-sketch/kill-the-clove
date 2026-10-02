# -*- coding: utf-8 -*-
"""文案改名：国王 -> 暮蝶，刺客 -> 皮蛋"""
import os

p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')
s = open(p, encoding='utf-8').read()
n1 = s.count('国王')
n2 = s.count('刺客')
s = s.replace('国王', '暮蝶').replace('刺客', '皮蛋')
open(p, 'w', encoding='utf-8').write(s)
print('国王 -> 暮蝶 :', n1)
print('刺客 -> 皮蛋 :', n2)
