# -*- coding: utf-8 -*-
"""按 reference 9 部分结构生成周榜/月榜的 10 张卡片 + 封面（竖版 3:4）。

用法：
    python generate_dimension.py weekly
    python generate_dimension.py monthly

输出：
    skill_cards_weekly/skill_01~10_*.svg + github_weekly_top10.html
    skill_cards_monthly/skill_01~10_*.svg + github_monthly_top10.html
"""
import html
import os
import sys

STAR_PATH = "M12 2l3.09 6.26 6.91.84-5 4.87 1.18 6.88L12 17.77 6.82 21l1.18-6.88-5-4.87 6.91-.84z"
COLORS = ['#FF2442', '#A855F7', '#3B82F6', '#22C55E', '#F59E0B',
          '#06B6D4', '#F97316', '#EC4899', '#8B5CF6', '#10B981']


def fmt(n: int) -> str:
    if n >= 1000:
        return f"{n/1000:.1f}k"
    return str(n)


def char_w(ch: str) -> float:
    return 1.0 if ord(ch) > 0x2E80 else 0.55


def wrap(text: str, font_size: int, max_px: int) -> list[str]:
    lines, cur, w = [], "", 0.0
    for ch in text:
        cw = char_w(ch) * font_size
        if w + cw > max_px and cur:
            lines.append(cur)
            cur, w = ch, cw
        else:
            cur += ch
            w += cw
    if cur:
        lines.append(cur)
    return lines


WEEKLY = [
    {"rank": 1, "cn_name": "Claude Code 图表库", "repo": "diagram-design", "owner": "cathrynlavery",
     "lang": "HTML", "stars": 18_981, "forks": 1_151, "gain": 14_735,
     "define": "为 Claude Code 准备的 29 种编辑级图表模板，用自包含 HTML+SVG 输出，强调清晰、克制、可编辑的视觉表达。",
     "tldr": "让 Claude Code 生成更专业的编辑级图表",
     "points": ["内置 29 种图表类型", "使用自包含 HTML 与 SVG", "避免模板化阴影和 Mermaid 风格"],
     "audience": "内容创作者、设计师、Claude Code 用户",
     "url": "github.com/cathrynlavery/diagram-design"},
    {"rank": 2, "cn_name": "自进化编程 Agent", "repo": "prime-agent", "owner": "PrimeIntellect-ai",
     "lang": "TypeScript", "stars": 16_393, "forks": 1_760, "gain": 8_488,
     "define": "一个会自我进化的强化学习 Agent，专攻编程工作流与长任务自主执行。",
     "tldr": "让 Agent 自己迭代变强，少人工干预",
     "points": ["自我进化(RLM)", "擅长长任务自主执行", "开源可本地运行"],
     "audience": "AI 研究者、自动化工程师",
     "url": "github.com/PrimeIntellect-ai/prime-agent"},
    {"rank": 3, "cn_name": "图原生 AI 基础设施", "repo": "semantica", "owner": "semantica-agi",
     "lang": "Python", "stars": 8_017, "forks": 819, "gain": 5_339,
     "define": "面向 AI 系统的「图原生」基础设施，管理上下文与可追责的 AI 系统。",
     "tldr": "给 AI Agent 一套图结构记忆与溯源底座",
     "points": ["图原生架构", "统一上下文管理", "可追责 AI 系统"],
     "audience": "AI 基础设施开发者",
     "url": "github.com/semantica-agi/semantica"},
    {"rank": 4, "cn_name": "腾讯 Agent 团队记忆中枢", "repo": "TencentDB-Agent-Memory", "owner": "TencentCloud",
     "lang": "TypeScript", "stars": 22_053, "forks": 2_023, "gain": 3_956,
     "define": "腾讯团队的 Agent 团队级记忆中枢，把对话、文档、代码转成 4 类可复用记忆资产。",
     "tldr": "让多个 Agent 共享一套团队记忆",
     "points": ["团队级记忆中枢", "4 类复用记忆资产", "跨框架通用"],
     "audience": "企业 AI 团队",
     "url": "github.com/TencentCloud/TencentDB-Agent-Memory"},
    {"rank": 5, "cn_name": "AI 编程生产级技能库", "repo": "agent-skills", "owner": "addyosmani",
     "lang": "JavaScript", "stars": 87_574, "forks": 9_384, "gain": 3_300,
     "define": "给 AI 编程 Agent 用的生产级 engineering skills 合集。",
     "tldr": "给 AI 编程助手一套现成最佳实践",
     "points": ["生产级工程技能", "覆盖主流工程实践", "Addy Osmani 出品"],
     "audience": "用 AI 写代码的开发者",
     "url": "github.com/addyosmani/agent-skills"},
    {"rank": 6, "cn_name": "14MB 端侧小模型", "repo": "needle", "owner": "cactus-compute",
     "lang": "Python", "stars": 6_199, "forks": 412, "gain": 2_488,
     "define": "只有 14MB 的端侧基础模型，能跑在手机、穿戴、智能家居和机器人上。",
     "tldr": "把小模型塞进手机和机器人里跑",
     "points": ["仅 14MB 超小体积", "端侧本地运行护隐私", "面向手机/穿戴/机器人"],
     "audience": "端侧 AI 开发者、硬件团队",
     "url": "github.com/cactus-compute/needle"},
    {"rank": 7, "cn_name": "团队统一工作区", "repo": "macro", "owner": "macro-inc",
     "lang": "Rust", "stars": 3_307, "forks": 330, "gain": 2_434,
     "define": "团队统一工作区：邮件、聊天、文档、任务、AI、CRM 全 @ 联动。",
     "tldr": "把团队工具收进一个带 AI 记忆的工作区",
     "points": ["统一工作区", "AI 共享记忆", "@ 联动各模块"],
     "audience": "团队协作者",
     "url": "github.com/macro-inc/macro"},
    {"rank": 8, "cn_name": "管理公司 Agent 的开源应用", "repo": "paperclip", "owner": "paperclipai",
     "lang": "TypeScript", "stars": 78_362, "forks": 14_364, "gain": 2_430,
     "define": "开源应用，统一管理公司里跑的各种 AI Agent。",
     "tldr": "给企业的 Agent 一个统一管理中心",
     "points": ["开源", "集中管理 Agent", "企业级能力"],
     "audience": "企业 IT / AI 负责人",
     "url": "github.com/paperclipai/paperclip"},
    {"rank": 9, "cn_name": "数学科普动画引擎", "repo": "manim", "owner": "3b1b",
     "lang": "Python", "stars": 91_270, "forks": 7_549, "gain": 2_008,
     "define": "3Blue1Brown 出品的教学数学动画引擎。",
     "tldr": "用代码做高质量数学科普视频",
     "points": ["数学动画引擎", "开源经典项目", "社区庞大"],
     "audience": "教育者、科普作者",
     "url": "github.com/3b1b/manim"},
    {"rank": 10, "cn_name": "给 Agent 配一台电脑", "repo": "computer", "owner": "cloudflare",
     "lang": "TypeScript", "stars": 8_292, "forks": 450, "gain": 1_966,
     "define": "Cloudflare 出的工具，给 AI Agent 配一台可操作的「电脑」。",
     "tldr": "让 Agent 像人一样用电脑",
     "points": ["给 Agent 一台电脑", "Cloudflare 出品", "自动化操作界面"],
     "audience": "Agent 开发者",
     "url": "github.com/cloudflare/computer"},
]

MONTHLY = [
    {"rank": 1, "cn_name": "工程师技能库", "repo": "skills", "owner": "mattpocock",
     "lang": "Shell", "stars": 218_695, "forks": 18_842, "gain": 47_580,
     "define": "来自 Matt Pocock .agents 目录的「真工程师」技能合集。",
     "tldr": "前端大佬的 AI 编程最佳实践打包",
     "points": ["实战工程技能", "Matt Pocock 出品", "Shell 配置即用"],
     "audience": "TypeScript / 前端开发者",
     "url": "github.com/mattpocock/skills"},
    {"rank": 2, "cn_name": "免费 AI 网关", "repo": "OmniRoute", "owner": "diegosouzapw",
     "lang": "TypeScript", "stars": 48_764, "forks": 6_639, "gain": 31_196,
     "define": "一个端点接 339 家供应商、1200+ 模型（含 90+ 免费）的 MIT 免费 AI 网关。",
     "tldr": "一套 API 调遍所有大模型，还能自动 fallback",
     "points": ["339 家供应商接入", "90+ 免费模型", "配额感知自动 fallback"],
     "audience": "用多家大模型的开发者",
     "url": "github.com/diegosouzapw/OmniRoute"},
    {"rank": 3, "cn_name": "并行 Agent 工作台", "repo": "orca", "owner": "stablyai",
     "lang": "TypeScript", "stars": 46_275, "forks": 3_235, "gain": 26_744,
     "define": "管理一组并行 Agent 的 ADE，用你自己的订阅跑任意编程 Agent。",
     "tldr": "一台机器同时跑多个 Agent 干活",
     "points": ["并行 Agent 管理", "用自己的订阅", "桌面/移动/VPS"],
     "audience": "重度 Agent 用户",
     "url": "github.com/stablyai/orca"},
    {"rank": 4, "cn_name": "全球态势监控面板", "repo": "worldmonitor", "owner": "koala73",
     "lang": "TypeScript", "stars": 82_228, "forks": 12_278, "gain": 20_570,
     "define": "实时全球情报面板：AI 聚合新闻、地缘监控、基础设施追踪。",
     "tldr": "一个看板掌握全球动态",
     "points": ["实时全球情报", "AI 聚合新闻", "统一态势界面"],
     "audience": "关注宏观/情报的人",
     "url": "github.com/koala73/worldmonitor"},
    {"rank": 5, "cn_name": "AI Agent 工具箱", "repo": "pi", "owner": "earendil-works",
     "lang": "TypeScript", "stars": 91_079, "forks": 11_304, "gain": 19_831,
     "define": "AI Agent 工具箱：统一 LLM API、Agent 循环、TUI、编程 Agent CLI。",
     "tldr": "一站式搭 Agent 的底层工具",
     "points": ["统一 LLM API", "Agent 循环", "TUI/CLI 工具"],
     "audience": "Agent 框架开发者",
     "url": "github.com/earendil-works/pi"},
    {"rank": 6, "cn_name": "反 AI 味设计技能", "repo": "hallmark", "owner": "Nutlope",
     "lang": "CSS", "stars": 25_185, "forks": 1_280, "gain": 18_188,
     "define": "给 Claude Code/Cursor/Codex 的「反 AI 腔」设计技能。",
     "tldr": "让 AI 生成的设计不像 AI 做的",
     "points": ["反 AI-slop 设计", "多客户端通用", "设计技能包"],
     "audience": "做产品的设计师/开发者",
     "url": "github.com/Nutlope/hallmark"},
    {"rank": 7, "cn_name": "逆向/安全技能路由包", "repo": "reverse-skill", "owner": "zhaoxuya520",
     "lang": "PowerShell", "stars": 25_559, "forks": 3_460, "gain": 17_376,
     "define": "逆向、授权渗透、安全研究的技能路由包，AI 自动路由+按需自举工具链。",
     "tldr": "给安全研究的 AI 技能包（仅限授权用途）",
     "points": ["安全技能路由", "AI 自动路由", "仅限授权渗透测试"],
     "audience": "安全研究员（授权用途）",
     "url": "github.com/zhaoxuya520/reverse-skill"},
    {"rank": 8, "cn_name": "腾讯 Agent 团队记忆中枢", "repo": "TencentDB-Agent-Memory", "owner": "TencentCloud",
     "lang": "TypeScript", "stars": 22_062, "forks": 2_023, "gain": 13_073,
     "define": "腾讯团队的 Agent 团队级记忆中枢，把对话、文档、代码转成 4 类记忆资产。",
     "tldr": "让多个 Agent 共享团队记忆",
     "points": ["团队级记忆中枢", "4 类复用记忆资产", "跨框架通用"],
     "audience": "企业 AI 团队",
     "url": "github.com/TencentCloud/TencentDB-Agent-Memory"},
    {"rank": 9, "cn_name": "书转 Claude 技能", "repo": "book-to-skill", "owner": "virgiliojr94",
     "lang": "Python", "stars": 21_961, "forks": 2_316, "gain": 13_193,
     "define": "把任意技术书 PDF 转成 Claude Code skill，边干活边学。",
     "tldr": "一本书变成可调用的工作技能",
     "points": ["PDF 转 skill", "边学边用", "Claude Code 集成"],
     "audience": "学习者、知识工作者",
     "url": "github.com/virgiliojr94/book-to-skill"},
    {"rank": 10, "cn_name": "本地代码审查图谱", "repo": "code-review-graph", "owner": "tirth8205",
     "lang": "Python", "stars": 30_295, "forks": 2_770, "gain": 10_869,
     "define": "本地优先的代码智能图谱，给 MCP/CLI 用，让 AI 只读关键代码。",
     "tldr": "给 AI 审查代码一张地图，省 token",
     "points": ["本地优先", "代码智能图谱", "MCP/CLI 支持"],
     "audience": "代码审查/大仓开发者",
     "url": "github.com/tirth8205/code-review-graph"},
]


def render(p: dict, period_word: str) -> str:
    W, H = 1200, 1600
    M = 70
    CW = W - 2 * M
    repo = html.escape(p["repo"])
    cn_name = html.escape(p["cn_name"])
    rank = f"#{p['rank']}"
    page = f"{p['rank']:02d} / 10"

    top_y, line_y = 92, 132
    rank_block_y, rank_block_h = 158, 118
    cn_name_y = rank_block_y + rank_block_h / 2 + 14
    repo_y = 352

    define_lines = wrap(p["define"], 36, CW - 20)
    define_start_y, define_line_h = 430, 58
    define_end = define_start_y + len(define_lines) * define_line_h

    pill_w = [160, 250, 260, 168]
    pill_gap = 22
    pill_h = 100
    total_pill_w = sum(pill_w) + pill_gap * (len(pill_w) - 1)
    pill_x0 = M + (CW - total_pill_w) / 2
    pill_y = define_end + 56

    tldr_lines = wrap(p["tldr"], 38, CW - 90)
    card_y = pill_y + pill_h + 56
    card_h = 112 + len(tldr_lines) * 56

    points_start_y = card_y + card_h + 52
    point_line_h = 64

    audience_title_y = points_start_y + 3 * point_line_h + 34
    audience_text_y = audience_title_y + 48

    bottom_line_y = audience_text_y + 62
    bottom_text_y = bottom_line_y + 40

    define_svg = "".join(
        f'<text x="{M}" y="{define_start_y + i * define_line_h}" font-size="36" fill="#444444" font-family="-apple-system, PingFang SC, Microsoft YaHei, sans-serif">{html.escape(ln)}</text>'
        for i, ln in enumerate(define_lines)
    )

    px = [pill_x0 + sum(pill_w[:i]) + pill_gap * i for i in range(len(pill_w))]
    pill_texts = [p["lang"], f"{fmt(p['stars'])}", f"+{p['gain']:,} {period_word}", f"{fmt(p['forks'])} Fork"]
    pill_fills = ["#F5F5F7", "#F5F5F7", "#E8F8EE", "#F5F5F7"]
    pill_colors = ["#555555", "#333333", "#07C160", "#333333"]

    pills_svg = ""
    for i, (x, w, txt, fill, color) in enumerate(zip(px, pill_w, pill_texts, pill_fills, pill_colors)):
        pills_svg += f'<rect x="{x:.1f}" y="0" width="{w}" height="{pill_h}" rx="{pill_h/2:.0f}" fill="{fill}"/>'
        if i == 1:
            icon_w, text_w = 38, len(txt) * 20 + 6
            inner_x = x + (w - icon_w - text_w) / 2
            pills_svg += f'<svg x="{inner_x:.1f}" y="21" width="38" height="38" viewBox="0 0 24 24" fill="#FFB800"><path d="{STAR_PATH}"/></svg>'
            pills_svg += f'<text x="{inner_x + icon_w + 6:.1f}" y="58" font-size="38" fill="{color}" font-family="-apple-system, PingFang SC, Microsoft YaHei, sans-serif" font-weight="700">{html.escape(txt)}</text>'
        else:
            pills_svg += f'<text x="{x+w/2:.1f}" y="58" font-size="38" fill="{color}" font-family="-apple-system, PingFang SC, Microsoft YaHei, sans-serif" text-anchor="middle" font-weight="700">{html.escape(txt)}</text>'

    points_svg = "".join(
        f'<g transform="translate({M},{points_start_y + i * point_line_h})">'
        f'<circle cx="9" cy="-14" r="8" fill="#07C160"/>'
        f'<text x="38" y="0" font-size="34" fill="#333333" font-family="-apple-system, PingFang SC, Microsoft YaHei, sans-serif">{html.escape(pt)}</text>'
        f"</g>"
        for i, pt in enumerate(p["points"])
    )

    tldr_svg = "".join(
        f'<text x="44" y="{108 + i * 56}" font-size="38" font-weight="700" fill="#FFFFFF" font-family="-apple-system, PingFang SC, Microsoft YaHei, sans-serif">{html.escape(ln)}</text>'
        for i, ln in enumerate(tldr_lines)
    )

    period_label = "本周榜" if period_word == "本周" else "本月榜"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="{W}" height="{H}" fill="#ffffff"/>
  <text x="{M}" y="{top_y}" font-size="34" fill="#999999" font-family="-apple-system, PingFang SC, Microsoft YaHei, sans-serif" font-weight="600">GitHub 爆火项目榜</text>
  <text x="{W-M}" y="{top_y}" font-size="34" fill="#999999" font-family="-apple-system, PingFang SC, Microsoft YaHei, sans-serif" text-anchor="end">{period_label}</text>
  <line x1="{M}" y1="{line_y}" x2="{W-M}" y2="{line_y}" stroke="#EEEEEE" stroke-width="2"/>
  <rect x="{M}" y="{rank_block_y}" width="{rank_block_h}" height="{rank_block_h}" rx="24" fill="#FF2442"/>
  <text x="{M+rank_block_h/2}" y="{rank_block_y + rank_block_h/2 + 18}" font-size="58" font-weight="800" fill="#ffffff" font-family="-apple-system, PingFang SC, Microsoft YaHei, sans-serif" text-anchor="middle">{rank}</text>
  <text x="{M+rank_block_h+22}" y="{cn_name_y}" font-size="44" font-weight="700" fill="#222222" font-family="-apple-system, PingFang SC, Microsoft YaHei, sans-serif">{cn_name}</text>
  <text x="{M}" y="{repo_y}" font-size="92" font-weight="800" fill="#111111" font-family="-apple-system, PingFang SC, Microsoft YaHei, sans-serif">{repo}</text>
  {define_svg}
  <g transform="translate(0, {pill_y})">
    {pills_svg}
  </g>
  <g transform="translate({M}, {card_y})">
    <rect x="0" y="0" width="{CW}" height="{card_h}" rx="22" fill="#1A1A1A"/>
    <text x="44" y="50" font-size="24" fill="#999999" font-family="-apple-system, PingFang SC, Microsoft YaHei, sans-serif" font-weight="600">一句话看懂</text>
    {tldr_svg}
  </g>
  {points_svg}
  <text x="{M}" y="{audience_title_y}" font-size="30" fill="#888888" font-family="-apple-system, PingFang SC, Microsoft YaHei, sans-serif" font-weight="600">适合谁？</text>
  <text x="{M}" y="{audience_text_y}" font-size="38" fill="#333333" font-family="-apple-system, PingFang SC, Microsoft YaHei, sans-serif">{html.escape(p['audience'])}</text>
  <line x1="{M}" y1="{bottom_line_y}" x2="{W-M}" y2="{bottom_line_y}" stroke="#EEEEEE" stroke-width="2"/>
  <text x="{M}" y="{bottom_text_y}" font-size="28" fill="#999999" font-family="-apple-system, PingFang SC, Microsoft YaHei, sans-serif">https://{html.escape(p['url'])}</text>
  <text x="{W-M}" y="{bottom_text_y}" font-size="28" fill="#999999" font-family="-apple-system, PingFang SC, Microsoft YaHei, sans-serif" text-anchor="end">{page}</text>
</svg>"""


def cover_html(data: list, period_word: str, period_en: str) -> str:
    max_gain = max(d["gain"] for d in data)
    items = ""
    for d in data:
        pct = max(4, round(d["gain"] / max_gain * 100))
        c = COLORS[d["rank"] - 1]
        items += (f'<div class="item"><div class="rk" style="background:{c}">#{d["rank"]}</div>'
                  f'<div class="main"><div class="nm">{html.escape(d["repo"])}</div>'
                  f'<div class="bar-wrap"><div class="bar" style="width:{pct}%;background:{c}"></div></div></div>'
                  f'<div class="num">+{d["gain"]:,}</div></div>\n')
    issue = "本周榜" if period_word == "本周" else "本月榜"
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GitHub {period_word}新增星标 Top10</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ background: #e8e8e5; font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif; display: flex; justify-content: center; padding: 28px 16px; }}
  .poster {{ width: 1080px; height: 1440px; background: #f7f7f4; border-radius: 32px; padding: 64px 58px 48px; box-shadow: 0 30px 80px rgba(0,0,0,.12); display: flex; flex-direction: column; }}
  .head {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px; }}
  .issue {{ font-size: 24px; color: #999999; font-weight: 500; letter-spacing: 1px; margin-top: 8px; }}
  .title-wrap {{ margin-bottom: 40px; }}
  h1 {{ font-size: 72px; font-weight: 800; color: #1a1a1a; letter-spacing: 1px; line-height: 1.1; }}
  .sub {{ font-size: 26px; color: #888888; margin-top: 14px; font-weight: 500; }}
  .list {{ flex: 1; display: flex; flex-direction: column; gap: 18px; }}
  .item {{ display: flex; align-items: center; gap: 22px; background: #ffffff; border-radius: 20px; padding: 22px 26px; box-shadow: 0 4px 14px rgba(0,0,0,.04); }}
  .rk {{ flex: 0 0 58px; width: 58px; height: 58px; border-radius: 14px; color: #fff; font-size: 24px; font-weight: 800; display: flex; align-items: center; justify-content: center; }}
  .main {{ flex: 1; min-width: 0; }}
  .nm {{ font-size: 26px; font-weight: 700; color: #1a1a1a; margin-bottom: 10px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
  .bar-wrap {{ width: 560px; height: 12px; background: #ededea; border-radius: 999px; overflow: hidden; }}
  .bar {{ height: 100%; border-radius: 999px; min-width: 4px; }}
  .num {{ flex: 0 0 130px; text-align: right; font-size: 28px; font-weight: 700; color: #07C160; }}
  .footer {{ margin-top: 30px; display: flex; justify-content: space-between; align-items: center; font-size: 20px; color: #aaaaaa; }}
</style>
</head>
<body>
  <div class="poster">
    <div class="head">
      <div class="title-wrap">
        <h1>GitHub 爆火项目榜</h1>
        <div class="sub">Top10 · {period_word}新增星标精选</div>
      </div>
      <div class="issue">{issue}</div>
    </div>
    <div class="list">
      {items}
    </div>
    <div class="footer">
      <span>数据：GitHub Trending {period_en}榜 · 2026.08.16</span>
      <span>{period_word}更新</span>
    </div>
  </div>
</body>
</html>"""


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "weekly"
    base = "/Users/peterli/WorkBuddy/2026-08-16-12-24-51"
    if mode == "weekly":
        data, period_word, period_en, card_dir, cover_file = WEEKLY, "本周", "周", "skill_cards_weekly", "github_weekly_top10.html"
    else:
        data, period_word, period_en, card_dir, cover_file = MONTHLY, "本月", "月", "skill_cards_monthly", "github_monthly_top10.html"

    os.makedirs(f"{base}/{card_dir}", exist_ok=True)
    for p in data:
        fname = f"skill_{p['rank']:02d}_{p['repo']}.svg"
        with open(f"{base}/{card_dir}/{fname}", "w", encoding="utf-8") as f:
            f.write(render(p, period_word))
        print("written:", fname)
    with open(f"{base}/{cover_file}", "w", encoding="utf-8") as f:
        f.write(cover_html(data, period_word, period_en))
    print("cover:", cover_file)
