#!/usr/bin/env python3
"""Rubric checks for generated live-commerce scripts."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


INFO_CATEGORY_PATTERNS = {
    "product_display": [r"上身", r"上脸", r"试吃", r"展示", r"外观", r"结构", r"妆后", r"试穿"],
    "product_parameters": [r"尺寸", r"规格", r"型号", r"颜色", r"色号", r"材质", r"成分", r"工艺", r"面料"],
    "fit_recommendation": [r"适合", r"人群", r"场景", r"通勤", r"肤质", r"身材", r"尺码", r"油皮", r"干皮"],
    "usage_instruction": [r"怎么用", r"用法", r"步骤", r"先.*再", r"注意", r"保存", r"选择", r"拍[一二三四五六七八九十\d]+"],
    "authority_proof": [r"备案", r"授权", r"质检", r"检测", r"报告", r"专利", r"资质", r"官方"],
    "after_sales": [r"运费险", r"七天无理由", r"7\s*天", r"退换", r"售后", r"客服", r"包邮"],
}

CATEGORY_ANCHORS = {
    "apparel": [r"面料", r"垂感", r"透气", r"上身", r"版型", r"显瘦", r"显高", r"腰线", r"通勤"],
    "food": [r"口感", r"酥", r"脆", r"绵密", r"糯", r"弹", r"香", r"甜", r"鲜", r"搭配"],
    "beauty": [r"肤感", r"清爽", r"不拔干", r"服帖", r"柔焦", r"雾面", r"光泽", r"遮瑕", r"持妆", r"上妆"],
    "electronics": [r"手感", r"重量", r"握持", r"响应", r"流畅", r"屏幕", r"续航", r"性能"],
    "home": [r"清洁", r"前后对比", r"效率", r"噪音", r"省心", r"便捷", r"生活"],
}

CONVERSION_PATTERNS = {
    "action_instruction": [r"链接", r"小黄车", r"拍[一二三四五六七八九十\d]+", r"下单", r"付款", r"点.*号"],
    "price_benefit": [r"到手价", r"券后", r"优惠", r"折算", r"原价", r"\d+\s*元", r"价格"],
    "scarcity_or_time": [r"库存", r"限时", r"今晚", r"最后", r"倒计时", r"恢复原价", r"发货"],
    "purchase_suggestion": [r"建议拍", r"适合.*拍", r"选.*号", r"拍.*件", r"大一码", r"规格"],
    "risk_buffer": [r"运费险", r"七天无理由", r"退换", r"售后", r"客服", r"官方", r"备案"],
}

EXTENSION_PATTERNS = {
    "usage_experience": [r"我.*用", r"我.*试", r"我.*上脸", r"我.*穿", r"我.*感受"],
    "pairing_or_usage_advice": [r"搭配", r"怎么用", r"怎么选", r"先.*再", r"建议.*用", r"通勤.*配"],
    "pitfall_guide": [r"别买错", r"别选错", r"不要只看", r"容易.*错", r"避坑"],
    "category_knowledge": [r"粉质", r"肤质", r"版型", r"面料", r"成分", r"工艺", r"品类"],
}

BLOCK_PHRASES = [
    r"不买.*后悔一辈子",
    r"中国人不骗中国人",
    r"懂的人直接上",
    r"不懂别问",
    r"假一赔命",
    r"绝对不起球",
    r"立马显瘦十斤",
    r"全网最低",
    r"最顶级",
    r"99%\s*都(?:是)?垃圾",
    r"尺码.*一断.*麻烦",
    r"先拍先锁",
    r"活动一过.*不一定",
    r"别等.*再临时买",
    r"错过这场.*不一定",
    r"颜色尺码没了.*真没了",
    r"福利库存不会放太久",
    r"未付款订单.*往后踢",
    r"卖一个少一个",
    r"不代表.*下次.*还有",
    r"晚一点来.*福利一收",
]

GENERIC_AD_WORDS = [r"品质卓越", r"尊贵体验", r"奢华享受", r"买到就是赚到"]
AWKWARD_GOLDSET_PATTERNS = [
    r"这个带宽",
    r"一根大嘴全怼",
    r"家里日常慢慢吃也有时间安排",
    r"压片的东西",
    r"不堆参数[\s\S]{0,120}(?:芯片|八核|全网通|双卡|UV400|mm)",
]


def count_matches(text: str, patterns: list[str]) -> int:
    """Count how many regex patterns appear in text."""
    return sum(1 for pattern in patterns if re.search(pattern, text, re.IGNORECASE))


def matched_keys(text: str, pattern_map: dict[str, list[str]]) -> list[str]:
    """Return keys whose pattern list appears at least once."""
    return [key for key, patterns in pattern_map.items() if count_matches(text, patterns)]


def evaluate_text(text: str, category: str = "auto") -> dict:
    """Evaluate a generated script against the live-script rubric."""
    info_categories = matched_keys(text, INFO_CATEGORY_PATTERNS)
    conversion_types = matched_keys(text, CONVERSION_PATTERNS)
    extension_types = matched_keys(text, EXTENSION_PATTERNS)
    category_anchor_hits = evaluate_category_anchors(text, category)
    block_findings = find_block_findings(text)
    unconfirmed_truth_claims = find_unconfirmed_truth_claims(text)

    checks = {
        "instruction_following_markers": has_instruction_following_markers(text),
        "factual_boundary": not unconfirmed_truth_claims and "需确认" in text,
        "product_audience_fit": contains_any(text, [r"适合", r"人群", r"宝宝", r"姐妹", r"用户", r"肤质", r"身材"]),
        "selling_point_scenarioization": has_scenarioized_selling_point(text),
        "information_richness": len(info_categories) >= 4 and count_information_points(text) >= 6,
        "compliance_marketing_boundary": not block_findings,
        "persona_fit": has_persona_fit(text),
        "category_atmosphere": category_anchor_hits["passed"],
        "fluency": has_fluency(text),
        "content_extension": len(extension_types) >= 2,
        "empathy_atmosphere": has_empathy_atmosphere(text),
        "conversion_ability": has_conversion_ability(conversion_types),
    }
    p0_keys = {
        "instruction_following_markers",
        "factual_boundary",
        "product_audience_fit",
        "selling_point_scenarioization",
        "information_richness",
        "compliance_marketing_boundary",
        "persona_fit",
        "category_atmosphere",
    }
    return {
        "passed": all(checks[key] for key in p0_keys),
        "checks": checks,
        "p0_failed": sorted(key for key in p0_keys if not checks[key]),
        "p1_failed": sorted(key for key, passed in checks.items() if key not in p0_keys and not passed),
        "info_categories": info_categories,
        "conversion_types": conversion_types,
        "extension_types": extension_types,
        "category_anchor_hits": category_anchor_hits,
        "block_findings": block_findings,
        "unconfirmed_truth_claims": unconfirmed_truth_claims,
        "recommendations": build_recommendations(checks, info_categories, conversion_types, extension_types),
    }


def contains_any(text: str, patterns: list[str]) -> bool:
    """Return whether any pattern appears in text."""
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


def has_instruction_following_markers(text: str) -> bool:
    """Require markers that preserve user-provided scene, product, audience, and selling points."""
    markers = [r"商品", r"卖点", r"适合|人群|宝宝|姐妹", r"场景|通勤|上脸|上身|使用"]
    return all(contains_any(text, [marker]) for marker in markers)


def has_scenarioized_selling_point(text: str) -> bool:
    """Require scene + action/process + perceivable detail/comparison."""
    dimensions = [
        [r"场景", r"通勤", r"约会", r"上班", r"夏天", r"出门", r"补妆", r"上身", r"上脸"],
        [r"先.*再", r"抹", r"拍", r"穿", r"搭", r"用", r"走路", r"照镜子", r"补"],
        [r"对比", r"不像", r"更", r"从.*到", r"前后"],
        [r"柔焦", r"雾面", r"垂感", r"透气", r"绵密", r"清爽", r"细腻", r"不卡", r"不闷"],
    ]
    return sum(contains_any(text, group) for group in dimensions) >= 3


def count_information_points(text: str) -> int:
    """Approximate concrete information points with bullets and semantically dense clauses."""
    bullet_count = len(re.findall(r"^\s*(?:[-*]|\d+[.、])\s+", text, re.MULTILINE))
    fact_clause_count = len(re.findall(r"(?:：|:).{2,40}", text))
    return bullet_count + fact_clause_count


def has_persona_fit(text: str) -> bool:
    """Require live-room persona markers instead of generic ad copy."""
    return (
        contains_any(text, [r"宝宝", r"姐妹", r"我帮你", r"我跟你说", r"是不是", r"对不对"])
        and not contains_any(text, GENERIC_AD_WORDS)
    )


def evaluate_category_anchors(text: str, category: str) -> dict:
    """Evaluate whether category-specific sensory/value anchors are present."""
    categories = [category] if category in CATEGORY_ANCHORS else list(CATEGORY_ANCHORS)
    hits = {
        key: count_matches(text, CATEGORY_ANCHORS[key])
        for key in categories
    }
    best_category = max(hits, key=hits.get) if hits else "auto"
    return {
        "passed": hits.get(best_category, 0) >= 2,
        "category": best_category,
        "hit_count": hits.get(best_category, 0),
        "all_hits": hits,
    }


def has_fluency(text: str) -> bool:
    """Reject obvious written-register or awkward scripts."""
    if contains_any(text, [r"此款", r"方面呈现", r"亦是", r"十分优惠", *AWKWARD_GOLDSET_PATTERNS]):
        return False
    long_lines = [line for line in text.splitlines() if len(line) > 180]
    return len(long_lines) <= 2


def has_empathy_atmosphere(text: str) -> bool:
    """Require concrete post-use feeling or state changes."""
    return contains_any(
        text,
        [
            r"状态",
            r"感觉",
            r"上脸.*(?:像|是|会|更)",
            r"穿上.*(?:像|显|更|不)",
            r"用完.*(?:更|不|省|轻松)",
            r"近看",
            r"出门.*(?:更|不用|不怕)",
        ],
    )


def has_conversion_ability(conversion_types: list[str]) -> bool:
    """Require action instruction plus at least one more conversion reason."""
    return "action_instruction" in conversion_types and len(conversion_types) >= 2


def find_block_findings(text: str) -> list[dict]:
    """Find rubric-level marketing boundary violations."""
    findings = []
    for regex in BLOCK_PHRASES:
        for match in re.finditer(regex, text, re.IGNORECASE):
            findings.append({"category": "rubric_block", "match": match.group(0), "start": match.start(), "end": match.end()})
    return findings


def find_unconfirmed_truth_claims(text: str) -> list[str]:
    """Return truth-dependent claims that should be marked for confirmation."""
    risky = []
    patterns = [
        r"(?:库存|限量|最后)\s*\d+",
        r"(?:全网|平台|销量|排名).{0,8}(?:第一|TOP|前三)",
        r"(?:官方旗舰|过敏包退|运费险|七天无理由)",
        r"(?:赠|送).{0,12}(?:正装|替换芯|小样|礼盒|粉扑)",
    ]
    for pattern in patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            window = text[max(0, match.start() - 20): min(len(text), match.end() + 20)]
            if "需确认" not in window and "以商品卡为准" not in window and "以页面为准" not in window:
                risky.append(match.group(0))
    return risky


def build_recommendations(
    checks: dict[str, bool],
    info_categories: list[str],
    conversion_types: list[str],
    extension_types: list[str],
) -> list[str]:
    """Create actionable repair suggestions."""
    recommendations = []
    if not checks["selling_point_scenarioization"]:
        recommendations.append("Add a scenarioized core selling point with scene, action/process, comparison, and perceivable detail.")
    if not checks["information_richness"]:
        recommendations.append(f"Expand information categories; current categories: {', '.join(info_categories) or 'none'}.")
    if not checks["category_atmosphere"]:
        recommendations.append("Add at least two category-specific sensory/value anchors with concrete details.")
    if not checks["conversion_ability"]:
        recommendations.append(f"Add action instruction plus conversion reasons; current conversion types: {', '.join(conversion_types) or 'none'}.")
    if not checks["content_extension"]:
        recommendations.append(f"Add at least two useful extensions; current extension types: {', '.join(extension_types) or 'none'}.")
    if not checks["factual_boundary"]:
        recommendations.append("Mark unverified price, stock, gifts, official policy, proof, and endorsements as 需确认.")
    return recommendations


def main() -> None:
    parser = argparse.ArgumentParser(description="Check a live-commerce script against the v1.1 evaluation rubric")
    parser.add_argument("path", help="Text or markdown file to scan")
    parser.add_argument("--category", default="auto", choices=["auto", *CATEGORY_ANCHORS.keys()])
    parser.add_argument("--json", action="store_true", help="Print JSON output")
    args = parser.parse_args()

    report = evaluate_text(Path(args.path).read_text(encoding="utf-8"), category=args.category)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    for name, passed in report["checks"].items():
        print(f"{'PASS' if passed else 'FAIL'}  {name}")
    if report["p0_failed"]:
        print("P0_FAILED " + ", ".join(report["p0_failed"]))
    if report["p1_failed"]:
        print("P1_FAILED " + ", ".join(report["p1_failed"]))
    print(f"OVERALL {'PASS' if report['passed'] else 'FAIL'}")


if __name__ == "__main__":
    main()
