---
name: cli-translation-overlay
description: Real-time semi-transparent English HUD overlay for Chinese DeepSeek CLI output. Full conversation view with operator/assistant roles, collapsible thinking traces, bidirectional prompt translation via local DeepSeek model (LM Studio / Ollama), state replay, and training-trace JSONL export. Terminus Protocol theme (hot pink, purple, cyan, gold on void black). Use when translating Chinese CLI output to English in real time, capturing AI conversation traces for training, or building a replayable translation layer over any Chinese-language terminal.
version: 0.3.0
---

# CLI Translation Overlay

## Operating Boundary

A borderless, always-on-top overlay that floats over a DeepSeek CLI terminal. It reads Chinese output, translates to English in real time, and displays the full conversation with role tags and expandable thinking traces. The overlay also supports bidirectional prompt translation: type English prompts in a bottom entry bar and they are translated to Chinese via a local DeepSeek model before being injected into the CLI.

This skill does NOT:
- Modify or interfere with the CLI process
- Replace the terminal — it floats above it
- Require cloud API keys (defaults to free Google Translate; local LM Studio or Ollama recommended for prompts)
- Claim production readiness without separate receipts

## When to use

- "Translate DeepSeek CLI output to English in real time"
- "Build a translation HUD overlay for my Chinese terminal"
- "Capture AI conversation traces for training data"
- "Replay a saved CLI session"
- "Type English prompts and have them translated to Chinese before hitting the CLI"

## Quickstart

```bash
# 1. Start the overlay
python3 overlay.py &

# 2. Pipe CLI output through the translator
deepseek-cli 2>&1 | python3 translator.py
```

The overlay reads from `/tmp/trans_fifo`. The translator writes JSON lines to that FIFO.

## Bidirectional Prompt Translation

Hover near the bottom of the overlay → a gold-bordered entry field appears.
Type your prompt in English → Enter → translated to Chinese via local model.

Model tiers (auto-fallback):
1. LM Studio (localhost:1234) — recommended, full control over context/temperature
2. Ollama (deepseek-r1:1.5b) — local fallback
3. Google Translate — emergency fallback

## State & Replay

Every session is saved to `~/.cli-overlay/state-{session-id}.json`. Replay:

```bash
python3 replay.py ~/.cli-overlay/state-*.json
python3 replay.py state.json --fast-forward  # instant replay
```

## Training Trace Export

Convert state files to ML-ready JSONL:

```bash
python3 scripts/export_training_trace.py ~/.cli-overlay/state-*.json --out trace.jsonl
```

## Theme

Terminus Protocol: hot pink `#ff6b9d` / purple `#9b59f0` / cyan `#40d8e0` / gold `#ffb347` / void `#0a0a0f`.

## Validation

```bash
make validate
make test
make receipt
```

## Never Do

- Never claim translation quality matches a professional human translator
- Never store API keys in the codebase
- Never claim regulatory compliance for translated output
- Never overwrite state files — always append
- Never silently drop translation errors

## Claim Boundary

PASS means no blocking issues were detected under configured checks. PASS does not mean the artifact is secure, vulnerability-free, or safe to execute without review. Translation accuracy varies by engine. State files may contain sensitive conversation content — handle accordingly.
