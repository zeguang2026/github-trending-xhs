---
name: github-trending-xhs
description: "Generate Xiaohongshu (小红书) 今日 GitHub 新增星标 Top10 carousel content from live GitHub Trending data, including copywriting, a 9-section per-project card SVG (竖版 3:4), a cover info-graphic, and PNG export. Use when the user wants to produce, schedule, or republish a daily or weekly GitHub trending post for Xiaohongshu."
agent_created: true
---

# GitHub Trending → 小红书图文

把 GitHub Trending 实时榜单变成可直接发布的小红书 carousel 图文（封面 + 10 张单项目卡片）。
整套产出：文案 `.md`、单页卡片 `skill_cards/skill_XX_*.svg`、汇总封面 `*.html`、以及导出用 PNG。

## 何时使用

- 用户说「做一期 GitHub 爆款」「今日 GitHub 新增星标 Top10」「每天更新一期 GitHub」等。
- 用户要更新/重排/换周期（日榜/周榜）已有内容。
- 用户要导出 PNG/JPG 方便上传小红书，或建定时自动化。

## 工作流

1. **抓数据**：用 WebFetch 抓 `https://github.com/trending?since=daily`（日榜）或 `since=weekly`（周榜）。
   对每张卡若要精确星数/Fork，单独抓 `https://github.com/owner/repo`。
   取 Top 10，记录：排名、owner/repo、语言、总星数、本期新增（stars today/this week）、Fork 数。
   保持「本期新增」降序作为排名依据（与卡片图一致）。

2. **写文案**：按 `references/conventions.md` 的标题格式与正文模板生成。
   硬约束：**正文只写 Top5 项目、字数 ≤ 1000、结尾固定用引流话术**（见约定文档，不要分三行写）。
   正文用用户确认的版本（含防限流分写：收cang / 关🐷我 / 平仑区），注意分行、不要违规诱导互动。
   文案存为 `github_today_top10_post.md`。
   （卡片图/封面仍出完整 Top10，靠正文结尾「左滑看更多」引导看剩余 5 张。）

3. **生成卡片**：用 `scripts/generate_card_v2.py`。把第 1 步的 10 条数据填进脚本顶部的 `ALL` 数组，
   运行即生成 `skill_cards/skill_01~10_*.svg`（竖版 3:4，9 部分结构，仅数据 pill 行放大）。

4. **生成封面**：用 `scripts/` 里的封面生成逻辑或现有 `github_today_top10.html` 模板，
   渲染为竖版 3:4 封面（浅色背景 + 顶部大标题/期数 + Top10 排行列表：排名色块+项目名+进度条+本期新增绿字）。

5. **导出 PNG**：用 `scripts/render_png.py` 把卡片 SVG 与封面 HTML 渲染成 2x PNG
   （卡片 2400×3200、封面 2160×2880），并 `zip -qj` 打包成 `github_xhs_export.zip` 供下载。
   本机无 cairo/rsvg，渲染走 Playwright + 已装的 chromium_headless_shell（见脚本内 `EXEC` 自动探测）。

6. **预览/交付**：用 present_files 给出 zip 与若干 PNG 预览，告知发布顺序（封面第 1 张、卡片 2~11 张）。

## 关键约束（务必遵守）

- 比例一律**竖版 3:4**（小红书图文最推荐，展示面积最大）。卡片 1200×1600，封面 1080×1440。
- 单页卡片结构固定 9 部分：顶部标识 / 排名红块+中文名 / 项目原名 / 定义 / 数据 pill（语言·星标·本期新增绿标·Fork）/ 一句话看懂深色卡 / 核心卖点 / 适合谁 / 底部链接+页码。
- 数据 pill 行是画面重点：高度约 100、字号约 38、4 个 pill 横向占满内容宽；其余文字保持中等字号，避免失衡。
- 标题格式固定：`🔥今日GitHub新增星标 Top10！YYYY-MM-DD`，日期用当期日期。
- 文案合规：不写「关注我」「收藏」「评论区」原文，用分写/emoji 替换防限流；提问式互动要自然，避免硬性诱导。
- 数据以 GitHub Trending 实时抓取为准；文案里的本期新增数字必须与卡片图一致。

## 复用脚本

- `scripts/generate_card_v2.py`：参数化生成日榜 10 张竖版 3:4 卡片（改 `ALL` 数据与顶部尺寸即可）。
- `scripts/render_png.py`：Playwright 渲染日榜 SVG/HTML 为 2x PNG 并打包 zip（自动探测本机 chromium）。
- `scripts/generate_dimension.py weekly|monthly`：生成周榜/月榜 10 张卡片 + 封面 HTML。
- `scripts/render_dimension_png.py weekly|monthly`：渲染周榜/月榜为 2x PNG 并打包 zip。
- `references/conventions.md`：标题格式、正文模板、图片规格、合规要点、维度扩展（周/月榜）的完整约定。
