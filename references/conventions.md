# 小红书 GitHub 爆款 内容约定

本文件是「github-trending-xhs」skill 的硬性约定，生成文案与图片时一律照此执行。

## 1. 标题格式

```
🔥今日GitHub新增星标 Top10！2026-08-16
```

- 前缀固定 `🔥今日GitHub新增星标 Top10！`
- 后缀为当期日期，格式 `YYYY-MM-DD`（用实际抓取日）。
- 不要改成「每周」「本期第 N 期」等，除非用户明确要求。

## 2. 正文模板（含防限流分写）

> 注意：用户明确要求把「收藏 / 关注 / 评论区」用分写或 emoji 替换，避免平台判定违规诱导互动。
> 下面的「收cang / 关🐷我 / 平仑区」是**有意为之**，不要还原成原词。

**硬约束**
- 正文字数 ≤ 1000 字。
- 文案只写 **Top5** 项目（卡片图/封面仍出完整 Top10，靠「左滑看更多」引导）。
- 结尾固定用下方「引流话术」，不再分三行写。

```
今天的 GitHub 又被刷屏了

🔥 第 1 名一天就涨了 2260 个 star，

我赶紧扒了完整榜单 全是能直接抄作业的 AI / 开源神器，普通人也能上手

但 GitHub Trending 全英文，很多人看一眼就划走了 😅

榜单只给一句话描述，根本看不出「这玩意到底能干嘛」

所以我把今日新增星标 Top10 翻译成中文、说人话、还配了图 👇

-

🥇 <owner> / <repo> ｜ 今日 +<n> ⭐

<一句话大白话讲清它是啥 + 你能拿来干嘛>

🥈 ...（依排名类推，写到第 5 名 5️⃣ 即止）

❓想 get 完整内容左滑看更多📌 收cang！ 免得以后找不到👀 记得关🐷我，每天更新一期 GitHub 爆款💬 平仑区告诉我：你觉得哪个最有用？
```

- 每个项目之间空一行；项目名与描述之间空一行；描述内如原版分两行也要保留换行。
- 本期新增数字 `今日 +<n> ⭐` 必须与卡片图 pill 里的「本期新增」一致。
- 不写 hashtag 行（用户自行添加），除非用户要求。

## 3. 图片规格

### 单页卡片（每个项目一张）
- 比例：竖版 3:4，1200 × 1600（导出 PNG 2x = 2400 × 3200）。
- 9 部分从上到下：
  1. 顶部标识：`GitHub 爆火项目榜`（左）· `第 1 期`（右）
  2. 排名红块 `#N` + 中文名
  3. 项目原名（最大字号，黑色加粗）
  4. 项目定义（一句话）
  5. 数据 pill 行：语言 / 星标（⭐图标+数字）/ 本期新增（绿字高亮）/ Fork —— **只放大这一行**（高~100、字号~38、横向占满）
  6. 「一句话看懂」深色卡（#1A1A1A）
  7. 核心卖点（3 个绿点 bullet）
  8. 适合谁？
  9. 底部：GitHub 链接（左）+ `NN / 10` 页码（右）
- 其余文字保持中等字号，整体构图要撑满、别留大片空白。

### 封面（汇总图）
- 比例：竖版 3:4，1080 × 1440。
- 风格：浅色背景 + 圆角卡片；顶部大标题 `GitHub 爆火项目榜` + 副标题 `Top10 · 今日新增星标精选` + 右上角 `第 1 期`。
- 主体：Top10 排行列表，每行 = 排名色块 `#1~#10` + 项目名 + 热度进度条 + 本期新增绿字。
- 底部：数据来源 + `每天更新一期`。

## 4. 合规要点

- 不出现「关注我」「收藏」「评论区」原文（用分写/emoji 替代）。
- 互动引导用提问句式（「你觉得哪个最有用？」），不硬凑「不关注就看不到了」之类。
- 数据真实、可核验（来自 GitHub Trending），不夸大。
- holehe 等涉及隐私/安全的项目，正经用途要写清楚，加「别干坏事」式提醒。

## 5. 文件落位（默认工作目录）

- 文案：`github_today_top10_post.md`
- 卡片：`skill_cards/skill_01~10_*.svg`
- 封面：`github_today_top10.html`（汇总信息图）
- 导出：`github_xhs_export.zip`（含 11 张 PNG）
- 生成脚本：`generate_card_v2.py`、`render_png.py`

## 6. 维度扩展（周榜 / 月榜）

除日榜总榜外，可生成「本周榜 / 本月榜」维度（用户已确认要周榜+月榜做发布物料；语言筛选等其他维度用户暂不需要）：

- 标题：`🔥本周GitHub新增星标 Top10！YYYY-MM-DD` / `🔥本月GitHub新增星标 Top10！YYYY-MM-DD`（把「今日」改「本周/本月」）。
- 数据来源：`https://github.com/trending?since=weekly` / `since=monthly`，按「本周/本月新增」降序取 Top10。
- 卡片 pill 第 3 个显示 `本周 +n` / `本月 +n`（绿色高亮）；其余 9 部分结构不变。
- 文案里「今日 +n ⭐」对应改「本周 +n ⭐」/「本月 +n ⭐」；开头钩子「一天涨」「今天」改「一周涨」「本周」/「一个月涨」「本月」。
- 生成脚本：`generate_dimension.py weekly|monthly`（出卡片 SVG + 封面 HTML 到 `skill_cards_weekly/`、`skill_cards_monthly/`、`github_weekly_top10.html`、`github_monthly_top10.html`）。
- 导出脚本：`render_dimension_png.py weekly|monthly`（出 PNG 并打包 `github_weekly_export.zip` / `github_monthly_export.zip`）。
- 文件落位：
  - 周榜：文案 `github_weekly_top10_post.md`、卡片 `skill_cards_weekly/`、封面 `github_weekly_top10.html`、导出 `github_weekly_export.zip`
  - 月榜：文案 `github_monthly_top10_post.md`、卡片 `skill_cards_monthly/`、封面 `github_monthly_top10.html`、导出 `github_monthly_export.zip
