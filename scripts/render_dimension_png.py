# -*- coding: utf-8 -*-
"""Playwright 无头 Chromium 把周榜/月榜的 10 张 SVG 卡片 + 封面 HTML 渲染成 2x PNG 并打包。

用法：
    python render_dimension_png.py weekly
    python render_dimension_png.py monthly
"""
import os
import sys
import glob
import zipfile
from playwright.sync_api import sync_playwright

BASE = "/Users/peterli/WorkBuddy/2026-08-16-12-24-51"
SCALE = 2
EXEC = "/Users/peterli/Library/Caches/ms-playwright/chromium_headless_shell-1228/chrome-headless-shell-mac-arm64/chrome-headless-shell"


def render(path, out_png, vw, vh):
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=EXEC)
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


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "weekly"
    if mode == "weekly":
        card_dir, cover, zip_name = "skill_cards_weekly", "github_weekly_top10.html", "github_weekly_export.zip"
    else:
        card_dir, cover, zip_name = "skill_cards_monthly", "github_monthly_top10.html", "github_monthly_export.zip"

    svg_files = sorted(glob.glob(os.path.join(BASE, card_dir, "skill_*.svg")))
    for f in svg_files:
        out = os.path.splitext(f)[0] + ".png"
        render(f, out, 1200, 1600)

    cover_out = os.path.join(BASE, cover.replace(".html", ".png"))
    render(os.path.join(BASE, cover), cover_out, 1080, 1440)

    # 打包
    zpath = os.path.join(BASE, zip_name)
    if os.path.exists(zpath):
        os.remove(zpath)
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(cover_out, os.path.basename(cover_out))
        for f in svg_files:
            png = os.path.splitext(f)[0] + ".png"
            z.write(png, os.path.basename(png))
    print("ZIP:", zip_name)
    print("ALL_DONE")
