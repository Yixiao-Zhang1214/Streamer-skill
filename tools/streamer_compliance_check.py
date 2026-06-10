#!/usr/bin/env python3
"""Compliance checks for live-commerce scripts.

The checker is intentionally conservative: it flags risky language and tells the
caller which claims need factual confirmation instead of trying to approve legal
copy on its own.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


BLOCK_PATTERNS = {
    "extreme_claim": [
        r"全网最低",
        r"全国第一",
        r"行业第一",
        r"国家级",
        r"顶级",
        r"绝对",
        r"永久",
        r"100%",
        r"零风险",
        r"保证(?:有效|见效|瘦|赚钱|收益|治)",
        r"\b(best|number\s*one|guaranteed|risk[- ]free)\b",
    ],
    "medical_or_health_effect": [
        r"根治",
        r"治疗",
        r"治愈",
        r"药效",
        r"降血糖",
        r"降血压",
        r"减肥(?:效果|疗程)",
        r"\b(cure|treat|medical effect)\b",
    ],
    "financial_return": [
        r"稳赚",
        r"保本",
        r"收益保证",
        r"投资回报",
        r"\bguaranteed return\b",
    ],
    "fabricated_proof": [
        r"官方认证",
        r"国家认证",
        r"明星同款",
        r"销量第一",
        r"平台第一",
        r"\bcertified by\b",
    ],
    "anxiety_pressure": [
        r"中国人不骗中国人",
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
    ],
}

TRUTH_DEPENDENT_PATTERNS = {
    "price_or_discount": [r"原价", r"到手价", r"券后", r"补贴", r"最低价", r"\d+\s*元"],
    "scarcity_or_countdown": [r"库存", r"限量", r"最后", r"倒计时", r"马上没了"],
    "sales_or_ranking": [r"销量", r"复购", r"排名", r"爆单", r"卖爆"],
    "material_or_origin": [r"纯棉", r"真丝", r"羊毛", r"进口", r"原产地", r"工厂直供"],
    "shipping_or_after_sales": [r"包邮", r"运费险", r"七天无理由", r"退换", r"售后"],
}

NEGATION_CONTEXT = re.compile(
    r"(不使用|不说|不要说|不能说|禁止|禁用|避免|移除|改写|不用|不得|不可|不要)",
    re.IGNORECASE,
)


def is_negated_context(text: str, start: int, end: int) -> bool:
    """Return whether a risky phrase is mentioned as a prohibited example."""
    prefix = text[max(0, start - 18):start]
    suffix = text[end:min(len(text), end + 8)]
    return bool(NEGATION_CONTEXT.search(prefix) or re.search(r"(等|这类)?表达", suffix))


def find_matches(text: str, patterns: dict[str, list[str]], severity: str) -> list[dict]:
    """Return matching compliance findings."""
    findings = []
    for category, regexes in patterns.items():
        for regex in regexes:
            for match in re.finditer(regex, text, re.IGNORECASE):
                if severity == "block" and is_negated_context(text, match.start(), match.end()):
                    continue
                findings.append(
                    {
                        "severity": severity,
                        "category": category,
                        "match": match.group(0),
                        "start": match.start(),
                        "end": match.end(),
                    }
                )
    return findings


def evaluate_text(text: str) -> dict:
    """Evaluate a generated live-commerce script."""
    block_findings = find_matches(text, BLOCK_PATTERNS, "block")
    confirm_findings = find_matches(text, TRUTH_DEPENDENT_PATTERNS, "confirm")
    findings = sorted(block_findings + confirm_findings, key=lambda item: item["start"])
    return {
        "passed": not block_findings,
        "block_count": len(block_findings),
        "confirm_count": len(confirm_findings),
        "findings": findings,
        "recommendations": build_recommendations(block_findings, confirm_findings),
    }


def build_recommendations(block_findings: list[dict], confirm_findings: list[dict]) -> list[str]:
    """Create concise next steps for the caller."""
    recommendations = []
    if block_findings:
        recommendations.append("Rewrite or remove block-level claims before publishing.")
    if confirm_findings:
        recommendations.append("Verify price, stock, ranking, material, shipping, and after-sales facts with the user.")
    if not block_findings and not confirm_findings:
        recommendations.append("No obvious compliance triggers were detected by the starter rule set.")
    return recommendations


def main() -> None:
    parser = argparse.ArgumentParser(description="Check live-commerce copy for compliance risks")
    parser.add_argument("path", help="Text or markdown file to scan")
    parser.add_argument("--json", action="store_true", help="Print JSON output")
    args = parser.parse_args()

    report = evaluate_text(Path(args.path).read_text(encoding="utf-8"))
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    for finding in report["findings"]:
        print(
            f"{finding['severity'].upper()}  {finding['category']}  "
            f"{finding['match']}  [{finding['start']}:{finding['end']}]"
        )
    print(f"OVERALL {'PASS' if report['passed'] else 'FAIL'}")


if __name__ == "__main__":
    main()
