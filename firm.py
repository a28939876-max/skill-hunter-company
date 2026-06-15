#!/usr/bin/env python3
"""skill-hunter-company — the headhunting firm for your AI agent skills.
skill 猎头公司 —— 为你的 AI agent 物色、核验、安置并长期管理最对的 skill。

A retained executive-search firm doesn't hand you a stack of résumés. It runs a
full lifecycle: source the market, vet every candidate, place the right one, and
then *keep managing the talent* so your team doesn't rot. This CLI does the same
for the skills your agent depends on.

完整流程 / The engagement (five consecutive risk points in a skill's life):
  source  找  Source   — 按需求搜罗候选 skill（连"挂不出来"的也猎回）
  vet     验  Vet      — 尽职调查：来源血统 + 安全背调（没通过你永远见不到）
  bespoke 融  Bespoke  — 市场上没有完美人选？按你的画像定制打造一个
  place   装  Place    — 落位安装，陪过上手期
  roster  治  Manage   — 持续人才管理：绩效、板凳深度、汰换、继任

默认流（大众）/ Default engagement:  source → vet → place
进阶流（长期客户）/ Retained client: roster → bespoke → (re)place

Pure stdlib. The heavy lifting is delegated to standalone sibling repos
(world-aid, skill-lineage); see ensure_firm.py. This file is the front desk.
"""
from __future__ import annotations

import argparse
import difflib
import glob
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
HOME = os.path.expanduser("~")
UA = "skill-hunter-company/0.1"

# ── 后台部门定位：开发机优先用本地姊妹仓，否则用 .firm-office 缓存 ────────────
# Locate a sibling-repo script: prefer a local checkout, else the fetched cache.
SIBLINGS = {  # dept -> local checkout candidates
    "world-aid": [os.path.join(HOME, "world-aid", "scripts")],
    "skill-lineage": [os.path.join(HOME, "skill-lineage", "scripts")],
}


def back_office(dept: str, script: str) -> str | None:
    """Return a runnable path to a department script, or None if unavailable."""
    env = os.environ.get(f"{dept.replace('-', '_').upper()}_DIR")
    candidates = ([os.path.join(env, "scripts"), env] if env else []) + SIBLINGS.get(dept, [])
    candidates.append(os.path.join(HERE, ".firm-office", dept))
    for base in candidates:
        path = os.path.join(base, script)
        if os.path.isfile(path):
            return path
    # not found locally — try to fetch it
    try:
        sys.path.insert(0, HERE)
        import ensure_firm
        return ensure_firm.fetch(dept).get(script)
    except Exception:  # noqa: BLE001
        return None


def run_script(path: str, args: list[str]) -> tuple[int, str]:
    proc = subprocess.run([sys.executable, path, *args],
                          capture_output=True, text=True)
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


# ── source 找 ────────────────────────────────────────────────────────────────
def cmd_source(a) -> int:
    need = " ".join(a.need).strip()
    script = back_office("world-aid", "search_skills.py")
    if not script:
        print("⚠ sourcing department offline: could not locate world-aid "
              "(run `python3 ensure_firm.py`).", file=sys.stderr)
        return 2
    extra = ["--limit", str(a.limit)] + (["--no-github"] if a.no_github else [])
    print(f"📇 The firm is working the market for: “{need}”\n"
          f"   （在测绘市场、搜罗候选——包括挂不出来的被动人选）\n")
    code, out = run_script(script, [need, *extra])
    if code != 0:
        print(out, file=sys.stderr)
        return code
    try:
        data = json.loads(out)
    except json.JSONDecodeError:
        print(out)
        return 0
    fams = sorted(data.get("families", []), key=lambda f: f["head"].get("stars", 0),
                  reverse=True)
    print(f"🗂  Shortlist — {data.get('family_count', 0)} distinct candidates "
          f"out of {data.get('total', 0)} sourced "
          f"(copies grouped into one; we don't pad the list):\n")
    for i, fam in enumerate(fams[:a.limit], 1):
        h = fam["head"]
        dup = f"  ·  {fam['size']} look-alikes folded in" if fam["size"] > 1 else ""
        print(f"  {i}. {h.get('author','?')}/{h.get('name','?')}  "
              f"★{h.get('stars',0)}{dup}")
        print(f"     {h.get('url','')}")
    for note in data.get("notes", []):
        print(f"\n   ⓘ {note}")
    print("\n   Next: vet a finalist →  firm.py vet <owner/repo>")
    return 0


# ── vet 验 ───────────────────────────────────────────────────────────────────
def cmd_vet(a) -> int:
    target = a.target
    script = back_office("skill-lineage", "find_derivatives.py")
    if not script:
        print("⚠ due-diligence department offline: could not locate skill-lineage.",
              file=sys.stderr)
        return 2
    print(f"🔎 Due diligence on {target}\n"
          f"   （查血统：找原版/衍生/镜像，看你手上这个是不是改良版或换皮抄袭）\n")
    code, out = run_script(script, [target])
    print(out)
    print("   Reference check done. For a deeper background check, diff against the "
          "original:\n   firm.py … (diff_skill via skill-lineage)\n"
          "   Security vetting plugs in SkillSpector/OSV as a backend signal.")
    return 0 if code == 0 else code


# ── place 装 ─────────────────────────────────────────────────────────────────
def cmd_place(a) -> int:
    script = back_office("world-aid", "install_skill.py")
    if not script:
        print("⚠ placement department offline: could not locate world-aid.",
              file=sys.stderr)
        return 2
    print(f"🤝 Extending an offer to {a.target} and walking it through onboarding…\n")
    code, out = run_script(script, [a.target, *a.passthrough])
    print(out)
    return code


# ── bespoke 融 ───────────────────────────────────────────────────────────────
def cmd_bespoke(a) -> int:
    print(BESPOKE_BRIEF)
    return 0


# ── roster 治 ────────────────────────────────────────────────────────────────
SKILL_FM = re.compile(r"^---\s*\n(.*?)\n---", re.S)


def _read_skill(md: str) -> dict | None:
    try:
        with open(md, encoding="utf-8", errors="replace") as f:
            text = f.read(20000)
    except OSError:
        return None
    name, desc = os.path.basename(os.path.dirname(md)), ""
    m = SKILL_FM.match(text)
    if m:
        fm = m.group(1)
        nm = re.search(r"^name:\s*(.+)$", fm, re.M)
        if nm:
            name = nm.group(1).strip().strip("\"'")
        dm = re.search(r"^description:\s*(.*?)(?=\n[A-Za-z_\-]+:|\Z)", fm, re.S | re.M)
        if dm:
            desc = " ".join(l.strip() for l in dm.group(1).splitlines()).strip()
    return {"name": name, "desc": desc[:400]}


def _usage(days: int | None) -> dict:
    """skill -> {count, last_used(epoch)} from Claude Code transcripts."""
    stats: dict[str, dict] = {}
    proj = os.path.join(HOME, ".claude", "projects")
    cutoff = time.time() - days * 86400 if days else 0
    for path in glob.glob(os.path.join(proj, "**", "*.jsonl"), recursive=True):
        try:
            fmtime = os.path.getmtime(path)
        except OSError:
            continue
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                for line in f:
                    if '"Skill"' not in line:
                        continue
                    try:
                        e = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if e.get("type") != "assistant":
                        continue
                    for b in e.get("message", {}).get("content", []) or []:
                        if (isinstance(b, dict) and b.get("type") == "tool_use"
                                and b.get("name") == "Skill"):
                            nm = (b.get("input") or {}).get("skill")
                            if not nm:
                                continue
                            ts = fmtime
                            t = e.get("timestamp")
                            if isinstance(t, str):
                                try:
                                    ts = datetime.fromisoformat(
                                        t.replace("Z", "+00:00")).timestamp()
                                except ValueError:
                                    pass
                            s = stats.setdefault(nm, {"count": 0, "last": 0})
                            s["count"] += 1
                            s["last"] = max(s["last"], ts)
        except OSError:
            continue
    return stats


def _dup_groups(skills: list[dict], thr: float = 0.82) -> list[list[str]]:
    groups: list[dict] = []
    for s in skills:
        norm = re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s["desc"].lower())).strip()
        for g in groups:
            if norm and difflib.SequenceMatcher(None, norm, g["norm"]).ratio() >= thr:
                g["names"].append(s["name"])
                break
        else:
            groups.append({"norm": norm, "names": [s["name"]]})
    return [g["names"] for g in groups if len(g["names"]) > 1]


def cmd_roster(a) -> int:
    skills_dir = a.skills_dir or os.environ.get("SKILLS_DIR") or \
        os.path.join(HOME, ".claude", "skills")
    if not os.path.isdir(skills_dir):
        print(f"⚠ no skills directory at {skills_dir}", file=sys.stderr)
        return 2
    roster = []
    for entry in sorted(os.listdir(skills_dir)):
        md = os.path.join(skills_dir, entry, "SKILL.md")
        if os.path.isfile(md):
            info = _read_skill(md)
            if info:
                roster.append(info)
    use = _usage(None)
    now = time.time()
    for s in roster:
        u = use.get(s["name"], {})
        s["count"] = u.get("count", 0)
        s["idle_days"] = int((now - u["last"]) / 86400) if u.get("last") else None

    cold = [s for s in roster if s["idle_days"] is None or s["idle_days"] >= a.days]
    top = sorted([s for s in roster if s["count"]], key=lambda s: s["count"],
                 reverse=True)[:8]
    dups = _dup_groups(roster)

    print("🏢 Talent review — your active skill roster\n"
          f"   （盘点在岗 skill 团队：绩效、板凳深度、重复编制）\n")
    print(f"   On the payroll : {len(roster)} skills installed in {skills_dir}")
    print(f"   On the bench   : {len(cold)} idle ≥ {a.days}d — candidates for archival")
    print(f"   Redundant hires: {len(dups)} overlapping-mandate groups\n")

    if top:
        print("   ⭐ Top performers (most-called):")
        for s in top:
            print(f"      {s['count']:>4}×  {s['name']}")
    if dups:
        print("\n   ♻ Overlapping mandates (consider keeping one, benching the rest):")
        for g in dups:
            print(f"      • {'  ↔  '.join(g)}")
    if cold:
        print(f"\n   🪑 On the bench (idle ≥ {a.days}d):")
        for s in sorted(cold, key=lambda s: (s['idle_days'] is not None, s['idle_days'] or 0)):
            tag = "never called" if s["idle_days"] is None else f"{s['idle_days']}d idle"
            print(f"      • {s['name']:<32} {tag}")
    print("\n   Recommendation: bench the idle, retire the redundant — every skill on "
          "the\n   payroll costs context budget each session, called or not.")
    return 0


def cmd_services(a) -> int:
    print(SERVICES)
    return 0


BESPOKE_BRIEF = """\
🧩 Bespoke search — when the market has no perfect candidate
   （市场上几个候选各有所长、但没一个完整达标时，按你的画像定制打造一个）

This is a retained, hands-on engagement, not a one-click hire. It is run by the
sibling project **skill-fusion**: extract the best mechanism from each partial
candidate, rewrite them into one new skill, and pass four manual quality gates
(extraction table → design → safety self-check → live acceptance).

   Engage it:  use the `skill-fusion` skill / repo.
   Result:     a new, purpose-built skill — then `firm.py place` it like any hire.
"""

SERVICES = """\
skill-hunter-company — the headhunting firm for your AI agent skills

  Find the right AI skills, install them with confidence,
  and keep your skill library clean.

The engagement (five consecutive risk points in a skill's life):

  source   找  Source the market for candidate skills
  vet      验  Due diligence: lineage + security background check
  bespoke  融  No perfect candidate? Develop one (via skill-fusion)
  place    装  Make the hire — install & onboard
  roster   治  Talent management: performance, bench strength, turnover

  Default engagement (most clients):  source → vet → place
  Retained client (power users):      roster → bespoke → (re)place

Usage:
  firm.py source "make a powerpoint from notes"   # find candidates
  firm.py vet <owner/repo>                         # background-check one
  firm.py place <github-url>                       # hire (install) it
  firm.py roster --days 60                         # review your installed team
  firm.py bespoke                                  # commission a custom skill

The departments that do the real work are standalone sibling repos
(world-aid, skill-lineage). Run `python3 ensure_firm.py` to bring them online.
"""


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="firm.py", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")

    p = sub.add_parser("source", help="找 — source candidate skills for a need")
    p.add_argument("need", nargs="+")
    p.add_argument("--limit", type=int, default=8)
    p.add_argument("--no-github", action="store_true")
    p.set_defaults(fn=cmd_source)

    p = sub.add_parser("vet", help="验 — due diligence on a candidate (owner/repo)")
    p.add_argument("target")
    p.set_defaults(fn=cmd_vet)

    p = sub.add_parser("place", help="装 — hire (install) a skill")
    p.add_argument("target")
    p.add_argument("passthrough", nargs="*", help="args passed to world-aid installer")
    p.set_defaults(fn=cmd_place)

    p = sub.add_parser("bespoke", help="融 — commission a custom skill (skill-fusion)")
    p.set_defaults(fn=cmd_bespoke)

    p = sub.add_parser("roster", help="治 — review & manage your installed skill team")
    p.add_argument("--days", type=int, default=60, help="idle threshold for the bench")
    p.add_argument("--skills-dir", default=None)
    p.set_defaults(fn=cmd_roster)

    args = ap.parse_args()
    if not getattr(args, "fn", None):
        return cmd_services(args)
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
