# CLI Translation Overlay — Premium HUD for DeepSeek

A borderless, always-on-top translation overlay that turns your Chinese DeepSeek
CLI into an English-readable conversation stream with zero friction.

## What It Does

- **Real-time translation** — Pipe DeepSeek CLI output through `translator.py` and
  English appears instantly in a floating HUD
- **Full conversation view** — Operator (▸ pink) and Assistant (▣ white) messages
  interleaved in order, scrollable
- **Thinking trace inspection** — Click "🧠 Show reasoning" on any assistant message
  to expand the model's hidden thinking
- **Bidirectional prompt translation** — Hover near the bottom, type English, hit
  Enter — your prompt is translated to Chinese via a local DeepSeek model and
  injected into the CLI
- **Transparency slider** — Adjust opacity from 20% to 100% so you can still see
  the Chinese terminal underneath
- **Alignment tools** — "Show Bounds" draws a pink dashed border around the overlay;
  "Snap Align" auto-positions it over your terminal
- **State replay** — Every session is saved. Replay it later or export to JSONL for
  ML fine-tuning
- **Terminus Protocol theme** — Hot pink, purple, cyan, and gold on void black.
  Premium, readable, doesn't look like a 1990s tool

## Who It Is For

- Developers working with Chinese DeepSeek CLI who want real-time English
- AI researchers capturing translation traces for training data
- Anyone who needs a clean, semi-transparent HUD over their terminal

## Requirements

- Python 3.10+
- `pip install deep-translator requests`
- For bidirectional prompts: LM Studio (recommended) or Ollama with `deepseek-r1:1.5b`

## Quickstart

```bash
# Terminal 1: start the overlay
python3 overlay.py &

# Terminal 2: run DeepSeek CLI through the translator
deepseek-cli 2>&1 | python3 translator.py
```

## Model Tiers (bidirectional prompts)

1. **LM Studio** (localhost:1234) — full control over context/temperature/reasoning
2. **Ollama** (`deepseek-r1:1.5b`) — local fallback, ~1.1 GB VRAM
3. **Google Translate** — emergency fallback, no setup needed

## Claim Boundary

PASS means no blocking issues were detected under configured checks. PASS does
not mean the artifact is secure, vulnerability-free, or safe to execute without
review. Translation accuracy varies by engine. State files may contain sensitive
conversation content — handle accordingly.
