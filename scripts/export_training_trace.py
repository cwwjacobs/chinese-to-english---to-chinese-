#!/usr/bin/env python3
"""
export_training_trace.py — Convert state file to training-ready JSONL.

Produces ML-compatible JSONL with structured tags for fine-tuning pipelines.
Each line is a single training example with role, original, translation,
thinking, model metadata, and deterministic translation tags.

Usage:
    python3 export_training_trace.py ~/.cli-overlay/state-*.json --out trace.jsonl
"""

import json
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path


TRAINING_SCHEMA = {
    "session_id": str,
    "exchange_index": int,
    "role": str,
    "original": str,
    "translation": str,
    "thinking": (str, type(None)),
    "translation_source": str,
    "timestamp": str,
    "tags": dict,
}


def export_state(state_file: str, out_file: str):
    path = Path(state_file)
    if not path.exists():
        print(f"State file not found: {state_file}", file=sys.stderr)
        return 1

    exchanges = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if obj.get("event") in ("session_start", "session_end"):
                continue
            exchanges.append(obj)

    session_id = exchanges[0].get("session_id", path.stem) if exchanges else path.stem

    out_path = Path(out_file)
    written = 0
    with open(out_path, "w", encoding="utf-8") as out:
        for i, ex in enumerate(exchanges):
            trace = {
                "session_id": session_id,
                "exchange_index": i + 1,
                "role": ex.get("role", "assistant"),
                "original": ex.get("original", ""),
                "translation": ex.get("translation", ""),
                "thinking": ex.get("thinking"),
                "translation_source": ex.get("translation_source", "unknown"),
                "timestamp": ex.get("timestamp", ""),
                "tags": {
                    "language_pair": "zh-en",
                    "model": "cli-translation-overlay-v0.3",
                    "deterministic": ex.get("translation_source") == "cache",
                    "has_thinking": ex.get("thinking") is not None,
                },
            }
            out.write(json.dumps(trace, ensure_ascii=False) + "\n")
            written += 1

    print(f"Exported {written} training traces to {out_path}")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Export state file as training trace JSONL")
    parser.add_argument("state_file", help="Path to state JSONL file")
    parser.add_argument("--out", default=None, help="Output JSONL path")
    parser.add_argument("--dir", default=None, help="Export all state files in directory")
    args = parser.parse_args()

    if args.dir:
        state_dir = Path(args.dir)
        total = 0
        for sf in sorted(state_dir.glob("state-*.json")):
            out = sf.with_suffix(".training.jsonl")
            export_state(str(sf), str(out))
            total += 1
        print(f"Exported {total} state files from {state_dir}")
        return 0

    out = args.out or Path(args.state_file).with_suffix(".training.jsonl")
    return export_state(args.state_file, str(out))


if __name__ == "__main__":
    sys.exit(main())
