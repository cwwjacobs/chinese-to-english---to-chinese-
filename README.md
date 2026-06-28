# chinese-to-english---to-chinese-

## Real-Time CLI Translation Overlay

A borderless, always-on-top HUD overlay that translates Chinese DeepSeek CLI output to English in real time — and your English prompts back to Chinese.

Built with Python + Tkinter. Terminus Protocol theme. Deterministic translation cache. State replay. Training trace export.

### Install

```bash
git clone https://github.com/cwwjacobs/chinese-to-english---to-chinese-.git
cd chinese-to-english---to-chinese-
pip install deep-translator pillow requests
```

### Use

```bash
# Terminal 1: start the overlay
python3 overlay.py &

# Terminal 2: run DeepSeek CLI through translator
deepseek-cli 2>&1 | python3 translator.py
```

Hover near overlay bottom → type English → Enter → translated to Chinese → injected to CLI.

### Bidirectional: your English → Chinese via local DeepSeek

1. 🟢 LM Studio (`localhost:1234`) — recommended
2. 🟡 Ollama (`deepseek-r1:1.5b`) — fallback
3. 🟠 Google Translate — emergency

### Replay & training trace

```bash
python3 replay.py ~/.cli-overlay/state-*.json
python3 scripts/export_training_trace.py state.json --out trace.jsonl
```

### Theme

Terminus Protocol: hot pink `#ff6b9d` / purple `#9b59f0` / cyan `#40d8e0` / gold `#ffb347` / void `#0a0a0f`

### Validate

```bash
make validate
make test
```

### License

MIT
