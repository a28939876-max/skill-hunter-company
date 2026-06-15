#!/usr/bin/env python3
"""小红书图文卡渲染器(JSON 驱动)。
用法: <CARD_PYTHON> render_cards.py spec.json [--outdir DIR]
spec.json 见 examples/。输出每张卡一张 PNG(默认 1080x1440, 3:4),并对内容溢出告警。

card.type:
  cover   封面: title(+可选 lead/badge/pill/note), swipe 提示
  story   叙事卡: heading + paragraphs[]
  method  方法卡: heading + items[]{h, p}
  list    清单/收藏卡: heading + items[](字符串)
  closing 收尾卡: heading + paragraphs[] (+可选 punch 金句行)
文本里用 *星号* 包裹的片段会加粗高亮。
style: cream(米色檀木衬线,开杠体) | dark(暗调琥珀,与视频同视觉)
"""
import argparse
import html as _html
import json
import os
import re
import sys

# ---- 风格主题 ----
STYLES = {
    "cream": {
        "bg": "#f7f0de",
        "fg": "#a07c3e",
        "head": "#a07c3e",
        "sub": "#8a6a35",
        "accent": "#8a6a35",
        "swipe": "#c8a96a",
        "arrow": "#e9c98e",
        "quote": "#f3d9a8",
        "font": '"Songti SC","STSong","Noto Serif SC",serif',
        "deco": ("background-image:radial-gradient(rgba(214,186,130,.18) 6px,transparent 7px),"
                 "radial-gradient(rgba(214,186,130,.12) 5px,transparent 6px);"
                 "background-size:260px 230px,190px 170px;background-position:30px 40px,120px 130px;"),
        "vignette": "",
    },
    "dark": {
        "bg": "#0d0c0a",
        "fg": "#e9e2d4",
        "head": "#ffffff",
        "sub": "#ffc24b",
        "accent": "#ffc24b",
        "swipe": "#9a917f",
        "arrow": "#e9c98e",
        "quote": "#3a3220",
        "font": '"PingFang SC","STHeiti",sans-serif',
        "deco": "",
        "vignette": ('<div style="position:absolute;inset:0;pointer-events:none;'
                     'background:radial-gradient(ellipse 90% 75% at 50% 44%,transparent 60%,rgba(0,0,0,.5) 100%);"></div>'),
    },
    # 品牌色:深藏青 + 薄荷绿,和 skill-hunter-company 的 banner/proof 一致
    "firm": {
        "bg": "radial-gradient(120% 120% at 18% 0%,#15233b 0%,#0d1117 55%)",
        "fg": "#c9d1d9",
        "head": "#e6edf3",
        "sub": "#7ee787",
        "accent": "#7ee787",
        "swipe": "#7d8590",
        "arrow": "#7ee787",
        "quote": "#1b2230",
        "font": '"PingFang SC","STHeiti","Helvetica Neue",sans-serif',
        "deco": "",
        "vignette": ('<div style="position:absolute;inset:0;pointer-events:none;'
                     'background:radial-gradient(ellipse 92% 78% at 50% 42%,transparent 62%,rgba(0,0,0,.45) 100%);"></div>'),
    },
}


def hl(s):
    out = _html.escape(s or "")
    return re.sub(r"\*([^*]+)\*", r'<b>\1</b>', out)


def card_html(card, S):
    t = card.get("type", "story")
    if t == "cover":
        lead = '<div class="lead">%s</div>' % hl(card["lead"]) if card.get("lead") else ""
        note = '<div class="note">%s</div>' % hl(card["note"]) if card.get("note") else ""
        return ('<div class="wrap cover"><div class="quote">&ldquo;</div>'
                '%s<h1>%s</h1>%s</div>'
                '<div class="swipe"><span>&#9678; %s</span><span class="arrow">&#10142;</span></div>'
                % (lead, hl(card["title"]), note, _html.escape(card.get("swipe", "右划查看全文"))))
    if t == "story" or t == "closing":
        ps = "".join("<p>%s</p>" % hl(p) for p in card.get("paragraphs", []))
        punch = '<div class="punch">%s</div>' % hl(card["punch"]) if card.get("punch") else ""
        head = '<h2>%s</h2>' % hl(card["heading"]) if card.get("heading") else ""
        return '<div class="wrap">%s%s%s</div>' % (head, ps, punch)
    if t == "method":
        items = "".join('<div class="item"><h3>%s</h3><p class="np">%s</p></div>'
                        % (hl(it["h"]), hl(it["p"])) for it in card.get("items", []))
        return '<div class="wrap"><h2>%s</h2>%s</div>' % (hl(card.get("heading", "")), items)
    if t == "list":
        rows = "<br>\n".join(hl(x) for x in card.get("items", []))
        return '<div class="wrap"><h2>%s</h2><div class="list">%s</div></div>' % (hl(card.get("heading", "")), rows)
    raise ValueError("unknown card type: " + t)


def page(card, S):
    css = """
*{margin:0;padding:0;box-sizing:border-box;}
body{width:1080px;height:1440px;position:relative;overflow:hidden;
 background:%(bg)s;%(deco)s font-family:%(font)s;color:%(fg)s;}
.wrap{position:absolute;top:140px;left:85px;right:85px;}
.wrap.cover{top:330px;}
.quote{font-size:300px;line-height:1;color:%(quote)s;font-family:Georgia,serif;letter-spacing:-30px;}
.lead{font-size:40px;color:%(sub)s;margin:30px 0 10px;letter-spacing:1px;}
h1{font-size:88px;font-weight:900;line-height:1.55;color:%(head)s;letter-spacing:4px;margin-top:40px;}
.note{font-size:34px;color:%(swipe)s;margin-top:46px;letter-spacing:1px;}
h2{font-size:56px;font-weight:900;line-height:1.5;color:%(head)s;letter-spacing:2px;margin-bottom:44px;}
h3{font-size:48px;font-weight:900;color:%(sub)s;margin:10px 0 18px;letter-spacing:1px;}
p{font-size:42px;line-height:1.9;text-align:justify;text-indent:2em;margin-bottom:34px;letter-spacing:1px;}
.np{text-indent:0;}
b{font-weight:900;color:%(accent)s;}
.item{margin-bottom:46px;}
.list{font-size:46px;line-height:2.35;color:%(sub)s;font-weight:700;letter-spacing:1px;}
.punch{font-size:48px;font-weight:900;color:%(accent)s;margin-top:20px;letter-spacing:1px;}
.swipe{position:absolute;bottom:120px;left:85px;right:85px;display:flex;align-items:center;
 justify-content:space-between;font-size:36px;color:%(swipe)s;letter-spacing:3px;}
.arrow{font-size:60px;color:%(arrow)s;}
""" % S
    return ("<!DOCTYPE html><html lang=zh-CN><head><meta charset=UTF-8><style>" + css
            + "</style></head><body>" + card_html(card, S) + S["vignette"] + "</body></html>")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--outdir", default=None)
    a = ap.parse_args()

    spec = json.load(open(a.spec))
    style = spec.get("style", "cream")
    if style not in STYLES:
        sys.exit("unknown style: %s (choose cream|dark)" % style)
    S = STYLES[style]
    outdir = a.outdir or spec.get("outdir") or os.path.join(os.path.dirname(os.path.abspath(a.spec)), "cards_out")
    os.makedirs(outdir, exist_ok=True)
    cards = spec["cards"]
    prefix = spec.get("prefix", "card")

    from playwright.sync_api import sync_playwright
    warnings = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1440})
        for i, card in enumerate(cards, 1):
            hp = os.path.join(outdir, "%s%02d.html" % (prefix, i))
            open(hp, "w").write(page(card, S))
            pg.goto("file://" + hp)
            pg.wait_for_timeout(350)
            # 溢出检测:内容底边超出安全区(1400px)就告警
            bottom = pg.evaluate(
                "() => {const w=document.querySelector('.wrap');"
                "if(!w)return 0;const r=w.getBoundingClientRect();return Math.round(r.bottom);}")
            png = os.path.join(outdir, "%s%02d.png" % (prefix, i))
            pg.screenshot(path=png)
            flag = ""
            if bottom > 1410:
                flag = "  ⚠ 内容溢出(底边 %dpx > 1410),建议缩短文字或拆卡" % bottom
                warnings.append((i, bottom))
            print("card %02d [%s] -> %s%s" % (i, card.get("type", "story"), png, flag))
        b.close()
    if warnings:
        print("\n%d 张卡内容溢出,需精简:%s" % (len(warnings), ", ".join("#%d" % i for i, _ in warnings)))
    else:
        print("\n全部 %d 张卡渲染完成,无溢出。" % len(cards))


if __name__ == "__main__":
    main()
