#!/usr/bin/env python3
"""ensure_firm.py — 把猎头公司的"后台部门"就位（运行时取回姊妹仓，不复制维护）。
Bring the firm's back-office departments online (fetch sibling repos on demand).

skill-hunter-company 是一家**编排型**猎头公司：它自己只管前台接待与叙事，
真正干活的几个部门是独立开源的姊妹项目——
  · world-aid     —— sourcing & placement（搜罗与落位引擎）
  · skill-lineage —— due diligence（背景调查 / 谱系核验）
本脚本按需把这些部门的零依赖脚本取到本地缓存（raw 直链，不耗 GitHub API 配额）。
开发机上若已有姊妹仓 checkout（~/world-aid 等），firm.py 会优先直接用它们。

This firm is an *orchestrator*: the real work is done by standalone sibling
projects. This script caches their zero-dep scripts locally on demand.

用法 / Usage:
  python3 ensure_firm.py [--refresh]
"""
from __future__ import annotations

import argparse
import os
import urllib.request

# 后台部门 = 姊妹仓 → 它要取回的脚本 / department -> scripts to fetch
DEPARTMENTS = {
    "world-aid": {
        "repo": "a28939876-max/world-aid",
        "ref": "main",
        "scripts": ["search_skills.py", "install_skill.py", "ensure_lineage.py"],
        "subdir": "scripts",
    },
    "skill-lineage": {
        "repo": "a28939876-max/skill-lineage",
        "ref": "main",
        "scripts": ["find_derivatives.py", "diff_skill.py"],
        "subdir": "scripts",
    },
}

OFFICE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".firm-office")
UA = "skill-hunter-company/0.1"


def fetch(dept: str, refresh: bool = False) -> dict:
    """取回一个部门的脚本到 .firm-office/<dept>/，返回 {script: path}。"""
    spec = DEPARTMENTS[dept]
    dst_dir = os.path.join(OFFICE, dept)
    os.makedirs(dst_dir, exist_ok=True)
    paths = {}
    for name in spec["scripts"]:
        dst = os.path.join(dst_dir, name)
        if os.path.exists(dst) and not refresh:
            paths[name] = dst
            continue
        url = (f"https://raw.githubusercontent.com/{spec['repo']}/"
               f"{spec['ref']}/{spec['subdir']}/{name}")
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        with open(dst, "wb") as fh:
            fh.write(data)
        paths[name] = dst
    return paths


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--refresh", action="store_true",
                    help="忽略缓存重新拉取 / re-fetch even if cached")
    args = ap.parse_args()
    for dept in DEPARTMENTS:
        paths = fetch(dept, args.refresh)
        for name, path in paths.items():
            print(f"{dept:>14}  {name:<22}  {path}")


if __name__ == "__main__":
    main()
