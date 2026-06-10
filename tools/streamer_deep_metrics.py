#!/usr/bin/env python3
"""Compute deep live-commerce ASR metrics for streamer Skill generation."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


PATTERN_GROUPS = {
    "address_terms": ["宝宝", "姐妹", "宝贝", "宝子"],
    "first_person": ["我", "我们"],
    "question_rhythm": ["对不对", "是不是", "知道吧", "听懂", "明白", "懂不懂", "有没有"],
    "conversion_actions": ["拍", "下单", "链接", "去拍", "直接拍", "拍下", "加购", "付款"],
    "scarcity": ["库存", "最后", "没了", "不返场", "送完", "倒计时", "三二一", "321"],
    "price_anchor": ["价格", "到手", "券后", "块钱", "两位数", "一百", "九十九", "十二块", "多少钱"],
    "gift": ["赠品", "送", "杯子", "粉扑", "小样", "替换芯", "正装"],
    "trust": ["官方", "旗舰", "正品", "报告", "运费险", "七天", "过敏", "售后", "放心"],
    "beauty_pain": ["脱妆", "卡粉", "斑驳", "暗沉", "出油", "眼镜", "补妆", "持妆", "定妆", "粉饼"],
    "decision_simplify": ["第一个", "一号", "链接", "白加黑", "黑加黑", "色号", "选项"],
}


def count_any(text: str, words: list[str]) -> int:
    """Count all occurrences of the given phrase list."""
    return sum(text.count(word) for word in words)


def evaluate_text(text: str, source: str = "") -> dict:
    """Return deep rhythm, persuasion, and commerce metrics for ASR text."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    sentences = [segment.strip() for segment in re.split(r"[。！？!?；;\n]+", text) if segment.strip()]
    lengths = [len(sentence) for sentence in sentences]
    question_mark_count = text.count("?") + text.count("？")
    exclamation_mark_count = text.count("!") + text.count("！")
    keyword_counts = {
        word: text.count(word)
        for words in PATTERN_GROUPS.values()
        for word in words
        if text.count(word) > 0
    }

    return {
        "source": source,
        "rows": len(lines),
        "chars": len(text),
        "sentence_count": len(sentences),
        "avg_sentence_length_chars": round(sum(lengths) / len(lengths), 2) if lengths else 0,
        "median_sentence_length_chars": sorted(lengths)[len(lengths) // 2] if lengths else 0,
        "question_mark_count": question_mark_count,
        "exclamation_mark_count": exclamation_mark_count,
        "comma_count": text.count(",") + text.count("，"),
        "period_count": text.count(".") + text.count("。"),
        "question_every_chars": round(len(text) / max(1, question_mark_count), 2),
        "exclamation_every_chars": round(len(text) / max(1, exclamation_mark_count), 2),
        "pattern_counts": {
            name: count_any(text, words)
            for name, words in PATTERN_GROUPS.items()
        },
        "keyword_counts": keyword_counts,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute deep streamer ASR metrics")
    parser.add_argument("path", help="ASR text file")
    parser.add_argument("--output", help="Optional JSON output path")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    args = parser.parse_args()

    path = Path(args.path)
    report = evaluate_text(path.read_text(encoding="utf-8"), source=str(path))
    payload = json.dumps(report, ensure_ascii=False, indent=2 if args.pretty else None)
    if args.output:
        Path(args.output).write_text(payload + "\n", encoding="utf-8")
    print(payload)


if __name__ == "__main__":
    main()
