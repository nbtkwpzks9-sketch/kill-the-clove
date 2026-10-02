# -*- coding: utf-8 -*-
"""通过 GitHub API 创建公开仓库并上传全部文件（本机 github.com 直连不通，但 API 可用）

用法：
    set GITHUB_TOKEN=ghp_xxxx        (PowerShell: $env:GITHUB_TOKEN='ghp_xxxx')
    python _publish_github.py

或把 token 写进 _gh_token.txt 后直接运行。
"""
import base64
import json
import os
import sys
import urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
REPO = 'kill-the-clove'
DESC = '刺杀暮蝶 · 潜行皮蛋 — 纯前端 canvas 潜行小游戏（HTML5 重制）'
SKIP_EXT = {'.pyc'}
SKIP_NAME = {'_gh_token.txt', '_publish_github.py'}
SKIP_DIR = {'__pycache__', '.git'}

TOKEN = os.environ.get('GITHUB_TOKEN') or ''
tf = os.path.join(BASE, '_gh_token.txt')
if not TOKEN and os.path.exists(tf):
    TOKEN = open(tf).read().strip()
if not TOKEN:
    print('缺少 token：设置环境变量 GITHUB_TOKEN 或写入 _gh_token.txt')
    sys.exit(1)

API = 'https://api.github.com'


def req(method, path, data=None):
    url = API + path
    body = json.dumps(data).encode() if data is not None else None
    r = urllib.request.Request(url, data=body, method=method, headers={
        'Authorization': 'Bearer ' + TOKEN,
        'Accept': 'application/vnd.github+json',
        'Content-Type': 'application/json',
        'User-Agent': 'assassinate-king-publisher',
    })
    try:
        with urllib.request.urlopen(r, timeout=60) as resp:
            return resp.status, json.loads(resp.read().decode() or '{}')
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or '{}')


st, me = req('GET', '/user')
if st != 200:
    print('token 无效或 API 不通:', st, me.get('message'))
    sys.exit(1)
owner = me['login']
print('登录用户:', owner)

st, res = req('POST', '/user/repos', {
    'name': REPO, 'description': DESC, 'private': False, 'auto_init': False,
    'has_issues': True, 'has_wiki': False, 'license_template': 'mit',
})
if st == 201:
    print('仓库已创建:', res['full_name'])
elif st == 422 and 'already exists' in json.dumps(res):
    print('仓库已存在，继续上传')
else:
    print('创建仓库失败:', st, json.dumps(res)[:200])
    sys.exit(1)

# 收集文件
files = []
for root, dirs, names in os.walk(BASE):
    dirs[:] = [d for d in dirs if d not in SKIP_DIR]
    for n in names:
        if n in SKIP_NAME or os.path.splitext(n)[1] in SKIP_EXT:
            continue
        p = os.path.join(root, n)
        rel = os.path.relpath(p, BASE).replace('\\', '/')
        files.append((rel, p))
print('待上传文件:', len(files))

# 1) blobs
tree = []
for rel, p in files:
    data = open(p, 'rb').read()
    st, b = req('POST', '/repos/%s/%s/git/blobs' % (owner, REPO),
                {'content': base64.b64encode(data).decode(), 'encoding': 'base64'})
    if st not in (200, 201):
        print('blob 失败', rel, st, json.dumps(b)[:160])
        sys.exit(1)
    tree.append({'path': rel, 'mode': '100644', 'type': 'blob', 'sha': b['sha']})
    print('  blob', rel, len(data))

# 2) tree
st, t = req('POST', '/repos/%s/%s/git/trees' % (owner, REPO), {'tree': tree})
if st not in (200, 201):
    print('tree 失败', st, json.dumps(t)[:200]); sys.exit(1)

# 3) commit
st, c = req('POST', '/repos/%s/%s/git/commits' % (owner, REPO),
            {'message': 'feat: 刺杀暮蝶 · 潜行皮蛋（首次开源）', 'tree': t['sha'], 'parents': []})
if st not in (200, 201):
    print('commit 失败', st, json.dumps(c)[:200]); sys.exit(1)

# 4) 指向 main
st, ref = req('POST', '/repos/%s/%s/git/refs' % (owner, REPO),
              {'ref': 'refs/heads/main', 'sha': c['sha']})
if st not in (200, 201):
    st, ref = req('PATCH', '/repos/%s/%s/git/refs/heads/main' % (owner, REPO), {'sha': c['sha']})
if st in (200, 201):
    print('完成: https://github.com/%s/%s' % (owner, REPO))
else:
    print('refs 失败', st, json.dumps(ref)[:200])
