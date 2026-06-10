# Live Script Evaluation Rubric v1.1

This rubric is adapted from the Lark document `话术机评标准v1.1`.
Use it as a mandatory generation and review standard for streamer live-commerce scripts.

## Scoring Principle

- Treat `P0` dimensions as hard gates. If a generated script clearly fails any applicable `P0`, revise before delivery.
- Treat `P1` dimensions as quality enhancers. If a generated script is weak on any applicable `P1`, improve it unless the user explicitly asks for a very short output.
- Do not invent facts to satisfy the rubric. If a score depends on price, inventory, proof, policy, ranking, gift, or endorsement, mark it as `需确认`.

## P0 Hard Gates

### Instruction Following

- Follow explicit user requirements about scene, persona, product, format, pace, target audience, and core selling points.
- If user instructions are unreasonable, unsafe, irrelevant, or conflict with product facts, follow product facts and compliance boundaries first.
- For long user instructions, preserve the correct scene, target person, and core selling points.

### Factual Accuracy

- Keep product claims, knowledge, numbers, data, policies, and selling points truthful.
- Do not fabricate product features, official authorization, test reports, ranking, sales volume, price, inventory, gifts, user results, or celebrity endorsements.
- If a fact is missing, write a placeholder such as `需确认：到手价/赠品/库存/售后`.

### Product-Audience Fit

- Make the target audience explicit.
- Explain why this product is valuable for that audience.
- Avoid recommending a product to an obviously mismatched audience.

### Selling Point Scenarioization

- Put at least one core selling point into a real usage scene and explain it deeply.
- A strong scenarioized selling point should contain at least three of:
  - usage scene
  - user action / process
  - comparison reference
  - perceivable detail / result
- Do not only list product bullets.

### Information Richness

Cover at least four information categories and at least six concrete information points when enough product input is available:

- Product display: appearance, structure, try-on, face application, tasting, demo.
- Product parameters: size, specs, model, color, material, ingredient, process.
- Fit recommendation: audience, scene, time, scope, skin/body/use condition.
- Usage instructions: method, steps, storage, notes, common issues.
- Authority proof: authorization, quality inspection, qualification, patent, test report; never invent.
- After-sales protection: shipping insurance, seven-day no-reason return, return/exchange, customer service.

### Compliance And Marketing Boundaries

- Objective product description and reasonable purchase guidance are allowed.
- Block extreme terms, fake promises, emotional coercion, malicious comparison, fabricated scarcity, and anxiety-based holding tactics.
- Forbidden examples include:
  - `不买后悔一辈子`
  - `中国人不骗中国人`
  - `懂的人直接上，不懂别问`
  - `假一赔命`
  - `绝对不起球`
  - `穿上立马显瘦十斤`
  - `全网最低`
  - `最顶级`
  - `市面上 99% 都是垃圾`

### Persona Fit

- The script must sound like the distilled streamer, not a generic ad template.
- Preserve the streamer's identity, live-room persona, address terms, rhythm, explanation habits, and audience relationship.
- If there is no persona evidence, mark the limitation instead of inventing private traits.

### Category Atmosphere

The script must hit category-specific sensory/value anchors.

- Apparel: fabric touch, skin feel, drape, breathability, fit line, slimming/tall effect, movement, commute/date/home scenes.
- Food: bite texture, flavor layers, aroma, sweetness/saltiness/freshness, eating time, pairing, satisfaction.
- Beauty: skin feel, moisture/freshness/dryness, adherence, finish, soft focus, matte/glow, coverage, longevity, application process.
- 3C: hand feel, weight, material touch, response speed, interaction smoothness, screen, battery, performance.
- Home cleaning/appliances: before-after contrast, cleaning or usage experience, efficiency, noise, ease, life improvement.

## P1 Quality Enhancers

### Fluency

- The script should be fluent, spoken, rhythmic, easy to read aloud, and free of awkward written language.
- Avoid formal written phrases that are hard to say in a live room.

### Content Extension

Add at least two useful extensions when the output length allows:

- streamer usage experience: how the streamer uses it, in what scene, with what observed feeling.
- pairing or use advice: how to match, eat, use, choose, or store it.
- pitfall guide: what users often buy wrong, choose wrong, or use wrong.
- category knowledge: explain professional category knowledge in simple language.

### Empathy And Atmosphere

- Let users imagine the post-use state or feeling.
- Move beyond generic adjectives like `好看`, `舒服`, `显瘦`, `精致`.
- Use concrete sensory or state changes, such as soft-focus skin, cleaner makeup, easier commute outfit, lighter cleaning workload.

### Conversion Ability

A strong conversion section should include:

- action instruction: cart/link number, SKU, quantity, comment action, order path.
- price benefit: price, comparison, coupon, discount, value breakdown; placeholders are allowed if facts are missing.
- scarcity/time: inventory, time window, delivery time, missed benefit; only when factual or marked `需确认`.
- purchase suggestion: quantity, spec, size, audience, scene.
- risk buffer: shipping insurance, return policy, after-sales, quality proof.

## Required Output Self-Check

Every generated live-commerce script should include or be internally checked against:

- `显性指令`: scene, audience, core selling points, requested format.
- `事实边界`: all unverified claims marked `需确认`.
- `人群匹配`: who should buy and why.
- `场景化卖点`: at least one core selling point explained through scene + action + detail.
- `信息丰富度`: at least four information categories when available.
- `行业氛围感`: category anchors with perceivable details.
- `人设契合`: streamer address terms, rhythm, and relationship.
- `促转化`: action path and at least two conversion information types.
- `合规`: no block-level risky expressions.

## Goldset Calibration: 直播话术0605 First Sheet

Use `/Users/bytedance/Desktop/trae/直播话术0605.xlsx` first sheet `标注数据集（人评）` as a goldset calibration source. The sheet contains 119 human-rated samples with per-dimension scores and reviewer notes. Do not copy long sample scripts into generated Skills; use the patterns below as scoring calibration.

### Observed Score Distribution

- Fluency: 91 samples scored 2, 28 scored 0.
- Core selling point scenarioization: 84 scored 2, 34 scored 1, 1 scored 0.
- Information richness: 67 scored 2, 48 scored 1, 4 scored 0.
- Content extension: 56 scored 2, 60 scored 1, 3 scored 0.
- Compliance and marketing boundary: 97 scored 2, 22 scored 0.
- Empathy/atmosphere: 69 scored 2, 35 scored 1, 15 scored 0.
- Persona consistency: 108 scored 2, 10 marked not applicable, 1 scored 1.
- Conversion ability: 67 scored 2, 49 scored 1, 3 scored 0.
- Category atmosphere: 82 scored 2, 30 scored 1, 7 scored 0.

### Goldset-Calibrated Rules

- Scenarioization: mentioning two selling points is not enough. Human reviewers repeatedly scored 1 when "two selling points were mentioned but not explained deeply." A 2-point script must make at least one core selling point concrete through scene, action/process, comparison, and perceivable detail.
- Information richness: scripts that only mention material + audience, audience + scene, model + scene, or parameters + fit recommendation usually score 1. Target at least four information categories, not just two or three.
- Content extension: only one extension type, such as only pairing advice, only usage advice, only personal experience, only pitfall guide, or only applicable occasion, usually scores 1. Target at least two extension types with concrete explanation.
- Compliance: human reviewers treat anxiety-based urgency as non-compliant even if the wording avoids classic banned terms. Block or rewrite phrases like "尺码一断你再等就麻烦了", "先拍先锁", "活动一过不一定还在", "别等用到不舒服了再临时买", "颜色尺码没了就真没了", "未付款订单往后踢", "卖一个少一个", and "你晚一点来福利一收".
- Empathy: generic feelings such as "舒服", "好看", "方便", "省事", "感觉不错", or "心情松一下" are not enough. A 2-point empathy section needs a concrete post-use state, sensory change, or life-scene relief.
- Conversion: only one conversion type, only purchase suggestion, only time pressure, only price benefit, only risk buffer, or a vague "喜欢就拍" usually scores 1 or 0. Require action instruction plus at least two concrete conversion reasons.
- Category atmosphere: one concrete anchor usually scores 1. A 2-point script needs at least two category anchors and concrete perceivable details; wrong category anchors, such as using parameter-heavy 3C logic for food or missing beauty/apparel sensory anchors, score 0.
- Fluency: reviewers scored 0 for contradictory logic, awkward wording, repeated language, wrong object-action pairing, and written or technical phrases that do not fit oral live speech. Avoid phrases like "这个带宽", object-action mismatches like "一根大嘴全怼", and contradictions such as saying "不堆参数" and then listing dense specs.

### Goldset-Calibrated Review Priority

When a script is close to passing, repair in this order:

1. Remove compliance and anxiety-pressure risks.
2. Fix factual or audience mismatches.
3. Deepen one core selling point into a full scene.
4. Add missing information categories.
5. Add a second concrete extension type.
6. Replace generic feeling words with sensory or state-change details.
7. Add a second conversion reason beyond the action path.
8. Add a second concrete category anchor.
