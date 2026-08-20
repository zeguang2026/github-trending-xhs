# -*- coding: utf-8 -*-
"""按参考图 9 部分结构批量生成 10 张 skill 卡片（竖版 3:4，小红书可发布）。

可编辑参数集中在 render() 顶部：W/H 画布、M 边距、各字号/间距。
竖版 3:4 = 高:宽 = 4:3，这里用 1200 x 1600。
仅「数据 pill」一行被放大（高度 100、字号 38），其余文字保持中等字号。

用法：把下方 ALL 数组替换为当期真实数据后运行：
    python generate_card_v2.py
输出到同目录 skill_cards/skill_01~10_<repo>.svg
"""
import html
import os

STAR_PATH = "M12 2l3.09 6.26 6.91.84-5 4.87 1.18 6.88L12 17.77 6.82 21l1.18-6.88-5-4.87 6.91-.84z"


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


# ===== 当期真实数据：抓 GitHub Trending 后替换这里 =====
ALL = [
    {"rank": 1, "cn_name": "免费 API 大合集", "repo": "public-apis", "owner": "public-apis",
     "lang": "Python", "stars": 460_403, "forks": 50_870, "today": 2_260,
     "define": "一份持续维护的免费公开 API 大全，按类别整理（天气 / 翻译 / 金融 / 图片…），开发者找接口不用再到处搜。",
     "tldr": "帮你一站式找齐免费 API，少走弯路",
     "points": ["收录上千个免费公开 API", "按类别清晰分类，即查即用", "社区持续维护，链接实时校验"],
     "audience": "后端 / 前端开发者、独立开发者、做原型验证的人",
     "url": "github.com/public-apis/public-apis"},
    {"rank": 2, "cn_name": "Claude Code 图表库", "repo": "diagram-design", "owner": "cathrynlavery",
     "lang": "HTML", "stars": 18_811, "forks": 1_140, "today": 1_607,
     "define": "为 Claude Code 准备的 29 种编辑级图表模板，用自包含 HTML+SVG 输出，强调清晰、克制、可编辑的视觉表达。",
     "tldr": "让 Claude Code 生成更专业的编辑级图表",
     "points": ["内置 29 种图表类型", "使用自包含 HTML 与 SVG", "避免模板化阴影和 Mermaid 风格"],
     "audience": "内容创作者、设计师、Claude Code 用户",
     "url": "github.com/cathrynlavery/diagram-design"},
    {"rank": 3, "cn_name": "规格驱动开发工具包", "repo": "spec-kit", "owner": "github",
     "lang": "Python", "stars": 129_274, "forks": 11_557, "today": 892,
     "define": "GitHub 官方出品的工具包，帮你按「先写规格、再写代码」的方式做开发（Spec-Driven Development）。",
     "tldr": "用规格文档驱动开发，少走弯路",
     "points": ["GitHub 官方维护", "规格→任务→代码的完整流程", "适合 AI 编程协作"],
     "audience": "开发者、AI 编程用户、技术团队",
     "url": "github.com/github/spec-kit"},
    {"rank": 4, "cn_name": "时空可组合元框架", "repo": "cordis", "owner": "cordiverse",
     "lang": "TypeScript", "stars": 4_212, "forks": 209, "today": 599,
     "define": "一个插件 / 模块元框架，主打「时空可组合」，用来搭建可组合、可扩展的应用架构。",
     "tldr": "用插件化思路搭可组合的应用架构",
     "points": ["插件 / 模块元框架", "主打时空可组合", "TypeScript 实现"],
     "audience": "前端 / 全栈开发者、框架作者",
     "url": "github.com/cordiverse/cordis"},
    {"rank": 5, "cn_name": "14MB 端侧小模型", "repo": "needle", "owner": "cactus-compute",
     "lang": "Python", "stars": 6_136, "forks": 409, "today": 547,
     "define": "只有 14MB 的端侧基础模型，能在手机、穿戴设备、智能家居和机器人上本地运行。",
     "tldr": "把小模型塞进手机和机器人里跑",
     "points": ["仅 14MB 的超小体积", "端侧本地运行，保护隐私", "面向手机 / 穿戴 / 机器人"],
     "audience": "端侧 AI 开发者、硬件 / 机器人团队",
     "url": "github.com/cactus-compute/needle"},
    {"rank": 6, "cn_name": "给 Agent 用的浏览器", "repo": "ego-lite", "owner": "citrolabs",
     "lang": "JavaScript", "stars": 11_096, "forks": 565, "today": 545,
     "define": "为 AI Agent 打造的最快浏览器，可把你的登录态共享给 Codex / Claude Code 做自动化，零成本零配置。",
     "tldr": "让 AI Agent 用上你已登录的浏览器",
     "points": ["专为 AI Agent 自动化设计", "共享已登录的浏览器状态", "零成本、零配置"],
     "audience": "AI Agent 开发者、自动化工程师",
     "url": "github.com/citrolabs/ego-lite"},
    {"rank": 7, "cn_name": "开源低代码平台", "repo": "ToolJet", "owner": "ToolJet",
     "lang": "JavaScript", "stars": 39_610, "forks": 5_302, "today": 544,
     "define": "开源的低代码平台，拖拽即可搭建内部工具、仪表盘、业务应用、工作流和 AI Agent。",
     "tldr": "拖拽就能搭出内部工具和 AI Agent",
     "points": ["开源低代码搭建", "内部工具 / 仪表盘 / 工作流", "内置 AI Agent 能力"],
     "audience": "开发者、企业内部工具团队",
     "url": "github.com/ToolJet/ToolJet"},
    {"rank": 8, "cn_name": "本地训练大模型 UI", "repo": "unsloth", "owner": "unslothai",
     "lang": "Python", "stars": 72_137, "forks": 6_503, "today": 434,
     "define": "本地运行的 UI，用来跑和微调大模型与扩散模型（Qwen、DeepSeek、Gemma、FLUX 等），支持消费级显卡。",
     "tldr": "在本地显卡上微调你的大模型",
     "points": ["本地 UI 跑 / 微调 LLM", "支持主流开源模型", "消费级显卡也能跑"],
     "audience": "AI 研究者、独立开发者、ML 工程师",
     "url": "github.com/unslothai/unsloth"},
    {"rank": 9, "cn_name": "邮箱泄露查询", "repo": "holehe", "owner": "megadose",
     "lang": "Python", "stars": 13_164, "forks": 1_744, "today": 382,
     "define": "输入邮箱即可查出它在哪些网站注册过（Twitter、Instagram 等），并通过找回密码功能回收账号信息。",
     "tldr": "查一个邮箱注册过哪些网站",
     "points": ["邮箱反查注册站点", "支持主流社交平台", "开源、可自托管"],
     "audience": "安全研究者、隐私自查用户",
     "url": "github.com/megadose/holehe"},
    {"rank": 10, "cn_name": "一份 YAML 微调模型", "repo": "Soup", "owner": "MakazhanAlpamys",
     "lang": "Python", "stars": 1_745, "forks": 267, "today": 297,
     "define": "用一份 YAML 就能微调大模型，分层流式训练让你在 4GB 笔记本显卡上训 8B 模型。",
     "tldr": "一份 YAML 配置就能微调大模型",
     "points": ["一份 YAML 搞定微调", "分层流式训练", "4GB 显卡训 8B 模型"],
     "audience": "开发者、学生、ML 爱好者",
     "url": "github.com/MakazhanAlpamys/Soup"},
]


def render(p: dict) -> str:
    W, H = 1200, 1600          # 竖版 3:4（高:宽 = 4:3）
    M = 70
    CW = W - 2 * M             # 内容宽 1060

    repo = html.escape(p["repo"])
    cn_name = html.escape(p["cn_name"])
    rank = f"#{p['rank']}"
    page = f"{p['rank']:02d} / 10"

    # ---- 1. 顶部标识 ----
    top_y = 92
    line_y = 132

    # ---- 2. 排名红块 + 中文名 ----
    rank_block_y = 158
    rank_block_h = 118
    cn_name_y = rank_block_y + rank_block_h / 2 + 14

    # ---- 3. 项目原名 ----
    repo_y = 352

    # ---- 4. 定义 ----
    define_lines = wrap(p["define"], 36, CW - 20)
    define_start_y = 430
    define_line_h = 58
    define_end = define_start_y + len(define_lines) * define_line_h

    # ---- 5. 数据 pill（只放大这一行）----
    pill_w = [160, 250, 260, 168]
    pill_gap = 22
    pill_h = 100
    total_pill_w = sum(pill_w) + pill_gap * (len(pill_w) - 1)
    pill_x0 = M + (CW - total_pill_w) / 2
    pill_y = define_end + 56

    # ---- 6. 一句话看懂（深色卡）----
    tldr_lines = wrap(p["tldr"], 38, CW - 90)
    card_y = pill_y + pill_h + 56
    card_h = 112 + len(tldr_lines) * 56

    # ---- 7. 核心卖点 ----
    points_start_y = card_y + card_h + 52
    point_line_h = 64

    # ---- 8. 适合谁 ----
    audience_title_y = points_start_y + 3 * point_line_h + 34
    audience_text_y = audience_title_y + 48

    # ---- 9. 底部链接 + 页码（跟随内容）----
    bottom_line_y = audience_text_y + 62
    bottom_text_y = bottom_line_y + 40

    # ---- 构建 SVG 片段 ----
    define_svg = "".join(
        f'<text x="{M}" y="{define_start_y + i * define_line_h}" font-size="36" fill="#444444" font-family="-apple-system, PingFang SC, Microsoft YaHei, sans-serif">{html.escape(ln)}</text>'
        for i, ln in enumerate(define_lines)
    )

    px = [pill_x0 + sum(pill_w[:i]) + pill_gap * i for i in range(len(pill_w))]
    pill_texts = [p["lang"], f"{fmt(p['stars'])}", f"+{p['today']:,} 今日", f"{fmt(p['forks'])} Fork"]
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

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="{W}" height="{H}" fill="#ffffff"/>

  <!-- 1. 顶部标识区 -->
  <text x="{M}" y="{top_y}" font-size="34" fill="#999999" font-family="-apple-system, PingFang SC, Microsoft YaHei, sans-serif" font-weight="600">GitHub 爆火项目榜</text>
  <text x="{W-M}" y="{top_y}" font-size="34" fill="#999999" font-family="-apple-system, PingFang SC, Microsoft YaHei, sans-serif" text-anchor="end">第 1 期</text>
  <line x1="{M}" y1="{line_y}" x2="{W-M}" y2="{line_y}" stroke="#EEEEEE" stroke-width="2"/>

  <!-- 2. 排名 + 中文称号 -->
  <rect x="{M}" y="{rank_block_y}" width="{rank_block_h}" height="{rank_block_h}" rx="24" fill="#FF2442"/>
  <text x="{M+rank_block_h/2}" y="{rank_block_y + rank_block_h/2 + 18}" font-size="58" font-weight="800" fill="#ffffff" font-family="-apple-system, PingFang SC, Microsoft YaHei, sans-serif" text-anchor="middle">{rank}</text>
  <text x="{M+rank_block_h+22}" y="{cn_name_y}" font-size="44" font-weight="700" fill="#222222" font-family="-apple-system, PingFang SC, Microsoft YaHei, sans-serif">{cn_name}</text>

  <!-- 3. 项目原名（最大字号） -->
  <text x="{M}" y="{repo_y}" font-size="92" font-weight="800" fill="#111111" font-family="-apple-system, PingFang SC, Microsoft YaHei, sans-serif">{repo}</text>

  <!-- 4. 项目定义 -->
  {define_svg}

  <!-- 5. 数据维度 pill -->
  <g transform="translate(0, {pill_y})">
    {pills_svg}
  </g>

  <!-- 6. 一句话看懂（深色卡） -->
  <g transform="translate({M}, {card_y})">
    <rect x="0" y="0" width="{CW}" height="{card_h}" rx="22" fill="#1A1A1A"/>
    <text x="44" y="50" font-size="24" fill="#999999" font-family="-apple-system, PingFang SC, Microsoft YaHei, sans-serif" font-weight="600">一句话看懂</text>
    {tldr_svg}
  </g>

  <!-- 7. 核心卖点 -->
  {points_svg}

  <!-- 8. 适合谁 -->
  <text x="{M}" y="{audience_title_y}" font-size="30" fill="#888888" font-family="-apple-system, PingFang SC, Microsoft YaHei, sans-serif" font-weight="600">适合谁？</text>
  <text x="{M}" y="{audience_text_y}" font-size="38" fill="#333333" font-family="-apple-system, PingFang SC, Microsoft YaHei, sans-serif">{html.escape(p['audience'])}</text>

  <!-- 9. 底部链接 + 页码 -->
  <line x1="{M}" y1="{bottom_line_y}" x2="{W-M}" y2="{bottom_line_y}" stroke="#EEEEEE" stroke-width="2"/>
  <text x="{M}" y="{bottom_text_y}" font-size="28" fill="#999999" font-family="-apple-system, PingFang SC, Microsoft YaHei, sans-serif">https://{html.escape(p['url'])}</text>
  <text x="{W-M}" y="{bottom_text_y}" font-size="28" fill="#999999" font-family="-apple-system, PingFang SC, Microsoft YaHei, sans-serif" text-anchor="end">{page}</text>
</svg>"""


if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "skill_cards")
    out_dir = os.path.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)
    for p in ALL:
        fname = f"skill_{p['rank']:02d}_{p['repo']}.svg"
        with open(os.path.join(out_dir, fname), "w", encoding="utf-8") as f:
            f.write(render(p))
        print("written:", fname)
