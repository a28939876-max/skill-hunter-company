# Case 02 — Retained client: review the team you already hired

**The need (verbatim):** "I've installed a pile of skills over months. Which ones are
dead weight? My agent feels bloated."

**The old plan:** there is none. No tool tells you which installed skills have gone
idle, which overlap, or what they cost you. You install and forget.

**What the firm did** (real run, 2026-06-15, fully offline — scans your local
`~/.claude/skills` + Claude Code transcripts):

```
$ python3 firm.py roster --days 45

🏢 Talent review — your active skill roster
   On the payroll : 34 skills installed in /Users/.../.claude/skills
   On the bench   : 16 idle ≥ 45d — candidates for archival
   Redundant hires: 0 overlapping-mandate groups

   ⭐ Top performers (most-called):
        11×  game-orchestration-planner
        10×  image2
         9×  playwright
         9×  poster-graphic-design
         7×  skill-hunter
   🪑 On the bench (idle ≥ 45d):
      • content-broadcast        never called
      • wechat-article           never called
      • visual-style-cookbook    never called
      • multi-platform-publishing never called
      …16 total
```

**What it surfaced on a real 34-skill install:**
- **16 of 34 skills** had not been called in ≥45 days (several never). Every one of
  them still costs context budget every session — the firm names them for the bench.
- A clear **top-performer** tail (`game-orchestration-planner`, `image2`, `playwright`)
  vs a long idle bench — the LRU signal you need to decide what to archive.
- **0 redundant-hire groups** at the default similarity threshold. This is an honest
  result: dedup compares full skill *descriptions*, which are distinct even when two
  skills overlap functionally. It's conservative on purpose (won't cry wolf); the
  knob is there to tighten.

**The retained-client loop:** bench the idle → if a recurring need has no whole
candidate, `firm.py bespoke` (commission one via skill-fusion) → `place` it →
review again next quarter.
