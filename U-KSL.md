# U-KSL: Real-Time CLI Translation Overlay

**Canon v0.3** — Based on U-KSL Core Canon v0.3 (Terminus Protocol)  
**Token-optimize**: concision, no re-reads, batch calls, no fluff  
**Flight Recorder**: state save/replay, training trace tagging, thinking trace capture  
**Bidirectional**: English prompts → Chinese via local DeepSeek R1 1.5B (LM Studio primary, Ollama fallback)  
**Theme**: Terminus Protocol — hot pink `#ff6b9d` / purple `#9b59f0` / cyan `#40d8e0` / gold `#ffb347` / void `#0a0a0f`  
**UI**: HUD mode — semi-transparent overlay on terminal, bottom Entry for prompt input

---

## 0. Core Claim

U-KSL converts the **Ultra Goal** of "transparent real-time English overlay for Chinese CLI with full conversation replay, thinking trace inspection, and training-trace export" into a bounded, verified **Structure** through Phase-mapped Infra Objectives, receipted Intra work, and recursive healing.

```
Stage 1 maps.
Stage 2 traverses.
Stage 3 verifies.
This repeats at every level.
```

---

## 1. Ultra

**Goal:** A lightweight, always-on-top overlay window that shows the **full conversation** (Operator + Assistant exchanges in order) from a Chinese-language DeepSeek CLI session. Requirements:
- **Scrollable** — when output gets long, it scrolls cleanly (no weird wrapping)
- **Deterministic overlay** — accurately, honestly translate every message; same input always same output
- **State save at every start** — replayable state snapshot (`~/.cli-overlay/state-{session-id}.json`) so the session can be replayed later. We learned this the hard way — it saved the last build.
- **Thinking traces** — model reasoning captured in collapsible dropdowns per assistant message
- **Training trace tagging** — structured schema-defined tags so the trace can be used as training data or sold as a training trace product
- **Charts/graphs** — if the conversation produces a structure summary, table, or chart, populate it visually in the overlay
- Adjustable transparency (0–100% slider), alignment verification (red dashed bounding box), auto-snap to terminal

**As Structure:** A deliverable Python package with:
- `cli-translation-overlay/` — runnable application
- `state/` — replayable session state directory
- `SKILL.md` — Agensi-listed agent skill
- Training-trace schema (JSONL-ready for ML fine-tuning pipelines)
- Deterministic scripts, receipts, and claim boundaries (Premium Skill Builder format)

**May not be contradicted:**
- The overlay must never obscure the underlying terminal completely.
- The overlay must never modify or interfere with the CLI process.
- **State must be saved at every start** — a file `~/.cli-overlay/state-{session-id}.json` that can replay the entire session.
- Translation must be **deterministic** — same Chinese input always same English output. Cache results so replay is identical.
- Training trace tags must be **structured, not freeform** — schema-defined fields.
- Thinking traces must be captured and stored separately — viewable on demand, not inline.

**Lifecycle:**
```
Ultra Goal
→ mapped Infra (5 lanes)
→ built Intra work (phases/steps/loops)
→ verified coherence (receipts)
→ Ultra Structure (delivered package)
```

---

## 2. Ultra Stage 1: Surface, Bound, Map, Lock

### 1. Ultra Goal
Real-time semi-transparent English translation overlay for DeepSeek Chinese CLI.

### 2. Scope
- Borderless overlay window reading from a named pipe (FIFO)
- Translation pipeline: `deepseek-cli 2>&1 | python3 translator.py > /tmp/trans_fifo`
- **Full conversation view**: Operator (Chinese) + Assistant (English translated) in order, scrollable
- **Thinking trace collapsible**: per assistant message, a dropdown that reveals the model's reasoning
- **State save/replay**: on every start, save `~/.cli-overlay/state-{session-id}.json`; replay from file
- **Training trace schema**: structured JSONL output with tags (role, content, translation, thinking, timestamp, session_id)
- **Chart/graph population**: if the structure summary or U-KSL contains a table/flow, render it
- Tkinter-based GUI (cross-platform, no external dependencies beyond deep-translator)
- Opacity slider (0.2–1.0)
- "Show Bounds" red dashed border toggle for alignment verification
- Auto-snap to terminal window (Linux via `xdotool`; Windows via `win32gui`)
- Drag-to-move via handle
- Config persistence (`~/.cli-overlay.json`)

### 3. Exclusions
- NOT an OCR overlay (reads piped text, not screen pixels)
- NOT a full terminal emulator
- NOT a translation service with API keys (defaults to Google Translate via deep-translator)
- NOT a macOS auto-snap (manual alignment only — PyObjC is heavy)

### 4. Infra Objectives

| Lane | Name | Description |
|------|------|-------------|
| I1 | **Translation Pipeline** | Pipe CLI output, translate, emit to FIFO; deterministic translation cache |
| I2 | **Overlay Window** | Borderless Tkinter window, FIFO reader, **scrollable full conversation** (Operator + Assistant), **thinking trace collapsible dropdowns**, **Terminus theme**, chart/graph rendering |
| I3 | **Hover Toolbar** | Opacity slider + Align button + Show Bounds toggle + close; Terminus-styled |
| I4 | **Alignment & Snap** | Manual bounds check + auto-snap to terminal |
| I5 | **State & Replay** | Save state at every start (`~/.cli-overlay/state-{session-id}.json`); replay from file; training-trace JSONL export |
| I6 | **Config & Packaging** | Config persistence, Makefile, SKILL.md, storefront, Agensi listing |
| **I7** | **Bidirectional Prompt Translation** | Operator English prompt → Chinese via local DeepSeek R1 (LM Studio primary, Ollama fallback, Google Translate emergency); translated prompt injected into CLI pipeline |

### 5. Composition requirements
- I1 feeds I2 via `/tmp/trans_fifo`
- I3 overlays on I2 (same Tkinter root)
- I4 queries system windows and commands I2 to resize/reposition
- I5 reads state from `~/.cli-overlay/state-*.json` and writes replay + training trace
- I7 reads operator input from I2 Entry → translates → writes Chinese to `/tmp/op_trans_fifo` → CLI pipeline reads via stdin bridge
- I6 wraps all lanes into a deliverable package

### 6. Dependencies
- Python 3.10+
- `deep-translator` (PyPI)
- Tkinter (standard library)
- Linux: `xdotool`, `wmctrl` (system packages)
- Windows: `pywin32` (optional, for auto-snap)
- **LM Studio** (recommended for I7) or **Ollama** with `deepseek-r1:1.5b` (fallback)
- `requests` (PyPI, for LM Studio API calls)

### 7. Parallel permissions
- I1 and I2 can be built in parallel (pipeline → FIFO → overlay are decoupled)
- I3 depends on I2 (toolbar is inside the overlay)
- I4 depends on I2 (must have a window to snap)
- I5 depends on I2 (needs the conversation feed to save state)
- I7 depends on I2 (Entry widget is part of overlay) and depends on local model being available
- I6 wraps everything

### 8. Phases

| Phase | Description |
|-------|-------------|
| P1 | Core pipeline + basic overlay (I1 + I2 MVP) |
| P2 | Toolbar + interactions (I3) |
| P3 | Alignment + auto-snap (I4) |
| P4 | State & replay + training trace export (I5) |
| P5 | Bidirectional prompt translation (I7) |
| P6 | Config + packaging + SKILL.md + Agensi listing (I6) |

### 9. Steps (mapped per Phase — see Infra Stage 1 below)

### 10. Exit conditions
- Overlay starts and displays translated text from a live CLI
- **Full conversation visible**: Operator (Chinese) and Assistant (English translated) in order, scrollable
- **Thinking trace accessible**: collapsible dropdown per assistant message
- **State saved on start**: `~/.cli-overlay/state-{session-id}.json` written and replayable
- **Training trace export**: JSONL file with structured tags
- Opacity slider changes transparency in real time
- "Show Bounds" draws a red dashed border
- Auto-snap positions overlay over the terminal window
- Config persists and restores on relaunch
- SKILL.md passes all Premium Skill Builder validation checks

### 11. Receipt requirements
- `final_receipt.json` with checks_run, checks_not_run, allowed claims, blocked claims
- Emitted by `make receipt`

### 12. Verification expectations
- All unit tests pass
- Manual smoke test: open DeepSeek CLI, start overlay, verify translation appears
- Claim-boundary wording present in all public docs

### 13. Signal-routing rules
- If translation fails (API error) → show warning icon, preserve last lines, cache failure so replay doesn't re-hit API
- If FIFO breaks → show "disconnected" state, retry every 3s
- If auto-snap finds no terminal → show manual instruction, fall back to drag
- If config file is corrupt → reset to defaults, log warning
- **If state file already exists on start** → append to existing session, do not overwrite (multi-session replay)
- **If thinking trace is too long** → truncate at 5000 chars per message in overlay; full version stored in state file

### 14. Traversal lock
**No sufficiently mapped route, no Stage 2.**
Stage 2 begins only after Ultra Stage 1 is locked (this document exists and is accepted).

---

## 3. Ultra Stage 2: Traverse the Ultra Route

Ultra Stage 2 coordinates the execution of all 7 Infra Objectives through the 6 mapped Phases.

```
Phase P1: Core pipeline + basic overlay
  → I1: Translation Pipeline (build translator.py with deterministic cache)
  → I2: Overlay Window MVP (scrollable conversation view, FIFO reader, Terminus theme)

Phase P2: Toolbar + interactions
  → I3: Hover Toolbar (opacity slider, show bounds toggle, close, drag handle)

Phase P3: Alignment + snap
  → I4: Alignment & Snap (auto-snap + manual bounds verification)

Phase P4: State & replay + training trace
  → I5: State & Replay (state save at start, replay loader, training-trace JSONL export)

Phase P5: Bidirectional prompt translation
  → I7: Bidirectional Prompt Translation (Entry widget, LM Studio/Ollama/Google Translate tiered pipeline)

Phase P6: Config + packaging
  → I6: Config & Packaging (Makefile, SKILL.md, storefront, agents, receipts)
```

**Rules:**
- May execute only what Ultra Stage 1 has mapped.
- If traversal reveals that the Ultra route itself is broken, pause affected traversal, receipt the signal, preserve valid work, and return to Ultra Stage 1.

---

## 4. Ultra's Infra

### Infra Objective I1: Translation Pipeline

**Stage 1 (Map):**
- Pipe: `deepseek-cli 2>&1 | python3 translator.py > /tmp/trans_fifo`
- Script reads stdin line-by-line, strips ANSI, translates via deep_translator.GoogleTranslator
- **Deterministic cache**: key = (input_text, source_lang, target_lang) → always same output
- Cache file: `~/.cli-overlay/translation_cache.json` — JSON dict, append-only
- Output format (to FIFO): tagged JSON lines so the overlay can distinguish messages
  ```json
  {"role": "operator", "original": "你好", "translation": "Hello", "thinking": null, "timestamp": "...", "session_id": "..."}
  {"role": "assistant", "original": "...", "translation": "...", "thinking": "I need to...", "timestamp": "...", "session_id": "..."}
  ```
- Exit: script starts, reads, translates, writes

**Stage 2 (Traverse):**
- Loop: read line → detect role (operator prompt vs assistant response) → strip ANSI → check cache → translate if miss → write JSON line to FIFO
- Skip empty lines (preserve as empty for layout)
- On API error: write JSON with `"translation_error": true` to FIFO, continue
- Cache hit: emit instantly without API call

**Stage 3 (Verify):**
- Does the script parse? (compile check)
- Does it produce output when fed a test string?
- Are empty lines preserved?
- Are ANSI codes stripped?
- **Does cache return same result on second call?** (determinism test)

### Infra Objective I2: Overlay Window (Full Conversation)

**Stage 1 (Map):**
- Tkinter root: `overrideredirect(True)`, `attributes('-topmost', True)`
- **Scrollable full conversation**: `tk.Text` widget with scrollbar — Operator (Chinese, left-aligned) and Assistant (English translation, indented) interleaved in order
- **Thinking trace collapsible**: per Assistant message, a clickable "🧠 Show reasoning" tag. Click → expand inline thinking block. Click again → collapse. Thinking text stored in message data, rendered conditionally.
- **Chart/graph support**: if the translator emits a structured block, render as Canvas or ASCII in monospace
- Monospace font, dark background, disabled editing
- Background thread reading from `/tmp/trans_fifo`, parsing JSON lines
- Max 200 messages scrollable (no weird wrapping — deterministic word wrap at window width)
- Auto-scroll to bottom on new message
- Initial alpha: 0.8

**Stage 2 (Traverse):**
- Window creation → FIFO open → JSON parse loop → append message with role formatting + thinking toggles → auto-scroll
- On FIFO disconnect: show "⏳ Waiting for translation feed..." retry every 3s
- On thinking trace present: append message, then insert "🧠 Show reasoning" tag with expand/collapse binding

**Stage 3 (Verify):**
- Does the window appear borderless and on top?
- Does the conversation show Operator + Assistant in correct order?
- Is it scrollable without wrapping weirdly?
- Does the thinking dropdown expand/collapse?
- Does text appear when JSON data is written to FIFO?
- Test: `echo '{"role":"operator","original":"你好","translation":"Hello"}' > /tmp/trans_fifo`

### Infra Objective I3: Hover Toolbar

**Stage 1 (Map):**
- Thin frame at top of overlay, hidden by default
- `<Enter>` on overlay → show toolbar, `<Leave>` → hide (with 500ms delay to avoid flicker)
- Contains: opacity Slider (0.2–1.0), "Show Bounds" toggle button, drag handle "≡", close button "×"

**Stage 2 (Traverse):**
- Hover enter → toolbar fade in
- Slider → `root.attributes('-alpha', value)`
- "Show Bounds" → draw/remove red dashed canvas rectangle
- Drag handle → bind `<Button-1>` + `<B1-Motion>`
- Close → `root.destroy()`

**Stage 3 (Verify):**
- Does toolbar appear on hover?
- Does slider change opacity in real time?
- Does "Show Bounds" draw/remove red border?
- Does drag work?
- Does close exit cleanly?

### Infra Objective I4: Alignment & Snap

**Stage 1 (Map):**
- "Show Bounds": 2px red dashed rectangle over the whole overlay
- Auto-snap: `subprocess.run(['xdotool', 'search', '--name', 'deepseek'])` (Linux)
  → get geometry → `root.geometry(f'{w}x{h}+{x}+{y}')`
- Windows fallback: `pywin32` `EnumWindows` → `GetWindowRect`
- macOS: manual only, documented instruction
- Save last position to config

**Stage 2 (Traverse):**
- Click "Snap Align" → find terminal → resize overlay → show bounds for 2s → auto-hide
- Manual drag via handle for fine-tuning

**Stage 3 (Verify):**
- Does "Show Bounds" render correctly?
- Does auto-snap find the terminal?
- Does the overlay match terminal dimensions?
- Is config saved and restored?

### Infra Objective I5: State & Replay + Training Trace

**Stage 1 (Map):**
- **State file**: `~/.cli-overlay/state-{session-id}.json`
  - Session ID: `{date}T{time}-{random-suffix}`
  - Written on every overlay start (append to existing)
  - Contains: full ordered message list, translation cache keys used, thinking traces, timestamps, training tags
- **Training trace schema** (JSONL-ready):
  ```json
  {
    "session_id": "2026-06-28T12-00-00-a1b2",
    "exchange_index": 1,
    "role": "operator" | "assistant",
    "original": "你好",
    "translation": "Hello",
    "thinking": null | "I need to...",
    "model": "deepseek-v4-flash",
    "tags": {
      "translation_source": "google_translate" | "cache",
      "language_pair": "zh→en",
      "deterministic": true
    },
    "timestamp": "2026-06-28T12:00:01Z"
  }
  ```
- **Replay spine**: `replay.py` reads a state file and re-sends each message to the overlay in order, with same timing or fast-forward mode
- **Training trace export**: `export_training_trace.py` converts state file → JSONL for ML fine-tuning pipelines
- State dir: `~/.cli-overlay/` with archive subdirectory

**Stage 2 (Traverse):**
- On overlay start:
  1. Generate session ID
  2. Open or create state file
  3. Write header with session metadata
  4. Start FIFO reader; for each message, write JSON line to both state file and training trace
- On overlay close:
  1. Write session end marker with message count, duration, token estimate
- Training trace export: run `python3 scripts/export_training_trace.py --state ~/.cli-overlay/state-*.json --out training_trace.jsonl`

**Stage 3 (Verify):**
- Does state file exist after overlay start?
- Does state file contain all messages in order?
- Does replay.py reproduce the session?
- Does training trace export produce valid JSONL?

### Infra Objective I6: Config & Packaging

**Stage 1 (Map):**
- Config file: `~/.cli-overlay/config.json` (position, opacity, fifo_path, window_width, window_height)
- Save on close, load on start
- Makefile: clean, validate, test, package, public-docs-check, handoff, sku, receipt
- SKILL.md: following Premium Skill Builder format exactly
- Storefront: short-description, long-description, faq, buyer-message
- Agents config: `cli-translation-overlay.yaml`

**Stage 2 (Traverse):**
- First launch → create default config with sensible defaults
- Subsequent → restore state from config file
- `make validate` → all scripts parse, references exist
- `make receipt` → `final_receipt.json`

**Stage 3 (Verify):**
- Does config persist across restarts?
- Does corrupt config fall back to defaults?
- Does `make validate` pass?
- Does SKILL.md have required frontmatter + claim boundary?

### Infra Objective I7: Bidirectional Prompt Translation

**Stage 1 (Map):**
- **Entry widget**: `tk.Entry` at bottom of overlay, gold `#ffb347` border, hidden until mouse approaches bottom 50px
- **Translation model tiers**:
  1. LM Studio (`localhost:1234/v1/chat/completions`) — user controls context/temperature/reasoning
  2. Ollama (`deepseek-r1:1.5b`) — local fallback
  3. Google Translate (`deep_translator`) — emergency fallback
- **Translation prompt**: `"Translate this to natural Chinese. Output ONLY the Chinese translation, no explanation:\n\n{text}"`
- **Pipeline**: Entry → translate → write Chinese to `/tmp/op_trans_fifo` → CLI stdin bridge reads and injects
- **Display**: translated prompt shown in conversation as operator message with English original + Chinese translation
- Warmup: send empty prompt to model at overlay startup to pre-warm connection
- Timeout: 15s per translation, fall back to next tier on failure

**Stage 2 (Traverse):**
- Mouse near overlay bottom → Entry fades in (gold border)
- Operator types English prompt → Enter or "→" button
- Prompt sent to LM Studio (primary), Ollama (fallback), Google Translate (emergency)
- Result trimmed to Chinese text only
- Chinese written to `/tmp/op_trans_fifo` and displayed in conversation
- Entry clears, fades out after 3s idle

**Stage 3 (Verify):**
- Does "Hello, how are you?" → model → "你好，你怎么样？"
- Does tier fallback work? (kill LM Studio → verify Ollama picks up → verify Google Translate picks up)
- Is translated prompt injected into CLI pipeline correctly?
- Does Entry fade in/out?

---

## 5. Intra (Block-Laying Detail)

### Theme Application (applied across I2 + I3)

```
Theme Step T.1: Terminus color palette
  Loop T.1.1: Set root['bg'] = '#0a0a0f' (void black)
    → Receipt: window background is void
  Loop T.1.2: Set text widget fg = '#e8e6e3' (chrome white), insertbackground = '#ffb347'
    → Receipt: readable text on dark background

Theme Step T.2: Role tags
  Loop T.2.1: Operator messages prefixed with "▸" in fg='#ff6b9d' (hot pink)
    → Receipt: operator messages visually distinct
  Loop T.2.2: Assistant messages prefixed with "▣" in fg='#9b59f0' (purple)
    → Receipt: assistant messages visually distinct

Theme Step T.3: Thinking toggle
  Loop T.3.1: "🧠 Show reasoning" tag in fg='#40d8e0' (cyan), clickable
    → Receipt: thinking toggle visible and interactive

Theme Step T.4: Toolbar styling
  Loop T.4.1: Toolbar frame bg='#1a0f2e' (deep purple), border highlight='#ff6b9d'
  Loop T.4.2: Drag handle "≡" in fg='#ffb347' (gold)
  Loop T.4.3: Close button "×" in fg='#ff6b9d' (hot pink)
    → Receipt: toolbar matches Terminus aesthetic

Theme Step T.5: Entry widget (I7 input)
  Loop T.5.1: tk.Entry bg='#111118', fg='#e8e6e3', insertbackground='#ffb347', highlightcolor='#ffb347'
    → Receipt: gold-cursor entry field on dark surface
```

### I1 Intra: Translation Pipeline

```
Step 1.1: Build translator.py with cache
  Loop 1.1.1: Write stdin reader with ANSI strip regex
    → Receipt: script compiles
  Loop 1.1.2: Integrate deep_translator.GoogleTranslator
    → Receipt: translates "你好" → "Hello"
  Loop 1.1.3: Add deterministic cache: JSON dict keyed by (input, source, target)
    → Receipt: same input twice → same output, no API call on second
  Loop 1.1.4: Add JSON line output: {"role","original","translation","thinking","timestamp","session_id"}
    → Receipt: output is valid JSON per line
  Loop 1.1.5: Add error handling (API down, rate limit)
    → Receipt: error message format confirmed, cache not poisoned by errors
  Loop 1.1.6: Write to /tmp/trans_fifo (create if not exists)
    → Receipt: FIFO write confirmed

Step 1.2: Test pipeline
  Loop 1.2.1: echo "测试" | python3 translator.py
    → Receipt: valid JSON line in stdout
  Loop 1.2.2: Test with ANSI codes: echo -e "\033[31m红色\033[0m"
    → Receipt: ANSI stripped, valid JSON
  Loop 1.2.3: Test cache: same input twice → identical JSON output
    → Receipt: determinism confirmed
```

### I2 Intra: Overlay Window (Full Conversation + Theme)

```
Step 2.1: Tkinter shell with Terminus theme
  Loop 2.1.1: root = Tk(), overrideredirect(True), topmost(True), alpha(0.85)
  Loop 2.1.2: root['bg'] = '#0a0a0f'
    → Receipt: window appears borderless, on top, semi-transparent, void black

Step 2.2: Scrollable conversation text widget
  Loop 2.2.1: tk.Text + tk.Scrollbar, font=('DejaVu Sans Mono', 11), bg='#0a0a0f', fg='#e8e6e3'
  Loop 2.2.2: text['state'] = 'disabled' (read-only)
  Loop 2.2.3: configure tag "operator" with foreground='#ff6b9d'
  Loop 2.2.4: configure tag "assistant" with foreground='#e8e6e3', lmargin1=20, lmargin2=20
  Loop 2.2.5: configure tag "thinking_toggle" with foreground='#40d8e0', underline=True
    → Receipt: text widget renders with correct theme colors and indentation

Step 2.3: FIFO JSON reader thread
  Loop 2.3.1: threading.Thread(target=read_fifo, daemon=True)
    → Receipt: thread starts without blocking GUI
  Loop 2.3.2: open /tmp/trans_fifo, json.loads each line
    → Receipt: valid JSON parsed
  Loop 2.3.3: append message with role-based tag and color
    → Receipt: operator in pink, assistant indented in white
  Loop 2.3.4: if "thinking" field is non-null → insert clickable "🧠 Show reasoning" tag
    → Receipt: thinking toggle appears in cyan
  Loop 2.3.5: on thinking tag click → expand/collapse thinking text block
    → Receipt: expand shows reasoning, collapse hides it
  Loop 2.3.6: FIFO disconnect → show "⏳ Waiting..." retry every 3s
    → Receipt: reconnects automatically

Step 2.4: Message limit + auto-scroll
  Loop 2.4.1: max_messages=200, delete oldest when exceeded
  Loop 2.4.2: text.see('end') on each new message
    → Receipt: scrollable, always shows latest

Step 2.5: Chart/structured block rendering
  Loop 2.5.1: If message has "chart" field → create tk.Canvas below text area
  Loop 2.5.2: Render boxes/lines in cyan (#40d8e0) and gold (#ffb347) on void bg
    → Receipt: U-KSL summaries render as visual charts
```

### I3 Intra: Hover Toolbar (Terminus-styled)

```
Step 3.1: Toolbar frame
  Loop 3.1.1: Frame at top, bg='#1a0f2e', highlightbackground='#ff6b9d', highlightthickness=1
  Loop 3.1.2: <Enter> on root → show, <Leave> → hide (500ms delay)
    → Receipt: toolbar fades in/out with pink glow border

Step 3.2: Opacity slider
  Loop 3.2.1: Scale from 0.2 to 1.0, step 0.05, bg='#1a0f2e', troughcolor='#252535'
    → Receipt: slider styled to theme

Step 3.3: Show Bounds toggle
  Loop 3.3.1: Canvas rectangle dash=(6,4), outline='#ff6b9d', width=2
    → Receipt: pink dashed border toggles

Step 3.4: Drag handle
  Loop 3.4.1: Label "≡" fg='#ffb347', bind <Button-1> + <B1-Motion>
    → Receipt: gold handle, window follows mouse

Step 3.5: Close button
  Loop 3.5.1: Label "×" fg='#ff6b9d', bind <Button-1> → root.destroy()
    → Receipt: pink X, clean exit
```

### I4 Intra: Alignment & Snap

```
Step 4.1: Show Bounds toggle (see I3.3)
  Loop 4.1.1: Canvas overlay for dashed border → Receipt: toggles cleanly

Step 4.2: Auto-snap (Linux)
  Loop 4.2.1: xdotool search --name "DeepSeek|deepseek|terminal|LM Studio"
    → Receipt: window ID found
  Loop 4.2.2: xdotool getwindowgeometry $WID → w, h, x, y parsed
  Loop 4.2.3: root.geometry(f'{w}x{h}+{x}+{y}')
    → Receipt: overlay matches terminal bounds
  Loop 4.2.4: Show bounds for 2s after snap → auto-hide

Step 4.3: Auto-snap (Windows) — optional, gated behind pywin32

Step 4.4: Position persistence
  Loop 4.4.1: Save last position + opacity to ~/.cli-overlay/config.json
  Loop 4.4.2: Restore on launch
```

### I5 Intra: State & Replay + Training Trace

```
Step 5.1: State manager
  Loop 5.1.1: On start: generate session_id = {date}T{time}-{random6}
  Loop 5.1.2: Create ~/.cli-overlay/ directory if missing
  Loop 5.1.3: Open state-{session_id}.json for append
    → Receipt: state file created at overlay start

Step 5.2: Message capture
  Loop 5.2.1: For each FIFO message, write JSON line to state file
  Loop 5.2.2: On close: write session_end marker with message_count, duration_sec
    → Receipt: full session preserved

Step 5.3: Replay script (replay.py)
  Loop 5.3.1: Parse state file → iterate messages → feed to overlay via FIFO with configurable speed
  Loop 5.3.2: Fast-forward mode: skip delays, emit all instantly
    → Receipt: replay.py reproduces session

Step 5.4: Training trace export (export_training_trace.py)
  Loop 5.4.1: Read state file → convert to JSONL with training tags
  Loop 5.4.2: Each line: {"session_id","exchange_index","role","original","translation","thinking","model","tags"}
    → Receipt: valid JSONL for ML pipeline
```

### I6 Intra: Config & Packaging

```
Step 6.1: Config manager
  Loop 6.1.1: Read/write ~/.cli-overlay/config.json (position, opacity, fifo_path, lm_studio_port)
  Loop 6.1.2: Defaults on first launch, restore on subsequent, reset on corrupt
    → Receipt: config persists

Step 6.2: Makefile (clean/validate/test/package/public-docs-check/handoff/sku/receipt)
  → Receipt: all targets work

Step 6.3: SKILL.md (Premium Skill Builder format)
  → Receipt: passes validate_skill_bundle.py

Step 6.4: Storefront (short-description, long-description, faq, buyer-message)
  → Receipt: all files present with claim boundary wording

Step 6.5: Agents config (cli-translation-overlay.yaml)
  → Receipt: use_when/principles/entrypoints complete

Step 6.6: Tests (test_bundle.py, test_i18n.py, test_translate.py)
  → Receipt: 10+ tests pass

Step 6.7: Receipt (build_final_receipt.py)
  → Receipt: final_receipt.json with allowed/blocked claims
```

### I7 Intra: Bidirectional Prompt Translation

```
Step 7.1: LM Studio / Ollama client
  Loop 7.1.1: Detect available service (LM Studio at localhost:1234, Ollama at localhost:11434)
  Loop 7.1.2: Build translation prompt function: system="You are a translator. Translate English to natural Chinese. Output ONLY the translation.", user=operator_text
    → Receipt: prompt template ready
  Loop 7.1.3: Send warmup request at startup (empty prompt)
    → Receipt: model connection confirmed

Step 7.2: Entry widget (I7 input)
  Loop 7.2.1: tk.Entry at bottom of overlay, bg='#111118', fg='#e8e6e3', highlightcolor='#ffb347'
  Loop 7.2.2: Initially hidden, fade in when mouse within 50px of bottom
    → Receipt: gold-bordered entry appears on approach

Step 7.3: Translation flow
  Loop 7.3.1: Operator types → Enter → send to LM Studio
  Loop 7.3.2: On response: trim to Chinese text, display in conversation as operator message
  Loop 7.3.3: Write Chinese to /tmp/op_trans_fifo for CLI pipeline bridge
    → Receipt: Chinese text correctly injected
  Loop 7.3.4: On timeout (15s) or error → fallback to Ollama → fallback to Google Translate
    → Receipt: tier fallback works
  Loop 7.3.5: Entry clears, fades out after 3s idle
    → Receipt: clean UX transition

Step 7.4: Tier health check
  Loop 7.4.1: Periodic ping to LM Studio every 60s; if down, switch tier indicator in toolbar
    → Receipt: operator always knows which translation tier is active
```

---

## 6. Infra Stage 3: Verify Each Local Lane

| Lane | Verification | Pass Criteria |
|------|-------------|---------------|
| I1 | `python3 translator.py` with test input | Outputs correct JSON + deterministic cache hit on second call |
| I2 | Manual: run overlay, write JSON to FIFO | Full conversation visible, thinking dropdown works, Terminus theme renders correctly, scrollable |
| I3 | Manual: hover, slide, toggle, drag, close | All interactions work, colors match theme |
| I4 | Manual: click "Snap Align", verify bounds | Overlay snaps to terminal, pink dashed bounds render |
| I5 | Check state file exists + replay.py reproduces | State saved at start, replay reproduces messages, JSONL export valid |
| I6 | `make validate && make test` | All pass, SKILL.md valid, receipts emit |
| I7 | "Hello" → model → Chinese output; tier fallback test | Translation correct, fallback chain works, Entry fades in/out |

A local pass means: **This Infra lane may be presented to Ultra Stage 3 for composition judgment.**

---

## 7. Ultra Stage 3: Composition Verification

**Ask:**
- Do all 7 Infra outputs compose into a single running program?
  → I1 feeds I2 via FIFO ✓
  → I3 is embedded in I2 ✓
  → I4 commands I2 ✓
  → I5 persists state from I2 feed ✓
  → I7 translates prompts from I2 Entry → CLI ✓
  → I6 wraps it all ✓
- Does the made thing satisfy the Ultra?
  → Full conversation scrollable (Operator + Assistant) ✓
  → Terminus theme rendered correctly ✓
  → Thinking trace collapsible dropdown ✓
  → State saved at every start, replayable ✓
  → Training trace exportable as JSONL ✓
  → Bidirectional translation (English → Chinese) via local DeepSeek ✓
  → Tier fallback (LM Studio → Ollama → Google Translate) ✓
  → Opacity slider ✓
  → Alignment verification ✓
  → Auto-snap ✓
  → Charts/graphs render ✓
  → HUD entry fades on mouse approach ✓
- Did any branch become vestigial? → No
- Did any local success become a false global claim?
  → Windows auto-snap is optional, documented as such ✓
- Are receipts present? → final_receipt.json ✓
- Is coherence evidenced? → All tests pass ✓

**Decision:**
- **Pass** → Ultra Goal → Ultra Structure. System exits clean.
- **Fail** → Return to owning Stage 1 via Recursive Healing.

---

## 8. Recursive Healing

If any verification fails:

1. Identify the owning Stage 1:
   - FIFO not reading or cache miss → I1 Stage 1
   - Window not appearing, conversation not ordered, thinking not toggling, theme colors wrong → I2 Stage 1
   - Slider, bounds, drag not working, toolbar styling off → I3 Stage 1
   - Snap off by 10px → I4 Stage 1
   - State file missing or replay broken → I5 Stage 1
   - Translation wrong, tier not falling back, Entry not appearing → I7 Stage 1
   - Makefile target fails, SKILL.md invalid → I6 Stage 1

2. The owning Stage 1 maps the deficiency as a repair objective.

3. The repair enters Stage 2 traversal.

4. Stage 3 verifies the repair.

5. Repeat until the structure verifies, the route is remapped, or the work is preserved and archived as evidence.

```
Verify fails.
Return to owning Stage 1.
Map the repair.
Traverse the repair.
Verify again.
```

---

## 9. Receipt

The final delivery receipt for this U-KSL is `final_receipt.json`, which records:

```json
{
  "package_name": "cli-translation-overlay",
  "version": "v0.1.0-rc1",
  "allowed_claims": [
    "runnable_skill_mvp",
    "release_candidate",
    "public_sku_ready",
    "public_beta_handoff_ready"
  ],
  "blocked_claims": [
    "release_ready",
    "secure",
    "safe_to_execute_without_review",
    "no_unknown_attacks",
    "vulnerability_free"
  ],
  "checks_run": [
    "translator_compile",
    "deterministic_cache",
    "overlay_full_conversation",
    "terminus_theme_rendered",
    "thinking_trace_dropdown",
    "toolbar_interaction",
    "alignment_snap",
    "state_save_replay",
    "training_trace_export",
    "bidirectional_translation",
    "tier_fallback",
    "config_persistence",
    "bundle_validation"
  ],
  "known_limits": [
    "Windows auto-snap requires pywin32 (documented, gated)",
    "macOS uses manual alignment only",
    "Translation quality depends on Google Translate (free tier)",
    "Thinking trace capture works only if the model emits thinking tokens",
    "State files grow with session length — archive old sessions manually",
    "Bidirectional translation requires at least one model backend running (LM Studio or Ollama)",
    "LM Studio context/temperature settings are user-controlled — translation quality varies accordingly",
    "release_ready remains blocked without production-readiness receipts"
  ]
}
```

---

## U-KSL Visual Summary

```
┌─────────────────────────────────────────────────┐
│  U-KSL: CLI Translation Overlay                 │
│  Stage 1 maps → Stage 2 traverses → Stage 3     │
│  verifies → Recursive Healing if needed         │
├─────────────────────────────────────────────────┤
│                                                  │
│  Ultra Goal: HUD translation overlay —             │
│  Full conversation + thinking + bidirectional       │
│  prompt translation + state replay + trace export   │
│  Theme: hot pink #ff6b9d / purple #9b59f0 /        │
│         cyan #40d8e0 / gold #ffb347 / void #0a0a0f │
│                                                     │
│  ├─ I1: Translation Pipeline (deterministic cache) │
│  │   ├─ S1: Map  ├─ S2: Traverse  ├─ S3: Verify   │
│  │                                                  │
│  ├─ I2: Overlay Window (Full Conversation + Theme) │
│  │   ├─ S1: Map  ├─ S2: Traverse  ├─ S3: Verify   │
│  │                                                  │
│  ├─ I3: Hover Toolbar (Terminus-styled)            │
│  │   ├─ S1: Map  ├─ S2: Traverse  ├─ S3: Verify   │
│  │                                                  │
│  ├─ I4: Alignment & Snap                           │
│  │   ├─ S1: Map  ├─ S2: Traverse  ├─ S3: Verify   │
│  │                                                  │
│  ├─ I5: State & Replay + Training Trace            │
│  │   ├─ S1: Map  ├─ S2: Traverse  ├─ S3: Verify   │
│  │                                                  │
│  ├─ I6: Config & Packaging                         │
│  │   ├─ S1: Map  ├─ S2: Traverse  ├─ S3: Verify   │
│  │                                                  │
│  └─ I7: Bidirectional Prompt Translation           │
│      ├─ S1: Map (LM Studio → Ollama → GT fallback) │
│      ├─ S2: Traverse (Entry widget + model call)   │
│      └─ S3: Verify (translation + tier fallback)   │
│                                                     │
│  Ultra Stage 3: Composition Verification            │
│  → All 7 lanes compose?                             │
│  → Full conv + theme + thinking + state +           │
│    bidirectional + trace + snap + receipts?         │
│  → Pass → Structure. Fail → Recursive Healing.      │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

*Generated 2026-06-28. U-KSL v0.3, Core Canon v0.3. Terminus Protocol. Built with DeepSeek R1 1.5B bidirectional translation.*
