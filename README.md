<div align="center">

# 🧬 Streamer.skill (直播带货达人引擎)

### *"将顶尖带货主播的转化逻辑，蒸馏为你的专属 AI 引擎"*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)

<br>

**基于 dot-skill 底层架构** · 由 [Yixiao-Zhang1214](https://github.com/Yixiao-Zhang1214) 深度升级

</div>

---

## 🆕 本次升级核心：深度直播带货引擎

本项目是对原 `dot-skill` 的一次深度重构与升级，**专为“直播带货达人（Streamer）”场景打造**。我们彻底重写了话术生成引擎，旨在产出专业级、高转化率的直播间带货脚本。

**核心升级亮点：**
1. **8 段式深度口播结构**：
   摒弃了传统的简易脚本格式，引入了行业标准的 8 段式转化模型：反常识吸引停留 → 场景代入 → 价效对比 → 材质体感拆解 → 痛点对冲 → 身份/供应链背书 → 互动决策 → 季节窗口与风险兜底。
2. **7 阶段 Selling Flow 方法论**：
   从真实的直播 ASR（逐字稿）中，深度提取主播的语速节奏、逼单机制和专属送礼话术，构建出可复用的 7 阶段带货逻辑。
3. **自动化机评与合规自检**：
   内置 `P0/P1` 话术质量评估体系与严格的合规自检门槛，在保持极高转化压迫感的同时，避免违规和绝对化用语。

---

## ⚡ 快速安装

你可以直接通过兼容的 Agent 宿主（如 Trae, Claude Code 或 OpenClaw）安装这款升级版引擎。只需对你的 Agent 说：

> 帮我安装 streamer skill：`https://github.com/Yixiao-Zhang1214/Streamer-skill`

Agent 会自动克隆仓库并注册入口。完成后，在任意终端输入 `/dot-skill-copy` 即可启动。

<details>
<summary><b>🛠️ 想要手动安装？点击查看对应路径</b></summary>

<br>

```bash
git clone https://github.com/Yixiao-Zhang1214/Streamer-skill <TARGET>
```

| 宿主 (Host) | `<TARGET>` 路径 |
|------|-----------------|
| Trae / Claude Code | `~/.claude/skills/dot-skill-copy` |
| OpenClaw | `~/.openclaw/workspace/skills/dot-skill-copy` |
| Codex | `~/.codex/skills/dot-skill-copy` |

</details>

---

## 🚀 使用指南

本仓库的核心能力在于 **Streamer（直播达人）** 的蒸馏与话术生成。以下是生成高转化带货脚本的标准工作流：

### 第一步：蒸馏达人模型 (Distill the Streamer)

1. 在你的 Agent 宿主（如 Trae）中，调用该 skill：
   `/dot-skill-copy`
2. 在被问及要创建的对象类型时，选择 **`streamer`** (数字 4)。
3. 提供该达人的抖音主页链接、目标受众画像，并**强烈建议上传其过往直播的 ASR 逐字稿（.txt 或 .xlsx 格式）**。
4. 引擎将自动对 ASR 进行切片分析，提取深层指标（如语速、提问密度、逼单锚点），并生成该达人专属的 7 阶段方法论模型。

### 第二步：生成带货话术 (Generate Scripts)

当达人模型（例如 `streamer-Xiaozhouz55`）生成完毕后，你可以随时调用它来为新商品撰写话术：

```text
User ❯ 使用 Xiaozhouz55 这个 skill。帮我写一段 CT 小金盘蜜粉的带货话术。
         目标人群是南方的年轻女性。
         价格 299 元，机制是买正装送 2 个粉扑和一支迷你口红。

Xiaozhouz55 ❯ (自动生成 8 段式深度口播话术...)
              "广东的姐妹们，夏天出门是不是一出汗就疯狂脱妆、卡粉？是不是？！..."
```

---

## ✨ 效果演示 (Demo)

> **深度信息提取**：从原始 ASR 逐字稿中解析语速、赠品机制和转化模型，生成高度结构化的 8 段式提词器话术。

```text
User           ❯ 帮我写一段 CT 小金盘的带货话术。目标人群：18-30岁女性，痛点：夏天脱妆。
                 价格299元，加赠2个粉扑和迷你口红。

streamer.skill ❯ ### 1. 吸引停留 · 反常识
                 广东的姐妹们，听我一句劝！夏天买散粉，真别老盯着那些便宜大碗的。
                 稍微出点汗，它就开始结块、斑驳、满脸白芝麻！今天这个CT小金盘为什么我愿意单拎出来讲？...
                 
                 ### 2. 吸引停留 · 代入场景
                 你就想一个很日常的场景，早上出门画了个美美的妆。结果挤个地铁、走几步路，天一热，
                 脸上就开始疯狂出油。一到办公室照镜子，满脸斑驳，是不是特别尴尬？对不对！...
                 
                 (生成完整的 8 段式话术，包含精确的节奏控制与合规机制确认)
```

<div align="center">

📚 你可以查看仓库内的 `skills/streamer/Xiaozhouz55` 目录，获取完整的达人生成产物示例。

</div>

---

## 🔧 核心架构

### 🧱 结构化能力底座

引擎在原有的 Persona（人设）基础上，专为 Streamer 新增了深度的商业化模块：

| 模块类别 | 核心产物 | 附加能力 (Streamer 专属) |
|--------|-----------------|-------------------|
| 🎙️ **Streamer** | 数据底座画像 · 直播间表达基因 (Expression DNA) · 转化模型 · 情绪曲线设计 · 商业人设 | ➕ **带货工作流系统**: 7 阶段 Selling Flow，8 段式深度口播模板，内置 P0/P1 质检系统与合规拦截门槛 |

> **执行逻辑**：接收商品信息 → Persona 决定语气与态度 → 商业模块填充转化逻辑与机制详情 → 输出达人专属的带货话术

---

<div align="center">

**MIT License** © 基于 dot-skill 开源协议

</div>
