#!/usr/bin/env python3
"""Segment live-commerce ASR into coarse selling-flow stages."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


STAGE_KEYWORDS = {
    "retention_opening": ["欢迎", "新进", "停留", "关注", "预约", "福利", "宝宝", "宝子"],
    "product_seeding": ["痛点", "适合", "卖点", "设计", "面料", "材质", "显瘦", "舒服"],
    "trust_building": ["放心", "实拍", "试穿", "工厂", "品质", "质检", "退换", "保障"],
    "price_dramatization": ["原价", "到手", "券", "补贴", "福利价", "今天", "划算"],
    "conversion_push": ["链接", "小黄车", "拍", "下单", "库存", "倒计时", "抢"],
    "holding_transition": ["等一下", "马上", "下一款", "过款", "补货", "别走"],
    "interaction_objection": ["尺码", "多高", "多重", "会不会", "能不能", "怎么选", "扣"],
}

SIGNAL_PATTERNS = {
    "link": [
        r"(?:一|二|三|四|五|六|七|八|九|十|\d+)\s*号?链接",
        r"链接\s*(?:一|二|三|四|五|六|七|八|九|十|\d+)",
        r"小黄车",
    ],
    "price": [
        r"\d+(?:\.\d+)?\s*元",
        r"\d+(?:\.\d+)?\s*块(?:钱)?",
        r"[一二三四五六七八九十百千两]+(?:块|块钱|毛)",
        r"[¥￥]\s*\d+(?:\.\d+)?",
        r"到手价",
        r"券后",
        r"福利价",
    ],
    "size": [
        r"[XSML]{1,3}",
        r"\d+\s*XL",
        r"[一二三四五六七八九十]\s*码",
        r"尺码",
        r"身高",
        r"体重",
    ],
    "stock": [
        r"库存",
        r"限量",
        r"补货",
        r"最后\s*\d*",
        r"没了",
    ],
    "sku_transition": [
        r"下一款",
        r"过款",
        r"换款",
        r"这款",
        r"这一套",
    ],
}


def split_sentences(text: str) -> list[str]:
    """Split ASR text into small speakable units."""
    candidates = re.split(r"(?<=[。！？!?；;])|\n+", text)
    return [item.strip() for item in candidates if item.strip()]


def score_sentence(sentence: str) -> dict[str, int]:
    """Score a sentence against every live-commerce stage."""
    return {
        stage: sum(sentence.count(keyword) for keyword in keywords)
        for stage, keywords in STAGE_KEYWORDS.items()
    }


def classify_sentence(sentence: str) -> str:
    """Return the most likely live-commerce stage for a sentence."""
    scores = score_sentence(sentence)
    best_stage, best_score = max(scores.items(), key=lambda item: item[1])
    return best_stage if best_score > 0 else "unclassified"


def extract_signals(sentence: str) -> dict[str, list[str]]:
    """Extract SKU, link, price, size, and stock signals from a sentence."""
    signals = {}
    for signal_name, regexes in SIGNAL_PATTERNS.items():
        matches = []
        for regex in regexes:
            matches.extend(match.group(0) for match in re.finditer(regex, sentence, re.IGNORECASE))
        if matches:
            signals[signal_name] = sorted(set(matches), key=matches.index)
    return signals


def build_stage_summary(records: list[dict]) -> dict:
    """Summarize stage and signal coverage for downstream analyzers."""
    stage_counts = {stage: 0 for stage in [*STAGE_KEYWORDS, "unclassified"]}
    signal_counts = {signal: 0 for signal in SIGNAL_PATTERNS}
    stage_signals = {stage: {signal: 0 for signal in SIGNAL_PATTERNS} for stage in stage_counts}

    for record in records:
        stage = record["stage"]
        stage_counts[stage] += 1
        for signal in record["signals"]:
            signal_counts[signal] += 1
            stage_signals[stage][signal] += 1

    return {
        "stage_counts": stage_counts,
        "signal_counts": signal_counts,
        "stage_signals": stage_signals,
    }


def classify_sentence_with_scores(sentence: str) -> tuple[str, dict[str, int]]:
    """Return the most likely stage and raw stage scores."""
    scores = {
        stage: sum(sentence.count(keyword) for keyword in keywords)
        for stage, keywords in STAGE_KEYWORDS.items()
    }
    best_stage, best_score = max(scores.items(), key=lambda item: item[1])
    return (best_stage if best_score > 0 else "unclassified"), scores


def segment_text(text: str) -> dict:
    """Segment text into stage buckets with counts and representative snippets."""
    buckets: dict[str, list[str]] = {stage: [] for stage in STAGE_KEYWORDS}
    buckets["unclassified"] = []
    records = []

    for sentence in split_sentences(text):
        stage, scores = classify_sentence_with_scores(sentence)
        signals = extract_signals(sentence)
        buckets[stage].append(sentence)
        records.append(
            {
                "text": sentence,
                "stage": stage,
                "scores": scores,
                "signals": signals,
            }
        )

    summary = build_stage_summary(records)
    return {
        **summary,
        "snippets": {stage: items[:10] for stage, items in buckets.items() if items},
        "records": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Segment live-commerce ASR by selling-flow stage")
    parser.add_argument("input", help="Plain-text ASR file")
    parser.add_argument("--output", help="Optional JSON output file")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    args = parser.parse_args()

    result = segment_text(Path(args.input).read_text(encoding="utf-8"))
    payload = json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None)

    if args.output:
        Path(args.output).write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)


if __name__ == "__main__":
    main()
