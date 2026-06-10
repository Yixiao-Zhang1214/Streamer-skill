#!/usr/bin/env python3
"""Quality checks for generated streamer Skills."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REQUIRED_PROMPT_KEYS = {
    "intake",
    "work_analyzer",
    "persona_analyzer",
    "work_builder",
    "persona_builder",
    "script_generator",
    "compliance",
    "merger",
}
REQUIRED_CAPABILITIES = {"persona", "work", "script_generator", "compliance"}
REQUIRED_TOOL_KEYS = {
    "douyin_profile_parser",
    "asr_segmenter",
    "streamer_deep_metrics",
    "streamer_compliance_check",
    "streamer_script_quality_check",
    "streamer_quality_check",
}
REQUIRED_REFERENCES = {
    "references/compliance_blacklist.md",
    "references/live_script_framework.md",
    "references/script_evaluation_rubric.md",
}


def load_skill_bundle(path: Path) -> tuple[str, dict, dict]:
    """Load SKILL.md, manifest.json, and meta.json from a file or skill directory."""
    skill_dir = path if path.is_dir() else path.parent
    skill_path = path / "SKILL.md" if path.is_dir() else path
    manifest_path = skill_dir / "manifest.json"
    meta_path = skill_dir / "meta.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    return skill_path.read_text(encoding="utf-8"), manifest, meta


def read_optional(skill_dir: Path, name: str) -> str:
    """Read an optional artifact from the skill directory."""
    path = skill_dir / name
    return path.read_text(encoding="utf-8") if path.exists() else ""


def contains_any(text: str, patterns: list[str]) -> bool:
    """Return True if any regex pattern appears in text."""
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


def evaluate_skill(path: Path) -> dict:
    """Evaluate a generated streamer skill directory or SKILL.md file."""
    text, manifest, meta = load_skill_bundle(path)
    skill_dir = path if path.is_dir() else path.parent
    work_text = read_optional(skill_dir, "work.md")
    persona_text = read_optional(skill_dir, "persona.md")
    engine = meta.get("engine", {})
    prompt_bundle = engine.get("prompt_bundle", {})
    streamer_tools = engine.get("streamer_tools", {})
    references = set(engine.get("references", []))
    capabilities = set(manifest.get("capabilities", []))

    checks = {
        "character_is_streamer": (
            meta.get("character") == "streamer"
            and manifest.get("character") == "streamer"
        ),
        "required_prompt_bundle": REQUIRED_PROMPT_KEYS.issubset(prompt_bundle.keys()),
        "required_capabilities": REQUIRED_CAPABILITIES.issubset(capabilities),
        "required_streamer_tools": REQUIRED_TOOL_KEYS.issubset(streamer_tools.keys()),
        "required_references": REQUIRED_REFERENCES.issubset(references),
        "input_contract": contains_any(text, [r"Input Contract", r"输入契约", r"商品信息", r"用户画像"]),
        "selling_flow": contains_any(text, [r"Selling Flow", r"带货\s*7\s*阶段", r"留人", r"种草"]),
        "script_generator": contains_any(text, [r"Script Generator", r"话术生成器", r"teleprompter", r"直播话术"]),
        "compliance_gate": contains_any(text, [r"Compliance Gate", r"合规", r"禁用词", r"需确认"]),
        "persona_expression": contains_any(text, [r"Expression DNA", r"表达 DNA", r"口头禅", r"情绪曲线"]),
        "audience_relationship": contains_any(text, [r"Audience Relationship", r"观众关系", r"粉丝", r"用户关系"]),
        "evidence_boundaries": contains_any(text, [r"Evidence", r"证据", r"边界", r"不可推断"]),
        "deep_persona_model": contains_any(
            text,
            [r"Signature Phrases", r"思维模型", r"Thinking Models", r"Anti-Features", r"不像她"],
        ),
        "deep_work_system": contains_any(
            text,
            [r"Template Bank", r"模板库", r"自检清单", r"异议处理", r"品类迁移", r"5\s*分钟"],
        ),
        "work_depth": has_work_depth(work_text),
        "persona_depth": has_persona_depth(persona_text),
        "quantitative_metrics": has_quantitative_metrics(text, meta),
        "research_artifacts": has_research_artifacts(skill_dir),
        "copyright_safe": is_copyright_safe(text),
    }
    return {
        "passed": all(checks.values()),
        "checks": checks,
        "character": meta.get("character") or manifest.get("character"),
        "capabilities": sorted(capabilities),
        "prompt_keys": sorted(prompt_bundle.keys()),
        "streamer_tool_keys": sorted(streamer_tools.keys()),
    }


def is_copyright_safe(text: str) -> bool:
    """Reject obvious transcript-like dumps in the rendered skill."""
    if re.search(r"\b\d{2}:\d{2}:\d{2}(?:[.,]\d{1,3})?\b", text):
        return False
    long_quote_lines = [
        line for line in text.splitlines()
        if len(line) > 220 and re.search(r"[“\"].+[”\"]", line)
    ]
    return len(long_quote_lines) == 0


def count_headings(text: str, pattern: str) -> int:
    """Count markdown headings matching a pattern."""
    return len(re.findall(pattern, text, re.MULTILINE | re.IGNORECASE))


def has_work_depth(text: str) -> bool:
    """Require a research-grade work model, not a thin outline."""
    if len(text) < 7000 or text.count("\n") < 330:
        return False
    methodology_count = count_headings(text, r"^###\s+方法论\s*\d+")
    template_count = count_headings(text, r"^###\s+模板\s*\d+")
    methodology_sections = re.split(r"^###\s+方法论\s*\d+.*$", text, flags=re.MULTILINE)[1:]
    template_sections = re.split(r"^###\s+模板\s*\d+.*$", text, flags=re.MULTILINE)[1:]
    required_phrases = [
        "核心主张",
        "核心逻辑",
        "操作步骤",
        "为什么有效",
        "适用场景",
        "90 分钟",
        "自检清单",
        "反特征",
        "关键指标",
        "合规",
    ]
    complete_methodology_count = sum(
        all(phrase in section for phrase in ("核心逻辑", "操作步骤", "为什么有效", "适用场景"))
        for section in methodology_sections
    )
    complete_template_count = sum(
        ("```" in section or "示例" in section) and len(section) >= 160
        for section in template_sections
    )
    return (
        methodology_count >= 6
        and complete_methodology_count >= 6
        and template_count >= 10
        and complete_template_count >= 10
        and all(phrase in text for phrase in required_phrases)
    )


def has_persona_depth(text: str) -> bool:
    """Require a substantial persona model."""
    if len(text) < 3500 or text.count("\n") < 120:
        return False
    required_phrases = [
        "数据底座",
        "Expression DNA",
        "Signature Phrases",
        "思维模型",
        "Audience Relationship",
        "Anti-Features",
        "Evidence Boundaries",
    ]
    signature_rows = len(re.findall(r"^\|.*\|.*\|.*\|", text, re.MULTILINE))
    thinking_model_count = len(re.findall(r"^###\s*\d+\.", text, re.MULTILINE))
    return (
        all(phrase in text for phrase in required_phrases)
        and signature_rows >= 4
        and thinking_model_count >= 5
    )


def has_quantitative_metrics(text: str, meta: dict) -> bool:
    """Return whether the streamer skill carries auditable numeric ASR metrics."""
    key_metrics = meta.get("key_metrics", {})
    required_keys = {"question_mark_count", "price_anchor_count", "gift_related_count"}
    if required_keys <= key_metrics.keys() and all(key_metrics.get(key, 0) > 0 for key in required_keys):
        return True
    return contains_any(
        text,
        [
            r"问号",
            r"question_mark_count",
            r"平均句长",
            r"price_anchor",
            r"赠品.*\d+",
        ],
    )


def has_research_artifacts(skill_dir: Path) -> bool:
    """Return whether deep streamer research notes were generated."""
    raw_dir = skill_dir / "knowledge" / "research" / "raw"
    merged_summary = skill_dir / "knowledge" / "research" / "merged" / "summary.md"
    if not raw_dir.exists() or not merged_summary.exists():
        return False
    required_raw_files = [
        raw_dir / "01_public_profile_and_scope.md",
        raw_dir / "02_asr_expression_metrics.md",
        raw_dir / "03_conversion_methodology.md",
    ]
    if not all(path.exists() for path in required_raw_files):
        return False
    raw_files = [path for path in raw_dir.glob("*.md") if path.is_file()]
    if len(raw_files) < 3:
        return False
    raw_lengths = [len(path.read_text(encoding="utf-8")) for path in required_raw_files]
    summary_text = merged_summary.read_text(encoding="utf-8")
    return min(raw_lengths) >= 120 and len(summary_text) >= 240


def main() -> None:
    parser = argparse.ArgumentParser(description="Run quality checks on a generated streamer skill")
    parser.add_argument("path", help="Path to streamer skill directory or SKILL.md")
    parser.add_argument("--json", action="store_true", help="Print JSON output")
    args = parser.parse_args()

    report = evaluate_skill(Path(args.path).expanduser())
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    for name, passed in report["checks"].items():
        print(f"{'PASS' if passed else 'FAIL'}  {name}")
    print(f"OVERALL {'PASS' if report['passed'] else 'FAIL'}")


if __name__ == "__main__":
    main()
