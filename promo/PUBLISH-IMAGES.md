# 配图编排手册 — 哪张图配哪个平台

> 所有数字来自 P3 真实验收（34 个在岗 skill、16 个闲置）。门禁③前不外发。

| 资产 | 文件 | 比例 | 用途 | 出法 |
|---|---|---|---|---|
| 实证图 / 头图 | `assets/proof-roster.png` | 16:9（1200×675） | README 首屏 · Twitter/X 头图 · 公众号头图 | **已出**。HTML 渲染 `firm.py roster` 真实输出后截 file://（实为本地 server + curl 核验内容再截，绕开 404 坑），**不是文生图** |
| Banner | `assets/banner.png` | 2:1（1280×640） | README hero · GitHub social preview · 社媒页眉 | **已出**。HTML 渲染（文字精确：brand + tagline + 找/验/融/装/治 五阶段），非文生图 |
| 小红书轮播 | `assets/xhs/shc01–05.png` | 3:4（1080×1440） | 小红书图文笔记（5 张：钩子/痛点/五步/数据/开源） | **已出**。xhs-card-post 渲染（HTML 出字、品牌 navy+mint）；标题+正文+发布策略见 `assets/xhs/shc_copy.md` |
| 概念图 | `assets/concept.png` | 2:3（1024×1536） | 备用封面 · Twitter 备选 | **已出**。image2（gpt-image-2）编辑风扁平插画：递 offer 给芯片机器人候选 + 名册看板（在岗 vs 板凳）。少字、反 slop |

## 平台适配
- **Twitter / X**：`proof-roster.png`（16:9）做头图；竖图会被裁。
- **小红书**：直接用 `assets/xhs/` 的 5 张轮播卡（封面 shc01）；文案+发布策略见 `assets/xhs/shc_copy.md`。concept.png 可做备用封面。
- **公众号**：原生比例，实证图直接可用。

## 外发纪律（门禁③）
文案（`launch-copy.md`）+ 配图成套给用户过目，**逐平台确认后才发**。本仓已是 public，往 README 嵌图属仓库内更新、非社媒外发。
