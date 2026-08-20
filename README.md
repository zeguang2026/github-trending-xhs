# github-trending-xhs

把 GitHub Trending 实时榜单变成可直接发布的小红书 carousel 图文（封面 + 10 张单项目卡片）。

## 这是什么

一个 WorkBuddy Skill，自动化「爬取 GitHub Trending → 生成小红书图文 → 导出 PNG」全流程。

## 产出

- 文案 `.md`：Top5 正文 + 固定结尾话术（含防限流分写）
- 单页卡片 SVG：竖版 3:4，9 部分结构（顶部标识 / 排名 / 原名 / 定义 / 数据 pill / 一句话看懂 / 核心卖点 / 适合谁 / 页脚）
- 汇总封面：排行榜 + 进度条
- 2x PNG 打包 zip，直接上传小红书

## 目录结构

```
github-trending-xhs/
├── SKILL.md                       # 工作流与关键约束
├── README.md                      # 本文件
├── references/
│   └── conventions.md             # 标题/正文模板、图片规格、合规要点
└── scripts/
    ├── generate_card_v2.py        # 日榜 10 张卡片（竖版 3:4）
    ├── render_png.py              # 日榜渲染 2x PNG + 打包
    ├── generate_dimension.py      # 周榜/月榜 10 张卡片 + 封面
    └── render_dimension_png.py    # 周榜/月榜渲染 2x PNG + 打包
```

## 使用

在 WorkBuddy 中调用本 skill，说「做一期 GitHub 爆款」「今日 GitHub 新增星标 Top10」「每天更新一期 GitHub」即可。

流程自动执行：

1. **抓数据**：WebFetch 抓 `https://github.com/trending?since=daily`（或 `weekly`/`monthly`），取 Top10 的星数 / 本期新增 / Fork / 语言。
2. **写文案**：按 `references/conventions.md` 模板生成，正文只写 Top5、≤1000 字、固定结尾话术。
3. **生成卡片**：`scripts/generate_card_v2.py` 填数据 → 生成 10 张 SVG。
4. **生成封面**：排行列表 + 进度条。
5. **导出 PNG**：`scripts/render_png.py` 用 Playwright 渲染 2x PNG 并打包 zip。

## 依赖

- Python 3
- Playwright + 本地 chromium（脚本自动探测 `chromium_headless_shell`，无需 cairo/rsvg）

## 数据来源

GitHub Trending（daily / weekly / monthly），通过 WebFetch 实时抓取。

> 官方 Trending 无历史日榜接口；如需回看某天榜单，需借助第三方历史归档（OSS Insight / TrendShift 等）或自建每日爬取存档。

## 合规要点

小红书发布注意防限流：不写「关注我 / 收藏 / 评论区」原文，用分写 / emoji 替换；互动提问要自然，避免硬性诱导。详见 `SKILL.md` 与 `references/conventions.md`。
