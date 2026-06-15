# 配图编排手册 — 哪张图配哪个平台

> 所有数字来自 P3 真实验收（34 个在岗 skill、16 个闲置）。门禁③前不外发。

| 资产 | 文件 | 比例 | 用途 | 出法 |
|---|---|---|---|---|
| 实证图 / 头图 | `assets/proof-roster.png` | 16:9（1200×675） | README 首屏 · Twitter/X 头图 · 公众号头图 | **已出**。HTML 渲染 `firm.py roster` 真实输出后截 file://（实为本地 server + curl 核验内容再截，绕开 404 坑），**不是文生图** |
| 概念图 | `assets/concept-*.png` | 3:4 + 16:9 | 小红书封面 · Twitter 备选 | 待出。猎头隐喻（给 skill 发 offer / 名册看板）。走 image2 / poster-graphic-design |
| Banner | `assets/banner.png` | 宽幅 | README / 社媒页眉 | 待出。一句定位 + 五阶段。走 image2 / poster |

## 平台适配
- **Twitter / X**：`proof-roster.png`（16:9）做头图；竖图会被裁。
- **小红书**：3:4 竖卡轮播——需把实证图重排成 3:4，或用概念卡。
- **公众号**：原生比例，实证图直接可用。

## 外发纪律（门禁③）
文案（`launch-copy.md`）+ 配图成套给用户过目，**逐平台确认后才发**。本仓已是 public，往 README 嵌图属仓库内更新、非社媒外发。
