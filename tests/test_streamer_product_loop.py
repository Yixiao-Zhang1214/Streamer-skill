from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


TOOLS_DIR = Path(__file__).resolve().parents[1] / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import asr_segmenter  # noqa: E402
import douyin_profile_parser  # noqa: E402
import skill_writer  # noqa: E402
import streamer_deep_metrics  # noqa: E402
import streamer_compliance_check  # noqa: E402
import streamer_script_quality_check  # noqa: E402
import streamer_quality_check  # noqa: E402


class StreamerProductLoopTest(unittest.TestCase):
    def test_douyin_profile_parser_reads_public_html_metadata(self) -> None:
        html = """
        <html>
          <head>
            <title>小美美妆的抖音 - 抖音</title>
            <meta name="description" content="夏季持妆、定妆喷雾、底妆技巧">
            <script type="application/ld+json">
              {"@type":"Person","name":"小美美妆","description":"专注平价美妆直播"}
            </script>
            <script id="RENDER_DATA" type="application/json">
              %7B%22user%22%3A%7B%22nickname%22%3A%22小美美妆%22%2C%22signature%22%3A%22定妆喷雾测评%22%2C%22followerCount%22%3A12345%7D%7D
            </script>
          </head>
        </html>
        """

        fields = douyin_profile_parser.parse_public_profile_html(html)

        self.assertEqual(fields["creator_name"], "小美美妆")
        self.assertIn("定妆", fields["signature"])
        self.assertEqual(fields["follower_count"], "12345")

    def test_douyin_profile_parser_can_skip_public_fetch(self) -> None:
        report = douyin_profile_parser.parse_profile_url(
            "https://www.douyin.com/user/MS4wLjABAAAAQ9L1?from_tab_name=main",
            fetch_public=False,
        )

        self.assertEqual(report["status"], "url_parsed")
        self.assertEqual(report["fields"]["profile_id"], "MS4wLjABAAAAQ9L1")
        self.assertNotIn("public_fetch", report)

    def test_douyin_profile_parser_filters_generic_platform_title(self) -> None:
        html = '<script id="RENDER_DATA" type="application/json">%7B%22name%22%3A%22看精选视频%22%7D</script>'

        fields = douyin_profile_parser.parse_public_profile_html(html)

        self.assertNotIn("creator_name", fields)

    def test_douyin_profile_parser_reads_public_ssr_profile_chunk(self) -> None:
        profile_id = "MS4wLjABAAAAQ9L1"
        html = (
            '<script>self.__pace_f.push([1,'
            '"{\\"uid\\":\\"839681591223438\\",'
            f'\\"secUid\\":\\"{profile_id}\\",'
            '\\"nickname\\":\\"欧气粥粥\\",'
            '\\"desc\\":\\"黄一白、混合肌选手\\",'
            '\\"uniqueId\\":\\"Xiaozhouz55\\",'
            '\\"followerCount\\":1069,'
            '\\"awemeCount\\":262}"])'
            "</script>"
        )

        fields = douyin_profile_parser.parse_public_profile_html(html, target_profile_id=profile_id)

        self.assertEqual(fields["creator_name"], "欧气粥粥")
        self.assertEqual(fields["douyin_id"], "Xiaozhouz55")
        self.assertEqual(fields["uid"], "839681591223438")
        self.assertEqual(fields["sec_uid"], profile_id)
        self.assertEqual(fields["follower_count"], "1069")
        self.assertIn("混合肌", fields["signature"])

    def test_douyin_profile_parser_prefers_public_display_follower_count(self) -> None:
        profile_id = "MS4wLjABAAAAQ9L1"
        html = (
            '<script>self.__pace_f.push([1,'
            '"{\\"uid\\":\\"839681591223438\\",'
            f'\\"secUid\\":\\"{profile_id}\\",'
            '\\"nickname\\":\\"欧气粥粥\\",'
            '\\"followerCount\\":1069355,'
            '\\"mplatformFollowersCount\\":1098692}"])'
            "</script>"
        )

        fields = douyin_profile_parser.parse_public_profile_html(html, target_profile_id=profile_id)

        self.assertEqual(fields["follower_count"], "1098692")
        self.assertEqual(fields["mplatform_follower_count"], "1098692")
        self.assertEqual(fields["account_follower_count"], "1069355")
        self.assertEqual(fields["follower_count_source"], "mplatformFollowersCount")

    def test_streamer_quality_passes_complete_generated_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            base_dir = Path(tmp_dir) / "skills" / "streamer"
            deep_work = "\n".join(
                [
                    "# Work Skill",
                    "## 核心主张",
                    "直播带货必须用价值重构、反问韵律、三层价格和合规事实隔离完成转化。",
                    "## Input Contract",
                    "- 输入商品信息、用户画像、价格机制和证明材料。",
                    "## Selling Flow",
                    "- 留人、种草、信任、报价、转化、互动答疑。",
                ]
                + [
                    "\n".join(
                        [
                            f"### 方法论 {index}：深度转化模型",
                            "**核心逻辑**：把用户从犹豫状态带到明确动作。",
                            "**操作步骤**：先识别痛点，再重构价值，再给链接动作。",
                            "**为什么有效**：用户需要在短时间内知道为什么需要、为什么值、拍哪个。",
                            "**适用场景**：直播间美妆、服装、个护和套装类商品。",
                            "- 诊断维度：痛点、赠品、价格、库存、色号、尺码和售后。",
                            "- 生成要求：每个方法论都必须能直接转成直播间口播动作。",
                            "- 合规：价格、库存、赠品、效果和官方权益必须确认。",
                        ]
                    )
                    for index in range(1, 7)
                ]
                + [
                    "\n".join(
                        [
                            f"### 模板 {index}：可复用话术模板",
                            "```text",
                            "宝宝先别划走，你是不是有 [痛点]？",
                            "不知道怎么选，我给你简化成 [选项]。",
                            "不要只看主品，要看整套到手价值。",
                            "适合就去链接，不适合别硬拍。",
                            "```",
                            "**美妆示例**：脱妆、卡粉、补妆和色号选择。",
                            "**通用示例**：服装、个护、食品和小家电都可迁移。",
                            "**风险边界**：不虚构价格、赠品、库存、效果、排名和官方权益。",
                            "**使用方法**：先替换人群和痛点，再替换商品证据，最后补链接动作。",
                        ]
                    )
                    for index in range(1, 11)
                ]
                + [
                    "## 90 分钟完整直播结构",
                    "- 0-5 分钟建立价值基准。",
                    "- 5-30 分钟高密度循环转化。",
                    "- 30-60 分钟增强催付密度。",
                    "- 60-90 分钟收尾二次转化。",
                    "## 自检清单",
                    "- 价格锚定、赠品价值、决策简化、互动韵律、合规事实逐项检查。",
                    "## 反特征",
                    "- 不写长篇品牌故事，不编价格库存，不用绝对承诺，不让用户慢慢想。",
                    "## 关键指标",
                    "- 问号、平均句长、价格锚点、赠品信号、转化动作都必须进入生成逻辑。",
                    "## Script Generator",
                    "- 话术生成器先诊断商品和人群，再输出直播话术。",
                    "## Compliance Gate",
                    "- 合规过滤禁用词，价格、库存和效果类话术必须标注需确认。",
                ]
                + [
                    "- 补充操作说明：每轮话术都要包含痛点、解决方案、价值重构、信任兜底和链接动作。"
                    for _ in range(340)
                ]
            )
            deep_persona = "\n".join(
                [
                    "# Persona",
                    "## 数据底座",
                    "- 使用公开主页、ASR 指标和用户画像作为证据。",
                    "## Expression DNA",
                    "- 口头禅短促，先叫宝宝再讲商品证明。",
                    "## Signature Phrases",
                    "| 表达 | 功能 | 证据 |",
                    "|---|---|---:|",
                    "| 宝宝 | 召回用户 | 120 |",
                    "| 到手价 | 价格锚定 | 88 |",
                    "| 赠品 | 价值重构 | 42 |",
                    "| 链接 | 转化动作 | 66 |",
                    "## 思维模型",
                    "### 1. 赠品价值重构",
                    "- 先讲整套到手，再讲主品。",
                    "### 2. 价格锚定",
                    "- 先高架锚，再到手锚，再拆分锚。",
                    "### 3. 决策简化",
                    "- 把复杂 SKU 压成明确选项。",
                    "### 4. 反问韵律",
                    "- 用是不是、对不对制造点头节奏。",
                    "### 5. 信任兜底",
                    "- 用官方、售后、证明材料降低风险。",
                    "## 情绪曲线",
                    "- 从平稳种草到转化高峰，再回到答疑。",
                    "## Audience Relationship",
                    "- 观众关系以陪伴、尺码建议和粉丝信任为核心。",
                    "## Anti-Features",
                    "- 不像她的表达：长篇品牌故事、没有链接动作、虚假绝对承诺。",
                    "## Evidence Boundaries",
                    "- 证据不足时说明边界，不可推断私下性格。",
                ]
                + ["- 深度人格维度补充：称呼、节奏、价格、赠品、链接动作和合规边界。" for _ in range(130)]
            )
            skill_dir = skill_writer.create_skill(
                base_dir,
                "pencil_xiaoxin",
                {
                    "character": "streamer",
                    "name": "Pencil Xiaoxin",
                    "classification": {"language": "zh-CN"},
                    "profile": "抖音大码女装直播带货达人。",
                    "tags": ["大码女装", "直播带货"],
                    "knowledge_sources": ["douyin-profile", "live-asr"],
                    "key_metrics": {
                        "question_mark_count": 120,
                        "price_anchor_count": 88,
                        "gift_related_count": 42,
                    },
                },
                deep_work,
                deep_persona,
            )
            raw_dir = skill_dir / "knowledge" / "research" / "raw"
            merged_dir = skill_dir / "knowledge" / "research" / "merged"
            raw_dir.mkdir(parents=True, exist_ok=True)
            merged_dir.mkdir(parents=True, exist_ok=True)
            for name in (
                "01_public_profile_and_scope.md",
                "02_asr_expression_metrics.md",
                "03_conversion_methodology.md",
            ):
                (raw_dir / name).write_text(
                    "research note with profile scope, ASR metrics, conversion methodology, "
                    "evidence boundaries, and category transfer analysis. " * 2,
                    encoding="utf-8",
                )
            (merged_dir / "summary.md").write_text(
                "merged summary with source coverage, public profile scope, ASR metrics, "
                "conversion methodology, audience portrait, evidence boundaries, and compliance risks. " * 2,
                encoding="utf-8",
            )

            report = streamer_quality_check.evaluate_skill(skill_dir)

            self.assertTrue(report["passed"], json.dumps(report, ensure_ascii=False, indent=2))
            self.assertIn("script_generator", report["capabilities"])
            self.assertIn("streamer_deep_metrics", report["streamer_tool_keys"])
            self.assertIn("streamer_compliance_check", report["streamer_tool_keys"])
            self.assertIn("streamer_script_quality_check", report["streamer_tool_keys"])

    def test_streamer_quality_rejects_thin_generated_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            base_dir = Path(tmp_dir) / "skills" / "streamer"
            skill_dir = skill_writer.create_skill(
                base_dir,
                "thin_streamer",
                {
                    "character": "streamer",
                    "name": "Thin Streamer",
                    "classification": {"language": "zh-CN"},
                    "profile": "抖音直播带货达人。",
                    "tags": ["直播带货"],
                    "knowledge_sources": ["douyin-profile"],
                    "key_metrics": {
                        "question_mark_count": 1,
                        "price_anchor_count": 1,
                        "gift_related_count": 1,
                    },
                },
                "\n".join(
                    [
                        "# Work Skill",
                        "## Input Contract",
                        "- 商品信息。",
                        "## Selling Flow",
                        "- 留人、种草、转化。",
                        "## Script Generator",
                        "- 生成直播话术。",
                        "## Compliance Gate",
                        "- 合规。",
                    ]
                ),
                "\n".join(
                    [
                        "# Persona",
                        "## Expression DNA",
                        "- 宝宝、姐妹。",
                        "## Audience Relationship",
                        "- 粉丝关系。",
                        "## Evidence Boundaries",
                        "- 不推断私下性格。",
                    ]
                ),
            )

            report = streamer_quality_check.evaluate_skill(skill_dir)

            self.assertFalse(report["passed"])
            self.assertFalse(report["checks"]["work_depth"])
            self.assertFalse(report["checks"]["persona_depth"])

    def test_compliance_checker_blocks_and_marks_truth_dependent_claims(self) -> None:
        text = "宝宝这个全网最低，今天库存最后 20 件，到手价 99 元，保证有效。"

        report = streamer_compliance_check.evaluate_text(text)

        self.assertFalse(report["passed"])
        self.assertGreaterEqual(report["block_count"], 2)
        self.assertGreaterEqual(report["confirm_count"], 2)
        categories = {finding["category"] for finding in report["findings"]}
        self.assertIn("extreme_claim", categories)
        self.assertIn("price_or_discount", categories)
        self.assertIn("scarcity_or_countdown", categories)

    def test_compliance_checker_allows_negated_risky_examples(self) -> None:
        text = "合规提醒：不使用“全网最低”“绝对不脱妆”“保证有效”等绝对化表达。库存需后台确认。"

        report = streamer_compliance_check.evaluate_text(text)

        self.assertTrue(report["passed"], json.dumps(report, ensure_ascii=False, indent=2))
        self.assertEqual(report["block_count"], 0)
        self.assertGreaterEqual(report["confirm_count"], 1)

    def test_script_quality_checker_passes_rubric_ready_script(self) -> None:
        text = """
        ## 主播版直播话术
        ### 【留人】
        宝宝，夏天出门补妆的姐妹先看这个商品，适合混油皮、通勤党和想要妆面更干净的用户。
        ### 【种草】
        核心卖点是柔焦和补妆：你早上上脸之后，下午鼻翼容易卡粉的时候，用粉扑轻轻按一下，妆面会从油光感变成更干净的雾面状态；不像厚粉饼那样一补就结块，近看还是你的皮肤状态。
        ### 【信任】
        商品参数：0 号色、正装规格、粉扑、替换芯、备案信息、官方售后都按商品卡核对；需确认：赠品是否随单、过敏包退、运费险、七天无理由。
        ### 【报价/福利】
        到手价需确认，赠品需确认，库存需确认；如果商品卡显示权益还在，想要补妆和柔焦的宝宝可以点链接看第 1 号。
        ### 【互动答疑】
        Q: 干皮能不能用？
        A: 干皮姐妹先做好保湿，T 区少量按压，不要整脸厚铺；如果你怕拔干，先看成分和客服建议。
        ### 【机评自检】
        - 指令遵循：商品、场景、人群、卖点都有保留。
        - 事实边界：价格、库存、赠品、售后均标注需确认。
        - 人群匹配：混油皮、通勤补妆、想要柔焦妆效。
        - 场景化卖点：出门补妆场景 + 按压动作 + 油光到雾面状态。
        - 信息丰富度：商品展示、商品参数、适用推荐、使用说明、权威凭证、使用保障。
        - 行业氛围感：肤感、柔焦、雾面、服帖、上妆过程。
        - 促转化：点链接第 1 号、价格利益需确认、赠品库存需确认、干皮使用建议、售后兜底。
        """

        report = streamer_script_quality_check.evaluate_text(text, category="beauty")

        self.assertTrue(report["passed"], json.dumps(report, ensure_ascii=False, indent=2))
        self.assertFalse(report["p0_failed"])
        self.assertIn("product_parameters", report["info_categories"])
        self.assertIn("action_instruction", report["conversion_types"])

    def test_script_quality_checker_rejects_thin_generic_script(self) -> None:
        text = "这个商品品质卓越，买到就是赚到，喜欢就拍。"

        report = streamer_script_quality_check.evaluate_text(text)

        self.assertFalse(report["passed"])
        self.assertIn("selling_point_scenarioization", report["p0_failed"])
        self.assertIn("information_richness", report["p0_failed"])
        self.assertIn("persona_fit", report["p0_failed"])

    def test_goldset_anxiety_pressure_is_blocked(self) -> None:
        text = "宝宝喜欢的你先拍先锁，拍完这波后面尺码一断你再等就麻烦了。"

        quality_report = streamer_script_quality_check.evaluate_text(text)
        compliance_report = streamer_compliance_check.evaluate_text(text)

        self.assertFalse(quality_report["checks"]["compliance_marketing_boundary"])
        self.assertFalse(compliance_report["passed"])
        self.assertIn("anxiety_pressure", {item["category"] for item in compliance_report["findings"]})

    def test_goldset_fluency_rejects_parameter_contradiction(self) -> None:
        text = (
            "宝宝我不跟你堆参数，A19 Pro芯片，八核，全网通5G，双卡双待，"
            "这个带宽你去买普通款都未必买到。"
        )

        report = streamer_script_quality_check.evaluate_text(text)

        self.assertFalse(report["checks"]["fluency"])

    def test_asr_segmenter_extracts_stage_scores_and_commerce_signals(self) -> None:
        text = (
            "欢迎新进直播间，宝宝点关注。"
            "三号链接这套到手价 99 元，S 到 3XL 都有。"
            "尺码不会选的扣身高体重，库存最后 20 件。"
            "下一款马上过款，别走。"
        )

        result = asr_segmenter.segment_text(text)

        self.assertGreaterEqual(result["stage_counts"]["retention_opening"], 1)
        self.assertGreaterEqual(result["signal_counts"]["link"], 1)
        self.assertGreaterEqual(result["signal_counts"]["price"], 1)
        self.assertGreaterEqual(result["signal_counts"]["size"], 1)
        self.assertGreaterEqual(result["signal_counts"]["stock"], 1)
        self.assertIn("records", result)
        self.assertTrue(any(record["signals"] for record in result["records"]))

    def test_streamer_deep_metrics_extracts_persuasion_signals(self) -> None:
        text = "宝宝是不是会卡粉？我帮你算，到手九十九，赠品送完就没了，三二一去链接拍。"

        result = streamer_deep_metrics.evaluate_text(text)

        self.assertGreaterEqual(result["question_mark_count"], 1)
        self.assertGreaterEqual(result["pattern_counts"]["address_terms"], 1)
        self.assertGreaterEqual(result["pattern_counts"]["price_anchor"], 1)
        self.assertGreaterEqual(result["pattern_counts"]["gift"], 1)
        self.assertGreaterEqual(result["pattern_counts"]["conversion_actions"], 1)


if __name__ == "__main__":
    unittest.main()
