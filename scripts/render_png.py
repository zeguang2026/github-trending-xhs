# -*- coding: utf-8 -*-
"""用 Playwright 无头 Chromium 把 10 张 SVG 卡片 + 封面 HTML 渲染成 2x PNG，并打包 zip。

本机没有 cairo/rsvg，所以用已装的 chromium_headless_shell 渲染。脚本自动探测本机
ms-playwright 缓存里的 chrome-headless-shell；找不到时回退到 Playwright 默认浏览器
（需先 `playwright install chromium`）。

用法（在项目工作目录执行）：
    python render_png.py
输出：skill_cards/skill_XX_*.png（2400x3200）、github_today_top10.png（2160x2880）、
      github_xhs_export.zip（含以上 11 张）。
"""
import os
import glob
import subprocess
import sys
from playwright.sync_api import sync_playwright

BASE = os.environ.get("XHS_BASE", os.getcwd())
CARD_DIR = os.path.join(BASE, "skill_cards")
COVER = os.path.join(BASE, "github_today_top10.html")
SCALE = 2  # 2 倍清晰度


def find_chromium() -> str | None:
    cache = os.path.expanduser("~/Library/Caches/ms-playwright")
    if not os.path.isdir(cache):
        return None
    for root, _dirs, files in os.walk(cache):
        for f in files:
            if f == "chrome-headless-shell":
                return os.path.join(root, f)
    return None


def render(path: str, out_png: str, vw: int, vh: int, exec_path: str | None):
    with sync_playwright() as p:
        if exec_path:
            browser = p.chromium.launch(executable_path=exec_path)
        else:
            browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": vw, "height": vh}, device_scale_factor=SCALE)
        page.goto("file://" + path)
        if path.endswith(".html"):
            page.add_style_tag(content="body{margin:0;padding:0;}")
            el = page.query_selector("body")
        else:
            el = page.query_selector("svg")
        el.screenshot(path=out_png)
        browser.close()
    print("written:", os.path.basename(out_png))


def main():
    exec_path = find_chromium()
    if not exec_path:
        print("[warn] 未探测到本机 chromium，将使用 Playwright 默认浏览器（如缺失请先 playwright install chromium）")

    svg_files = sorted(glob.glob(os.path.join(CARD_DIR, "skill_*.svg")))
    for f in svg_files:
        out = os.path.splitext(f)[0] + ".png"
        render(f, out, 1200, 1600, exec_path)

    if os.path.exists(COVER):
        render(COVER, os.path.join(BASE, "github_today_top10.png"), 1080, 1440, exec_path)
    else:
        print("[skip] 未找到封面", COVER)

    # 打包 zip
    zip_path = os.path.join(BASE, "github_xhs_export.zip")
    if os.path.exists(zip_path):
        os.remove(zip_path)
    subprocess.run([
        "zip", "-qj", zip_path,
        os.path.join(BASE, "github_today_top10.png"),
        *glob.glob(os.path.join(CARD_DIR, "skill_*.png")),
    ], check=True)
    print("zip ->", zip_path)
    print("ALL_DONE")


if __name__ == "__main__":
    main()
