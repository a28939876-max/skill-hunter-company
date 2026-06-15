---
name: skill-hunter-company
description: skill 猎头公司——为你的 AI agent 物色、核验、安置并长期管理最对的 skill。把高管猎聘（executive search）的完整流程搬给 agent skill：找(source 跨源搜罗候选)→验(vet 谱系+安全背调)→融(bespoke 没有完整人选时定制打造)→装(place 落位安装)→治(roster 持续人才管理:绩效/板凳深度/汰换)。默认流 source→vet→place 面向大众;进阶流 roster→bespoke 面向重度用户。是一个编排型项目,真正干活的是独立姊妹仓 world-aid(找装引擎)+skill-lineage(背调)+skill-fusion(定制)。Use when: 想按需求找一个现成 skill 并放心装上、或想盘点/治理已装的一堆 skill(揪出闲置/重复/陈旧)。触发词:"找个能做 xx 的 skill"、"我的 skill 库该清理了"、"skill 猎头"、"source/vet/place a skill"、"audit my skills"。不适用于:已点名要装的具体 skill(直接装)、从零写新 skill(走 skill-creator)。
---

# skill-hunter-company · skill 猎头公司

把高管猎聘（executive search）的文化搬给 AI agent skill：不是甩给你一墙简历，
而是**找对、查清、安置、长期管好**。

## 命令面（pure stdlib，`python3 firm.py <cmd>`）

```
source  找  跨源搜罗候选 skill（同源拷贝归并，低星改良版顶上来）
vet     验  尽职调查：谱系（原版/fork/换皮克隆）+ 安全背调
bespoke 融  没有完整人选时，从各候选提炼机制定制打造（交 skill-fusion）
place   装  发 offer——安装并冒烟
roster  治  盘点在岗团队：绩效排名、板凳深度（闲置）、重复编制
```

默认流（大众）：`source → vet → place`
进阶流（长期客户）：`roster → bespoke → (re)place`

## 怎么用

```bash
python3 ensure_firm.py                          # 后台部门就位（取回姊妹仓）
python3 firm.py source "pptx powerpoint slides" # 用紧凑关键词，别用整句
python3 firm.py vet  owner/repo
python3 firm.py place https://github.com/owner/repo
python3 firm.py roster --days 60
```

匿名即可用；设 `GITHUB_TOKEN` / `SKILLSMP_API_KEY` 解除限流并解锁完整背调。

## 架构（constellation，编排型）

本仓是前台 + 叙事 + 命令面；真正干活的是独立姊妹仓：
- `world-aid` —— 搜罗与落位引擎（source / place）
- `skill-lineage` —— 背调台（vet 的谱系部分）
- `skill-fusion` —— 定制打造（bespoke）
- SkillSpector / OSV —— 安全后端（不重造扫描器，当策略信号接入）

详见 [README](README.md) / [README.zh-CN](README.zh-CN.md)。
