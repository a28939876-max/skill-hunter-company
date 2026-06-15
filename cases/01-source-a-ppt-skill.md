# Case 01 — Default engagement: source a skill for a need

**The need (verbatim):** "I want a skill that turns my notes into a PowerPoint deck."

**The old plan:** open SkillsMP / GitHub, search "powerpoint", scroll a wall of
look-alikes sorted by stars, pick whichever has the most — and hope it isn't a
re-skinned clone.

**What the firm did** (real run, 2026-06-15, anonymous, no token):

```
$ python3 firm.py source "pptx powerpoint slides" --limit 6

🗂  Shortlist — 6 distinct candidates out of 6 sourced:
  1. ningzimu/image-to-editable-ppt-skill           ★581
  2. w1163222589-coder/slide-image-to-editable-pptx ★142
  3. Akxan/ppt-agent-skill                          ★83
  4. tristan-mcinnis/pptx-from-layouts-skill        ★75
  5. kdnsna/ultimate-ppt-master-skill              ★48
  6. Phlegonlabs/Powerpoint-fancy-design            ★26
   ⓘ skillsmp failed: HTTP Error 500: Internal Server Error
```

**Notes from the run (the lesson that became a feature):**
- The first attempt passed the full sentence as one query and returned **0** results —
  the sourcing engine under-recalls on prose. Instead of pushing "use keywords" onto the
  user (which fights the whole "say what you want" pitch), `source` now distills any brief
  into a few keyword passes (broad → narrow) and merges them. The same sentence
  *"make a powerpoint deck from my notes"* now returns **27 candidates across 3 passes**.
  `--exact "<keywords>"` still searches verbatim when you want control.
- SkillsMP was down (HTTP 500, a known-flaky upstream). The firm **reported it and
  carried on** with the GitHub desk — the search did not crash. Graceful degradation
  is the point.
- Copies are folded into families; here all 6 were genuinely distinct (no padding).

**Next steps in the engagement:** `firm.py vet ningzimu/image-to-editable-ppt-skill`
(background check) → `firm.py place <url>` (hire/install).
