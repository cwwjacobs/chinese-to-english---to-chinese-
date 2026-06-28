#!/usr/bin/env python3
"""
translator.py — DeepSeek CLI translation pipeline.

Reads Chinese CLI output from stdin, strips ANSI, detects operator/assistant
roles, translates to English via Google Translate (free, no API key),
caches translations deterministically, and emits tagged JSON lines to
/tmp/trans_fifo for the overlay to consume.

Usage:
    deepseek-cli 2>&1 | python3 translator.py
    deepseek-cli 2>&1 | python3 translator.py --fifo /tmp/trans_fifo

CACHE: ~/.cli-overlay/translation_cache.json
"""

import sys
import os
import re
import json
import hashlib
import argparse
from datetime import datetime, timezone
from pathlib import Path

try:
    from deep_translator import GoogleTranslator
except ImportError:
    print("pip install deep-translator", file=sys.stderr)
    sys.exit(1)

CACHE_DIR = Path.home() / ".cli-overlay"
CACHE_FILE = CACHE_DIR / "translation_cache.json"
FIFO_PATH = "/tmp/trans_fifo"

ANSI_RE = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]")
OP_PROMPT_RE = re.compile(r"^(>>>|>|>>>|Human:|User:|operator)", re.IGNORECASE)


def strip_ansi(text: str) -> str:
    return ANSI_RE.sub("", text)


def load_cache() -> dict:
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def save_cache(cache: dict) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    tmp = str(CACHE_FILE) + ".tmp"
    Path(tmp).write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, CACHE_FILE)


def cache_key(text: str, source: str, target: str) -> str:
    return hashlib.sha256(f"{source}:{target}:{text}".encode()).hexdigest()[:16]


def detect_role(line: str) -> str:
    if OP_PROMPT_RE.match(line):
        return "operator"
    return "assistant"


def translate_line(text: str, cache: dict, session_id: str) -> dict:
    if not text.strip():
        return None

    key = cache_key(text, "zh", "en")

    if key in cache:
        cached = cache[key]
        return {
            "session_id": session_id,
            "role": detect_role(text),
            "original": text,
            "translation": cached["translation"],
            "thinking": None,
            "translation_source": "cache",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    try:
        result = GoogleTranslator(source="auto", target="en").translate(text)
    except Exception as e:
        result = None
        err_msg = str(e)
    else:
        err_msg = None

    if result is None:
        return {
            "session_id": session_id,
            "role": detect_role(text),
            "original": text,
            "translation": f"[translation error: {err_msg}]",
            "thinking": None,
            "translation_error": True,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    cache[key] = {"translation": result, "original": text}
    return {
        "session_id": session_id,
        "role": detect_role(text),
        "original": text,
        "translation": result,
        "thinking": None,
        "translation_source": "google_translate",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def write_fifo(line: str, fifo_path: str) -> None:
    Path(fifo_path).parent.mkdir(parents=True, exist_ok=True)
    if not os.path.exists(fifo_path):
        os.mkfifo(fifo_path)
    with open(fifo_path, "w") as f:
        f.write(line + "\n")


def main():
    parser = argparse.ArgumentParser(description="DeepSeek CLI translation pipeline")
    parser.add_argument("--fifo", default=FIFO_PATH, help="FIFO output path")
    parser.add_argument("--no-fifo", action="store_true", help="Write to stdout only")
    args = parser.parse_args()

    session_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    cache = load_cache()
    cache_modified = False
    save_interval = 0


    def maybe_save():
        nonlocal save_interval
        save_interval += 1
        if save_interval >= 10:
            save_cache(cache)
            save_interval = 0

    for raw_line in sys.stdin:
        line = strip_ansi(raw_line.rstrip("\n\r"))

        if not line.strip():
            if not args.no_fifo:
                try:
                    write_fifo("", args.fifo)
                except OSError:
                    pass
            continue

        msg = translate_line(line, cache, session_id)
        if msg is None:
            continue

        if msg.get("translation_source") != "cache":
            cache_modified = True

        json_line = json.dumps(msg, ensure_ascii=False)
        print(json_line, flush=True)

        if not args.no_fifo:
            try:
                write_fifo(json_line, args.fifo)
            except OSError:
                pass

        maybe_save()

    if cache_modified:
        save_cache(cache)


if __name__ == "__main__":
    main()
