---
name: cli-translation-overlay
description: Real-time semi-transparent English HUD overlay for Chinese DeepSeek-style CLI output. Shows translated English conversation output, supports English-to-Chinese prompt translation through LM Studio, Ollama, or Google Translate fallback, writes translated prompts to an operator FIFO, supports a FIFO bridge into CLI stdin, and includes deterministic cache, state replay, and training-trace JSONL export. Terminus Protocol theme: hot pink, purple, cyan, and gold on void black.
version: 0.3.0
---

# CLI Translation Overlay

## Operating Boundary

A borderless, always-on-top overlay that floats over a Chinese-language CLI terminal. It reads JSON messages from `/tmp/trans_fifo`, displays translated English output with role tags and optional thinking traces, and lets the operator type English prompts in a bottom entry bar.

For bidirectional use, English prompts are translated to Chinese and written to `/tmp/op_trans_fifo`. A FIFO bridge such as `tail -f /tmp/op_trans_fifo | deepseek-cli 2>&1 | python3 translator.py --fifo /tmp/trans_fifo` feeds those translated prompts into the CLI stdin while sending CLI output back through the translator.

This skill does NOT:

- Directly modify or hook the CLI process
- Replace the terminal — it floats above it
- Guarantee professional translation quality
- Require cloud API keys
- Claim production readiness without separate receipts
- Claim translated commands are safe to execute without operator review

## When to use

- "Translate DeepSeek CLI output to English in real time"
- "Build a translation HUD overlay for my Chinese terminal"
- "Use English prompts with a Chinese-language CLI through a FIFO bridge"
- "Capture AI conversation traces for training data"
- "Replay a saved CLI session"

## Quickstart

Terminal 1 — start the overlay:

```bash
make prepare-fifos
python3 overlay.py
```

Terminal 2 — run the CLI through the bidirectional FIFO bridge:

```bash
make run-deepseek
```

Equivalent command:

```bash
tail -f /tmp/op_trans_fifo | deepseek-cli 2>&1 | python3 translator.py --fifo /tmp/trans_fifo
```

Use a different CLI command with:

```bash
CLI_CMD="deepseek-cli --model deepseek-chat" make run-deepseek
```

## Output-only mode

If you only need Chinese output translated into English:

```bash
deepseek-cli 2>&1 | python3 translator.py
```

## Bidirectional Prompt Translation

Hover near the bottom of the overlay → a gold-bordered entry field appears.
Type your prompt in English → Enter → translated to Chinese → written to `/tmp/op_trans_fifo`.

Translation tiers for English → Chinese prompts:

1. LM Studio (`localhost:1234`) — recommended, local, user-controlled
2. Ollama (`localhost:11434`, `deepseek-r1:1.5b`) — local fallback
3. Google Translate via `deep-translator` — emergency fallback

Chinese → English output translation currently uses `deep-translator` with a deterministic local cache.

## State & Replay

Every session is saved to `~/.cli-overlay/state-{session-id}.json`. Replay:

```bash
python3 replay.py ~/.cli-overlay/state-*.json
python3 replay.py state.json --fast-forward
```

## Training Trace Export

Convert state files to ML-ready JSONL:

```bash
python3 scripts/export_training_trace.py ~/.cli-overlay/state-*.json --out trace.jsonl
python3 scripts/export_training_trace.py --dir ~/.cli-overlay
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
- Never claim CLI prompt injection unless the FIFO bridge is running

## Claim Boundary

PASS means no blocking issues were detected under configured checks. PASS does not mean the artifact is secure, vulnerability-free, production-ready, or safe to execute without review. Translation accuracy varies by engine. State files may contain sensitive conversation content — handle accordingly.
