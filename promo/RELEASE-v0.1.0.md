![skill-hunter-company](https://raw.githubusercontent.com/a28939876-max/skill-hunter-company/main/assets/banner.png)

**The headhunting firm for your AI agent skills.** Find the right skill, install it with confidence, and keep your skill library clean.

A retained executive-search firm doesn't dump 15 résumés on your desk — it sources the market, vets every candidate, places the right one, and then *keeps managing the talent* so your team doesn't rot. `skill-hunter-company` does exactly that for Claude Code / agent **skills**. It's not another search box; it runs the whole lifecycle.

### The engagement (找 → 验 → 融 → 装 → 治)
- **找 source** — work the whole market for candidate skills; copies folded into one, low-star improvements surfaced
- **验 vet** — due diligence: lineage (original vs fork vs re-skinned clone) + security background check
- **融 bespoke** — no perfect fit? build one from the best parts (via skill-fusion)
- **装 place** — make the hire: install & onboard
- **治 manage** — talent management: performance, bench strength, turnover

On a real 34-skill install, `firm.py roster` flagged **16 skills idle on the bench** — each still drawing a context-budget paycheck every session.

### Quick start
```bash
git clone https://github.com/a28939876-max/skill-hunter-company
cd skill-hunter-company
python3 ensure_firm.py                            # bring the back-office online
python3 firm.py source "pptx powerpoint slides"   # work the market
python3 firm.py roster --days 60                  # review your installed team
```

Pure Python stdlib, zero deps, anonymous out of the box. An orchestrator over the sibling repos **world-aid** (find+install) and **skill-lineage** (lineage); security plugs in **SkillSpector/OSV** as a backend signal.

**Family:** [world-aid](https://github.com/a28939876-max/world-aid) · [skill-lineage](https://github.com/a28939876-max/skill-lineage) · [world-intro](https://github.com/a28939876-max/world-intro)
