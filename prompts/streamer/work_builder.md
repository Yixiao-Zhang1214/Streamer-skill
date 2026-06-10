# Streamer Work Builder

Build `work.md` for a Douyin live-commerce creator. This document defines the commercial method, script-generation workflow, reusable templates, and compliance operating system.

The output must be a deep operational method model, comparable to or stronger than the `livestream-host-zhouzhou` reference style. It should be useful for writing scripts, training new hosts, auditing scripts, and migrating the streamer's method across adjacent categories.
It must also embed the live-script evaluation rubric from `references/script_evaluation_rubric.md` so runtime scripts can be judged against instruction following, factual accuracy, audience fit, scenarioized selling points, information richness, persona fit, category atmosphere, and conversion ability.

## Minimum Depth Standard

- Target length: roughly 350-550 lines unless source material is genuinely thin.
- Include 5-8 named methodology models with logic, steps, use cases, and risk boundaries.
- Include a reusable template bank: retention, pain awakening, solution, gift/value reconstruction, price anchoring, trust buffer, conversion, objection handling, short loops.
- Include a full live-session structure such as 5-minute loop and 60/90-minute flow.
- Include a live-room self-check checklist.
- Include a `Script Evaluation Rubric` or `机评标准` section that separates P0 hard gates from P1 quality enhancers.
- Include category migration rules and anti-features.
- Include a `Compliance Gate` that separates performance atmosphere from truth-dependent claims.
- Never paste long transcript blocks; use summarized patterns and phrase-level markers only.

## Required Sections

```markdown
# Work Skill: {creator_name} Live-Commerce Methodology

## Scope
- Generate live-commerce scripts from product information and user portraits.
- Generate stage-based teleprompter copy, short loops, product-card bullets, and comment replies.
- Refuse or rewrite claims that fail the compliance layer.

## Input Contract
- Product information: name, category, specs, material, price, benefits, images, inventory truth.
- User portrait: body type / need / budget / scene / concern.
- Campaign context: price mechanism, coupon, stock, delivery, return policy, proof material.
- Compliance config: banned words, sensitive categories, truth-dependent claims.

## Selling Flow
### 1. 吸引停留 · 反常识 (Retention / Counter-Intuitive)
### 2. 吸引停留 · 代入场景 (Retention / Relatable Scene)
### 3. 吸引停留 · 价效对比 (Retention / Value Prop)
### 4. 商品讲解 · 材质体感拆解 (Seeding / Sensory Breakdown)
### 5. 商品讲解 · 肤质/身材痛点代入 (Seeding / Pain Point)
### 6. 信任背书 · 身份/保障背书 (Trust / Guarantee)
### 7. 引导互动 · 决策建议互动 (Interaction / Driving Choices)
### 8. 转化促单 · 季节窗口+风险兜底 (Conversion / Risk Reversal)

## Core Methodology Models
- Value reconstruction / gift-first model.
- Price anchoring and unit economics model.
- SKU naming and decision-simplification model.
- Question-rhythm interaction model.
- Conversion-loop model.
- Scarcity and stock-trigger model.
- Trust buffer and risk-reversal model.

## Template Bank
- 10s retention hook.
- 30s pain awakening.
- Solution and SKU selection.
- Gift/value reconstruction.
- Three-layer price anchoring.
- Trust/risk buffer.
- Inventory conversion.
- Objection handling by audience concern.
- 15s / 30s / 60s short loops.

## Full Live Flow
- 5-minute teleprompter loop.
- 60/90-minute session structure.
- Cold-room recovery.
- New-user and old-user routing.

## Script Generator Rules
- Diagnose the product and audience first.
- Pick the matching selling flow.
- Inject persona phrasing only after the structure is correct.
- Apply the script evaluation rubric before final output: preserve user instructions, mark factual boundaries, show audience fit, scenarioize at least one core selling point, cover enough information categories, include category atmosphere, and provide conversion action.
- Run compliance filtering before final output.
- Mark stock, price, ranking, and effect claims that require factual confirmation.

## Script Evaluation Rubric
- P0 hard gates: instruction following, factual accuracy, product-audience fit, scenarioized selling point, information richness, compliance boundary, persona fit, category atmosphere.
- P1 quality enhancers: fluency, content extension, empathy/atmosphere, conversion ability.
- Information richness target: at least 4 categories and 6 concrete points when source input supports it.
- Scenarioization target: at least one core selling point with usage scene, action/process, comparison reference, and perceivable detail.
- Conversion target: action instruction plus at least two conversion information types.
- Runtime check command: `python3 tools/streamer_script_quality_check.py "{script_file}"`.

## Output Formats
- Full 8-segment live-room script (under 800 words).
- 15s / 30s / 60s short loop.
- Comment reply bank.
- Product-card bullet copy.
- A/B versions by audience pain point.

## Compliance Gate
- Extreme claims are forbidden.
- Medical, financial, and health-effect claims require refusal or safe rewrite.
- Price, stock, sales rank, and discount claims must be truthful and user-provided.

## Anti-Features
- What not to do if trying to sound like this streamer.
- Long brand essays without link actions.
- Claims that sound powerful but are unsupported.
- Soft seeding without conversion structure.
```
