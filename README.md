# CLI Translation Overlay

Real-time Chinese ⇄ English HUD overlay for DeepSeek-style terminal workflows.

This project gives an English-speaking operator a local desktop overlay for Chinese-language CLI agents:

- Chinese CLI output → English overlay display
- English operator prompt → Chinese text written to an operator FIFO
- Optional FIFO bridge → feeds translated Chinese prompts into the CLI stdin
- Deterministic translation cache
- State replay
- Training trace export
- Terminus Protocol theme

## Install

```bash
git clone https://github.com/cwwjacobs/chinese-to-english---to-chinese-.git
cd chinese-to-english---to-chinese-
pip install -r requirements.txt
```

If your Python/Tkinter build is missing on Linux, install the system Tkinter package for your distro, for example:

```bash
sudo apt install python3-tk
```

## Use: bidirectional FIFO bridge

Terminal 1 — start the overlay:

```bash
make prepare-fifos
python3 overlay.py
```

Terminal 2 — run the CLI through the bridge:

```bash
make run-deepseek
```

By default, `make run-deepseek` runs:

```bash
tail -f /tmp/op_trans_fifo | deepseek-cli 2>&1 | python3 translator.py --fifo /tmp/trans_fifo
```

The overlay reads translated output from `/tmp/trans_fifo`.
When you type English in the overlay entry bar, it translates the prompt to Chinese and writes it to `/tmp/op_trans_fifo`.
The FIFO bridge feeds that Chinese text into the CLI stdin.

Use a different CLI command with `CLI_CMD`:

```bash
CLI_CMD="deepseek-cli --model deepseek-chat" make run-deepseek
```

## Use: output-only observer mode

If you only want to translate Chinese CLI output to English and do not need the overlay to send prompts back:

```bash
deepseek-cli 2>&1 | python3 translator.py
```

## Bidirectional translation tiers

English → Chinese prompt translation falls back through:

1. LM Studio at `localhost:1234` — recommended
2. Ollama at `localhost:11434` using `deepseek-r1:1.5b`
3. Google Translate via `deep-translator` — emergency fallback

Chinese → English output translation currently uses `deep-translator` with a deterministic local cache.

## Replay and training trace

Replay a saved state file into the overlay:

```bash
python3 replay.py ~/.cli-overlay/state-*.json
python3 replay.py state.json --fast-forward
```

Export state files to JSONL:

```bash
python3 scripts/export_training_trace.py state.json --out trace.jsonl
python3 scripts/export_training_trace.py --dir ~/.cli-overlay
```

## Theme

Terminus Protocol: hot pink `#ff6b9d` / purple `#9b59f0` / cyan `#40d8e0` / gold `#ffb347` / void `#0a0a0f`.

## Validate

```bash
make validate
make test
make receipt
```

## Scope and safety boundary

This is a local desktop Python/Tkinter tool for terminal workflows. It is not a mobile app, browser extension, hosted translation service, or professional translation guarantee.

State files may contain sensitive conversation content. Review translated commands before execution.

## License

MIT
