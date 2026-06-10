#!/usr/bin/env python3
"""Best-effort Douyin profile URL parser for streamer intake.

This helper intentionally avoids crawling private or protected data. It extracts
stable identifiers from a user-provided URL and leaves business-critical fields
for user confirmation.
"""

from __future__ import annotations

import argparse
from html import unescape
import json
import re
from urllib.parse import parse_qs, unquote, urlparse
from urllib.request import Request, urlopen


MAX_PUBLIC_PAGE_BYTES = 2_000_000
SAFE_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}
GENERIC_CREATOR_NAMES = {
    "抖音",
    "抖音网页版",
    "看精选视频",
    "精选视频",
    "验证码",
    "安全验证",
}


def parse_profile_url(url: str, fetch_public: bool = True, timeout: float = 8.0) -> dict:
    """Extract public, URL-level identifiers from a Douyin profile URL."""
    parsed = urlparse(url)
    path_parts = [part for part in parsed.path.split("/") if part]
    result = {
        "platform": "douyin",
        "url": url,
        "host": parsed.netloc,
        "status": "partial",
        "fields": {},
        "missing_required_fields": [
            "creator_name",
            "persona_positioning",
            "main_category",
            "price_band",
            "target_audience",
            "live_asr",
        ],
        "notes": [
            "URL-level public identifiers were parsed.",
            "Public page fetch uses plain HTTP GET only: no login, no browser automation, no anti-bot bypass.",
        ],
    }

    if len(path_parts) >= 2 and path_parts[0] == "user":
        result["fields"]["profile_id"] = path_parts[1]

    query = parse_qs(parsed.query)
    for key in ("from_tab_name", "sec_uid", "uid"):
        if query.get(key):
            result["fields"][key] = query[key][0]

    if re.search(r"(^|\.)douyin\.com$", parsed.netloc):
        result["status"] = "url_parsed"

    if fetch_public:
        public_report = fetch_public_profile(url, timeout=timeout)
        result["public_fetch"] = public_report
        if public_report["ok"]:
            result["fields"].update(public_report["fields"])
            result["status"] = "public_profile_parsed" if public_report["fields"] else "public_page_fetched"
            if public_report.get("signals", {}).get("looks_blocked") and not public_report["fields"]:
                result["notes"].append("Public page was fetched but appears to be a protected or generic page.")
            result["missing_required_fields"] = missing_required_fields(result["fields"])
        else:
            result["notes"].append(public_report["reason"])

    return result


def missing_required_fields(fields: dict) -> list[str]:
    """Return the still-missing streamer intake fields."""
    required = {
        "creator_name": ["creator_name", "nickname", "name"],
        "persona_positioning": ["persona_positioning", "signature", "bio", "description"],
        "main_category": ["main_category"],
        "price_band": ["price_band"],
        "target_audience": ["target_audience"],
        "live_asr": ["live_asr"],
    }
    missing = []
    for canonical, aliases in required.items():
        if not any(fields.get(alias) for alias in aliases):
            missing.append(canonical)
    return missing


def fetch_public_profile(url: str, timeout: float = 8.0) -> dict:
    """Fetch a public Douyin page with ordinary HTTP and parse visible metadata."""
    try:
        request = Request(url, headers=SAFE_HEADERS)
        with urlopen(request, timeout=timeout) as response:
            status_code = getattr(response, "status", None)
            content_type = response.headers.get("content-type", "")
            body = response.read(MAX_PUBLIC_PAGE_BYTES + 1)
    except Exception as exc:  # noqa: BLE001 - caller needs a graceful fallback reason.
        return {
            "ok": False,
            "reason": f"public page fetch failed: {type(exc).__name__}: {exc}",
            "fields": {},
        }

    if len(body) > MAX_PUBLIC_PAGE_BYTES:
        body = body[:MAX_PUBLIC_PAGE_BYTES]

    encoding = "utf-8"
    match = re.search(r"charset=([^;]+)", content_type, re.IGNORECASE)
    if match:
        encoding = match.group(1).strip()
    html = body.decode(encoding, errors="replace")
    target_profile_id = extract_profile_id_from_url(url)
    fields = parse_public_profile_html(html, target_profile_id=target_profile_id)
    signals = detect_public_page_signals(html)
    if fields:
        signals["looks_blocked"] = False
    return {
        "ok": True,
        "status_code": status_code,
        "content_type": content_type,
        "bytes_read": len(body),
        "fields": fields,
        "signals": signals,
    }


def parse_public_profile_html(html: str, target_profile_id: str = "") -> dict:
    """Parse public profile fields from ordinary HTML metadata and embedded JSON."""
    fields: dict[str, str] = {}
    title = extract_title(html)
    description = extract_meta_content(html, "description")
    og_title = extract_meta_content(html, "og:title")
    og_description = extract_meta_content(html, "og:description")

    if og_title or title:
        fields["creator_name"] = clean_profile_title(og_title or title)
    if og_description or description:
        fields["signature"] = clean_text(og_description or description)

    for data in extract_embedded_json_objects(html, target_profile_id=target_profile_id):
        merge_profile_fields(fields, data)

    if is_generic_creator_name(fields.get("creator_name", "")):
        fields.pop("creator_name", None)

    return {key: value for key, value in fields.items() if value not in ("", None, [], {})}


def extract_profile_id_from_url(url: str) -> str:
    """Return the Douyin profile identifier from a user URL when present."""
    parsed = urlparse(url)
    path_parts = [part for part in parsed.path.split("/") if part]
    if len(path_parts) >= 2 and path_parts[0] == "user":
        return path_parts[1]
    return ""


def extract_title(html: str) -> str:
    """Extract the document title."""
    match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    return clean_text(match.group(1)) if match else ""


def extract_meta_content(html: str, key: str) -> str:
    """Extract a meta tag by name or property."""
    pattern = (
        r"<meta[^>]+(?:name|property)=[\"']"
        + re.escape(key)
        + r"[\"'][^>]+content=[\"'](.*?)[\"'][^>]*>"
    )
    match = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
    if not match:
        pattern = (
            r"<meta[^>]+content=[\"'](.*?)[\"'][^>]+(?:name|property)=[\"']"
            + re.escape(key)
            + r"[\"'][^>]*>"
        )
        match = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
    return clean_text(match.group(1)) if match else ""


def extract_embedded_json_objects(html: str, target_profile_id: str = "") -> list[dict]:
    """Extract JSON blobs that commonly carry public profile data."""
    objects: list[dict] = []
    for match in re.finditer(
        r"<script[^>]+type=[\"']application/ld\+json[\"'][^>]*>(.*?)</script>",
        html,
        re.IGNORECASE | re.DOTALL,
    ):
        add_json_object(objects, clean_text(match.group(1)))

    render_match = re.search(
        r"<script[^>]+id=[\"']RENDER_DATA[\"'][^>]*>(.*?)</script>",
        html,
        re.IGNORECASE | re.DOTALL,
    )
    if render_match:
        add_json_object(objects, unquote(clean_text(render_match.group(1))))

    searchable_texts = [html]
    searchable_texts.extend(extract_react_flight_chunks(html))

    if target_profile_id:
        for text in searchable_texts:
            if target_profile_id not in text:
                continue
            for snippet in extract_json_like_snippets(text, target_profile_id):
                add_json_object(objects, snippet)
        if objects:
            return objects

    for text in searchable_texts:
        for marker in ("nickname", "realName", "signature", "desc", "follower", "sec_uid", "secUid"):
            if marker not in text:
                continue
            for snippet in extract_json_like_snippets(text, marker):
                add_json_object(objects, snippet)
            break
    return objects


def add_json_object(objects: list[dict], payload: str) -> None:
    """Append a parsed JSON object when possible."""
    for candidate in json_payload_candidates(payload):
        try:
            data = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(data, dict):
            objects.append(data)
            return


def json_payload_candidates(payload: str) -> list[str]:
    """Return safe decoding variants for normal and escaped JSON payloads."""
    candidates = [payload]
    decoded_url = unquote(payload)
    if decoded_url != payload:
        candidates.append(decoded_url)
    if '\\"' in payload or "\\n" in payload or "\\u" in payload:
        unescaped = payload.replace('\\"', '"').replace("\\/", "/").replace("\\n", "\n")
        candidates.append(unescaped)
    return candidates


def extract_react_flight_chunks(html: str) -> list[str]:
    """Extract public React/SSR stream chunks that may contain profile JSON."""
    chunks = []
    pattern = r"self\.__pace_f\.push\(\[1,\"((?:\\.|[^\"\\])*)\"\]\)"
    for match in re.finditer(pattern, html):
        escaped_chunk = match.group(1)
        try:
            chunks.append(json.loads(f'"{escaped_chunk}"'))
        except json.JSONDecodeError:
            chunks.append(escaped_chunk.replace('\\"', '"').replace("\\n", "\n"))
    return chunks


def extract_json_like_snippets(html: str, marker: str) -> list[str]:
    """Find small balanced JSON snippets near a marker."""
    snippets = []
    for match in re.finditer(re.escape(marker), html):
        start = html.rfind("{", 0, match.start())
        if start < 0:
            continue
        end = find_matching_brace(html, start)
        if end > start:
            snippets.append(html[start:end + 1])
    return snippets[:5]


def find_matching_brace(text: str, start: int) -> int:
    """Find the closing brace for a JSON-like object."""
    depth = 0
    in_string = False
    escape = False
    quote = ""
    for index in range(start, min(len(text), start + 200_000)):
        char = text[index]
        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == quote:
                in_string = False
            continue
        if char in ('"', "'"):
            in_string = True
            quote = char
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return index
    return -1


def merge_profile_fields(fields: dict, data: dict) -> None:
    """Recursively merge profile-like keys from embedded public JSON."""
    stack = [data]
    while stack:
        item = stack.pop()
        if isinstance(item, dict):
            capture_profile_keys(fields, item)
            stack.extend(value for value in item.values() if isinstance(value, (dict, list)))
        elif isinstance(item, list):
            stack.extend(value for value in item if isinstance(value, (dict, list)))


def capture_profile_keys(fields: dict, item: dict) -> None:
    """Capture known public profile keys from a JSON object."""
    looks_like_profile = any(
        key in item for key in ("nickname", "realName", "uid", "secUid", "sec_uid", "uniqueId", "shortId")
    )
    key_map = {
        "nickname": "creator_name",
            "realName": "creator_name",
        "uniqueId": "douyin_id",
        "shortId": "douyin_id",
            "uid": "uid",
        "secUid": "sec_uid",
        "sec_uid": "sec_uid",
        "signature": "signature",
        "description": "signature",
        "followerCount": "follower_count",
        "followers": "follower_count",
            "mplatformFollowersCount": "mplatform_follower_count",
        "followingCount": "following_count",
        "awemeCount": "video_count",
        "favoritingCount": "liked_count",
        "totalFavorited": "liked_count",
    }
    for source_key, target_key in key_map.items():
        if source_key in item and item[source_key] not in ("", None, [], {}):
            value = clean_text(str(item[source_key]))
            if target_key == "creator_name" and is_generic_creator_name(value):
                continue
            if target_key == "creator_name" and is_generic_creator_name(fields.get(target_key, "")):
                fields[target_key] = value
            else:
                fields.setdefault(target_key, value)
    if looks_like_profile and item.get("desc") not in ("", None, [], {}):
        fields.setdefault("signature", clean_text(str(item["desc"])))
    if item.get("name") not in ("", None, [], {}) and (
        looks_like_profile or str(item.get("@type", "")).lower() in {"person", "organization"}
    ):
        value = clean_text(str(item["name"]))
        if not is_generic_creator_name(value):
            fields.setdefault("creator_name", value)
    if item.get("mplatformFollowersCount") not in ("", None, [], {}):
        fields["account_follower_count"] = clean_text(str(item.get("followerCount", "")))
        fields["follower_count"] = clean_text(str(item["mplatformFollowersCount"]))
        fields["follower_count_source"] = "mplatformFollowersCount"


def clean_profile_title(title: str) -> str:
    """Clean a Douyin title into a likely creator name."""
    title = clean_text(title)
    title = re.sub(r"[-_｜|].*$", "", title).strip()
    title = re.sub(r"的抖音.*$", "", title).strip()
    return title


def is_generic_creator_name(name: str) -> bool:
    """Return whether the parsed name is a platform-level generic label."""
    normalized = clean_text(name)
    return normalized in GENERIC_CREATOR_NAMES or bool(re.search(r"(验证码|安全验证|精选视频)$", normalized))


def clean_text(text: str) -> str:
    """Normalize whitespace and HTML entities."""
    text = re.sub(r"<[^>]+>", "", text)
    text = unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def detect_public_page_signals(html: str) -> dict:
    """Return diagnostics that explain whether the public page was readable."""
    lowered = html.lower()
    return {
        "has_title": bool(re.search(r"<title[^>]*>.*?</title>", html, re.IGNORECASE | re.DOTALL)),
        "has_description": "description" in lowered,
        "has_render_data": "render_data" in lowered,
        "has_json_ld": "application/ld+json" in lowered,
        "looks_blocked": any(marker in html for marker in ("风控", "验证码", "安全验证", "访问过于频繁")),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse a Douyin profile URL for streamer intake")
    parser.add_argument("url", help="Douyin creator profile URL")
    parser.add_argument(
        "--no-fetch",
        action="store_true",
        help="Skip ordinary public-page HTTP fetch and only parse URL-level identifiers",
    )
    parser.add_argument("--timeout", type=float, default=8.0, help="HTTP timeout for public-page fetch")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    args = parser.parse_args()

    print(
        json.dumps(
            parse_profile_url(args.url, fetch_public=not args.no_fetch, timeout=args.timeout),
            ensure_ascii=False,
            indent=2 if args.pretty else None,
        )
    )


if __name__ == "__main__":
    main()
