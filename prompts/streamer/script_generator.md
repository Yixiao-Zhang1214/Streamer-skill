# Streamer Script Generator

Use this prompt at runtime when the user provides product information and user portraits.
Read `references/script_evaluation_rubric.md` before drafting. The final script must satisfy the rubric's P0 hard gates and should improve P1 dimensions when output length allows.

## Pipeline

1. **Parse input**: product, specs, price mechanism, audience, proof, risks, required output format.
2. **Diagnose fit**: identify the audience pain point and the strongest truthful selling angle.
3. **Apply methodology**: map to Retention -> Seeding -> Trust -> Price -> Conversion -> Interaction.
4. **Apply persona**: add the creator's address terms, rhythm, proof gestures, and emotional curve.
5. **Rubric check**: enforce instruction following, factual boundary, audience fit, scenarioized selling point, information richness, persona fit, category atmosphere, and conversion ability.
6. **Compliance check**: remove banned claims, rewrite risky phrases, and mark truth-dependent claims.
7. **Output structured script**: make it directly speakable.

## Default Output

When generating a full live-room script (长口播), follow this 8-segment structure. Keep the total length under 800 words. Do not invent price, stock, or identity facts.

```markdown
## 主播版直播话术 (8段式深度版)

### 1. 吸引停留 · 反常识
{script: challenge a common misconception about the product or category to grab attention}

### 2. 吸引停留 · 代入场景
{script: paint a relatable, concrete usage scene for the target audience}

### 3. 吸引停留 · 价效对比
{script: explain the value proposition compared to conventional options; mark mechanism as 需确认}

### 4. 商品讲解 · 材质体感拆解
{script: explain the texture, material, or sensory experience in detail}

### 5. 商品讲解 · 肤质/身材痛点代入
{script: map the product features to specific audience physical or emotional pain points}

### 6. 信任背书 · 身份/保障背书
{script: include creator's personal guarantee or official after-sales; mark as 需确认}

### 7. 引导互动 · 决策建议互动
{script: ask a question that helps the user choose a version/size/spec; drive comments}

### 8. 转化促单 · 季节窗口+风险兜底
{script: emphasize the current timing and risk reversal policies; mark as 需确认}

### 【机评自检】
- 指令遵循：{scene / audience / core selling points preserved}
- 事实边界：{price / stock / gift / official policy / proof / endorsement needing confirmation}
- 人群匹配：{target user and why this product fits}
- 场景化卖点：{scene + action/process + detail}
- 信息丰富度：{covered info categories}
- 行业氛围感：{category sensory/value anchors}
- 促转化：{action instruction + conversion reason types}

### 【合规提醒】
- {claims needing confirmation}
- {rewritten or removed risky phrases}
```

For short loops or replies, use a condensed version of the above.

## Rules

- Do not invent price, stock, sales rank, material test, certifications, or user results.
- Do not use absolute superiority claims.
- If a needed fact is missing, either ask a concise follow-up or output a placeholder marked `需确认`.
- Keep the script in the creator's live-room persona, not a generic ad style.
- P0 hard gates: instruction following, factual accuracy, product-audience fit, scenarioized selling point, information richness, compliance boundary, persona fit, and category atmosphere.
- P1 upgrades: fluency, content extension, empathy/atmosphere, and conversion ability.
- Information richness target: cover at least 4 categories and 6 concrete points when product input supports it.
- Conversion target: include a clear action instruction and at least 2 conversion information types: price benefit, scarcity/time, purchase suggestion, or risk buffer.
- Category atmosphere target: include at least 2 concrete anchors for the product category, such as beauty skin feel / finish / application process, apparel fabric / fit / scene, food texture / flavor / eating scene.
- Before presenting the final script, write it to a temporary file and run `python3 tools/streamer_script_quality_check.py "{script_file}"`; if P0 fails, revise first.
