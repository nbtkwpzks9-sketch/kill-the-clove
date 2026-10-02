# 刺杀暮蝶 · 潜行皮蛋

一个纯前端（单页 canvas）的潜行小游戏：你是**皮蛋**，要尾随并刺杀背对你的**暮蝶**。
原玩法来自经典 Flash 小游戏《刺杀国王》，本仓库是 HTML5 重制版。

- 仓库：https://github.com/nbtkwpzks9-sketch/kill-the-clove
- 在线试玩（B站 Toy）：https://www.bilibili.com/toy/assassinate-king/index.html

## 玩法

- **按住** 鼠标 / 空格 = 前进；**松手** = 立刻停住
- 第一段：穿过披萨店街道（`scene1`）
- 第二段：进入后院，暮蝶就在那里（`scene2`）
- 暮蝶**背对你**时可以前进；他一**回头（⚠）**必须立刻松手，否则被抓进地牢
- 3 条命；摸到暮蝶背后即可刺杀

## 目录结构

```
index.html          游戏全部逻辑（HTML+CSS+JS 单文件，方便直接部署）
assets/             素材
  scene1.jpg        场景一（披萨店街道，16:9）
  scene2.jpg        场景二（后院，16:9）
  king_sleep.png    暮蝶 · 睡觉态（背对玩家，抠像透明）
  king_alert.png    暮蝶 · 警觉态（回头，持枪，抠像透明）
  spy_sneak_cut.png 皮蛋 · 静止（抠像透明，426x240）
  spy_walk_sheet.png 皮蛋 · 走路 3 帧精灵表（1278x240 = 3 x 426x240）
  intro.mp4         开场视频
  fail.mp4          失败视频（命尽）
  win.mp4           通关视频
_cutout_spy.py      走路 GIF 抠像 -> 精灵表（中位数背景 + 差分 + grabCut）
_cutout_sneak.py    潜行图单独抠像（grabCut，因与 GIF 不同机位）
_crop_scenes.py     场景图居中裁成 16:9
_prep_assets.py     原始素材搬入并统一定向
_prep_video.py      视频转码为 720p H.264+AAC
_rename.py          文案批量改名
_qa.js / _qa_live.js 本地与线上无头浏览器自检
```

## 本地运行

```bash
# 任意静态服务器即可（不要直接用 file://，路径与视频加载会有问题）
python -m http.server 8000
# 打开 http://127.0.0.1:8000/index.html
```

## 渲染设计（改动前请先读）

- **逻辑坐标固定 960×540（16:9）**，所有游戏坐标都在这个坐标系里
- canvas 物理尺寸 = 窗口实际像素；绘制分两层变换：
  - **世界层 cover**：`scale = max(vw/W, vh/H)`，铺满窗口**只裁切不拉伸**；窗口比 16:9 更扁时**底部对齐**（保地面，裁天空）
  - **UI 层 fit**：`scale = min(...)`，HUD 任何比例下完整可见
- **地面线** `FOOT_Y = H * 0.92`，对齐场景图里的人行道/后院地面
- 角色贴图**保持原始 16:9 画幅**（426×240），只把背景抠透明，**不要裁剪画框**，否则比例会变
- 走路动画是**精灵表逐帧播放**（130ms/帧），不依赖 GIF 在 canvas 里自动播放
- 每帧自检窗口尺寸并给 320×240 兜底 —— Toy 内嵌 WebView 可能 `window.innerWidth = 0` 导致 canvas 0×0 全黑

## 发布到 B站 Toy

```bash
toy update 37382787422208 . --poster poster.png --icon icon.png --yes
# 改名：
toy update 37382787422208 --title "刺杀暮蝶 · 潜行皮蛋" --yes
```

## 素材与版权（重要）

- 角色形象取自 Riot Games《无畏契约》（暮蝶 Clove / 皮蛋），相关美术版权归原作者所有
- 场景与视频为自制 / AI 生成素材
- 本项目仅供学习交流，**禁止商用**；若你是权利人，请提 issue 联系下架
- 代码部分见 [LICENSE](./LICENSE)（MIT）

## 欢迎共创

请先看 [CONTRIBUTING.md](./CONTRIBUTING.md)。欢迎：新关卡/新场景、更好的抠像算法、
移动端适配、音效、排行榜、剧情分支。
