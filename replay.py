#!/usr/bin/env python3
"""
replay.py — Replay a saved state file into the overlay.

Reads a state file and sends messages to the overlay FIFO in order.
Usage:
    python3 replay.py ~/.cli-overlay/state-20260628T120000-a1b2.json
    python3 replay.py state.json --fast-forward  # no delays
    python3 replay.py state.json --speed 2.0     # 2x speed
"""

import json
import sys
import os
import time
import argparse
from pathlib import Path

FIFO_PATH = "/tmp/trans_fifo"


def write_fifo(line: str, fifo_path: str) -> None:
    Path(fifo_path).parent.mkdir(parents=True, exist_ok=True)
    if not os.path.exists(fifo_path):
        os.mkfifo(fifo_path)
    with open(fifo_path, "w") as f:
        f.write(line + "\n")


def replay(state_file: str, fifo: str, fast_forward: bool = False, speed: float = 1.0):
    path = Path(state_file)
    if not path.exists():
        print(f"State file not found: {state_file}", file=sys.stderr)
        return 1

    messages = []
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
            messages.append(obj)

    print(f"Replaying {len(messages)} messages from {path.name}")
    delay = 0 if fast_forward else max(0.1 / speed, 0.01)

    for i, msg in enumerate(messages):
        json_line = json.dumps(msg, ensure_ascii=False)
        print(f"[{i+1}/{len(messages)}] {msg.get('role', '?')}: {msg.get('translation', '')[:80]}")
        try:
            write_fifo(json_line, fifo)
        except OSError as e:
            print(f"FIFO write error: {e}", file=sys.stderr)
        if delay:
            time.sleep(delay)

    print("Replay complete.")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Replay a saved overlay state file")
    parser.add_argument("state_file", help="Path to state JSONL file")
    parser.add_argument("--fifo", default=FIFO_PATH, help="FIFO to write to")
    parser.add_argument("--fast-forward", action="store_true", help="No delay between messages")
    parser.add_argument("--speed", type=float, default=1.0, help="Replay speed multiplier")
    args = parser.parse_args()

    return replay(args.state_file, args.fifo, args.fast_forward, args.speed)


if __name__ == "__main__":
    sys.exit(main())
